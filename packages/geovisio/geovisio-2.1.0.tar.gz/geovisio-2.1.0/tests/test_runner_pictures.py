import time
import os
import pytest
import psycopg
import re
import io
from uuid import UUID
from psycopg.rows import dict_row
from PIL import Image
from fs import open_fs
from . import conftest
from . import test_pictures
from geovisio import runner_pictures, pictures, filesystems, create_app

FIXTURE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")


@conftest.SEQ_IMGS
@conftest.SEQ_IMGS_FLAT
@pytest.mark.parametrize(
    ("singleSeq", "full", "db", "cache", "original"),
    (
        (True, False, False, False, False),
        (True, True, False, False, False),
        (True, False, True, False, False),
        (True, False, False, True, False),
        (True, False, False, False, True),
        (False, False, False, False, False),
        (False, True, False, False, False),
        (False, False, True, False, False),
        (False, False, False, True, False),
        (False, False, False, False, True),
    ),
)
def test_cleanup(datafiles, initSequenceApp, dburl, singleSeq, full, db, cache, original):
    client, app = initSequenceApp(datafiles)

    with app.app_context():
        with psycopg.connect(dburl) as conn:
            sequences = []
            picsSeq1 = sorted(
                [
                    str(p[0])
                    for p in conn.execute(
                        "SELECT pic_id FROM sequences_pictures WHERE seq_id = (SELECT id FROM sequences WHERE metadata->>'title'='seq1')"
                    )
                ]
            )
            picsSeq2 = sorted(
                [
                    str(p[0])
                    for p in conn.execute(
                        "SELECT pic_id FROM sequences_pictures WHERE seq_id = (SELECT id FROM sequences WHERE metadata->>'title'='seq2')"
                    )
                ]
            )

            if singleSeq:
                sequences = [conn.execute("SELECT id FROM sequences WHERE metadata->>'title'='seq1'").fetchone()[0]]

            runner_pictures.cleanup(sequences, full, db, cache, original)

            # Check db cleanup
            if full or db:
                assert [p[0] for p in conn.execute("SELECT metadata->>'title' FROM sequences").fetchall()] == (
                    ["seq2"] if singleSeq else []
                )
                if singleSeq:
                    assert sorted([str(p[0]) for p in conn.execute("SELECT id FROM pictures").fetchall()]) == picsSeq2
                else:
                    assert len(conn.execute("SELECT id FROM pictures").fetchall()) == 0
            else:
                assert [p[0] for p in conn.execute("SELECT metadata->>'title' FROM sequences").fetchall()] == ["seq1", "seq2"]

            # Check derivates cleanup
            if full or cache:
                if singleSeq:
                    for p in picsSeq1:
                        assert not os.path.isdir(datafiles / "derivates" / p[0:2] / p[2:4] / p[4:6] / p[6:8] / p[9:])
                else:
                    assert len(os.listdir(datafiles / "derivates")) == 0

            # Check original pictures cleanup
            if full or original:
                if singleSeq:
                    for p in picsSeq1:
                        assert not os.path.isdir(datafiles / "permanent" / p[0:2] / p[2:4] / p[4:6] / p[6:8])
                else:
                    assert len(os.listdir(datafiles / "permanent")) == 0


