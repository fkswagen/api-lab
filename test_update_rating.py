import pytest


# Boundary values save only stars 1 through 5 and preserve refused updates.
@pytest.mark.parametrize(
    "stars, expected_status",
    [(0, 400), (1, 200), (5, 200), (6, 400)],
)
def test_update_rating_boundaries(
    api, auth, rating, stars, expected_status
):
    path = f"/api/ratings/{rating['id']}"
    response = api.put(path, json={"stars": stars}, headers=auth)
    assert response.status_code == expected_status

    current = api.get(path, headers=auth)
    assert current.status_code == 200
    expected_stars = stars if expected_status == 200 else 3
    assert current.json()["stars"] == expected_stars
