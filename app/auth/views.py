import requests
import json
from flask import request, Response
from firebase_admin.auth import revoke_refresh_tokens
from firebase_admin.exceptions import FirebaseError
from .utils import (
    build_auth_url,
    get_email_and_password_payload,
    create_session_and_refresh_token,
)

from ..utils import validate_json_request
from ..config import firebase_api_key

auth_session = requests.Session()


@validate_json_request("email", "password")
def register_user():
    payload = get_email_and_password_payload(request)

    r = auth_session.post(build_auth_url(firebase_api_key, "signUp"), json=payload)
    response_data = r.json()

    if not r.ok:
        error_msg = response_data["error"]["message"]
        if error_msg == "EMAIL_EXISTS":
            error_msg = "Failed to register, email is already exists"

        return Response(
            json.dumps({"status": "error", "message": error_msg}), status=r.status_code
        )

    return {"status": "ok"}


@validate_json_request("email", "password")
def login():
    payload = get_email_and_password_payload(request)

    r = auth_session.post(
        build_auth_url(firebase_api_key, "signInWithPassword"), json=payload
    )
    response_data = r.json()

    if not r.ok:
        error_msg = response_data["error"]["message"]

        return Response(
            json.dumps({"status": "error", "message": error_msg}), status=r.status_code
        )

    return create_session_and_refresh_token(response_data)


@validate_json_request("refreshToken")
def refresh():
    refresh_token = request.json["refreshToken"]
    payload = {"idToken": refresh_token}

    r = auth_session.post(build_auth_url(firebase_api_key, "lookup"), json=payload)
    response_data = r.json()

    if not r.ok:
        error_msg = response_data["error"]["message"]
        if "INVALID_ID_TOKEN" in error_msg:
            error_msg = "Refresh token is expired, please log in again"

        return Response(
            json.dumps({"status": "error", "message": error_msg}), status=r.status_code
        )

    return create_session_and_refresh_token(
        {"localId": response_data["users"][0]["localId"], "idToken": refresh_token}
    )


@validate_json_request("userId")
def logout():
    try:
        revoke_refresh_tokens(request.json["userId"])
    except FirebaseError as e:
        return Response(json.dumps({"status": "error", "message": str(e)}), status=400)

    return {"status": "ok"}


@validate_json_request("email")
def send_reset_password_email():
    payload = {
        "requestType": "PASSWORD_RESET",
        "email": request.get_json().get("email"),
    }

    r = auth_session.post(build_auth_url(firebase_api_key, "sendOobCode"), json=payload)
    response_data = r.json()

    if not r.ok:
        error_msg = response_data.get("error", {}).get("message", "Unknown error")

        return Response(
            json.dumps({"status": "error", "message": error_msg}), status=r.status_code
        )

    return {"status": "ok", "message": "Password reset email sent"}


@validate_json_request("oobCode", "newPassword")
def reset_password():
    payload = {
        "oobCode": request.get_json().get("oobCode"),
        "newPassword": request.get_json().get("newPassword"),
    }

    r = auth_session.post(
        build_auth_url(firebase_api_key, "resetPassword"), json=payload
    )
    response_data = r.json()

    if not r.ok:
        error_msg = response_data.get("error", {}).get("message", "Unknown error")

        return Response(
            json.dumps({"status": "error", "message": error_msg}), status=r.status_code
        )

    return {"status": "ok", "message": "Password has been reset"}
