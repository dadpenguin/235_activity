import pytest

from music.domainmodel.album import Album

def test_album_id_is_valid():
    album = Album(album_id=123, album_title='Tailor Swift', release_year=2020, total_tracks=3)
    assert album.album_id == 123

def test_album_id_is_negative():
    with pytest.raises(ValueError):
        Album(album_id=-123, album_title='Tailor Swift', release_year=2020, total_tracks=3)

def test_album_id_is_string():
    with pytest.raises(ValueError):
        Album(album_id="Nahuatl", album_title='Tailor Swift', release_year=2020, total_tracks=3)

def test_album_id_is_none():
    with pytest.raises(ValueError):
        Album(album_id=None, album_title='Tailor Swift', release_year=2020, total_tracks=3)

def test_album_title_is_valid():
    album = Album(album_id=123, album_title='Tailor Swift', release_year=2020, total_tracks=3)
    assert album.album_title == "Tailor Swift"

def test_album_title_is_int():
    with pytest.raises(ValueError):
        Album(album_id=123, album_title=12345, release_year=2020, total_tracks=3)

def test_album_title_is_spaced_empty_string():
    with pytest.raises(ValueError):
        Album(album_id=123, album_title="         ", release_year=2020, total_tracks=3)

def test_album_title_is_empty_string():
    with pytest.raises(ValueError):
        Album(album_id=123, album_title="", release_year=2020, total_tracks=3)

def test_album_title_is_none():
    with pytest.raises(ValueError):
        Album(album_id=123, album_title="", release_year=2020, total_tracks=3)

def test_album_title_is_not_random_unicode_character():
    with pytest.raises(ValueError):
        Album(album_id=123, album_title="\u180e", release_year=2020, total_tracks=3)

def test_album_title_removes_unwanted_spacing():
    album = Album(album_id=123, album_title="     x        ", release_year=2020, total_tracks=3)
    assert album.album_title == "x"

def test_album_title_removes_more_than_one_space():
    album = Album(album_id=123, album_title="a      b        c", release_year=2020, total_tracks=3)
    assert album.album_title == "a b c"

def test_release_year_is_valid():
    album = Album(album_id=123, album_title="Steve", release_year=2020, total_tracks=3)
    assert album.release_year == 2020

def test_release_year_is_negative():
    with pytest.raises(ValueError):
        Album(album_id=123, album_title='Tailor Swift', release_year=-2020, total_tracks=3)

def test_release_year_is_in_the_future():
    with pytest.raises(ValueError):
        Album(album_id=123, album_title='Tailor Swift', release_year=2345, total_tracks=3)

def test_release_year_is_string():
    with pytest.raises(ValueError):
        Album(album_id=123, album_title='Tailor Swift', release_year="HITHERE", total_tracks=3)

def test_release_year_is_true():
    with pytest.raises(ValueError):
        Album(album_id=123, album_title='Tailor Swift', release_year=True, total_tracks=3)

def test_total_tracks_is_valid():
    album = Album(album_id=123, album_title='Tailor Swift', release_year=2020, total_tracks=354)

def test_total_tracks_is_negative():
    with pytest.raises(ValueError):
        Album(album_id=123, album_title='Tailor Swift', release_year=2020, total_tracks=-234)

def test_total_tracks_is_true():
    with pytest.raises(ValueError):
        Album(album_id=123, album_title='Tailor Swift', release_year=2020, total_tracks=True)