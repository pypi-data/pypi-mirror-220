from fs import open_fs
from fs.path import dirname
from PIL import Image, ImageOps
from flask import current_app
import psycopg
import traceback
from psycopg.types.json import Jsonb
from psycopg.errors import UniqueViolation
from . import pictures, utils, errors
from geopic_tag_reader import reader
from dataclasses import asdict, dataclass
import logging
from contextlib import contextmanager
from enum import Enum
from typing import Any
import threading

log = logging.getLogger("geovisio.runner_pictures")


class PictureBackgroundProcessor(object):
    def init_app(self, app):
        nb_threads = app.config["EXECUTOR_MAX_WORKERS"]
        self.enabled = nb_threads != 0

        if self.enabled:
            from flask_executor import Executor

            self.executor = Executor(app, name="PicProcessor")
        else:
            import sys

            if "run" in sys.argv or "waitress" in sys.argv:  # hack not to display a frightening warning uselessly
                log.warning("No picture background processor run, no picture will be processed unless another separate worker is run")
                log.warning("A separate process can be run with:")
                log.warning("flask picture-worker")

    def process_pictures(self):
        """
        Ask for a background picture process that will run until not pictures need to be processed
        """
        if self.enabled:
            worker = PictureProcessor(config=current_app.config)
            return self.executor.submit(worker.process_next_pictures)


background_processor = PictureBackgroundProcessor()


def setSequencesHeadings(sequences, value, overwrite):
    with psycopg.connect(current_app.config["DB_URL"], autocommit=True) as db:
        if len(sequences) == 0:
            log.info("Updating all sequences")
            sequences = [r[0] for r in db.execute("SELECT id FROM sequences").fetchall()]

        for seq in sequences:
            updateSequenceHeadings(db, seq, value, not overwrite)

        log.info("Done processing %s sequences" % len(sequences))


def cleanup(sequences=[], full=False, database=False, cache=False, permanentPics=False):
    """Cleans up various data or files of GeoVisio

    Parameters
    ----------
    sequences : list
            List of sequences IDs to clean-up. If none is given, all sequences are cleaned up.
    full : bool
            For full cleaning (deletes DB entries and derivates files including blur masks)
    database : bool
            For removing database entries without deleting derivates files
    cache : bool
            For removing derivates files
    permanentPics : bool
            For removing original picture file
    """

    if full:
        database = True
        cache = True
        permanentPics = True

    if database is False and cache is False and permanentPics is False:
        return True

    allSequences = len(sequences) == 0

    with psycopg.connect(current_app.config["DB_URL"], autocommit=True) as conn:
        fses = current_app.config["FILESYSTEMS"]
        if allSequences:
            pics = [str(p[0]) for p in conn.execute("SELECT id FROM pictures").fetchall()]
        else:
            # Find pictures in sequences to cleanup
            pics = [
                str(p[0])
                for p in conn.execute(
                    """
				WITH pic2rm AS (
					SELECT DISTINCT pic_id FROM sequences_pictures WHERE seq_id = ANY(%(seq)s)
				)
				SELECT * FROM pic2rm
				EXCEPT
				SELECT DISTINCT pic_id FROM sequences_pictures WHERE pic_id IN (SELECT * FROM pic2rm) AND seq_id != ANY(%(seq)s)
			""",
                    {"seq": sequences},
                ).fetchall()
            ]

        if database:
            log.info("Cleaning up database...")
            if allSequences:
                conn.execute("DELETE FROM pictures_to_process")
                conn.execute("DELETE FROM sequences_pictures")
                conn.execute("DELETE FROM sequences")
                conn.execute("DELETE FROM pictures")
            else:
                conn.execute("DELETE FROM pictures_to_process WHERE picture_id = ANY(%s)", [pics])
                conn.execute("DELETE FROM sequences_pictures WHERE seq_id = ANY(%s)", [sequences])
                conn.execute("DELETE FROM sequences WHERE id = ANY(%s)", [sequences])
                conn.execute("DELETE FROM pictures WHERE id = ANY(%s)", [pics])

            conn.close()

        if permanentPics:
            log.info("Cleaning up original files...")
            if allSequences:
                utils.removeFsTreeEvenNotFound(fses.permanent, "/")
            else:
                for picId in pics:
                    utils.removeFsTreeEvenNotFound(fses.permanent, dirname(pictures.getHDPicturePath(picId)))

        if cache:
            log.info("Cleaning up derivates files...")
            if allSequences:
                utils.removeFsTreeEvenNotFound(fses.derivates, "/")
            else:
                for picId in pics:
                    picPath = pictures.getPictureFolderPath(picId)
                    # Many paths are not used anymore in GeoVisio >= 2.0.0
                    # But are kept for retrocompatibility
                    utils.removeFsEvenNotFound(fses.derivates, picPath + "/blurred.webp")
                    utils.removeFsEvenNotFound(fses.derivates, picPath + "/thumb.webp")
                    utils.removeFsEvenNotFound(fses.derivates, picPath + "/sd.webp")
                    utils.removeFsTreeEvenNotFound(fses.derivates, picPath + "/tiles")
                    utils.removeFsEvenNotFound(fses.derivates, picPath + "/blurred.jpg")
                    utils.removeFsEvenNotFound(fses.derivates, picPath + "/thumb.jpg")
                    utils.removeFsEvenNotFound(fses.derivates, picPath + "/sd.jpg")
                    utils.removeFsEvenNotFound(fses.derivates, picPath + "/progressive.jpg")
                    utils.removeFsEvenNotFound(fses.derivates, picPath + "/blur_mask.png")

                    if fses.derivates.isdir(picPath) and fses.derivates.isempty(picPath):
                        fses.derivates.removedir(picPath)

        # Remove empty group of pictures folders
        if cache or permanentPics:
            for fs in [fses.tmp, fses.derivates, fses.permanent]:
                for picDir in fs.walk.dirs(search="depth"):
                    if fs.isempty(picDir):
                        fs.removedir(picDir)

    log.info("Cleanup done")
    return True


