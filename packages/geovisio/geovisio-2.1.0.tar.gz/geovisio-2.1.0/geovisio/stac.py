import psycopg
import re
import json
from uuid import UUID
from psycopg.sql import SQL
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb
from dateutil import tz
import datetime
import dateutil.parser
from dateutil.parser import parse as dateparser
from flask import Blueprint, current_app, request, url_for
from urllib.parse import unquote
from werkzeug.datastructures import MultiDict
from typing import Optional
from PIL import Image
from fs.path import dirname
import typing
from . import errors, pictures, runner_pictures, auth
import os
import logging


STAC_VERSION = "1.0.0"
STAC_PREFIX = "/api"
CONFORMANCE_LIST = [
    "http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/core",
    "http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/geojson",
    f"https://api.stacspec.org/v{STAC_VERSION}/core",
    f"https://api.stacspec.org/v{STAC_VERSION}/browseable",
    f"https://api.stacspec.org/v{STAC_VERSION}/collections",
    f"https://api.stacspec.org/v{STAC_VERSION}/ogcapi-features",
    f"https://api.stacspec.org/v{STAC_VERSION}/item-search",
]

SEQUENCES_DEFAULT_FETCH = 100
SEQUENCES_MAX_FETCH = 1000

bp = Blueprint("stac", __name__, url_prefix=STAC_PREFIX)


def parse_datetime(value, error, fallback_as_UTC=False):
    """
    Parse a datetime and raises an error if the parse fails
    Note: if fallback_as_UTC is True and the date as no parsed timezone, consider it as UTC
    This should be done for server's date (like a date automaticaly set by the server) but not user's date (like the datetime of the picture)
    >>> parse_datetime("2020-05-31T10:00:00Z", error="")
    datetime.datetime(2020, 5, 31, 10, 0, tzinfo=tzutc())
    >>> parse_datetime("2023-06-17T21:22:18.406856+02:00", error="")
    datetime.datetime(2023, 6, 17, 21, 22, 18, 406856, tzinfo=datetime.timezone(datetime.timedelta(seconds=7200)))
    >>> parse_datetime("2020-05-31", error="")
    datetime.datetime(2020, 5, 31, 0, 0)
    >>> parse_datetime("20231", error="oh no") # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    geovisio.errors.InvalidAPIUsage: oh no
    >>> parse_datetime("2020-05-31T10:00:00", error="")
    datetime.datetime(2020, 5, 31, 10, 0)
    >>> parse_datetime("2020-05-31T10:00:00", error="", fallback_as_UTC=True) ==  parse_datetime("2020-05-31T10:00:00", error="").astimezone(tz.UTC)
    True

    """
    # Hack to parse a date
    # dateutils know how to parse lots of date, but fail to correctly parse date formated by `datetime.isoformat()`
    # (like all the dates returned by the API).
    # datetime.isoformat is like: `2023-06-17T21:22:18.406856+02:00`
    # dateutils silently fails the parse, and create an incorect date
    # so we first try to parse it like an isoformated date, and if this fails we try the flexible dateutils
    d = None
    try:
        d = datetime.datetime.fromisoformat(value)
    except ValueError as e:
        pass
    if not d:
        try:
            d = dateparser(value)
            return d
        except dateutil.parser.ParserError as e:
            raise errors.InvalidAPIUsage(message=error, payload={"details": {"error": str(e)}})
    if fallback_as_UTC and d.tzinfo is None:
        d = d.astimezone(tz.UTC)
    return d


@bp.route("/")
def getLanding():
    """Retrieves API resources list
    ---
    tags:
        - Metadata
    responses:
        200:
            description: the Catalog listing resources available in this API. A non-standard "extent" property is also available (note that this may evolve in the future)
            content:
                application/json:
                    schema:
                        $ref: '#/components/schemas/GeoVisioLanding'
    """

    with psycopg.connect(current_app.config["DB_URL"]) as conn:
        with conn.cursor() as cursor:
            spatial_xmin, spatial_ymin, spatial_xmax, spatial_ymax, temporal_min, temporal_max = cursor.execute(
                """
				SELECT
					ST_XMin(ST_EstimatedExtent('pictures', 'geom')),
					ST_YMin(ST_EstimatedExtent('pictures', 'geom')),
					ST_XMax(ST_EstimatedExtent('pictures', 'geom')),
					ST_YMax(ST_EstimatedExtent('pictures', 'geom')),
					MIN(ts), MAX(ts)
				FROM pictures
			"""
            ).fetchone()

            extent = (
                {
                    "spatial": {"bbox": [[spatial_xmin, spatial_ymin, spatial_xmax, spatial_ymax]]} if spatial_xmin is not None else None,
                    "temporal": {"interval": [[dbTsToStac(temporal_min), dbTsToStac(temporal_max)]]} if temporal_min is not None else None,
                }
                if spatial_xmin is not None or temporal_min is not None
                else None
            )

            sequences = [
                {"rel": "child", "title": f'User "{s[1]}" sequences', "href": url_for("stac.getUserCatalog", userId=s[0], _external=True)}
                for s in cursor.execute(
                    """
					SELECT DISTINCT s.account_id, a.name
					FROM sequences s
					JOIN accounts a ON s.account_id = a.id
				"""
                ).fetchall()
            ]

            catalog = dbSequencesToStacCatalog(
                "geovisio",
                "GeoVisio STAC API",
                "This catalog list all geolocated pictures available in this GeoVisio instance",
                sequences,
                request,
                extent,
            )

            mapUrl = (
                url_for("map.getTile", x="111", y="222", z="333", format="mvt", _external=True)
                .replace("111", "{x}")
                .replace("222", "{y}")
                .replace("333", "{z}")
            )

            if "stac_extensions" not in catalog:
                catalog["stac_extensions"] = []

            catalog["stac_extensions"] += ["https://stac-extensions.github.io/web-map-links/v1.0.0/schema.json"]

            catalog["links"] += cleanNoneInList(
                [
                    {"rel": "service-desc", "type": "application/json", "href": url_for("flasgger.swagger", _external=True)},
                    {"rel": "service-doc", "type": "text/html", "href": url_for("flasgger.apidocs", _external=True)},
                    {"rel": "conformance", "type": "application/json", "href": url_for("stac.getConformance", _external=True)},
                    {"rel": "data", "type": "application/json", "href": url_for("stac.getAllCollections", _external=True)},
                    {"rel": "search", "type": "application/geo+json", "href": url_for("stac.searchItems", _external=True)},
                    {
                        "rel": "xyz",
                        "type": "application/vnd.mapbox-vector-tile",
                        "href": mapUrl,
                        "title": "Pictures and sequences vector tiles",
                    },
                    {
                        "rel": "collection-preview",
                        "type": "image/jpeg",
                        "href": url_for("stac.getCollectionThumbnail", collectionId="{id}", _external=True),
                        "title": "Thumbnail URL for a given sequence",
                    },
                    {
                        "rel": "item-preview",
                        "type": "image/jpeg",
                        "href": url_for("pictures.getPictureThumb", pictureId="{id}", format="jpg", _external=True),
                        "title": "Thumbnail URL for a given picture",
                    },
                    _get_license_link(),
                ]
            )

            return catalog, 200, {"Content-Type": "application/json"}

        raise errors.InvalidAPIUsage("Failed to connect to database", status_code=500)

    raise errors.InvalidAPIUsage("Failed to connect to database", status_code=500)


@bp.route("/conformance")
def getConformance():
    """List definitions this API conforms to
    ---
    tags:
        - Metadata
    responses:
        200:
            description: the list of definitions this API conforms to
            content:
                application/json:
                    schema:
                        $ref: '#/components/schemas/STACConformance'
    """

    return {"conformsTo": CONFORMANCE_LIST}, 200, {"Content-Type": "application/json"}


def dbSequenceToStacCollection(dbSeq):
    """Transforms a sequence extracted from database into a STAC Collection

    Parameters
    ----------
    dbSeq : dict
        A row from sequences table in database (with id, name, minx, miny, maxx, maxy, mints, maxts fields)
    request
    current_app

    Returns
    -------
    object
        The equivalent in STAC Collection format
    """

    mints, maxts, insertedAt, updatedAt = dbSeq.get("mints"), dbSeq.get("maxts"), dbSeq.get("inserted_at"), dbSeq.get("updated_at")
    return removeNoneInDict(
        {
            "type": "Collection",
            "stac_version": STAC_VERSION,
            "stac_extensions": ["https://stac-extensions.github.io/stats/v0.2.0/schema.json"],  # For stats: fields
            "id": str(dbSeq["id"]),
            "title": str(dbSeq["name"]),
            "description": "A sequence of geolocated pictures",
            "keywords": ["pictures", str(dbSeq["name"])],
            "license": current_app.config["API_PICTURES_LICENSE_SPDX_ID"],
            "created": dbTsToStac(insertedAt),
            "updated": dbTsToStac(updatedAt),
            "geovisio:status": dbSeq.get("status"),
            "providers": [
                {"name": dbSeq["account_name"], "roles": ["producer"]},
            ],
            "extent": {
                "spatial": {"bbox": [[dbSeq["minx"] or -180.0, dbSeq["miny"] or -90.0, dbSeq["maxx"] or 180.0, dbSeq["maxy"] or 90.0]]},
                "temporal": {
                    "interval": [
                        [
                            dbTsToStac(mints),
                            dbTsToStac(maxts),
                        ]
                    ]
                },
            },
            "summaries": cleanNoneInDict({"pers:interior_orientation": dbSeq.get("metas")}),
            "stats:items": removeNoneInDict({"count": dbSeq.get("nbpic")}),
            "links": cleanNoneInList(
                [
                    {
                        "rel": "items",
                        "type": "application/geo+json",
                        "title": "Pictures in this sequence",
                        "href": url_for("stac.getCollectionItems", _external=True, collectionId=dbSeq["id"]),
                    },
                    {
                        "rel": "parent",
                        "type": "application/json",
                        "title": "Instance catalog",
                        "href": url_for("stac.getLanding", _external=True),
                    },
                    _get_root_link(),
                    {
                        "rel": "self",
                        "type": "application/json",
                        "title": "Metadata of this sequence",
                        "href": url_for("stac.getCollection", _external=True, collectionId=dbSeq["id"]),
                    },
                    _get_license_link(),
                ]
            ),
        }
    )


