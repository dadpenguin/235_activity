import math

from flask import render_template, request, Blueprint

import music.adapters.repository as repo
from music.browse.services import BrowseService

browse_blueprint = Blueprint('browse_bp', __name__)

@browse_blueprint.route('/browse/<string:sorting>/<int:page>')
def browse(sorting: str, page: int):
    pages = []
    tracks = []
    main_dict = {}
    sorting_dict = {}

    if sorting == "genre":

        pages = BrowseService.browse_get_genre_dictionary(
            repo=repo.repo_instance
        )

    elif sorting == "alphabetical":

        pages = BrowseService.browse_get_alphabetical_dictionary(
            repo=repo.repo_instance
        )

    elif sorting == "id":
        pages = BrowseService.browse_get_id_lists(
            repo=repo.repo_instance
        )

    elif sorting == "artist":
        pages = BrowseService.browse_get_artist_dictionary(
            repo=repo.repo_instance
        )

    elif sorting == "album":
        pages = BrowseService.browse_get_album_dictionary(
            repo=repo.repo_instance
        )

    if page < 1 or page > len(pages):
        return "Page not found", 404

    if sorting == "id":
        tracks = pages[page - 1]

    if sorting == "genre" or sorting == "alphabetical" or sorting == "artist" or sorting == "album":
        main_dict = pages[page - 1]

    return render_template('browse.html', sorting=sorting, page=page, tracks=tracks, pages = pages, main_dict=main_dict)