def insertNewPictureInDatabase(db, sequenceId, position, picture, associatedAccountID, addtionalMetadata):
    """Inserts a new 'pictures' entry in the database, from a picture file.
    Database is not committed in this function, to make entry definitively stored
    you have to call db.commit() after or use an autocommit connection.
    Also, picture is by default in state "preparing", so you may want to update
    this as well after function run.

    Parameters
    ----------
    db : psycopg.Connection
            Database connection
    position : int
            Position of picture in sequence
    picture : PIL.Image
            Image file in Pillow format
    associatedAccountId : str
            Identifier of the author account
    isBlurred : bool
            Was the picture blurred by its author ? (defaults to false)

    Returns
    -------
    uuid : The uuid of the new picture entry in the database
    """

    # Create a fully-featured metadata object
    metadata = readPictureMetadata(picture, True) | pictures.getPictureSizing(picture) | addtionalMetadata

    # Remove cols/rows information for flat pictures
    if metadata["type"] == "flat":
        metadata.pop("cols")
        metadata.pop("rows")

    # Create a lighter metadata field to remove duplicates fields
    lighterMetadata = dict(filter(lambda v: v[0] not in ["ts", "heading", "lon", "lat", "exif"], metadata.items()))
    if lighterMetadata.get("tagreader_warnings") is not None and len(lighterMetadata["tagreader_warnings"]) == 0:
        del lighterMetadata["tagreader_warnings"]

    with db.transaction():
        # Add picture metadata to database
        picId = db.execute(
            """
			INSERT INTO pictures (ts, heading, metadata, geom, account_id, exif)
			VALUES (to_timestamp(%s), %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326), %s, %s)
			RETURNING id
		""",
            (
                metadata["ts"],
                metadata["heading"],
                Jsonb(lighterMetadata),
                metadata["lon"],
                metadata["lat"],
                associatedAccountID,
                Jsonb(metadata["exif"]),
            ),
        ).fetchone()[0]

        # Process field of view for each pictures
        # Flat pictures = variable fov
        if metadata["type"] == "flat":
            make, model = metadata.get("make"), metadata.get("model")
            if make is not None and model is not None:
                db.execute("SET pg_trgm.similarity_threshold = 0.9")
                db.execute(
                    """
					UPDATE pictures
					SET metadata = jsonb_set(metadata, '{field_of_view}'::text[], COALESCE(
						(
							SELECT ROUND(DEGREES(2 * ATAN(sensor_width / (2 * (metadata->>'focal_length')::float))))::varchar
							FROM cameras
							WHERE model %% CONCAT(%(make)s::text, ' ', %(model)s::text)
							ORDER BY model <-> CONCAT(%(make)s::text, ' ', %(model)s::text)
							LIMIT 1
						),
						'null'
					)::jsonb)
					WHERE id = %(id)s
				""",
                    {"id": picId, "make": make, "model": model},
                )

        # 360 pictures = 360° fov
        else:
            db.execute(
                """
				UPDATE pictures
				SET metadata = jsonb_set(metadata, '{field_of_view}'::text[], '360'::jsonb)
    			WHERE id = %s
			""",
                [picId],
            )

        try:
            db.execute("INSERT INTO sequences_pictures(seq_id, rank, pic_id) VALUES(%s, %s, %s)", [sequenceId, position, picId])
        except UniqueViolation as e:
            raise PicturePositionConflict() from e

    return picId


