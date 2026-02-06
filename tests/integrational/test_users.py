from .test_client import client

def test_users_me():
    response = client.get("/users/me")
    assert response.status_code == 401