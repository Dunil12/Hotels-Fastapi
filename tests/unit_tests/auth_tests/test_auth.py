from src.services.auth import AuthService


def test_create_access_token():
    user_data = {"user_id": 1}
    token = AuthService().create_access_token(user_data)

    assert token
    assert isinstance(token, str)

def test_hash_password():
    user_data = {"email": "email@gmail.com", "password": "password"}
    hashed_password = AuthService().hash_password(user_data["password"])

    assert hashed_password != user_data["password"]