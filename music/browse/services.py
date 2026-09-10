from music.adapters.repository import AbstractRepository

def get_all_tracks(repo: AbstractRepository):
    tracks = repo.get_tracks()

    return sorted(
        tracks,
        key=lambda track: (track.title or "").lower()
    )

def get_number_of_tracks(repo: AbstractRepository):
    return repo.get_number_of_tracks()

def get_tracks_for_page(page:int, track_per_page:int, repo: AbstractRepository):
    tracks = get_all_tracks(repo)
    start_index = (page - 1) * track_per_page
    end_index = page * track_per_page

    return tracks[start_index:end_index]

class BrowseService:
    @classmethod
    def browse_get_genre_dictionary(cls, repo: AbstractRepository):
        pages = []
        main_dict = {}
        sorting_dict = {}

        for track in repo.get_tracks():
            for genre in track.genres:
                if genre and genre not in sorting_dict:
                    sorting_dict[genre] = [thing for thing in repo.get_tracks_by_genre(genre.name)]

        sorting_dict = dict(sorted(sorting_dict.items(), key=lambda item: item[0].name))

        for genre in sorting_dict:
            main_dict[genre] = sorting_dict[genre]

            if len(main_dict) % 3 == 0 and len(main_dict) != 0:
                pages.append(main_dict)
                main_dict = {}

        return pages

    @classmethod
    def browse_get_alphabetical_dictionary(cls, repo: AbstractRepository):
        pages = []
        main_dict = {}
        sorting_dict = {}

        for track in repo.get_tracks():
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

        return pages

    @classmethod
    def browse_get_id_lists(cls, repo: AbstractRepository):
        pages = []
        tracks = []

        for track in repo.get_tracks():
            if track and track not in tracks:
                tracks.append(track)

            if len(tracks) % 10 == 0 and len(tracks) != 0:
                pages.append(tracks)
                tracks = []

        return pages

    @classmethod
    def browse_get_album_dictionary(cls, repo: AbstractRepository):
        pages = []
        main_dict = {}
        sorting_dict = {}

        for track in repo.get_tracks():
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

        return pages

    @classmethod
    def browse_get_artist_dictionary(cls, repo: AbstractRepository):
        pages = []
        main_dict = {}
        sorting_dict = {}

        for track in repo.get_tracks():
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

        return pages
