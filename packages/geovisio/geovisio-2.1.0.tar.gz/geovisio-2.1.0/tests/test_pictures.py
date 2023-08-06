from flask import json
import os
import pytest
import psycopg
import io
import re
import math
import requests
from fs import open_fs
from PIL import Image, ImageChops, ImageStat
from . import conftest
from geovisio import create_app, pictures, runner_pictures, filesystems


FIXTURE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")

MOCK_BLUR_API = "https://geovisio-blurring.net"


def assertPicturesSimilar(pic1, pic2, limit, assertNot=False):
    """Checks if two images have less than limit % of differences"""
    diff = ImageChops.difference(pic1.convert("RGB"), pic2.convert("RGB"))
    stat = ImageStat.Stat(diff)
    diff_ratio = sum(stat.mean) / (len(stat.mean) * 255) * 100
    if assertNot:
        assert diff_ratio > limit
    else:
        assert diff_ratio <= limit


def test_getHDPicturePath(app):
    with app.app_context():
        assert pictures.getHDPicturePath("4366dddb-8a71-4f6e-a3d4-cb6b545476bb") == "/43/66/dd/db/8a71-4f6e-a3d4-cb6b545476bb.jpg"


def test_getPictureFolderPath(app):
    with app.app_context():
        assert pictures.getPictureFolderPath("4366dddb-8a71-4f6e-a3d4-cb6b545476bb") == "/43/66/dd/db/8a71-4f6e-a3d4-cb6b545476bb"


@conftest.SEQ_IMGS
@pytest.mark.parametrize(("preprocess"), ((True), (False)))
def test_checkPictureStatus(preprocess, datafiles, initSequenceApp, fsesUrl, dburl):
    client, app = initSequenceApp(datafiles, preprocess=preprocess)

    # Retrieve loaded sequence metadata
    fses = filesystems.openFilesystems(fsesUrl)

    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            picId = str(cursor.execute("SELECT id FROM pictures LIMIT 1").fetchone()[0])

            assert len(str(picId)) > 0

            with app.app_context(), app.test_request_context():
                picMetadata = pictures.checkPictureStatus(fses, picId)
                assert picMetadata["status"] == "ready"
                assert picMetadata["type"] == "equirectangular"
                assert pictures.areDerivatesAvailable(fses.derivates, picId, "equirectangular")


@conftest.SEQ_IMGS
@conftest.SEQ_IMGS_FLAT
@pytest.mark.parametrize(("derivates", "pictype"), ((True, "equirectangular"), (False, "equirectangular"), (True, "flat"), (False, "flat")))
def test_areDerivatesAvailable(derivates, pictype, datafiles, initSequenceApp, dburl):
    if pictype == "flat":
        os.remove(datafiles / "1.jpg")
        os.remove(datafiles / "2.jpg")
        os.remove(datafiles / "3.jpg")
        os.remove(datafiles / "4.jpg")
        os.remove(datafiles / "5.jpg")
    else:
        os.remove(datafiles / "b1.jpg")
        os.remove(datafiles / "b2.jpg")

    client, app = initSequenceApp(datafiles, preprocess=derivates)

    # Retrieve loaded sequence metadata
    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            picId = cursor.execute("SELECT id FROM pictures LIMIT 1").fetchone()[0]

            assert len(str(picId)) > 0

            with app.app_context():
                with open_fs(str(datafiles / "derivates")) as fs:
                    res = pictures.areDerivatesAvailable(fs, picId, pictype)
                    assert res == derivates


@conftest.SEQ_IMG
def test_generatePictureDerivates(datafiles, tmp_path, dburl):
    srcPath = str(datafiles)

    destPath = tmp_path / "out"
    destPath.mkdir()

    with open_fs(str(tmp_path)) as fs:
        res = pictures.generatePictureDerivates(
            fs, Image.open(srcPath + "/1.jpg"), {"cols": 8, "rows": 4, "width": 5760, "height": 2880}, "/out"
        )
        assert res is True

        # Check folder content
        assert sorted(fs.listdir("/out")) == ["sd.jpg", "thumb.jpg", "tiles"]


