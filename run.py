import os
from app import main

if os.environ.get("FIREBASE_API_KEY") is None:
    api_key = input("Masukkan firebase api key anda\n=> ")

    os.environ.setdefault("FIREBASE_API_KEY")

main()
