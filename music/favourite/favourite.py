from flask import redirect, url_for, Blueprint, session, render_template
from flask.helpers import abort

import music.adapters.repository as repo
from music.authentication.authentication import login_required
from music.authentication.services import AuthService
from music.domainmodel.favourite import Favourite
from music.domainmodel.user import User
from music.favourite.services import FavouriteService


favourite_blueprint = Blueprint(
    "favourite_bp",
    __name__,
    url_prefix="/favourite"
)


@favourite_blueprint.route('/favourites', methods=['GET'])
@login_required
def favourites(user_name: str):
    user_favourites = FavouriteService.get_favourites_by_user(
        user_name, repo.repo_instance
    )
    return render_template('favourites.html', favourites=user_favourites)


@favourite_blueprint.route('/<int:track_id>', methods=['POST'])
@login_required
def favourite(user_name: str, track_id: int):
    success = FavouriteService.register_favourite(
        user_name, track_id, repo.repo_instance
    )
    if not success:
        abort(500)

    return redirect(url_for('track_detail_bp.track_detail', track_id=track_id))


@favourite_blueprint.route('/remove/<int:track_id>', methods=['POST'])
@login_required
def unfavourite(user_name: str, track_id: int):
    success = FavouriteService.remove_favourite(
        user_name, track_id, repo.repo_instance
    )
    if not success:
        abort(500)

    return redirect(url_for('track_detail_bp.track_detail', track_id=track_id))
