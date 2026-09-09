
from music.adapters import repository


class SearchService:

    @classmethod
    def getAllTracks(cls, keyword: str = "", search_type: str | None = None) -> dict:
        keyword = keyword.lower()

        tracks = repository.repo_instance.get_tracks_by_title(keyword) or []
        artists = repository.repo_instance.get_artists_by_name(keyword) or []
        genres = repository.repo_instance.get_genres_by_name(keyword) or []
        albums = repository.repo_instance.get_albums_by_name(keyword) or []


        filtered_tracks = list({item for item in tracks if keyword in str(item).lower()})
        filtered_artists = list({item for item in artists if keyword in str(item).lower()})
        filtered_genres = list({item for item in genres if keyword in str(item).lower()})
        filtered_album = list({item for item in albums if keyword in str(item).lower()})


        if search_type == "track":
            return {"track": filtered_tracks}
        if search_type == "artist":
            return {"artist": filtered_artists}
        if search_type == "genre":
            return {"genre": filtered_genres}
        if search_type == "album":
            return {"album": filtered_album}

        return {
            "track": filtered_tracks,
            "artist": filtered_artists,
            "genre": filtered_genres,
            "album": filtered_album

        }
