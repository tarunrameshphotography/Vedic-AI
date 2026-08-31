"""/cases -- always against a tmp_path root, never the real Cases/.

Real Cases/ holds actual people's birth details and is entirely
.gitignore'd; these tests must not read, list, or write anything under it.
`Api.cases.list_cases/load_case/save_case` resolve `DEFAULT_CASES_ROOT` as a
late-bound module global (not a frozen default argument), so patching
`Api.cases.DEFAULT_CASES_ROOT` redirects every call, including the ones made
through the FastAPI routes.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

import Api.cases as cases_module
from Api.app import app
from Api.cases import CaseError, list_cases, load_case, save_case

client = TestClient(app)


@pytest.fixture(autouse=True)
def isolated_cases_root(tmp_path, monkeypatch):
    monkeypatch.setattr(cases_module, "DEFAULT_CASES_ROOT", tmp_path)
    return tmp_path


BIRTH = {
    "date": "1990-06-15", "time": "06:00", "timezone": "Asia/Kolkata",
    "latitude": 13.0827, "longitude": 80.2707, "place_name": "Chennai",
    "time_precision": "minute", "time_source": "certificate", "sex": "unknown",
    "ayanamsa": "lahiri", "house_system": "whole_sign",
}


def test_list_is_empty_when_no_cases_saved():
    assert list_cases() == []


def test_save_then_load_round_trips_every_field():
    saved = save_case("Test Native", "some notes", BIRTH)
    assert saved["slug"] == "test_native"
    loaded = load_case("test_native")
    assert loaded["label"] == "Test Native"
    assert loaded["notes"] == "some notes"
    assert loaded["birth"] == BIRTH
    assert "created_at" in loaded


def test_load_missing_case_returns_none():
    assert load_case("does-not-exist") is None


def test_slugify_rejects_a_label_with_no_usable_characters():
    with pytest.raises(CaseError):
        save_case("!!!", "", BIRTH)


def test_api_cases_post_then_get_round_trip():
    r = client.post("/cases", json={"label": "API Native", "notes": "n", "birth": BIRTH})
    assert r.status_code == 201
    slug = r.json()["slug"]

    r2 = client.get("/cases")
    assert any(c["slug"] == slug for c in r2.json())

    r3 = client.get(f"/cases/{slug}")
    assert r3.status_code == 200
    assert r3.json()["label"] == "API Native"


def test_api_cases_get_missing_slug_is_404():
    r = client.get("/cases/does-not-exist")
    assert r.status_code == 404
    assert r.json()["detail"]["error_type"] == "not_found"


def test_api_cases_post_empty_label_is_400():
    r = client.post("/cases", json={"label": "   ---   ", "notes": "", "birth": BIRTH})
    assert r.status_code == 400
    assert r.json()["detail"]["error_type"] == "invalid_input"
