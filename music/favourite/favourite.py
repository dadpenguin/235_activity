from flask import redirect, url_for, Blueprint, session

import music.adapters.repository as repo
from music.authentication.services import AuthService
from music.domainmodel.favourite import Favourite
from music.domainmodel.user import User
from music.favourite.services import FavouriteService

favourite_blueprint = Blueprint(
    "favourite_bp", __name__, url_prefix="/favourite"
)

@favourite_blueprint.route('/<int:track_id>')
def favourite(track_id: int):
    user_name = AuthService.get_authenticated_user_name()

    if user_name is None or user_name == "":
        return "must be logged in"

    isSuccessful = FavouriteService.register_favourite(user_name, track_id, repo.repo_instance)


    if isSuccessful:
        return redirect(url_for('track_detail_bp.track_detail', track_id=track_id))
    else:
        return "error"

@favourite_blueprint.route('/remove/<int:track_id>')
def unfavourite(track_id: int):
    user_name = AuthService.get_authenticated_user_name()
    isSuccessful = FavouriteService.remove_favourite(user_name, track_id, repo.repo_instance)

    if user_name is None or user_name == "":
        return "must be logged in"




    if isSuccessful:
        return redirect(url_for('track_detail_bp.track_detail', track_id=track_id))
    else:
        return "error"
