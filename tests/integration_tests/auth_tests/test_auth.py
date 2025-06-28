from first_project.src.services.auth import AuthService


def test_create_and_decode_access_token():
    data = {"user_id": 1}
    token = AuthService().create_access_token(data)
    decoded_token = AuthService().decode_token(token)

    assert decoded_token
    assert decoded_token["user_id"] == data["user_id"]