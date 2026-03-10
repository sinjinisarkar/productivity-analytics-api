def test_create_habit(client):
    u = client.post("/users", json={
        "username": "habituser",
        "email": "habituser@example.com",
        "password": "StrongPass123"
    }).json()

    res = client.post("/habits", json={
        "user_id": u["id"],
        "name": "Morning Run",
        "frequency": "daily"
    })
    assert res.status_code == 201
    body = res.json()
    assert body["name"] == "Morning Run"
    assert body["frequency"] == "daily"
    assert body["user_id"] == u["id"]


def test_create_habit_log(client):
    u = client.post("/users", json={
        "username": "loguser",
        "email": "loguser@example.com",
        "password": "StrongPass123"
    }).json()

    habit = client.post("/habits", json={
        "user_id": u["id"],
        "name": "Read 30 mins",
        "frequency": "daily"
    }).json()

    res = client.post(f"/habits/{habit['id']}/logs", json={
        "date": "2026-03-10",
        "completed": True
    })
    assert res.status_code == 201
    body = res.json()
    assert body["habit_id"] == habit["id"]
    assert body["completed"] is True


def test_duplicate_habit_log_rejected(client):
    u = client.post("/users", json={
        "username": "dupuser",
        "email": "dupuser@example.com",
        "password": "StrongPass123"
    }).json()

    habit = client.post("/habits", json={
        "user_id": u["id"],
        "name": "Meditate",
        "frequency": "daily"
    }).json()

    client.post(f"/habits/{habit['id']}/logs", json={
        "date": "2026-03-10",
        "completed": True
    })

    # Second log for same date should be rejected
    res = client.post(f"/habits/{habit['id']}/logs", json={
        "date": "2026-03-10",
        "completed": True
    })
    assert res.status_code == 409