from flask import json
import pytest
import psycopg
import re
from pystac import Catalog, Collection, ItemCollection, Item
from geovisio import create_app, stac, pictures, runner_pictures
from datetime import datetime, date
from uuid import UUID
from . import conftest
from urllib.parse import urlencode
import time
import io
import os
import itertools
import requests
from PIL import Image
from geopic_tag_reader import reader

STAC_VERSION = "1.0.0"


def test_landing(client):
    response = client.get("/api/")
    data = response.json

    assert response.status_code == 200
    assert data["type"] == "Catalog"
    ctl = Catalog.from_dict(data)
    assert len(ctl.links) > 0
    assert ctl.title == "GeoVisio STAC API"
    assert ctl.id == "geovisio"
    assert ctl.extra_fields.get("extent") is None
    assert ctl.get_links("self")[0].get_absolute_href() == "http://localhost:5000/api/"
    assert ctl.get_links("xyz")[0].get_absolute_href() == "http://localhost:5000/api/map/{z}/{x}/{y}.mvt"
    assert ctl.get_links("collection-preview")[0].get_absolute_href() == "http://localhost:5000/api/collections/{id}/thumb.jpg"
    assert ctl.get_links("item-preview")[0].get_absolute_href() == "http://localhost:5000/api/pictures/{id}/thumb.jpg"


@conftest.SEQ_IMGS
def test_landing_extent(datafiles, initSequence):
    client = initSequence(datafiles, preprocess=False)
    response = client.get("/api/")
    data = response.json

    assert response.status_code == 200
    assert data["type"] == "Catalog"
    ctl = Catalog.from_dict(data)
    assert len(ctl.links) > 0

    assert len(ctl.extra_fields["extent"]["temporal"]["interval"]) == 1
    assert len(ctl.extra_fields["extent"]["temporal"]["interval"][0]) == 2
    assert re.match(r"^2021-07-29T", ctl.extra_fields["extent"]["temporal"]["interval"][0][0])
    assert re.match(r"^2021-07-29T", ctl.extra_fields["extent"]["temporal"]["interval"][0][1])
    assert ctl.extra_fields["extent"]["spatial"] == {
        "bbox": [[1.9191854000091553, 49.00688934326172, 1.919199824333191, 49.00697708129883]]
    }


def test_conformance(client):
    response = client.get("/api/conformance")
    data = response.json

    assert response.status_code == 200
    assert data["conformsTo"] == stac.CONFORMANCE_LIST


def test_dbSequenceToStacCollection(client):
    dbSeq = {
        "id": UUID("{12345678-1234-5678-1234-567812345678}"),
        "name": "Test sequence",
        "minx": -1.0,
        "maxx": 1.0,
        "miny": -2.0,
        "maxy": 2.0,
        "mints": datetime.fromisoformat("2020-01-01T12:50:37+00:00"),
        "maxts": datetime.fromisoformat("2020-01-01T13:30:42+00:00"),
        "inserted_at": datetime.fromisoformat("2023-01-01T12:42:00+02:00"),
        "updated_at": datetime.fromisoformat("2023-01-01T13:42:00+02:00"),
        "account_name": "Default account",
        "nbpic": 10,
    }

    res = stac.dbSequenceToStacCollection(dbSeq)

    assert res
    assert res["type"] == "Collection"
    assert res["stac_version"] == STAC_VERSION
    assert res["id"] == "12345678-1234-5678-1234-567812345678"
    assert res["title"] == "Test sequence"
    assert res["description"] == "A sequence of geolocated pictures"
    assert res["providers"] == [
        {"name": "Default account", "roles": ["producer"]},
    ]
    assert res["keywords"] == ["pictures", "Test sequence"]
    assert res["license"] == "etalab-2.0"
    assert res["created"] == "2023-01-01T10:42:00+00:00"
    assert res["updated"] == "2023-01-01T11:42:00+00:00"
    assert res["extent"]["spatial"]["bbox"] == [[-1.0, -2.0, 1.0, 2.0]]
    assert res["extent"]["temporal"]["interval"] == [["2020-01-01T12:50:37+00:00", "2020-01-01T13:30:42+00:00"]]
    assert res["stats:items"]["count"] == 10
    assert len(res["links"]) == 5
    l = next(l for l in res["links"] if l["rel"] == "license")
    assert l["title"] == "License for this object (etalab-2.0)"
    assert l["href"] == "https://raw.githubusercontent.com/DISIC/politique-de-contribution-open-source/master/LICENSE"


def test_dbSequenceToStacCollectionEmptyTemporalInterval(client):
    dbSeq = {
        "id": UUID("{12345678-1234-5678-1234-567812345678}"),
        "name": "Test sequence",
        "minx": -1.0,
        "maxx": 1.0,
        "miny": -2.0,
        "maxy": 2.0,
        "mints": None,
        "inserted_at": datetime.fromisoformat("2023-01-01T12:42:00+02:00"),
        "account_name": "Default account",
    }

    res = stac.dbSequenceToStacCollection(dbSeq)

    assert res
    assert res["type"] == "Collection"
    assert res["stac_version"] == STAC_VERSION
    assert res["id"] == "12345678-1234-5678-1234-567812345678"
    assert res["title"] == "Test sequence"
    assert res["description"] == "A sequence of geolocated pictures"
    assert res["providers"] == [
        {"name": "Default account", "roles": ["producer"]},
    ]
    assert res["keywords"] == ["pictures", "Test sequence"]
    assert res["license"] == "etalab-2.0"
    assert res["created"] == "2023-01-01T10:42:00+00:00"
    assert res["extent"]["spatial"]["bbox"] == [[-1.0, -2.0, 1.0, 2.0]]
    assert res["extent"]["temporal"]["interval"] == [[None, None]]
    assert len(res["links"]) == 5


def test_dbSequenceToStacCollectionEmptyBbox(client):
    dbSeq = {
        "id": UUID("{12345678-1234-5678-1234-567812345678}"),
        "name": "Test sequence",
        "minx": None,
        "maxx": None,
        "miny": None,
        "maxy": None,
        "mints": datetime.fromisoformat("2020-01-01T12:50:37+00:00"),
        "maxts": datetime.fromisoformat("2020-01-01T13:30:42+00:00"),
        "inserted_at": datetime.fromisoformat("2023-01-01T12:42:00+02:00"),
        "account_name": "Default account",
    }

    res = stac.dbSequenceToStacCollection(dbSeq)

    assert res
    assert res["type"] == "Collection"
    assert res["stac_version"] == STAC_VERSION
    assert res["id"] == "12345678-1234-5678-1234-567812345678"
    assert res["title"] == "Test sequence"
    assert res["description"] == "A sequence of geolocated pictures"
    assert res["providers"] == [
        {"name": "Default account", "roles": ["producer"]},
    ]
    assert res["keywords"] == ["pictures", "Test sequence"]
    assert res["license"] == "etalab-2.0"
    assert res["created"] == "2023-01-01T10:42:00+00:00"
    assert res["extent"]["spatial"]["bbox"] == [[-180.0, -90.0, 180.0, 90.0]]

    l = next(l for l in res["links"] if l["rel"] == "license")
    assert l["title"] == "License for this object (etalab-2.0)"
    assert l["href"] == "https://raw.githubusercontent.com/DISIC/politique-de-contribution-open-source/master/LICENSE"


@pytest.fixture
def no_license_app_client(dburl, fsesUrl):
    app = create_app(
        {
            "TESTING": True,
            "DB_URL": dburl,
            "FS_URL": None,
            "FS_TMP_URL": fsesUrl.tmp,
            "FS_PERMANENT_URL": fsesUrl.permanent,
            "FS_DERIVATES_URL": fsesUrl.derivates,
            "SERVER_NAME": "localhost:5000",
            "PICTURE_PROCESS_DERIVATES_STRATEGY": "ON_DEMAND",
            "SECRET_KEY": "a very secret key",
        }
    )
    with app.app_context(), app.test_client() as client:
        yield client


def test_dbSequenceToStacCollectionNoLicense(no_license_app_client):
    dbSeq = {
        "id": UUID("{12345678-1234-5678-1234-567812345678}"),
        "name": "Test sequence",
        "minx": -1.0,
        "maxx": 1.0,
        "miny": -2.0,
        "maxy": 2.0,
        "mints": datetime.fromisoformat("2020-01-01T12:50:37+00:00"),
        "maxts": datetime.fromisoformat("2020-01-01T13:30:42+00:00"),
        "inserted_at": datetime.fromisoformat("2023-01-01T12:42:00+02:00"),
        "updated_at": datetime.fromisoformat("2023-01-01T13:42:00+02:00"),
        "account_name": "Default account",
    }

    res = stac.dbSequenceToStacCollection(dbSeq)

    assert res
    assert res["type"] == "Collection"
    assert res["stac_version"] == STAC_VERSION
    assert res["id"] == "12345678-1234-5678-1234-567812345678"
    assert res["title"] == "Test sequence"
    assert res["description"] == "A sequence of geolocated pictures"
    assert res["providers"] == [
        {"name": "Default account", "roles": ["producer"]},
    ]
    assert res["keywords"] == ["pictures", "Test sequence"]
    assert res["license"] == "proprietary"
    assert res["created"] == "2023-01-01T10:42:00+00:00"
    assert res["updated"] == "2023-01-01T11:42:00+00:00"
    assert res["extent"]["spatial"]["bbox"] == [[-1.0, -2.0, 1.0, 2.0]]
    assert res["extent"]["temporal"]["interval"] == [["2020-01-01T12:50:37+00:00", "2020-01-01T13:30:42+00:00"]]
    assert len(res["links"]) == 4
    rels = [l for l in res["links"] if l["rel"] == "license"]
    assert not rels


def test_no_license_main_endpoint(no_license_app_client):
    response = no_license_app_client.get("/api")
    assert response.status_code < 400

    # there should not be a license link since we do not know the license
    rels = [l for l in response.json["links"] if l["rel"] == "license"]
    assert not rels


def test_defined_license_main_endpoint(client):
    response = client.get("/api")
    assert response.status_code < 400

    # there should not be a license link since we do not know the license
    rels = [l for l in response.json["links"] if l["rel"] == "license"]
    assert len(rels) == 1
    l = rels[0]
    assert l == {
        "href": "https://raw.githubusercontent.com/DISIC/politique-de-contribution-open-source/master/LICENSE",
        "rel": "license",
        "title": "License for this object (etalab-2.0)",
    }


def test_collectionsEmpty(client):
    response = client.get("/api/collections")

    assert response.status_code == 200
    assert len(response.json["collections"]) == 0
    assert set((l["rel"] for l in response.json["links"])) == {"root", "parent", "self", "first"}


@conftest.SEQ_IMGS
def test_user_catalog(datafiles, dburl, initSequence):
    client = initSequence(datafiles, preprocess=False)

    # Get user ID
    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            userId, userName = cursor.execute("SELECT id, name FROM accounts WHERE is_default").fetchone()

            response = client.get("/api/users/" + str(userId) + "/catalog")
            data = response.json

            assert response.status_code == 200
            assert data["type"] == "Catalog"
            ctl = Catalog.from_dict(data)
            assert len(ctl.links) > 0
            assert ctl.title == userName + "'s sequences"
            assert ctl.id == f"user:{userId}"
            assert ctl.description == "List of all sequences of user " + userName
            assert ctl.extra_fields.get("extent") is None
            assert ctl.get_links("self")[0].get_absolute_href() == "http://localhost/api/users/" + str(userId) + "/catalog/"

            # Check links
            for link in ctl.get_links("child"):
                assert link.title is not None
                assert link.extra_fields["id"] is not None
                assert link.get_absolute_href() == "http://localhost/api/collections/" + link.extra_fields["id"]
                assert link.extra_fields["extent"]["temporal"] == {"interval": [["2021-07-29T09:16:54+00:00", "2021-07-29T09:17:02+00:00"]]}
                assert link.extra_fields["stats:items"]["count"] == 5


@conftest.SEQ_IMGS
def test_collections(datafiles, initSequence):
    client = initSequence(datafiles, preprocess=False)

    response = client.get("/api/collections")
    data = response.json

    assert response.status_code == 200

    assert len(data["collections"]) == 1
    assert len(data["links"]) == 5

    assert data["links"][0]["rel"] == "root"
    assert data["links"][0]["href"].endswith("/api/")
    assert data["links"][1]["rel"] == "parent"
    assert data["links"][1]["href"].endswith("/api/")
    assert data["links"][2]["rel"] == "self"
    assert data["links"][2]["href"].endswith("/api/collections")
    assert data["links"][3]["rel"] == "first"
    assert data["links"][3]["href"] == "http://localhost/api/collections?limit=100"
    assert data["links"][4]["rel"] == "last"
    assert "http://localhost/api/collections?limit=100&created_before=" in data["links"][4]["href"]

    clc = Collection.from_dict(data["collections"][0])

    assert data["collections"][0]["type"] == "Collection"
    assert data["collections"][0]["stac_version"] == STAC_VERSION
    assert len(data["collections"][0]["id"]) > 0
    assert len(data["collections"][0]["title"]) > 0
    assert data["collections"][0]["description"] == "A sequence of geolocated pictures"
    assert len(data["collections"][0]["keywords"]) > 0
    assert len(data["collections"][0]["license"]) > 0
    assert len(data["collections"][0]["extent"]["spatial"]["bbox"][0]) == 4
    assert len(data["collections"][0]["extent"]["temporal"]["interval"][0]) == 2
    assert len(data["collections"][0]["links"]) == 4
    assert data["collections"][0]["created"].startswith(date.today().isoformat())
    assert data["collections"][0]["stats:items"]["count"] == 5


@conftest.SEQ_IMGS
def test_collections_pagination_classic(datafiles, initSequence, dburl):
    client = initSequence(datafiles, preprocess=False)
    conftest.createManySequences(dburl)

    # Launch all calls against API
    nextLink = "/api/collections?limit=50"
    receivedLinks = []
    receivedSeqIds = []

    while nextLink:
        response = client.get(nextLink)
        assert response.status_code == 200

        myLinks = {l["rel"]: l["href"] for l in response.json["links"]}

        receivedLinks.append(myLinks)
        nextLink = myLinks.get("next")

        for c in response.json["collections"]:
            receivedSeqIds.append(c["id"])

    # Check received links
    for i, links in enumerate(receivedLinks):
        assert "root" in links
        assert "parent" in links
        assert "self" in links
        assert "/api/collections?limit=50" in links["self"]
        assert links["first"] == "http://localhost/api/collections?limit=50"
        assert "last" in links

        if i == 0:
            assert "next" in links
            assert "prev" not in links
        elif i == len(receivedLinks) - 1:
            assert "next" not in links
            assert "prev" in links
        else:
            assert "next" in links
            assert "prev" in links
            prevLinks = receivedLinks[i - 1]
            prevLinks["next"] = links["self"]
            prevLinks["self"] = links["prev"]
            nextLinks = receivedLinks[i + 1]
            links["next"] = nextLinks["self"]
            links["self"] = nextLinks["prev"]

    # Check received sequence IDS
    assert len(receivedSeqIds) == 1024
    assert len(set(receivedSeqIds)) == 1024


