import os
from datetime import datetime

import pytest

from music.adapters.csvdatareader import CSVDataReader
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.favourite import Favourite
from music.domainmodel.genre import Genre
from music.domainmodel.review import Review
from music.domainmodel.track import Track
from music.domainmodel.user import User


class TestAlbum:

    @pytest.fixture
    def album(self):
        return Album(album_id=12, title="Ghost", release_year=1999, total_tracks=3)

    def test_album_construction(self, album):
        assert album.id == 12
        assert album.title == "Ghost"
        assert album.release_year == 1999
        assert album.total_tracks == 3

    def test_album_id_is_read_only(self, album):
        with pytest.raises(AttributeError):
            album.id = 13

    def test_album_title_setter(self, album):
        album.title = "Steve"
        assert album.title == "Steve"

    @pytest.mark.parametrize(
        "invalid_values", [2, "", None, 10.5, [], False]
    )
    def test_album_title_invalid_values(self, album, invalid_values):
        with pytest.raises(ValueError):
            album.title = invalid_values

    def test_album_release_year_setter(self, album):
        album.release_year = 2002
        assert album.release_year == 2002

    @pytest.mark.parametrize("invalid_years", [-2020, -1])
    def test_album_release_year_setter_invalid_value(
        self, album, invalid_years
    ):
        with pytest.raises(ValueError):
            album.release_year = invalid_years

    def test_album_total_tracks_setter(self, album):
        album.total_tracks = 6
        assert album.total_tracks == 6

    @pytest.mark.parametrize("invalid_track_values", [-2020, -5])
    def test_album_total_tracks_setter_invalid_value(
        self, album, invalid_track_values
    ):
        with pytest.raises(ValueError):
            album.total_tracks = invalid_track_values

    def test_album_repr(self, album):
        assert repr(album) == "<Album Ghost, album id = 12>"

    @pytest.mark.parametrize(
        "invalid_repr", ["", "Taylor Swift", "Album", "Album:"]
    )
    def test_album_repr_fail(self, album, invalid_repr):
        assert repr(album) != invalid_repr

    def test_album_eq_valid(self, album):
        album2 = Album(
            album_id=12, title="Ghost", release_year=1999, total_tracks=3
        )
        assert album == album2

    def test_album_eq_invalid(self, album):
        album2 = Album(
            album_id=14, title="Ghost", release_year=1999, total_tracks=3
        )
        assert album != album2

    def test_album_lt_valid(self, album):
        album2 = Album(
            album_id=10, title="Ghost", release_year=1999, total_tracks=3
        )
        assert album2 < album

    def test_album_lt_invalid_greater(self, album):
        album2 = Album(
            album_id=18, title="Ghost", release_year=1999, total_tracks=3
        )
        assert not (album2 < album)

    def test_album_lt_invalid_equals(self, album):
        album2 = Album(
            album_id=12, title="Ghost", release_year=1999, total_tracks=3
        )
        assert not (album2 < album)

    def test_album_hash(self, album):
        album2 = Album(
            album_id=12, title="Ghost", release_year=1999, total_tracks=3
        )
        assert hash(album2) == hash(album)