@conftest.SEQ_IMGS
@conftest.SEQ_IMGS_FLAT
@conftest.SEQ_IMG_BLURRED
def test_cleanup_blur(monkeypatch, datafiles, initSequenceApp, tmp_path, dburl):
    monkeypatch.setattr(pictures, "createBlurredHDPicture", mockCreateBlurredHDPictureFactory(datafiles))
    client, app = initSequenceApp(datafiles, blur=True)

    with app.app_context():
        with psycopg.connect(dburl) as db:
            sequences = [db.execute("SELECT id FROM sequences WHERE metadata->>'title'='seq1'").fetchone()[0]]
            picsSeq1 = sorted(
                [
                    str(p[0])
                    for p in db.execute(
                        "SELECT pic_id FROM sequences_pictures WHERE seq_id = (SELECT id FROM sequences WHERE metadata->>'title' = 'seq1')"
                    )
                ]
            )
            picsSeq2 = sorted(
                [
                    str(p[0])
                    for p in db.execute(
                        "SELECT pic_id FROM sequences_pictures WHERE seq_id = (SELECT id FROM sequences WHERE metadata->>'title' = 'seq2')"
                    )
                ]
            )

            runner_pictures.cleanup(sequences, False, False, False, True)

            # Check DB and other derivates are untouched
            assert [p[0] for p in db.execute("SELECT metadata->>'title' FROM sequences").fetchall()] == ["seq1", "seq2"]

            for p in picsSeq1:
                assert not os.path.isdir(datafiles / "permanent" / p[0:2] / p[2:4] / p[4:6] / p[6:8])
                assert os.path.isdir(datafiles / "derivates" / p[0:2] / p[2:4] / p[4:6] / p[6:8])
                assert os.path.isfile(datafiles / "derivates" / p[0:2] / p[2:4] / p[4:6] / p[6:8] / p[9:] / "sd.jpg")
                assert os.path.isfile(datafiles / "derivates" / p[0:2] / p[2:4] / p[4:6] / p[6:8] / p[9:] / "thumb.jpg")
            for p in picsSeq2:
                assert os.path.isfile(datafiles / "permanent" / p[0:2] / p[2:4] / p[4:6] / p[6:8] / p[9:] + ".jpg")
                assert os.path.isdir(datafiles / "derivates" / p[0:2] / p[2:4] / p[4:6] / p[6:8])
                assert os.path.isfile(datafiles / "derivates" / p[0:2] / p[2:4] / p[4:6] / p[6:8] / p[9:] / "sd.jpg")
                assert os.path.isfile(datafiles / "derivates" / p[0:2] / p[2:4] / p[4:6] / p[6:8] / p[9:] / "thumb.jpg")


@conftest.SEQ_IMGS
@conftest.SEQ_IMGS_FLAT
def test_cleanup_allInDb_unfinished_allseqs(datafiles, initSequenceApp, dburl):
    client, app = initSequenceApp(datafiles)

    with app.app_context():
        with psycopg.connect(dburl) as conn:
            # Add a single picture to process table
            conn.execute("INSERT INTO pictures_to_process(picture_id) SELECT id FROM pictures LIMIT 1")
            conn.commit()

            runner_pictures.cleanup(database=True)

            assert len(conn.execute("SELECT id FROM pictures").fetchall()) == 0


@conftest.SEQ_IMGS
@conftest.SEQ_IMGS_FLAT
def test_cleanup_allInDb_unfinished_1seq(datafiles, initSequenceApp, dburl):
    client, app = initSequenceApp(datafiles)

    with app.app_context():
        with psycopg.connect(dburl) as conn:
            # Select a single sequence
            seqId = conn.execute("SELECT id FROM sequences LIMIT 1").fetchone()[0]

            # Add a single picture to process table
            conn.execute(
                "INSERT INTO pictures_to_process(picture_id) SELECT pic_id FROM sequences_pictures WHERE seq_id = %s LIMIT 1", [seqId]
            )
            conn.commit()

            runner_pictures.cleanup(sequences=[seqId], database=True)

            assert len(conn.execute("SELECT pic_id FROM sequences_pictures WHERE seq_id = %s", [seqId]).fetchall()) == 0


