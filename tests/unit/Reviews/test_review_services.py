import sys
import types

import pytest

from music.adapters.memory_repository import MemoryRepository
from music.domainmodel.track import Track

import utils.user


fake_exceptions = types.ModuleType("music.track.exceptions")


class TrackNotFound(Exception):
    pass


fake_exceptions.TrackNotFound = TrackNotFound
sys.modules["music.track.exceptions"] = fake_exceptions


utils.user.generate_random_review_id = lambda: 1234


from music.review.services import ReviewService

#
def create_repo_with_track():
    repo = MemoryRepository()

    track = Track(
        track_id=10,
        track_title="Test Track"
    )

    repo.add_track(track)

    return repo, track


def test_create_review_success():
    repo, track = create_repo_with_track()

    review = ReviewService.create_review(
        repo=repo,
        user_name="hameed",
        track_id=10,
        stars=5,
        paragraph="Great track"
    )

    assert review is not None
    assert review.user == "hameed"
    assert review.track == track
    assert review.rating == 5
    assert review.review_text == "Great track"


def test_create_review_adds_review_to_repository():
    repo, track = create_repo_with_track()

    review = ReviewService.create_review(
        repo=repo,
        user_name="hameed",
        track_id=10,
        stars=4,
        paragraph="Very good"
    )

    reviews = repo.get_reviews_by_track(10)

    assert len(reviews) == 1
    assert reviews[0] == review


def test_create_review_track_not_found():
    repo = MemoryRepository()

    with pytest.raises(TrackNotFound):
        ReviewService.create_review(
            repo=repo,
            user_name="hameed",
            track_id=999,
            stars=5,
            paragraph="Great track"
        )


def test_create_review_stores_correct_track():
    repo, track = create_repo_with_track()

    review = ReviewService.create_review(
        repo=repo,
        user_name="hameed",
        track_id=10,
        stars=3,
        paragraph="It was okay"
    )

    assert review.track.track_id == 10


def test_create_review_stores_correct_rating():
    repo, track = create_repo_with_track()

    review = ReviewService.create_review(
        repo=repo,
        user_name="hameed",
        track_id=10,
        stars=4,
        paragraph="Good song"
    )

    assert review.rating == 4


def test_create_review_stores_review_text():
    repo, track = create_repo_with_track()

    review = ReviewService.create_review(
        repo=repo,
        user_name="hameed",
        track_id=10,
        stars=5,
        paragraph="Excellent song"
    )

    assert review.review_text == "Excellent song"