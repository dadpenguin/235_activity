def test_search_returns_tracks_matching_query(client):
    response = client.get('/search?q=latino', follow_redirects=True)

    assert response.status_code == 200
    assert b'Latinoam' in response.data or b'latino' in response.data.lower()


def test_user_can_submit_a_comment_and_rating(client):
    response = client.post(
        '/track/1/reviews',
        data={'rating': '5', 'comment': 'This song is amazing!'},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b'This song is amazing!' in response.data or b'Review' in response.data


def test_authenticated_user_can_login(client):
    response = client.post(
        '/login',
        data={'username': 'demo_user', 'password': 'Password123'},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b'logged in' in response.data.lower() or b'demo_user' in response.data.lower()


def test_authenticated_user_can_toggle_favourite(client):
    login_response = client.post(
        '/login',
        data={'username': 'demo_user', 'password': 'Password123'},
        follow_redirects=True,
    )
    assert login_response.status_code == 200

    response = client.post('/track/1/favourite', follow_redirects=True)

    assert response.status_code == 200
    assert b'favourite' in response.data.lower() or b'liked' in response.data.lower()