def _get_root_link():
    return {
        "rel": "root",
        "type": "application/json",
        "title": "Instance catalog",
        "href": url_for("stac.getLanding", _external=True),
    }


def _get_license_link():
    license_url = current_app.config.get("API_PICTURES_LICENSE_URL")
    if not license_url:
        return None
    return {
        "rel": "license",
        "title": f"License for this object ({current_app.config['API_PICTURES_LICENSE_SPDX_ID']})",
        "href": license_url,
    }


def dbSequencesToStacCatalog(id, title, description, sequences, request, extent=None, **selfUrlValues):
    """Transforms a set of sequences into a STAC Catalog

    Parameters
    ----------
    id : str
        The catalog ID
    title : str
        The catalog name
    description : str
        The catalog description
    sequences : list
        List of sequences as STAC child links
    request
    current_app
    extent : dict
        Spatial and temporal extent of the catalog, in STAC format
    selfRoute : str
        API route to access this catalog (defaults to empty, for root catalog)

    Returns
    -------
    object
            The equivalent in STAC Catalog format
    """

    return removeNoneInDict(
        {
            "stac_version": STAC_VERSION,
            "id": id,
            "title": title,
            "description": description,
            "type": "Catalog",
            "conformsTo": CONFORMANCE_LIST,
            "extent": extent,
            "links": [
                {"rel": "self", "type": "application/json", "href": url_for(request.endpoint, _external=True, **selfUrlValues)},
                _get_root_link(),
            ]
            + sequences,
        }
    )


@bp.route("/collections")
def getAllCollections():
    """List available collections
    ---
    tags:
        - Sequences
    parameters:
        - name: limit
          in: query
          description: Estimated number of items that should be present in response. Defaults to 100. Note that response can contain a bit more or a bit less responses due to internal mechanisms.
          required: false
          schema:
            type: integer
            minimum: 1
            maximum: 1000
        - name: created_after
          in: query
          description: Filter for collection created after this date
          required: false
          schema:
            type: string
            format: date-time
        - name: created_before
          in: query
          description: Filter for collection created before this date
          required: false
          schema:
            type: string
            format: date-time
    responses:
        200:
            description: the list of available collections
            content:
                application/json:
                    schema:
                        $ref: '#/components/schemas/GeoVisioCollections'
    """

    args = request.args
    limit = args.get("limit", SEQUENCES_DEFAULT_FETCH)
    created_after = args.get("created_after")
    created_before = args.get("created_before")

    # Check if limit is valid
    try:
        limit = int(limit)
    except ValueError:
        raise errors.InvalidAPIUsage(f"limit parameter should be a valid, positive integer (between 1 and {SEQUENCES_MAX_FETCH})")
    if limit < 1 or limit > SEQUENCES_MAX_FETCH:
        raise errors.InvalidAPIUsage(f"limit parameter should be an integer between 1 and {SEQUENCES_MAX_FETCH}")
    params: dict = {"limit": limit}

    seq_filter = [SQL("s.status = 'ready'")]

    fields = SQL(
        """s.id,
                s.metadata->>'title' AS name,
                ST_XMin(s.geom) AS minx,
                ST_YMin(s.geom) AS miny,
                ST_XMax(s.geom) AS maxx,
                ST_YMax(s.geom) AS maxy,
                accounts.name AS account_name,
                s.inserted_at,
                s.updated_at"""
    )

    sequence_table = SQL(
        """SELECT {fields}
                FROM sequences s
                JOIN accounts ON accounts.id = s.account_id
                WHERE {sequence_filter}
                ORDER BY s.inserted_at
                LIMIT %(limit)s"""
    )

    if created_after:
        created_after = parse_datetime(created_after, error=f"Invalid `created_after` argument", fallback_as_UTC=True)
        seq_filter.append(SQL("s.inserted_at > %(created_after)s::timestamp with time zone"))
        params["created_after"] = created_after

    if created_before:
        created_before = parse_datetime(created_before, error=f"Invalid `created_before` argument", fallback_as_UTC=True)
        seq_filter.append(SQL("s.inserted_at < %(created_before)s::timestamp with time zone"))
        params["created_before"] = created_before

        if not created_after:
            # If there is only a created_before parameter, we want all last collections that have been created before the date
            sequence_table = SQL(
                """SELECT * FROM (
                    SELECT {fields}
                        FROM sequences s 
                        JOIN accounts ON accounts.id = s.account_id
                        WHERE {sequence_filter}
                        ORDER BY s.inserted_at DESC
                        LIMIT %(limit)s
                    ) s
                    ORDER BY s.inserted_at
                """
            )

    paginated = limit is not None or created_after is not None or created_before is not None

    sequence_table = sequence_table.format(sequence_filter=SQL(" AND ").join(seq_filter), fields=fields)
    with psycopg.connect(current_app.config["DB_URL"], row_factory=dict_row) as conn:
        with conn.cursor() as cursor:
            stats = cursor.execute("SELECT min(inserted_at) as min, max(inserted_at) as max FROM sequences").fetchone()
            inserted_at_bound = (stats["min"], stats["max"]) if stats is not None else (None, None)

            if inserted_at_bound[1] and created_after and created_after > inserted_at_bound[1]:
                raise errors.InvalidAPIUsage(f"There is no collection created after {created_after}")
            if inserted_at_bound[0] and created_before and created_before < inserted_at_bound[0]:
                raise errors.InvalidAPIUsage(f"There is no collection created before {created_before}")

            query = SQL(
                """
                SELECT *
                    FROM (
                        {sequence_table}
                    ) s
                LEFT JOIN LATERAL (
                        SELECT MIN(p.ts) as mints,
                                MAX(p.ts) as maxts,
                                COUNT(p.*) AS nbpic
                        FROM sequences_pictures sp
                                JOIN pictures p ON sp.pic_id = p.id
                        WHERE p.status = 'ready'
                                AND sp.seq_id = s.id
                        GROUP BY sp.seq_id
                ) sub ON true;
                """
            ).format(sequence_table=sequence_table)
            records = cursor.execute(
                query,
                params,
            ).fetchall()
            # print(f"  sql = {psycopg.ClientCursor(conn).mogrify(query, params)}")

            collections = []
            min_inserted_at = None
            max_inserted_at = None
            for dbSeq in records:
                if min_inserted_at is None:
                    min_inserted_at = dbSeq["inserted_at"]
                max_inserted_at = dbSeq["inserted_at"]
                collections.append(dbSequenceToStacCollection(dbSeq))

            # Compute paginated links
            links = [
                _get_root_link(),
                {"rel": "parent", "type": "application/json", "href": url_for("stac.getLanding", _external=True)},
                {
                    "rel": "self",
                    "type": "application/json",
                    "href": url_for(
                        "stac.getAllCollections", _external=True, limit=args.get("limit"), created_after=args.get("created_after")
                    ),
                },
            ]

            links.append(
                {"rel": "first", "type": "application/json", "href": url_for("stac.getAllCollections", _external=True, limit=limit)}
            )
            if paginated:
                if inserted_at_bound[1]:
                    links.append(
                        {
                            "rel": "last",
                            "type": "application/json",
                            "href": url_for(
                                "stac.getAllCollections",
                                _external=True,
                                limit=limit,
                                created_before=dbTsToStac(inserted_at_bound[1] + datetime.timedelta(seconds=1)),
                            ),
                        }
                    )

            has_more_sequences_before = min_inserted_at > inserted_at_bound[0] if inserted_at_bound[0] and min_inserted_at else False
            if has_more_sequences_before:
                links.append(
                    {
                        "rel": "prev",
                        "type": "application/json",
                        "href": url_for("stac.getAllCollections", _external=True, limit=limit, created_before=dbTsToStac(min_inserted_at)),
                    }
                )

            has_more_sequences_after = max_inserted_at < inserted_at_bound[1] if inserted_at_bound[1] and max_inserted_at else False
            if has_more_sequences_after:
                links.append(
                    {
                        "rel": "next",
                        "type": "application/json",
                        "href": url_for("stac.getAllCollections", _external=True, limit=limit, created_after=dbTsToStac(max_inserted_at)),
                    }
                )

            return (
                {
                    "collections": collections,
                    "links": links,
                },
                200,
                {"Content-Type": "application/json"},
            )


