import requests


SITE = "https://quickpizza.grafana.com"
MADE_UP_AUTH = {"Authorization": "token 0000000000000000"}


# A made-up token is read-only in this suite and must not be used for mutations.
def test_made_up_token_can_read_ratings():
    response = requests.get(SITE + "/api/ratings", headers=MADE_UP_AUTH)
    assert response.status_code == 200
    assert isinstance(response.json()["ratings"], list)
