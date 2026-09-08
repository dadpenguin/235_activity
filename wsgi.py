"""App entry point."""
from music import create_app
from music.adapters.memory_repository import MemoryRepository, populate
from flask import Flask, render_template, redirect, url_for, request
from music.domainmodel.favourite import Favourite
from music.domainmodel.user import User

app = create_app()
repo = MemoryRepository()
populate("music/adapters/data", repo)

@app.route('/')
def index():
    name = 'steve'
    return render_template('simple_track.html', name = name)

@app.route('/track/<int:track_id>')
def track_detail(track_id: int):
    track = repo.get_track(track_id)
    favourited = False

    for favourite in repo.get_favourites_by_user("Steve"):
        if favourite.track.track_id == track_id:
            favourited = True
            break

    total_rating = 0
    average_rating = 0
    if not track:
        return "Track not found", 404

    reviews = repo.get_reviews_by_track(track_id)
    for review in reviews:
        total_rating += review.rating
        average_rating = total_rating / len(reviews)
    return render_template('track_detail.html', track=track, reviews=reviews, average_rating=average_rating, track_id = track_id, favourited=favourited)


@app.route('/search/<type>/<keyword>')
def search(type: str, keyword: str):
    if request.args.get('keyword') != None:
        keyword = request.args.get('keyword')
        return redirect(url_for('search', type = type, keyword = keyword))

    results = []

    if type not in ['all', 'title', 'album', 'genre', 'artist']:
        return redirect(url_for('search', type = 'all', keyword='track'))

    if type == 'all':
        for track in repo.get_tracks():
            if track.title and keyword.lower() in track.title.lower() and track.title not in results:
                results.append(track.title)

            for genre in track.genres:
                if genre.name and keyword.lower() in genre.name.lower() and genre.name not in results:
                    results.append(genre.name)

            if track.album and keyword.lower() in track.album.title.lower() and track.album.title not in results:
                results.append(track.album.title)

            if track.artist and keyword.lower() in track.artist.full_name.lower() and track.artist.full_name not in results:
                results.append(track.artist.full_name)

    elif type == 'title':
        for track in repo.get_tracks():
            if track.title and keyword.lower() in track.title.lower() and track.title not in results:
                results.append(track.title)

    elif type == 'album':
        for track in repo.get_tracks():
            if track.album and keyword.lower() in track.album.title.lower() and track.album.title not in results:
                results.append(track.album.title)

    elif type == 'artist':
        for track in repo.get_tracks():
            if track.artist and keyword.lower() in track.artist.full_name.lower() and track.artist.full_name not in results:
                results.append(track.artist.full_name)

    elif type == 'genre':
        for track in repo.get_tracks():
            for genre in track.genres:
                if genre and keyword.lower() in genre.name.lower() and genre.name not in results:
                    results.append(genre.name)


    return render_template('search.html', results = results, keyword = keyword)

@app.route('/favourite/<int:track_id>')
def favourite(track_id: int):

    new_track = repo.get_track(track_id)
    new_user = User(user_id = 300, user_name = 'Steve', password = 'password123')
    repo.add_user(new_user)
    favourite = Favourite(favourite_id = track_id, user = new_user, track = new_track)
    repo.add_favourite(favourite)

    return redirect(url_for('track_detail', track_id = track_id))

@app.route('/unfavourite/<int:track_id>')
def unfavourite(track_id: int):

    for favourite in repo.get_favourites_by_user("Steve"):
        if favourite.track.track_id == track_id:
            not_favourite = Favourite(favourite_id=track_id, user = "Steve", track = repo.get_track(track_id))

    repo.remove_favourite(not_favourite)

    return redirect(url_for('track_detail', track_id = track_id))

if __name__ == "__main__":
    app.run(host='localhost', port=5000, threaded=False, Debug = True)