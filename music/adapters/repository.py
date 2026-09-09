from abc import ABC, abstractmethod

from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.favourite import Favourite
from music.domainmodel.genre import Genre
from music.domainmodel.review import Review
from music.domainmodel.track import Track
from music.domainmodel.user import User


class AbstractRepository(ABC):
    """Repository contract used by the application's service layer."""

    @abstractmethod
    def add_track(self, track: Track) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_track(self, track_id: int) -> Track | None:
        raise NotImplementedError

    @abstractmethod
    def get_tracks(self) -> list[Track]:
        raise NotImplementedError

    @abstractmethod
    def get_number_of_tracks(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_tracks_by_title(self, title: str) -> list[Track]:
        raise NotImplementedError

    @abstractmethod
    def get_albums_by_name(self, album_name: str) -> list[Album]:
        raise NotImplementedError

    @abstractmethod
    def get_artists_by_name(self, artist_name: str) -> list[Artist]:
        raise NotImplementedError


    @abstractmethod
    def get_genres_by_name(self, genre_name: str) -> list[Genre]:
        raise NotImplementedError

    @abstractmethod
    def get_tracks_by_artist(self, artist_name: str) -> list[Track]:
        raise NotImplementedError

    @abstractmethod
    def get_tracks_by_genre(self, genre_name: str) -> list[Track]:
        raise NotImplementedError

    @abstractmethod
    def add_user(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_user(self, user_name: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    def add_review(self, review: Review) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_reviews_by_track(self, track_id: int) -> list[Review]:
        raise NotImplementedError

    @abstractmethod
    def add_favourite(self, favourite: Favourite) -> None:
        raise NotImplementedError

    @abstractmethod
    def remove_favourite(self, favourite: Favourite) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_favourites_by_user(self, user_name: str) -> list[Favourite]:
        raise NotImplementedError

    @abstractmethod
    def get_favourite(self, user_name: str, track_id: int) -> Favourite | None:
        raise NotImplementedError

repo_instance: AbstractRepository