class TestReview:

    @pytest.fixture
    def review(self):

        return Review(
            review_id=6,
            user="Steve",
            track="Steve Tunes",
            rating=5,
            review_text="TUNES 10/10",
            timestamp=datetime(2026, 1, 1, 12, 0, 0),
        )

    def test_review_construction(self, review):
        assert review.id == 6
        assert review.user == "Steve"
        assert review.track == "Steve Tunes"
        assert review.rating == 5
        assert review.review_text == "TUNES 10/10"
        assert review.timestamp == datetime(2026, 1, 1, 12, 0, 0)

    def test_review_id_is_read_only(self, review):
        with pytest.raises(AttributeError):
            review.id = 13

    def test_review_rating_setter(self, review):
        review.rating = 4
        assert review.rating == 4

    @pytest.mark.parametrize("out_of_bounds_ratings", [-1, 0, 6, 11])
    def test_review_rating_setter_invalid_value(self, review, out_of_bounds_ratings):
        with pytest.raises(ValueError):
            review.rating = out_of_bounds_ratings

    @pytest.mark.parametrize("wrong_type_ratings", [True, "Taylor Swift", 4.5, None])
    def test_review_rating_setter_invalid_type(self, review, wrong_type_ratings):
        with pytest.raises(TypeError):
            review.rating = wrong_type_ratings

    def test_review_text_setter(self, review):
        review.review_text = "one tune two tunes"
        assert review.review_text == "one tune two tunes"

    @pytest.mark.parametrize(
        "empty_strings",
        [
            "         ",
            "",
            "\x20",
            "\t",
            "\n",
            "\r",
            "\v",
            "\f",
            "\ufeff",
            "\u200d",
            "\u200c",
            "\u200b",
        ],
    )
    def test_review_text_setter_empty_value(self, review, empty_strings):
        with pytest.raises(ValueError):
            review.review_text = empty_strings

    @pytest.mark.parametrize("wrong_types", [-1, 11, True, None, 4.5])
    def test_review_text_setter_invalid_type(self, review, wrong_types):
        with pytest.raises(TypeError):
            review.review_text = wrong_types

    def test_review_default_timestamp(self):

        r = Review(6, "Steve", "Steve Tunes", 5, "Great")
        assert isinstance(r.timestamp, datetime)

    def test_review_repr(self, review):
        assert repr(review) == "<Review user=Steve rating=5 id=6>"

    @pytest.mark.parametrize(
        "invalid_review_repr", ["", "Taylor Swift", "Review", "Review:"]
    )
    def test_review_repr_fail(self, review, invalid_review_repr):
        assert repr(review) != invalid_review_repr

    def test_review_eq_valid(self, review):
        review2 = Review(
            review_id=6,
            user="Steve",
            track="Steve Tunes",
            rating=5,
            review_text="Different text",
            timestamp=None,
        )
        assert review == review2

    def test_review_eq_invalid(self, review):
        review2 = Review(
            review_id=4,
            user="Steve",
            track="Steve Tunes",
            rating=5,
            review_text="TUNES 10/10",
            timestamp=review.timestamp,
        )
        assert review != review2

    def test_review_lt(self, review):

        review2 = Review(
            review_id=4,
            user="Steve",
            track="Steve Tunes",
            rating=5,
            review_text="TUNES 10/10",
            timestamp=review.timestamp,
        )
        assert review2 < review

    def test_review_lt_invalid_greater(self, review):
        # Same timestamp, higher ID -> review2 is NOT less than review
        review2 = Review(
            review_id=8,
            user="Steve",
            track="Steve Tunes",
            rating=5,
            review_text="TUNES 10/10",
            timestamp=review.timestamp,
        )
        assert not (review2 < review)

    def test_review_lt_invalid_equals(self, review):
        review2 = Review(
            review_id=6,
            user="Steve",
            track="Steve Tunes",
            rating=5,
            review_text="TUNES 10/10",
            timestamp=review.timestamp,
        )
        assert not (review2 < review)

    def test_review_hash(self, review):
        review2 = Review(
            review_id=6,
            user="Steve",
            track="Steve Tunes",
            rating=5,
            review_text="TUNES 10/10",
            timestamp=None,
        )
        assert hash(review2) == hash(review)

class TestFavourite:

    @pytest.fixture
    def favourite(self):
        # Uses positional args / 'id' parameter matching your original __init__(self, id, user, track)
        return Favourite(3, "Steve", "Steve Tunes")

    def test_favourite_construction(self, favourite):
        assert favourite.id == 3
        assert favourite.user == "Steve"
        assert favourite.track == "Steve Tunes"

    def test_favourite_id_is_read_only(self, favourite):
        with pytest.raises(AttributeError):
            favourite.id = 13

    def test_favourite_user_property(self, favourite):
        assert favourite.user == "Steve"

    def test_favourite_track_property(self, favourite):
        assert favourite.track == "Steve Tunes"

    def test_favourite_repr(self, favourite):
        # Matches your exact __repr__ format: f"<Favourite - {self.track} ,user = {self.user} ,favourite_id = {self.id}"
        assert repr(favourite) == "<Favourite - Steve Tunes ,user = Steve ,favourite_id = 3>"

    @pytest.mark.parametrize("invalid_favourite_repr", ["", "Taylor Swift", "Favourite", "Favourite:"])
    def test_favourite_repr_fail(self, favourite, invalid_favourite_repr):
        assert repr(favourite) != invalid_favourite_repr

    def test_favourite_eq_valid(self, favourite):
        favourite2 = Favourite(3, "Steve", "Steve Tunes")
        assert favourite == favourite2

    def test_favourite_eq_invalid(self, favourite):
        favourite2 = Favourite(1, "Steve", "Steve Tunes")
        assert favourite != favourite2

    def test_favourite_lt(self, favourite):
        favourite2 = Favourite(1, "Steve", "Steve Tunes")
        assert favourite2 < favourite

    def test_favourite_lt_invalid_greater(self, favourite):
        favourite2 = Favourite(10, "Steve", "Steve Tunes")
        assert not (favourite2 < favourite)

    def test_favourite_lt_invalid_equals(self, favourite):
        favourite2 = Favourite(3, "Steve", "Steve Tunes")
        assert not (favourite2 < favourite)

    def test_favourite_hash(self, favourite):
        favourite2 = Favourite(3, "Steve", "Steve Tunes")
        assert hash(favourite2) == hash(favourite)

