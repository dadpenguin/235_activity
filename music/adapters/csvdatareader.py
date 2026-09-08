import ast
import csv
import os

from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre
from music.domainmodel.track import Track

# Complete the implementation of the CSVDataReader class.
# The last five tests in tests/unit/test_domainmodel.py are currently expected
# to fail because the CSVDataReader has not yet been implemented.
# All five tests should pass once the implementation is complete.
# Use these tests to verify that the provided CSV files are read correctly.
    # pass

class CSVDataReader:

    def __init__(self, albums_file_name, tracks_file_name):
        self.albums_file_name = albums_file_name
        self.tracks_file_name = tracks_file_name

    def read_csv_files(self):
        with open(self.albums_file_name, 'r') as albums_file, open(self.tracks_file_name, 'r') as tracks_file:
            albums_reader = csv.reader(albums_file)
            tracks_reader = csv.reader(tracks_file)

            next(albums_reader)
            next(tracks_reader)

            albums_data = [row for row in albums_reader]
            tracks_data = [row for row in tracks_reader]


            albums = []
            for album in albums_data:
                try:
                    album_id = int(album[0])

                except (ValueError, TypeError, SyntaxError):
                    continue

                for item in albums:
                    if album_id == item.id:
                        break

                else:
                    try:
                        new_album = Album(album_id=int(album[0]), title=str(album[12]))

                    except (ValueError, TypeError, SyntaxError):
                        continue

                    try:
                        new_album.release_year = int(album[3])

                    except (ValueError, TypeError, SyntaxError):
                        new_album.release_year = None

                    try:
                        new_album.total_tracks = int(album[13])

                    except (ValueError, TypeError, SyntaxError):
                        new_album.total_tracks = None

                    albums.append(new_album)

            artists = []
            for artist in tracks_data:
                try:
                    artist_id = int(artist[4])

                except (ValueError, TypeError, SyntaxError):
                    continue

                for item in artists:
                    if artist_id == item.artist_id:
                        break

                else:
                    try:
                        new_artist = Artist(artist_id=int(artist[4]), full_name=artist[5])

                    except (ValueError, TypeError, SyntaxError):
                        continue

                    artists.append(new_artist)


            genres = []
            for genre in tracks_data:
                try:
                    genre_text = ast.literal_eval(genre[27])

                except (ValueError, TypeError, SyntaxError):
                    continue

                for genre_data in genre_text:
                    try:
                        genre_id = int(genre_data['genre_id'])

                    except (ValueError, TypeError, SyntaxError):
                        continue

                    for item in genres:
                        if genre_id == item.genre_id:
                            break

                    else:
                        try:
                            new_genre = Genre(genre_id=int(genre_data['genre_id']), genre_name=str(genre_data['genre_title']))

                        except (ValueError, TypeError, SyntaxError):
                            continue

                        genres.append(new_genre)


            tracks = []
            for track in tracks_data:
                try:
                    new_track = Track(track_id=int(track[0]), track_title=str(track[37]))

                except (ValueError, TypeError, SyntaxError):
                    continue

                try:
                    new_track.track_url = track[12]
                    new_track.track_duration = int(track[22])

                except(ValueError, TypeError, SyntaxError):
                    new_track.track_url = None

                try:
                    new_track.track_duration = int(track[22])

                except(ValueError, TypeError, SyntaxError):
                    new_track.track_duration = None

                try:
                    artist_id = int(track[4])

                    for artist in artists:
                        if artist_id == artist.artist_id:
                            new_track.artist = artist

                except (ValueError, TypeError, SyntaxError):
                    artist_id == None

                try:
                    album_id = int(track[1])

                    for album in albums:
                        if album_id == album.id:
                            new_track.album = album

                except (ValueError, TypeError, SyntaxError):
                    new_track.album == None

                try:
                    for genre in ast.literal_eval(track[27]):

                        genre_id = int(genre['genre_id'])

                        for genre2 in genres:
                            if genre_id == genre2.genre_id:
                                new_track.add_genre(genre2)

                except (ValueError, TypeError, SyntaxError):
                    new_track.add_genre(None)


                tracks.append(new_track)

            self.dataset_of_tracks = tracks
            self.dataset_of_albums = albums
            self.dataset_of_artists = artists
            self.dataset_of_genres = genres