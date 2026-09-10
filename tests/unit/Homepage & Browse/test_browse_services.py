import pytest


from music.adapters.memory_repository import MemoryRepository
import music.adapters.repository as repo
from music.browse.services import BrowseService

class TestBrowseService:

    def test_browse_get_genre_dictionary_returns_genres(self):
        repo = MemoryRepository()
        results = BrowseService.browse_get_genre_dictionary(repo=repo)
        genres = []
        for page in results:
            for genre in page:
                assert genre.name

    def test_browse_get_genre_dictionary_groups_tracks_by_genre(self):
        repo = MemoryRepository()
        results = BrowseService.browse_get_genre_dictionary(repo=repo)

        for page in results:
            genres = list(page.keys())
            for genre in genres:
                for track in page[genre]:
                    assert genre in track.genres

    def test_browse_get_genre_dictionary_sorts_genres_alphabetically(self):
        repo = MemoryRepository()
        results = BrowseService.browse_get_genre_dictionary(repo=repo)
        for page in results:
            genres = list(page.keys())
            assert genres == sorted(genres, key=lambda genre: genre.name)

    def test_browse_get_genre_dictionary_returns_three_genres_per_page(self):
        repo = MemoryRepository()
        results = BrowseService.browse_get_genre_dictionary(repo=repo)
        for page in results:
            genres = list(page.keys())
            assert len(genres) >= 0
            assert len(genres) <= 3

    def test_browse_get_alphabetical_dictionary_groups_tracks_by_first_letter(self):
        repo = MemoryRepository()
        results = BrowseService.browse_get_alphabetical_dictionary(repo=repo)
        for page in results:
            letters = list(page.keys())
            for letter in letters:
                for track in page[letter]:
                    assert letter == track.title[0].lower()

    def test_browse_get_alphabetical_dictionary_sorts_letters_alphabetically(self):
        repo = MemoryRepository()
        results = BrowseService.browse_get_alphabetical_dictionary(repo=repo)
        for page in results:
            letters = list(page.keys())
            assert letters == sorted(letters, key=lambda letter: letter)

    def test_browse_get_alphabetical_dictionary_does_not_duplicate_tracks(self):
        repo = MemoryRepository()
        results = BrowseService.browse_get_alphabetical_dictionary(repo=repo)
        track_list = []
        for page in results:
            letters = list(page.keys())
            for letter in letters:
                for track in page[letter]:
                    assert track not in track_list
                    track_list.append(track)

    def test_browse_get_alphabetical_dictionary_returns_three_letters_per_page(self):
        repo = MemoryRepository()
        results = BrowseService.browse_get_alphabetical_dictionary(repo=repo)
        for page in results:
            letters = list(page.keys())
            assert len(letters) >= 0
            assert len(letters) <= 3


    def test_browse_get_id_lists_returns_tracks(self):
        repo = MemoryRepository()
        results = BrowseService.browse_get_id_lists(repo=repo)
        for page in results:
            for track in page:
                assert track.title


    def test_browse_get_id_lists_does_not_duplicate_tracks(self):
        repo = MemoryRepository()
        results = BrowseService.browse_get_id_lists(repo=repo)
        tracks = []
        for page in results:
            for track in page:
                assert track not in tracks
                tracks.append(track)


    def test_browse_get_id_lists_returns_ten_tracks_per_page(self):
        repo = MemoryRepository()
        results = BrowseService.browse_get_id_lists(repo=repo)
        for page in results:
            assert len(page) <= 10

    def test_browse_get_album_dictionary_groups_tracks_by_album(self):
        repo = MemoryRepository()
        results = BrowseService.browse_get_album_dictionary(repo=repo)
        for page in results:
            albums = list(page.keys())
            for album in albums:
                for track in page[album]:
                    assert album == track.album


    def test_browse_get_album_dictionary_sorts_albums_alphabetically(self):
        repo = MemoryRepository()
        results = BrowseService.browse_get_album_dictionary(repo=repo)
        for page in results:
            albums = list(page.keys())
            assert albums == sorted(albums, key=lambda album: album.title)

    def test_browse_get_album_dictionary_does_not_duplicate_tracks(self):
        repo = MemoryRepository()
        results = BrowseService.browse_get_album_dictionary(repo=repo)
        track_list = []
        for page in results:
            albums = list(page.keys())
            for album in albums:
                for track in page[album]:
                    assert track not in track_list
                    track_list.append(track)

    def test_browse_get_album_dictionary_returns_three_albums_per_page(self):
        repo = MemoryRepository()
        results = BrowseService.browse_get_album_dictionary(repo=repo)
        for page in results:
            albums = list(page.keys())
            assert len(albums) >= 0
            assert len(albums) <= 3

    def test_browse_get_artist_dictionary_groups_tracks_by_artist(self):
        repo = MemoryRepository()
        results = BrowseService.browse_get_artist_dictionary(repo=repo)
        for page in results:
            artists = list(page.keys())
            for artist in artists:
                for track in page[artist]:
                    assert track.artist == artist


    def test_browse_get_artist_dictionary_sorts_artists_alphabetically(self):
        repo = MemoryRepository()
        results = BrowseService.browse_get_artist_dictionary(repo=repo)
        for page in results:
            artists = list(page.keys())
            assert artists == sorted(artists, key=lambda artist: artist.full_name)

    def test_browse_get_artist_dictionary_does_not_duplicate_tracks(self):
        repo = MemoryRepository()
        results = BrowseService.browse_get_artist_dictionary(repo=repo)
        track_list = []
        for page in results:
            artists = list(page.keys())
            for artist in artists:
                for track in page[artist]:
                    assert track not in track_list
                    track_list.append(track)

    def test_browse_get_artist_dictionary_returns_three_artists_per_page(self):
        repo = MemoryRepository()
        results = BrowseService.browse_get_artist_dictionary(repo=repo)
        for page in results:
            artists = list(page.keys())
            assert len(artists) >= 0
            assert len(artists) <= 3