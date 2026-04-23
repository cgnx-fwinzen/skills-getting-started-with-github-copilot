def test_root_redirects_to_static_index(client):
    # The root endpoint should redirect to the static frontend page.
    response = client.get("/", follow_redirects=False)

    assert response.status_code in (302, 307)
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_activity_map(client):
    # The activities endpoint should return a dictionary keyed by activity name.
    response = client.get("/activities")

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, dict)
    assert "Chess Club" in payload

    # Verify one known activity includes the expected fields and data types.
    chess = payload["Chess Club"]
    assert chess["description"]
    assert chess["schedule"]
    assert isinstance(chess["max_participants"], int)
    assert isinstance(chess["participants"], list)
