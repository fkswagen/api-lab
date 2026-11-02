import pytest


# Zero, one, or two excluded tools still produce a pizza using another tool.
@pytest.mark.parametrize(
    "excluded",
    [[], ["Knife"], ["Knife", "Pizza cutter"]],
)
def test_excluded_tool_is_not_used(api, auth, excluded):
    response = api.post(
        "/api/pizza",
        json={"excludedTools": excluded},
        headers=auth,
    )
    assert response.status_code == 200
    assert response.json()["pizza"]["tool"] not in excluded


# All tools excluded should return a client error with a JSON error body.
@pytest.mark.xfail(
    reason="Defect 1: excluding all three tools returns 500 with an empty body",
    strict=True,
)
def test_all_tools_excluded_is_refused(api, auth):
    response = api.post(
        "/api/pizza",
        json={"excludedTools": ["Knife", "Pizza cutter", "Scissors"]},
        headers=auth,
    )
    assert response.status_code == 400
    body = response.json()
    assert isinstance(body, dict)
    assert "error" in body
