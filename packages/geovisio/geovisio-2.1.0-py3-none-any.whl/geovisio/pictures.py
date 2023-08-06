import psycopg
from psycopg.rows import dict_row
import io
import os
import math
from itertools import repeat
from flask import Blueprint, current_app, request, send_file
from PIL import Image
import requests
from . import errors, auth, utils
from flask import redirect
from typing import Optional
import fs.base
import logging

bp = Blueprint("pictures", __name__, url_prefix="/api/pictures")

log = logging.getLogger("geovisio.pictures")


def getPictureSizing(picture):
    """Calculates image dimensions (width, height, amount of columns and rows for tiles)

    Parameters
    ----------
    picture : PIL.Image
            Picture

    Returns
    -------
    dict
            { width, height, cols, rows }
    """
    tileSize = getTileSize(picture.size)
    return {"width": picture.size[0], "height": picture.size[1], "cols": tileSize[0], "rows": tileSize[1]}


def getHDPicturePath(pictureId):
    """Get the path to a picture HD version as a string

    Parameters
    ----------
    pictureId : str
            The ID of picture

    Returns
    -------
    str
            The path to picture derivates
    """
    return f"/{str(pictureId)[0:2]}/{str(pictureId)[2:4]}/{str(pictureId)[4:6]}/{str(pictureId)[6:8]}/{str(pictureId)[9:]}.jpg"


def getPictureFolderPath(pictureId):
    """Get the path to GeoVisio picture folder as a string

    Parameters
    ----------
    pictureId : str
            The ID of picture

    Returns
    -------
    str
            The path to picture derivates
    """
    return f"/{str(pictureId)[0:2]}/{str(pictureId)[2:4]}/{str(pictureId)[4:6]}/{str(pictureId)[6:8]}/{str(pictureId)[9:]}"


def checkPictureStatus(fses, pictureId):
    """Checks if picture exists in database, is ready to serve, and retrieves its metadata

    Parameters
    ----------
    fses : filesystems.Filesystems
            Filesystem to look through
    pictureId : str
            The ID of picture

    Returns
    -------
    dict
            Picture metadata extracted from database
    """

    account = auth.get_current_account()
    accountId = account.id if account is not None else None
    # Check picture availability + status
    with psycopg.connect(current_app.config["DB_URL"], row_factory=dict_row) as db:
        picMetadata = db.execute(
            """
			SELECT
				p.status,
				(p.metadata->>'cols')::int AS cols,
				(p.metadata->>'rows')::int AS rows,
				p.metadata->>'type' AS type,
				p.account_id,
				s.status AS seq_status
			FROM pictures p
			JOIN sequences_pictures sp ON sp.pic_id = p.id
			JOIN sequences s ON s.id = sp.seq_id
   			WHERE p.id = %s
		""",
            [pictureId],
        ).fetchone()

        if picMetadata is None:
            raise errors.InvalidAPIUsage("Picture can't be found, you may check its ID", status_code=404)

        if (picMetadata["status"] != "ready" or picMetadata["seq_status"] != "ready") and accountId != str(picMetadata["account_id"]):
            raise errors.InvalidAPIUsage("Picture is not available (either hidden by admin or processing)", status_code=403)

        # Check original image availability
        if not fses.permanent.exists(getHDPicturePath(pictureId)):
            raise errors.InvalidAPIUsage("HD Picture file is not available", status_code=500)

        # Check derivates availability
        if areDerivatesAvailable(fses.derivates, pictureId, picMetadata["type"]):
            return picMetadata
        else:
            picDerivates = getPictureFolderPath(pictureId)

            # Try to create derivates folder if it doesn't exist yet
            fses.derivates.makedirs(picDerivates, recreate=True)

            picture = Image.open(fses.permanent.openbin(getHDPicturePath(pictureId)))

            # Force generation of derivates
            if generatePictureDerivates(fses.derivates, picture, getPictureSizing(picture), picDerivates, picMetadata["type"]):
                return picMetadata
            else:
                raise errors.InvalidAPIUsage("Picture derivates file are not available", status_code=500)


