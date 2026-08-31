from __future__ import annotations

from fastapi.testclient import TestClient

from Api.app import app

client = TestClient(app)


def test_health_ok():
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert body["card_count"] > 0
    assert body["engine_version"]
