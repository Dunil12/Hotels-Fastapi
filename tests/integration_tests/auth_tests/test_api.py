


async def test_auth_crud(ac):
    response = await ac.post("/auth/register", json={"email": "email123@gmail.com", "password": "password"})
    assert response.status_code == 200