@conftest.SEQ_IMG
def test_generatePictureDerivates_skipThumbnail(datafiles, tmp_path, dburl):
    srcPath = str(datafiles)

    destPath = tmp_path / "out"
    destPath.mkdir()

    with open_fs(str(tmp_path)) as fs:
        res = pictures.generatePictureDerivates(
            fs, Image.open(srcPath + "/1.jpg"), {"cols": 8, "rows": 4, "width": 5760, "height": 2880}, "/out", skipThumbnail=True
        )
        assert res is True

        # Check folder content
        assert sorted(fs.listdir("/out")) == ["sd.jpg", "tiles"]


@pytest.mark.datafiles(os.path.join(FIXTURE_DIR, "b1.jpg"))
def test_generatePictureDerivates_flat(datafiles, tmp_path, dburl):
    srcPath = str(datafiles)

    destPath = tmp_path / "out"
    destPath.mkdir()

    with open_fs(str(tmp_path)) as fs:
        res = pictures.generatePictureDerivates(fs, Image.open(srcPath + "/b1.jpg"), {"width": 4288, "height": 3216}, "/out", "flat")
        assert res is True

        # Check folder content
        assert sorted(fs.listdir("/out")) == ["sd.jpg", "thumb.jpg"]


def mockBlurringAPIPost(datafiles, requests_mock):
    with open(datafiles + "/1_blurred.jpg", "rb") as mask:
        requests_mock.post(MOCK_BLUR_API + "/blur/", headers={"Content-Type": "image/jpeg"}, content=mask.read())


@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, "1.jpg"),
    os.path.join(FIXTURE_DIR, "1_blurred.jpg"),
)
def test_createBlurredHDPicture(requests_mock, datafiles, tmp_path):
    destPath = str(tmp_path)

    with open_fs(destPath) as fs:
        with fs.openbin("1.jpg") as f:
            picture = Image.open(f)
            mockBlurringAPIPost(datafiles, requests_mock)

            res = pictures.createBlurredHDPicture(fs, MOCK_BLUR_API, f, "/output.jpg")

            assert res.size == picture.size
            assert sorted(fs.listdir("/")) == sorted(["1.jpg", "1_blurred.jpg", "output.jpg"])


@conftest.SEQ_IMGS
def test_getPictureHD(datafiles, initSequence, dburl):
    client = initSequence(datafiles)

    # Retrieve loaded sequence metadata
    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            picId = cursor.execute("SELECT id FROM pictures LIMIT 1").fetchone()[0]

            assert len(str(picId)) > 0

            # Call on WebP
            response = client.get("/api/pictures/" + str(picId) + "/hd.webp")
            assert response.status_code == 200
            assert response.content_type == "image/webp"

            # Call on JPEG
            response = client.get("/api/pictures/" + str(picId) + "/hd.jpg")
            assert response.status_code == 200
            assert response.content_type == "image/jpeg"

            # Call on invalid format
            response = client.get("/api/pictures/" + str(picId) + "/hd.gif")
            assert response.status_code == 404

            # Call on unexisting picture
            response = client.get("/api/pictures/ffffffff-ffff-ffff-ffff-ffffffffffff/hd.webp")
            assert response.status_code == 404

            # Call on hidden picture
            cursor.execute("UPDATE pictures SET status = 'hidden' WHERE id = %s", [picId])
            conn.commit()
            response = client.get("/api/pictures/" + str(picId) + "/hd.webp")
            assert response.status_code == 403


@pytest.mark.skipci
@conftest.SEQ_IMG
@conftest.SEQ_IMG_BLURRED
def test_getPictureHD_blurred(requests_mock, datafiles, initSequenceApp, dburl):
    mockBlurringAPIPost(datafiles, requests_mock)
    client, app = initSequenceApp(datafiles, blur=True)

    # Retrieve loaded sequence metadata
    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            picId = cursor.execute("SELECT id FROM pictures LIMIT 1").fetchone()[0]

            assert len(str(picId)) > 0

            # Call on WebP
            response = client.get("/api/pictures/" + str(picId) + "/hd.webp")
            assert response.status_code == 200
            assert response.content_type == "image/webp"

            # Call on JPEG
            response = client.get("/api/pictures/" + str(picId) + "/hd.jpg")
            assert response.status_code == 200
            assert response.content_type == "image/jpeg"


@conftest.SEQ_IMG
def test_createSDPicture(datafiles, tmp_path):
    picture = Image.open(str(datafiles / "1.jpg"))
    destPath = str(tmp_path)

    # Generate file
    with open_fs(destPath) as fs:
        res = pictures.createSDPicture(fs, picture, "/sd.jpg")
        assert res is True

        # Check result file
        resImg = Image.open(destPath + "/sd.jpg")
        w, h = resImg.size
        assert w == 2048
        assert resImg.info["exif"] == picture.info["exif"]


