from src.app import activities


def test_unregister_successfully_removes_participant(client):
    # A registered student should be able to unregister from an activity.
    activity_name = "Science Club"
    email = activities[activity_name]["participants"][0]

    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )

    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]


def test_unregister_unknown_activity_returns_404(client):
    # Attempting to unregister from a non-existent activity should return a 404 error.
    response = client.delete(
        "/activities/Unknown%20Club/participants",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_missing_participant_returns_404(client):
    # Attempting to unregister a student not in an activity should return a 404 error.
    response = client.delete(
        "/activities/Chess%20Club/participants",
        params={"email": "notpresent@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"


def test_unregister_twice_fails_on_second_attempt(client):
    # Unregistering the same student twice should fail on the second attempt.
    activity_name = "Art Studio"
    email = activities[activity_name]["participants"][0]

    first_response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )
    second_response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )

    assert first_response.status_code == 200
    assert second_response.status_code == 404
    assert second_response.json()["detail"] == "Participant not found in this activity"
