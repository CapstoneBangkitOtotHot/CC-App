import json
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.responses import RedirectResponse, JSONResponse
from .auth.urls import urls_patterns as auth_urls
from .profile.urls import urls_patterns as profile_urls
from .utils import comma_separated_text

app = FastAPI(
    servers=[
        dict(url="https://api.bangkit-c241-ps005.site/", description="Production"),
        dict(url="http://localhost:5000/", description="Development"),
    ],
)


async def validation_exception_handler(
    request: Request, exceptions: RequestValidationError
):
    print(exceptions.errors())

    missing_fields = []
    for exc in exceptions.errors():
        if exc["type"] == "missing":
            missing_fields.append(exc["loc"][1])

    if not missing_fields:
        err = await request_validation_exception_handler(request, exceptions)
        err_body = {"status": "error"}
        err_body.update(json.loads(err.body))

        err.body = err.render(err_body)
        err.init_headers()
        return err

    missing_fields = comma_separated_text(missing_fields)

    error_message = f"{missing_fields} "
    if request.method == "GET":
        error_message += "tidak ada didalam query parameters"
    else:
        error_message += "tidak ada didalam data JSON nya"
    return JSONResponse({"status": "error", "message": error_message}, status_code=400)


def redirect_docs():
    return RedirectResponse("/docs")


for kwargs_url in auth_urls:
    app.add_api_route(**kwargs_url)

for kwargs_url in profile_urls:
    app.add_api_route(**kwargs_url)

app.add_api_route("/", endpoint=redirect_docs, include_in_schema=False)

app.add_exception_handler(RequestValidationError, validation_exception_handler)
