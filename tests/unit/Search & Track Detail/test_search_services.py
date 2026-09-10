import pytest

from music.search.services import SearchService
from music.adapters.memory_repository import MemoryRepository
import music.adapters.repository as repo

class TestSearchService:
    def test_getAllTracks_returns_tracks_that_match_keyword(self):
        results = SearchService.getAllTracks("Let's Climb a Mossy Hill")
        assert "Let's Climb a Mossy Hill" in results["track"]

    def test_getAllTracks_returns_artists_that_match_keyword(self):
        results = SearchService.getAllTracks("Celesteville")
        assert "Celesteville" in results["artist"]

    def test_getAllTracks_returns_genres_that_match_keyword(self):
        results = SearchService.getAllTracks("Lo-Fi")
        assert "Lo-Fi" in results["genre"]

    def test_getAllTracks_returns_albums_that_match_keyword(self):
        results = SearchService.getAllTracks("Lingua Ignota")
        assert "Lingua Ignota" in results["album"]

    def test_getAllTracks_partial_keyword_matches_track(self):
        results = SearchService.getAllTracks("Hi")
        assert "Let's Climb a Mossy Hill" in results["track"]

    def test_getAllTracks_search_is_case_insensitive(self):
        results = SearchService.getAllTracks("HITHERE")
        assert "hithere" in results["track"]

    def test_getAllTracks_no_matching_tracks_returns_empty_list(self):
        results = SearchService.getAllTracks("THIS DOES NOT EXIST")
        assert results["track"] == []

    def test_getAllTracks_no_matching_artists_returns_empty_list(self):
        results = SearchService.getAllTracks("THIS DOES NOT EXIST")
        assert results["artist"] == []

    def test_getAllTracks_no_matching_genres_returns_empty_list(self):
        results = SearchService.getAllTracks("THIS DOES NOT EXIST")
        assert results["genre"] == []

    def test_getAllTracks_no_matching_albums_returns_empty_list(self):
        results = SearchService.getAllTracks("THIS DOES NOT EXIST")
        assert results["album"] == []

    def test_getAllTracks_search_type_track_only_returns_tracks(self):
        results = SearchService.getAllTracks(
            "Let's Climb a Mossy Hill", search_type="track"
        )
        assert results["album"] == []
        assert results["artist"] == []
        assert results["genre"] == []
        assert results["track"] != []

    def test_getAllTracks_search_type_artist_only_returns_artists(self):
        results = SearchService.getAllTracks(
            "Celesteville", search_type="artist"
        )
        assert results["album"] == []
        assert results["artist"] != []
        assert results["genre"] == []
        assert results["track"] == []

    def test_getAllTracks_search_type_genre_only_returns_genres(self):
        results = SearchService.getAllTracks(
            "Lo-Fi", search_type="genre"
        )
        assert results["album"] == []
        assert results["artist"] == []
        assert results["genre"] != []
        assert results["track"] == []

    def test_getAllTracks_search_type_album_only_returns_albums(self):
        results = SearchService.getAllTracks(
            "Lingua Ignota", search_type="album"
        )
        assert results["album"] != []
        assert results["artist"] == []
        assert results["genre"] == []
        assert results["track"] == []

    def test_getAllTracks_without_search_type_returns_all_categories(self):
        results = SearchService.getAllTracks("")

        assert results["album"] != []
        assert results["artist"] != []
        assert results["genre"] != []
        assert results["track"] != []

    def test_getAllTracks_none_keyword_raises_type_error(self):
        with pytest.raises(TypeError):
            SearchService.getAllTracks(None)
