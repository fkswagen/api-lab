import requests


SITE = "https://quickpizza.grafana.com"
AUTH = {"Authorization": "token abcdef0123456789"}


# The tools endpoint returns all three pizza-cutting tools.
def test_tools_are_listed():
    response = requests.get(SITE + "/api/tools", headers=AUTH)
    assert response.status_code == 200
    assert response.json() == {
        "tools": ["Knife", "Pizza cutter", "Scissors"]
    }