class TestArtist:

    def test_construction(self):
        artist1 = Artist(1, 'Tailor Swift')
        assert str(artist1) == "<Artist Tailor Swift, artist id = 1>"
        artist2 = Artist(2, "Maroon 5")
        assert str(artist2) == '<Artist Maroon 5, artist id = 2>'
        artist3 = Artist(3, 'Kate Bush')
        assert str(artist3) == '<Artist Kate Bush, artist id = 3>'

        # Test full_name with trailing spaces
        artist4 = Artist(4, ' Bad Bunny ')
        assert str(artist4) == '<Artist Bad Bunny, artist id = 4>'

        # Test when the id is None
        with pytest.raises(ValueError):
            Artist(None, 'Harry Styles')

        # Test when the id is negative
        with pytest.raises(ValueError):
            Artist(-3, 'Harry Styles')

        # full_name is a required field -> invalid type raises, not None
        with pytest.raises(ValueError):
            Artist(5, 2910)

    def test_setters(self):
        artist1 = Artist(1, 'Tailor Swift')

        # Test full_name setter
        artist1.full_name = '  Tailor Fixed  '
        assert artist1.full_name == 'Tailor Fixed'
        assert str(artist1) == '<Artist Tailor Fixed, artist id = 1>'

        # full_name is required -> invalid type raises
        with pytest.raises(ValueError):
            artist1.full_name = 32
        assert artist1.full_name == 'Tailor Fixed'

        with pytest.raises(ValueError):
            artist1.full_name = '   '
        assert artist1.full_name == 'Tailor Fixed'

    def test_equality(self):
        artist1 = Artist(1, 'Tailor Swift')
        artist2 = Artist(2, "Maroon 5")
        artist3 = Artist(3, 'Kate Bush')
        artist3_copy = Artist(3, 'Kate Bush')

        # Check equality of the same artists
        assert artist1 == artist1
        assert artist2 == artist2
        assert artist3 == artist3
        assert artist3 == artist3_copy

        # Check inequality of different artists
        assert artist1 != artist2
        assert artist1 != artist3
        assert artist2 != artist3

        # Check equality with different types
        assert artist1 != 'Tailor Swift'
        assert artist1 is not None

    def test_sorting(self):
        artist1 = Artist(2, 'Tailor Swift')
        artist2 = Artist(5, "Maroon 5")
        artist3 = Artist(8, 'Kate Bush')

        # Basic inequality comparison
        assert artist1 < artist2
        assert artist2 < artist3
        assert artist3 > artist1

        # Test actual sorting of the list of artists
        artist_list = [artist3, artist2, artist1]
        assert sorted(artist_list) == [artist1, artist2, artist3]

    def test_set(self):
        artist1 = Artist(1, 'Tailor Swift')
        artist2 = Artist(3, "Maroon 5")
        artist3 = Artist(8, 'Kate Bush')

        artist_set = set()
        # Test addition
        artist_set.add(artist1)
        artist_set.add(artist2)
        artist_set.add(artist3)

        assert sorted(artist_set) == [artist1, artist2, artist3]

        # Test removal
        artist_set.discard(artist1)
        assert sorted(artist_set) == [artist2, artist3]


