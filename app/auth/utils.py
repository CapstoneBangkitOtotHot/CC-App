import jwt
from datetime import datetime
from requests import Session
from firebase_admin.auth import create_custom_token
from fastapi.security import HTTPBearer
from fastapi.exceptions import HTTPException
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from ..config import firebase_api_key


def build_auth_url(action):
    return f"https://identitytoolkit.googleapis.com/v1/accounts:{action}?key={firebase_api_key}"


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


# Reference: https://testdriven.io/blog/fastapi-jwt-auth/#:~:text=This%20is%20done%20by%20scanning,%2Fauth%2Fauth_handler.py.
class JWTBearer(HTTPBearer):

    async def __call__(self, request: Request):
        cred = await super().__call__(request)
        if cred:
            if not self.verify_jwt(cred.credentials):
                raise HTTPException(
                    status_code=403,
                    detail="Login session is invalid, please log in again",
                )

            return cred
        else:
            raise HTTPException(status_code=403, detail="Authentication is required")

    def verify_jwt(self, token: str):
        try:
            data = jwt.decode(token, options={"verify_signature": False})
        except Exception as e:
            print(e)
            return False

        expiration_time = datetime.fromtimestamp(data["exp"])
        now = datetime.now()

        if now > expiration_time:
            return False

        return True


def get_user_data_with_session_token(token: str, session: Session):
    r = session.post(build_auth_url("signInWithCustomToken"), json={"token": token})
    if not r.ok:
        return None

    id_token = r.json()["idToken"]

    r = session.post(build_auth_url("lookup"), json={"idToken": id_token})
    if not r.ok:
        return None

    response_data = r.json()
    user_data = response_data["users"][0]
    user_data["idToken"] = id_token

    return user_data


def send_confirm_email(id_token: str, auth_session: Session):
    r = auth_session.post(
        build_auth_url("sendOobCode"),
        json={"idToken": id_token, "requestType": "VERIFY_EMAIL"},
    )
    response_data = r.json()

    if not r.ok:
        error_msg = response_data["error"]["message"]

        return JSONResponse(
            {"status": "error", "message": error_msg}, status_code=r.status_code
        )

    # Return none if success
