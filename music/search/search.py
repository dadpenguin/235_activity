from flask import Flask, render_template, redirect, url_for, request, Blueprint
from flask.helpers import abort
from flask.json import jsonify

import music.adapters.repository as repo
from music.adapters.memory_repository import MemoryRepository, populate
from music.domainmodel.favourite import Favourite
from music.domainmodel.user import User
from music.search.services import SearchService

search_blueprint = Blueprint(
    'search_bp', __name__, url_prefix='/search'
)


@search_blueprint.route('/')
def search():

    query = request.args.get('q', '').strip()
    search_type = request.args.get('type', '').strip()

    results = SearchService.getAllTracks(query, search_type)

    is_empty = False

    has_results = results and any(results.values())
    if not has_results:
        is_empty = True

    tracks = results.get("track") or []
    artists = results.get("artist") or []
    genres = results.get("genre") or []
    albums = results.get("album") or []

    return render_template('search.html', results_track=tracks, results_artist=artists, results_genre=genres, results_album=albums, keyword=query, is_empty=is_empty)