class TestGenre:

    def test_construction(self):
        genre1 = Genre(1, 'Jazz ')
        genre2 = Genre(2, ' Electronic ')

        assert str(genre1) == '<Genre Jazz, genre id = 1>'
        assert str(genre2) == '<Genre Electronic, genre id = 2>'

        # Test invalid id raises error
        with pytest.raises(ValueError):
            Genre('abc', 'Chill')

        # Test invalid id raises error
        with pytest.raises(ValueError):
            Genre(-30, 'Chill')

        # name is a required field -> invalid type raises
        with pytest.raises(ValueError):
            Genre(3, 300)

    def test_setters(self):
        genre1 = Genre(1, 'Jazz')

        assert genre1.genre_id == 1

        genre1.name = 'New Jazz'
        assert genre1.name == 'New Jazz'

        # Invalid type assignment raises and leaves the value untouched
        with pytest.raises(ValueError):
            genre1.name = 100
        assert genre1.name == 'New Jazz'

        # Empty string assignment raises and leaves the value untouched
        with pytest.raises(ValueError):
            genre1.name = ''
        assert genre1.name == 'New Jazz'

    def test_equality(self):
        genre1 = Genre(1, 'Jazz')
        genre2 = Genre(2, 'Electronic')
        genre3 = Genre(5, 'Electronic')

        assert genre1 == genre1
        assert genre1 != genre2
        assert genre2 != genre3

        assert genre1 != 'Jazz'
        assert genre2 != 105

    def test_sorting(self):
        genre1 = Genre(1, 'Jazz')
        genre2 = Genre(2, 'Electronic')
        genre3 = Genre(8, 'Latin')

        assert genre1 < genre2
        assert genre2 < genre3
        assert genre3 > genre1

        genre_list = [genre3, genre2, genre1]
        assert sorted(genre_list) == [genre1, genre2, genre3]

    def test_set(self):
        genre1 = Genre(1, 'Jazz')
        genre2 = Genre(2, 'Electronic')
        genre3 = Genre(8, 'Latin')

        genre_set = set()
        genre_set.add(genre1)
        genre_set.add(genre2)
        genre_set.add(genre3)

        assert sorted(genre_set) == [genre1, genre2, genre3]

        genre_set.discard(genre2)
        genre_set.discard(genre1)
        assert sorted(genre_set) == [genre3]


class TestTrack:

    def test_construction(self):
        track1 = Track(1, 'As it Was ')
        track2 = Track(2, ' Heat Waves')
        track3 = Track(3, ' Tarot ')

        assert str(track1) == '<Track As it Was, track id = 1>'
        assert str(track2) == '<Track Heat Waves, track id = 2>'
        assert str(track3) == '<Track Tarot, track id = 3>'

        # Test if id of wrong type raises error
        with pytest.raises(ValueError):
            Track(None, 'Te Felicito')

        # Test negative value of id raises error
        with pytest.raises(ValueError):
            Track(-1, 'Te Felicito')

        # title is a required field -> invalid type raises, not None
        with pytest.raises(ValueError):
            Track(5, 32)

    def test_attributes(self):
        track1 = Track(1, 'Shivers')

        # Test title setter
        track1.title = 'Fixed Shivers'
        assert track1.title == 'Fixed Shivers'

        # Title with trailing spaces
        track1.title = '  Fixed Shivers2   '
        assert track1.title == 'Fixed Shivers2'

        # Test track_url
        track1.track_url = ' https://spotify/track/1 '
        assert track1.track_url == 'https://spotify/track/1'

        # track_url is optional -> None is a valid value
        track1.track_url = None
        assert track1.track_url is None

        # Test track duration
        track1.track_duration = 300
        assert track1.track_duration == 300

        # track_duration is optional -> None is a valid value
        track1.track_duration = None
        assert track1.track_duration is None

        artist = Artist(31, 'Justin Bieber')
        # Test artist attribute
        track1.artist = artist
        assert track1.artist == artist

        # artist is optional -> None is a valid value
        track1.artist = None
        assert track1.artist is None

    def test_attributes_fail(self):
        track1 = Track(1, 'Shivers')
        track2 = Track(2, 'Heat Waves')

        with pytest.raises(ValueError):
            track1.track_url = 23
        assert track1.track_url is None

        # title is required -> invalid type raises
        with pytest.raises(ValueError):
            track1.title = 1256
        assert track1.title == 'Shivers'

        with pytest.raises(ValueError):
            track1.title = ''
        assert track1.title == 'Shivers'

        with pytest.raises(ValueError):
            track1.track_duration = '300 seconds'

        with pytest.raises(ValueError):
            track2.track_duration = -20

        assert track1.track_duration is None
        assert track2.track_duration is None

        # Assigning artist of invalid type raises; value stays None
        with pytest.raises(ValueError):
            track1.artist = 3235
        with pytest.raises(ValueError):
            track2.artist = 'invalid artist'
        assert track1.artist is None
        assert track2.artist is None

        # Assigning album of invalid type raises; value stays None
        with pytest.raises(ValueError):
            track1.album = 1983
        with pytest.raises(ValueError):
            track2.album = 'Invalid album'
        assert track1.album is None
        assert track2.album is None

    def test_genre_methods(self):
        track1 = Track(1, 'Shivers')
        genre1 = Genre(10, 'Jazz')
        genre2 = Genre(11, 'Clasical')

        track1.add_genre(genre1)
        track1.add_genre(genre2)
        assert track1.genres == [genre1, genre2]

        # Should do nothing
        track1.add_genre('32')
        assert track1.genres == [genre1, genre2]

    def test_equality(self):
        track1 = Track(1, 'Shivers')
        track2 = Track(2, 'Heat Waves')
        track3 = Track(3, 'Bad Habit')

        assert track1 == track1
        assert track2 == track2
        assert track1 != track2
        assert track1 != track3

        assert track2 != 30
        assert track3 != 'Bad Habit'

    def test_sorting(self):
        track1 = Track(1, 'Shivers')
        track2 = Track(8, 'Heat Waves')
        track3 = Track(10, 'Bad Habit')

        assert track1 < track2
        assert track2 < track3
        assert track3 > track1

        track_list = [track3, track1, track2, track1]
        assert sorted(track_list) == [track1, track1, track2, track3]

    def test_set(self):
        track1 = Track(1, 'Shivers')
        track2 = Track(8, 'Heat Waves')
        track3 = Track(10, 'Bad Habit')

        track_set = set()
        track_set.add(track1)
        track_set.add(track2)
        track_set.add(track3)

        assert len(track_set) == 3

        track_set.discard(track1)
        assert sorted(track_set) == [track2, track3]

        track_set.discard(track2)
        track_set.discard(track3)
        assert len(track_set) == 0


