from firebase_admin import initialize_app
from firebase_admin.credentials import Certificate
from firebase_admin.storage import bucket
from pathlib import Path

def get_bucket():
    return bucket("model-inference-c241-ps005")