@conftest.SEQ_IMGS
def test_collections_pagination_descending(datafiles, initSequence, dburl):
    client = initSequence(datafiles, preprocess=False)
    conftest.createManySequences(dburl)

    # Call collections endpoint to get last page
    response = client.get("/api/collections?limit=50")
    assert response.status_code == 200

    lastLink = next((l for l in response.json["links"] if l["rel"] == "last"))

    # Launch all calls against API
    prevLink = lastLink["href"]
    receivedLinks = []
    receivedSeqIds = []

    while prevLink:
        response = client.get(prevLink)
        assert response.status_code == 200

        myLinks = {l["rel"]: l["href"] for l in response.json["links"]}

        receivedLinks.append(myLinks)
        prevLink = myLinks.get("prev")

        for c in response.json["collections"]:
            receivedSeqIds.append(c["id"])

    # Check received links
    for i, links in enumerate(receivedLinks):
        assert "root" in links
        assert "parent" in links
        assert "self" in links
        assert "/api/collections?limit=50" in links["self"]
        assert "first" in links
        assert links["first"].endswith("/api/collections?limit=50")
        assert "last" in links

        if i == 0:
            assert "next" not in links
            assert "prev" in links
        elif i == len(receivedLinks) - 1:
            assert "next" in links
            assert "prev" not in links
        else:
            assert "next" in links
            assert "prev" in links
            prevLinks = receivedLinks[i + 1]
            prevLinks["next"] = links["self"]
            prevLinks["self"] = links["prev"]
            nextLinks = receivedLinks[i - 1]
            links["next"] = nextLinks["self"]
            links["self"] = nextLinks["prev"]

    # Check received sequence IDS
    assert len(receivedSeqIds) == 1024
    assert len(set(receivedSeqIds)) == 1024


@conftest.SEQ_IMGS
def test_collections_pagination_outalimit(datafiles, initSequence):
    client = initSequence(datafiles, preprocess=False)

    response = client.get("/api/collections?limit=50&created_after=2100-01-01T10:00:00Z")
    assert response.status_code == 400
    assert response.json == {"message": "There is no collection created after 2100-01-01 10:00:00+00:00", "status_code": 400}

    response = client.get("/api/collections?limit=50&created_before=2000-01-01T10:00:00Z")
    assert response.status_code == 400
    assert response.json == {"message": "There is no collection created before 2000-01-01 10:00:00+00:00", "status_code": 400}

    response = client.get("/api/collections?limit=-1")
    assert response.status_code == 400
    assert response.json == {"message": "limit parameter should be an integer between 1 and 1000", "status_code": 400}

    response = client.get("/api/collections?limit=1001")
    assert response.status_code == 400
    assert response.json == {"message": "limit parameter should be an integer between 1 and 1000", "status_code": 400}


@conftest.SEQ_IMGS
def test_collections_created_date_filtering(datafiles, initSequence, dburl):
    from dateutil.tz import UTC

    client = initSequence(datafiles, preprocess=False)
    conftest.createManySequences(dburl)

    def get_creation_date(response):
        from dateutil.parser import parse as dateparser

        return sorted(dateparser(r["created"]) for r in response.json["collections"])

    response = client.get("/api/collections?limit=10")
    assert response.status_code == 200
    initial_creation_date = get_creation_date(response)
    last_date = initial_creation_date[-1]

    def compare_query(query, date, after):
        response = client.get(query)
        assert response.status_code == 200
        creation_dates = get_creation_date(response)
        assert creation_dates
        if after:
            assert all([d > date for d in creation_dates])
        else:
            assert all([d < date for d in creation_dates])

    compare_query(
        f"/api/collections?limit=10&created_after={last_date.strftime('%Y-%m-%dT%H:%M:%S')}", last_date.replace(microsecond=0), after=True
    )
    # date without hour should be ok
    compare_query(
        f"/api/collections?limit=10&created_after={last_date.strftime('%Y-%m-%d')}",
        datetime.combine(last_date.date(), last_date.min.time(), tzinfo=UTC),
        after=True,
    )
    compare_query(
        f"/api/collections?limit=10&created_after={last_date.strftime('%Y-%m-%dT%H:%M:%SZ')}", last_date.replace(microsecond=0), after=True
    )
    # isoformated date should work
    compare_query(
        f"/api/collections?limit=10&created_after={last_date.strftime('%Y-%m-%dT%H:%M:%S')}%2B00:00",
        last_date.replace(microsecond=0),
        after=True,
    )

    # same filters should work with the `created_before` parameter
    compare_query(
        f"/api/collections?limit=10&created_before={last_date.strftime('%Y-%m-%dT%H:%M:%S')}", last_date.replace(microsecond=0), after=False
    )
    compare_query(
        f"/api/collections?limit=10&created_before={last_date.strftime('%Y-%m-%d')}",
        datetime.combine(last_date.date(), last_date.min.time(), tzinfo=UTC),
        after=False,
    )
    compare_query(
        f"/api/collections?limit=10&created_before={last_date.strftime('%Y-%m-%dT%H:%M:%SZ')}",
        last_date.replace(microsecond=0),
        after=False,
    )
    compare_query(
        f"/api/collections?limit=10&created_before={last_date.strftime('%Y-%m-%dT%H:%M:%S')}%2B00:00",
        last_date.replace(microsecond=0),
        after=False,
    )

    # We can also filter by both created_before and created_after
    mid_date = initial_creation_date[int(len(initial_creation_date) / 2)]
    response = client.get(
        f"/api/collections?limit=10&created_before={last_date.strftime('%Y-%m-%dT%H:%M:%SZ')}&created_after={mid_date.strftime('%Y-%m-%dT%H:%M:%SZ')}"
    )
    assert response.status_code == 200
    creation_dates = get_creation_date(response)
    assert creation_dates
    assert all([d > mid_date.replace(microsecond=0) and d < last_date for d in creation_dates])


@conftest.SEQ_IMGS
def test_collections_invalid_created_after(datafiles, initSequence):
    client = initSequence(datafiles, preprocess=False)

    response = client.get("/api/collections?limit=50&created_after=pouet")
    assert response.status_code == 400
    assert response.json == {
        "details": {"error": "Unknown string format: pouet"},
        "message": "Invalid `created_after` argument",
        "status_code": 400,
    }


@conftest.SEQ_IMGS
def test_collections_hidden(datafiles, initSequence, dburl):
    client = initSequence(datafiles, preprocess=False)

    seqId, picId = conftest.getFirstPictureIds(dburl)

    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            cursor.execute("UPDATE sequences SET status = 'hidden'")
            conn.commit()

    response = client.get("/api/collections")
    assert response.status_code == 200
    assert len(response.json["collections"]) == 0


