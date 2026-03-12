def get_auth_headers(client, username="taskuser", email="taskuser@example.com", password="StrongPass123"):
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


def test_create_task(client):
    headers = get_auth_headers(client)

    res = client.post("/tasks", json={
        "title": "Test task",
        "description": "Check task creation",
        "due_date": "2026-03-05"
    }, headers=headers)

    assert res.status_code == 201
    body = res.json()
    assert body["title"] == "Test task"
    assert body["completed"] is False
    assert "user_id" in body


def test_list_tasks(client):
    headers = get_auth_headers(client)

    client.post("/tasks", json={
        "title": "Task 1",
        "description": "First task",
        "due_date": "2026-03-05"
    }, headers=headers)

    res = client.get("/tasks", headers=headers)

    assert res.status_code == 200
    body = res.json()
    assert isinstance(body, list)
    assert len(body) == 1
    assert body[0]["title"] == "Task 1"


def test_update_task(client):
    headers = get_auth_headers(client)

    created = client.post("/tasks", json={
        "title": "Task to update",
        "description": "Old description",
        "due_date": "2026-03-05"
    }, headers=headers).json()

    res = client.patch(f"/tasks/{created['id']}", json={
        "title": "Updated task",
        "completed": True
    }, headers=headers)

    assert res.status_code == 200
    body = res.json()
    assert body["title"] == "Updated task"
    assert body["completed"] is True
    assert body["completed_at"] is not None


def test_delete_task(client):
    headers = get_auth_headers(client)

    created = client.post("/tasks", json={
        "title": "Task to delete",
        "description": "Delete me",
        "due_date": "2026-03-05"
    }, headers=headers).json()

    res = client.delete(f"/tasks/{created['id']}", headers=headers)
    assert res.status_code == 204

    res2 = client.get(f"/tasks/{created['id']}", headers=headers)
    assert res2.status_code == 404