def test_create_task(client):
    u = client.post("/users", json={
        "username": "taskuser",
        "email": "taskuser@example.com",
        "password": "StrongPass123"
    }).json()

    res = client.post("/tasks", json={
        "user_id": u["id"],
        "title": "Test task",
        "description": "Check task creation",
        "due_date": "2026-03-05"
    })
    assert res.status_code == 201
    body = res.json()
    assert body["title"] == "Test task"
    assert body["user_id"] == u["id"]