@conftest.SEQ_IMGS
def test_getPictureSD(datafiles, initSequence, dburl):
    client = initSequence(datafiles)

    # Retrieve loaded sequence metadata
    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            picId = cursor.execute("SELECT id FROM pictures LIMIT 1").fetchone()[0]

            assert len(str(picId)) > 0

            # Call on WebP
            response = client.get("/api/pictures/" + str(picId) + "/sd.webp")
            assert response.status_code == 200
            assert response.content_type == "image/webp"

            # Call on JPEG
            response = client.get("/api/pictures/" + str(picId) + "/sd.jpg")
            assert response.status_code == 200
            assert response.content_type == "image/jpeg"

            img = Image.open(io.BytesIO(response.get_data()))
            w, h = img.size
            assert w == 2048

            # Call API on unexisting picture
            response = client.get("/api/pictures/ffffffff-ffff-ffff-ffff-ffffffffffff/sd.jpg")
            assert response.status_code == 404

            # Call API on hidden picture
            cursor.execute("UPDATE pictures SET status = 'hidden' WHERE id = %s", [picId])
            conn.commit()
            response = client.get("/api/pictures/" + str(picId) + "/sd.jpg")
            assert response.status_code == 403


@conftest.SEQ_IMG
def test_createThumbPicture(datafiles, tmp_path):
    picture = Image.open(str(datafiles / "1.jpg"))
    destPath = str(tmp_path)

    # Generate file
    with open_fs(destPath) as fs:
        res = pictures.createThumbPicture(fs, picture, "/thumb.jpg")
        assert res is True

        # Check result file
        resImg = Image.open(destPath + "/thumb.jpg")
        w, h = resImg.size
        assert w == 500
        assert h == 300


@pytest.mark.datafiles(os.path.join(FIXTURE_DIR, "b1.jpg"))
def test_createThumbPicture_flat(datafiles, tmp_path):
    picture = Image.open(str(datafiles / "b1.jpg"))
    destPath = str(tmp_path)

    # Generate file
    with open_fs(destPath) as fs:
        res = pictures.createThumbPicture(fs, picture, "/thumb.jpg", "flat")
        assert res is True

        # Check result file
        resImg = Image.open(destPath + "/thumb.jpg")
        w, h = resImg.size
        assert w == 500
        assert h == 375


@conftest.SEQ_IMGS
def test_getPictureThumb(datafiles, initSequence, dburl):
    client = initSequence(datafiles)

    # Retrieve loaded sequence metadata
    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            picId = cursor.execute("SELECT id FROM pictures LIMIT 1").fetchone()[0]

            assert len(str(picId)) > 0

            # Call on WebP
            response = client.get("/api/pictures/" + str(picId) + "/thumb.webp")
            assert response.status_code == 200
            assert response.content_type == "image/webp"

            # Call on JPEG
            response = client.get("/api/pictures/" + str(picId) + "/thumb.jpg")
            assert response.status_code == 200
            assert response.content_type == "image/jpeg"

            img = Image.open(io.BytesIO(response.get_data()))
            w, h = img.size
            assert w == 500
            assert h == 300

            # Call API on unexisting picture
            response = client.get("/api/pictures/ffffffff-ffff-ffff-ffff-ffffffffffff/thumb.webp")
            assert response.status_code == 404

            # Call API on hidden picture
            cursor.execute("UPDATE pictures SET status = 'hidden' WHERE id = %s", [picId])
            conn.commit()
            response = client.get("/api/pictures/" + str(picId) + "/thumb.webp")
            assert response.status_code == 403


@pytest.mark.parametrize(
    ("imgWidth", "tileCols"), ((512, 4), (1024, 4), (2048, 4), (4096, 8), (5760, 8), (8192, 16), (32768, 64), (655536, 64))
)
def test_getTileSize(imgWidth, tileCols):
    res = pictures.getTileSize((imgWidth, imgWidth / 2))
    assert isinstance(res[0], int)
    assert isinstance(res[1], int)
    assert res[0] == tileCols
    assert res[1] == tileCols / 2
    assert tileCols in [4, 8, 16, 32, 64]


