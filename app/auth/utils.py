from firebase_admin.auth import create_custom_token


def build_auth_url(key, action):
    return f"https://identitytoolkit.googleapis.com/v1/accounts:{action}?key={key}"


def get_email_and_password_payload(r):
    data = r.get_json()
    return {"email": data["email"], "password": data["password"]}


def get_reset_password_payload(r):
    data = r.get_json()
    return {
        "oobCode": data.get("oobCode"),
        "newPassword": data.get("newPassword"),
        "email": data.get("email"),
        "oldPassword": data.get("oldPassword"),
    }


def create_session_and_refresh_token(response_data):
    session_token = create_custom_token(response_data["localId"])
    refresh_token = response_data["idToken"]

    return {
        "status": "ok",
        "data": {
            "session_token": session_token.decode(),
            "refresh_token": refresh_token,
        },
    }