@conftest.SEQ_IMGS
def test_processSequence(datafiles, initSequence, tmp_path, dburl, defaultAccountID):
    initSequence(datafiles)

    # Check results
    with psycopg.connect(dburl, row_factory=dict_row) as db2:
        # Sequence definition
        res0 = db2.execute("SELECT id, status, metadata, account_id, ST_AsText(geom) AS geom FROM sequences").fetchall()[0]

        seqId = str(res0["id"])
        assert len(seqId) > 0

        # use regex because float precision may differ between systems
        expectedGeom = re.compile(
            r"^LINESTRING\(1\.919185441799\d+ 49\.00688961988\d+,1\.919189623000\d+ 49\.0068986458\d+,1\.919196360602\d+ 49\.00692625960\d+,1\.919199780601\d+ 49\.00695484980\d+,1\.919194019996\d+ 49\.00697341759\d+\)$"
        )
        assert expectedGeom.match(res0["geom"]) is not None
        assert res0["status"] == "ready"
        assert res0["account_id"] == defaultAccountID
        assert res0["metadata"]["title"] == "seq1"

        # Pictures
        res1 = db2.execute("SELECT id, ts, status, metadata, account_id FROM pictures ORDER BY ts").fetchall()

        assert len(res1) == 5
        assert len(str(res1[0]["id"])) > 0
        assert res1[0]["ts"].timestamp() == 1627550214.0
        assert res1[0]["status"] == "ready"
        assert res1[0]["metadata"]["field_of_view"] == 360
        assert res1[0]["account_id"] == defaultAccountID

        picIds = []
        for rec in res1:
            picIds.append(str(rec["id"]))

        # Sequences + pictures
        with db2.cursor() as cursor:
            res2 = cursor.execute("SELECT pic_id FROM sequences_pictures WHERE seq_id = %s ORDER BY rank", [seqId]).fetchall()
            resPicIds = [str(f["pic_id"]) for f in res2]

            assert resPicIds == picIds

        # Check destination folder structure
        for picId in picIds:
            permaPath = str(tmp_path / "permanent" / picId[0:2] / picId[2:4] / picId[4:6] / picId[6:8] / picId[9:]) + ".jpg"
            derivPath = tmp_path / "derivates" / picId[0:2] / picId[2:4] / picId[4:6] / picId[6:8] / picId[9:]
            assert os.path.isfile(permaPath)
            assert os.path.isdir(derivPath)
            assert os.path.isdir(derivPath / "tiles")
            assert os.path.isfile(derivPath / "sd.jpg")
            assert os.path.isfile(derivPath / "thumb.jpg")

        # Check upload folder has been removed
        assert len(os.listdir(tmp_path / "tmp")) == 0

        newSequencePicturesEntries = db2.execute(
            "select rank from sequences_pictures inner join pictures on (pic_id = id) order by ts asc"
        ).fetchall()
        assert newSequencePicturesEntries == [{"rank": rank} for rank in range(1, len(newSequencePicturesEntries) + 1)]


@conftest.SEQ_IMGS_FLAT
def test_processSequence_flat(datafiles, initSequence, tmp_path, dburl, defaultAccountID):
    with psycopg.connect(dburl, row_factory=dict_row) as db2:
        # Add camera metadata
        db2.execute("INSERT INTO cameras(model, sensor_width) VALUES ('OLYMPUS IMAGING CORP. SP-720UZ', 6.16) ON CONFLICT DO NOTHING")
        db2.commit()

        # Run processing
        app = initSequence(datafiles)

        # Sequence definition
        res0 = db2.execute("SELECT id, status, metadata, account_id, ST_AsText(geom) AS geom FROM sequences").fetchall()[0]

        seqId = str(res0["id"])
        assert len(seqId) > 0
        # use regex because float precision may differ between systems
        expectedGeom = re.compile(r"^LINESTRING\(-1\.949973106007\d+ 48\.139852239480\d+,-1\.949124581909\d+ 48\.13939279199\d+\)$")
        assert expectedGeom.match(res0["geom"]) is not None
        assert res0["status"] == "ready"
        assert res0["account_id"] == defaultAccountID
        assert res0["metadata"]["title"] == "seq1"

        # Pictures
        res1 = db2.execute("SELECT id, ts, status, metadata, account_id FROM pictures ORDER BY ts").fetchall()

        assert len(res1) == 2
        assert len(str(res1[0]["id"])) > 0
        assert res1[0]["ts"].timestamp() == 1429976177.0
        assert res1[0]["status"] == "ready"
        assert res1[0]["metadata"]["field_of_view"] == 67
        assert res1[0]["account_id"] == defaultAccountID

        picIds = []
        for rec in res1:
            picIds.append(str(rec["id"]))

        # Check destination folder structure
        for picId in picIds:
            permaPath = str(tmp_path / "permanent" / picId[0:2] / picId[2:4] / picId[4:6] / picId[6:8] / picId[9:]) + ".jpg"
            derivPath = tmp_path / "derivates" / picId[0:2] / picId[2:4] / picId[4:6] / picId[6:8] / picId[9:]
            assert os.path.isfile(permaPath)
            assert os.path.isdir(derivPath)
            assert not os.path.isdir(derivPath / "tiles")
            assert os.path.isfile(derivPath / "sd.jpg")
            assert os.path.isfile(derivPath / "thumb.jpg")

        # Check upload folder has been removed
        assert len(os.listdir(tmp_path / "tmp")) == 0


