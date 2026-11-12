"""
Unit tests — Twilio and the scheduler are mocked so no credentials are needed.
Run with:  pytest tests/
"""
import os
import pytest
from datetime import datetime, timezone, timedelta
from unittest.mock import patch, MagicMock

os.environ.setdefault("TWILIO_ACCOUNT_SID", "ACtest")
os.environ.setdefault("TWILIO_AUTH_TOKEN", "testtoken")

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@patch("app.routes.send_whatsapp_message", return_value="SM123")
def test_send_now(mock_send):
    resp = client.post("/whatsapp/send", json={"to": "whatsapp:+919876543210", "message": "Hello"})
    assert resp.status_code == 200
    assert resp.json()["message_sid"] == "SM123"
    mock_send.assert_called_once()


@patch("app.routes.schedule_message")
def test_schedule(mock_sched):
    future = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
    mock_sched.return_value = MagicMock(
        job_id="abc",
        to="whatsapp:+919876543210",
        message="Hi",
        send_at=datetime.now(timezone.utc) + timedelta(hours=1),
        recurrence=None,
        status="pending",
        model_dump=lambda: {
            "job_id": "abc",
            "to": "whatsapp:+919876543210",
            "message": "Hi",
            "send_at": future,
            "recurrence": None,
            "status": "pending",
        },
    )
    resp = client.post(
        "/whatsapp/schedule",
        json={"to": "whatsapp:+919876543210", "message": "Hi", "send_at": future},
    )
    assert resp.status_code == 201
    mock_sched.assert_called_once()


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_get_missing_job():
    resp = client.get("/whatsapp/jobs/nonexistent-id")
    assert resp.status_code == 404


def test_invalid_to_number():
    resp = client.post("/whatsapp/send", json={"to": "+919876543210", "message": "Hi"})
    assert resp.status_code == 422  # validation error — missing "whatsapp:" prefix
