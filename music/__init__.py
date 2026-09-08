"""Initialize Flask app."""

from pathlib import Path

from flask import Flask, render_template, redirect, url_for, request

import music.adapters.repository as repo

from music.adapters.memory_repository import MemoryRepository, populate


def register_blueprints(app: Flask):
    with app.app_context():

        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)


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

    # Create the Flask app object.
    app = Flask(__name__)

    data_path = init_config(app, test_config)

    repository = MemoryRepository()
    repo.repo_instance = repository

    app.extensions['repository'] = repository

    # populate(data_path, repository)

    register_blueprints(app)



    # temporary homepage
    @app.route('/')
    def homepage():
        return "homepage"

    return app