from typing import Annotated
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from ..auth.utils import get_user_data_with_session_token
from ..auth.views import auth_scheme, auth_session


def get_profile(
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

    data = {
        "username": user_data["displayName"],
        "email": user_data["email"],
        "photo_url": user_data["photoUrl"],
    }

    return {"status": "ok", "data": data}
