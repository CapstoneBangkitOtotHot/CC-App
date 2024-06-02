import json
from werkzeug.wrappers import Response
from flask import request
from functools import wraps


# Adapted from
# https://github.com/mansuf/mangadex-downloader/blob/v2.10.3/mangadex_downloader/utils.py#L105-L119
# with some modifications
def comma_separated_text(array):
    # Opening square bracket
    text = "["

    if not array:
        text += "]"
        return text

    # Append first item
    text += array.pop(0)

    # Add the rest of items
    for item in array:
        text += ", " + item

    # Closing square bracket
    text += "]"

    return text


# Error handlers for flask
def json_error_handler(message="Server Error"):
    return Response(
        response=json.dumps({"status": "error", "message": message}),
        status=400,
        content_type="application/json",
    )


def validate_json_request(*json_keys):

    # Dear god, wtf is this
    def wrap(func):

        @wraps(func)
        def validate():
            request_data = request.get_json(silent=True)
            if request_data is None:
                return json_error_handler(message="MANA DATA JSON NYA WOY")

            for key in json_keys:
                if key not in list(request.json.keys()):
                    return json_error_handler(
                        message=f"{key!r} gak ada di data JSON nya woy"
                    )

            return func()

        return validate

    return wrap