@bp.route("/collections/<uuid:collectionId>")
def getCollection(collectionId):
    """Retrieve metadata of a single collection
    ---
    tags:
        - Sequences
    parameters:
        - name: collectionId
          in: path
          description: ID of collection to retrieve
          required: true
          schema:
            type: string
    responses:
        200:
            description: the collection metadata
            content:
                application/json:
                    schema:
                        $ref: '#/components/schemas/GeoVisioCollection'
    """

    account = auth.get_current_account()

    params = {
        "id": collectionId,
        # Only the owner of an account can view sequence not 'ready'
        "account": account.id if account is not None else None,
    }

    with psycopg.connect(current_app.config["DB_URL"], row_factory=dict_row) as conn:
        with conn.cursor() as cursor:
            record = cursor.execute(
                """
				SELECT
					s.id, s.metadata->>'title' AS name,
					ST_XMin(s.geom) AS minx,
					ST_YMin(s.geom) AS miny,
					ST_XMax(s.geom) AS maxx,
					ST_YMax(s.geom) AS maxy,
					s.status,
     			accounts.name AS account_name,
     			s.inserted_at,
     			s.updated_at,
					a.*
				FROM sequences s
				JOIN accounts ON s.account_id = accounts.id, (
					SELECT
						MIN(ts) as mints,
						MAX(ts) as maxts,
						array_agg(DISTINCT jsonb_build_object(
							'make', metadata->>'make',
							'model', metadata->>'model',
							'focal_length', metadata->>'focal_length',
							'field_of_view', metadata->>'field_of_view'
						)) AS metas,
						COUNT(*) AS nbpic
					FROM pictures p
					JOIN sequences_pictures sp ON sp.seq_id = %(id)s AND sp.pic_id = p.id
				) a
				WHERE s.id = %(id)s
					AND (s.status != 'hidden' OR s.account_id = %(account)s)
			""",
                params,
            ).fetchone()

            if record is None:
                raise errors.InvalidAPIUsage("Collection doesn't exist", status_code=404)

            return (
                dbSequenceToStacCollection(record),
                200,
                {
                    "Content-Type": "application/json",
                },
            )


@bp.route("/users/<uuid:userId>/catalog/")
@auth.isUserIdMatchingCurrentAccount()
def getUserCatalog(userId, userIdMatchesAccount=False):
    """Retrieves an user list of sequences (catalog)
    ---
    tags:
        - Sequences
        - Users
    parameters:
        - name: userId
          in: path
          description: User ID
          required: true
          schema:
            type: string
    responses:
        200:
            description: the Catalog listing all sequences associated to given user
            content:
                application/json:
                    schema:
                        $ref: '#/components/schemas/GeoVisioCatalog'
    """

    with psycopg.connect(current_app.config["DB_URL"]) as conn:
        with conn.cursor() as cursor:
            userName = cursor.execute("SELECT name FROM accounts WHERE id = %s", [userId]).fetchone()

            if not userName:
                raise errors.InvalidAPIUsage(f"Impossible to find user {userId}")
            userName = userName[0]
            sqlSequencesConds = ["s.account_id = %s"]

            if not userIdMatchesAccount:
                sqlSequencesConds.append("s.status = 'ready'")
                sqlSequencesConds.append("p.status = 'ready'")

            sqlSequences = (
                """
				SELECT
					s.id,
					COUNT(sp.pic_id) AS nb_pics,
					s.status,
					s.metadata->>'title' AS title,
					MIN(p.ts) AS mints,
					MAX(p.ts) AS maxts
				FROM sequences s
				LEFT JOIN sequences_pictures sp ON s.id = sp.seq_id
				LEFT JOIN pictures p on sp.pic_id = p.id
				WHERE """
                + " AND ".join(sqlSequencesConds)
                + """
				GROUP BY s.id
			"""
            )

            sequences = [
                removeNoneInDict(
                    {
                        "id": s[0],
                        "title": s[3],
                        "rel": "child",
                        "href": url_for("stac.getCollection", _external=True, collectionId=s[0]),
                        "stats:items": {"count": s[1]},
                        "extent": {
                            "temporal": {
                                "interval": [
                                    [
                                        dbTsToStac(s[4]),
                                        dbTsToStac(s[5]),
                                    ]
                                ]
                            }
                        },
                        "geovisio:status": s[2] if userIdMatchesAccount else None,
                    }
                )
                for s in cursor.execute(sqlSequences, [userId]).fetchall()
            ]

            return (
                dbSequencesToStacCatalog(
                    f"user:{userId}",
                    f"{userName}'s sequences",
                    f"List of all sequences of user {userName}",
                    sequences,
                    request,
                    userId=str(userId),
                ),
                200,
                {"Content-Type": "application/json"},
            )

        raise errors.InvalidAPIUsage("Failed to connect to database", status_code=500)

    raise errors.InvalidAPIUsage("Failed to connect to database", status_code=500)


def removeNoneInDict(val):
    """Removes empty values from dictionnary"""
    return {k: v for k, v in val.items() if v is not None}


def cleanNoneInDict(val):
    """Removes empty values from dictionnary, and return None if dict is empty"""
    res = removeNoneInDict(val)
    return res if len(res) > 0 else None


def cleanNoneInList(val: typing.List) -> typing.List:
    """Removes empty values from list"""
    return list(filter(lambda e: e is not None, val))


def dbTsToStac(dbts):
    """Transforms timestamp returned by PostgreSQL into UTC ISO format expected by STAC"""
    return dbts.astimezone(tz.gettz("UTC")).isoformat() if dbts is not None else None


def dbPictureToStacItem(seqId, dbPic):
    """Transforms a picture extracted from database into a STAC Item

    Parameters
    ----------
    seqId : uuid
        Associated sequence ID
    dbSeq : dict
        A row from pictures table in database (with id, geojson, ts, heading, cols, rows, width, height, prevpic, nextpic, prevpicgeojson, nextpicgeojson fields)

    Returns
    -------
    object
        The equivalent in STAC Item format
    """

    item = removeNoneInDict(
        {
            "type": "Feature",
            "stac_version": STAC_VERSION,
            "stac_extensions": [
                "https://stac-extensions.github.io/view/v1.0.0/schema.json",  # "view:" fields
                "https://stac-extensions.github.io/perspective-imagery/v1.0.0/schema.json",  # "pers:" fields
            ],
            "id": str(dbPic["id"]),
            "geometry": dbPic["geojson"],
            "bbox": dbPic["geojson"]["coordinates"] + dbPic["geojson"]["coordinates"],
            "providers": [
                {"name": dbPic["account_name"], "roles": ["producer"]},
            ],
            "properties": {
                "datetime": dbTsToStac(dbPic["ts"]),
                "created": dbTsToStac(dbPic["processed_at"]),
                # TODO : add "updated" TS for last edit time of metadata
                "license": current_app.config["API_PICTURES_LICENSE_SPDX_ID"],
                "view:azimuth": dbPic["heading"],
                "pers:interior_orientation": removeNoneInDict(
                    {
                        "camera_manufacturer": dbPic["metadata"].get("make"),
                        "camera_model": dbPic["metadata"].get("model"),
                        "focal_length": dbPic["metadata"].get("focal_length"),
                        "field_of_view": dbPic["metadata"].get("field_of_view"),
                    }
                )
                if "metadata" in dbPic
                and len([True for f in dbPic["metadata"] if f in ["make", "model", "focal_length", "field_of_view"]]) > 0
                else {},
                "geovisio:status": dbPic.get("status"),
            },
            "links": cleanNoneInList(
                [
                    _get_root_link(),
                    {
                        "rel": "parent",
                        "type": "application/json",
                        "href": url_for("stac.getCollection", _external=True, collectionId=seqId),
                    },
                    {
                        "rel": "self",
                        "type": "application/geo+json",
                        "href": url_for("stac.getCollectionItem", _external=True, collectionId=seqId, itemId=dbPic["id"]),
                    },
                    {
                        "rel": "collection",
                        "type": "application/json",
                        "href": url_for("stac.getCollection", _external=True, collectionId=seqId),
                    },
                    _get_license_link(),
                ]
            ),
            "assets": {
                "hd": {
                    "title": "HD picture",
                    "description": "Highest resolution available of this picture",
                    "roles": ["data"],
                    "type": "image/jpeg",
                    "href": _getHDJpgPictureURL(dbPic["id"], status=dbPic.get("status")),
                },
                "sd": {
                    "title": "SD picture",
                    "description": "Picture in standard definition (fixed width of 2048px)",
                    "roles": ["visual"],
                    "type": "image/jpeg",
                    "href": _getSDJpgPictureURL(dbPic["id"], status=dbPic.get("status")),
                },
                "thumb": {
                    "title": "Thumbnail",
                    "description": "Picture in low definition (fixed width of 500px)",
                    "roles": ["thumbnail"],
                    "type": "image/jpeg",
                    "href": _getThumbJpgPictureURL(dbPic["id"], status=dbPic.get("status")),
                },
            },
            "collection": str(seqId),
        }
    )

    # Next / previous links if any
    if "nextpic" in dbPic and dbPic["nextpic"] is not None:
        item["links"].append(
            {
                "rel": "next",
                "type": "application/geo+json",
                "geometry": dbPic["nextpicgeojson"],
                "id": dbPic["nextpic"],
                "href": url_for("stac.getCollectionItem", _external=True, collectionId=seqId, itemId=dbPic["nextpic"]),
            }
        )

    if "prevpic" in dbPic and dbPic["prevpic"] is not None:
        item["links"].append(
            {
                "rel": "prev",
                "type": "application/geo+json",
                "geometry": dbPic["prevpicgeojson"],
                "id": dbPic["prevpic"],
                "href": url_for("stac.getCollectionItem", _external=True, collectionId=seqId, itemId=dbPic["prevpic"]),
            }
        )

    #
    # Picture type-specific properties
    #

    # Equirectangular
    if dbPic["metadata"]["type"] == "equirectangular":
        item["stac_extensions"].append("https://stac-extensions.github.io/tiled-assets/v1.0.0/schema.json")  # "tiles:" fields

        item["properties"]["tiles:tile_matrix_sets"] = {
            "geovisio": {
                "type": "TileMatrixSetType",
                "title": "GeoVisio tile matrix for picture " + str(dbPic["id"]),
                "identifier": "geovisio-" + str(dbPic["id"]),
                "tileMatrix": [
                    {
                        "type": "TileMatrixType",
                        "identifier": "0",
                        "scaleDenominator": 1,
                        "topLeftCorner": [0, 0],
                        "tileWidth": dbPic["metadata"]["width"] / dbPic["metadata"]["cols"],
                        "tileHeight": dbPic["metadata"]["height"] / dbPic["metadata"]["rows"],
                        "matrixWidth": dbPic["metadata"]["cols"],
                        "matrixHeight": dbPic["metadata"]["rows"],
                    }
                ],
            }
        }

        item["asset_templates"] = {
            "tiles": {
                "title": "HD tiled picture",
                "description": "Highest resolution available of this picture, as tiles",
                "roles": ["data"],
                "type": "image/jpeg",
                "href": _getTilesJpgPictureURL(dbPic["id"], status=dbPic.get("status")),
            }
        }

    return item


