from .views import register_user, login

urls_patterns = [
    {"rule": "/auth/register", "view_func": register_user, "methods": ["GET"]},
    {"rule": "/auth/login", "view_func": login, "methods": ["GET"]},
]
