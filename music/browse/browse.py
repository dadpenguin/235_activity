import math

from flask import render_template, request, Blueprint

import music.adapters.repository as repo
import music.browse.services as services

browse_blueprint = Blueprint('browse_bp', __name__)

@browse_blueprint.route('/browse/<string:sorting>/<int:page>')
def browse(sorting: str, page: int):
    pages = []
    tracks = []
    main_dict ={}
    sorting_dict = {}

    if sorting == "genre":
        for track in repo.repo_instance.get_tracks():
            for genre in track.genres:
                if genre and genre not in sorting_dict:
                    sorting_dict[genre] = [thing for thing in repo.repo_instance.get_tracks_by_genre(genre.name)]

        sorting_dict = dict(sorted(sorting_dict.items(), key=lambda item: item[0].name))

        for genre in sorting_dict:
            main_dict[genre] = sorting_dict[genre]

            if len(main_dict) % 3 == 0 and len(main_dict) != 0:
                pages.append(main_dict)
                main_dict = {}

    elif sorting == "alphabetical":
        for track in repo.repo_instance.get_tracks():
            if track.title and track.title[0].lower() not in sorting_dict:
                sorting_dict[track.title[0].lower()] = [track]

            elif track.title and track not in sorting_dict[track.title[0].lower()]:
                sorting_dict[track.title[0].lower()].append(track)

        sorting_dict = dict(sorted(sorting_dict.items(), key=lambda item: item[0].lower()))

        for letter in sorting_dict:
            main_dict[letter] = sorting_dict[letter]

            if len(main_dict) % 3 == 0 and len(main_dict) != 0:
                pages.append(main_dict)
                main_dict = {}

    elif sorting == "id":
        for track in repo.repo_instance.get_tracks():
            if track and track not in tracks:
                tracks.append(track)

            if len(tracks) % 10 == 0 and len(tracks) != 0:
                pages.append(tracks)
                tracks = []

    elif sorting == "artist":
        for track in repo.repo_instance.get_tracks():
            if track.artist and track.artist.full_name not in sorting_dict:
                sorting_dict[track.artist.full_name] = [track]

            elif track.artist and track not in sorting_dict[track.artist.full_name]:
                sorting_dict[track.artist.full_name].append(track)

        sorting_dict = dict(sorted(sorting_dict.items(), key=lambda item: item[0].lower()))

        for artist in sorting_dict:
            main_dict[artist] = sorting_dict[artist]

            if len(main_dict) % 3 == 0 and len(main_dict) != 0:
                pages.append(main_dict)
                main_dict = {}

    elif sorting == "album":
        for track in repo.repo_instance.get_tracks():
            if track.album and track.album.title not in sorting_dict:
                sorting_dict[track.album.title] = [track]

            elif track.album and track not in sorting_dict[track.album.title]:
                sorting_dict[track.album.title].append(track)

        sorting_dict = dict(sorted(sorting_dict.items(), key=lambda item: item[0]))

        for artist in sorting_dict:
            main_dict[artist] = sorting_dict[artist]

            if len(main_dict) % 3 == 0 and len(main_dict) != 0:
                pages.append(main_dict)
                main_dict = {}

    if page < 1 or page > len(pages):
        return "Page not found", 404

    if sorting == "id":
        tracks = pages[page - 1]

    if sorting == "genre" or sorting == "alphabetical" or sorting == "artist" or sorting == "album":
        main_dict = pages[page - 1]

    return render_template('browse.html', sorting=sorting, page=page, tracks=tracks, pages = pages, main_dict=main_dict)