def as_uuid(value: str, error: str) -> UUID:
    """Convert the value to an UUID and raises an error if it's not possible"""
    try:
        return UUID(value)
    except ValueError:
        raise errors.InvalidAPIUsage(error)


@bp.route("/collections/<uuid:collectionId>/thumb.jpg", methods=["GET"])
def getCollectionThumbnail(collectionId):
    """Get the thumbnail representing a single collection
    ---
    tags:
        - Sequences
    parameters:
        - name: collectionId
          in: path
          description: ID of collection to retrieve
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
    """
    account = auth.get_current_account()

    params = {
        "seq": collectionId,
        # Only the owner of an account can view pictures not 'ready'
        "account": account.id if account is not None else None,
    }

    with psycopg.connect(current_app.config["DB_URL"], row_factory=dict_row) as conn:
        with conn.cursor() as cursor:
            records = cursor.execute(
                """
				SELECT
					sp.pic_id
				FROM sequences_pictures sp
				JOIN pictures p ON sp.pic_id = p.id
				JOIN sequences s ON sp.seq_id = s.id
				WHERE
					sp.seq_id = %(seq)s
					AND (p.status = 'ready' OR p.account_id = %(account)s)
					AND (s.status = 'ready' OR s.account_id = %(account)s)
				LIMIT 1
			""",
                params,
            ).fetchone()

            if records is None:
                raise errors.InvalidAPIUsage("Impossible to find a thumbnail for the collection", status_code=404)

            return pictures.sendThumbnail(records["pic_id"], "jpg")


def get_first_rank_of_page(rankToHave: int, limit: Optional[int]) -> int:
    """if there is a limit, we try to emulate a page, so we'll return the nth page that should contain this picture
    Note: the ranks starts from 1
    >>> get_first_rank_of_page(3, 2)
    3
    >>> get_first_rank_of_page(4, 2)
    3
    >>> get_first_rank_of_page(3, None)
    3
    >>> get_first_rank_of_page(123, 10)
    121
    >>> get_first_rank_of_page(10, 10)
    1
    >>> get_first_rank_of_page(10, 100)
    1
    """
    if not limit:
        return rankToHave

    return int((rankToHave - 1) / limit) * limit + 1


@bp.route("/collections/<uuid:collectionId>/items", methods=["GET"])
def getCollectionItems(collectionId):
    """List items of a single collection
    ---
    tags:
        - Sequences
    parameters:
        - name: collectionId
          in: path
          description: ID of collection to retrieve
          required: true
          schema:
            type: string
        - name: limit
          in: query
          description: Number of items that should be present in response. Unlimited by default.
          required: false
          schema:
            type: integer
            minimum: 1
            maximum: 10000
        - name: startAfterRank
          in: query
          description: Position of last received picture in sequence. Response will start with the following picture.
          required: false
          schema:
            type: integer
            minimum: 1
        - name: withPicture
          in: query
          description: Used in the pagination context, if present, the api will return the given picture in the results.
            Can be used in the same time as the `limit` parameter, but not with the `startAfterRank` parameter.
          required: false
          schema:
            type: string
            format: uuid
    responses:
        200:
            description: the items list
            content:
                application/geo+json:
                    schema:
                        $ref: '#/components/schemas/GeoVisioCollectionItems'
    """

    account = auth.get_current_account()

    params = {
        "seq": collectionId,
        # Only the owner of an account can view pictures not 'ready'
        "account": account.id if account is not None else None,
    }

    args = request.args
    limit = args.get("limit")
    startAfterRank = args.get("startAfterRank")
    withPicture = args.get("withPicture")

    filters = [
        SQL("sp.seq_id = %(seq)s"),
        SQL("(p.status = 'ready' OR p.account_id = %(account)s)"),
        SQL("(s.status = 'ready' OR s.account_id = %(account)s)"),
    ]

    # Check if limit is valid
    sql_limit = SQL("")
    if limit is not None:
        try:
            limit = int(limit)
            if limit < 1 or limit > 10000:
                raise errors.InvalidAPIUsage("limit parameter should be an integer between 1 and 10000", status_code=400)
        except ValueError:
            raise errors.InvalidAPIUsage("limit parameter should be a valid, positive integer (between 1 and 10000)", status_code=400)
        sql_limit = SQL("LIMIT %(limit)s")
        params["limit"] = limit

    if withPicture and startAfterRank:
        raise errors.InvalidAPIUsage(f"`startAfterRank` and `withPicture` are mutually exclusive parameters")

    # Check if rank is valid
    if startAfterRank is not None:
        try:
            startAfterRank = int(startAfterRank)
            if startAfterRank < 1:
                raise errors.InvalidAPIUsage("startAfterRank parameter should be a positive integer (starting from 1)", status_code=400)
        except ValueError:
            raise errors.InvalidAPIUsage("startAfterRank parameter should be a valid, positive integer", status_code=400)

        filters.append(SQL("rank > %(start_after_rank)s"))
        params["start_after_rank"] = startAfterRank

    paginated = startAfterRank is not None or limit is not None or withPicture is not None

    with psycopg.connect(current_app.config["DB_URL"], row_factory=dict_row) as conn:
        with conn.cursor() as cursor:
            # check on sequence
            seqMeta = cursor.execute(
                "SELECT s.id "
                + (", MAX(sp.rank) AS max_rank, MIN(sp.rank) AS min_rank " if paginated else "")
                + "FROM sequences s "
                + ("LEFT JOIN sequences_pictures sp ON sp.seq_id = s.id " if paginated else "")
                + "WHERE s.id = %(seq)s AND (s.status = 'ready' OR s.account_id = %(account)s) "
                + ("GROUP BY s.id" if paginated else ""),
                params,
            ).fetchone()

            if seqMeta is None:
                raise errors.InvalidAPIUsage("Collection doesn't exist", status_code=404)

            maxRank = seqMeta.get("max_rank")

            if startAfterRank is not None and startAfterRank >= maxRank:
                raise errors.InvalidAPIUsage(f"No more items in this collection (last available rank is {maxRank})", status_code=404)

            if withPicture is not None:
                withPicture = as_uuid(withPicture, "withPicture should be a valid UUID")
                pic = cursor.execute(
                    "SELECT rank FROM pictures p JOIN sequences_pictures sp ON sp.pic_id = p.id WHERE p.id = %(id)s AND sp.seq_id = %(seq)s",
                    params={"id": withPicture, "seq": collectionId},
                ).fetchone()
                if not pic:
                    raise errors.InvalidAPIUsage(f"Picture with id {withPicture} does not exists")
                rank = get_first_rank_of_page(pic["rank"], limit)

                filters.append(SQL("rank >= %(start_after_rank)s"))
                params["start_after_rank"] = rank

            query = SQL(
                """
				SELECT
					p.id, p.ts, p.heading, p.metadata, p.processed_at, p.status,
					ST_AsGeoJSON(p.geom)::json AS geojson,
					a.name AS account_name,
                    sp.rank,
					CASE WHEN LAG(p.status) OVER othpics = 'ready' THEN LAG(p.id) OVER othpics END AS prevpic,
					CASE WHEN LAG(p.status) OVER othpics = 'ready' THEN ST_AsGeoJSON(LAG(p.geom) OVER othpics)::json END AS prevpicgeojson,
					CASE WHEN LEAD(p.status) OVER othpics = 'ready' THEN LEAD(p.id) OVER othpics END AS nextpic,
					CASE WHEN LEAD(p.status) OVER othpics = 'ready' THEN ST_AsGeoJSON(LEAD(p.geom) OVER othpics)::json END AS nextpicgeojson
				FROM sequences_pictures sp
				JOIN pictures p ON sp.pic_id = p.id
				JOIN accounts a ON a.id = p.account_id
				JOIN sequences s ON s.id = sp.seq_id
				WHERE
    				{filter}
				WINDOW othpics AS (PARTITION BY sp.seq_id ORDER BY sp.rank)
				ORDER BY rank
                {limit}
                """
            ).format(filter=SQL(" AND ").join(filters), limit=sql_limit)

            records = cursor.execute(query, params)

            min_query_rank, max_query_rank = None, None
            items = []
            for dbPic in records:
                if not min_query_rank:
                    min_query_rank = dbPic["rank"]
                max_query_rank = dbPic["rank"]
                items.append(dbPictureToStacItem(collectionId, dbPic))

            links = [
                _get_root_link(),
                {
                    "rel": "parent",
                    "type": "application/json",
                    "href": url_for("stac.getCollection", _external=True, collectionId=collectionId),
                },
                {
                    "rel": "self",
                    "type": "application/geo+json",
                    "href": url_for(
                        "stac.getCollectionItems", _external=True, collectionId=collectionId, limit=limit, startAfterRank=startAfterRank
                    ),
                },
            ]

            if paginated and items:
                links.append(
                    {
                        "rel": "first",
                        "type": "application/geo+json",
                        "href": url_for("stac.getCollectionItems", _external=True, collectionId=collectionId, limit=limit),
                    }
                )
                has_item_before = min_query_rank > seqMeta["min_rank"]
                if has_item_before:
                    # Previous page link
                    #   - If limit is set, rank is current - limit
                    #   - If no limit is set, rank is 0 (none)
                    if startAfterRank is not None:
                        prevRank = startAfterRank - limit if limit is not None else 0
                        if prevRank < 1:
                            prevRank = None
                        links.append(
                            {
                                "rel": "prev",
                                "type": "application/geo+json",
                                "href": url_for(
                                    "stac.getCollectionItems",
                                    _external=True,
                                    collectionId=collectionId,
                                    limit=limit,
                                    startAfterRank=prevRank,
                                ),
                            }
                        )

                has_item_after = max_query_rank < seqMeta["max_rank"]
                if has_item_after:
                    links.append(
                        {
                            "rel": "next",
                            "type": "application/geo+json",
                            "href": url_for(
                                "stac.getCollectionItems",
                                _external=True,
                                collectionId=collectionId,
                                limit=limit,
                                startAfterRank=max_query_rank,
                            ),
                        }
                    )

                # Last page link
                #   - If this page is the last one, rank equals to rank given by user
                #   - Otherwise, rank equals max rank - limit

                lastPageRank = startAfterRank
                if limit is not None:
                    if seqMeta["max_rank"] > max_query_rank:
                        lastPageRank = seqMeta["max_rank"] - limit
                        if lastPageRank < max_query_rank:
                            lastPageRank = max_query_rank

                links.append(
                    {
                        "rel": "last",
                        "type": "application/geo+json",
                        "href": url_for(
                            "stac.getCollectionItems",
                            _external=True,
                            collectionId=collectionId,
                            limit=limit,
                            startAfterRank=lastPageRank,
                        ),
                    }
                )

            return (
                {
                    "type": "FeatureCollection",
                    "features": items,
                    "links": links,
                },
                200,
                {"Content-Type": "application/geo+json"},
            )


