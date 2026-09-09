from flask import redirect, url_for, Blueprint

import music.adapters.repository as repo
from music.domainmodel.favourite import Favourite
from music.domainmodel.user import User

favourite_blueprint = Blueprint(
    "favourite_bp", __name__, url_prefix="/favourite"
)

@favourite_blueprint.route('/<int:track_id>')
def favourite(track_id: int):
    new_track = repo.repo_instance.get_track(track_id)
    new_user = User(user_id=300, user_name='Steve', password='password123')
    repo.repo_instance.add_user(new_user)
    favourite = Favourite(favourite_id=track_id, user=new_user, track=new_track)
    repo.repo_instance.add_favourite(favourite)

    return redirect(url_for('track_detail_bp.track_detail', track_id=track_id))

@favourite_blueprint.route('/remove/<int:track_id>')
def unfavourite(track_id: int):

    for favourite in repo.repo_instance.get_favourites_by_user("Steve"):
        if favourite.track.track_id == track_id:
            repo.repo_instance.remove_favourite(favourite)

    return redirect(url_for('track_detail_bp.track_detail', track_id=track_id))


