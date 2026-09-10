from music.adapters.memory_repository import MemoryRepository
from music.domainmodel.track import Track
from music.domainmodel.user import User
from music.favourite.services import FavouriteService


def create_repo():
    repo = MemoryRepository()

    user = User(1, "hameed", "password123")
    track = Track(10, "Test Track")

    repo.add_user(user)
    repo.add_track(track)

    return repo


def test_add_favourite():
    repo = create_repo()

    result = FavouriteService.register_favourite(
        "hameed",
        10,
        repo
    )

    assert result is True


def test_remove_favourite():
    repo = create_repo()

    FavouriteService.register_favourite(
        "hameed",
        10,
        repo
    )

    result = FavouriteService.remove_favourite(
        "hameed",
        10,
        repo
    )
#
    assert result is True