def test_collectionMissing(client):
    response = client.get("/api/collections/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


@conftest.SEQ_IMGS
def test_collectionById(datafiles, initSequence, dburl):
    client = initSequence(datafiles, preprocess=False)

    seqId, picId = conftest.getFirstPictureIds(dburl)

    response = client.get("/api/collections/" + str(seqId))
    data = response.json

    assert response.status_code == 200
    clc = Collection.from_dict(data)
    assert clc.extra_fields["stats:items"]["count"] == 5


@conftest.SEQ_IMGS
def test_items(datafiles, initSequence, dburl):
    client = initSequence(datafiles, preprocess=False)

    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            seqId = cursor.execute("SELECT id FROM sequences LIMIT 1").fetchone()[0]

            response = client.get("/api/collections/" + str(seqId) + "/items")
            data = response.json

            assert response.status_code == 200

            assert data["type"] == "FeatureCollection"
            assert len(data["features"]) == 5
            assert len(data["links"]) == 3

            clc = ItemCollection.from_dict(data)
            assert len(clc) == 5

            # Check if items have next/prev picture info
            i = 0
            for item in clc:
                nbPrev = len([l for l in item.links if l.rel == "prev"])
                nbNext = len([l for l in item.links if l.rel == "next"])
                if i == 0:
                    assert nbPrev == 0
                    assert nbNext == 1
                elif i == len(clc) - 1:
                    assert nbPrev == 1
                    assert nbNext == 0
                else:
                    assert nbPrev == 1
                    assert nbNext == 1

                i += 1

            # Make one picture not available
            picHidden = data["features"][0]["id"]
            cursor.execute("UPDATE pictures SET status = 'hidden' WHERE id = %s", [picHidden])
            conn.commit()

            response = client.get("/api/collections/" + str(seqId) + "/items")
            data = response.json

            assert response.status_code == 200

            assert data["type"] == "FeatureCollection"
            assert len(data["features"]) == 4
            picIds = [f["id"] for f in data["features"]]
            assert picHidden not in picIds
            assert data["features"][0]["providers"] == [
                {"name": "Default account", "roles": ["producer"]},
            ]


@conftest.SEQ_IMGS
def test_items_pagination_classic(datafiles, initSequence, dburl):
    """Linear test case : get page one by one, consecutively"""

    client = initSequence(datafiles, preprocess=False)
    seq = conftest.getPictureIds(dburl)[0]
    picIds = [p.id for p in seq.pictures]

    # First page
    response = client.get(f"/api/collections/{seq.id}/items?limit=2")
    data = response.json

    assert response.status_code == 200
    assert data["type"] == "FeatureCollection"

    clc = ItemCollection.from_dict(data)
    assert len(clc) == 2

    assert clc[0].id == picIds[0]
    assert clc[1].id == picIds[1]

    links = clc.extra_fields["links"]
    assert len(links) == 6

    assert links[0]["rel"] == "root"
    assert links[1]["rel"] == "parent"
    assert links[2]["rel"] == "self"
    assert links[2]["href"].endswith(f"/api/collections/{seq.id}/items?limit=2")
    assert links[3]["rel"] == "first"
    assert links[3]["href"].endswith(f"/api/collections/{seq.id}/items?limit=2")
    assert links[4]["rel"] == "next"
    assert links[4]["href"].endswith(f"/api/collections/{seq.id}/items?limit=2&startAfterRank=2")
    assert links[5]["rel"] == "last"
    assert links[5]["href"].endswith(f"/api/collections/{seq.id}/items?limit=2&startAfterRank=3")

    # Second page
    response = client.get(f"/api/collections/{seq.id}/items?limit=2&startAfterRank=2")
    data = response.json

    assert response.status_code == 200
    clc = ItemCollection.from_dict(data)
    assert len(clc) == 2
    links = clc.extra_fields["links"]
    assert len(links) == 7

    assert clc[0].id == picIds[2]
    assert clc[1].id == picIds[3]

    assert links[0]["rel"] == "root"
    assert links[1]["rel"] == "parent"
    assert links[2]["rel"] == "self"
    assert links[2]["href"].endswith(f"/api/collections/{seq.id}/items?limit=2&startAfterRank=2")
    assert links[3]["rel"] == "first"
    assert links[3]["href"].endswith(f"/api/collections/{seq.id}/items?limit=2")
    assert links[4]["rel"] == "prev"
    assert links[4]["href"].endswith(f"/api/collections/{seq.id}/items?limit=2")
    assert links[5]["rel"] == "next"
    assert links[5]["href"].endswith(f"/api/collections/{seq.id}/items?limit=2&startAfterRank=4")
    assert links[6]["rel"] == "last"
    assert links[6]["href"].endswith(f"/api/collections/{seq.id}/items?limit=2&startAfterRank=4")

    # Third page
    response = client.get(f"/api/collections/{seq.id}/items?limit=2&startAfterRank=4")
    data = response.json

    assert response.status_code == 200
    clc = ItemCollection.from_dict(data)
    assert len(clc) == 1
    links = clc.extra_fields["links"]
    assert len(links) == 6

    assert clc[0].id == picIds[4]

    assert links[0]["rel"] == "root"
    assert links[1]["rel"] == "parent"
    assert links[2]["rel"] == "self"
    assert links[2]["href"].endswith(f"/api/collections/{seq.id}/items?limit=2&startAfterRank=4")
    assert links[3]["rel"] == "first"
    assert links[3]["href"].endswith(f"/api/collections/{seq.id}/items?limit=2")
    assert links[4]["rel"] == "prev"
    assert links[4]["href"].endswith(f"/api/collections/{seq.id}/items?limit=2&startAfterRank=2")
    assert links[5]["rel"] == "last"
    assert links[5]["href"].endswith(f"/api/collections/{seq.id}/items?limit=2&startAfterRank=4")


@conftest.SEQ_IMGS
def test_items_pagination_nolimit(datafiles, initSequence, dburl):
    """Calling next without limit"""

    client = initSequence(datafiles, preprocess=False)
    seq = conftest.getPictureIds(dburl)[0]

    response = client.get(f"/api/collections/{seq.id}/items?startAfterRank=2")
    assert response.status_code == 200
    clc = ItemCollection.from_dict(response.json)
    assert len(clc) == 3
    links = clc.extra_fields["links"]
    assert len(links) == 6, [l["rel"] for l in links]

    assert clc[0].id == seq.pictures[2].id
    assert clc[1].id == seq.pictures[3].id
    assert clc[2].id == seq.pictures[4].id

    assert links[0]["rel"] == "root"
    assert links[1]["rel"] == "parent"
    assert links[2]["rel"] == "self"
    assert links[2]["href"].endswith(f"/api/collections/{seq.id}/items?startAfterRank=2")
    assert links[3]["rel"] == "first"
    assert links[3]["href"].endswith(f"/api/collections/{seq.id}/items")
    assert links[4]["rel"] == "prev"
    assert links[4]["href"].endswith(f"/api/collections/{seq.id}/items")
    assert links[5]["rel"] == "last"
    assert links[5]["href"].endswith(f"/api/collections/{seq.id}/items?startAfterRank=2")


@conftest.SEQ_IMGS
def test_items_pagination_outalimit(datafiles, initSequence, dburl):
    """Requests using invalid or out of limit values"""
    client = initSequence(datafiles, preprocess=False)
    seq = conftest.getPictureIds(dburl)[0]

    # Invalid limit
    for v in ["100000000000000000000", "prout", "-1"]:
        response = client.get("/api/collections/" + seq.id + "/items?limit=" + v)
        assert response.status_code == 400

    # Out of bounds next rank
    response = client.get("/api/collections/" + seq.id + "/items?startAfterRank=9000")
    assert response.status_code == 404
    assert response.json == {"message": "No more items in this collection (last available rank is 5)", "status_code": 404}

    # Remove everything
    with psycopg.connect(dburl, autocommit=True) as conn:
        conn.execute("DELETE FROM sequences_pictures")

    response = client.get("/api/collections/" + seq.id + "/items?limit=2")
    assert response.status_code == 200 and response.json["features"] == []


@conftest.SEQ_IMGS
def test_items_empty_collection(app, client, datafiles, initSequence, dburl, bobAccountToken):
    """Requests the items of an empty collection"""
    seq_location = conftest.createSequence(client, "a_sequence", jwtToken=bobAccountToken(app))
    seq_id = seq_location.split("/")[-1]

    # the collection is not ready (there is no pictures), so it is hidden by default
    response = client.get(f"/api/collections/{seq_id}/items")
    assert response.status_code == 404
    assert response.json == {"message": "Collection doesn't exist", "status_code": 404}

    # but bob see an empty collection
    response = client.get(f"/api/collections/{seq_id}/items", headers={"Authorization": f"Bearer {bobAccountToken(app)}"})
    assert response.status_code == 200 and response.json["features"] == []


@conftest.SEQ_IMGS
def test_items_withPicture_no_limit(datafiles, initSequence, dburl):
    """Asking for a page with a specific picture in it"""

    client = initSequence(datafiles, preprocess=False)
    seq = conftest.getPictureIds(dburl)[0]
    pic_ids = [p.id for p in seq.pictures]

    response = client.get(f"/api/collections/{seq.id}/items?withPicture={seq.pictures[1].id}")
    assert response.status_code == 200
    clc = ItemCollection.from_dict(response.json)
    assert len(clc) == 4
    links = {l["rel"]: l["href"] for l in clc.extra_fields["links"]}
    # we should have all the pagination links
    assert links == {
        "root": "http://localhost/api/",
        "parent": f"http://localhost/api/collections/{seq.id}",
        "first": f"http://localhost/api/collections/{seq.id}/items",
        "last": f"http://localhost/api/collections/{seq.id}/items",
        "self": f"http://localhost/api/collections/{seq.id}/items",
    }

    assert [c.id for c in clc] == pic_ids[1:]


@conftest.SEQ_IMGS
def test_items_withPicture_with_limit(datafiles, initSequence, dburl):
    """
    Asking for a page with a specific picture in it with a limit, we should get the nth page with the picture
    There is 5 pics, if we ask for the fourth pic, with a limit=2, we should get a page with the third and the fourth pic
    """
    client = initSequence(datafiles, preprocess=False)
    seq = conftest.getPictureIds(dburl)[0]
    pic_ids = [p.id for p in seq.pictures]

    response = client.get(f"/api/collections/{seq.id}/items?withPicture={seq.pictures[3].id}&limit=2")
    assert response.status_code == 200
    clc = ItemCollection.from_dict(response.json)
    assert len(clc) == 2
    links = {l["rel"]: l["href"] for l in clc.extra_fields["links"]}
    # we should have all the pagination links
    assert links == {
        "root": "http://localhost/api/",
        "parent": f"http://localhost/api/collections/{seq.id}",
        "first": f"http://localhost/api/collections/{seq.id}/items?limit=2",
        "last": f"http://localhost/api/collections/{seq.id}/items?limit=2&startAfterRank=4",
        "next": f"http://localhost/api/collections/{seq.id}/items?limit=2&startAfterRank=4",
        "self": f"http://localhost/api/collections/{seq.id}/items?limit=2",
    }

    assert [c.id for c in clc] == pic_ids[2:4]


@conftest.SEQ_IMGS
@conftest.SEQ_IMGS_FLAT
def test_items_withPicture_invalid(datafiles, initSequence, dburl):
    client = initSequence(datafiles, preprocess=False)
    seqs = conftest.getPictureIds(dburl)

    response = client.get(f"/api/collections/{seqs[0].id}/items?withPicture=plop")
    assert response.status_code == 400
    assert response.json == {"message": "withPicture should be a valid UUID", "status_code": 400}

    response = client.get(f"/api/collections/{seqs[0].id}/items?withPicture=00000000-0000-0000-0000-000000000000")
    assert response.status_code == 400
    assert response.json == {"message": "Picture with id 00000000-0000-0000-0000-000000000000 does not exists", "status_code": 400}

    # asking for a picture in another collection should also trigger an error
    response = client.get(f"/api/collections/{seqs[0].id}/items?withPicture={seqs[1].pictures[0].id}")
    assert response.status_code == 400
    assert response.json == {"message": f"Picture with id {seqs[1].pictures[0].id} does not exists", "status_code": 400}


@conftest.SEQ_IMGS
def test_items_pagination_nonconsecutive(datafiles, initSequence, dburl):
    """Pagination over non-consecutive pictures ranks"""

    client = initSequence(datafiles, preprocess=False)

    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            seq = conftest.getPictureIds(dburl)[0]

            cursor.execute("DELETE FROM sequences_pictures WHERE rank IN (1, 3)")
            conn.commit()

            # Calling on sequence start
            response = client.get(f"/api/collections/{seq.id}/items?limit=2")

            assert response.status_code == 200
            clc = ItemCollection.from_dict(response.json)
            assert len(clc) == 2
            links = clc.extra_fields["links"]
            assert len(links) == 6

            assert clc[0].id == seq.pictures[1].id
            assert clc[1].id == seq.pictures[3].id

            assert links[0]["rel"] == "root"
            assert links[1]["rel"] == "parent"
            assert links[2]["rel"] == "self"
            assert links[2]["href"].endswith(f"/api/collections/{seq.id}/items?limit=2")
            assert links[3]["rel"] == "first"
            assert links[3]["href"].endswith(f"/api/collections/{seq.id}/items?limit=2")
            assert links[4]["rel"] == "next"
            assert links[4]["href"].endswith(f"/api/collections/{seq.id}/items?limit=2&startAfterRank=4")
            assert links[5]["rel"] == "last"
            assert links[5]["href"].endswith(f"/api/collections/{seq.id}/items?limit=2&startAfterRank=4")

            # Calling on the middle
            response = client.get(f"/api/collections/{seq.id}/items?limit=2&startAfterRank=2")

            assert response.status_code == 200
            clc = ItemCollection.from_dict(response.json)
            assert len(clc) == 2
            links = clc.extra_fields["links"]
            assert len(links) == 6

            assert clc[0].id == seq.pictures[3].id
            assert clc[1].id == seq.pictures[4].id

            assert links[0]["rel"] == "root"
            assert links[1]["rel"] == "parent"
            assert links[2]["rel"] == "self"
            assert links[2]["href"].endswith(f"/api/collections/{seq.id}/items?limit=2&startAfterRank=2")
            assert links[3]["rel"] == "first"
            assert links[3]["href"].endswith(f"/api/collections/{seq.id}/items?limit=2")
            assert links[4]["rel"] == "prev"
            assert links[4]["href"].endswith(f"/api/collections/{seq.id}/items?limit=2")
            assert links[5]["rel"] == "last"
            assert links[5]["href"].endswith(f"/api/collections/{seq.id}/items?limit=2&startAfterRank=2")


@conftest.SEQ_IMGS
def test_item(datafiles, initSequence, dburl):
    client = initSequence(datafiles, preprocess=False)

    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            seqId, picId = cursor.execute("SELECT seq_id, pic_id FROM sequences_pictures WHERE rank = 1").fetchone()

            response = client.get("/api/collections/" + str(seqId) + "/items/" + str(picId))

            assert response.status_code == 200
            data = response.json

            assert data["type"] == "Feature"
            assert data["geometry"]["type"] == "Point"
            assert len(str(data["id"])) > 0
            assert re.match(r"^2021-07-29T", data["properties"]["datetime"])
            assert data["properties"]["view:azimuth"] >= 0
            assert data["properties"]["view:azimuth"] <= 360
            assert re.match(
                r"^https?://.*/api/pictures/" + str(picId) + r"/tiled/\{TileCol\}_\{TileRow\}.jpg$",
                data["asset_templates"]["tiles"]["href"],
            )
            assert re.match(r"^https?://.*/api/pictures/" + str(picId) + "/hd.jpg$", data["assets"]["hd"]["href"])
            assert re.match(r"^https?://.*/api/pictures/" + str(picId) + "/sd.jpg$", data["assets"]["sd"]["href"])
            assert re.match(r"^https?://.*/api/pictures/" + str(picId) + "/thumb.jpg$", data["assets"]["thumb"]["href"])
            assert data["properties"]["tiles:tile_matrix_sets"]["geovisio"]["tileMatrix"][0]["tileWidth"] == 720
            assert data["properties"]["tiles:tile_matrix_sets"]["geovisio"]["tileMatrix"][0]["tileHeight"] == 720
            assert data["properties"]["tiles:tile_matrix_sets"]["geovisio"]["tileMatrix"][0]["matrixHeight"] == 4
            assert data["properties"]["tiles:tile_matrix_sets"]["geovisio"]["tileMatrix"][0]["matrixWidth"] == 8
            assert data["properties"]["pers:interior_orientation"]["camera_manufacturer"] == "GoPro"
            assert data["properties"]["pers:interior_orientation"]["camera_model"] == "Max"
            assert data["properties"]["pers:interior_orientation"]["field_of_view"] == 360
            assert data["properties"]["created"].startswith(date.today().isoformat())
            assert data["properties"]["geovisio:status"] == "ready"
            assert data["providers"] == [
                {"name": "Default account", "roles": ["producer"]},
            ]

            item = Item.from_dict(data)
            assert len(item.links) == 5
            assert len([l for l in item.links if l.rel == "next"]) == 1

            # Make picture not available
            cursor.execute("UPDATE pictures SET status = 'hidden' WHERE id = %s", [picId])
            conn.commit()

            response = client.get("/api/collections/" + str(seqId) + "/items/" + str(picId))
            assert response.status_code == 404


@conftest.SEQ_IMGS_FLAT
def test_item_flat(datafiles, initSequence, dburl):
    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO cameras VALUES ('OLYMPUS IMAGING CORP. SP-720UZ', 6.16) ON CONFLICT DO NOTHING")
            conn.commit()

            client = initSequence(datafiles, preprocess=False)

            seqId, picId = cursor.execute("SELECT seq_id, pic_id FROM sequences_pictures WHERE rank = 1").fetchone()

            response = client.get("/api/collections/" + str(seqId) + "/items/" + str(picId))
            data = response.json

            assert response.status_code == 200

            assert data["type"] == "Feature"
            assert data["geometry"]["type"] == "Point"
            assert len(str(data["id"])) > 0
            assert re.match(r"^2015-04-25T", data["properties"]["datetime"])
            assert data["properties"]["view:azimuth"] >= 0
            assert data["properties"]["view:azimuth"] <= 360
            assert re.match(r"^https?://.*/api/pictures/" + str(picId) + "/hd.jpg$", data["assets"]["hd"]["href"])
            assert re.match(r"^https?://.*/api/pictures/" + str(picId) + "/sd.jpg$", data["assets"]["sd"]["href"])
            assert re.match(r"^https?://.*/api/pictures/" + str(picId) + "/thumb.jpg$", data["assets"]["thumb"]["href"])
            assert "assert_templates" not in data
            assert "tiles:tile_matrix_sets" not in data["properties"]
            assert data["properties"]["pers:interior_orientation"]["camera_manufacturer"] == "OLYMPUS IMAGING CORP."
            assert data["properties"]["pers:interior_orientation"]["camera_model"] == "SP-720UZ"
            assert data["properties"]["pers:interior_orientation"]["field_of_view"] == 67
            assert data["properties"]["created"].startswith(date.today().isoformat())

            item = Item.from_dict(data)
            assert len(item.links) == 5
            assert len([l for l in item.links if l.rel == "next"]) == 1


@conftest.SEQ_IMG_FLAT
def test_item_flat_fov(datafiles, initSequence, dburl):
    client = initSequence(datafiles, preprocess=False)
    seqId, picId = conftest.getFirstPictureIds(dburl)

    response = client.get("/api/collections/" + str(seqId) + "/items/" + str(picId))
    data = response.json

    assert response.status_code == 200

    assert len(str(data["id"])) > 0
    assert data["properties"]["pers:interior_orientation"]["camera_manufacturer"] == "Canon"
    assert data["properties"]["pers:interior_orientation"]["camera_model"] == "EOS 6D0"
    assert "field_of_view" not in data["properties"]["pers:interior_orientation"]  # Not in cameras DB


@conftest.SEQ_IMG_FLAT
def test_item_missing_all_metadata(datafiles, initSequence, dburl):
    client = initSequence(datafiles, preprocess=False)

    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            seqId, picId = cursor.execute("SELECT seq_id, pic_id FROM sequences_pictures WHERE rank = 1").fetchone()

            # Remove EXIF metadata from DB
            cursor.execute(
                "UPDATE pictures SET metadata = %s WHERE id = %s",
                [
                    '{"ts": 1430744932.0, "lat": 48.85779642035038, "lon": 2.3392783047650747, "type": "flat", "width": 4104, "height": 2736, "heading": 302}',
                    picId,
                ],
            )
            conn.commit()

            response = client.get("/api/collections/" + str(seqId) + "/items/" + str(picId))
            data = response.json

            assert response.status_code == 200

            assert len(str(data["id"])) > 0
            assert len(data["properties"]["pers:interior_orientation"]) == 0


@conftest.SEQ_IMG_FLAT
@pytest.mark.parametrize(("status", "httpCode"), (("ready", 200), ("hidden", 404), ("preparing", 102), ("broken", 500)))
def test_item_status_httpcode(datafiles, initSequence, dburl, status, httpCode):
    client = initSequence(datafiles, preprocess=False)

    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            seqId, picId = cursor.execute("SELECT seq_id, pic_id FROM sequences_pictures WHERE rank = 1").fetchone()

            # Remove EXIF metadata from DB
            cursor.execute("UPDATE pictures SET status = %s WHERE id = %s", [status, picId])
            conn.commit()

            response = client.get("/api/collections/" + str(seqId) + "/items/" + str(picId))
            assert response.status_code == httpCode


@conftest.SEQ_IMG_FLAT
def test_item_missing_partial_metadata(datafiles, initSequence, dburl):
    client = initSequence(datafiles, preprocess=False)

    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            seqId, picId = cursor.execute("SELECT seq_id, pic_id FROM sequences_pictures WHERE rank = 1").fetchone()

            # Remove EXIF metadata from DB
            cursor.execute(
                "UPDATE pictures SET metadata = %s WHERE id = %s",
                [
                    '{"ts": 1430744932.0, "lat": 48.85779642035038, "lon": 2.3392783047650747, "make": "Canon", "type": "flat", "width": 4104, "height": 2736, "heading": 302}',
                    picId,
                ],
            )
            conn.commit()

            response = client.get("/api/collections/" + str(seqId) + "/items/" + str(picId))
            data = response.json

            assert response.status_code == 200

            assert len(str(data["id"])) > 0
            assert data["properties"]["pers:interior_orientation"] == {"camera_manufacturer": "Canon"}


intersectsGeojson1 = json.dumps(
    {
        "type": "Polygon",
        "coordinates": [
            [
                [1.9191969931125639, 49.00691313179996],
                [1.9191332906484602, 49.00689685694783],
                [1.9191691651940344, 49.00687024535389],
                [1.919211409986019, 49.006892018477274],
                [1.9191969931125639, 49.00691313179996],
            ]
        ],
    }
)
intersectsGeojson2 = json.dumps({"type": "Point", "coordinates": [1.919185442, 49.00688962]})


@pytest.mark.parametrize(
    ("limit", "bbox", "datetime", "intersects", "ids", "collections", "httpCode", "validRanks"),
    (
        (None, None, None, None, None, None, 200, [1, 2, 3, 4, 5]),
        (2, None, None, None, None, None, 200, None),
        (-1, None, None, None, None, None, 400, None),
        (99999, None, None, None, None, None, 400, None),
        ("bla", None, None, None, None, None, 400, None),
        (None, [0, 0, 1, 1], None, None, None, None, 200, []),
        (None, "[0,0,1,1", None, None, None, None, 400, None),
        (None, [1], None, None, None, None, 400, None),
        (None, [1.919185, 49.00688, 1.919187, 49.00690], None, None, None, None, 200, [1]),
        (None, None, "2021-07-29T11:16:54+02", None, None, None, 200, [1]),
        (None, None, "2021-07-29T00:00:00Z/..", None, None, None, 200, [1, 2, 3, 4, 5]),
        (None, None, "../2021-07-29T00:00:00Z", None, None, None, 200, []),
        (None, None, "2021-01-01T00:00:00Z/2021-07-29T11:16:58+02", None, None, None, 200, [1, 2, 3]),
        (None, None, "2021-01-01T00:00:00Z/", None, None, None, 400, None),
        (None, None, "/2021-01-01T00:00:00Z", None, None, None, 400, None),
        (None, None, "..", None, None, None, 400, None),
        (None, None, "2021-07-29TNOTATIME", None, None, None, 400, None),
        (None, None, None, intersectsGeojson1, None, None, 200, [1, 2]),
        (None, None, None, intersectsGeojson2, None, None, 200, [1]),
        (None, None, None, "{ 'broken': ''", None, None, 400, None),
        (None, None, None, "{ 'type': 'Feature' }", None, None, 400, None),
        (None, None, None, None, [1, 2], None, 200, [1, 2]),
        (None, None, None, None, None, True, 200, [1, 2, 3, 4, 5]),
    ),
)
@conftest.SEQ_IMGS
def test_search(datafiles, initSequence, dburl, limit, bbox, datetime, intersects, ids, collections, httpCode, validRanks):
    client = initSequence(datafiles, preprocess=False)

    # Transform input ranks into picture ID to pass to query
    if ids is not None and len(ids) > 0:
        with psycopg.connect(dburl) as conn:
            with conn.cursor() as cursor:
                ids = json.dumps(
                    cursor.execute(
                        "SELECT array_to_json(array_agg(pic_id::varchar)) FROM sequences_pictures WHERE rank = ANY(%s)", [ids]
                    ).fetchone()[0]
                )

    # Retrieve sequence ID to pass into collections in query
    if collections is True:
        with psycopg.connect(dburl) as conn:
            with conn.cursor() as cursor:
                collections = json.dumps([cursor.execute("SELECT id::varchar FROM sequences").fetchone()[0]])

    query = {"limit": limit, "bbox": bbox, "datetime": datetime, "intersects": intersects, "ids": ids, "collections": collections}
    query = dict(filter(lambda val: val[1] is not None, query.items()))

    response = client.get("/api/search?" + urlencode(query))

    assert response.status_code == httpCode

    if httpCode == 200:
        clc = ItemCollection.from_dict(response.json)

        # all search response should have a link to the root of the stac catalog
        assert response.json["links"] == [
            {"rel": "root", "href": "http://localhost/api/", "title": "Instance catalog", "type": "application/json"}
        ]
        if validRanks is not None:
            assert len(clc) == len(validRanks)

            if len(validRanks) > 0:
                with psycopg.connect(dburl) as db:
                    validIds = db.execute(
                        "SELECT array_agg(pic_id ORDER BY rank) FROM sequences_pictures WHERE rank = ANY(%s)", [validRanks]
                    ).fetchone()[0]
                    allIds = db.execute("SELECT array_agg(pic_id ORDER BY rank) FROM sequences_pictures").fetchone()[0]
                    resIds = [UUID(item.id) for item in clc]
                    assert sorted(resIds) == sorted(validIds)

                    for i in range(len(validRanks)):
                        r = validRanks[i]
                        id = validIds[i]
                        links = [it.links for it in clc.items if it.id == str(id)][0]
                        if r == 1:
                            assert [l.target.split("/").pop() for l in links if l.rel == "next"] == [str(allIds[r])]
                            assert [l.target.split("/").pop() for l in links if l.rel == "prev"] == []
                        elif r == 5:
                            assert [l.target.split("/").pop() for l in links if l.rel == "next"] == []
                            assert [l.target.split("/").pop() for l in links if l.rel == "prev"] == [str(allIds[r - 2])]
                        else:
                            assert [l.target.split("/").pop() for l in links if l.rel == "next"] == [str(allIds[r])]
                            assert [l.target.split("/").pop() for l in links if l.rel == "prev"] == [str(allIds[r - 2])]

        elif limit is not None:
            assert len(clc) == limit


@conftest.SEQ_IMGS
def test_search_post(datafiles, initSequence):
    client = initSequence(datafiles, preprocess=False)

    response = client.post("/api/search", json={"limit": 1, "intersects": intersectsGeojson1})
    data = response.json

    assert response.status_code == 200
    clc = ItemCollection.from_dict(data)
    assert len(clc) == 1


def test_post_collection_nobody(client, dburl):
    response = client.post("/api/collections")

    assert response.status_code == 200
    assert response.headers.get("Location").startswith("http://localhost:5000/api/collections/")
    seqId = UUID(response.headers.get("Location").split("/").pop())
    assert seqId != ""

    # Check if JSON is a valid STAC collection
    assert response.json["type"] == "Collection"
    assert response.json["id"] == str(seqId)
    # the collection is associated to the default account since no auth was done
    assert response.json["providers"] == [{"name": "Default account", "roles": ["producer"]}]

    # Check if collection exists in DB
    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            seqStatus = cursor.execute("SELECT status FROM sequences WHERE id = %s", [seqId]).fetchone()[0]
            assert seqStatus == "waiting-for-process"


@conftest.SEQ_IMGS
def test_search_hidden_pic(datafiles, initSequenceApp, dburl, bobAccountToken):
    client, app = initSequenceApp(datafiles, withBob=True)
    sequence = conftest.getPictureIds(dburl)[0]
    assert len(sequence.pictures) == 5

    # hide sequence
    response = client.patch(
        f"/api/collections/{sequence.id}", data={"visible": "false"}, headers={"Authorization": f"Bearer {bobAccountToken(app)}"}
    )
    assert response.status_code == 200

    # searching the sequence should result in an empty set
    response = client.get(f'/api/search?collections=["{sequence.id}"]')
    assert response.status_code == 200, response
    assert len(response.json["features"]) == 0

    # searching the picture should result in an empty set
    for p in sequence.pictures:
        response = client.get(f'/api/search?ids=["{p.id}"]')
        assert response.status_code == 200
        assert len(response.json["features"]) == 0


@conftest.SEQ_IMGS
def test_search_hidden_pic_as_owner(datafiles, initSequenceApp, dburl, bobAccountToken):
    """
    Searching for hidden pic change if it's the owner that searches
    """
    client, app = initSequenceApp(datafiles, withBob=True)
    sequence = conftest.getPictureIds(dburl)[0]
    assert len(sequence.pictures) == 5

    # hide sequence
    response = client.patch(
        f"/api/collections/{sequence.id}", data={"visible": "false"}, headers={"Authorization": f"Bearer {bobAccountToken(app)}"}
    )
    assert response.status_code == 200

    # searching the sequence as Bob should return all pictures
    response = client.get(f'/api/search?collections=["{sequence.id}"]', headers={"Authorization": f"Bearer {bobAccountToken(app)}"})
    assert response.status_code == 200
    assert len(response.json["features"]) == 5

    # searching the picture as Bob should also result in an empty set, event if it's the owner
    for p in sequence.pictures:
        response = client.get(f'/api/search?ids=["{p.id}"]', headers={"Authorization": f"Bearer {bobAccountToken(app)}"})
        assert response.status_code == 200
        assert len(response.json["features"]) == 1


@conftest.SEQ_IMGS
def test_get_hidden_sequence(datafiles, initSequenceApp, dburl, bobAccountToken):
    client, app = initSequenceApp(datafiles, withBob=True)
    sequence = conftest.getPictureIds(dburl)[0]
    assert len(sequence.pictures) == 5

    # hide sequence
    response = client.patch(
        f"/api/collections/{sequence.id}", data={"visible": "false"}, headers={"Authorization": f"Bearer {bobAccountToken(app)}"}
    )
    assert response.status_code == 200
    assert response.json["geovisio:status"] == "hidden"

    # status should be set to hidden in db
    with psycopg.connect(dburl) as conn, conn.cursor() as cursor:
        seqStatus = cursor.execute("SELECT status FROM sequences WHERE id = %s", [sequence.id]).fetchone()
        assert seqStatus
        assert seqStatus[0] == "hidden"

    # The sequence is hidden, public call cannot see it, only Bob
    r = client.get(f"/api/collections/{sequence.id}")
    assert r.status_code == 404
    r = client.get(f"/api/collections/{sequence.id}/items")
    assert r.status_code == 404

    # same for the list of items in the collection
    r = client.get(f"/api/collections/{sequence.id}", headers={"Authorization": f"Bearer {bobAccountToken(app)}"})
    assert r.status_code == 200
    r = client.get(f"/api/collections/{sequence.id}/items", headers={"Authorization": f"Bearer {bobAccountToken(app)}"})
    assert r.status_code == 200
    assert len(r.json["features"]) == 5

    for p in sequence.pictures:
        r = client.get(f"/api/collections/{sequence.id}/items/{p.id}")
        assert r.status_code == 404

        r = client.get(f"/api/collections/{sequence.id}/items/{p.id}", headers={"Authorization": f"Bearer {bobAccountToken(app)}"})
        assert r.status_code == 200

    # other sequence's routes are also unavailable for public access
    r = client.get(f"/api/collections/{sequence.id}/geovisio_status")
    assert r.status_code == 404
    r = client.get(f"/api/collections/{sequence.id}/geovisio_status", headers={"Authorization": f"Bearer {bobAccountToken(app)}"})
    assert r.status_code == 200

    # if we set the sequence back to public, it should be fine for everybody
    response = client.patch(
        f"/api/collections/{sequence.id}", data={"visible": "true"}, headers={"Authorization": f"Bearer {bobAccountToken(app)}"}
    )
    assert response.status_code == 200

    assert client.get(f"/api/collections/{sequence.id}").status_code == 200
    for p in sequence.pictures:
        assert client.get(f"/api/collections/{sequence.id}/items/{p.id}").status_code == 200


@conftest.SEQ_IMGS
def test_get_hidden_sequence_and_pictures(datafiles, initSequenceApp, dburl, bobAccountToken):
    """
    If we:
            * hide the pictures n°1
            * hide the sequence
            * un-hide the sequence

    The pictures n°1 should stay hidden
    """
    client, app = initSequenceApp(datafiles, withBob=True)
    sequence = conftest.getPictureIds(dburl)[0]
    assert len(sequence.pictures) == 5

    # hide pic
    response = client.patch(
        f"/api/collections/{sequence.id}/items/{sequence.pictures[0].id}",
        data={"visible": "false"},
        headers={"Authorization": f"Bearer {bobAccountToken(app)}"},
    )

    r = client.get(f"/api/collections/{sequence.id}/items/{sequence.pictures[0].id}")
    assert r.status_code == 404

    # hide sequence
    response = client.patch(
        f"/api/collections/{sequence.id}", data={"visible": "false"}, headers={"Authorization": f"Bearer {bobAccountToken(app)}"}
    )
    assert response.status_code == 200

    r = client.get(f"/api/collections/{sequence.id}")
    assert r.status_code == 404

    # set the sequence to visible
    response = client.patch(
        f"/api/collections/{sequence.id}", data={"visible": "true"}, headers={"Authorization": f"Bearer {bobAccountToken(app)}"}
    )
    assert response.status_code == 200
    r = client.get(f"/api/collections/{sequence.id}")
    assert r.status_code == 200

    # but the pic is still hidden
    r = client.get(f"/api/collections/{sequence.id}/items/{sequence.pictures[0].id}")
    assert r.status_code == 404


@conftest.SEQ_IMGS
def test_invalid_sequence_hide(datafiles, initSequenceApp, dburl, bobAccountToken):
    client, app = initSequenceApp(datafiles, withBob=True)
    sequence = conftest.getPictureIds(dburl)[0]

    # hide pic
    response = client.patch(
        f"/api/collections/{sequence.id}", data={"visible": "invalid_value"}, headers={"Authorization": f"Bearer {bobAccountToken(app)}"}
    )
    assert response.status_code == 400


@conftest.SEQ_IMGS
def test_hide_unexisting_seq(datafiles, initSequenceApp, dburl, bobAccountToken):
    client, app = initSequenceApp(datafiles, withBob=True)

    response = client.patch(
        f"/api/collections/00000000-0000-0000-0000-000000000000",
        data={"visible": "false"},
        headers={"Authorization": f"Bearer {bobAccountToken(app)}"},
    )
    assert response.status_code == 404
    assert response.json == {"message": "Sequence 00000000-0000-0000-0000-000000000000 wasn't found in database", "status_code": 404}


@conftest.SEQ_IMGS
def test_empty_sequence_patch(datafiles, initSequenceApp, dburl, bobAccountToken):
    client, app = initSequenceApp(datafiles, withBob=True)
    sequence = conftest.getPictureIds(dburl)[0]

    response = client.patch(
        f"/api/collections/{sequence.id}/items/{sequence.pictures[0].id}", headers={"Authorization": f"Bearer {bobAccountToken(app)}"}
    )
    # changing no value is valid, and should result if the same thing as a get
    assert response.status_code == 200


@conftest.SEQ_IMGS
def test_anomynous_sequence_patch(datafiles, initSequenceApp, dburl):
    """Patching a sequence as an unauthentified user should result in an error"""
    client, app = initSequenceApp(datafiles, withBob=True)
    sequence = conftest.getPictureIds(dburl)[0]

    response = client.patch(
        f"/api/collections/{sequence.id}",
    )
    assert response.status_code == 401
    assert response.json == {"message": "Authentication is mandatory"}


@conftest.SEQ_IMGS
def test_set_already_visible_sequence(datafiles, initSequenceApp, dburl, bobAccountToken):
    """Setting an already visible sequence to visible is valid, and change nothing"""
    client, app = initSequenceApp(datafiles, withBob=True)
    sequence = conftest.getPictureIds(dburl)[0]

    # hide sequence
    p = client.patch(
        f"/api/collections/{sequence.id}", data={"visible": "true"}, headers={"Authorization": f"Bearer {bobAccountToken(app)}"}
    )
    assert p.status_code == 200
    r = client.get(f"/api/collections/{sequence.id}")
    assert r.status_code == 200


@conftest.SEQ_IMGS
def test_picture_next_hidden(datafiles, initSequenceApp, dburl, bobAccountToken):
    """
    if pic n°3 is hidden:
    * for anonymous call, the next link of pic n°2 should be pic n°4 and previous link of pic n°4 should be pic n°2
    * for the owner, the next link of pic n°2 should be pic n°3 and previous link of pic n°4 should be pic n°3
    """
    client, app = initSequenceApp(datafiles, withBob=True)
    sequence = conftest.getPictureIds(dburl)[0]
    assert len(sequence.pictures) == 5

    response = client.patch(
        f"/api/collections/{str(sequence.id)}/items/{sequence.pictures[2].id}",
        data={"visible": "false"},
        headers={"Authorization": f"Bearer {bobAccountToken(app)}"},
    )
    assert response.status_code == 200

    r = client.get(f"/api/collections/{sequence.id}/items/{sequence.pictures[2].id}")
    assert r.status_code == 404

    def _get_prev_link(r):
        return next(l for l in r.json["links"] if l["rel"] == "prev")

    def _get_next_link(r):
        return next(l for l in r.json["links"] if l["rel"] == "next")

    pic2 = client.get(f"/api/collections/{sequence.id}/items/{sequence.pictures[1].id}")
    assert pic2.status_code == 200
    next_link = _get_next_link(pic2)
    assert next_link["id"] == str(sequence.pictures[3].id)
    pic4 = client.get(f"/api/collections/{sequence.id}/items/{sequence.pictures[3].id}")
    assert pic4.status_code == 200
    prev_link = _get_prev_link(pic4)
    assert prev_link["id"] == str(sequence.pictures[1].id)

    # but calling this as the owner should return the right links
    pic2 = client.get(
        f"/api/collections/{sequence.id}/items/{sequence.pictures[1].id}", headers={"Authorization": f"Bearer {bobAccountToken(app)}"}
    )
    assert pic2.status_code == 200
    next_link = _get_next_link(pic2)
    assert next_link["id"] == str(sequence.pictures[2].id)
    pic4 = client.get(
        f"/api/collections/{sequence.id}/items/{sequence.pictures[3].id}", headers={"Authorization": f"Bearer {bobAccountToken(app)}"}
    )
    assert pic4.status_code == 200
    prev_link = _get_prev_link(pic4)
    assert prev_link["id"] == str(sequence.pictures[2].id)


@conftest.SEQ_IMGS
def test_patch_collection_contenttype(datafiles, initSequenceApp, dburl, bobAccountToken):
    """Setting an already visible sequence to visible is valid, and change nothing"""
    client, app = initSequenceApp(datafiles, withBob=True)
    sequence = conftest.getPictureIds(dburl)[0]

    # hide sequence
    p = client.patch(
        f"/api/collections/{sequence.id}",
        data={"visible": "false"},
        headers={"Content-Type": "multipart/form-data; whatever=blabla", "Authorization": f"Bearer {bobAccountToken(app)}"},
    )

    assert p.status_code == 200

    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            newStatus = cursor.execute("SELECT status FROM sequences WHERE id = %s", [sequence.id]).fetchone()[0]
            assert newStatus == "hidden"


@conftest.SEQ_IMGS
def test_not_owned_sequence_patch(datafiles, initSequenceApp, dburl, defaultAccountToken):
    """Patching a sequence that does not belong to us should result in an error"""
    client, app = initSequenceApp(datafiles, withBob=True)  # the sequence belongs to Bob
    sequence = conftest.getPictureIds(dburl)[0]

    response = client.patch(
        f"/api/collections/{sequence.id}", data={"visible": "true"}, headers={"Authorization": f"Bearer {defaultAccountToken(app)}"}
    )
    assert response.status_code == 403


def test_post_collection_body_form(client):
    response = client.post("/api/collections", data={"title": "Séquence"})

    assert response.status_code == 200
    assert response.headers.get("Location").startswith("http://localhost:5000/api/collections/")
    seqId = UUID(response.headers.get("Location").split("/").pop())
    assert seqId != ""

    # Check if JSON is a valid STAC collection
    assert response.json["type"] == "Collection"
    assert response.json["id"] == str(seqId)
    assert response.json["title"] == "Séquence"


def test_post_collection_body_json(client):
    response = client.post("/api/collections", json={"title": "Séquence"})

    assert response.status_code == 200
    assert response.headers.get("Location").startswith("http://localhost:5000/api/collections/")
    seqId = UUID(response.headers.get("Location").split("/").pop())
    assert seqId != ""

    # Check if JSON is a valid STAC collection
    assert response.json["type"] == "Collection"
    assert response.json["id"] == str(seqId)
    assert response.json["title"] == "Séquence"


@conftest.SEQ_IMG_FLAT
def test_post_item_nobody(datafiles, initSequence, dburl):
    client = initSequence(datafiles, preprocess=False)
    seqId, picId = conftest.getFirstPictureIds(dburl)
    response = client.post(f"/api/collections/{seqId}/items")
    assert response.status_code == 415


@pytest.mark.parametrize(
    ("filename", "position", "httpCode"),
    (
        ("1.jpg", 2, 202),
        ("1.jpg", 1, 409),
        (None, 2, 400),
        ("1.jpg", -1, 400),
        ("1.jpg", "bla", 400),
        ("1.txt", 2, 400),
    ),
)
@conftest.SEQ_IMG_FLAT
def test_post_item_body_formdata(datafiles, initSequence, dburl, filename, position, httpCode):
    client = initSequence(datafiles, preprocess=False)

    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            seqId = cursor.execute("SELECT id FROM sequences LIMIT 1").fetchone()[0]

            # Make sequence marked as preparing
            cursor.execute("UPDATE sequences SET status='preparing' WHERE id = %s", [seqId])
            conn.commit()

            if filename is not None and filename != "1.jpg":
                os.mknod(datafiles / "seq1" / filename)

            origMetadata = None
            if filename == "1.jpg":
                origMetadata = reader.readPictureMetadata(Image.open(str(datafiles / "seq1" / filename)))
                assert len(origMetadata.exif) > 0

            response = client.post(
                f"/api/collections/{seqId}/items",
                headers={"Content-Type": "multipart/form-data"},
                data={"position": position, "picture": (datafiles / "seq1" / filename).open("rb") if filename is not None else None},
            )

            assert response.status_code == httpCode

            # Further testing if picture was accepted
            if httpCode == 202:
                assert response.headers.get("Location").startswith(f"http://localhost/api/collections/{seqId}/items/")
                picId = UUID(response.headers.get("Location").split("/").pop())
                assert str(picId) != ""

                # Check the returned JSON
                assert response.json["type"] == "Feature"
                assert response.json["id"] == str(picId)
                assert response.json["collection"] == str(seqId)
                # since the upload was not authenticated, the pictures are associated to the default account
                assert response.json["providers"] == [{"name": "Default account", "roles": ["producer"]}]

                # Check that picture has been correctly processed
                retries = 0
                while retries < 10 and retries != -1:
                    dbStatus = cursor.execute("SELECT status FROM pictures WHERE id = %s", [picId]).fetchone()[0]

                    if dbStatus == "ready":
                        retries = -1
                        laterResponse = client.get(f"/api/collections/{seqId}/items/{picId}")
                        assert laterResponse.status_code == 200

                        # Check file is available on filesystem
                        assert os.path.isfile(datafiles + "/permanent" + pictures.getHDPicturePath(picId))
                        assert not os.path.isdir(datafiles + "/permanent" + pictures.getPictureFolderPath(picId))

                        # Check sequence is marked as ready
                        seqStatus = cursor.execute("SELECT status FROM sequences WHERE id = %s", [seqId]).fetchone()
                        assert seqStatus and seqStatus[0] == "ready"

                        # Check picture has its metadata still stored
                        storedMetadata = reader.readPictureMetadata(
                            Image.open(str(datafiles + "/permanent" + pictures.getHDPicturePath(picId)))
                        )
                        assert str(storedMetadata) == str(origMetadata)

                    else:
                        retries += 1
                        time.sleep(2)

                if retries == 10:
                    raise Exception("Picture has never been processed")


def test_getCollectionImportStatus_noseq(client):
    response = client.get(f"/api/collections/00000000-0000-0000-0000-000000000000/geovisio_status")
    assert response.status_code == 404


@conftest.SEQ_IMGS_FLAT
def test_getCollectionImportStatus_ready(datafiles, initSequence, dburl):
    client = initSequence(datafiles, preprocess=False)
    seqId, picId = conftest.getFirstPictureIds(dburl)

    response = client.get(f"/api/collections/{seqId}/geovisio_status")

    assert response.status_code == 200
    assert len(response.json["items"]) == 2

    for i in response.json["items"]:
        assert len(i) == 6
        assert UUID(i["id"]) is not None
        assert i["rank"] > 0
        assert i["status"] == "ready"
        assert i["processed_at"].startswith(date.today().isoformat())
        assert i["nb_errors"] == 0
        assert i["process_error"] is None


@conftest.SEQ_IMGS_FLAT
def test_getCollectionImportStatus_hidden(datafiles, initSequence, dburl):
    client = initSequence(datafiles, preprocess=False)
    seqId, picId = conftest.getFirstPictureIds(dburl)

    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            cursor.execute("UPDATE pictures SET status = 'hidden' WHERE id = %s", [picId])
            conn.commit()

            response = client.get(f"/api/collections/{seqId}/geovisio_status")

            assert response.status_code == 200
            assert len(response.json["items"]) == 1
            assert response.json["items"][0]["id"] != picId
            assert response.json["items"][0]["status"] == "ready"


@conftest.SEQ_IMGS_FLAT
def test_upload_sequence(datafiles, client, dburl):
    # Create sequence
    resPostSeq = client.post("/api/collections")
    assert resPostSeq.status_code == 200
    seqId = resPostSeq.json["id"]
    seqLocation = resPostSeq.headers["Location"]

    # Create first image
    resPostImg1 = client.post(
        f"/api/collections/{seqId}/items",
        headers={"Content-Type": "multipart/form-data"},
        data={"position": 1, "picture": (datafiles / "b1.jpg").open("rb")},
    )

    assert resPostImg1.status_code == 202

    # Create second image
    resPostImg2 = client.post(
        f"/api/collections/{seqId}/items",
        headers={"Content-Type": "multipart/form-data"},
        data={"position": 2, "picture": (datafiles / "b2.jpg").open("rb")},
    )

    assert resPostImg2.status_code == 202

    # Check upload status
    conftest.waitForSequence(client, seqLocation)

    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            dbSeq = cursor.execute("SELECT status, geom FROM sequences where id = %s", [seqId]).fetchone()
            assert dbSeq
            # Check sequence is ready
            assert dbSeq[0] == "ready"
            # the sequence geometry should have been computed too
            assert dbSeq[1] is not None

    resGetSeq = client.get(f"/api/collections/{seqId}")
    assert resGetSeq.status_code == 200

    # the sequence should have some metadata computed
    seq = resGetSeq.json

    assert seq["extent"]["spatial"] == {"bbox": [[-1.9499731060073981, 48.13939279199841, -1.9491245819090675, 48.139852239480945]]}
    assert seq["extent"]["temporal"]["interval"] == [["2015-04-25T15:36:17+00:00", "2015-04-25T15:37:48+00:00"]]

    # 2 pictures should be in the collections
    r = client.get(f"/api/collections/{seqId}/items")
    assert r.status_code == 200

    assert len(r.json["features"]) == 2
    # both pictures should be ready
    assert r.json["features"][0]["properties"]["geovisio:status"] == "ready"
    assert r.json["features"][1]["properties"]["geovisio:status"] == "ready"

    # the pictures should have the original filename and size as metadata
    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            blurred = cursor.execute("SELECT id, metadata FROM pictures").fetchall()
            assert blurred and len(blurred) == 2
            blurred = {str(p[0]): p[1] for p in blurred}
            assert os.path.getsize(datafiles / "b1.jpg") == blurred[resPostImg1.json["id"]]["originalFileSize"]
            assert blurred[resPostImg1.json["id"]] == {
                "make": "OLYMPUS IMAGING CORP.",
                "type": "flat",
                "model": "SP-720UZ",
                "width": 4288,
                "height": 3216,
                "focal_length": 4.66,
                "field_of_view": 67,
                "blurredByAuthor": False,
                "originalFileName": "b1.jpg",
                "originalFileSize": 2731046,
            }
            assert os.path.getsize(datafiles / "b2.jpg") == blurred[resPostImg2.json["id"]]["originalFileSize"]
            assert blurred[resPostImg2.json["id"]] == {
                "make": "OLYMPUS IMAGING CORP.",
                "type": "flat",
                "model": "SP-720UZ",
                "width": 4288,
                "height": 3216,
                "focal_length": 4.66,
                "field_of_view": 67,
                "blurredByAuthor": False,
                "originalFileName": "b2.jpg",
                "originalFileSize": 2896575,
            }


@conftest.SEQ_IMGS_FLAT
def test_upload_on_unknown_sequence(datafiles, client, dburl):
    # add image on unexisting sequence
    resPostImg = client.post(
        f"/api/collections/00000000-0000-0000-0000-000000000000/items",
        headers={"Content-Type": "multipart/form-data"},
        data={"position": 1, "picture": (datafiles / "b1.jpg").open("rb")},
    )

    assert resPostImg.status_code == 404
    assert resPostImg.json["message"] == "Sequence 00000000-0000-0000-0000-000000000000 wasn't found in database"


@pytest.fixture()
def removeDefaultAccount(dburl):
    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            accountID = cursor.execute("UPDATE accounts SET is_default = false WHERE is_default = true RETURNING id").fetchone()
            assert accountID

            conn.commit()
            yield
            # put back the account at the end of the test
            cursor.execute("UPDATE accounts SET is_default = true WHERE id = %s", [accountID[0]])


def test_upload_sequence_noDefaultAccount(client, dburl, removeDefaultAccount):
    resPostSeq = client.post("/api/collections")
    assert resPostSeq.status_code == 500
    assert resPostSeq.json == {"message": "No default account defined, please contact your instance administrator", "status_code": 500}


def mockBlurringAPIPostKO(requests_mock):
    """accessing the blurring api result in a connection timeout"""
    requests_mock.post(
        conftest.MOCK_BLUR_API + "/blur/",
        exc=requests.exceptions.ConnectTimeout,
    )


@conftest.SEQ_IMG
@conftest.SEQ_IMG_BLURRED
def test_upload_picture_skip_blurring(requests_mock, datafiles, tmp_path, dburl):
    """
    Inserting a picture which is already blurred should not call the KO Blur API, thus leading to no error
    """
    mockBlurringAPIPostKO(requests_mock)
    app = create_app(
        {
            "TESTING": True,
            "API_BLUR_URL": conftest.MOCK_BLUR_API,
            "PICTURE_PROCESS_DERIVATES_STRATEGY": "ON_DEMAND",
            "DB_URL": dburl,
            "FS_URL": str(tmp_path),
            "FS_TMP_URL": None,
            "FS_PERMANENT_URL": None,
            "FS_DERIVATES_URL": None,
        }
    )

    with app.app_context():
        with app.test_client() as client:
            seq_location = conftest.createSequence(client, "a_sequence")
            conftest.uploadPicture(client, seq_location, open(datafiles / "1.jpg", "rb"), "1.jpg", 1, isBlurred=True)

            conftest.waitForSequence(client, seq_location)

            with psycopg.connect(dburl) as conn:
                with conn.cursor() as cursor:
                    blurred = cursor.execute(
                        "SELECT (metadata->>'blurredByAuthor')::boolean FROM pictures WHERE metadata->>'originalFileName' = '1.jpg'"
                    ).fetchone()
                    assert blurred and blurred[0] is True


def mockBlurringAPIPostOkay(requests_mock, datafiles):
    """Mock a working blur API call"""
    requests_mock.post(
        conftest.MOCK_BLUR_API + "/blur/",
        body=open(datafiles / "1_blurred.jpg", "rb"),
    )


@conftest.SEQ_IMG
@conftest.SEQ_IMG_BLURRED
def test_upload_picture_blurring_okay(requests_mock, datafiles, tmp_path, dburl):
    mockBlurringAPIPostOkay(requests_mock, datafiles)
    app = create_app(
        {
            "TESTING": True,
            "API_BLUR_URL": conftest.MOCK_BLUR_API,
            "PICTURE_PROCESS_DERIVATES_STRATEGY": "ON_DEMAND",
            "DB_URL": dburl,
            "FS_URL": str(tmp_path),
            "FS_TMP_URL": None,
            "FS_PERMANENT_URL": None,
            "FS_DERIVATES_URL": None,
        }
    )

    with app.app_context():
        with app.test_client() as client, psycopg.connect(dburl) as conn:
            with conn.cursor() as cursor:
                seq_location = conftest.createSequence(client, "a_sequence")

                origMetadata = reader.readPictureMetadata(Image.open(str(datafiles / "1_blurred.jpg")))
                assert len(origMetadata.exif) > 0

                response = client.post(
                    f"{seq_location}/items",
                    headers={"Content-Type": "multipart/form-data"},
                    data={"position": 1, "picture": (datafiles / "1.jpg").open("rb")},
                )

                assert response.status_code == 202 and response.json

                assert response.headers["Location"].startswith(f"{seq_location}/items/")
                picId = UUID(response.headers["Location"].split("/").pop())
                assert str(picId) != ""

                # Check the returned JSON
                assert response.json["type"] == "Feature"
                assert response.json["id"] == str(picId)
                # since the upload was not authenticated, the pictures are associated to the default account
                assert response.json["providers"] == [{"name": "Default account", "roles": ["producer"]}]

                conftest.waitForSequence(client, seq_location)

                # Check that picture has been correctly processed
                laterResponse = client.get(f"{seq_location}/items/{picId}")
                assert laterResponse.status_code == 200

                # Check if picture sent to blur API is same as one from FS
                reqSize = int(requests_mock.request_history[0].headers["Content-Length"])
                picSize = os.path.getsize(datafiles / "1.jpg")
                assert reqSize <= picSize * 1.01

                # Check file is available on filesystem
                assert os.path.isfile(datafiles + "/permanent" + pictures.getHDPicturePath(picId))
                assert not os.path.isdir(datafiles + "/permanent" + pictures.getPictureFolderPath(picId))

                # Check picture has its metadata still stored
                storedMetadata = reader.readPictureMetadata(Image.open(str(datafiles + "/permanent" + pictures.getHDPicturePath(picId))))
                assert storedMetadata == origMetadata
                assert str(storedMetadata) == str(origMetadata)


@conftest.SEQ_IMG
@conftest.SEQ_IMG_BLURRED
def test_process_picture_with_pic_process_ko_1(requests_mock, datafiles, tmp_path, dburl):
    """
    Inserting a picture with the bluring api ko should result in the image having a broken status
    """
    mockBlurringAPIPostKO(requests_mock)
    app = create_app(
        {
            "TESTING": True,
            "API_BLUR_URL": conftest.MOCK_BLUR_API,
            "PICTURE_PROCESS_DERIVATES_STRATEGY": "PREPROCESS",
            "DB_URL": dburl,
            "FS_URL": str(tmp_path),
            "FS_TMP_URL": None,
            "FS_PERMANENT_URL": None,
            "FS_DERIVATES_URL": None,
        }
    )

    with app.app_context():
        with app.test_client() as client:
            seq_location = conftest.createSequence(client, "a_sequence")
            conftest.uploadPicture(client, seq_location, open(datafiles / "1.jpg", "rb"), "1.jpg", 1)

            def wanted_state(seq):
                pic_status = {p["rank"]: p["status"] for p in seq.json["items"]}
                return pic_status == {1: "broken"}

            conftest.waitForSequenceState(client, seq_location, wanted_state)

            s = client.get(f"{seq_location}/geovisio_status")

            assert s.json
            pic = s.json["items"][0]

            assert pic["status"] == "broken"
            assert pic["nb_errors"] == 1
            assert pic["processed_at"].startswith(date.today().isoformat())
            assert pic["process_error"] == "Blur API failure: ConnectTimeout"

            assert (
                s.json["status"] == "waiting-for-process"
            )  # since no pictures have been uploaded for the sequence, it's still in the 'waiting-for-processs' status


@conftest.SEQ_IMGS
@conftest.SEQ_IMG_BLURRED
def test_process_picture_with_pic_process_ko_2(datafiles, dburl, tmp_path, monkeypatch):
    """
    Inserting 2 pictures ('1.jpg' and '2.jpg'), and '1.jpg' cannot have its derivates generated should result in
    * '1.jpg' being in a 'broken' state
    * '2.jpg' being 'ready'
    * the sequence being 'ready'
    """
    from geovisio import runner_pictures

    def new_processPictureFiles(db, dbPic, config):
        """Mock function that raises an exception for 1.jpg"""
        pic_name = db.execute("SELECT metadata->>'originalFileName' FROM pictures WHERE id = %s", [dbPic.id]).fetchone()[0]
        if pic_name == "1.jpg":
            raise Exception("oh no !")
        elif pic_name == "2.jpg":
            return  # all good
        raise Exception(f"picture {pic_name} not handled")

    with conftest.monkeypatched_function(runner_pictures, "processPictureFiles", new_processPictureFiles):
        app = create_app(
            {
                "TESTING": True,
                "API_BLUR_URL": conftest.MOCK_BLUR_API,
                "PICTURE_PROCESS_DERIVATES_STRATEGY": "PREPROCESS",
                "DB_URL": dburl,
                "FS_URL": str(tmp_path),
                "FS_TMP_URL": None,
                "FS_PERMANENT_URL": None,
                "FS_DERIVATES_URL": None,
            }
        )

        with app.app_context():
            with app.test_client() as client:
                seq_location = conftest.createSequence(client, "a_sequence")
                conftest.uploadPicture(client, seq_location, open(datafiles / "1.jpg", "rb"), "1.jpg", 1)
                conftest.uploadPicture(client, seq_location, open(datafiles / "2.jpg", "rb"), "2.jpg", 2)

                import time

                time.sleep(1)

                s = client.get(f"{seq_location}/geovisio_status")
                assert s and s.status_code == 200 and s.json
                pic_status = {p["rank"]: p["status"] for p in s.json["items"]}

                assert pic_status == {1: "broken", 2: "ready"}
                assert s.json["status"] == "ready"


@conftest.SEQ_IMGS
@conftest.SEQ_IMG_BLURRED
def test_process_picture_with_last_picture_ko(datafiles, dburl, tmp_path, monkeypatch):
    """
    Inserting 3 pictures ('1.jpg', '2.jpg' and '3.jpg" ), and '3.jpg' cannot have its derivates generated should result in
    * '1.jpg' and '2.jpg' being in a 'ready' state
    * '3.jpg' being 'broken'
    * the sequence being 'ready', and with it's metadata generated (shapes for example)
    """
    from geovisio import runner_pictures

    def new_processPictureFiles(db, dbPic, config):
        """Mock function that raises an exception for 1.jpg"""
        pic_name = db.execute("SELECT metadata->>'originalFileName' FROM pictures WHERE id = %s", [dbPic.id]).fetchone()[0]
        if pic_name in ("1.jpg", "2.jpg"):
            return  # all good
        elif pic_name == "3.jpg":
            raise Exception("oh no !")
        raise Exception(f"picture {pic_name} not handled")

    with conftest.monkeypatched_function(runner_pictures, "processPictureFiles", new_processPictureFiles):
        app = create_app(
            {
                "TESTING": True,
                "API_BLUR_URL": conftest.MOCK_BLUR_API,
                "PICTURE_PROCESS_DERIVATES_STRATEGY": "PREPROCESS",
                "DB_URL": dburl,
                "FS_URL": str(tmp_path),
                "FS_TMP_URL": None,
                "FS_PERMANENT_URL": None,
                "FS_DERIVATES_URL": None,
            }
        )

        with app.app_context():
            with app.test_client() as client:
                seq_location = conftest.createSequence(client, "a_sequence")
                conftest.uploadPicture(client, seq_location, open(datafiles / "1.jpg", "rb"), "1.jpg", 1)
                conftest.uploadPicture(client, seq_location, open(datafiles / "2.jpg", "rb"), "2.jpg", 2)
                conftest.uploadPicture(client, seq_location, open(datafiles / "3.jpg", "rb"), "3.jpg", 3)

                def wanted_state(seq):
                    pic_status = {p["rank"]: p["status"] for p in seq.json["items"]}
                    return pic_status == {1: "ready", 2: "ready", 3: "broken"}

                conftest.waitForSequenceState(client, seq_location, wanted_state)
                seq = client.get(seq_location)
                assert seq.status_code == 200 and seq.json

                # the sequence should have been processed, and it's sequence computed
                assert seq.json["extent"]["spatial"]["bbox"] == [
                    [1.9191854417991367, 49.00688961988304, 1.9191963606027425, 49.00692625960235]
                ]


@conftest.SEQ_IMGS
@conftest.SEQ_IMG_BLURRED
def test_upload_picture_storage_ko(datafiles, dburl, tmp_path, monkeypatch):
    """
    Failing to save a picture in the storage should result in a 500 and no changes in the database
    """
    app = create_app(
        {
            "TESTING": True,
            "API_BLUR_URL": "",
            "PICTURE_PROCESS_DERIVATES_STRATEGY": "PREPROCESS",
            "DB_URL": dburl,
            "FS_URL": str(tmp_path),
            "FS_TMP_URL": None,
            "FS_PERMANENT_URL": None,
            "FS_DERIVATES_URL": None,
        }
    )

    class StorageException(Exception):
        pass

    with app.app_context():
        # files will be stored in permanent storage as there is no bluring
        permanent_storage = app.config["FILESYSTEMS"].permanent

        def new_writefile(*args, **kwargs):
            """Mock function that fails to store file"""
            raise StorageException("oh no !")

        with conftest.monkeypatched_function(permanent_storage, "writefile", new_writefile):
            with app.test_client() as client:
                seq_location = conftest.createSequence(client, "a_sequence")

                # with pytest.raises(StorageException):
                picture_response = client.post(
                    f"{seq_location}/items",
                    data={"position": 1, "picture": (open(datafiles / "1.jpg", "rb"), "1.jpg")},
                    content_type="multipart/form-data",
                )
                assert picture_response.status_code == 500

                # we post again the picture, now it should work, even with the same position
                picture_response = client.post(
                    f"{seq_location}/items",
                    data={"position": 1, "picture": (open(datafiles / "1.jpg", "rb"), "1.jpg")},
                    content_type="multipart/form-data",
                )
                assert picture_response.status_code == 500  # and not a 409, conflict

                # there should be nothing in the database
                with psycopg.connect(dburl) as conn:
                    with conn.cursor() as cursor:
                        nb_pic = cursor.execute("SELECT count(*) from pictures").fetchone()
                        assert nb_pic is not None and nb_pic[0] == 0
                        nb_pic_in_seq = cursor.execute("SELECT count(*) from sequences_pictures").fetchone()
                        assert nb_pic_in_seq is not None and nb_pic_in_seq[0] == 0


@pytest.mark.datafiles(os.path.join(conftest.FIXTURE_DIR, "invalid_exif.jpg"))
def test_upload_picture_invalid_metadata(datafiles, client):
    """
    Inserting a picture with invalid metada should result in a 400 error with details about why the picture has been rejected
    """

    seq_location = conftest.createSequence(client, "a_sequence")

    picture_response = client.post(
        f"{seq_location}/items",
        data={"position": 1, "picture": (open(datafiles / "invalid_exif.jpg", "rb"), "invalid_exif.jpg")},
        content_type="multipart/form-data",
    )

    assert picture_response.status_code == 400
    assert picture_response.json == {
        "details": {"error": "Broken GPS coordinates in picture EXIF tags"},
        "message": "Impossible to parse picture metadata",
        "status_code": 400,
    }


@conftest.SEQ_IMGS
def test_patch_item_noauth(datafiles, initSequence, dburl):
    client = initSequence(datafiles, preprocess=False)
    seqId, picId = conftest.getFirstPictureIds(dburl)

    itemRoute = "/api/collections/" + str(seqId) + "/items/" + str(picId)
    response = client.get(itemRoute)
    assert response.status_code == 200

    # Lacks authentication
    response = client.patch(itemRoute, data={"visible": "false"})
    assert response.status_code == 401


@conftest.SEQ_IMGS
def test_patch_item_authtoken(datafiles, initSequenceApp, dburl, bobAccountToken):
    client, app = initSequenceApp(datafiles, preprocess=False, withBob=True)
    seqId, picId = conftest.getFirstPictureIds(dburl)

    itemRoute = "/api/collections/" + str(seqId) + "/items/" + str(picId)
    response = client.get(itemRoute)
    assert response.status_code == 200

    # Prepare auth headers
    headers = {"Authorization": "Bearer " + bobAccountToken(app)}

    # Make picture not visible
    response = client.patch(itemRoute, data={"visible": "false"}, headers=headers)
    assert response.status_code == 200
    data = response.json
    assert data["id"] == str(picId)
    assert data["properties"]["geovisio:status"] == "hidden"

    # Try to retrieve hidden picture as public
    response = client.get(itemRoute)
    assert response.status_code == 404

    # we should also be able to see the picture from the /items route as bob
    all_pics_as_bob = client.get(f"/api/collections/{str(seqId)}/items", headers=headers)
    assert all_pics_as_bob.status_code == 200
    assert len(all_pics_as_bob.json["features"]) == 5
    assert all_pics_as_bob.json["features"][0]["id"] == str(picId)
    assert all_pics_as_bob.json["features"][0]["properties"]["geovisio:status"] == "hidden"
    for f in all_pics_as_bob.json["features"][1:]:
        assert f["properties"]["geovisio:status"] == "ready"

    # but an unauthentified call should see only 1 pic in the collection
    all_pics_unauthentified = client.get(f"/api/collections/{str(seqId)}/items")
    assert all_pics_unauthentified.status_code == 200
    assert len(all_pics_unauthentified.json["features"]) == 4
    assert picId not in [f["id"] for f in all_pics_unauthentified.json["features"]]
    for f in all_pics_unauthentified.json["features"]:
        assert f["properties"]["geovisio:status"] == "ready"

    # we should also be able to see the picture from the /items route as bob
    all_pics_as_bob = client.get(f"/api/collections/{str(seqId)}/items", headers=headers)
    assert all_pics_as_bob.status_code == 200
    assert len(all_pics_as_bob.json["features"]) == 5
    assert all_pics_as_bob.json["features"][0]["id"] == str(picId)
    assert all_pics_as_bob.json["features"][0]["properties"]["geovisio:status"] == "hidden"
    for f in all_pics_as_bob.json["features"][1:]:
        assert f["properties"]["geovisio:status"] == "ready"

    # but an unauthentified call should see only 1 pic in the collection
    all_pics_unauthentified = client.get(f"/api/collections/{str(seqId)}/items")
    assert all_pics_unauthentified.status_code == 200
    assert len(all_pics_unauthentified.json["features"]) == 4
    assert picId not in [f["id"] for f in all_pics_unauthentified.json["features"]]
    for f in all_pics_unauthentified.json["features"]:
        assert f["properties"]["geovisio:status"] == "ready"

    # Re-enable picture
    response = client.patch(itemRoute, data={"visible": "true"}, headers=headers)
    assert response.status_code == 200
    data = response.json
    assert data["id"] == str(picId)
    assert data["properties"]["geovisio:status"] == "ready"


@conftest.SEQ_IMGS
def test_patch_item_missing(datafiles, initSequenceApp, bobAccountToken):
    client, app = initSequenceApp(datafiles, preprocess=False, withBob=True)
    response = client.patch(
        "/api/collections/00000000-0000-0000-0000-000000000000/items/00000000-0000-0000-0000-000000000000",
        data={"visible": "false"},
        headers={"Authorization": "Bearer " + bobAccountToken(app)},
    )
    assert response.status_code == 404


@conftest.SEQ_IMGS
def test_patch_item_invalidVisible(datafiles, initSequenceApp, dburl, bobAccountToken):
    client, app = initSequenceApp(datafiles, preprocess=False, withBob=True)
    seqId, picId = conftest.getFirstPictureIds(dburl)

    itemRoute = "/api/collections/" + str(seqId) + "/items/" + str(picId)

    response = client.patch(itemRoute, data={"visible": "pouet"}, headers={"Authorization": "Bearer " + bobAccountToken(app)})

    assert response.status_code == 400
    assert response.json == {"message": "Picture visibility parameter (visible) should be either unset, true or false", "status_code": 400}


@conftest.SEQ_IMGS
def test_patch_item_nullvisibility(datafiles, initSequenceApp, dburl, bobAccountToken):
    client, app = initSequenceApp(datafiles, preprocess=False, withBob=True)
    seqId, picId = conftest.getFirstPictureIds(dburl)
    itemRoute = "/api/collections/" + str(seqId) + "/items/" + str(picId)

    response = client.patch(itemRoute, data={}, headers={"Authorization": "Bearer " + bobAccountToken(app)})

    assert response.status_code == 200


@conftest.SEQ_IMGS
def test_patch_item_unchangedvisibility(datafiles, initSequenceApp, dburl, bobAccountToken):
    client, app = initSequenceApp(datafiles, preprocess=False, withBob=True)
    seqId, picId = conftest.getFirstPictureIds(dburl)
    itemRoute = "/api/collections/" + str(seqId) + "/items/" + str(picId)

    response = client.patch(itemRoute, data={"visible": "true"}, headers={"Authorization": "Bearer " + bobAccountToken(app)})

    assert response.status_code == 200


@conftest.SEQ_IMGS
def test_patch_item_contenttype(datafiles, initSequenceApp, dburl, bobAccountToken):
    client, app = initSequenceApp(datafiles, preprocess=False, withBob=True)
    seqId, picId = conftest.getFirstPictureIds(dburl)
    itemRoute = "/api/collections/" + str(seqId) + "/items/" + str(picId)

    response = client.patch(
        itemRoute,
        data={"visible": "false"},
        headers={"Content-Type": "multipart/form-data; whatever=blabla", "Authorization": "Bearer " + bobAccountToken(app)},
    )

    assert response.status_code == 200

    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            newStatus = cursor.execute("SELECT status FROM pictures WHERE id = %s", [picId]).fetchone()
            assert newStatus and newStatus[0] == "hidden"


@conftest.SEQ_IMGS
def test_get_collection_thumbnail(datafiles, initSequenceApp, dburl):
    client, _ = initSequenceApp(datafiles)
    seqId, picId = conftest.getFirstPictureIds(dburl)

    response = client.get(f"/api/collections/{str(seqId)}/thumb.jpg")
    assert response.status_code == 200
    assert response.content_type == "image/jpeg"
    img = Image.open(io.BytesIO(response.get_data()))
    assert img.size == (500, 300)

    first_pic_thumb = client.get(f"/api/pictures/{str(picId)}/thumb.jpg")
    assert first_pic_thumb.data == response.data


@conftest.SEQ_IMGS
def test_get_collection_thumbnail_first_pic_hidden(datafiles, initSequenceApp, dburl, bobAccountToken, defaultAccountToken):
    """ "
    If the first pic is hidden, the owner of the sequence should still be able to see it as the thumbnail,
    but all other users should see another pic as the thumbnail
    """
    client, app = initSequenceApp(datafiles, preprocess=False, withBob=True)
    sequence = conftest.getPictureIds(dburl)[0]

    # change the first pic visibility
    response = client.patch(
        f"/api/collections/{sequence.id}/items/{sequence.pictures[0].id}",
        data={"visible": "false"},
        headers={"Authorization": f"Bearer {bobAccountToken(app)}"},
    )
    assert response.status_code == 200

    response = client.get(f"/api/collections/{sequence.id}/thumb.jpg")
    assert response.status_code == 200
    assert response.content_type == "image/jpeg"
    img = Image.open(io.BytesIO(response.get_data()))
    assert img.size == (500, 300)

    # non logged users should not see the same picture
    first_pic_thumb = client.get(f"/api/pictures/{sequence.pictures[0].id}/thumb.jpg")
    assert first_pic_thumb.status_code == 403  # this picture should not be visible to the other users

    second_pic_thumb = client.get(f"/api/pictures/{str(sequence.pictures[1].id)}/thumb.jpg")
    assert second_pic_thumb.status_code == 200  # the second picture is not hidden and should be visible and be the thumbnail
    assert response.data == second_pic_thumb.data

    # same thing for a logged user that is not the owner
    first_pic_thumb = client.get(
        f"/api/pictures/{sequence.pictures[0].id}/thumb.jpg", headers={"Authorization": f"Bearer {defaultAccountToken(app)}"}
    )
    assert first_pic_thumb.status_code == 403

    second_pic_thumb = client.get(
        f"/api/pictures/{str(sequence.pictures[1].id)}/thumb.jpg", headers={"Authorization": f"Bearer {defaultAccountToken(app)}"}
    )
    assert second_pic_thumb.status_code == 200
    assert response.data == second_pic_thumb.data

    owner_thumbnail = client.get(f"/api/collections/{sequence.id}/thumb.jpg", headers={"Authorization": f"Bearer {bobAccountToken(app)}"})
    assert owner_thumbnail.status_code == 200
    assert owner_thumbnail.content_type == "image/jpeg"
    owner_first_pic_thumbnail = client.get(
        f"/api/pictures/{sequence.pictures[0].id}/thumb.jpg", headers={"Authorization": f"Bearer {bobAccountToken(app)}"}
    )
    assert owner_first_pic_thumbnail.status_code == 200
    assert owner_thumbnail.data == owner_first_pic_thumbnail.data  # the owner should see the first pic


@conftest.SEQ_IMGS
def test_get_collection_thumbnail_all_pics_hidden(datafiles, initSequenceApp, dburl, bobAccountToken, defaultAccountToken):
    """ "
    If the all pics are hidden, the owner of the sequence should still be able to see a the thumbnail,
    but all other users should not have any thumbnails
    """
    client, app = initSequenceApp(datafiles, preprocess=False, withBob=True)
    sequence = conftest.getPictureIds(dburl)[0]

    # change the first pic visibility
    for p in sequence.pictures:
        response = client.patch(
            f"/api/collections/{sequence.id}/items/{str(p.id)}",
            data={"visible": "false"},
            headers={"Authorization": f"Bearer {bobAccountToken(app)}"},
        )
        assert response.status_code == 200

    # non logged users should not see a thumbnail
    response = client.get(f"/api/collections/{sequence.id}/thumb.jpg")
    assert response.status_code == 404

    for p in sequence.pictures:
        # the pictures should not be visible to the any other users, logged or not
        # specific hidden pictures will result on 403, not 404
        first_pic_thumb = client.get(f"/api/pictures/{str(p.id)}/thumb.jpg")
        assert first_pic_thumb.status_code == 403
        first_pic_thumb = client.get(
            f"/api/pictures/{sequence.pictures[0].id}/thumb.jpg", headers={"Authorization": f"Bearer {defaultAccountToken(app)}"}
        )
        assert first_pic_thumb.status_code == 403

    # but the owner should see it
    owner_thumbnail = client.get(f"/api/collections/{sequence.id}/thumb.jpg", headers={"Authorization": f"Bearer {bobAccountToken(app)}"})
    assert owner_thumbnail.status_code == 200
    assert owner_thumbnail.content_type == "image/jpeg"
    owner_first_pic_thumbnail = client.get(
        f"/api/pictures/{sequence.pictures[0].id}/thumb.jpg", headers={"Authorization": f"Bearer {bobAccountToken(app)}"}
    )
    assert owner_first_pic_thumbnail.status_code == 200
    assert owner_thumbnail.data == owner_first_pic_thumbnail.data  # the owner should see the first pic


@conftest.SEQ_IMGS
def test_get_collection_thumbnail_sequence_hidden(datafiles, initSequenceApp, dburl, bobAccountToken, defaultAccountToken):
    """ "
    If the sequence is hidden, the owner of the sequence should still be able to see a the thumbnail,
    but all other users should not have any thumbnails
    """
    client, app = initSequenceApp(datafiles, preprocess=False, withBob=True)
    sequence = conftest.getPictureIds(dburl)[0]

    # change the sequence visibility
    response = client.patch(
        f"/api/collections/{sequence.id}", data={"visible": "false"}, headers={"Authorization": f"Bearer {bobAccountToken(app)}"}
    )
    assert response.status_code == 200

    # non logged users should not see a thumbnail
    response = client.get(f"/api/collections/{sequence.id}/thumb.jpg")
    assert response.status_code == 404

    for p in sequence.pictures:
        # the pictures should not be visible to the any other users, logged or not
        # specific hidden pictures will result on 403, not 404
        first_pic_thumb = client.get(f"/api/pictures/{str(p.id)}/thumb.jpg")
        assert first_pic_thumb.status_code == 403
        first_pic_thumb = client.get(
            f"/api/pictures/{sequence.pictures[0].id}/thumb.jpg", headers={"Authorization": f"Bearer {defaultAccountToken(app)}"}
        )
        assert first_pic_thumb.status_code == 403

    # but the owner should see it
    owner_thumbnail = client.get(f"/api/collections/{sequence.id}/thumb.jpg", headers={"Authorization": f"Bearer {bobAccountToken(app)}"})
    assert owner_thumbnail.status_code == 200
    assert owner_thumbnail.content_type == "image/jpeg"
    owner_first_pic_thumbnail = client.get(
        f"/api/pictures/{sequence.pictures[0].id}/thumb.jpg", headers={"Authorization": f"Bearer {bobAccountToken(app)}"}
    )
    assert owner_first_pic_thumbnail.status_code == 200
    assert owner_thumbnail.data == owner_first_pic_thumbnail.data  # the owner should see the first pic


@conftest.SEQ_IMGS
def test_delete_picture_on_demand(datafiles, initSequenceApp, dburl, bobAccountToken):
    client, app = initSequenceApp(datafiles, preprocess=False, withBob=True)
    sequence = conftest.getPictureIds(dburl)[0]
    first_pic_id = sequence.pictures[0].id

    # before the delte, we can query the first picture
    response = client.get(f"/api/collections/{sequence.id}/items/{first_pic_id}")
    assert response.status_code == 200

    response = client.get(f"/api/collections/{sequence.id}/items")
    assert len(response.json["features"]) == 5
    assert first_pic_id in [f["id"] for f in response.json["features"]]

    assert os.path.exists(
        datafiles / "derivates" / first_pic_id[0:2] / first_pic_id[2:4] / first_pic_id[4:6] / first_pic_id[6:8] / first_pic_id[9:]
    )
    assert os.path.exists(datafiles / "permanent" / first_pic_id[0:2] / first_pic_id[2:4] / first_pic_id[4:6] / first_pic_id[6:8])

    response = client.delete(
        f"/api/collections/{sequence.id}/items/{first_pic_id}", headers={"Authorization": f"Bearer {bobAccountToken(app)}"}
    )
    assert response.status_code == 204

    # The first picture should not be returned in any response
    response = client.get(f"/api/collections/{sequence.id}/items/{first_pic_id}")
    assert response.status_code == 404

    response = client.get(f"/api/collections/{sequence.id}/items")
    assert len(response.json["features"]) == 4
    assert first_pic_id not in [f["id"] for f in response.json["features"]]

    # check that all files have correctly been deleted
    assert not os.path.exists(
        datafiles / "derivates" / first_pic_id[0:2] / first_pic_id[2:4] / first_pic_id[4:6] / first_pic_id[6:8] / first_pic_id[9:]
    )
    assert not os.path.exists(datafiles / "permanent" / first_pic_id[0:2] / first_pic_id[2:4] / first_pic_id[4:6] / first_pic_id[6:8])
    # there should be no empty directory
    for dirpath, dirname, files in itertools.chain(os.walk(datafiles / "permanent"), os.walk(datafiles / "derivates")):
        assert files or dirname, f"directory {dirpath} is empty"

    # requesting the picture now should result in a 404
    response = client.get(f"/api/collections/{sequence.id}/items/{first_pic_id}")
    assert response.status_code == 404

    # and we should not see it anymore in the collection's item
    all_pics = client.get(f"/api/collections/{sequence.id}/items")
    assert all_pics.status_code == 200
    assert len(all_pics.json["features"]) == 4
    assert first_pic_id not in [f["id"] for f in all_pics.json["features"]]

    # same for deleting it again
    response = client.delete(
        f"/api/collections/{sequence.id}/items/{first_pic_id}", headers={"Authorization": f"Bearer {bobAccountToken(app)}"}
    )
    assert response.status_code == 404


@conftest.SEQ_IMGS
def test_delete_picture_preprocess(datafiles, initSequenceApp, dburl, bobAccountToken):
    """Deleting a picture with the API configured as preprocess should work fine, and all derivates should be deleted"""
    client, app = initSequenceApp(datafiles, preprocess=True, withBob=True)
    sequence = conftest.getPictureIds(dburl)[0]
    first_pic_id = sequence.pictures[0].id

    # before the delte, we can query the first picture
    response = client.get(f"/api/collections/{sequence.id}/items/{first_pic_id}")
    assert response.status_code == 200

    response = client.get(f"/api/collections/{sequence.id}/items")
    assert len(response.json["features"]) == 5
    assert first_pic_id in [f["id"] for f in response.json["features"]]

    assert os.path.exists(
        datafiles / "derivates" / first_pic_id[0:2] / first_pic_id[2:4] / first_pic_id[4:6] / first_pic_id[6:8] / first_pic_id[9:]
    )
    assert os.path.exists(datafiles / "permanent" / first_pic_id[0:2] / first_pic_id[2:4] / first_pic_id[4:6] / first_pic_id[6:8])

    response = client.delete(
        f"/api/collections/{sequence.id}/items/{first_pic_id}", headers={"Authorization": f"Bearer {bobAccountToken(app)}"}
    )
    assert response.status_code == 204

    # The first picture should not be returned in any response
    response = client.get(f"/api/collections/{sequence.id}/items/{first_pic_id}")
    assert response.status_code == 404

    response = client.get(f"/api/collections/{sequence.id}/items")
    assert len(response.json["features"]) == 4
    assert first_pic_id not in [f["id"] for f in response.json["features"]]

    # check that all files have correctly been deleted
    assert not os.path.exists(
        datafiles / "derivates" / first_pic_id[0:2] / first_pic_id[2:4] / first_pic_id[4:6] / first_pic_id[6:8] / first_pic_id[9:]
    )
    assert not os.path.exists(datafiles / "permanent" / first_pic_id[0:2] / first_pic_id[2:4] / first_pic_id[4:6] / first_pic_id[6:8])
    # there should be no empty directory
    for dirpath, dirname, files in itertools.chain(os.walk(datafiles / "permanent"), os.walk(datafiles / "derivates")):
        assert files or dirname, f"directory {dirpath} is empty"

    # requesting the picture now should result in a 404
    response = client.get(f"/api/collections/{sequence.id}/items/{first_pic_id}")
    assert response.status_code == 404


@conftest.SEQ_IMGS
def test_delete_picture_no_auth(datafiles, initSequenceApp, dburl):
    """Deleting a picture wihout being identified is forbidden"""
    client, app = initSequenceApp(datafiles, preprocess=True, withBob=True)
    sequence = conftest.getPictureIds(dburl)[0]
    first_pic_id = sequence.pictures[0].id
    response = client.delete(f"/api/collections/{sequence.id}/items/{first_pic_id}")
    assert response.status_code == 401


@conftest.SEQ_IMGS
def test_delete_picture_as_another_user(datafiles, initSequenceApp, dburl, defaultAccountToken):
    """
    Deleting a not owned picture should be forbidden
    Here the pictures are owned by Bob and the default account tries to delete them
    """
    client, app = initSequenceApp(datafiles, preprocess=True, withBob=True)
    sequence = conftest.getPictureIds(dburl)[0]
    first_pic_id = sequence.pictures[0].id
    response = client.delete(
        f"/api/collections/{sequence.id}/items/{first_pic_id}", headers={"Authorization": f"Bearer {defaultAccountToken(app)}"}
    )
    assert response.status_code == 403


@conftest.SEQ_IMGS
def test_delete_picture_still_waiting_for_process(datafiles, tmp_path, initSequenceApp, dburl, bobAccountToken):
    """Deleting a picture that is still waiting to be processed should be fine (and the picture should be removed from the process queue)"""

    app = create_app(
        {
            "TESTING": True,
            "PICTURE_PROCESS_DERIVATES_STRATEGY": "PREPROCESS",
            "DB_URL": dburl,
            "FS_URL": str(tmp_path),
            "SECRET_KEY": "a very secret key",
            "FS_TMP_URL": None,
            "FS_PERMANENT_URL": None,
            "FS_DERIVATES_URL": None,
            "PICTURE_PROCESS_THREADS_LIMIT": 0,  # we run the API without any picture worker, so no pictures will be processed
        }
    )

    with app.app_context():
        with app.test_client() as client, psycopg.connect(dburl) as conn:
            token = bobAccountToken(app)
            seq_location = conftest.createSequence(client, os.path.basename(datafiles), jwtToken=token)
            seq_id = seq_location.split("/")[-1]
            pic_id = conftest.uploadPicture(client, seq_location, open(datafiles / "1.jpg", "rb"), "1.jpg", 1, jwtToken=token)

            r = conn.execute("SELECT count(*) FROM pictures_to_process").fetchone()
            assert r and r[0] == 1

            r = conn.execute("SELECT id, status FROM pictures").fetchall()
            assert r and list(r) == [(UUID(pic_id), "waiting-for-process")]

            assert os.path.exists(datafiles / "permanent" / pic_id[0:2] / pic_id[2:4] / pic_id[4:6] / pic_id[6:8])
            assert not os.path.exists(datafiles / "derivates" / pic_id[0:2] / pic_id[2:4] / pic_id[4:6] / pic_id[6:8] / pic_id[9:])

            response = client.delete(
                f"/api/collections/{seq_id}/items/{pic_id}", headers={"Authorization": f"Bearer {bobAccountToken(app)}"}
            )
            assert response.status_code == 204

            r = conn.execute("SELECT count(*) FROM pictures_to_process").fetchone()
            assert r and r[0] == 0

            r = conn.execute("SELECT count(*) FROM pictures").fetchone()
            assert r and r[0] == 0

            # pic should have been deleted too
            assert not os.path.exists(datafiles / "permanent" / pic_id[0:2] / pic_id[2:4] / pic_id[4:6] / pic_id[6:8])


def _wait_for_pics_deletion(pics_id, dburl):
    with psycopg.connect(dburl) as conn:
        waiting_time = 0.1
        total_time = 0
        nb_pics = 0
        while total_time < 10:
            nb_pics = conn.execute("SELECT count(*) FROM pictures WHERE id = ANY(%(pics)s)", {"pics": pics_id}).fetchone()

            # we wait for the collection and all its pictures to be ready
            if nb_pics and not nb_pics[0]:
                return
            time.sleep(waiting_time)
            total_time += waiting_time
        assert False, f"All pictures not deleted ({nb_pics} remaining)"


@conftest.SEQ_IMGS
def test_delete_sequence(datafiles, initSequenceApp, dburl, bobAccountToken):
    client, app = initSequenceApp(datafiles, preprocess=False, withBob=True)
    sequence = conftest.getPictureIds(dburl)[0]
    first_pic_id = sequence.pictures[0].id

    # before the delete, we can query the seq
    response = client.get(f"/api/collections/{sequence.id}")
    assert response.status_code == 200

    response = client.get(f"/api/collections/{sequence.id}/items")
    assert len(response.json["features"]) == 5
    assert first_pic_id in [f["id"] for f in response.json["features"]]

    assert os.path.exists(
        datafiles / "derivates" / first_pic_id[0:2] / first_pic_id[2:4] / first_pic_id[4:6] / first_pic_id[6:8] / first_pic_id[9:]
    )
    assert os.path.exists(datafiles / "permanent" / first_pic_id[0:2] / first_pic_id[2:4] / first_pic_id[4:6] / first_pic_id[6:8])

    response = client.delete(f"/api/collections/{sequence.id}", headers={"Authorization": f"Bearer {bobAccountToken(app)}"})
    assert response.status_code == 204

    # The sequence or its pictures should not be returned in any response
    response = client.get(f"/api/collections/{sequence.id}/items/{first_pic_id}")
    assert response.status_code == 404

    response = client.get(f"/api/collections/{sequence.id}")
    assert response.status_code == 404

    with psycopg.connect(dburl) as conn:
        seq = conn.execute("SELECT * FROM sequences WHERE id = %s", [sequence.id]).fetchone()
        assert not seq

        pic_status = conn.execute(
            "SELECT distinct(status) FROM pictures WHERE id = ANY(%(pics)s)", {"pics": [p.id for p in sequence.pictures]}
        ).fetchall()

        # pics are either already deleted or waiting deleting
        assert pic_status == [] or pic_status == [("waiting-for-delete",)]

    # async job should delete at one point all the pictures
    _wait_for_pics_deletion(pics_id=[p.id for p in sequence.pictures], dburl=dburl)

    # check that all files have correctly been deleted since it was the only sequence
    assert os.listdir(datafiles / "derivates") == []
    assert os.listdir(datafiles / "permanent") == []


@conftest.SEQ_IMGS
@conftest.SEQ_IMGS_FLAT
def test_delete_1_sequence_over_2(datafiles, initSequenceApp, dburl, bobAccountToken):
    """2 sequences available, and delete of them, we should not mess with the other sequence"""
    client, app = initSequenceApp(datafiles, preprocess=False, withBob=True)
    sequence = conftest.getPictureIds(dburl)
    assert len(sequence) == 2

    # before the delete, we can query both seq
    for seq in sequence:
        response = client.get(f"/api/collections/{seq.id}")
        assert response.status_code == 200

        response = client.get(f"/api/collections/{seq.id}/items")
        assert response.status_code == 200

    for s in sequence:
        for p in s.pictures:
            assert os.path.exists(p.get_derivate_dir(datafiles))
            assert os.path.exists(p.get_permanent_file(datafiles))

    # we delete the first sequence
    response = client.delete(f"/api/collections/{sequence[0].id}", headers={"Authorization": f"Bearer {bobAccountToken(app)}"})
    assert response.status_code == 204

    # The sequence or its pictures should not be returned in any response
    response = client.get(f"/api/collections/{sequence[0].id}/items/{sequence[0].pictures[0].id}")
    assert response.status_code == 404

    response = client.get(f"/api/collections/{sequence[0].id}")
    assert response.status_code == 404

    # everything is still fine for the other sequence
    assert client.get(f"/api/collections/{sequence[1].id}/items/{sequence[1].pictures[0].id}").status_code == 200
    assert client.get(f"/api/collections/{sequence[1].id}").status_code == 200

    with psycopg.connect(dburl) as conn:
        seq = conn.execute("SELECT * FROM sequences WHERE id = %s", [sequence[0].id]).fetchone()
        assert not seq

        pic_status = conn.execute(
            "SELECT distinct(status) FROM pictures WHERE id = ANY(%(pics)s)", {"pics": [p.id for p in sequence[0].pictures]}
        ).fetchall()

        # pics are either already deleted or waiting deleting
        assert pic_status == [] or pic_status == [("waiting-for-delete",)]

    # async job should delete at one point all the pictures
    _wait_for_pics_deletion(pics_id=[p.id for p in sequence[0].pictures], dburl=dburl)

    for p in sequence[0].pictures:
        assert not os.path.exists(p.get_derivate_dir(datafiles))
        assert not os.path.exists(p.get_permanent_file(datafiles))
    for p in sequence[1].pictures:
        assert os.path.exists(p.get_derivate_dir(datafiles))
        assert os.path.exists(p.get_permanent_file(datafiles))


@conftest.SEQ_IMGS
def test_delete_sequence_no_auth(datafiles, initSequenceApp, dburl):
    """A sequence cannot be deleted with authentication"""
    client, app = initSequenceApp(datafiles, preprocess=False, withBob=True)
    sequence = conftest.getPictureIds(dburl)
    response = client.delete(f"/api/collections/{sequence[0].id}")
    assert response.status_code == 401
    assert response.json == {"message": "Authentication is mandatory"}


@conftest.SEQ_IMGS
def test_delete_sequence_not_owned(datafiles, initSequenceApp, dburl, defaultAccountToken):
    """A sequence cannot be deleted with authentication"""
    client, app = initSequenceApp(datafiles, preprocess=False, withBob=True)
    sequence = conftest.getPictureIds(dburl)
    response = client.delete(f"/api/collections/{sequence[0].id}", headers={"Authorization": f"Bearer {defaultAccountToken(app)}"})
    assert response.status_code == 403
    assert response.json == {"message": "You're not authorized to edit this sequence", "status_code": 403}


@conftest.SEQ_IMGS
def test_delete_sequence_with_pic_still_waiting_for_process(datafiles, tmp_path, initSequenceApp, dburl, bobAccountToken):
    """Deleting a sequence with pictures that are still waiting to be processed should be fine (and the picture should be removed from the process queue)"""
    app = create_app(
        {
            "TESTING": True,
            "PICTURE_PROCESS_DERIVATES_STRATEGY": "PREPROCESS",
            "DB_URL": dburl,
            "FS_URL": str(tmp_path),
            "SECRET_KEY": "a very secret key",
            "FS_TMP_URL": None,
            "FS_PERMANENT_URL": None,
            "FS_DERIVATES_URL": None,
            "PICTURE_PROCESS_THREADS_LIMIT": 0,  # we run the API without any picture worker, so no pictures will be processed
        }
    )

    with app.app_context(), app.test_client() as client, psycopg.connect(dburl) as conn:
        token = bobAccountToken(app)
        seq_location = conftest.createSequence(client, os.path.basename(datafiles), jwtToken=token)
        pic_id = conftest.uploadPicture(client, seq_location, open(datafiles / "1.jpg", "rb"), "1.jpg", 1, jwtToken=token)
        sequence = conftest.getPictureIds(dburl)[0]

        r = conn.execute("SELECT count(*) FROM pictures_to_process").fetchone()
        assert r and r[0] == 1

        r = conn.execute("SELECT id, status FROM pictures").fetchall()
        assert r and list(r) == [(UUID(pic_id), "waiting-for-process")]

        assert not os.path.exists(sequence.pictures[0].get_derivate_dir(datafiles))
        assert os.path.exists(sequence.pictures[0].get_permanent_file(datafiles))

        response = client.delete(f"/api/collections/{sequence.id}", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 204

        # since there are no background worker, the deletion is not happening, but the picture should be marked for deletion
        r = conn.execute("SELECT picture_id, task FROM pictures_to_process").fetchall()
        assert r and r == [(UUID(pic_id), "delete")]

        r = conn.execute("SELECT count(*) FROM pictures").fetchone()
        assert r and r[0] == 1

        # pic should not have been deleted, since we background worker is there
        assert os.path.exists(sequence.pictures[0].get_permanent_file(datafiles))

        # we start the runner picture as a separate process
        import multiprocessing

        def process():
            with app.app_context():
                w = runner_pictures.PictureProcessor(config=app.config, stop=False)
                w.process_next_pictures()

        p = multiprocessing.Process(target=process)
        p.start()
        p.join(timeout=3)  # wait 3 seconds before killing the process
        if p.is_alive():
            p.terminate()
        r = conn.execute("SELECT count(*) FROM pictures_to_process").fetchone()
        assert r and r[0] == 0
        r = conn.execute("SELECT count(*) FROM pictures").fetchone()
        assert r and r[0] == 0

        assert not os.path.exists(sequence.pictures[0].get_permanent_file(datafiles))
        assert not os.path.exists(sequence.pictures[0].get_derivate_dir(datafiles))
