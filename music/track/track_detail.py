from flask import Blueprint, render_template

import music.adapters.repository as repo
from music.authentication.services import AuthService
from music.track.services import TrackService

track_detail_blueprint = Blueprint("track_detail_bp", __name__, url_prefix="/track")


@track_detail_blueprint.route("/<int:track_id>")
def track_detail(track_id: int):

    track = TrackService.get_track(track_id, repo.repo_instance)

    user_name = AuthService.get_authenticated_user_name()

    favourited = TrackService.is_user_favourite(user_name, repo.repo_instance, track_id)

    if not track:
        return "Track not found", 404

    reviews = TrackService.get_reviews_by_track_id(track_id, repo.repo_instance)

    average_rating = TrackService.get_average_ratings(reviews)


    return render_template(
        "track_detail.html",
        track=track,
        reviews=reviews,
        average_rating=average_rating,
        track_id=track_id,
        favourited=favourited,
        logged_in=user_name,
    )