class TestUser:

    def test_construction(self):
        user1 = User(7231, 'amotys', 'amotys277')
        user2 = User(9137, '  yunwi5  ', 'urrabbit978')

        assert str(user1) == '<User amotys, user id = 7231>'
        assert str(user2) == '<User yunwi5, user id = 9137>'

        # Invalid ID type raises error
        with pytest.raises(ValueError):
            User('invalid id', 'pedri', 'pedri1928')

        # ID less than 0 raises error
        with pytest.raises(ValueError):
            User(-10, 'peri', 'pedri1928')

        # Test user_name is all lowercase
        user3 = User(3829, ' GAVI ', 'gavi1928')
        assert user3.user_name == 'gavi'

        # user_name is required -> invalid type raises
        with pytest.raises(ValueError):
            User(8190, 1259, 'memphis212')

        # password is required -> invalid type raises
        with pytest.raises(ValueError):
            User(6737, 'Memphis', 325)

        # password is required -> empty string raises
        with pytest.raises(ValueError):
            User(9821, 'Memphis', '')

        # password length < 7 raises
        with pytest.raises(ValueError):
            User(6878, 'memphis', 'mempi')

        # Password of length 7 constructs correctly
        user6 = User(2918, 'Memphis', 'mempi12')
        assert user6.password == 'mempi12'

    # User class has getters for each attribute, but no setters.
    def test_attributes(self):
        user1 = User(7231, '  AMOTYS  ', 'amotys277')
        assert user1.user_id == 7231
        assert user1.user_name == 'amotys'
        assert user1.password == 'amotys277'

    def test_attributes_fail(self):
        user1 = User(7231, '  LEOROSE  ', 'LEOROSE277')

        with pytest.raises(AttributeError):
            user1.user_name = 'changed'

        with pytest.raises(AttributeError):
            user1.user_id = 1232

        with pytest.raises(AttributeError):
            user1.password = 'asdfe'

    def test_equality(self):
        user1 = User(2231, 'amotys', 'amotys277')
        user1_copy = User(2231, 'amotys', 'amotys277')
        user2 = User(7232, 'gavi', 'gavi9281')
        user3 = User(9300, 'phil', 'phi8901')

        assert user1 == user1_copy
        assert user1 != user2
        assert user2 != user3

        # Check equality with different types
        track1 = Track(2231, 'Chill with me')
        assert user1 != track1
        assert user1 != 'some user'
        assert user2 != 7120
        assert user3 is not None

    def test_sorting(self):
        user1 = User(2231, 'amotys', 'amotys277')
        user2 = User(7232, 'gavi', 'gavi9281')
        user3 = User(9300, 'phil', 'phi8901')

        assert user1 < user2
        assert user2 < user3
        assert user3 > user1

        user_list = [user3, user2, user1, user2]
        assert sorted(user_list) == [user1, user2, user2, user3]

    def test_set(self):
        user1 = User(2231, 'amotys', 'amotys277')
        user2 = User(7232, 'gavi', 'gavi9281')
        user3 = User(9300, 'phil', 'phi8901')

        user_set = set()
        user_set.add(user1)
        user_set.add(user2)
        user_set.add(user3)

        # Test all users were added to the set
        assert sorted(user_set) == [user1, user2, user3]

        # Test users are successfully removed from the set.
        user_set.discard(user1)
        user_set.discard(user2)
        assert list(user_set) == [user3]


