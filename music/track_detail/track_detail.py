from flask import render_template, Blueprint, session
from music.authentication.services import AuthService

import music.adapters.repository as repo

track_detail_blueprint = Blueprint(
    'track_detail_bp', __name__, url_prefix='/track'
)

@track_detail_blueprint.route('/<int:track_id>')
def track_detail(track_id: int):

    track = repo.repo_instance.get_track(track_id)
    favourited = False

    logged_in = AuthService.get_authenticated_user_name()

    for favourite in repo.repo_instance.get_favourites_by_user(logged_in):
        if favourite.track.track_id == track_id:
            favourited = True
            break

    total_rating = 0
    average_rating = 0
    if not track:
        return "Track not found", 404

    reviews = repo.repo_instance.get_reviews_by_track(track_id)
    reviews.sort(key=lambda review: review.timestamp, reverse=True)

    for review in reviews:
        total_rating += review.rating
        average_rating = total_rating / len(reviews)
    return render_template('track_detail.html', track=track, reviews=reviews, average_rating=average_rating,
                               track_id=track_id, favourited=favourited, logged_in=logged_in)