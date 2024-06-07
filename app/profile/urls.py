from .views import (
    get_profile,
)

urls_patterns = [
    {
        "path": "/profile/get-user",
        "endpoint": get_profile,
        "methods": ["POST"],
    },
]

for url in urls_patterns:
    url["tags"] = ["Profile"]
