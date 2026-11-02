# A newly created user can log in and starts with no ratings.
def test_new_user_has_no_ratings(api, auth):
    response = api.get("/api/ratings", headers=auth)
    assert response.status_code == 200
    assert response.json() == {"ratings": []}
