"""GeoVisio API - Main"""
__version__ = "2.1.0"

import os
import configparser
import click
from flask import Flask, jsonify, stream_template, send_from_directory, redirect
from flask.cli import with_appcontext
from flask_cors import CORS
from flask_compress import Compress
from flasgger import Swagger
from . import (
    pictures,
    runner_pictures,
    errors,
    stac,
    map,
    db_migrations,
    auth,
    users,
    config_app,
    filesystems,
    configuration,
    tokens,
    docs,
    tasks,
)
import logging
from logging.config import dictConfig

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"simple": {"format": "%(asctime)s [%(threadName)s][%(levelname)s] %(name)s: %(message)s"}},
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "stream": "ext://sys.stdout",
        },
        "stderr": {
            "class": "logging.StreamHandler",
            "level": "ERROR",
            "formatter": "simple",
            "stream": "ext://sys.stderr",
        },
    },
    "loggers": {
        "PIL": {"handlers": ["stdout", "stderr"], "level": "WARN", "propagate": False},  # lower PIL loggers to only have warnings
    },
    "root": {"level": "INFO", "handlers": ["stderr", "stdout"]},
}
dictConfig(LOGGING_CONFIG)


def create_app(test_config=None, app=None):
    """API launcher method"""
    #
    # Create and setup Flask App
    #
    if app is None:
        app = Flask(__name__, instance_relative_config=True)
    CORS(app, supports_credentials=True)
    Compress(app)

    config_app.read_config(app, test_config)

    # Prepare filesystem
    createDirNoFailure(app.instance_path)
    app.config["FILESYSTEMS"] = filesystems.openFilesystemsFromConfig(app.config)

    # Check database connection and update its schema if needed
    db_migrations.update_db_schema(app.config["DB_URL"])

    if "OAUTH_PROVIDER" in app.config:
        auth.make_auth(app)
        app.register_blueprint(auth.bp)
    else:
        app.register_blueprint(auth.disabled_auth_bp())

    nb_proxies = app.config.get("INFRA_NB_PROXIES")
    if nb_proxies:
        nb_proxies = int(nb_proxies)
        # tell flask that it runs behind NB_PROXIES proxies so that it can trust the `X-Forwarded-` headers
        # https://flask.palletsprojects.com/en/2.2.x/deploying/proxy_fix/
        from werkzeug.middleware.proxy_fix import ProxyFix

        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=nb_proxies, x_proto=nb_proxies, x_host=nb_proxies, x_prefix=nb_proxies)

    runner_pictures.background_processor.init_app(app)

    #
    # List available routes/blueprints
    #

    app.register_blueprint(pictures.bp)
    app.register_blueprint(stac.bp)
    app.register_blueprint(map.bp)
    app.register_blueprint(users.bp)
    app.register_blueprint(configuration.bp)
    app.register_blueprint(tokens.bp)

    #
    # API documentation
    #

    # Read API metadata from setup.cfg
    setupCfg = configparser.RawConfigParser()
    setupCfg.read(os.path.join(os.path.dirname(__file__), "setup.cfg"))
    apiMeta = dict(setupCfg.items("metadata"))
    swagger = Swagger(app, config=docs.API_CONFIG, merge=True, template=docs.getApiDocs(apiMeta))

    #
    # Add generic routes
    #

    template_vars = {"API_VERSION_MAJOR_MINOR": ".".join(__version__.split(".")[0:2])}

    # Main page
    @app.route("/")
    def index():
        return stream_template(app.config["API_MAIN_PAGE"], **template_vars)

    # Viewer
    @app.route("/viewer")
    def viewer():
        return stream_template(app.config["API_VIEWER_PAGE"], **template_vars)

    @app.route("/apidocs")
    @app.route("/apidocs/")
    def apidocsRedirects():
        return redirect(docs.API_CONFIG["specs_route"], 301)

    @app.route("/apispec_1.json")
    def apispecRedirects():
        return redirect(docs.API_CONFIG["specs"][0]["route"], 301)

    @app.route("/static/img/<path:path>")
    def viewer_img(path):
        return send_from_directory(os.path.join(os.path.dirname(__file__), "../images"), path)

    # Errors
    @app.errorhandler(errors.InvalidAPIUsage)
    def invalid_api_usage(e):
        return jsonify(e.to_dict()), e.status_code

    @app.errorhandler(errors.InternalError)
    def internal_error(e):
        return jsonify(e.to_dict()), e.status_code

    #
    # Add CLI functions
    #

    @app.cli.command("process-sequences")
    @with_appcontext
    def process_sequences():
        """Deprecated entry point, use https://gitlab.com/geovisio/cli to upload a sequence instead"""
        logging.error("This function has been deprecated, use https://gitlab.com/geovisio/cli to upload a sequence instead.")
        logging.error(
            "To upload a sequence with this tool, install it with `pip install geovisio_cli`, then run:\ngeovisio upload --path <directory> --api-url <api-url>"
        )

    @app.cli.command("redo-sequences")
    @click.argument("sequences", nargs=-1)
    @with_appcontext
    def redo_sequences(sequences):
        """Re-processes already imported sequences.
        This updates database and derivates according to changes in original picture files.
        """
        logging.error("This function has been removed, if you need it back, feel free to open an issue")

    @app.cli.command("set-sequences-heading")
    @click.option("--value", show_default=True, default=0, help="Heading value relative to movement path (in degrees)")
    @click.option("--overwrite", is_flag=True, show_default=True, default=False, help="Overwrite existing heading values in database")
    @click.argument("sequencesIds", nargs=-1)
    @with_appcontext
    def set_sequences_heading(sequencesids, value, overwrite):
        """Changes pictures heading metadata.
        This uses the sequence movement path to compute new heading value.
        """
        runner_pictures.setSequencesHeadings(sequencesids, value, overwrite)

    @app.cli.group("sequences")
    def sequences():
        """Commands to handle operations on sequences"""
        pass

    @sequences.command("reorder")
    @click.argument("sequence_ids", nargs=-1)
    @with_appcontext
    def reorder(sequence_ids):
        """Reorders sequences by ascending timestamp.
        If no sequence ID is given, all sequences will be updated"""
        all = len(sequence_ids) == 0
        tasks.reorder_sequences.reorder_sequences(all, sequence_ids)

    @app.cli.command("cleanup")
    @click.option("--full", is_flag=True, show_default=True, default=False, help="For full cleanup (DB, cache, original pictures)")
    @click.option("--database", is_flag=True, show_default=True, default=False, help="Deletes database entries")
    @click.option("--cache", is_flag=True, show_default=True, default=False, help="Deletes cached derivates files (except blur masks)")
    @click.option("--permanent-pictures", is_flag=True, show_default=True, default=False, help="Deletes only original pictures")
    @click.argument("sequencesIds", nargs=-1)
    @with_appcontext
    def cleanup(sequencesids, full, database, cache, permanent_pictures):
        """Cleans up GeoVisio files and database."""
        if full is False and database is False and cache is False and permanent_pictures is False:
            full = True
        runner_pictures.cleanup(sequencesids, full, database, cache, permanent_pictures)

    @app.cli.group("db")
    def db():
        """Commands to handle database operations"""
        pass

    @db.command("upgrade")
    @with_appcontext
    def upgrade():
        """Update database schema"""
        db_migrations.update_db_schema(app.config["DB_URL"], force=True)

    @db.command("rollback")
    @click.option(
        "--all",
        is_flag=True,
        default=False,
        show_default=True,
        help="rollbacks all migrations instead, meaning everything created by Geovisio in database is deleted",
    )
    @with_appcontext
    def rollback(all):
        """Rollbacks the latest database migration"""
        db_migrations.rollback_db_schema(app.config["DB_URL"], all)

    @app.cli.command("picture-worker")
    @with_appcontext
    def run_picture_worker():
        """Run a worker to process pictures after upload. Each worker use one thread, and several workers can be run in parallel"""
        logging.info("Running picture worker")
        worker = runner_pictures.PictureProcessor(config=app.config, stop=False)
        worker.process_next_pictures()

    @app.cli.group("default-account-token")
    def tokens_group():
        """Commands to handle authorization tokens operations"""
        pass

    @tokens_group.command("get")
    @with_appcontext
    def get_default():
        """
        Get JWT default account token

        Note: Be sure to not share this JWT token!
        """
        try:
            print(tokens.get_default_account_jwt_token())
        except errors.InternalError as e:
            print(f"Impossible to get default account's JWT token: {e.message}")

    return app


def createDirNoFailure(directory):
    """Creates a directory on disk if not already existing

    Parameters
    ----------
    directory : str
            Path of the directory to create
    """

    try:
        os.makedirs(directory)
    except OSError:
        pass
