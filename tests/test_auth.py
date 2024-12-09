import pytest
from app.models.user import User
from app import db


def test_register_route(client):
    resp = client.post(
        "/register", data={"username": "newuser", "password": "password123"}
    )
    assert resp.status_code in [200, 302]


def test_login_route(client):
    resp = client.post(
        "/login", data={"username": "testuser", "password": "password123"}
    )
    assert resp.status_code in [200, 302]


def test_logout_route(client):
    client.post("/login", data={"username": "testuser", "password": "password123"})
    resp = client.get("/logout")
    assert resp.status_code in [200, 302]
