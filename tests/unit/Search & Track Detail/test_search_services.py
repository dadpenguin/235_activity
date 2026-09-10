import pytest

from music.domainmodel.artist import Artist
from music.search.services import SearchService
from music.adapters.memory_repository import MemoryRepository, populate
import music.adapters.repository as repo

@pytest.fixture
def repo_instance():
    repo.repo_instance = MemoryRepository()

    populate("music/adapters/data", repo.repo_instance)

    return repo.repo_instance

class TestSearchService:
    def test_getAllTracks_returns_tracks_that_match_keyword(self, repo_instance):
        results = SearchService.getAllTracks("Let's Climb a Mossy Hill")
        assert any(track.title == "Let's Climb a Mossy Hill" for track in results["track"])

    def test_getAllTracks_returns_artists_that_match_keyword(self, repo_instance):
        results = SearchService.getAllTracks("Celesteville")
        assert any(artist.full_name == "Celesteville" for artist in results["artist"])

    def test_getAllTracks_returns_genres_that_match_keyword(self, repo_instance):
        results = SearchService.getAllTracks("Lo-Fi")
        assert any(genre.name == "Lo-Fi" for genre in results["genre"])

    def test_getAllTracks_returns_albums_that_match_keyword(self, repo_instance):
        results = SearchService.getAllTracks("Lingua Ignota")
        assert any(album.title == "Lingua Ignota" for album in results["album"])

    def test_getAllTracks_partial_keyword_matches_track(self, repo_instance):
        results = SearchService.getAllTracks("Hi")
        assert any(track.title ==  "Let's Climb a Mossy Hill" for track in results["track"])

    def test_getAllTracks_search_is_case_insensitive(self, repo_instance):
        results = SearchService.getAllTracks("BIG CITY")
        assert any(track.title == "Big City" for track in results["track"])

    def test_getAllTracks_no_matching_tracks_returns_empty_list(self, repo_instance):
        results = SearchService.getAllTracks("THIS DOES NOT EXIST")
        assert results["track"] == []

    def test_getAllTracks_no_matching_artists_returns_empty_list(self, repo_instance):
        results = SearchService.getAllTracks("THIS DOES NOT EXIST")
        assert results["artist"] == []

    def test_getAllTracks_no_matching_genres_returns_empty_list(self, repo_instance):
        results = SearchService.getAllTracks("THIS DOES NOT EXIST")
        assert results["genre"] == []

    def test_getAllTracks_no_matching_albums_returns_empty_list(self, repo_instance):
        results = SearchService.getAllTracks("THIS DOES NOT EXIST")
        assert results["album"] == []

    def test_getAllTracks_search_type_track_only_returns_tracks(self, repo_instance):
        results = SearchService.getAllTracks(
            "Let's Climb a Mossy Hill", search_type="track"
        )
        assert "track" in results
        assert len(results) == 1

    def test_getAllTracks_search_type_artist_only_returns_artists(self, repo_instance):
        results = SearchService.getAllTracks(
            "Celesteville", search_type="artist"
        )
        assert "artist" in results
        assert len(results) == 1

    def test_getAllTracks_search_type_genre_only_returns_genres(self, repo_instance):
        results = SearchService.getAllTracks(
            "Lo-Fi", search_type="genre"
        )
        assert "genre" in results
        assert len(results) == 1

    def test_getAllTracks_search_type_album_only_returns_albums(self, repo_instance):
        results = SearchService.getAllTracks(
            "Lingua Ignota", search_type="album"
        )
        assert "album" in results
        assert len(results) == 1

    def test_getAllTracks_without_search_type_returns_all_categories(self, repo_instance):
        results = SearchService.getAllTracks("")

        assert results["album"] != []
        assert results["artist"] != []
        assert results["genre"] != []
        assert results["track"] != []

    def test_getAllTracks_none_keyword_raises_type_error(self, repo_instance):
        with pytest.raises(AttributeError):
            SearchService.getAllTracks(None)