def updateSequenceHeadings(db, sequenceId, relativeHeading=0, updateOnlyMissing=True):
    """Defines pictures heading according to sequence path.
    Database is not committed in this function, to make entry definitively stored
    you have to call db.commit() after or use an autocommit connection.

    Parameters
    ----------
    db : psycopg.Connection
            Database connection
    sequenceId : uuid
            The sequence's uuid, as stored in the database
    relativeHeading : int
            Camera relative orientation compared to path, in degrees clockwise.
            Example: 0° = looking forward, 90° = looking to right, 180° = looking backward, -90° = looking left.
    updateOnlyMissing : bool
            If true, doesn't change existing heading values in database
    """

    db.execute(
        """
		WITH h AS (
			SELECT
				p.id,
				CASE
					WHEN LEAD(sp.rank) OVER othpics IS NULL AND LAG(sp.rank) OVER othpics IS NULL
						THEN NULL
					WHEN LEAD(sp.rank) OVER othpics IS NULL
						THEN (360 + FLOOR(DEGREES(ST_Azimuth(LAG(p.geom) OVER othpics, p.geom)))::int + (%(diff)s %% 360)) %% 360
					ELSE
						(360 + FLOOR(DEGREES(ST_Azimuth(p.geom, LEAD(p.geom) OVER othpics)))::int + (%(diff)s %% 360)) %% 360
				END AS heading
			FROM pictures p
			JOIN sequences_pictures sp ON sp.pic_id = p.id AND sp.seq_id = %(seq)s
			WINDOW othpics AS (ORDER BY sp.rank)
		)
		UPDATE pictures p
		SET heading = h.heading, heading_computed = true
		FROM h
		WHERE h.id = p.id
		"""
        + (
            " AND (p.heading IS NULL OR p.heading = 0 OR p.heading_computed)" if updateOnlyMissing else ""
        ),  # lots of camera have heading set to 0 for unset heading, so we recompute the heading when it's 0 too, even if this could be a valid value
        {"seq": sequenceId, "diff": relativeHeading},
    )