@conftest.SEQ_IMGS_NOHEADING
def test_processSequence_noheading(datafiles, initSequence, tmp_path, dburl):
    with psycopg.connect(dburl, row_factory=dict_row) as db2:
        initSequence(datafiles, preprocess=False)

        # Sequence definition
        seqId = db2.execute("SELECT id FROM sequences").fetchall()
        assert len(seqId) == 1

        # Pictures
        pics = db2.execute("SELECT * FROM pictures ORDER BY ts").fetchall()

        for r in pics:
            assert r["status"] == "ready"
            assert r["metadata"].get("heading") is None

        headings = {r["metadata"].get("originalFileName"): r["heading"] for r in pics}
        assert headings == {"1.jpg": 277, "2.jpg": 272, "3.jpg": 272, "4.jpg": 270, "5.jpg": 270}


def mockCreateBlurredHDPictureFactory(datafiles):
    """Mock function for pictures.createBlurredHDPicture"""

    def mockCreateBlurredHDPicture(fs, blurApi, pictureBytes, outputFilename):
        with open(datafiles + "/1_blurred.jpg", "rb") as f:
            fs.writebytes(outputFilename, f.read())
            return Image.open(str(datafiles + "/1_blurred.jpg"))

    return mockCreateBlurredHDPicture


@conftest.SEQ_IMG
def test_insertNewPictureInDatabase(datafiles, tmp_path, dburl, app, defaultAccountID):
    picture = Image.open(str(datafiles / "1.jpg"))
    with psycopg.connect(dburl) as db:
        seqId = runner_pictures.createSequence({}, defaultAccountID)

        picId = runner_pictures.insertNewPictureInDatabase(db, seqId, 1, picture, defaultAccountID, {"another metadata": "a_value"})
        db.commit()

        with psycopg.connect(dburl, row_factory=dict_row) as db2:
            res = db2.execute(
                """
				SELECT id, ts, heading, ST_X(geom) AS lon, ST_Y(geom) AS lat, status, metadata, exif
				FROM pictures
				WHERE id = %s
			""",
                [picId],
            ).fetchone()
            assert res
            assert len(str(res["id"])) > 0
            assert res["ts"].timestamp() == 1627550214.0
            assert res["heading"] == 349
            assert res["lon"] == 1.9191854417991367
            assert res["lat"] == 49.00688961988304
            assert res["status"] == "waiting-for-process"
            assert res["metadata"]["width"] == 5760
            assert res["metadata"]["height"] == 2880
            assert res["metadata"]["cols"] == 8
            assert res["metadata"]["rows"] == 4
            assert res["metadata"].get("lat") is None
            assert res["metadata"].get("lon") is None
            assert res["metadata"].get("ts") is None
            assert res["metadata"].get("heading") is None
            assert res["metadata"]["another metadata"] == "a_value"
            assert len(res["exif"]) > 0


