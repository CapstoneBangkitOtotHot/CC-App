import json
from firebase_admin.storage import bucket
from pathlib import Path


def get_bucket():
    return bucket("model-inference-c241-ps005")


tips_json = json.loads((Path(__file__).parent.resolve() / "tips.json").read_text())


def get_tips(fruit_type, percentage):
    list_data = tips_json[fruit_type]

    for data in list_data:
        start, end = data["range"]
        tips = data["tips"]
        if percentage in range(start - 1, end + 1):
            return tips

    return None
