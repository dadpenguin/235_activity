from flask import Blueprint, redirect, render_template, url_for

import music.adapters.repository as repo
from music.authentication.services import AuthService
from music.review.exceptions import ReviewFieldsMissing
from music.review.forms import ReviewForm
from music.review.services import ReviewService

review_blueprint = Blueprint(
    "review_bp", __name__, url_prefix="/review"
)



@review_blueprint.route("/make/<int:track_id>", methods=["GET", "POST"])
def create_review(track_id: int):
    user_name = AuthService.get_authenticated_user_name()
    if user_name is None:
        return redirect(url_for("signup"))

    form = ReviewForm(track_id=track_id)

    review_error_message = None

    if form.validate_on_submit():
        stars = form.stars.data
        paragraph = form.paragraph.data

        if stars is None or paragraph is None:
            raise ReviewFieldsMissing("stars or paragraph field is missing")

        status = ReviewService.create_review(
            repo.repo_instance,
            user_name,
            track_id,
            int(stars),
            paragraph.strip()
        )

        if status is not None:
            return redirect(url_for('track_detail_bp.track_detail', track_id=track_id))

        review_error_message = "Failed to submit review. Please try again."

    return render_template(
        'reviewmake.html',
        title='Write a Review',
        form=form,
        track_id=track_id,
        review_error_message=review_error_message,
        handler_url=url_for('review_bp.create_review', track_id=track_id)
    )
