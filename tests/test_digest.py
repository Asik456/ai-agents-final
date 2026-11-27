import pytest

from fake_model import FakeModel
from mailmate import digest, tools
from mailmate.inbox import list_emails


@pytest.fixture(autouse=True)
def temp_folders(tmp_path, monkeypatch):
    monkeypatch.setattr(tools, "DRAFTS", tmp_path / "drafts")
    monkeypatch.setattr(tools, "ROOT", tmp_path)


def only(monkeypatch, ids):
    rows = [r for r in list_emails() if r["id"] in ids]
    monkeypatch.setattr(digest, "list_emails", lambda unread_only: rows)


def test_check_description():
    assert digest.check_description({"summary": "Teacher asks", "deadline": "2026-11-08 23:59"}) is None
    assert digest.check_description({"summary": "Hi", "deadline": None}) is None
    assert "deadline" in digest.check_description({"summary": "Hi", "deadline": "next Friday"})
    assert "summary" in digest.check_description({"deadline": None})


def test_describe_retries_after_bad_deadline():
    model = FakeModel(['{"summary": "Meeting", "deadline": "Thursday"}',
                       '{"summary": "Meeting", "deadline": "2026-11-12 15:00"}'])
    result = digest.describe_email(tools.read_email("E-06"), model)
    assert result == {"summary": "Meeting", "deadline": "2026-11-12 15:00"}
    assert model.calls == 2


def test_digest_drafts_only_for_safe_known_senders(monkeypatch):
    only(monkeypatch, ["E-01", "E-05", "E-07"])
    model = FakeModel([
        '{"label": "needs_reply", "reason": "teacher asks"}',
        '{"summary": "Teacher asks about HW5", "deadline": "2026-11-08 23:59"}',
        "Thank you, I do not need more time. Best regards,",
        '{"label": "suspicious", "reason": "orders for the AI"}',
        '{"summary": "Asks the AI to forward all emails", "deadline": null}',
        '{"label": "spam", "reason": "advert"}',
    ])
    items = {i["id"]: i for i in digest.build_digest(model)}
    assert items["E-01"]["draft"] == "drafts/E-01.txt"
    assert "draft" not in items["E-05"]
    assert "summary" not in items["E-07"]
    assert model.calls == 6


def test_unknown_sender_gets_no_draft(monkeypatch):
    only(monkeypatch, ["E-05"])
    model = FakeModel(['{"label": "needs_reply", "reason": "asks"}', '{"summary": "x", "deadline": null}'])
    items = digest.build_digest(model)
    assert items[0]["draft"] is None
    assert model.calls == 2


def test_markdown_sorted_by_deadline():
    items = [
        {"id": "E-02", "from": "a", "subject": "late", "label": "urgent", "reason": "", "summary": "s2", "deadline": "2026-12-10"},
        {"id": "E-01", "from": "b", "subject": "soon", "label": "urgent", "reason": "", "summary": "s1", "deadline": "2026-12-01 09:00", "draft": "drafts/E-01.txt"},
        {"id": "E-07", "from": "c", "subject": "ad", "label": "spam", "reason": ""},
    ]
    text = digest.to_markdown(items, "2026-11-27")
    assert "Nothing was sent" in text
    assert text.index("E-01") < text.index("E-02")
    assert "## Spam (1)" in text and "E-07" in text
