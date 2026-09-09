from music.adapters.repository import AbstractRepository
from music.domainmodel.review import Review

class TrackService:
    @classmethod
    def get_track(cls, track_id, repo: AbstractRepository):
        return repo.get_track(track_id)

    @classmethod
    def is_user_favourite(cls,user_name: str, repo: AbstractRepository, track_id: int):

        if user_name is None or user_name == "":
            return False

        for favourite in repo.get_favourites_by_user(user_name):
            if favourite.track.track_id == track_id:
                return True

        return False


    @classmethod
    def get_track_by_track_id(cls, track_id, repo: AbstractRepository):
        return repo.get_track(track_id)




    @classmethod
    def get_reviews_by_track_id(cls, track_id, repo: AbstractRepository):
        reviews = repo.get_reviews_by_track(track_id)
        reviews.sort(key=lambda review: review.timestamp, reverse=True)

        return reviews

    @classmethod
    def  get_average_ratings(cls, reviews: list[Review]) -> float:
        if not reviews:
            return 0.0

        total_rating = sum(review.rating for review in reviews)
        average_rating = total_rating / len(reviews)

        return average_rating
