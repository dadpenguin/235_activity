"""Initialize Flask app."""

from pathlib import Path

from flask import Flask

import music.adapters.repository as repo
from music.adapters.memory_repository import MemoryRepository, populate



def create_app(test_config=None):
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)

    # Create default root: music/adapters/data
    data_path = Path('music') / 'adapters' / 'data'

    if test_config is None:
        # Configure the app from configuration-file settings.
        app.config.from_object('config.Config')
    else:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    # Create and expose the repository used by services and blueprints.
    repository = MemoryRepository()
    repo.repo_instance = repository
    app.extensions['repository'] = repository

    # fill the content of the repository from the provided csv files
    populate(data_path, repository)

    return app