def areDerivatesAvailable(fs, pictureId, pictureType):
    """Checks if picture derivates files are ready to serve

    Parameters
    ----------
    fs : fs.base.FS
            Filesystem to look through
    pictureId : str
            The ID of picture
    pictureType : str
            The picture type (flat, equirectangular)

    Returns
    -------
    bool
            True if all derivates files are available
    """

    path = getPictureFolderPath(pictureId)

    # Check if SD picture + thumbnail are available
    if not (fs.exists(path + "/sd.jpg") and fs.exists(path + "/thumb.jpg")):
        return False

    # Check if tiles are available
    if pictureType == "equirectangular" and not (fs.isdir(path + "/tiles") and len(fs.listdir(path + "/tiles")) >= 2):
        return False

    return True


def generatePictureDerivates(fs, picture, sizing, outputFolder, type="equirectangular", skipThumbnail=False):
    """Creates all derivated version of a picture (thumbnail, small, tiled)

    Parameters
    ----------
    fs : fs.base.FS
            Filesystem to look through
    picture : PIL.Image
            Picture file
    sizing : dict
            Picture dimensions (width, height, cols, rows)
    outputFolder : str
            Path to output folder (relative to instance root)
    type : str (optional)
            Type of picture (flat, equirectangular (default))
    skipThumbnail : bool (optional)
            Do not generate thumbnail (default to false, ie thumbnail is generated)

    Returns
    -------
    bool
            True if worked
    """

    # Thumbnail + fixed-with versions
    if not skipThumbnail:
        createThumbPicture(fs, picture, outputFolder + "/thumb.jpg", type)
    createSDPicture(fs, picture, outputFolder + "/sd.jpg")

    # Tiles
    if type == "equirectangular":
        tileFolder = outputFolder + "/tiles"
        fs.makedir(tileFolder, recreate=True)
        createTiledPicture(fs, picture, tileFolder, sizing["cols"], sizing["rows"])

    return True


def createBlurredHDPicture(fs, blurApi, pictureBytes, outputFilename):
    """Create the blurred version of a picture using a blurMask

    Parameters
    ----------
    fs : fs.base.FS
            Filesystem to look through
    blurApi : str
            The blurring API HTTP URL
    pictureBytes : io.IOBase
            Input image (as bytes)
    outputFilename : str
            Path to output file (relative to instance root)

    Returns
    -------
    PIL.Image
            The blurred version of the image
    """

    if blurApi is not None:
        # Call blur API
        pictureBytes.seek(0)
        blurResponse = requests.post(blurApi + "/blur/", files={"picture": ("picture.jpg", pictureBytes.read(), "image/jpeg")})
        blurResponse.raise_for_status()

        # Save mask to FS
        fs.writebytes(outputFilename, blurResponse.content)

        return Image.open(io.BytesIO(blurResponse.content))

    else:
        return None


def checkFormatParam(format):
    """Verify that user asks for a valid image format"""

    valid = ["jpg", "webp"]
    if format not in valid:
        raise errors.InvalidAPIUsage(
            "Invalid '" + format + "' format for image, only the following formats are available: " + ", ".join(valid), status_code=404
        )


def sendInFormat(picture, picFormat, httpFormat):
    """Send picture file in queried format"""

    httpFormat = "jpeg" if httpFormat == "jpg" else httpFormat
    picFormat = "jpeg" if picFormat == "jpg" else picFormat

    if picFormat == httpFormat:
        return send_file(picture, mimetype="image/" + httpFormat)
    else:
        imgio = io.BytesIO()
        Image.open(picture).save(imgio, format=httpFormat, quality=90)
        imgio.seek(0)
        return send_file(imgio, mimetype="image/" + httpFormat)


