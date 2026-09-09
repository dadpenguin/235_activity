"""Initialize Flask app."""

from pathlib import Path

from flask import Flask, render_template, redirect, url_for, request

import music.adapters.repository as repo

from music.adapters.memory_repository import MemoryRepository, populate

from flask import Flask, render_template, redirect, url_for, request
from music.domainmodel.favourite import Favourite
from music.domainmodel.user import User
from search.search import search_blueprint


def register_blueprints(app: Flask):
    with app.app_context():

        # Authentication blueprint
        from .authentication import authentication
        app.register_blueprint(
            authentication.authentication_blueprint
        )

        # Browse blueprint
        from .browse import browse_blueprint
        app.register_blueprint(
            browse_blueprint
        )

        from favourite import favourite
        app.register_blueprint(favourite.favourite_blueprint)

        from search import search
        app.register_blueprint(search.search_blueprint)

        from track_detail import track_detail
        app.register_blueprint(track_detail.track_detail_blueprint)


def init_config(app: Flask, test_config):

    # Create default root: music/adapters/data
    data_path = Path('music') / 'adapters' / 'data'

    if test_config is None:
        app.config.from_object('config.Config')
    else:
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    return data_path


def create_app(test_config=None):
    """Construct the core application."""

    # Create the Flask app object
    app = Flask(__name__)

    data_path = init_config(app, test_config)

    # Create repository
    repository = MemoryRepository()

    repo.repo_instance = repository #Also don't change this

    populate("music/adapters/data", repository) #Remove this and all my html pages will break

    app.extensions['repository'] = repository

    # Load data into repository
    populate(data_path, repository)

    # Register blueprints
    register_blueprints(app)

    return app

