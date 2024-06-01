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
        "oldPassword": data.get("oldPassword")
    }