from src.app import activities


def test_signup_successfully_adds_participant(client):
    # A new student should successfully register for an activity with available spots.
    activity_name = "Debate Team"
    email = "newstudent@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    assert response.status_code == 200
    assert email in activities[activity_name]["participants"]


def test_signup_unknown_activity_returns_404(client):
    # Signing up for a non-existent activity should return a 404 error.
    response = client.post("/activities/Unknown%20Club/signup", params={"email": "student@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_participant_returns_400(client):
    # A student already signed up for an activity should not be able to sign up again.
    activity_name = "Chess Club"
    existing_email = activities[activity_name]["participants"][0]

    response = client.post(f"/activities/{activity_name}/signup", params={"email": existing_email})

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_full_activity_returns_400(client):
    # Signing up for an activity at max capacity should be rejected.
    activity_name = "Basketball Team"
    activities[activity_name]["participants"] = [
        f"player{i}@mergington.edu" for i in range(activities[activity_name]["max_participants"])
    ]

    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": "lateplayer@mergington.edu"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"
