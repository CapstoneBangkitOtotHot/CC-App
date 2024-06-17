from .backend import predict
from .models import PredictImageResponseModel

urls_patterns = [
    {
        "path": "/api/predict/fruit",
        "endpoint": predict,
        "methods": ["POST"],
        "summary": "Process image to be predicted",
        "description": """Process image and return data that has been segmented, processed, \
        and analyzed its freshness""",
        "responses": {200: {"model": PredictImageResponseModel}},
    },
]

for url in urls_patterns:
    url["tags"] = ["ML BACKEND"]
