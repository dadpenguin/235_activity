from datetime import datetime

from music.adapters.repository import AbstractRepository
from music.domainmodel.review import Review
from music.track.exceptions import TrackNotFound
from music.track.services import TrackService
from utils.user import generate_random_review_id


class ReviewService:
    @classmethod
    def create_review(cls, repo: AbstractRepository, user_name: str, track_id: int, stars: int, paragraph: str):

        track = TrackService.get_track_by_track_id(track_id, repo)

        if track is None:
            raise TrackNotFound("Track is not found")

        review_id = generate_random_review_id()
        now = datetime.now()

        new_review = Review(review_id=review_id, user=user_name, track=track, rating=stars, review_text=paragraph,timestamp = now)

        repo.add_review(new_review)

        return new_review
