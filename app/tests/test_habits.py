def get_auth_headers(client, username="habituser", email="habituser@example.com", password="StrongPass123"):
    client.post("/users", json={
        "username": username,
        "email": email,
        "password": password
    })

    login = client.post("/auth/login", data={
        "username": username,
        "password": password
    })

    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_habit(client):
    headers = get_auth_headers(client)

    res = client.post("/habits", json={
        "name": "Drink water",
        "frequency": "daily"
    }, headers=headers)

    assert res.status_code == 201
    body = res.json()
    assert body["name"] == "Drink water"
    assert body["frequency"] == "daily"
    assert "user_id" in body


def test_list_habits(client):
    headers = get_auth_headers(client)

    client.post("/habits", json={
        "name": "Read book",
        "frequency": "weekly"
    }, headers=headers)

    res = client.get("/habits", headers=headers)

    assert res.status_code == 200
    body = res.json()
    assert isinstance(body, list)
    assert len(body) == 1
    assert body[0]["name"] == "Read book"


def test_update_habit(client):
    headers = get_auth_headers(client)

    created = client.post("/habits", json={
        "name": "Workout",
        "frequency": "daily"
    }, headers=headers).json()

    res = client.patch(f"/habits/{created['id']}", json={
        "frequency": "weekly"
    }, headers=headers)

    assert res.status_code == 200
    body = res.json()
    assert body["frequency"] == "weekly"


def test_delete_habit(client):
    headers = get_auth_headers(client)

    created = client.post("/habits", json={
        "name": "Meditate",
        "frequency": "daily"
    }, headers=headers).json()

    res = client.delete(f"/habits/{created['id']}", headers=headers)
    assert res.status_code == 204

    res2 = client.get(f"/habits/{created['id']}", headers=headers)
    assert res2.status_code == 404


def test_log_habit(client):
    headers = get_auth_headers(client)

    habit = client.post("/habits", json={
        "name": "Journal",
        "frequency": "daily"
    }, headers=headers).json()

    res = client.post(f"/habits/{habit['id']}/logs", json={
        "date": "2026-03-12",
        "completed": True
    }, headers=headers)

    assert res.status_code == 201
    body = res.json()
    assert body["habit_id"] == habit["id"]
    assert body["completed"] is True


def test_list_habit_logs(client):
    headers = get_auth_headers(client)

    habit = client.post("/habits", json={
        "name": "Stretch",
        "frequency": "daily"
    }, headers=headers).json()

    client.post(f"/habits/{habit['id']}/logs", json={
        "date": "2026-03-12",
        "completed": True
    }, headers=headers)

    res = client.get(f"/habits/{habit['id']}/logs", headers=headers)

    assert res.status_code == 200
    body = res.json()
    assert isinstance(body, list)
    assert len(body) == 1
    assert body[0]["habit_id"] == habit["id"]