from music.adapters.repository import AbstractRepository
from music.authentication.services import AuthService
from music.domainmodel.favourite import Favourite
from music.track.services import TrackService


class FavouriteService:


    @classmethod
    def get_user(cls, user_name: str, repo: AbstractRepository):
        return repo.get_user(user_name)

    @classmethod
    def register_favourite(cls, user_name: str, track_id: int, repo: AbstractRepository):

        new_track = TrackService.get_track(track_id, repo)

        user = cls.get_user(user_name, repo)

        if user is None:
            return False

        favourite = Favourite(favourite_id=track_id, user=user, track=new_track)
        repo.add_favourite(favourite)

        print("added to favourites")
        return True

    @classmethod
    def remove_favourite(cls, user_name: str, track_id: int, repo: AbstractRepository):

        if user_name is None:
            return False

        for favourite in repo.get_favourites_by_user(user_name):
            if favourite.track.track_id == track_id:
                repo.remove_favourite(favourite)
                print("removed from favourites")
                return True
        return False
