from PIL import Image, UnidentifiedImageError
from fastapi.responses import JSONResponse

ALLOWED_IMAGE_FORMATS = ["JPEG", "JPG", "PNG"]


def verify_image_format(fp):
    try:
        im = Image.open(fp)
    except UnidentifiedImageError:
        return JSONResponse(
            {
                "status": "error",
                "message": f"Unknown image format, choices are {ALLOWED_IMAGE_FORMATS!r}",
            },
            status_code=400,
        )

    # TODO: Add convertion for transparency images
    if im.has_transparency_data:
        return JSONResponse(
            {
                "status": "error",
                "message": "Image cannot be transparent or alpha channel",
            },
            status_code=400,
        )

    if im.format not in ALLOWED_IMAGE_FORMATS:
        return JSONResponse(
            {
                "status": "error",
                "message": f"Image format not allowed, choices are {ALLOWED_IMAGE_FORMATS!r}",
            },
            status_code=400,
        )

    if getattr(im, "is_animated", False):
        return JSONResponse(
            {"status": "error", "message": "Image cannot be GIF or animated"},
            status_code=400,
        )

    # Return none for success


def get_image_format(fp):
    im = Image.open(fp)
    fmt = im.format
    return fmt