def _getPictureItemById(collectionId, itemId):
    """Get a picture metadata by its ID and collection ID

    ---
    tags:
        - Pictures
    parameters:
        - name: collectionId
          in: path
          description: ID of collection to retrieve
          required: true
          schema:
            type: string
        - name: itemId
          in: path
          description: ID of item to retrieve
          required: true
          schema:
            type: string
    """
    with psycopg.connect(current_app.config["DB_URL"], row_factory=dict_row) as conn:
        with conn.cursor() as cursor:
            # Check if there is a logged user
            account = auth.get_current_account()
            accountId = account.id if account else None

            # Get rank + position of wanted picture
            record = cursor.execute(
                """
				SELECT
    				p.id, sp.rank, ST_AsGeoJSON(p.geom)::json AS geojson, p.heading, p.ts, p.metadata, p.processed_at, p.status, accounts.name AS account_name,
					spl.prevpic, spl.prevpicgeojson, spl.nextpic, spl.nextpicgeojson
				FROM pictures p
				JOIN sequences_pictures sp ON sp.pic_id = p.id
				JOIN accounts ON p.account_id = accounts.id
				JOIN sequences s ON sp.seq_id = s.id
				LEFT JOIN (
					SELECT
						p.id,
						LAG(p.id) OVER othpics AS prevpic,
						ST_AsGeoJSON(LAG(p.geom) OVER othpics)::json AS prevpicgeojson,
						LEAD(p.id) OVER othpics AS nextpic,
						ST_AsGeoJSON(LEAD(p.geom) OVER othpics)::json AS nextpicgeojson
					FROM pictures p
					JOIN sequences_pictures sp ON p.id = sp.pic_id
					WHERE
						sp.seq_id = %(seq)s
						AND (p.account_id = %(acc)s OR p.status != 'hidden')
					WINDOW othpics AS (PARTITION BY sp.seq_id ORDER BY sp.rank)
				) spl ON p.id = spl.id
				WHERE sp.seq_id = %(seq)s
					AND p.id = %(pic)s
					AND (p.account_id = %(acc)s OR p.status != 'hidden')
					AND (s.account_id = %(acc)s OR s.status != 'hidden')
				""",
                {"seq": collectionId, "pic": itemId, "acc": accountId},
            ).fetchone()

            if record is None:
                return None

            return dbPictureToStacItem(collectionId, record)


@bp.route("/collections/<uuid:collectionId>/items/<uuid:itemId>")
def getCollectionItem(collectionId, itemId):
    """Get a single item from a collection
    ---
    tags:
        - Pictures
    parameters:
        - name: collectionId
          in: path
          description: ID of collection to retrieve
          required: true
          schema:
            type: string
        - name: itemId
          in: path
          description: ID of item to retrieve
          required: true
          schema:
            type: string
    responses:
        102:
            description: the item (which is still under process)
            content:
                application/geo+json:
                    schema:
                        $ref: '#/components/schemas/GeoVisioItem'
        200:
            description: the wanted item
            content:
                application/geo+json:
                    schema:
                        $ref: '#/components/schemas/GeoVisioItem'
    """

    stacItem = _getPictureItemById(collectionId, itemId)
    if stacItem is None:
        raise errors.InvalidAPIUsage("Item doesn't exist", status_code=404)

    account = auth.get_current_account()
    picStatusToHttpCode = {
        "preparing": 102,
        "preparing-derivates": 102,
        "preparing-blur": 102,
        "waiting-for-process": 102,
        "ready": 200,
        "hidden": 200 if account else 404,
        "broken": 500,
    }
    return stacItem, picStatusToHttpCode[stacItem["properties"]["geovisio:status"]], {"Content-Type": "application/geo+json"}


