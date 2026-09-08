import math

from flask import render_template, request

import music.adapters.repository as repo
import music.browse.services as services

from music.browse import browse_blueprint


@browse_blueprint.route('/', methods=['GET'])
def home():
    """
    display the homepage with an alphabetical list of tracks.
    """

    page = request.args.get(
        'page',
        1,
        type=int
    )

    if page < 1:
        page = 1

    tracks_per_page = 10

    total_tracks = services.get_number_of_tracks(
        repo.repo_instance
    )

    total_pages = math.ceil(
        total_tracks / tracks_per_page
    )

    if total_pages > 0 and page > total_pages:
        page = total_pages

    tracks = services.get_tracks_for_page(
        page,
        tracks_per_page,
        repo.repo_instance
    )

    return render_template(
        'homepage.html',
        tracks=tracks,
        total_tracks=total_tracks,
        current_page=page,
        total_pages=total_pages
    )