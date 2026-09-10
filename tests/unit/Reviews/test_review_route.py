from pathlib import Path

import pytest
from music import create_app


TEST_DATA_PATH = Path(__file__).resolve().parents[2] / "data"


@pytest.fixture
def client():
    app = create_app({
        "TESTING": True,
        "TEST_DATA_PATH": TEST_DATA_PATH,
        "SECRET_KEY": "test-secret-key"
    })
    return app.test_client()


def test_review_page_loads(client):
    with client.session_transaction() as session:
        session["user_name"] = "hameed"

    response = client.get("/review/make/1")

    assert response.status_code == 200


def test_review_page_not_found(client):
    with client.session_transaction() as session:
        session["user_name"] = "hameed"

    response = client.get("/review/not-a-page")

    assert response.status_code == 404