@bp.route("/<uuid:pictureId>/hd.<format>")
def getPictureHD(pictureId, format):
    """Get picture image (high-definition)
    ---
    tags:
        - Pictures
    parameters:
        - name: pictureId
          in: path
          description: ID of picture to retrieve
          required: true
          schema:
            type: string
        - name: format
          in: path
          description: Wanted format for output image (either jpg or webp)
          required: true
          schema:
            type: string
    responses:
        200:
            description: High-definition
            content:
                image/jpeg:
                    schema:
                        type: string
                        format: binary
                image/webp:
                    schema:
                        type: string
                        format: binary
    """

    checkFormatParam(format)

    fses = current_app.config["FILESYSTEMS"]
    metadata = checkPictureStatus(fses, pictureId)

    external_url = getPublicHDPictureExternalUrl(pictureId, format)
    if external_url and metadata["status"] == "ready":
        return redirect(external_url)

    try:
        picture = fses.permanent.openbin(getHDPicturePath(pictureId))
    except:
        raise errors.InvalidAPIUsage("Unable to read picture on filesystem", status_code=500)

    return sendInFormat(picture, "jpeg", format)


def createSDPicture(fs, picture, outputFilename):
    """Create a standard definition version of given picture and save it on filesystem

    Parameters
    ----------
    fs : fs.base.FS
            Filesystem to look through
    picture : PIL.Image
            Input image
    outputFilename : str
            Path to output file (relative to instance root)

    Returns
    -------
    bool
            True if operation was successful
    """

    sdImg = picture.resize((2048, int(picture.size[1] * 2048 / picture.size[0])), Image.HAMMING)

    sdImgBytes = io.BytesIO()
    sdImg.save(sdImgBytes, format="jpeg", quality=75, exif=(picture.info.get("exif") or bytes()))
    fs.writebytes(outputFilename, sdImgBytes.getvalue())

    return True


@bp.route("/<uuid:pictureId>/sd.<format>")
def getPictureSD(pictureId, format):
    """Get picture image (standard definition)
    ---
    tags:
        - Pictures
    parameters:
        - name: pictureId
          in: path
          description: ID of picture to retrieve
          required: true
          schema:
            type: string
        - name: format
          in: path
          description: Wanted format for output image (either jpg or webp)
          required: true
          schema:
            type: string
    responses:
        200:
            description: Standard definition (width of 2048px)
            content:
                image/jpeg:
                    schema:
                        type: string
                        format: binary
                image/webp:
                    schema:
                        type: string
                        format: binary
    """
    checkFormatParam(format)

    fses = current_app.config["FILESYSTEMS"]
    metadata = checkPictureStatus(fses, pictureId)

    external_url = getPublicDerivatePictureExternalUrl(pictureId, format, "sd.jpg")
    if external_url and metadata["status"] == "ready":
        return redirect(external_url)

    try:
        picture = fses.derivates.openbin(getPictureFolderPath(pictureId) + "/sd.jpg")
    except:
        raise errors.InvalidAPIUsage("Unable to read picture on filesystem", status_code=500)

    return sendInFormat(picture, "jpeg", format)


def createThumbPicture(fs, picture, outputFilename, type="equirectangular"):
    """Create a thumbnail version of given picture and save it on filesystem

    Parameters
    ----------
    fs : fs.base.FS
            Filesystem to look through
    picture : PIL.Image
            Input image
    outputFilename : str
            Path to output file (relative to instance root)
    type : str (optional)
            Type of picture (flat, equirectangular (default))

    Returns
    -------
    bool
            True if operation was successful
    """

    if type == "equirectangular":
        tbImg = picture.resize((2000, 1000), Image.HAMMING).crop((750, 350, 1250, 650))
    else:
        tbImg = picture.resize((500, int(picture.size[1] * 500 / picture.size[0])), Image.HAMMING)

    tbImgBytes = io.BytesIO()
    tbImg.save(tbImgBytes, format="jpeg", quality=75)
    fs.writebytes(outputFilename, tbImgBytes.getvalue())

    return True


