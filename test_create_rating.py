import pytest


STARS_ERROR = "number of stars must be between 1 and 5 (inclusive)"


# Base choice saves whole-number stars for a real pizza with the user's token.
def test_base_choice_is_saved(api, auth, pizza_id):
    response = api.post(
        "/api/ratings",
        json={"pizza_id": pizza_id, "stars": 3},
        headers=auth,
    )
    assert response.status_code == 201
    body = response.json()
    try:
        assert body["stars"] == 3
        assert body["pizza_id"] == pizza_id
    finally:
        api.delete(f"/api/ratings/{body['id']}", headers=auth)


# Whole-number stars below one or above five return the documented JSON error.
@pytest.mark.parametrize("stars", [0, 6])
def test_stars_out_of_range(api, auth, pizza_id, stars):
    response = api.post(
        "/api/ratings",
        json={"pizza_id": pizza_id, "stars": stars},
        headers=auth,
    )
    assert response.status_code == 400
    assert response.json() == {"error": STARS_ERROR}


# Decimal stars are rejected with status 400 and no response body.
def test_decimal_stars_is_refused_with_empty_body(api, auth, pizza_id):
    response = api.post(
        "/api/ratings",
        json={"pizza_id": pizza_id, "stars": 3.5},
        headers=auth,
    )
    assert response.status_code == 400
    assert response.json() == {
        "error": "json: cannot unmarshal number 3.5 into Go struct field Rating.stars of type int"
    }


# Text stars are rejected with status 400 and no response body.
def test_text_stars_is_refused_with_empty_body(api, auth, pizza_id):
    response = api.post(
        "/api/ratings",
        json={"pizza_id": pizza_id, "stars": "3"},
        headers=auth,
    )
    assert response.status_code == 400
    assert response.json() == {
        "error": "json: cannot unmarshal string into Go struct field Rating.stars of type int"
    }


# Missing stars are rejected with status 400 and no response body.
def test_missing_stars_is_refused_with_empty_body(api, auth, pizza_id):
    response = api.post(
        "/api/ratings",
        json={"pizza_id": pizza_id},
        headers=auth,
    )
    assert response.status_code == 400
    assert response.json() == {
        "error": "number of stars must be between 1 and 5 (inclusive)"
    }


# A nonexistent pizza is rejected with status 400 and no response body.
def test_nonexistent_pizza_is_refused_with_empty_body(api, auth):
    response = api.post(
        "/api/ratings",
        json={"pizza_id": 999999999, "stars": 3},
        headers=auth,
    )
    assert response.status_code == 400
    assert response.json() == {"error": "pizza ID 999999999 not found"}


# A short token is rejected with 401 and no response body.
def test_short_token_is_refused_with_empty_body(api, pizza_id):
    response = api.post(
        "/api/ratings",
        json={"pizza_id": pizza_id, "stars": 3},
        headers={"Authorization": "token 0000"},
    )
    assert response.status_code == 401
    assert response.json() == {"error": "authentication failed"}


# Do not send a valid rating without Authorization: live API may create orphaned data.
