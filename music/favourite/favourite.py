from flask import redirect, url_for, Blueprint, session, render_template

import music.adapters.repository as repo
from music.authentication.services import AuthService
from music.domainmodel.favourite import Favourite
from music.domainmodel.user import User
<<<<<<< Updated upstream
from music.favourite.services import FavouriteService

=======
from music.authentication.services import AuthService
>>>>>>> Stashed changes

favourite_blueprint = Blueprint(
    "favourite_bp",
    __name__,
    url_prefix="/favourite"
)


@favourite_blueprint.route('/favourites')
def favourites():
    user_name = AuthService.get_authenticated_user_name()

    if user_name is None or user_name == "":
        return redirect(url_for('authentication_bp.login'))

    favourites = repo.repo_instance.get_favourites_by_user(user_name)

    return render_template(
        'favourites.html',
        favourites=favourites
    )


@favourite_blueprint.route('/<int:track_id>')
def favourite(track_id: int):
<<<<<<< Updated upstream
    user_name = AuthService.get_authenticated_user_name()

    if user_name is None or user_name == "":
        return "must be logged in"
=======

    new_track = repo.repo_instance.get_track(track_id)
    username = AuthService.get_authenticated_user_name()

    if username == None:
        return redirect(url_for('track_detail_bp.track_detail', track_id=track_id))

    user = repo.repo_instance.get_user(username.strip().lower())
>>>>>>> Stashed changes

    isSuccessful = FavouriteService.register_favourite(
        user_name,
        track_id,
        repo.repo_instance
    )

    if isSuccessful:
        return redirect(
            url_for(
                'track_detail_bp.track_detail',
                track_id=track_id
            )
        )
    else:
        return "error"


@favourite_blueprint.route('/remove/<int:track_id>')
def unfavourite(track_id: int):
    user_name = AuthService.get_authenticated_user_name()

    if user_name is None or user_name == "":
        return "must be logged in"

    isSuccessful = FavouriteService.remove_favourite(
        user_name,
        track_id,
        repo.repo_instance
    )

    if isSuccessful:
        return redirect(
            url_for(
                'track_detail_bp.track_detail',
                track_id=track_id
            )
        )
    else:
        return "error"