@bp.route("/search", methods=["GET", "POST"])
def searchItems():
    """Search through all available items
    ---
    tags:
        - Pictures
    get:
        parameters:
            - $ref: 'https://api.stacspec.org/v1.0.0/item-search/openapi.yaml#/components/parameters/bbox'
            - $ref: 'https://api.stacspec.org/v1.0.0/item-search/openapi.yaml#/components/parameters/intersects'
            - $ref: 'https://api.stacspec.org/v1.0.0/item-search/openapi.yaml#/components/parameters/datetime'
            - $ref: 'https://api.stacspec.org/v1.0.0/item-search/openapi.yaml#/components/parameters/limit'
            - $ref: 'https://api.stacspec.org/v1.0.0/item-search/openapi.yaml#/components/parameters/ids'
            - $ref: 'https://api.stacspec.org/v1.0.0/item-search/openapi.yaml#/components/parameters/collectionsArray'
    post:
        requestBody:
            content:
              application/json:
                schema:
                  $ref: 'https://api.stacspec.org/v1.0.0/item-search/openapi.yaml#/components/schemas/searchBody'
    responses:
        200:
            description: the items list
            content:
                application/geo+json:
                    schema:
                        $ref: 'https://api.stacspec.org/v1.0.0/item-search/openapi.yaml#/components/schemas/itemCollection'
    """

    account = auth.get_current_account()
    accountId = account.id if account is not None else None
    sqlWhere = ["(p.status = 'ready' OR p.account_id = %(account)s)", "(s.status = 'ready' OR s.account_id = %(account)s)"]
    sqlParams = {"account": accountId}
    sqlSubQueryWhere = ["(p.status = 'ready'OR p.account_id = %(account)s)"]

    #
    # Parameters parsing and verification
    #

    # Method + content-type
    args = None
    if request.method == "GET":
        args = request.args
    elif request.method == "POST":
        if request.headers.get("Content-Type") == "application/json":
            args = MultiDict(request.json)
        else:
            raise errors.InvalidAPIUsage("Search using POST method should have a JSON body", status_code=400)

    # Limit
    if args.get("limit") is not None:
        limit = args.get("limit", type=int)
        if limit is None or limit < 1 or limit > 10000:
            raise errors.InvalidAPIUsage("Parameter limit must be either empty or a number between 1 and 10000", status_code=400)
        else:
            sqlParams["limit"] = limit
    else:
        sqlParams["limit"] = 10000

    # Bounding box
    if args.get("bbox") is not None:
        try:
            bbox = [float(n) for n in args.get("bbox")[1:-1].split(",")]
            if len(bbox) != 4 or not all(isinstance(x, float) for x in bbox):
                raise ValueError()
            elif (
                bbox[0] < -180
                or bbox[0] > 180
                or bbox[1] < -90
                or bbox[1] > 90
                or bbox[2] < -180
                or bbox[2] > 180
                or bbox[3] < -90
                or bbox[3] > 90
            ):
                raise errors.InvalidAPIUsage(
                    "Parameter bbox must contain valid longitude (-180 to 180) and latitude (-90 to 90) values", status_code=400
                )
            else:
                sqlWhere.append("p.geom && ST_MakeEnvelope(%(minx)s, %(miny)s, %(maxx)s, %(maxy)s, 4326)")
                sqlParams["minx"] = bbox[0]
                sqlParams["miny"] = bbox[1]
                sqlParams["maxx"] = bbox[2]
                sqlParams["maxy"] = bbox[3]
        except ValueError:
            raise errors.InvalidAPIUsage("Parameter bbox must be in format [minX, minY, maxX, maxY]", status_code=400)

    # Datetime
    if args.get("datetime") is not None:
        try:
            dates = args.get("datetime").split("/")

            if len(dates) == 1:
                date = dateparser(dates[0])
                sqlWhere.append("p.ts = %(ts)s::timestamp with time zone")
                sqlParams["ts"] = date

            elif len(dates) == 2:
                # Check if interval is closed or open-ended
                if dates[0] == "..":
                    date = dateparser(dates[1])
                    sqlWhere.append("p.ts <= %(ts)s::timestamp with time zone")
                    sqlParams["ts"] = date
                elif dates[1] == "..":
                    date = dateparser(dates[0])
                    sqlWhere.append("p.ts >= %(ts)s::timestamp with time zone")
                    sqlParams["ts"] = date
                else:
                    date0 = dateparser(dates[0])
                    date1 = dateparser(dates[1])
                    sqlWhere.append("p.ts >= %(mints)s::timestamp with time zone")
                    sqlWhere.append("p.ts <= %(maxts)s::timestamp with time zone")
                    sqlParams["mints"] = date0
                    sqlParams["maxts"] = date1
            else:
                raise errors.InvalidAPIUsage("Parameter datetime should contain one or two dates", status_code=400)
        except:
            raise errors.InvalidAPIUsage("Parameter datetime contains an invalid date definition", status_code=400)

    # Intersects
    if args.get("intersects") is not None:
        try:
            intersects = json.loads(args.get("intersects"))
            if intersects["type"] == "Point":
                sqlWhere.append("ST_DWithin(p.geom::geography, ST_GeomFromGeoJSON(%(geom)s)::geography, 0.01)")
            else:
                sqlWhere.append("p.geom && ST_GeomFromGeoJSON(%(geom)s)")
                sqlWhere.append("ST_Intersects(p.geom, ST_GeomFromGeoJSON(%(geom)s))")
            sqlParams["geom"] = Jsonb(intersects)
        except:
            raise errors.InvalidAPIUsage("Parameter intersects should contain a valid GeoJSON Geometry (not a Feature)", status_code=400)

    # Ids
    if args.get("ids") is not None:
        sqlWhere.append("p.id = ANY(%(ids)s)")
        try:
            sqlParams["ids"] = [UUID(j) for j in json.loads(args.get("ids"))]
        except:
            raise errors.InvalidAPIUsage("Parameter ids should be a JSON array of strings", status_code=400)

    # Collections
    if args.get("collections") is not None:
        try:
            collections_json = json.loads(args["collections"])
        except:
            raise errors.InvalidAPIUsage("Parameter collections should be a JSON array of strings", status_code=400)
        sqlWhere.append("sp.seq_id = ANY(%(collections)s)")
        sqlParams["collections"] = [UUID(j) for j in collections_json]

        # custom subquery filtering to help PG query plan
        sqlSubQueryWhere.append("sp.seq_id = ANY(%(collections)s)")

    # To speed up search, if it's a search by id and on only one id, we use the same code as /collections/:cid/items/:id
    if args.get("ids") is not None and args:
        ids = json.loads(args.get("ids"))
        if len(ids) == 1:
            picture_id = ids[0]

            with psycopg.connect(current_app.config["DB_URL"]) as conn, conn.cursor() as cursor:
                seq = cursor.execute("SELECT seq_id FROM sequences_pictures WHERE pic_id = %s", [picture_id]).fetchone()
                if not seq:
                    raise errors.InvalidAPIUsage("Picture doesn't exist", status_code=404)

                item = _getPictureItemById(seq[0], UUID(picture_id))
                features = [item] if item else []
                return (
                    {"type": "FeatureCollection", "features": features, "links": [_get_root_link()]},
                    200,
                    {"Content-Type": "application/geo+json"},
                )

    #
    # Database query
    #

    with psycopg.connect(current_app.config["DB_URL"], row_factory=dict_row, options="-c statement_timeout=30000") as conn:
        with conn.cursor() as cursor:
            query = (
                """
				SELECT
					p.id, p.ts, p.heading, p.metadata, p.processed_at,
					ST_AsGeoJSON(p.geom)::json AS geojson,
					sp.seq_id,
					spl.prevpic, spl.prevpicgeojson, spl.nextpic, spl.nextpicgeojson,
					accounts.name AS account_name
				FROM pictures p
				LEFT JOIN sequences_pictures sp ON p.id = sp.pic_id
				LEFT JOIN sequences s ON s.id = sp.seq_id
				LEFT JOIN accounts ON p.account_id = accounts.id
				LEFT JOIN (
					SELECT
						p.id,
						LAG(p.id) OVER othpics AS prevpic,
						ST_AsGeoJSON(LAG(p.geom) OVER othpics)::json AS prevpicgeojson,
						LEAD(p.id) OVER othpics AS nextpic,
						ST_AsGeoJSON(LEAD(p.geom) OVER othpics)::json AS nextpicgeojson
					FROM pictures p
					JOIN sequences_pictures sp ON p.id = sp.pic_id
					WHERE
					"""
                + " AND ".join(sqlSubQueryWhere)
                + """
					WINDOW othpics AS (PARTITION BY sp.seq_id ORDER BY sp.rank)
				) spl ON p.id = spl.id
				WHERE
				"""
                + " AND ".join(sqlWhere)
                + """
				LIMIT %(limit)s
			"""
            )
            records = cursor.execute(query, sqlParams)

            items = [dbPictureToStacItem(str(dbPic["seq_id"]), dbPic) for dbPic in records]

            return (
                {
                    "type": "FeatureCollection",
                    "features": items,
                    "links": [
                        _get_root_link(),
                    ],
                },
                200,
                {"Content-Type": "application/geo+json"},
            )


@bp.route("/collections", methods=["POST"])
@auth.login_required_by_setting("API_FORCE_AUTH_ON_UPLOAD")
def postCollection(account=None):
    """Create a new sequence
    ---
    tags:
        - Upload
    requestBody:
        content:
            application/json:
                schema:
                    $ref: '#/components/schemas/GeoVisioPostCollection'
            application/x-www-form-urlencoded:
                schema:
                    $ref: '#/components/schemas/GeoVisioPostCollection'
            multipart/form-data:
                schema:
                    $ref: '#/components/schemas/GeoVisioPostCollection'
    security:
        - bearerToken: []
        - cookieAuth: []
    responses:
        200:
            description: the collection metadata
            content:
                application/json:
                    schema:
                        $ref: '#/components/schemas/GeoVisioCollection'
    """

    # Parse received parameters
    metadata = {}
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        metadata["title"] = request.json.get("title")
    elif content_type in ["multipart/form-data", "application/x-www-form-urlencoded"]:
        metadata["title"] = request.form.get("title")

    metadata = removeNoneInDict(metadata)

    # Create sequence folder
    accountId = accountIdOrDefault(account)
    seqId = runner_pictures.createSequence(metadata, accountId)

    # Return created sequence
    return (
        getCollection(seqId)[0],
        200,
        {
            "Content-Type": "application/json",
            "Access-Control-Expose-Headers": "Location",  # Needed for allowing web browsers access Location header
            "Location": url_for("stac.getCollection", _external=True, collectionId=seqId),
        },
    )