def create_csv_reader():
    dirname = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # # Test dataset location
    # albums_file_name = os.path.join(dirname, 'data/raw_albums_test.csv')
    # tracks_file_name = os.path.join(dirname, 'data/raw_tracks_test.csv')

    # Real dataset location
    albums_file_name = os.path.join(dirname, '../music/adapters/data/raw_albums_excerpt.csv')
    tracks_file_name = os.path.join(dirname, '../music/adapters/data/raw_tracks_excerpt.csv')

    reader = CSVDataReader(albums_file_name, tracks_file_name)
    reader.read_csv_files()
    return reader


class TestCSVDataReader:

    def test_csv_reader(self):
        reader = create_csv_reader()

        assert len(reader.dataset_of_tracks) == 2000
        assert len(reader.dataset_of_artists) == 263
        assert len(reader.dataset_of_albums) == 427
        assert len(reader.dataset_of_genres) == 60

    def test_tracks_dataset(self):
        reader = create_csv_reader()
        tracks = reader.dataset_of_tracks

        sorted_tracks = sorted(tracks)
        # Test there are total 10 unique tracks in the test dataset // 2000 in real dataset.
        assert len(sorted_tracks) == 2000

        sorted_tracks_str = str(sorted_tracks[:3])
        assert sorted_tracks_str == '[<Track Food, track id = 2>, <Track Electric Ave, track id = 3>, <Track This World, track id = 5>]'

        # Test all tracks have artists
        tracks_no_artists = list(
            filter(lambda track: track.artist is None, tracks))
        assert len(tracks_no_artists) == 0

    def test_albums_dataset(self):
        reader = create_csv_reader()
        albums_set = reader.dataset_of_albums
        sorted_albums = sorted(albums_set)

        # Test there are total 5 unique albums in the test dataset // 427 in real dataset.
        assert len(sorted_albums) == 427

        sorted_albums_sample = str(sorted_albums[:3])
        assert sorted_albums_sample == '[<Album AWOL - A Way Of Life, album id = 1>, <Album Niris, album id = 4>, <Album Constant Hitmaker, album id = 6>]'

    def test_artists_dataset(self):
        reader = create_csv_reader()
        artists_set = reader.dataset_of_artists
        sorted_artists = sorted(artists_set)

        # Test there are total 5 unique artists in the test dataset // 263 in real dataset.
        assert len(sorted_artists) == 263

        sorted_artists_sample = str(sorted_artists[:3])
        assert sorted_artists_sample == '[<Artist AWOL, artist id = 1>, <Artist Nicky Cook, artist id = 4>, <Artist Kurt Vile, artist id = 6>]'

    def test_genres_dataset(self):
        reader = create_csv_reader()
        genres_set = reader.dataset_of_genres

        sorted_genres = sorted(genres_set)

        # Test there are total 7 unique genres in the test dataset // 60 in real dataset.
        assert len(sorted_genres) == 60

        sorted_genre_sample = str(sorted_genres[:3])
        assert sorted_genre_sample == '[<Genre Avant-Garde, genre id = 1>, <Genre International, genre id = 2>, <Genre Blues, genre id = 3>]'
