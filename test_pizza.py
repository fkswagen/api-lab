import requests


SITE = "https://quickpizza.grafana.com"
AUTH = {"Authorization": "token abcdef0123456789"}
VEGETARIAN = {"mustBeVegetarian": True}


# A vegetarian request returns a named pizza with vegetarian ingredients only.
def test_vegetarian_pizza():
    response = requests.post(
        SITE + "/api/pizza", json=VEGETARIAN, headers=AUTH
    )
    assert response.status_code == 200
    pizza = response.json()["pizza"]
    assert pizza["name"] != ""
    assert all(ingredient["vegetarian"] for ingredient in pizza["ingredients"])


# A pizza request without a token is refused with the authentication error.
def test_pizza_without_token_is_refused():
    response = requests.post(SITE + "/api/pizza", json=VEGETARIAN)
    assert response.status_code == 401
    assert response.json() == {"error": "authentication failed"}
