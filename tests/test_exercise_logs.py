def test_create_exercise_log(client, auth_headers):
    workout_payload = {
        "title": "Push Day",
        "workout_date": "2026-03-25",
        "notes": "chest day"
    }

    workout_response = client.post("/workouts", json=workout_payload, headers=auth_headers)
    assert workout_response.status_code == 201

    workout_id = workout_response.json()["id"]

    exercise_payload = {
        "exercise_name": "Bench Press",
        "sets": 4,
        "reps": 8,
        "weight": 60,
        "notes": "felt good"
    }

    response = client.post(
        f"/workouts/{workout_id}/exercise-logs",
        json=exercise_payload,
        headers=auth_headers
    )

    assert response.status_code == 201

    data = response.json()
    assert data["exercise_name"] == "Bench Press"
    assert data["sets"] == 4
    assert data["reps"] == 8
    assert data["weight"] == 60
    assert data["notes"] == "felt good"
    assert data["workout_id"] == workout_id
    assert "id" in data
    assert "created_at" in data

def test_cannot_create_exercise_log_in_another_users_workout(client, auth_headers, another_auth_headers):
    workout_payload = {
        "title": "Push Day",
        "workout_date": "2026-03-25",
        "notes": "chest day"
    }

    workout_response = client.post("/workouts", json=workout_payload, headers=auth_headers)
    assert workout_response.status_code == 201

    workout_id = workout_response.json()["id"]

    exercise_payload = {
        "exercise_name": "Bench Press",
        "sets": 4,
        "reps": 8,
        "weight": 60,
        "notes": "not your workout"
    }

    response = client.post(
        f"/workouts/{workout_id}/exercise-logs",
        json=exercise_payload,
        headers=another_auth_headers
    )

    assert response.status_code in (403, 404)