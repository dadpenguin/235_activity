import os
import csv
import ast


from music.domainmodel.artist import Artist
from music.domainmodel.album import Album
from music.domainmodel.track import Track
from music.domainmodel.genre import Genre


# Complete the implementation of the CSVDataReader class.
# The last five tests in tests/unit/test_domainmodel.py are currently expected
# to fail because the CSVDataReader has not yet been implemented.
# All five tests should pass once the implementation is complete.
# Use these tests to verify that the provided CSV files are read correctly.
    # pass

class CSVDataReader:

    def __init__(self, albums_file_name, tracks_file_name):
        # CSV file paths + datasets
        self.__tracks_file_name = tracks_file_name
        self.__albums_file_name = albums_file_name

        self.__dataset_of_tracks = []
        self.__dataset_of_artists = []
        self.__dataset_of_albums = []
        self.__dataset_of_genres = []

        self.__albums_by_id = {}
        self.__artists_by_id = {}
        self.__genres_by_id = {}
        self.__tracks_by_id = {}

    # Properties
    @property
    def dataset_of_tracks(self):
        return self.__dataset_of_tracks

    @property
    def dataset_of_artists(self):
        return self.__dataset_of_artists

    @property
    def dataset_of_albums(self):
        return self.__dataset_of_albums

    @property
    def dataset_of_genres(self):
        return self.__dataset_of_genres

    # Public Method: Read both CSV files and fill all datasets.
    def read_csv_files(self):
        self._read_albums_file()
        self._read_tracks_file()

    # Create Album Objects
    def _read_albums_file(self):
        with open(
                self.__albums_file_name,
                mode="r",
                encoding="latin1",
                newline=""
        ) as albums_file:

            reader = csv.DictReader(albums_file)
            for row in reader:
                album = self._create_album_from_row(row)
                self.__dataset_of_albums.append(album)
                self.__albums_by_id[album.id] = album

    def _create_album_from_row(self, row):
        # csv file row title: album_id,album_comments,album_date_created,album_year_released,album_engineer,album_favorites,album_handle,album_image_file,album_images,album_information,album_listens,album_producer,album_title,album_tracks,album_type,album_url,artist_name,artist_url,tags
        album_id = int(row["album_id"])
        album_title = row["album_title"]
        album_release_year = (
            int(row["album_year_released"])
            if row["album_year_released"] else None
        )
        album_total_tracks = (
            int(row["album_tracks"])
            if row["album_tracks"] else None
        )
        album = Album(
                    album_id,
                    album_title,
                    album_release_year,
                    album_total_tracks)
        return album


    # Create Track Objects
    def _read_tracks_file(self):
        with open(
                self.__tracks_file_name,
                mode="r",
                encoding="latin1",
                newline=""
        ) as albums_file:

            reader = csv.DictReader(albums_file)

            for row in reader:
                # Create Artist Object
                artist_id = int(row["artist_id"])
                if artist_id not in self.__artists_by_id:
                    artist = Artist(artist_id, row["artist_name"])
                    self.__artists_by_id[artist_id] = artist
                    self.__dataset_of_artists.append(artist)
                else:
                    artist = self.__artists_by_id[artist_id]

                # Create Album Object
                album = (
                    self.__albums_by_id.get(int(row["album_id"]))
                    if row["album_id"] else None
                )

                # Create Track Object
                track = Track(
                    int(row["track_id"]),
                    row["track_title"]
                )
                track.artist = artist
                track.album = album
                track.track_url = row["track_url"] or None
                track.track_duration = (
                    int(float(row["track_duration"]))
                    if row["track_duration"] else None
                )

                # Create Genre Objects
                genre_rows = ast.literal_eval(row["track_genres"] or "[]")
                for genre_row in genre_rows:
                    genre_id = int(genre_row["genre_id"])

                    if genre_id not in self.__genres_by_id:
                        genre = Genre(genre_id, genre_row["genre_title"])
                        self.__genres_by_id[genre_id] = genre
                        self.__dataset_of_genres.append(genre)
                    else:
                        genre = self.__genres_by_id[genre_id]

                    track.add_genre(genre)

                # Add track
                self.__dataset_of_tracks.append(track)

