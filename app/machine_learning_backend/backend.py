import secrets
from typing import Annotated
from fastapi import Depends, UploadFile
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from ..auth.utils import get_user_data_with_session_token
from ..auth.views import auth_scheme, auth_session
from ..profile.utils import verify_image_format
from .utils import get_bucket

from .ML_Backend.model import inference_model
from .ML_Backend.metadata import FruitMetadata, FruitClass


from PIL import Image
import numpy as np
import io

bucket = get_bucket()


def numpy_binary_to_bucket_url(np_img):
    image = Image.fromarray(np.uint8(np_img)).convert("RGB")
    image_byte_stream = io.BytesIO()
    image.save(image_byte_stream, format="PNG")
    image_byte_stream.seek(0)

    filename = secrets.token_urlsafe(40) + ".png"
    blob = bucket.blob(filename)
    while True:
        if not blob.exists():
            break

        filename = secrets.token_urlsafe(40) + ".png"
        blob = bucket.blob(filename)
        continue

    # Begin upload the image to the bucket !
    try:
        blob.upload_from_file(image_byte_stream)
    except Exception as e:
        print(e)
        return JSONResponse({"status": "error", "message": "Internal upload error"})

    return blob.public_url


# ==================== Prediction ====================
def predict(
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

    # pre processs for feeding to model
    im = Image.open(image.file)
    im = np.array(im)

    # Predict image
    # GYATTTT THIS MODEL IS THICC 🥵
    # Um i mean huge 🥵
    # Ummm i mean big 😋
    # yea... idk... sry...
    data = inference_model(im)

    # for every image replace with bucket url

    data["orig_img"] = numpy_binary_to_bucket_url(data["orig_img"])
    for inference in data["inferences"]:
        inference["cropped_img"] = numpy_binary_to_bucket_url(inference["cropped_img"])
        inference["class"] = FruitMetadata[FruitClass(inference["class"])]["string"]

    print(data)

    return {"status": "ok", "data": data}
