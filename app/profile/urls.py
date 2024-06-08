from .views import (
    get_profile,
    set_username
)
from .models import GetProfileResponseModel, SetUsernameResponseModel

urls_patterns = [
    {
        "path": "/profile/get-user",
        "endpoint": get_profile,
        "methods": ["POST"],
        "summary": "Get User Profile",
        "description": "Get user data using session token",
        "responses": {200: {"model": GetProfileResponseModel}},
    },
    {
        "path": "/profile/set-username",
        "endpoint": set_username,
        "methods": ["POST"],
        "summary": "Set Username",
        "description": "Set username using session token",
        "responses": {200: {"model": SetUsernameResponseModel}},
    },
]

for url in urls_patterns:
    url["tags"] = ["Profile"]
