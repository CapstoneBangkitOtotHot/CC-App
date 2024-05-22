import requests
import json
from flask import request, Response
from .utils import build_auth_url, get_email_and_password_payload

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

    return {
        "status": "ok",
        "data": {
            "session_token": response_data["idToken"],
        },
    }
