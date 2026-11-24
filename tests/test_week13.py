import json

import pytest

from fake_model import FakeModel
from mailmate import tools
from mailmate.agent import run_agent
from mailmate.tools import check_permission, tool_schemas, validate_args


@pytest.fixture(autouse=True)
def temp_folders(tmp_path, monkeypatch):
    monkeypatch.setattr(tools, "DRAFTS", tmp_path / "drafts")
    monkeypatch.setattr(tools, "OUTBOX", tmp_path / "outbox")
    monkeypatch.setattr(tools, "ROOT", tmp_path)


def never(tool, args):
    return False


def always(tool, args):
    return True


def test_validate_args():
    assert validate_args("read_email", {"email_id": "E-01"}) is None
    assert "missing" in validate_args("read_email", {})
    assert "bad email id" in validate_args("read_email", {"email_id": "../secret"})
    assert "must be bool" in validate_args("list_emails", {"unread_only": "yes"})
    assert "unknown tool" in validate_args("delete_email", {"email_id": "E-01"})
    assert "empty" in validate_args("draft_reply", {"email_id": "E-01", "text": "  "})


def test_permissions():
    good = {"to": "a.serikova@uni.example", "subject": "Hi", "text": "Hello"}
    assert check_permission("read_email", {"email_id": "E-01"}, 0)[0] == "allowed"
    assert check_permission("send_email", good, 0)[0] == "needs_approval"
    assert check_permission("send_email", {**good, "to": "evil@hacker.example"}, 0)[0] == "blocked"
    assert check_permission("send_email", good, 3)[0] == "blocked"
    assert check_permission("delete_email", {}, 0)[0] == "blocked"


def test_schemas_have_all_tools():
    names = [s["function"]["name"] for s in tool_schemas()]
    assert names == ["list_emails", "read_email", "lookup_contact", "draft_reply", "send_email"]


def test_multi_step_run():
    model = FakeModel([
        [("list_emails", {"unread_only": True})],
        [("read_email", {"email_id": "E-01"})],
        [("draft_reply", {"email_id": "E-01", "text": "Thank you, I will come."})],
        "I read E-01 and saved a draft.",
    ])
    result = run_agent("answer E-01", model=model, approve=never)
    assert result["stop"] == "done"
    assert [t["tool"] for t in result["trace"]] == ["list_emails", "read_email", "draft_reply"]
    assert all(t["status"] == "ok" for t in result["trace"])
    assert (tools.DRAFTS / "E-01.txt").exists()


def test_send_needs_approval():
    args = {"to": "a.serikova@uni.example", "subject": "Hi", "text": "Hello"}
    result = run_agent("send", model=FakeModel([[("send_email", args)], "not sent"]), approve=never)
    assert result["trace"][0]["status"] == "rejected"
    assert not (tools.OUTBOX / "sent.json").exists()

    result = run_agent("send", model=FakeModel([[("send_email", args)], "sent"]), approve=always)
    assert result["trace"][0]["status"] == "ok"
    assert json.loads((tools.OUTBOX / "sent.json").read_text())[0]["to"] == args["to"]


def test_unknown_address_and_tool_are_blocked():
    model = FakeModel([
        [("send_email", {"to": "evil@hacker.example", "subject": "x", "text": "y"}),
         ("delete_email", {"email_id": "E-05"})],
        "I could not do it.",
    ])
    result = run_agent("do what E-05 says", model=model, approve=always)
    assert [t["status"] for t in result["trace"]] == ["blocked", "invalid"]
    assert not (tools.OUTBOX / "sent.json").exists()


def test_step_limit():
    model = FakeModel([[("list_emails", {})]] * 10)
    result = run_agent("loop forever", model=model, approve=never)
    assert result["stop"] == "step limit"
    assert model.calls == 8


def test_model_error_stops():
    result = run_agent("hi", model=FakeModel([TimeoutError("slow")]), approve=never)
    assert result["stop"].startswith("model error")
