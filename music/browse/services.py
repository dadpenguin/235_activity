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
