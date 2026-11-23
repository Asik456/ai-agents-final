from fake_model import FakeModel

from mailmate.inbox import list_emails, read_email
from mailmate.summary import summarize
from mailmate.triage import parse_label, triage_email


def test_list_emails_and_unread_filter():
    assert len(list_emails()) == 13
    assert all(email["unread"] for email in list_emails(unread_only=True))
    assert len(list_emails(unread_only=True)) == 12


def test_read_email_rejects_bad_or_unknown_id():
    assert "error" in read_email("E-99")
    assert "error" in read_email("delete everything")
    assert "error" in read_email(5)
    assert read_email("E-01")["untrusted"] is True


def test_email_without_subject_gets_placeholder():
    assert read_email("E-10")["subject"] == "(no subject)"


def test_good_json_label_is_accepted():
    model = FakeModel(['{"label": "spam", "reason": "an ad"}'])
    assert triage_email("E-07", model) == {"id": "E-07", "label": "spam", "reason": "an ad"}


def test_bad_json_is_retried_then_accepted():
    model = FakeModel(["I think this is spam", '{"label": "spam", "reason": "an ad"}'])
    result = triage_email("E-07", model)
    assert result["label"] == "spam"
    assert model.calls == 2


def test_wrong_label_twice_gives_error():
    model = FakeModel(['{"label": "important", "reason": "x"}', '{"label": "important", "reason": "x"}'])
    result = triage_email("E-01", model)
    assert "error" in result
    assert "label must be one of" in result["error"]


def test_parse_label_checks_fields():
    assert parse_label('```json\n{"label": "info", "reason": "ok"}\n```')[0]["label"] == "info"
    assert parse_label('{"label": "info"}')[0] is None
    assert parse_label("[1, 2]")[0] is None


def test_model_failure_does_not_crash():
    model = FakeModel([TimeoutError("api timeout"), TimeoutError("api timeout")])
    result = triage_email("E-01", model)
    assert "model call failed" in result["error"]
    assert summarize("E-01", FakeModel([TimeoutError("api timeout")]))["ok"] is False