def processPictureFiles(db, dbPic, config):
    """Generates the files associated with a sequence picture.

    If needed the image is blurred before the tiles and thumbnail are generated.

    Parameters
    ----------
    db : psycopg.Connection
            Database connection
    dbPic : DbPicture
            The picture metadata extracted from database
    config : dict
            Flask app.config (passed as param to allow using ThreadPoolExecutor)
    """

    skipBlur = dbPic.isBlurred or config.get("API_BLUR_URL") == None
    fses = config["FILESYSTEMS"]
    fs = fses.permanent if skipBlur else fses.tmp
    picHdPath = pictures.getHDPicturePath(dbPic.id)

    with fs.openbin(picHdPath) as pictureBytes:
        picture = Image.open(pictureBytes)
        metadata = readPictureMetadata(picture) | pictures.getPictureSizing(picture)

        # Create picture folders for this specific picture
        picDerivatesFolder = pictures.getPictureFolderPath(dbPic.id)
        fses.derivates.makedirs(picDerivatesFolder, recreate=True)
        fses.permanent.makedirs(dirname(picHdPath), recreate=True)

        # Create blurred version if required
        if not skipBlur:
            _set_status(db, dbPic.id, "preparing-blur")
            try:
                picture = pictures.createBlurredHDPicture(fses.permanent, config.get("API_BLUR_URL"), pictureBytes, picHdPath)
            except Exception as e:
                logging.exception(e)
                raise Exception("Blur API failure: " + errors.getMessageFromException(e)) from e

            # Delete original unblurred file
            utils.removeFsEvenNotFound(fses.tmp, picHdPath)

            # Cleanup parent folders
            parentFolders = picHdPath.split("/")
            parentFolders.pop()
            checkFolder = parentFolders.pop()
            while checkFolder:
                currentFolder = "/".join(parentFolders) + "/" + checkFolder
                if fses.tmp.isempty(currentFolder):
                    utils.removeFsTreeEvenNotFound(fses.tmp, currentFolder)
                    checkFolder = parentFolders.pop()
                else:
                    checkFolder = False

        else:
            # Make sure image rotation is always applied
            #  -> Not necessary on pictures from blur API, as SGBlur ensures rotation is always applied
            picture = ImageOps.exif_transpose(picture)

        _set_status(db, dbPic.id, "preparing-derivates")

        # Always pre-generate thumbnail
        pictures.createThumbPicture(fses.derivates, picture, picDerivatesFolder + "/thumb.jpg", metadata["type"])

        # Create SD and tiles
        if config.get("PICTURE_PROCESS_DERIVATES_STRATEGY") == "PREPROCESS":
            pictures.generatePictureDerivates(fses.derivates, picture, metadata, picDerivatesFolder, metadata["type"], skipThumbnail=True)


def readPictureMetadata(picture, fullExif=False):
    """Extracts metadata from picture file

    Parameters
    ----------
    picture : PIL.Image
            Picture file
    fullExif : bool
            Embed full EXIF metadata in given result (defaults to False)

    Returns
    -------
    dict
            Various metadata fields : lat, lon, ts, heading, type, make, model, focal_length
    """

    try:
        metadata = asdict(reader.readPictureMetadata(picture))
    except Exception as e:
        raise MetadataReadingError(details=str(e))

    if not fullExif:
        metadata.pop("exif")
    else:
        # Cleanup raw EXIF tags to avoid SQL issues
        cleanedExif = dict()

        for k, v in metadata["exif"].items():
            try:
                if isinstance(v, bytes):
                    try:
                        cleanedExif[k] = v.decode("utf-8").replace("\x00", "")
                    except UnicodeDecodeError:
                        cleanedExif[k] = str(v).replace("\x00", "")
                elif isinstance(v, str):
                    cleanedExif[k] = v.replace("\x00", "")
                else:
                    try:
                        cleanedExif[k] = str(v)
                    except:
                        log.warning("Unsupported EXIF tag conversion: " + k + " " + str(type(v)))
            except:
                log.exception("Can't read EXIF tag: " + k + " " + str(type(v)))

        metadata["exif"] = cleanedExif

    return metadata


def printPictureProcessingError(e, sequenceFolder, pictureFilename):
    """Prints a decorated error on stdout.

    Parameters
    ----------
    e : Error
            The error that caused the processing to stop
    sequenceFolder : str
            The sequence folder containing the picture that broke
    pictureFilename : str
            The picture's file name that couldn't be processed
    """
    log.info("")
    log.info("---------------------------------------------------------")
    log.info("WARNING : an error occured while processing picture '%s/%s'" % (sequenceFolder, pictureFilename))
    log.info("".join(traceback.format_exception(type(e), e, e.__traceback__)))
    log.info("---------------------------------------------------------")
    log.info("")


def createSequence(metadata, accountId) -> str:
    with psycopg.connect(current_app.config["DB_URL"]) as conn:
        with conn.cursor() as cursor:
            # Add sequence in database
            seqId = cursor.execute(
                "INSERT INTO sequences(account_id, metadata) VALUES(%s, %s) RETURNING id", [accountId, Jsonb(metadata)]
            ).fetchone()

            # Make changes definitive in database
            conn.commit()

            if seqId is None:
                raise Exception(f"impossible to insert sequence in database")
            return seqId[0]


