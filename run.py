import os
from pathlib import Path
from subprocess import Popen
from argparse import ArgumentParser

firebase_file_key = "firebase-web-api.key"

if os.path.exists(firebase_file_key):
    os.environ.setdefault("FIREBASE_API_KEY", Path(firebase_file_key).read_text())

elif os.environ.get("FIREBASE_API_KEY") is None:
    api_key = input("Masukkan firebase api key anda\n=> ")

    os.environ.setdefault("FIREBASE_API_KEY", api_key)

argsparser = ArgumentParser("CC-App-CLI-Runner")
argsparser.add_argument("--debug", action="store_true")

args = argsparser.parse_args()

proc = Popen(["fastapi", "dev" if args.debug else "run", "app", "--port", "5000"])
proc.communicate()
