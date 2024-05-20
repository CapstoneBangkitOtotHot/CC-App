import json
from werkzeug.wrappers import Response
from flask import request
from functools import wraps


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
