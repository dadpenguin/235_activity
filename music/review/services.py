from datetime import datetime

from music.adapters.repository import AbstractRepository
from music.domainmodel.review import Review
from music.track.services import TrackService
from utils.user import generate_random_review_id


class ReviewService:
    @classmethod
    def create_review(cls, repo: AbstractRepository, user_name: str, track_id: int, stars: int, paragraph: str):

        track = TrackService.get_track_by_track_id(track_id, repo)
        review_id = generate_random_review_id()
        now = datetime.now()

        new_review = Review(review_id=review_id, user=user_name, track=track, rating=stars, review_text=paragraph,timestamp = now)

        repo.add_review(new_review)

        return True



        # reviews = []

        # for track in repo.repo_instance.get_tracks():
        #     for review in repo.repo_instance.get_reviews_by_track(track.track_id):
        #         reviews.append(review)

        # review_id = len(reviews) + 1

        # new_review = Review(review_id=review_id, user=AuthService.get_authenticated_user_name(), track=repo.repo_instance.get_track(track_id), rating=stars, review_text=paragraph,timestamp = datetime.now())
        # repo.repo_instance.add_review(new_review)
