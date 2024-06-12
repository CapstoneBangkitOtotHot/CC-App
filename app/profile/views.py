import secrets
from typing import Annotated
from fastapi import Depends, UploadFile
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from ..auth.utils import get_user_data_with_session_token, build_auth_url
from ..auth.views import auth_scheme, auth_session
from ..firebase import get_bucket
from .models import SetUsernameRequestModel
from .utils import verify_image_format, get_image_format


# ==================== GET PROFILE ====================
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


# ==================== SET USERNAME ====================
def set_username(
    auth: Annotated[HTTPAuthorizationCredentials, Depends(auth_scheme)],
    data: SetUsernameRequestModel,
):
    user_data = get_user_data_with_session_token(
        token=auth.credentials, session=auth_session
    )

    if user_data is None:
        return JSONResponse(
            {"status": "error", "message": "Login invalid or user not found"},
            status_code=400,
        )

    id_token = user_data.get("idToken")  # Get idToken from user data
    if not id_token:
        return JSONResponse(
            {"status": "error", "message": "ID token not found in user data"},
            status_code=400,
        )

    payload = {
        "idToken": id_token,
        "displayName": data.displayName,
    }

    r = auth_session.post(build_auth_url("update"), json=payload)
    response_data = r.json()

    if not r.ok:
        error_msg = response_data.get("error", {}).get("message", "Unknown error")

        return JSONResponse(
            {"status": "error", "message": error_msg}, status_code=r.status_code
        )

    return {"status": "ok", "message": "Username updated successfully"}


def upload_photo_profile(
    auth: Annotated[HTTPAuthorizationCredentials, Depends(auth_scheme)],
    image: UploadFile,
):
    user_data = get_user_data_with_session_token(
        token=auth.credentials, session=auth_session
    )

    if user_data is None:
        return JSONResponse(
            {"status": "error", "message": "Login invalid or user not found"},
            status_code=400,
        )

    # Verify if this file is valid image
    err = verify_image_format(image.file)
    if err:
        return err

    # Get image format
    image.file.seek(0)
    file_ext = get_image_format(image.file).lower()

    # TODO: Create checking if user has already photo profile
    # if the user already have photo profile delete it and upload the new one

    # Generate unique filename for the image
    image.file.seek(0)
    bucket = get_bucket()
    filename = secrets.token_urlsafe(40) + f".{file_ext}"
    blob = bucket.blob(filename)
    while True:
        if not blob.exists():
            break

        filename = secrets.token_urlsafe(40) + f".{file_ext}"
        blob = bucket.blob(filename)
        continue

    # Begin upload the image to the bucket !
    try:
        blob.upload_from_file(image.file)
    except Exception as e:
        print(e)
        return JSONResponse({"status": "error", "message": "Internal upload error"})

    # Update photoUrl in profile
    r = auth_session.post(
        build_auth_url("update"),
        json={"idToken": user_data["idToken"], "photoUrl": blob.public_url},
    )
    response_data = r.json()

    if not r.ok:
        error_msg = response_data.get("error", {}).get("message", "Unknown error")

        return JSONResponse(
            {"status": "error", "message": error_msg}, status_code=r.status_code
        )

    return {"status": "ok"}
