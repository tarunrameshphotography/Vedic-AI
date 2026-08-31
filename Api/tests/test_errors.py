"""Error taxonomy -> HTTP status (§19): distinct, never swallowed, never
downgraded to a friendlier invented message.

`BirthDataError` and the pydantic-validation case are triggered for real
(a genuinely unknown IANA zone; a genuinely incomplete request body).
`EphemerisError` and `PipelineError`'s two distinct messages are forced by
monkeypatching `Api.app.run` -- reproducing a live ephemeris failure or a
corrupted rule store deterministically is not practical here, and what is
under test is the app's own mapping from exception to status code, not the
engine internals that already have their own test suites.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

import Api.app as app_module
from Api.app import app
from Engine.ephemeris import EphemerisError
from Engine.pipeline import PipelineError

client = TestClient(app)

BIRTH = {
    "date": "1990-06-15", "time": "06:00", "timezone": "Asia/Kolkata",
    "latitude": 13.0827, "longitude": 80.2707,
}


def test_birth_data_error_via_real_invalid_timezone_is_400():
    r = client.post("/consult", json=dict(BIRTH, timezone="Not/A/Zone"))
    assert r.status_code == 400
    assert r.json()["detail"]["error_type"] == "invalid_input"


def test_missing_required_field_is_422():
    r = client.post("/consult", json={"date": "1990-06-15"})
    assert r.status_code == 422


@pytest.mark.parametrize("exc,status,error_type", [
    (EphemerisError("ephemeris file missing"), 502, "ephemeris_failure"),
    (PipelineError("rule store failed verification; refusing to run:\n  x"),
     500, "rule_store_failure"),
    (PipelineError("groundedness verification failed; report not emitted:\n  x"),
     500, "verification_failure"),
    (PipelineError("some other pipeline problem"), 500, "engine_failure"),
    (RuntimeError("totally unexpected"), 500, "engine_failure"),
])
def test_engine_exceptions_map_to_the_right_status_and_error_type(
    monkeypatch, exc, status, error_type,
):
    def fake_run(*args, **kwargs):
        raise exc
    monkeypatch.setattr(app_module, "run", fake_run)

    r = client.post("/consult", json=BIRTH)
    assert r.status_code == status
    detail = r.json()["detail"]
    assert detail["error_type"] == error_type
    assert str(exc) in detail["message"]