@conftest.SEQ_IMG
def test_getPictureSizing(datafiles):
    res = pictures.getPictureSizing(Image.open(str(datafiles / "1.jpg")))
    assert res["cols"] == 8
    assert res["rows"] == 4
    assert res["width"] == 5760
    assert res["height"] == 2880


@conftest.SEQ_IMG
def test_createTiledPicture(datafiles, tmp_path):
    picture = Image.open(str(datafiles / "1.jpg"))
    destPath = str(tmp_path)
    cols = 4
    rows = 2

    # Generate tiles
    with open_fs(destPath) as fs:
        res = pictures.createTiledPicture(fs, picture, "/", cols, rows)
        assert res is True

        # Check every single file
        origImgSize = picture.size
        colWidth = math.floor(origImgSize[0] / cols)
        rowHeight = math.floor(origImgSize[1] / rows)

        for col in range(cols):
            for row in range(rows):
                tilePath = destPath + "/" + str(col) + "_" + str(row) + ".jpg"
                assert os.path.isfile(tilePath)
                tile = Image.open(tilePath)
                assert tile.size == (colWidth, rowHeight)

                origImgTile = picture.crop((colWidth * col, rowHeight * row, colWidth * (col + 1), rowHeight * (row + 1)))

                assert tile.height == origImgTile.height and tile.width == origImgTile.width

                if tile.mode == origImgTile.mode == "RGBA":
                    img1_alphas = [pixel[3] for pixel in tile.getdata()]
                    img2_alphas = [pixel[3] for pixel in origImgTile.getdata()]
                    assert img1_alphas == img2_alphas

                assertPicturesSimilar(tile, origImgTile, 1)


def test_getPictureTiledEmpty(tmp_path, client):
    # Call API on unexisting picture
    response = client.get("/api/pictures/00000000-0000-0000-0000-000000000000/tiled/0_0.jpg")
    assert response.status_code == 404


@pytest.mark.parametrize(
    ("col", "row", "httpCode", "picStatus", "format"),
    (
        (0, 0, 200, "ready", "webp"),
        (0, 0, 200, "ready", "jpeg"),
        (7, 3, 200, "ready", "jpeg"),
        (8, 4, 404, "ready", "jpeg"),
        (-1, -1, 404, "ready", "jpeg"),
        (0, 0, 403, "hidden", "jpeg"),
    ),
)
@conftest.SEQ_IMGS
def test_getPictureTiled(datafiles, initSequence, dburl, col, row, httpCode, picStatus, format):
    client = initSequence(datafiles)

    # Retrieve loaded sequence metadata
    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            picId = cursor.execute("SELECT id FROM pictures LIMIT 1").fetchone()[0]

            assert len(str(picId)) > 0

            seqId = cursor.execute("SELECT id FROM sequences LIMIT 1").fetchone()[0]

            assert len(str(seqId)) > 0

            if picStatus != "ready":
                cursor.execute("UPDATE pictures SET status = %s WHERE id = %s", (picStatus, picId))
                conn.commit()

            # Call on WebP
            response = client.get(
                "/api/pictures/" + str(picId) + "/tiled/" + str(col) + "_" + str(row) + "." + ("jpg" if format == "jpeg" else format)
            )
            assert response.status_code == httpCode

            if httpCode == 200:
                assert response.content_type == "image/" + format

                diskImg = Image.open(
                    str(datafiles)
                    + "/derivates/"
                    + str(picId)[0:2]
                    + "/"
                    + str(picId)[2:4]
                    + "/"
                    + str(picId)[4:6]
                    + "/"
                    + str(picId)[6:8]
                    + "/"
                    + str(picId)[9:]
                    + "/tiles/"
                    + str(col)
                    + "_"
                    + str(row)
                    + ".jpg"
                )
                apiImg = Image.open(io.BytesIO(response.get_data()))

                assertPicturesSimilar(diskImg, apiImg, 2)


@conftest.SEQ_IMGS_FLAT
def test_getPictureTiled_flat(datafiles, initSequence, tmp_path, dburl):
    client = initSequence(datafiles)

    # Prepare sequence
    with psycopg.connect(dburl) as db:
        # Get picture ID
        picId = db.execute("SELECT id FROM pictures LIMIT 1").fetchone()[0]
        assert len(str(picId)) > 0

        # Check tiles API call
        response = client.get("/api/pictures/" + str(picId) + "/tiled/0_0.webp")
        assert response.status_code == 404
