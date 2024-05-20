def build_auth_url(key, action):
    return f"https://identitytoolkit.googleapis.com/v1/accounts:{action}?key={key}"


def get_email_and_password_payload(r):
    return {"email": r.json["email"], "password": r.json["password"]}
