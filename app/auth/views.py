import requests
from typing import Annotated
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from firebase_admin.auth import revoke_refresh_tokens
from firebase_admin.exceptions import FirebaseError
from .utils import (
    build_auth_url,
    create_session_and_refresh_token,
    JWTBearer,
    get_user_data_with_session_token,
)
from .models import LoginRequestModel, RefreshTokenRequestModel


auth_session = requests.Session()
auth_scheme = JWTBearer()


def register_user(data: LoginRequestModel):
    payload = {"email": data.email, "password": data.password}

    r = auth_session.post(build_auth_url("signUp"), json=payload)
    response_data = r.json()

    if not r.ok:
        error_msg = response_data["error"]["message"]
        if error_msg == "EMAIL_EXISTS":
            error_msg = "Failed to register, email is already exists"

        return JSONResponse(
            {"status": "error", "message": error_msg}, status_code=r.status_code
        )

    r = auth_session.post(
        build_auth_url("update"),
        json={"displayName": "", "photoUrl": "", "idToken": response_data["idToken"]},
    )
    response_data = r.json()

    if not r.ok:
        error_msg = response_data["error"]["message"]

        return JSONResponse(
            {"status": "error", "message": error_msg}, status_code=r.status_code
        )

    return {"status": "ok"}


def login(data: LoginRequestModel):
    payload = {"email": data.email, "password": data.password}

    r = auth_session.post(build_auth_url("signInWithPassword"), json=payload)
    response_data = r.json()

    if not r.ok:
        error_msg = response_data["error"]["message"]

        return JSONResponse(
            {"status": "error", "message": error_msg}, status_code=r.status_code
        )

    return create_session_and_refresh_token(response_data)


def refresh(data: RefreshTokenRequestModel):
    payload = {"idToken": data.token}

    r = auth_session.post(build_auth_url("lookup"), json=payload)
    response_data = r.json()

    if not r.ok:
        error_msg = response_data["error"]["message"]
        if "INVALID_ID_TOKEN" in error_msg:
            error_msg = "Refresh token is expired, please log in again"

        return JSONResponse(
            {"status": "error", "message": error_msg}, status_code=r.status_code
        )

    return create_session_and_refresh_token(
        {"localId": response_data["users"][0]["localId"], "idToken": data.token}
    )


def logout(
    auth: Annotated[HTTPAuthorizationCredentials, Depends(auth_scheme)],
):
    user_data = get_user_data_with_session_token(
        token=auth.credentials, session=auth_session
    )

    if user_data is None:
        return JSONResponse(
            {"status": "error", "message": "Login invalid or user not found"},
            status_code=400,
        )

    try:
        revoke_refresh_tokens(user_data["localId"])
    except FirebaseError as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=400)

    return {"status": "ok"}


def reset_password(
    auth: Annotated[HTTPAuthorizationCredentials, Depends(auth_scheme)],
):
    user_data = get_user_data_with_session_token(
        token=auth.credentials, session=auth_session
    )

    if user_data is None:
        return JSONResponse(
            {"status": "error", "message": "Login invalid or user not found"},
            status_code=400,
        )

    payload = {
        "requestType": "PASSWORD_RESET",
        "email": user_data["email"],
    }

    r = auth_session.post(build_auth_url("sendOobCode"), json=payload)
    response_data = r.json()

    if not r.ok:
        error_msg = response_data.get("error", {}).get("message", "Unknown error")

        return JSONResponse(
            {"status": "error", "message": error_msg}, status_code=r.status_code
        )

    return {"status": "ok", "message": "Password reset email sent"}
