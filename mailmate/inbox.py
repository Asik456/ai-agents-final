import json
import re
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
ID_PATTERN = re.compile(r"^E-\d{2}$")


def load_emails():
    return json.loads((DATA / "inbox.json").read_text(encoding="utf-8"))["emails"]


def get_email(email_id):
    for email in load_emails():
        if email["id"] == email_id:
            return email
    return None


def list_emails(unread_only=False):
    result = []
    for email in load_emails():
        if unread_only and not email["unread"]:
            continue
        result.append({
            "id": email["id"],
            "from": email["from"],
            "subject": email["subject"] or "(no subject)",
            "date": email["date"],
            "unread": email["unread"],
        })
    return result


def read_email(email_id):
    if not isinstance(email_id, str) or not ID_PATTERN.match(email_id):
        return {"error": f"bad email id {email_id!r}, it must look like E-01"}
    email = get_email(email_id)
    if email is None:
        return {"error": f"no email with id {email_id}"}
    return {**email, "subject": email["subject"] or "(no subject)", "untrusted": True}
