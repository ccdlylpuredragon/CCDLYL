import pytest

from app import app, db


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.app_context():
        db.create_all()
        with app.test_client() as client:
            yield client
        db.drop_all()


def test_index(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert "CCDLYL".encode() in resp.data


def test_register_page(client):
    resp = client.get("/register")
    assert resp.status_code == 200


def test_register_user(client):
    resp = client.post("/register", data={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123",
        "confirm_password": "password123",
    }, follow_redirects=True)
    assert resp.status_code == 200
    assert "testuser".encode() in resp.data


def test_register_duplicate_user(client):
    data = {
        "username": "dup",
        "email": "dup@example.com",
        "password": "password123",
        "confirm_password": "password123",
    }
    client.post("/register", data=data, follow_redirects=True)
    resp = client.post("/register", data=data, follow_redirects=True)
    assert resp.status_code == 200


def test_upload_page(client):
    resp = client.get("/upload")
    assert resp.status_code == 200


def test_admin_page(client):
    resp = client.get("/admin")
    assert resp.status_code == 200