def sendThumbnail(pictureId, format):
    """Send the thumbnail of a picture in a given format"""
    checkFormatParam(format)

    fses = current_app.config["FILESYSTEMS"]
    metadata = checkPictureStatus(fses, pictureId)

    external_url = getPublicDerivatePictureExternalUrl(pictureId, format, "thumb.jpg")
    if external_url and metadata["status"] == "ready":
        return redirect(external_url)

    try:
        picture = fses.derivates.openbin(getPictureFolderPath(pictureId) + "/thumb.jpg")
    except:
        raise errors.InvalidAPIUsage("Unable to read picture on filesystem", status_code=500)

    return sendInFormat(picture, "jpeg", format)


@bp.route("/<uuid:pictureId>/thumb.<format>")
def getPictureThumb(pictureId, format):
    """Get picture thumbnail
    ---
    tags:
        - Pictures
    parameters:
        - name: pictureId
          in: path
          description: ID of picture to retrieve
          required: true
          schema:
            type: string
        - name: format
          in: path
          description: Wanted format for output image (either jpg or webp)
          required: true
          schema:
            type: string
    responses:
        200:
            description: 500px wide ready-for-display image
            content:
                image/jpeg:
                    schema:
                        type: string
                        format: binary
                image/webp:
                    schema:
                        type: string
                        format: binary
    """
    return sendThumbnail(pictureId, format)


def getTileSize(imgSize):
    """Compute ideal amount of rows and columns to give a tiled version of an image according to its original size

    Parameters
    ----------
    imgSize : tuple
        Original image size, as (width, height)

    Returns
    -------
    tuple
        Ideal tile splitting as (cols, rows)
    """

    possibleCols = [4, 8, 16, 32, 64]  # Limitation of PSV, see https://photo-sphere-viewer.js.org/guide/adapters/tiles.html#cols-required
    idealCols = max(min(int(int(imgSize[0] / 512) / 2) * 2, 64), 4)
    cols = possibleCols[0]
    for c in possibleCols:
        if idealCols >= c:
            cols = c
    return (int(cols), int(cols / 2))


def createTiledPicture(fs, picture, destPath, cols, rows):
    """Create tiled version of an input image into destination directory.

    Output images are named following col_row.jpg format, 0_0.webp being the top-left corner.

    Parameters
    ----------
    fs : fs.base.FS
        Filesystem to look through
    picture : PIL.Image
        Input image
    destPath : str
        Path of the output directory
    cols : int
        Amount of columns for splitted image
    rows : int
        Amount of rows for splitted image
    """

    colWidth = math.floor(picture.size[0] / cols)
    rowHeight = math.floor(picture.size[1] / rows)

    def createTile(picture, col, row):
        tilePath = destPath + "/" + str(col) + "_" + str(row) + ".jpg"
        tile = picture.crop((colWidth * col, rowHeight * row, colWidth * (col + 1), rowHeight * (row + 1)))
        tileBytes = io.BytesIO()
        tile.save(tileBytes, format="jpeg", quality=95)
        fs.writebytes(tilePath, tileBytes.getvalue())
        return True

    for col in range(cols):
        for row in range(rows):
            createTile(picture, col, row)

    return True


