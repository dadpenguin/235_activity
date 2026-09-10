def login_test_user(client):
    with client.session_transaction() as session:
        session['user_name'] = 'thorke'


def test_favourites_page_requires_login(client):
    response = client.get('/favourite/favourites')

    assert response.status_code == 302
    assert '/authentication/login' in response.headers['Location']


def test_favourites_page_loads_when_logged_in(client):
    login_test_user(client)

    response = client.get('/favourite/favourites')

    assert response.status_code == 200


def test_favourites_page_contains_heading(client):
    login_test_user(client)

    response = client.get('/favourite/favourites')

    assert response.status_code == 200
    assert b'My Favourites' in response.data


def test_favourites_page_empty_message(client):
    login_test_user(client)

    response = client.get('/favourite/favourites')

    assert response.status_code == 200
    assert b'No favourites yet' in response.data