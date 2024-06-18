import secrets
import cv2
import io
import numpy as np
from typing import Annotated
from fastapi import Depends, UploadFile
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from PIL import Image

from ..auth.utils import get_user_data_with_session_token
from ..auth.views import auth_scheme, auth_session
from ..profile.utils import verify_image_format
from .utils import get_bucket, get_tips
from .ML_Backend.model import inference_model
from .ML_Backend.metadata import FruitClass


bucket = get_bucket()

SUPPORTED_FRUITS = [
    FruitClass.APPLE.value,
    FruitClass.MANGO.value,
    FruitClass.SAPODILLA.value,
    FruitClass.TOMATO.value,
]


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

    # Remove transparency in the image
    # to avoid error while predicting
    fp = io.BytesIO()
    im = Image.open(image.file)
    im.convert("RGB").save(fp, format="JPEG")
    im.close()

    # Begin prosessing the image
    im = Image.open(fp, formats=["JPEG"])
    im = np.array(im)

    # BUG: cv2.imread are converting image to BGR mode
    # while PIL.Image.open doesn't do that, instead they going RGB mode
    # cv.imread Reference: https://docs.opencv.org/4.x/d4/da8/group__imgcodecs.html#gab32ee19e22660912565f8140d0f675a8
    # cv2.cvColor Reference: https://gist.github.com/panzi/1ceac1cb30bb6b3450aa5227c02eedd3
    im = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)

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

    for info in data["inferences"]:

        # Ignore unsupported fruits
        try:
            SUPPORTED_FRUITS.index(info["fruit_class"])
        except ValueError:
            continue

        # Temporary workaround for freshness_percentage
        fp = info["freshness_percentage"]
        fp = int((abs(fp) * 100) / 20 * 10)
        if fp >= 100:
            fp = 100

        info["freshness_percentage"] = f"{fp}%"

        # Workaround for freshness_days
        fd = int(abs(info["freshness_days"]))
        if fp <= 15:
            info["freshness_days"] = 0
        else:
            info["freshness_days"] = fd

        # Add tips
        info["tips"] = get_tips(info["fruit_class_string"].lower(), fp)

    return {"status": "ok", "data": data}
