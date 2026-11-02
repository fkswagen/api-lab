# A new rating returns its id, star value, and pizza id.
def test_create_rating(api, auth, pizza_id):
    response = api.post(
        "/api/ratings",
        json={"pizza_id": pizza_id, "stars": 5},
        headers=auth,
    )
    assert response.status_code == 201
    body = response.json()
    try:
        assert body["stars"] == 5
        assert body["pizza_id"] == pizza_id
        assert isinstance(body["id"], int)
    finally:
        api.delete(f"/api/ratings/{body['id']}", headers=auth)


# An owned rating can be read back unchanged.
def test_read_rating(api, auth, rating):
    response = api.get(f"/api/ratings/{rating['id']}", headers=auth)
    assert response.status_code == 200
    assert response.json() == rating


# Updating an owned rating returns its new star value.
def test_update_rating(api, auth, rating):
    response = api.put(
        f"/api/ratings/{rating['id']}",
        json={"stars": 4},
        headers=auth,
    )
    assert response.status_code == 200
    assert response.json()["stars"] == 4


# Deleting an owned rating returns no content, and later reads return not found.
def test_delete_rating(api, auth, rating):
    path = f"/api/ratings/{rating['id']}"
    response = api.delete(path, headers=auth)
    assert response.status_code == 204

    response = api.get(path, headers=auth)
    assert response.status_code == 404
