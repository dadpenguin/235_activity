from werkzeug.security import check_password_hash, generate_password_hash

from music.adapters.repository import AbstractRepository
from music.domainmodel.user import User
from utils.user import generate_random_user_id


class NameNotUniqueException(Exception):
    pass

class UnknownUserException(Exception):
    pass

class AuthenticationException(Exception):
    pass


class AuthService:
    @classmethod
    def add_user(cls, user_name: str, password: str, repo: AbstractRepository):
        user = repo.get_user(user_name)
        if user is not None:
            raise NameNotUniqueException

        password_hash = generate_password_hash(password)

        user = User(generate_random_user_id(),user_name, password_hash)
        repo.add_user(user)


    @classmethod
    def authenticate_user(cls, user_name: str, password: str, repo: AbstractRepository):
        authenticated = False

        user = repo.get_user(user_name)
        if user is not None:
            authenticated = check_password_hash(user.password, password)
        if not authenticated:
            raise AuthenticationException

        return authenticated

    @classmethod
    def __user_to_dict(cls, user: User):
        user_dict = {
            'user_name': user.user_name,
            'password': user.password
        }
        return user_dict

    @classmethod
    def get_user(cls, user_name: str, repo: AbstractRepository):
        user = repo.get_user(user_name)
        if user is None:
            raise UnknownUserException

        return cls.__user_to_dict(user)