class RecoverableProcessException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class PicturePositionConflict(Exception):
    def __init__(self):
        super().__init__()


class MetadataReadingError(Exception):
    def __init__(self, details):
        super().__init__()
        self.details = details


class PictureProcessor:
    stop: bool
    config: dict[Any, Any]

    def __init__(self, config, stop=True) -> None:
        self.config = config
        self.stop = stop
        if threading.current_thread() is threading.main_thread():
            # if worker is in daemon mode, register signals to gracefully stop it
            self._register_signals()

    def process_next_pictures(self):
        try:
            while True:
                r = process_next_picture(self.config)
                if self.stop:
                    return
                if not r:
                    # no more picture to process
                    # wait a bit until there are some
                    import time

                    time.sleep(1)

        except:
            log.exception("Exiting thread")

    def _register_signals(self):
        import signal

        signal.signal(signal.SIGINT, self._graceful_shutdown)
        signal.signal(signal.SIGTERM, self._graceful_shutdown)

    def _graceful_shutdown(self, *args):
        log.info("Stoping worker, waiting for last picture processing to finish...")
        self.stop = True


class ProcessTask(str, Enum):
    prepare = "prepare"
    delete = "delete"


@dataclass
class DbPicture:
    id: str
    isBlurred: bool
    task: ProcessTask


def process_next_picture(config):
    with _get_next_picture_to_process(config) as db_pic:
        if db_pic is None:
            return False
        if db_pic.task == ProcessTask.prepare:
            with utils.log_elapsed(f"Processing picture {db_pic.id}"), psycopg.connect(config["DB_URL"], autocommit=True) as db:
                # open another connection for reporting and queries
                _process_picture(db, config, db_pic)
        elif db_pic.task == ProcessTask.delete:
            with utils.log_elapsed(f"Deleting picture {db_pic.id}"), psycopg.connect(config["DB_URL"], autocommit=True) as db:
                _delete_picture(db_pic)
        else:
            raise RecoverableProcessException(f"Unhandled process task: {db_pic.task}")

        return True


@contextmanager
def _get_next_picture_to_process(config):
    """
    Open a new connection and return the next picture to process
    Note: the picture should be used as a context manager to close the connection when we stop using the returned picture.

    The new connection is needed because we lock the `pictures_to_process` for the whole transaction for another worker not to process the same picture
    """
    with psycopg.connect(config["DB_URL"]) as locking_transaction:
        r = locking_transaction.execute(
            """
		SELECT p.id, COALESCE((p.metadata->>'blurredByAuthor')::boolean, false), pictures_to_process.task
			FROM pictures_to_process
			JOIN pictures p ON p.id = pictures_to_process.picture_id
			ORDER by
				p.nb_errors,
				CASE
					WHEN p.status = 'waiting-for-process' THEN 0
					WHEN p.status = 'waiting-for-delete' THEN 0
					WHEN p.status::text LIKE 'preparing%' THEN 1
				END,
				pictures_to_process.ts
			FOR UPDATE of pictures_to_process SKIP LOCKED
			LIMIT 1
		"""
        ).fetchone()
        if r is None:
            # Nothing to process
            yield None
        else:
            log.debug(f"Processing {r[0]}")

            db_pic = DbPicture(id=str(r[0]), isBlurred=r[1], task=r[2])
            try:
                yield db_pic

                # Finalize the picture process, set the picture status and remove the picture from the queue process
                _finalize_picture_process(locking_transaction, db_pic)
                log.debug(f"Picture {db_pic.id} processed")
            except RecoverableProcessException as e:
                log.exception(f"Impossible to process picture {db_pic.id} for the moment")
                _mark_process_as_error(locking_transaction, db_pic, e, recoverable=True)
                locking_transaction.commit()
            except InterruptedError as interruption:
                log.error(f"Interruption received, stoping process of picture {db_pic.id}")
                # starts a new connection, since the current one can be corrupted by the exception
                with psycopg.connect(config["DB_URL"], autocommit=True) as t:
                    _mark_process_as_error(t, db_pic, interruption, recoverable=True)
                raise interruption
            except Exception as e:
                log.exception(f"Impossible to process picture {db_pic.id}")
                _mark_process_as_error(locking_transaction, db_pic, e, recoverable=False)
                locking_transaction.commit()
                raise e


