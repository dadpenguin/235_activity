
"""""
ID
album title,
release year,
total tracks,
other album-related details.
"""
class Album:
    def __init__(self, album_id: int, title: str, release_year: int = None, total_tracks: int = None):
        self._album_id = album_id
        self._title = title
        self._release_year = release_year
        self._total_tracks = total_tracks

    @property
    def id(self) -> int:
        return self._album_id

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, new_title: str):
        if not new_title or not isinstance(new_title, str):
            raise ValueError("Title must be a non-empty string.")
        self._title = new_title

    @property
    def release_year(self) -> int:
        return self._release_year

    @release_year.setter
    def release_year(self, new_release_year: int):
        if new_release_year is not None and new_release_year < 0:
            raise ValueError("Release year must be a positive integer.")
        self._release_year = new_release_year

    @property
    def total_tracks(self) -> int:
        return self._total_tracks

    @total_tracks.setter
    def total_tracks(self, new_total_tracks: int):
        if new_total_tracks is not None and new_total_tracks < 0:
            raise ValueError("Total tracks must be a non-negative integer.")
        self._total_tracks = new_total_tracks

    def __repr__(self) -> str:
        return f"<Album {self.title}, album id = {self.id}>"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Album):
            return False
        return self.id == other.id

    def __lt__(self, other) -> bool:
        if not isinstance(other, Album):
            return NotImplemented
        return self.id < other.id

    def __hash__(self) -> int:
        return hash(self.id)
