import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"


def load_emails():
    return json.loads((DATA / "inbox.json").read_text(encoding="utf-8"))["emails"]


def get_email(email_id):
    for email in load_emails():
        if email["id"] == email_id:
            return email
    return None
