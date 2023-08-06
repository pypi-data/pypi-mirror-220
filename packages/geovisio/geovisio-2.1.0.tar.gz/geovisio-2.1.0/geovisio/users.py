import flask
from . import auth

bp = flask.Blueprint("user", __name__, url_prefix="/api/users")


@bp.route("/me")
@auth.login_required_with_redirect()
def getUserInfo(account):
    """Get current logged user informations
    ---
    tags:
        - Users
    responses:
        200:
            description: Information about the logged account
            content:
                application/json:
                    schema:
                        $ref: '#/components/schemas/GeoVisioUser'
    """
    response = {
        "id": account.id,
        "name": account.name,
        "links": [{"rel": "catalog", "type": "application/json", "href": flask.url_for("user.getCatalog", _external=True)}],
    }
    return flask.jsonify(response)


@bp.route("/me/catalog/")
@auth.login_required_with_redirect()
def getCatalog(account):
    """Get current logged user catalog
    ---
    tags:
        - Users
        - Sequences
    responses:
        200:
            description: the Catalog listing all sequences associated to given user
            content:
                application/json:
                    schema:
                        $ref: '#/components/schemas/GeoVisioCatalog'
    """
    return flask.redirect(flask.url_for("stac.getUserCatalog", userId=account.id, _external=True))