@bp.route("/collections/<uuid:collectionId>/items", methods=["POST"])
@auth.login_required_by_setting("API_FORCE_AUTH_ON_UPLOAD")
def postCollectionItem(collectionId, account=None):
    """Add a new picture in a given sequence
    ---
    tags:
        - Upload
    parameters:
        - name: collectionId
          in: path
          description: ID of sequence to add this picture into
          required: true
          schema:
            type: string
    requestBody:
        content:
            multipart/form-data:
                schema:
                    $ref: '#/components/schemas/GeoVisioPostItem'
    security:
        - bearerToken: []
        - cookieAuth: []
    responses:
        202:
            description: the added picture metadata
            content:
                application/geo+json:
                    schema:
                        $ref: '#/components/schemas/GeoVisioItem'
    """

    if not request.headers.get("Content-Type", "").startswith("multipart/form-data"):
        raise errors.InvalidAPIUsage("Content type should be multipart/form-data", status_code=415)

    # Check if position was given
    if request.form.get("position") is None:
        raise errors.InvalidAPIUsage('Missing "position" parameter', status_code=400)
    else:
        try:
            position = int(request.form.get("position"))
            if position <= 0:
                raise ValueError()
        except ValueError:
            raise errors.InvalidAPIUsage("Position in sequence should be a positive integer", status_code=400)

    # Check if picture blurring status is valid
    if request.form.get("isBlurred") is None or request.form.get("isBlurred") in ["true", "false"]:
        isBlurred = request.form.get("isBlurred") == "true"
    else:
        raise errors.InvalidAPIUsage("Picture blur status should be either unset, true or false", status_code=400)

    # Check if a picture file was given
    if "picture" not in request.files:
        raise errors.InvalidAPIUsage("No picture file was sent", status_code=400)
    else:
        picture = request.files["picture"]

        # Check file validity
        if not (picture.filename != "" and "." in picture.filename and picture.filename.rsplit(".", 1)[1].lower() in ["jpg", "jpeg"]):
            raise errors.InvalidAPIUsage("Picture file is either missing or in an unsupported format (should be jpg)", status_code=400)

    fses = current_app.config["FILESYSTEMS"]
    picInPermanentStorage = isBlurred or current_app.config["API_BLUR_URL"] is None

    with psycopg.connect(current_app.config["DB_URL"]) as conn:
        with conn.cursor() as cursor:
            # Check if sequence exists
            seq = cursor.execute("SELECT id FROM sequences WHERE id = %s", [collectionId]).fetchone()
            if not seq or len(seq) != 1:
                raise errors.InvalidAPIUsage(f"Sequence {collectionId} wasn't found in database", status_code=404)

            # Compute various metadata
            accountId = accountIdOrDefault(account)
            picture.read()
            filesize = picture.tell()  # get the position after read to get the file size in bytes

            additionalMetadata = {
                "blurredByAuthor": isBlurred,
                "originalFileName": os.path.basename(picture.filename),
                "originalFileSize": filesize,
            }

            # Insert picture into database
            try:
                picture.seek(0)  # Allows re-reading picture
                picId = runner_pictures.insertNewPictureInDatabase(
                    conn, collectionId, position, Image.open(picture), accountId, additionalMetadata
                )
            except runner_pictures.PicturePositionConflict:
                raise errors.InvalidAPIUsage("Picture at given position already exist", status_code=409)
            except runner_pictures.MetadataReadingError as e:
                raise errors.InvalidAPIUsage("Impossible to parse picture metadata", payload={"details": {"error": e.details}})

            # Save file into appropriate filesystem
            try:
                picture.seek(0)  # Allows re-reading picture
                picFs = fses.permanent if picInPermanentStorage else fses.tmp
                picFs.makedirs(dirname(pictures.getHDPicturePath(picId)), recreate=True)
                picFs.writefile(pictures.getHDPicturePath(picId), picture)
            except:
                logging.exception("Picture wasn't correctly saved in filesystem")
                raise errors.InvalidAPIUsage("Picture wasn't correctly saved in filesystem", status_code=500)

            conn.commit()

            runner_pictures.background_processor.process_pictures()

            # Return picture metadata
            return (
                getCollectionItem(collectionId, picId)[0],
                202,
                {
                    "Content-Type": "application/json",
                    "Access-Control-Expose-Headers": "Location",  # Needed for allowing web browsers access Location header
                    "Location": url_for("stac.getCollectionItem", _external=True, collectionId=collectionId, itemId=picId),
                },
            )


@bp.route("/collections/<uuid:collectionId>/items/<uuid:itemId>", methods=["PATCH"])
@auth.login_required()
def patchCollectionItem(collectionId, itemId, account):
    """Edits properties of an existing picture
    ---
    tags:
        - Editing
    parameters:
        - name: collectionId
          in: path
          description: ID of sequence the picture belongs to
          required: true
          schema:
            type: string
        - name: itemId
          in: path
          description: ID of picture to edit
          required: true
          schema:
            type: string
    requestBody:
        content:
            application/json:
                schema:
                    $ref: '#/components/schemas/GeoVisioPatchItem'
            application/x-www-form-urlencoded:
                schema:
                    $ref: '#/components/schemas/GeoVisioPatchItem'
            multipart/form-data:
                schema:
                    $ref: '#/components/schemas/GeoVisioPatchItem'
    security:
        - bearerToken: []
        - cookieAuth: []
    responses:
        200:
            description: the wanted item
            content:
                application/geo+json:
                    schema:
                        $ref: '#/components/schemas/GeoVisioItem'
    """

    # Parse received parameters
    metadata = {}
    content_type = (request.headers.get("Content-Type") or "").split(";")[0]
    if content_type == "application/json":
        metadata["visible"] = request.json.get("visible")
    elif content_type in ["multipart/form-data", "application/x-www-form-urlencoded"]:
        metadata["visible"] = request.form.get("visible")

    # Check if visibility param is valid
    if metadata.get("visible") is None:
        # /!\ As visible is the only editable thing for now, we can return if it's null
        # The line below may be removed when other parameters will be available for patching
        # Otherwise, you might want to do: visible = None
        return getCollectionItem(collectionId, itemId)

    elif metadata.get("visible") in ["true", "false"]:
        visible = metadata.get("visible") == "true"
    else:
        raise errors.InvalidAPIUsage("Picture visibility parameter (visible) should be either unset, true or false", status_code=400)

    # Check if picture exists and if given account is authorized to edit
    with psycopg.connect(current_app.config["DB_URL"]) as conn:
        with conn.cursor() as cursor:
            pic = cursor.execute("SELECT status, account_id FROM pictures WHERE id = %s", [itemId]).fetchone()

            # Picture not found
            if not pic:
                raise errors.InvalidAPIUsage(f"Picture {itemId} wasn't found in database", status_code=404)

            # Account associated to picture doesn't match current user
            if account is not None and account.id != str(pic[1]):
                raise errors.InvalidAPIUsage("You're not authorized to edit this picture", status_code=403)

            # Let's edit this picture
            oldStatus = pic[0]
            newStatus = None

            if visible is not None:
                if visible is True and oldStatus == "hidden":
                    newStatus = "ready"
                elif visible is False and oldStatus == "ready":
                    newStatus = "hidden"
                elif (visible is True and oldStatus == "ready") or (visible is False and oldStatus == "hidden"):
                    newStatus = oldStatus

                    # /!\ As visible is the only editable thing for now, we can return if it's unchanged
                    # The line below may be removed when other parameters will be available for patching
                    return getCollectionItem(collectionId, itemId)

                else:
                    # Picture is in a preparing/broken/... state so no edit possible
                    raise errors.InvalidAPIUsage(
                        f"Picture {itemId} is in {oldStatus} state, its visibility can't be changed for now", status_code=400
                    )

            if newStatus:
                cursor.execute("UPDATE pictures SET status = %s WHERE id = %s", [newStatus, itemId])
                conn.commit()

            # Redirect response to a classic GET
            return getCollectionItem(collectionId, itemId)


@bp.route("/collections/<uuid:collectionId>/items/<uuid:itemId>", methods=["DELETE"])
@auth.login_required()
def deleteCollectionItem(collectionId, itemId, account):
    """Delete an existing picture
    ---
    tags:
        - Editing
    parameters:
        - name: collectionId
          in: path
          description: ID of sequence the picture belongs to
          required: true
          schema:
            type: string
        - name: itemId
          in: path
          description: ID of picture to edit
          required: true
          schema:
            type: string
    security:
        - bearerToken: []
        - cookieAuth: []
    responses:
        204:
            description: The object has been correctly deleted
    """

    # Check if picture exists and if given account is authorized to edit
    with psycopg.connect(current_app.config["DB_URL"]) as conn:
        with conn.cursor() as cursor:
            pic = cursor.execute("SELECT status, account_id FROM pictures WHERE id = %s", [itemId]).fetchone()

            # Picture not found
            if not pic:
                raise errors.InvalidAPIUsage(f"Picture {itemId} wasn't found in database", status_code=404)

            # Account associated to picture doesn't match current user
            if account is not None and account.id != str(pic[1]):
                raise errors.InvalidAPIUsage("You're not authorized to edit this picture", status_code=403)

            cursor.execute("DELETE FROM pictures WHERE id = %s", [itemId])

            # delete images
            pictures.removeAllFiles(itemId)

            conn.commit()

            return "", 204