@conftest.SEQ_IMGS
def test_updateSequenceHeadings_unchanged(datafiles, initSequence, dburl):
    initSequence(datafiles, preprocess=False)

    with psycopg.connect(dburl, autocommit=True) as db:
        seqId = db.execute("SELECT id FROM sequences").fetchone()
        assert seqId
        seqId = seqId[0]
        picHeadings = {}
        for key, value in db.execute("SELECT id, heading FROM pictures").fetchall():
            picHeadings[key] = value

        runner_pictures.updateSequenceHeadings(db, seqId, 10, True)

        for id, heading, headingMetadata in db.execute("SELECT id, heading, metadata->>'heading' AS mh FROM pictures").fetchall():
            assert picHeadings[id] == heading
            assert headingMetadata is None


@conftest.SEQ_IMGS
def test_updateSequenceHeadings_updateAllExisting(datafiles, initSequence, dburl):
    initSequence(datafiles, preprocess=False)

    with psycopg.connect(dburl, autocommit=True) as db:
        seqId = db.execute("SELECT id FROM sequences").fetchone()
        assert seqId is not None
        seqId = seqId[0]
        runner_pictures.updateSequenceHeadings(db, seqId, 10, False)
        res = db.execute("select metadata->>'originalFileName', heading, metadata->>'heading' AS mh from pictures").fetchall()
        for r in res:
            assert r[2] is None
        headings = {r[0].split("/")[-1]: r[1] for r in res}
        assert headings == {"1.jpg": 34, "2.jpg": 23, "3.jpg": 16, "4.jpg": 352, "5.jpg": 352}


@conftest.SEQ_IMG
def test_processPictureFiles_noblur_preprocess(datafiles, tmp_path, fsesUrl, dburl):
    permPath = datafiles / "permanent" / "9e" / "ae" / "c8" / "17"
    os.makedirs(permPath)
    os.makedirs(datafiles / "derivates" / "gvs_picder")
    permFile = permPath / "5348-4852-9443-0d5e5a8d8b77.jpg"
    os.rename(datafiles / "1.jpg", permFile)
    dbPic = runner_pictures.DbPicture(
        id=UUID("9eaec817-5348-4852-9443-0d5e5a8d8b77"), isBlurred=False, task=runner_pictures.ProcessTask.prepare
    )
    picture = Image.open(str(permFile))
    pictureOrig = picture.copy()

    appConfig = {"PICTURE_PROCESS_DERIVATES_STRATEGY": "PREPROCESS", "FILESYSTEMS": filesystems.openFilesystems(fsesUrl)}

    with psycopg.connect(dburl) as db:
        runner_pictures.processPictureFiles(db, dbPic, appConfig)

        # Blur + on-demand derivates = generates thumbnail + edits original file
        # Check folder has been created
        assert sorted(appConfig["FILESYSTEMS"].derivates.listdir("/9e/ae/c8/17/5348-4852-9443-0d5e5a8d8b77/")) == [
            "sd.jpg",
            "thumb.jpg",
            "tiles",
        ]
        test_pictures.assertPicturesSimilar(pictureOrig, Image.open(str(permFile)), 1)

        # Check content is same as generatePictureDerivates
        resPicDer = pictures.generatePictureDerivates(
            appConfig["FILESYSTEMS"].derivates, picture, {"cols": 8, "rows": 4, "width": 5760, "height": 2880}, "/gvs_picder"
        )
        assert resPicDer is True
        assert sorted(appConfig["FILESYSTEMS"].derivates.listdir("/9e/ae/c8/17/5348-4852-9443-0d5e5a8d8b77/")) == sorted(
            appConfig["FILESYSTEMS"].derivates.listdir("/gvs_picder/")
        )
        assert sorted(appConfig["FILESYSTEMS"].derivates.listdir("/9e/ae/c8/17/5348-4852-9443-0d5e5a8d8b77/tiles/")) == sorted(
            appConfig["FILESYSTEMS"].derivates.listdir("/gvs_picder/tiles/")
        )


