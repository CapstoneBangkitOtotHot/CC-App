from .views import get_profile, set_username, upload_photo_profile
from .models import GetProfileResponseModel, SetUsernameResponseModel
from ..auth.models import OkResponseModel

urls_patterns = [
    {
        "path": "/profile/get-user",
        "endpoint": get_profile,
        "methods": ["GET"],
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
    {
        "path": "/profile/upload-photo",
        "endpoint": upload_photo_profile,
        "methods": ["POST"],
        "summary": "Upload photo profile",
        "description": "Upload image for photo profile user",
        "responses": {200: {"model": OkResponseModel}},
    },
]

for url in urls_patterns:
    url["tags"] = ["Profile"]
