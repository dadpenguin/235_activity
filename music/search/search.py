from flask import Flask, render_template, redirect, url_for, request, Blueprint

import music.adapters.repository as repo
from music.adapters.memory_repository import MemoryRepository, populate
from music.domainmodel.favourite import Favourite
from music.domainmodel.user import User

search_blueprint = Blueprint(
    'search_bp', __name__, url_prefix='/search'
)


@search_blueprint.route('/<type>/<keyword>')
def search(type: str, keyword: str):
    if request.args.get('query') != None:
        keyword = request.args.get('query')
        return redirect(url_for('search_bp.search', type=type, keyword=keyword))

    results_track = []
    results_genre = []
    results_album = []
    results_artist = []

    if type not in ['all', 'title', 'album', 'genre', 'artist']:
        return redirect(url_for('search_bp.search', type='all', keyword='track'))

    if type == 'all':
        for track in repo.repo_instance.get_tracks():
            if track.title and keyword.lower() in track.title.lower() and track not in results_track:
                results_track.append(track)

            for genre in track.genres:
                if genre.name and keyword.lower() in genre.name.lower() and genre not in results_genre:
                    results_genre.append(genre)

            if track.album and keyword.lower() in track.album.title.lower() and track.album not in results_album:
                results_album.append(track.album)

            if track.artist and keyword.lower() in track.artist.full_name.lower() and track.artist not in results_artist:
                results_artist.append(track.artist)

    elif type == 'title':
        for track in repo.repo_instance.get_tracks():
            if track.title and keyword.lower() in track.title.lower() and track not in results_track:
                results_track.append(track)

    elif type == 'album':
        for track in repo.repo_instance.get_tracks():
            if track.album and keyword.lower() in track.album.title.lower() and track.album not in results_album:
                results_album.append(track.album)

    elif type == 'artist':
        for track in repo.repo_instance.get_tracks():
            if track.artist and keyword.lower() in track.artist.full_name.lower() and track.artist not in results_artist:
                results_artist.append(track.artist)

    elif type == 'genre':
        for track in repo.repo_instance.get_tracks():
            for genre in track.genres:
                if genre and keyword.lower() in genre.name.lower() and genre not in results_genre:
                    results_genre.append(genre)

    return render_template('search.html', results_track=results_track, results_artist=results_artist, results_genre=results_genre, results_album=results_album, keyword=keyword)