@conftest.SEQ_IMG
def test_processPictureFiles_noblur_ondemand(datafiles, tmp_path, fsesUrl, dburl):
    permPath = datafiles / "permanent" / "9e" / "ae" / "c8" / "17"
    os.makedirs(permPath)
    permFile = permPath / "5348-4852-9443-0d5e5a8d8b77.jpg"
    os.rename(datafiles / "1.jpg", permFile)
    dbPic = runner_pictures.DbPicture(
        id=UUID("9eaec817-5348-4852-9443-0d5e5a8d8b77"), isBlurred=False, task=runner_pictures.ProcessTask.prepare
    )
    picture = Image.open(str(permFile))
    pictureOrig = picture.copy()

    appConfig = {"PICTURE_PROCESS_DERIVATES_STRATEGY": "ON_DEMAND", "FILESYSTEMS": filesystems.openFilesystems(fsesUrl)}

    with psycopg.connect(dburl) as db:
        runner_pictures.processPictureFiles(db, dbPic, appConfig)

        # Blur + on-demand derivates = generates thumbnail + edits original file
        # Check folder has been created
        assert sorted(appConfig["FILESYSTEMS"].derivates.listdir("/9e/ae/c8/17/5348-4852-9443-0d5e5a8d8b77/")) == ["thumb.jpg"]
        test_pictures.assertPicturesSimilar(pictureOrig, Image.open(str(permFile)), 1)


@conftest.SEQ_IMG
@conftest.SEQ_IMG_BLURRED
def test_processPictureFiles_blur_preprocess(monkeypatch, datafiles, tmp_path, fsesUrl, dburl):
    monkeypatch.setattr(pictures, "createBlurredHDPicture", mockCreateBlurredHDPictureFactory(datafiles))

    tmpPath = datafiles / "tmp" / "9e" / "ae" / "c8" / "17"
    permPath = datafiles / "permanent" / "9e" / "ae" / "c8" / "17"
    os.makedirs(tmpPath)
    tmpFile = tmpPath / "5348-4852-9443-0d5e5a8d8b77.jpg"
    permFile = permPath / "5348-4852-9443-0d5e5a8d8b77.jpg"
    os.rename(datafiles / "1.jpg", tmpFile)
    dbPic = runner_pictures.DbPicture(
        id=UUID("9eaec817-5348-4852-9443-0d5e5a8d8b77"), isBlurred=False, task=runner_pictures.ProcessTask.prepare
    )
    pictureOrig = Image.open(str(tmpFile))

    appConfig = {
        "API_BLUR_URL": "https://geovisio-blurring.net",
        "PICTURE_PROCESS_DERIVATES_STRATEGY": "PREPROCESS",
        "FILESYSTEMS": filesystems.openFilesystems(fsesUrl),
    }

    with psycopg.connect(dburl) as db:
        runner_pictures.processPictureFiles(db, dbPic, appConfig)

        # Blur + on-demand derivates = generates thumbnail + edits original file
        # Check folder has been created
        assert sorted(appConfig["FILESYSTEMS"].derivates.listdir("/9e/ae/c8/17/5348-4852-9443-0d5e5a8d8b77/")) == [
            "sd.jpg",
            "thumb.jpg",
            "tiles",
        ]
        test_pictures.assertPicturesSimilar(pictureOrig, Image.open(str(permFile)), 1, True)

        # Check tmp folder has been removed
        assert len(appConfig["FILESYSTEMS"].tmp.listdir("/")) == 0


