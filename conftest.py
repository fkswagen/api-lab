import uuid

import pytest
import requests


SITE = "https://quickpizza.grafana.com"


class QuickPizza(requests.Session):
    """Session that prefixes relative paths with the QuickPizza address."""

    def request(self, method, url, *args, **kwargs):
        return super().request(method, SITE + url, *args, **kwargs)


@pytest.fixture(scope="session")
def api():
    """Keep one load-balancer session for the complete test run."""
    with QuickPizza() as session:
        yield session


def log_in_new_user(api):
    """Create a throwaway user, log in, and return its authorization header."""
    user = {
        "username": "lab-" + uuid.uuid4().hex[:12],
        "password": "Pizza-2026",
    }
    response = api.post("/api/users", json=user)
    assert response.status_code == 201

    response = api.post("/api/users/token/login", json=user)
    assert response.status_code == 200
    return {"Authorization": "token " + response.json()["token"]}


@pytest.fixture
def auth(api):
    """Return a fresh throwaway user's authorization header."""
    return log_in_new_user(api)


@pytest.fixture
def other_auth(api):
    """Return a second fresh throwaway user's authorization header."""
    return log_in_new_user(api)


@pytest.fixture
def pizza_id(api, auth):
    """Create a pizza for the current throwaway user and return its id."""
    response = api.post("/api/pizza", json={}, headers=auth)
    assert response.status_code == 200
    return response.json()["pizza"]["id"]


@pytest.fixture
def rating(api, auth, pizza_id):
    """Create one owned rating and remove it after the test."""
    response = api.post(
        "/api/ratings",
        json={"pizza_id": pizza_id, "stars": 3},
        headers=auth,
    )
    assert response.status_code == 201
    made = response.json()

    yield made

    api.delete(f"/api/ratings/{made['id']}", headers=auth)
