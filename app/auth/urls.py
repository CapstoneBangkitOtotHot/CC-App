from .views import (
    register_user,
    login,
    reset_password,
    logout,
    refresh,
    send_password_reset_email,
    delete_account
)
from .models import OkResponseModel, ResetPasswordResponseModel, LoginResponseModel, SendPasswordResetEmailResponseModel, DeleteAccountResponseModel

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
        "summary": "Reset Password (Logged In)",
        "description": "Reset password when logged in using session token",
        "responses": {200: {"model": ResetPasswordResponseModel}},
    },
    {
        "path": "/auth/send-password-reset-email",
        "endpoint": send_password_reset_email,
        "methods": ["POST"],
        "summary": "Send Password Reset Email",
        "description": "Send reset password link to email for users who forgot their password",
        "responses": {200: {"model": SendPasswordResetEmailResponseModel}},
    },
    {
        "path": "/auth/delete-account",
        "endpoint": delete_account,
        "methods": ["POST"],
        "summary": "Delete Account",
        "description": "Delete user account using session token",
        "responses": {200: {"model": DeleteAccountResponseModel}},
    },
]

for url in urls_patterns:
    url["tags"] = ["Authentication"]
