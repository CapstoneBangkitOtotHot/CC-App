from .views import (
    register_user,
    login,
    change_password,
    logout,
    refresh,
    send_password_reset_email,
    delete_account,
    get_status_email_verification,
    send_email_verification_handler,
)
from .models import (
    OkResponseModel,
    ChangePasswordResponseModel,
    LoginResponseModel,
    SendPasswordResetEmailResponseModel,
    DeleteAccountResponseModel,
    GetStatusEmailVerificationResponseModel,
)

urls_patterns = [
    {
        "path": "/auth/register",
        "endpoint": register_user,
        "methods": ["POST"],
        "summary": "Register",
        "description": "Register using email and password and send email confirmation",
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
        "path": "/auth/change-password",
        "endpoint": change_password,
        "methods": ["POST"],
        "summary": "Change Password",
        "description": "Change password when logged in using session token",
        "responses": {200: {"model": ChangePasswordResponseModel}},
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
    {
        "path": "/auth/get-status-email-confirmation",
        "endpoint": get_status_email_verification,
        "methods": ["GET"],
        "summary": "Get status email verification",
        "description": "Check if user email is verified or not",
        "responses": {200: {"model": GetStatusEmailVerificationResponseModel}},
    },
    {
        "path": "/auth/send-email-confirmation",
        "endpoint": send_email_verification_handler,
        "methods": ["POST"],
        "summary": "Send email confirmation",
        "description": "Send email confirmation to the user",
        "responses": {200: {"model": OkResponseModel}},
    },
]

for url in urls_patterns:
    url["tags"] = ["Authentication"]
