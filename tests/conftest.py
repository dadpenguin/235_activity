
import pytest
import sys

from music import create_app
from music.adapters import memory_repository
from music.adapters.memory_repository import MemoryRepository

from utils import get_project_root





# the csv files in the test folder are different from the csv files in the music/adapters/data folder!
# tests are written against the csv files in tests, this data path is used to override default path for testing
TEST_DATA_PATH = get_project_root() / "tests" / "data"


@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    memory_repository.populate(TEST_DATA_PATH, repo)
    return repo


@pytest.fixture
def client():
    my_app = create_app({
        'TESTING': True,
        'TEST_DATA_PATH': TEST_DATA_PATH,
        'WTF_CSRF_ENABLED': False,
        'SECRET_KEY': 'test-secret-key'
    })

    return my_app.test_client()

class AuthenticationManager:
    def __init__(self, client):
        self.__client = client

    def login(self, user_name='thorke', password='cLQ^C#oFXloS'):
        return self.__client.post(
            '/authentication/login',
            data={
                'user_name': user_name,
                'password': password
            }
        )

    def logout(self):
        return self.__client.get('/authentication/logout')


@pytest.fixture
def auth(client):
    return AuthenticationManager(client)
  
# @pytest.fixture()
# def app():
#     app = create_app()
#     app.config.update(
#         TESTING=True,
#         SECRET_KEY="test-secret-key",
#         WTF_CSRF_ENABLED=False,
#     )
#     with app.app_context():
#         yield app


# @pytest.fixture()
# def client(app):
#     return app.test_client()
# >>>>>>> main





