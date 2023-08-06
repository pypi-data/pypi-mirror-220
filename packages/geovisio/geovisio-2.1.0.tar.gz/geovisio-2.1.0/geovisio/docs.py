from . import stac

API_CONFIG = {
    "openapi": "3.0.2",
    "paths": {
        "/api/docs/specs.json": {
            "get": {
                "summary": "The OpenAPI 3 specification for this API",
                "tags": ["Metadata"],
                "responses": {
                    "200": {
                        "description": "JSON file documenting API routes",
                        "content": {"application/json": {"schema": {"$ref": "https://spec.openapis.org/oas/3.0/schema/2021-09-28"}}},
                    }
                },
            }
        },
        "/api/docs/swagger": {
            "get": {
                "summary": "The human-readable API documentation",
                "tags": ["Metadata"],
                "responses": {"200": {"description": "API Swagger", "content": {"text/html": {}}}},
            }
        },
    },
    "components": {
        "securitySchemes": {
            "bearerToken": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"},
            "cookieAuth": {"type": "apiKey", "in": "cookie", "name": "session"},
        },
        "schemas": {
            "STACLanding": {"$ref": f"https://api.stacspec.org/v{stac.STAC_VERSION}/core/openapi.yaml#/components/schemas/landingPage"},
            "STACConformance": {"$ref": "http://schemas.opengis.net/ogcapi/features/part1/1.0/openapi/schemas/confClasses.yaml"},
            "STACCatalog": {"$ref": f"https://api.stacspec.org/v{stac.STAC_VERSION}/core/openapi.yaml#/components/schemas/catalog"},
            "STACCollections": {
                "$ref": f"https://api.stacspec.org/v{stac.STAC_VERSION}/collections/openapi.yaml#/components/schemas/collections"
            },
            "STACCollection": {
                "$ref": f"https://api.stacspec.org/v{stac.STAC_VERSION}/collections/openapi.yaml#/components/schemas/collection"
            },
            "STACCollectionItems": {
                "$ref": f"https://api.stacspec.org/v{stac.STAC_VERSION}/ogcapi-features/openapi.yaml#/components/schemas/featureCollectionGeoJSON"
            },
            "STACItem": {"$ref": f"https://api.stacspec.org/v{stac.STAC_VERSION}/ogcapi-features/openapi.yaml#/components/schemas/item"},
            "STACExtent": {"$ref": f"https://api.stacspec.org/v{stac.STAC_VERSION}/collections/openapi.yaml#/components/schemas/extent"},
            "STACExtentTemporal": {
                "type": "object",
                "properties": {
                    "temporal": {
                        "$ref": f"https://api.stacspec.org/v{stac.STAC_VERSION}/collections/openapi.yaml#/components/schemas/extent/properties/temporal"
                    },
                },
            },
            "STACStatsForItems": {"$ref": "https://stac-extensions.github.io/stats/v0.2.0/schema.json#/definitions/stats_for_items"},
            "STACLinks": {
                "type": "object",
                "properties": {
                    "links": {"$ref": f"https://api.stacspec.org/v{stac.STAC_VERSION}/collections/openapi.yaml#/components/schemas/links"}
                },
            },
            "GeoVisioLanding": {
                "allOf": [
                    {"$ref": "#/components/schemas/STACLanding"},
                    {"type": "object", "properties": {"extent": {"$ref": "#/components/schemas/STACExtent"}}},
                ]
            },
            "GeoVisioCatalog": {
                "allOf": [
                    {"$ref": "#/components/schemas/STACCatalog"},
                    {
                        "type": "object",
                        "properties": {
                            "links": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "required": ["href", "rel"],
                                    "properties": {
                                        "stats:items": {"$ref": "#/components/schemas/STACStatsForItems"},
                                        "extent": {"$ref": "#/components/schemas/STACExtentTemporal"},
                                        "geovisio:status": {"$ref": "#/components/schemas/GeoVisioCollectionStatus"},
                                    },
                                },
                            }
                        },
                    },
                ]
            },
            "GeoVisioCollections": {
                "allOf": [
                    {"$ref": "#/components/schemas/STACCollections"},
                    {"$ref": "#/components/schemas/STACLinks"},
                    {
                        "type": "object",
                        "properties": {"collections": {"type": "array", "items": {"$ref": "#/components/schemas/GeoVisioCollection"}}},
                    },
                ]
            },
            "GeoVisioCollection": {
                "allOf": [
                    {"$ref": "#/components/schemas/STACCollectionItems"},
                    {"type": "object", "properties": {"stats:items": {"$ref": "#/components/schemas/STACStatsForItems"}}},
                ]
            },
            "GeoVisioCollectionImportStatus": {
                "type": "object",
                "properties": {
                    "status": {"$ref": "#/components/schemas/GeoVisioCollectionStatus"},
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "string"},
                                "status": {"$ref": "#/components/schemas/GeoVisioItemStatus"},
                                "rank": {"type": "integer"},
                            },
                        },
                    },
                },
            },
            "GeoVisioPostCollection": {
                "type": "object",
                "properties": {"title": {"type": "string", "description": "The sequence title"}},
            },
            "GeoVisioPatchCollection": {
                "type": "object",
                "properties": {
                    "visible": {
                        "type": "string",
                        "description": "Should the sequence be publicly visible ?",
                        "enum": ["true", "false", "null"],
                        "default": "null",
                    }
                },
            },
            "GeoVisioCollectionItems": {
                "allOf": [
                    {"$ref": "#/components/schemas/STACCollectionItems"},
                    {"$ref": "#/components/schemas/STACLinks"},
                    {
                        "type": "object",
                        "properties": {"features": {"type": "array", "items": {"$ref": "#/components/schemas/GeoVisioItem"}}},
                    },
                ]
            },
            "GeoVisioItem": {
                "allOf": [
                    {"$ref": "#/components/schemas/STACItem"},
                    {
                        "type": "object",
                        "properties": {
                            "properties": {
                                "type": "object",
                                "properties": {"geovisio:status": {"$ref": "#/components/schemas/GeoVisioItemStatus"}},
                            }
                        },
                    },
                ],
            },
            "GeoVisioPostItem": {
                "type": "object",
                "properties": {
                    "position": {"type": "integer", "description": "Position of picture in sequence (starting from 1)"},
                    "picture": {
                        "type": "string",
                        "format": "binary",
                        "description": "Picture to upload",
                    },
                    "isBlurred": {
                        "type": "string",
                        "description": "Is picture blurred",
                        "enum": ["true", "false", "null"],
                        "default": "false",
                    },
                },
            },
            "GeoVisioPatchItem": {
                "type": "object",
                "properties": {
                    "visible": {
                        "type": "string",
                        "description": "Should the picture be publicly visible ?",
                        "enum": ["true", "false", "null"],
                        "default": "null",
                    }
                },
            },
            "GeoVisioCollectionStatus": {"type": "string", "enum": ["ready", "broken", "preparing", "waiting-for-process"]},
            "GeoVisioItemStatus": {
                "type": "string",
                "enum": ["ready", "broken", "preparing", "waiting-for-process", "preparing-derivates", "preparing-blur"],
            },
            "GeoVisioUser": {
                "type": "object",
                "properties": {
                    "id": {"type": "string", "format": "uuid"},
                    "name": {"type": "string"},
                    "links": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {"href": {"type": "string"}, "ref": {"type": "string"}, "type": {"type": "string"}},
                        },
                    },
                },
            },
            "GeoVisioUserAuth": {
                "type": "object",
                "properties": {
                    "id": {"type": "string", "format": "uuid"},
                    "name": {"type": "string"},
                    "oauth_provider": {"type": "string"},
                    "oauth_id": {"type": "string"},
                },
            },
            "GeoVisioConfiguration": {
                "type": "object",
                "properties": {
                    "auth": {
                        "type": "object",
                        "properties": {
                            "user_profile": {"type": "object", "properties": {"url": {"type": "string"}}},
                            "enabled": {"type": "boolean"},
                        },
                        "required": ["enabled"],
                    },
                    "license": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string", "description": "SPDX id of the license"},
                            "url": {"type": "string"},
                        },
                        "required": ["id"],
                    },
                },
                "required": ["auth"],
            },
            "GeoVisioTokens": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "description": {"type": "string"},
                        "generated_at": {"type": "string"},
                        "links": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {"href": {"type": "string"}, "ref": {"type": "string"}, "type": {"type": "string"}},
                            },
                        },
                    },
                },
            },
            "JWToken": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "description": {"type": "string"},
                    "generated_at": {"type": "string"},
                    "jwt_token": {
                        "type": "string",
                        "description": "this jwt_token will be needed to authenticate future queries as Bearer token",
                    },
                },
            },
            "JWTokenClaimable": {
                "allOf": [
                    {"$ref": "#/components/schemas/JWToken"},
                    {
                        "type": "object",
                        "properties": {
                            "links": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "href": {"type": "string"},
                                        "ref": {"type": "string"},
                                        "type": {"type": "string"},
                                    },
                                },
                            }
                        },
                    },
                ]
            },
        },
    },
    "specs": [
        {
            "endpoint": "swagger",
            "route": "/api/docs/specs.json",
        }
    ],
    "swagger_ui": True,
    "specs_route": "/api/docs/swagger",
}


def getApiDocs(apiMeta: object):
    """Returns API documentation object for Swagger"""

    return {
        "info": {
            "title": apiMeta["name"],
            "version": apiMeta["version"],
            "description": apiMeta["description"],
            "contact": {"name": apiMeta["maintainer"], "url": apiMeta["url"], "email": apiMeta["maintainer_email"]},
        },
        "tags": [
            {"name": "Metadata", "description": "API metadata"},
            {"name": "Sequences", "description": "Collections of pictures"},
            {"name": "Pictures", "description": "Geolocated images"},
            {"name": "Map", "description": "Tiles for web map display"},
            {"name": "Upload", "description": "Sending pictures & sequences"},
            {"name": "Editing", "description": "Modifying pictures & sequences"},
            {"name": "Users", "description": "Account management"},
            {"name": "Auth", "description": "User authentication"},
        ],
    }