@conftest.SEQ_IMG
@conftest.SEQ_IMG_BLURRED
def test_processPictureFiles_blur_ondemand(monkeypatch, datafiles, tmp_path, fsesUrl, dburl):
    monkeypatch.setattr(pictures, "createBlurredHDPicture", mockCreateBlurredHDPictureFactory(datafiles))

    tmpPath = datafiles / "tmp" / "9e" / "ae" / "c8" / "17"
    permPath = datafiles / "permanent" / "9e" / "ae" / "c8" / "17"
    os.makedirs(tmpPath)
    tmpFile = tmpPath / "5348-4852-9443-0d5e5a8d8b77.jpg"
    permFile = permPath / "5348-4852-9443-0d5e5a8d8b77.jpg"
    os.rename(datafiles / "1.jpg", tmpFile)
    dbPic = runner_pictures.DbPicture(
        id=UUID("9eaec817-5348-4852-9443-0d5e5a8d8b77"), isBlurred=False, task=runner_pictures.ProcessTask.prepare
    )
    pictureOrig = Image.open(str(tmpFile))

    appConfig = {
        "API_BLUR_URL": "https://geovisio-blurring.net",
        "PICTURE_PROCESS_DERIVATES_STRATEGY": "ON_DEMAND",
        "FILESYSTEMS": filesystems.openFilesystems(fsesUrl),
    }

    with psycopg.connect(dburl) as db:
        runner_pictures.processPictureFiles(db, dbPic, appConfig)

        # Blur + on-demand derivates = generates thumbnail + edits original file
        # Check folder has been created
        assert sorted(appConfig["FILESYSTEMS"].derivates.listdir("/9e/ae/c8/17/5348-4852-9443-0d5e5a8d8b77/")) == ["thumb.jpg"]
        test_pictures.assertPicturesSimilar(pictureOrig, Image.open(str(permFile)), 1, True)

        # Check tmp folder has been removed
        assert len(appConfig["FILESYSTEMS"].tmp.listdir("/")) == 0


@conftest.SEQ_IMG
def test_readPictureMetadata(datafiles):
    result = runner_pictures.readPictureMetadata(Image.open(str(datafiles) + "/1.jpg"))
    assert result == {
        "lat": 49.00688961988304,
        "lon": 1.9191854417991367,
        "ts": 1627550214.0,
        "heading": 349,
        "type": "equirectangular",
        "make": "GoPro",
        "model": "Max",
        "focal_length": 3,
        "tagreader_warnings": [],
    }


@conftest.SEQ_IMG
def test_readPictureMetadata_fullExif(datafiles):
    result = runner_pictures.readPictureMetadata(Image.open(str(datafiles) + "/1.jpg"), fullExif=True)
    assert len(result["exif"]) > 0


@conftest.SEQ_IMGS
def test_get_next_picture_to_process(datafiles, app, tmp_path, dburl, defaultAccountID):
    """
    Test runner_pictures._get_next_picture_to_process
    Insert 3 images, they should be taken in order 1 -> 3 -> 2 -> None (since 2 is marked as 'preparing-derivates' and should be taken last as we consider it has already been tried)
    """
    picture = Image.open(str(datafiles / "1.jpg"))

    seqId = runner_pictures.createSequence({}, defaultAccountID)
    with psycopg.connect(dburl) as db:
        db.commit()
        pic1_id = runner_pictures.insertNewPictureInDatabase(db, seqId, 1, picture, defaultAccountID, {})
        db.commit()  # we commit each insert to get different insert_at timestamp
        pic2_id = runner_pictures.insertNewPictureInDatabase(db, seqId, 2, picture, defaultAccountID, {})
        db.commit()
        pic3_id = runner_pictures.insertNewPictureInDatabase(db, seqId, 3, picture, defaultAccountID, {})
        db.commit()
        # being 'preparing-derivates' should only makes pic 2 to be taken last
        db.execute("UPDATE pictures SET status = 'preparing-derivates' WHERE id = %s", [pic2_id])
        db.commit()

    config = {"DB_URL": dburl}
    with runner_pictures._get_next_picture_to_process(config) as db_pic:
        assert db_pic is not None
        assert db_pic.id == str(pic1_id)

        with runner_pictures._get_next_picture_to_process(config) as db_pic2:
            assert db_pic2 is not None
            assert db_pic2.id == str(pic3_id)

            try:
                with runner_pictures._get_next_picture_to_process(config) as db_pic3:
                    assert db_pic3 is not None
                    assert db_pic3.id == str(pic2_id)

                    # There should no more be pictures to process
                    with runner_pictures._get_next_picture_to_process(config) as db_pic4:
                        assert db_pic4 is None

                    # An exception is raised, a rollback should occure, pic2 should be marked on error and lock should be released
                    raise Exception("some exception")
            except:
                pass

            with runner_pictures._get_next_picture_to_process(config) as db_pic5:
                assert db_pic5 is None