@bp.route("/collections/<uuid:collectionId>", methods=["PATCH"])
@auth.login_required()
def patchCollection(collectionId, account):
    """Edits properties of an existing collection
    ---
    tags:
        - Editing
    parameters:
        - name: collectionId
          in: path
          description: The sequence ID
          required: true
          schema:
            type: string
    requestBody:
        content:
            application/json:
                schema:
                    $ref: '#/components/schemas/GeoVisioPatchCollection'
            application/x-www-form-urlencoded:
                schema:
                    $ref: '#/components/schemas/GeoVisioPatchCollection'
            multipart/form-data:
                schema:
                    $ref: '#/components/schemas/GeoVisioPatchCollection'
    security:
        - bearerToken: []
        - cookieAuth: []
    responses:
        200:
            description: the wanted collection
            content:
                application/json:
                    schema:
                        $ref: '#/components/schemas/GeoVisioCollection'
    """

    # Parse received parameters
    metadata = {}
    content_type = (request.headers.get("Content-Type") or "").split(";")[0]
    if content_type == "application/json":
        metadata["visible"] = request.json.get("visible")
    elif content_type in ["multipart/form-data", "application/x-www-form-urlencoded"]:
        metadata["visible"] = request.form.get("visible")

    # Check if visibility param is valid
    visible = metadata.get("visible")
    if visible is not None:
        if visible in ["true", "false"]:
            visible = visible == "true"
        else:
            raise errors.InvalidAPIUsage("Picture visibility parameter (visible) should be either unset, true or false", status_code=400)

    if visible is None:
        # /!\ As visible is the only editable thing for now, we can return if it's null
        # The line below may be removed when other parameters will be available for patching
        return getCollection(collectionId)

    # Check if sequence exists and if given account is authorized to edit
    with psycopg.connect(current_app.config["DB_URL"]) as conn, conn.cursor() as cursor:
        seq = cursor.execute("SELECT status, account_id FROM sequences WHERE id = %s", [collectionId]).fetchone()

        # Sequence not found
        if not seq:
            raise errors.InvalidAPIUsage(f"Sequence {collectionId} wasn't found in database", status_code=404)

        # Account associated to sequence doesn't match current user
        if account is not None and account.id != str(seq[1]):
            raise errors.InvalidAPIUsage("You're not authorized to edit this sequence", status_code=403)

        # Let's edit this picture
        oldStatus = seq[0]

        if visible is not None:
            if oldStatus not in ["ready", "hidden"]:
                # Sequence is in a preparing/broken/... state so no edit possible
                raise errors.InvalidAPIUsage(
                    f"Sequence {collectionId} is in {oldStatus} state, its visibility can't be changed for now", status_code=400
                )

            newStatus = "ready" if visible is True else "hidden"

            if newStatus != oldStatus:
                cursor.execute("UPDATE sequences SET status = %s WHERE id = %s", [newStatus, collectionId])
                conn.commit()

        # Redirect response to a classic GET
        return getCollection(collectionId)


@bp.route("/collections/<uuid:collectionId>", methods=["DELETE"])
@auth.login_required()
def deleteCollection(collectionId, account):
    """Delete a collection and all the associated pictures
    The associated images will be hidden right away and deleted asynchronously
    ---
    tags:
        - Editing
    parameters:
        - name: collectionId
          in: path
          description: ID of the collection
          required: true
          schema:
            type: string
    security:
        - bearerToken: []
        - cookieAuth: []
    responses:
        204:
            description: The collection has been correctly deleted
    """

    # Check if collection exists and if given account is authorized to edit
    with psycopg.connect(current_app.config["DB_URL"]) as conn:
        with conn.cursor() as cursor:
            sequence = cursor.execute("SELECT status, account_id FROM sequences WHERE id = %s", [collectionId]).fetchone()

            # sequence not found
            if not sequence:
                raise errors.InvalidAPIUsage(f"Collection {collectionId} wasn't found in database", status_code=404)

            # Account associated to sequence doesn't match current user
            if account is not None and account.id != str(sequence[1]):
                raise errors.InvalidAPIUsage("You're not authorized to edit this sequence", status_code=403)

            logging.info(f"Asking for deletion of sequence {collectionId} and all its pictures")

            # mark all the pictures as waiting for deletion for async removal as this can be quite long if the storage is slow if there are lots of pictures
            nb_updated = cursor.execute(
                """
                WITH pic2rm AS (
                        SELECT pic_id FROM sequences_pictures WHERE seq_id = %(seq)s
                ),
                picWithoutOtherSeq AS (
                    SELECT pic_id FROM pic2rm
                    EXCEPT
                    SELECT pic_id FROM sequences_pictures WHERE pic_id IN (SELECT pic_id FROM pic2rm) AND seq_id != %(seq)s
                ),
                -- Add async task to delete all picture
                pic_insertion AS (
                    INSERT INTO pictures_to_process(picture_id, task)
                        SELECT pic_id, 'delete' FROM picWithoutOtherSeq
                    ON CONFLICT (picture_id) DO UPDATE SET task = 'delete'
                )
                UPDATE pictures SET status = 'waiting-for-delete' WHERE id IN (SELECT pic_id FROM picWithoutOtherSeq)
			""",
                {"seq": collectionId},
            ).rowcount

            cursor.execute("DELETE FROM sequences WHERE id = %s", [collectionId])
            conn.commit()

            # add background task if needed, to really delete pictures
            for _ in range(nb_updated):
                runner_pictures.background_processor.process_pictures()

            return "", 204


def accountIdOrDefault(account):
    # Get default account ID
    if account is not None:
        return account.id
    with psycopg.connect(current_app.config["DB_URL"]) as conn:
        accountId = conn.execute("SELECT id FROM accounts WHERE is_default").fetchone()
        if accountId is None:
            raise errors.InternalError("No default account defined, please contact your instance administrator")
        return str(accountId[0])


@bp.route("/collections/<uuid:collectionId>/geovisio_status")
def getCollectionImportStatus(collectionId):
    """Retrieve import status of all pictures in sequence
    ---
    tags:
        - Upload
    parameters:
        - name: collectionId
          in: path
          description: ID of collection to retrieve
          required: true
          schema:
            type: string
    responses:
        200:
            description: the pictures statuses
            content:
                application/json:
                    schema:
                        $ref: '#/components/schemas/GeoVisioCollectionImportStatus'
    """

    account = auth.get_current_account()
    params = {"seq_id": collectionId, "account": account.id if account is not None else None}
    with psycopg.connect(current_app.config["DB_URL"], row_factory=dict_row) as conn:
        with conn.cursor() as cursor:
            sequence_status = cursor.execute(
                """
			WITH items AS (
				SELECT p.id, p.status, sp.rank, sp.seq_id, p.process_error, p.nb_errors, p.processed_at
				FROM sequences_pictures sp
				JOIN pictures p on sp.pic_id = p.id
				JOIN sequences s on sp.seq_id = s.id
				WHERE
    				sp.seq_id = %(seq_id)s
        			AND (p.status != 'hidden' OR p.account_id = %(account)s)
        			AND (s.status != 'hidden' OR s.account_id = %(account)s)
				ORDER BY sp.rank
			)
			SELECT json_build_object(
					'status', s.status,
					'items', json_agg(
							json_build_object(
									'id', i.id,
									'status', i.status,
									'process_error', i.process_error,
									'nb_errors', i.nb_errors,
									'processed_at', i.processed_at,
									'rank', i.rank
							)
					)
			) AS sequence
			FROM items i
			JOIN sequences s on i.seq_id = s.id
			GROUP by s.id;
			""",
                params,
            ).fetchall()

            if len(sequence_status) == 0:
                raise errors.InvalidAPIUsage("Sequence is either empty or doesn't exists", status_code=404)

            return sequence_status[0]["sequence"]


def _getHDJpgPictureURL(picId: str, status: Optional[str]):
    external_url = pictures.getPublicHDPictureExternalUrl(picId, format="jpg")
    if external_url and status == "ready":  # we always serve non ready pictures through the API to be able to check permission:
        return external_url
    return url_for("pictures.getPictureHD", _external=True, pictureId=picId, format="jpg")


def _getSDJpgPictureURL(picId: str, status: Optional[str]):
    external_url = pictures.getPublicDerivatePictureExternalUrl(picId, format="jpg", derivateFileName="sd.jpg")
    if external_url and status == "ready":  # we always serve non ready pictures through the API to be able to check permission:
        return external_url
    return url_for("pictures.getPictureSD", _external=True, pictureId=picId, format="jpg")


def _getThumbJpgPictureURL(picId: str, status: Optional[str]):
    external_url = pictures.getPublicDerivatePictureExternalUrl(picId, format="jpg", derivateFileName="thumb.jpg")
    if external_url and status == "ready":  # we always serve non ready pictures through the API to be able to check permission
        return external_url
    return url_for("pictures.getPictureThumb", _external=True, pictureId=picId, format="jpg")


def _getTilesJpgPictureURL(picId: str, status: Optional[str]):
    external_url = pictures.getPublicDerivatePictureExternalUrl(picId, format="jpg", derivateFileName="tiles/{TileCol}_{TileRow}.jpg")
    if external_url and status == "ready":  # we always serve non ready pictures through the API to be able to check permission:
        return external_url
    return unquote(url_for("pictures.getPictureTile", _external=True, pictureId=picId, format="jpg", col="{TileCol}", row="{TileRow}"))
