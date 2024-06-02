from firebase_admin import initialize_app
from firebase_admin.credentials import Certificate
from pathlib import Path

account_key = Path(__file__).parent.parent.resolve() / "serviceaccountkey.json"

if not account_key.exists():
    raise ValueError("Mohon buat service account API key untuk keperluan firebase")

app = initialize_app(Certificate(account_key))