def _process_picture(db, config, db_pic: DbPicture):
    _start_process(db, db_pic)

    try:
        processPictureFiles(db, db_pic, config)
        _set_status(db, db_pic.id, "ready")
    finally:
        _finalize_sequence_if_last_picture(db, db_pic)


def _finalize_picture_process(db, pic: DbPicture):
    db.execute(
        """
		DELETE FROM pictures_to_process WHERE picture_id = %(id)s
   		""",
        {"id": pic.id},
    )
    if pic.task == ProcessTask.delete:
        # for picture deletion, we also cleanup the picture from the database
        db.execute("DELETE FROM pictures WHERE id = %s", [pic.id])


def _set_status(db, pic_id: str, status: str):
    db.execute("UPDATE pictures SET status = %s WHERE id = %s", [status, pic_id])


def _start_process(db, pic: DbPicture):
    db.execute(
        """
	UPDATE pictures SET
		status = 'preparing',
		processed_at = NOW()
	WHERE id = %(id)s
	""",
        {"id": pic.id},
    )


def _mark_process_as_error(db, db_pic: DbPicture, e: Exception, recoverable: bool = False):
    if recoverable:
        db.execute(
            """
			UPDATE pictures SET
				status = 'waiting-for-process',
				nb_errors = nb_errors + 1,
				process_error = %(err)s
			WHERE id = %(id)s
			""",
            {"err": str(e), "id": db_pic.id},
        )
    else:
        # on unrecoverable error, we remove the picture from the queue to process
        db.execute(
            """
			WITH pic_to_process_update AS (
				DELETE FROM pictures_to_process
				WHERE picture_id = %(id)s
			)
			UPDATE pictures SET
				status = 'broken',
				nb_errors = nb_errors + 1,
				process_error = %(err)s
			WHERE id = %(id)s
			""",
            {"err": str(e), "id": db_pic.id},
        )


def _finalize_sequence_if_last_picture(db, db_pic: DbPicture):
    r = db.execute(
        """
		SELECT sp.seq_id AS id FROM sequences_pictures AS sp
		WHERE sp.pic_id = %(id)s
	""",
        {"id": db_pic.id},
    ).fetchone()
    if not r:
        raise Exception(f"impossible to find sequence associated to picture {db_pic.id}")

    seqId = r[0]

    is_sequence_finalized = _is_sequence_finalized(db, seqId)
    if not is_sequence_finalized:
        log.debug("sequence not finalized")
        return
    log.debug(f"Finalizing sequence {seqId}")

    with utils.log_elapsed(f"Finalizing sequence {seqId}"):
        # Complete missing headings in pictures
        updateSequenceHeadings(db, seqId)

        # Change sequence database status in DB
        db.execute(
            """
			UPDATE sequences
			SET status = 'ready', geom = ST_MakeLine(ARRAY(
				SELECT p.geom
				FROM sequences_pictures sp
				JOIN pictures p ON sp.pic_id = p.id
				WHERE sp.seq_id = %(seq)s
				ORDER BY sp.rank
			))
			WHERE id = %(seq)s
		""",
            {"seq": seqId},
        )

        log.info(f"Sequence {seqId} is ready")


def _is_sequence_finalized(db, seq_id: str):
    statuses = db.execute(
        """
		SELECT p.status FROM pictures p
		JOIN sequences_pictures sp ON sp.pic_id = p.id
		WHERE sp.seq_id = %(id)s
  		;
	""",
        {"id": seq_id},
    ).fetchall()

    for s in statuses:
        if s[0] == "waiting-for-process" or s[0].startswith("preparing"):
            return False
    return True


def _delete_picture(db_pic: DbPicture):
    """Delete a picture from the filesystem"""
    log.debug(f"Deleting picture files {db_pic.id}")
    pictures.removeAllFiles(db_pic.id)
