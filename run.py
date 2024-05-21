import os
from pathlib import Path

firebase_file_key = "firebase-web-api.key"

if os.path.exists(firebase_file_key):
    os.environ.setdefault("FIREBASE_API_KEY", Path(firebase_file_key).read_text())

elif os.environ.get("FIREBASE_API_KEY") is None:
    api_key = input("Masukkan firebase api key anda\n=> ")

    os.environ.setdefault("FIREBASE_API_KEY", api_key)

from app import main  # noqa: E402

main()
