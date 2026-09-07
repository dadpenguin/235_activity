from datetime import datetime

class Review:
    def __init__(self, review_id: int, user, track, rating: int, review_text: str, timestamp=None):
        if not isinstance(review_id, int) or isinstance(review_id, bool) or review_id <= 0:
            raise ValueError("review_id must be a positive integer.")

        self._review_id = review_id
        self._user = user
        self._track = track
        self.rating = rating
        self.review_text = review_text
        self._timestamp = timestamp if timestamp is not None else datetime.now()

    @property
    def id(self) -> int:
        return self._review_id

    @property
    def user(self):
        return self._user

    @property
    def track(self):
        return self._track

    @property
    def rating(self) -> int:
        return self._rating

    @rating.setter
    def rating(self, new_rating: int):
        # Exclude bool explicitly since isinstance(True, int) is True
        if not isinstance(new_rating, int) or isinstance(new_rating, bool):
            raise TypeError("Rating must be an integer.")
        if not (1 <= new_rating <= 5):
            raise ValueError("Rating must be between 1 and 5.")
        self._rating = new_rating

    @property
    def review_text(self) -> str:
        return self._review_text

    @review_text.setter
    def review_text(self, new_text: str):
        if not isinstance(new_text, str):
            raise TypeError("Review text must be a string.")

        # Strip zero-width/special unicode characters alongside default whitespace
        cleaned_text = new_text.strip(" \t\n\r\v\f\ufeff\u200b\u200c\u200d")

        if not cleaned_text:
            raise ValueError("Review text cannot be empty or whitespace only.")
        self._review_text = cleaned_text

    @property
    def timestamp(self):
        return self._timestamp

    def __repr__(self) -> str:
        return f"<Review user={self.user} rating={self.rating} id={self.id}>"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Review):
            return NotImplemented
        return self.id == other.id

    def __lt__(self, other) -> bool:
        if not isinstance(other, Review):
            return NotImplemented
        if self.timestamp != other.timestamp:
            return self.timestamp < other.timestamp
        return self.id < other.id

    def __hash__(self) -> int:
        return hash(self.id)
