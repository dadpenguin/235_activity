from pathlib import Path

from music.adapters.repository import AbstractRepository
from music.adapters.csvdatareader import CSVDataReader
from music.domainmodel.favourite import Favourite
from music.domainmodel.review import Review
from music.domainmodel.track import Track
from music.domainmodel.user import User


class MemoryRepository(AbstractRepository):
    """Store the application's domain objects in memory."""

    def __init__(self):
        self.__tracks: list[Track] = []
        self.__users: list[User] = []
        self.__reviews: list[Review] = []
        self.__favourites: list[Favourite] = []

    def add_track(self, track: Track) -> None:
        if track not in self.__tracks:
            self.__tracks.append(track)

    def get_track(self, track_id: int) -> Track | None:
        return next(
            (track for track in self.__tracks if track.track_id == track_id),
            None,
        )

    def get_tracks(self) -> list[Track]:
        return list(self.__tracks)

    def get_number_of_tracks(self) -> int:
        return len(self.__tracks)

    def get_tracks_by_title(self, title: str) -> list[Track]:
        search_term = title.strip().lower()
        return [
            track
            for track in self.__tracks
            if search_term in track.title.lower()
        ]

    def get_tracks_by_artist(self, artist_name: str) -> list[Track]:
        search_term = artist_name.strip().lower()
        return [
            track
            for track in self.__tracks
            if track.artist is not None
            and search_term in track.artist.full_name.lower()
        ]

    def get_tracks_by_genre(self, genre_name: str) -> list[Track]:
        search_term = genre_name.strip().lower()
        return [
            track
            for track in self.__tracks
            if any(search_term in genre.name.lower() for genre in track.genres)
        ]

    def add_user(self, user: User) -> None:
        if self.get_user(user.user_name) is None:
            self.__users.append(user)

    def get_user(self, user_name: str) -> User | None:
        normalized_name = user_name.strip().lower()
        return next(
            (
                user
                for user in self.__users
                if user.user_name == normalized_name
            ),
            None,
        )

    def add_review(self, review: Review) -> None:
        if review not in self.__reviews:
            self.__reviews.append(review)

    def get_reviews_by_track(self, track_id: int) -> list[Review]:
        return [
            review
            for review in self.__reviews
            if review.track.track_id == track_id
        ]

    def add_favourite(self, favourite: Favourite) -> None:
        existing = self.get_favourite(
            favourite.user.user_name,
            favourite.track.track_id,
        )
        if existing is None:
            self.__favourites.append(favourite)

    def remove_favourite(self, favourite: Favourite) -> None:
        if favourite in self.__favourites:
            self.__favourites.remove(favourite)

    def get_favourites_by_user(self, user_name: str) -> list[Favourite]:
        normalized_name = user_name.strip().lower()
        return [
            favourite
            for favourite in self.__favourites
            if favourite.user.user_name == normalized_name
        ]

    def get_favourite(
        self, user_name: str, track_id: int
    ) -> Favourite | None:
        normalized_name = user_name.strip().lower()
        return next(
            (
                favourite
                for favourite in self.__favourites
                if favourite.user.user_name == normalized_name
                and favourite.track.track_id == track_id
            ),
            None,
        )


def populate(data_path, repo: AbstractRepository) -> None:
    """Load tracks from the CSV files located in ``data_path``."""

    data_path = Path(data_path)
    albums_file = _find_data_file(
        data_path, "raw_albums_test.csv", "raw_albums_excerpt.csv"
    )
    tracks_file = _find_data_file(
        data_path, "raw_tracks_test.csv", "raw_tracks_excerpt.csv"
    )

    reader = CSVDataReader(albums_file, tracks_file)
    reader.read_csv_files()

    for track in reader.dataset_of_tracks:
        repo.add_track(track)


def _find_data_file(data_path: Path, *file_names: str) -> Path:
    for file_name in file_names:
        candidate = data_path / file_name
        if candidate.is_file():
            return candidate
    raise FileNotFoundError(
        f"None of {file_names!r} exists in data directory {data_path}"
    )
