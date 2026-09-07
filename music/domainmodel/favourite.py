class Favourite:

    def __init__(self, favourite_id: int, user, track):
        if not isinstance(favourite_id, int) or favourite_id <= 0:
            raise ValueError("favourite_id must be a positive integer.")

        self._favourite_id = favourite_id
        self._user = user
        self._track = track

    @property
    def favourite_id(self) -> int:
        return self._favourite_id

    @property
    def id(self) -> int:

        return self._favourite_id

    @property
    def user(self):
        return self._user

    @property
    def track(self):
        return self._track

    def __repr__(self) -> str:
        return f"<Favourite - {self.track} ,user = {self.user} ,favourite_id = {self.favourite_id}>"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Favourite):
            return NotImplemented
        return self.favourite_id == other.favourite_id

    def __lt__(self, other) -> bool:
        if not isinstance(other, Favourite):
            return NotImplemented
        return self.favourite_id < other.favourite_id

    def __hash__(self) -> int:
        return hash(self.favourite_id)
