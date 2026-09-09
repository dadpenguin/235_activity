import math

from flask import render_template, request

import music.adapters.repository as repo
import music.browse.services as services

from music.browse import browse_blueprint

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
