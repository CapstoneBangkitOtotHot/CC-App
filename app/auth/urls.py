from .views import (
    register_user,
    login,
    reset_password,
    logout,
    refresh,
)
from .models import OkResponseModel, ResetPasswordResponseModel, LoginResponseModel

urls_patterns = [
    {
        "path": "/auth/register",
        "endpoint": register_user,
        "methods": ["POST"],
        "summary": "Register",
        "description": "Register using email and password",
        "responses": {200: {"model": OkResponseModel}},
    },
    {
        "path": "/auth/login",
        "endpoint": login,
        "methods": ["POST"],
        "summary": "Login",
        "description": "Authenticate using email and password",
        "responses": {200: {"model": LoginResponseModel}},
    },
    {
        "path": "/auth/logout",
        "endpoint": logout,
        "methods": ["POST"],
        "summary": "Logout",
        "description": "Logout",
        "responses": {200: {"model": OkResponseModel}},
    },
    {
        "path": "/auth/refresh",
        "endpoint": refresh,
        "methods": ["POST"],
        "summary": "Refresh session token using refresh token",
        "description": "Get new session and refresh token",
        "responses": {200: {"model": LoginResponseModel}},
    },
    {
        "path": "/auth/reset-password",
        "endpoint": reset_password,
        "methods": ["POST"],
        "summary": "Reset password using email",
        "description": "Send reset password link with email",
        "responses": {200: {"model": ResetPasswordResponseModel}},
    },
]

for url in urls_patterns:
    url["tags"] = ["Authentication"]
