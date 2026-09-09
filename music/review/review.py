from flask import redirect, url_for, Blueprint, session, render_template, request
from music.authentication.services import AuthService

import music.adapters.repository as repo
from music.domainmodel.favourite import Favourite
from music.domainmodel.user import User
from music.domainmodel.review import Review

review_blueprint = Blueprint(
    "review_bp", __name__, url_prefix="/review"
)

@review_blueprint.route('/make/<int:track_id>')
def make_review(track_id: int):
    if AuthService.get_authenticated_user_name() == None:
        return redirect(url_for("signup"))

    else:
        return render_template('reviewmake.html', track_id=track_id)

@review_blueprint.route('/make/final/<int:track_id>')
def make_review_final(track_id: int):
    if AuthService.get_authenticated_user_name() == None:
        return redirect(url_for("signup"))

    else:
        stars = int(request.args.get('stars'))
        paragraph = request.args.get('paragraph')

        reviews = []

        for track in repo.repo_instance.get_tracks():
            for review in repo.repo_instance.get_reviews_by_track(track.track_id):
                reviews.append(review)

        review_id = len(reviews) + 1

        new_review = Review(review_id=review_id, user=AuthService.get_authenticated_user_name(), track=repo.repo_instance.get_track(track_id), rating=stars, review_text=paragraph)
        repo.repo_instance.add_review(new_review)
        return redirect(url_for("track_detail_bp.track_detail", track_id=track_id))