@bp.route("/<uuid:pictureId>/tiled/<col>_<row>.<format>")
def getPictureTile(pictureId, col, row, format):
    """Get picture tile
    ---
    tags:
        - Pictures
    parameters:
        - name: pictureId
          in: path
          description: ID of picture to retrieve
          required: true
          schema:
            type: string
        - name: col
          in: path
          description: Tile column ID
          required: true
          schema:
            type: number
        - name: row
          in: path
          description: Tile row ID
          required: true
          schema:
            type: number
        - name: format
          in: path
          description: Wanted format for output image (either jpg or webp)
          required: true
          schema:
            type: string
    responses:
        200:
            description: Tile image (size depends of original image resolution, square with side size around 512px)
            content:
                image/jpeg:
                    schema:
                        type: string
                        format: binary
                image/webp:
                    schema:
                        type: string
                        format: binary
    """

    checkFormatParam(format)

    fses = current_app.config["FILESYSTEMS"]

    metadata = checkPictureStatus(fses, pictureId)
    external_url = getPublicDerivatePictureExternalUrl(pictureId, format, f"tiles/{col}_{row}.jpg")
    if external_url and metadata["status"] == "ready":
        return redirect(external_url)

    picPath = f"{getPictureFolderPath(pictureId)}/tiles/{col}_{row}.jpg"

    if metadata["type"] == "flat":
        raise errors.InvalidAPIUsage("Tiles are not available for flat pictures", status_code=404)

    try:
        col = int(col)
    except:
        raise errors.InvalidAPIUsage("Column parameter is invalid, should be an integer", status_code=404)

    if col < 0 or col >= metadata["cols"]:
        raise errors.InvalidAPIUsage("Column parameter is invalid", status_code=404)

    try:
        row = int(row)
    except:
        raise errors.InvalidAPIUsage("Row parameter is invalid, should be an integer", status_code=404)

    if row < 0 or row >= metadata["rows"]:
        raise errors.InvalidAPIUsage("Row parameter is invalid", status_code=404)

    try:
        picture = fses.derivates.openbin(picPath)
    except:
        raise errors.InvalidAPIUsage("Unable to read picture on filesystem", status_code=500)

    return sendInFormat(picture, "jpeg", format)


def getPublicDerivatePictureExternalUrl(pictureId: str, format: str, derivateFileName: str) -> Optional[str]:
    """
    Get the external public url for a derivate picture

    A picture has an external url if the `API_DERIVATES_PICTURES_PUBLIC_URL` has been defined.

    To make it work, the pictures must be available at this url, and stored in the same way as in geovisio.

    It can be more performant for example to serve the images right from a public s3 bucket, or an nginx.
    """
    if format != "jpg":
        return None
    external_root_url = current_app.config.get("API_DERIVATES_PICTURES_PUBLIC_URL")
    if not external_root_url:
        return None
    if current_app.config.get("PICTURE_PROCESS_DERIVATES_STRATEGY") == "PREPROCESS":
        url = f"{external_root_url}{getPictureFolderPath(pictureId)}/{derivateFileName}"
        return url
    # TODO: if needed, handle pic existance checking for `ON_DEMAND`
    return None


def getPublicHDPictureExternalUrl(pictureId: str, format: str) -> Optional[str]:
    """
    Get the external public url for a HD picture

    A picture has an external url if the `API_PERMANENT_PICTURES_PUBLIC_URL` has been defined.

    To make it work, the pictures must be available at this url, and stored in the same way as in geovisio.

    It can be more performant for example to serve the image right from a public s3 bucket, or an nginx.
    """
    if format != "jpg":
        return None
    external_root_url = current_app.config.get("API_PERMANENT_PICTURES_PUBLIC_URL")
    if not external_root_url:
        return None
    return f"{external_root_url}{getHDPicturePath(pictureId)}"


def removeAllFiles(picId: str):
    """
    Remove all picture's associated files (the picture and all its derivate)
    """
    picPath = getPictureFolderPath(picId)

    fses = current_app.config["FILESYSTEMS"]

    utils.removeFsTreeEvenNotFound(fses.derivates, picPath + "/tiles")
    utils.removeFsEvenNotFound(fses.derivates, picPath + "/blurred.jpg")
    utils.removeFsEvenNotFound(fses.derivates, picPath + "/thumb.jpg")
    utils.removeFsEvenNotFound(fses.derivates, picPath + "/sd.jpg")

    _remove_empty_parent_dirs(fses.derivates, picPath)

    hd_pic_path = getHDPicturePath(picId)
    utils.removeFsEvenNotFound(fses.permanent, hd_pic_path)
    _remove_empty_parent_dirs(fses.permanent, os.path.dirname(hd_pic_path))


def _remove_empty_parent_dirs(fs: fs.base.FS, dir: str):
    """Remove all empty parent dir"""
    current_dir = dir
    while current_dir and current_dir != "/":
        if not fs.exists(current_dir) or not fs.isempty(current_dir):
            return
        log.debug(f"removing empty directory {current_dir}")
        fs.removedir(current_dir)
        current_dir = os.path.dirname(current_dir)
