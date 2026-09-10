import pytest
from flask import session

from music import create_app
import music.adapters.repository as repo_module
from music.adapters.memory_repository import MemoryRepository
from music.authentication.services import (
    AuthenticationException,
    AuthService,
    NameNotUniqueException,
    UnknownUserException,
)


class TestAuthService:

    @pytest.fixture
    def app(self):
        app = create_app()
        return app

    @pytest.fixture
    def repo(self):
        repo_module.repo_instance = MemoryRepository()
        return repo_module.repo_instance

    def test_get_authenticated_user_name_with_session(self, app):
        with app.test_request_context():
            session['user_name'] = "alice"
            assert AuthService.get_authenticated_user_name() == "alice"

    def test_get_authenticated_user_name_empty_session(self, app):
        with app.test_request_context():
            assert AuthService.get_authenticated_user_name() is None

    def test_add_user_success(self, repo):
        AuthService.add_user("alice", "password123", repo)

        user = repo.get_user("alice")
        assert user is not None
        assert user.user_name == "alice"
        assert user.password != "password123"

    def test_add_user_duplicate_raises_exception(self, repo):
        AuthService.add_user("alice", "password123", repo)

        with pytest.raises(NameNotUniqueException):
            AuthService.add_user("alice", "different_pass", repo)

    def test_authenticate_user_success(self, repo):
        AuthService.add_user("alice", "password123", repo)

        is_authenticated = AuthService.authenticate_user("alice", "password123", repo)
        assert is_authenticated is True

    def test_authenticate_user_wrong_password_raises_exception(self, repo):
        AuthService.add_user("alice", "password123", repo)

        with pytest.raises(AuthenticationException):
            AuthService.authenticate_user("alice", "wrongpassword", repo)

    def test_authenticate_nonexistent_user_raises_exception(self, repo):
        with pytest.raises(AuthenticationException):
            AuthService.authenticate_user("ghost", "password123", repo)

    def test_get_user_success(self, repo):
        AuthService.add_user("alice", "password123", repo)

        user_dict = AuthService.get_user("alice", repo)
        assert user_dict['user_name'] == "alice"
        assert 'password' in user_dict

    def test_get_unknown_user_raises_exception(self, repo):
        with pytest.raises(UnknownUserException):
            AuthService.get_user("ghost", repo)
