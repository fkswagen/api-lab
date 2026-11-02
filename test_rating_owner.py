# Another user cannot read an owner's rating.
def test_other_user_cannot_read_rating(api, auth, other_auth, rating):
    response = api.get(
        f"/api/ratings/{rating['id']}",
        headers=other_auth,
    )
    assert response.status_code == 404
    assert response.json() == {"error": "not found"}

    owner_read = api.get(
        f"/api/ratings/{rating['id']}",
        headers=auth,
    )
    assert owner_read.status_code == 200
    assert owner_read.json() == rating


# Another user cannot change an owner's rating.
def test_other_user_cannot_update_rating(api, auth, other_auth, rating):
    response = api.put(
        f"/api/ratings/{rating['id']}",
        json={"stars": 4},
        headers=other_auth,
    )
    assert response.status_code == 400
    assert response.json() == {
        "error": f"rating ID {rating['id']} not found"
    }

    owner_read = api.get(
        f"/api/ratings/{rating['id']}",
        headers=auth,
    )
    assert owner_read.status_code == 200
    assert owner_read.json() == rating


# Another user cannot delete an owner's rating.
def test_other_user_cannot_delete_rating(api, auth, other_auth, rating):
    path = f"/api/ratings/{rating['id']}"
    response = api.delete(path, headers=other_auth)
    assert response.status_code == 400
    assert response.json() == {
        "error": f"rating ID {rating['id']} not found"
    }

    owner_read = api.get(path, headers=auth)
    assert owner_read.status_code == 200
    assert owner_read.json() == rating
