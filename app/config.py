import os

firebase_api_key = os.environ.get("FIREBASE_API_KEY")

if firebase_api_key is None:
    raise ValueError("Mohon inisialisasi FIREBASE_API_KEY kedalam environment CMD nya")
