from .views import register_user, login, send_reset_password_email, reset_password

urls_patterns = [
    {"rule": "/auth/register", "view_func": register_user, "methods": ["POST"]},
    {"rule": "/auth/login", "view_func": login, "methods": ["POST"]},
    {"rule": "/auth/send-reset-password-email", "view_func": send_reset_password_email, "methods": ["POST"]},
    {"rule": "/auth/reset-password", "view_func": reset_password, "methods": ["POST"]},
]