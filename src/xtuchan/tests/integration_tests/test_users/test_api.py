import pytest

@pytest.mark.parametrize("email, password, status_code", [
    ("kot@pes.com", "kotopes", 200),
    ("kot@pes.com", "kot0pes", 409),
    ("pes@kot.com", "peskot", 200),
    ("abcde", "pesokot", 422),
])
def test_register_user(email, password, status_code, client):
    response = client.post("/auth/register", json={
        "email": email,
        "password": password,
    })

    assert response.status_code == status_code