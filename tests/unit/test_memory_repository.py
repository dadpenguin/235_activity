import pytest

from music.adapters.memory_repository import MemoryRepository
from music.domainmodel.artist import Artist
from music.domainmodel.favourite import Favourite
from music.domainmodel.genre import Genre
from music.domainmodel.review import Review
from music.domainmodel.track import Track
from music.domainmodel.user import User


def make_track(
    track_id=1,
    title="Midnight Song",
    artist_name="The Testers",
    genre_name="Electronic",
):
    """Create a complete Track object for repository tests."""
    track = Track(track_id, title)
    track.artist = Artist(track_id, artist_name)
    track.add_genre(Genre(track_id, genre_name))
    return track


@pytest.fixture
def repo():
    """Provide a new empty repository for each test."""
    return MemoryRepository()


# Test that a new repository starts with no tracks.
def test_repository_is_empty_when_created(repo):
    assert repo.get_tracks() == []
    assert repo.get_number_of_tracks() == 0


# Test that a track can be stored and retrieved by its ID.
def test_add_and_get_track(repo):
    track = make_track()

    repo.add_track(track)

    assert repo.get_track(track.track_id) is track
    assert repo.get_number_of_tracks() == 1


# Test that adding the same track twice does not create a duplicate.
def test_add_track_does_not_add_duplicates(repo):
    track = make_track()

    repo.add_track(track)
    repo.add_track(track)

    assert repo.get_tracks() == [track]


# Test that requesting an unknown track ID returns None.
def test_get_unknown_track_returns_none(repo):
    assert repo.get_track(9999) is None


# Test that callers receive a copy and cannot modify the repository's track list.
def test_get_tracks_returns_a_copy(repo):
    track = make_track()
    repo.add_track(track)

    returned_tracks = repo.get_tracks()
    returned_tracks.clear()

    assert repo.get_tracks() == [track]


# Test that title search is case-insensitive and supports partial matches.
def test_get_tracks_by_title(repo):
    matching_track = make_track(1, "Midnight Song")
    other_track = make_track(2, "Morning News")
    repo.add_track(matching_track)
    repo.add_track(other_track)

    assert repo.get_tracks_by_title("NIGHT") == [matching_track]


# Test that artist search is case-insensitive and supports partial matches.
def test_get_tracks_by_artist(repo):
    matching_track = make_track(1, artist_name="The Testers")
    other_track = make_track(2, artist_name="Another Band")
    repo.add_track(matching_track)
    repo.add_track(other_track)

    assert repo.get_tracks_by_artist("tester") == [matching_track]


# Test that genre search is case-insensitive and supports partial matches.
def test_get_tracks_by_genre(repo):
    matching_track = make_track(1, genre_name="Electronic")
    other_track = make_track(2, genre_name="Classical")
    repo.add_track(matching_track)
    repo.add_track(other_track)

    assert repo.get_tracks_by_genre("ELECTRO") == [matching_track]


# Test that a user can be stored and retrieved with a case-insensitive username.
def test_add_and_get_user(repo):
    user = User(1, "Alice", "password1")

    repo.add_user(user)

    assert repo.get_user("  ALICE  ") is user


# Test that two users with the same normalized username are not both stored.
def test_add_user_does_not_add_duplicate_username(repo):
    first_user = User(1, "Alice", "password1")
    duplicate_user = User(2, "ALICE", "password2")

    repo.add_user(first_user)
    repo.add_user(duplicate_user)

    assert repo.get_user("alice") is first_user


# Test that reviews are returned only for the requested track.
def test_add_and_get_reviews_by_track(repo):
    user = User(1, "Alice", "password1")
    first_track = make_track(1, "First Song")
    second_track = make_track(2, "Second Song")
    first_review = Review(1, user, first_track, 5, "Excellent track")
    second_review = Review(2, user, second_track, 3, "Average track")

    repo.add_review(first_review)
    repo.add_review(second_review)

    assert repo.get_reviews_by_track(first_track.track_id) == [first_review]


# Test that adding the same review twice does not create a duplicate.
def test_add_review_does_not_add_duplicates(repo):
    user = User(1, "Alice", "password1")
    track = make_track()
    review = Review(1, user, track, 5, "Excellent track")

    repo.add_review(review)
    repo.add_review(review)

    assert repo.get_reviews_by_track(track.track_id) == [review]


# Test that a favourite can be stored and found by username and track ID.
def test_add_and_get_favourite(repo):
    user = User(1, "Alice", "password1")
    track = make_track()
    favourite = Favourite(1, user, track)

    repo.add_favourite(favourite)

    assert repo.get_favourite("ALICE", track.track_id) is favourite
    assert repo.get_favourites_by_user("alice") == [favourite]


# Test that a user cannot favourite the same track more than once.
def test_add_favourite_does_not_add_duplicate_user_track_pair(repo):
    user = User(1, "Alice", "password1")
    track = make_track()
    first_favourite = Favourite(1, user, track)
    duplicate_favourite = Favourite(2, user, track)

    repo.add_favourite(first_favourite)
    repo.add_favourite(duplicate_favourite)

    assert repo.get_favourites_by_user("alice") == [first_favourite]


# Test that favourites belonging to different users remain separate.
def test_get_favourites_by_user_only_returns_that_users_favourites(repo):
    alice = User(1, "Alice", "password1")
    bob = User(2, "Bob", "password2")
    track = make_track()
    alice_favourite = Favourite(1, alice, track)
    bob_favourite = Favourite(2, bob, track)
    repo.add_favourite(alice_favourite)
    repo.add_favourite(bob_favourite)

    assert repo.get_favourites_by_user("alice") == [alice_favourite]


# Test that removing a favourite makes it unavailable to later queries.
def test_remove_favourite(repo):
    user = User(1, "Alice", "password1")
    track = make_track()
    favourite = Favourite(1, user, track)
    repo.add_favourite(favourite)

    repo.remove_favourite(favourite)

    assert repo.get_favourite(user.user_name, track.track_id) is None
    assert repo.get_favourites_by_user(user.user_name) == []


# Test that the populated fixture loads all tracks from the test CSV files.
def test_populate_loads_test_tracks(in_memory_repo):
    assert in_memory_repo.get_number_of_tracks() == 10
    assert all(track.artist is not None for track in in_memory_repo.get_tracks())
