def test_get_users(client):
    response = client.get("/api/users")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 2
