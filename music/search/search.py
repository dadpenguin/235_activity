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
    if request.args.get('keyword') != None:
        keyword = request.args.get('keyword')
        return redirect(url_for('search_bp.search', type=type, keyword=keyword))

    results = []

    if type not in ['all', 'title', 'album', 'genre', 'artist']:
        return redirect(url_for('search_bp.search', type='all', keyword='track'))

    if type == 'all':
        for track in repo.repo_instance.get_tracks():
            if track.title and keyword.lower() in track.title.lower() and track.title not in results:
                results.append(track.title)

            for genre in track.genres:
                if genre.name and keyword.lower() in genre.name.lower() and genre.name not in results:
                    results.append(genre.name)

            if track.album and keyword.lower() in track.album.title.lower() and track.album.title not in results:
                results.append(track.album.title)

            if track.artist and keyword.lower() in track.artist.full_name.lower() and track.artist.full_name not in results:
                results.append(track.artist.full_name)

    elif type == 'title':
        for track in repo.repo_instance.get_tracks():
            if track.title and keyword.lower() in track.title.lower() and track.title not in results:
                results.append(track.title)

    elif type == 'album':
        for track in repo.repo_instance.get_tracks():
            if track.album and keyword.lower() in track.album.title.lower() and track.album.title not in results:
                results.append(track.album.title)

    elif type == 'artist':
        for track in repo.repo_instance.get_tracks():
            if track.artist and keyword.lower() in track.artist.full_name.lower() and track.artist.full_name not in results:
                results.append(track.artist.full_name)

    elif type == 'genre':
        for track in repo.repo_instance.get_tracks():
            for genre in track.genres:
                if genre and keyword.lower() in genre.name.lower() and genre.name not in results:
                    results.append(genre.name)

    return render_template('search.html', results=results, keyword=keyword)