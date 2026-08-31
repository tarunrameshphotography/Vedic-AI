"""POST /consult against the project's own standing demo chart.

Not pinned to `Cases/demo/trace.json`'s claim count -- that file is a stale
snapshot from an earlier milestone (9 claims, predating most of the current
store) and was never regenerated; comparing against it would assert the API
matches a fixture that is already known to disagree with the live engine.
The real regression oracle (live CLI vs live API, same input, same run) is
`test_regression_vs_cli.py`. This file checks response *shape* -- every
field the master prompt's screens need is present and typed as expected --
against the project's real, current rule store.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from Api.app import app

client = TestClient(app)

DEMO_BIRTH = {
    "date": "1987-03-14", "time": "04:22", "timezone": "Asia/Kolkata",
    "latitude": 10.787, "longitude": 79.1378,
    "place_name": "Thanjavur, Tamil Nadu, India",
    "time_precision": "minute", "time_source": "certificate",
}


def _consult(**overrides):
    body = dict(DEMO_BIRTH)
    body.update(overrides)
    return client.post("/consult", json=body)


def test_consult_returns_200_and_a_real_result():
    r = _consult()
    assert r.status_code == 200
    body = r.json()
    assert body["claims"], "the demo chart is known to activate claims today"
    assert body["verification"]["ok"] is True


def test_claim_shape_carries_every_field_the_master_prompt_needs():
    body = _consult().json()
    claim = body["claims"][0]
    for field in ("claim_id", "astronomical", "derived", "source", "passage",
                  "weight", "specificity", "tier", "stability", "text", "window"):
        assert field in claim
    for field in ("book_id", "book_title", "chapter", "verse", "tier"):
        assert field in claim["source"]
    for field in ("quote", "quote_display", "page_anchor", "quote_sha256"):
        assert field in claim["passage"]


def test_dasa_timeline_has_nine_periods_with_attached_claims():
    body = _consult().json()
    timeline = body["dasa_timeline"]
    assert len(timeline) == 9
    assert {p["ordinal"] for p in timeline} == set(range(1, 10))
    for p in timeline:
        for field in ("graha", "years", "start", "end", "balance_at_birth", "claim_ids"):
            assert field in p
    assert any(p["claim_ids"] for p in timeline), "at least one dasa claim fires on this chart"


def test_adjudications_carry_full_provenance_on_both_parties():
    body = _consult().json()
    assert body["adjudications"], "the demo chart is known to produce adjudications today"
    adj = body["adjudications"][0]
    for field in ("subject", "relationship", "resolution", "reason", "parties",
                  "basis", "declared_as", "claim_ids"):
        assert field in adj
    assert len(adj["parties"]) >= 2
    for party in adj["parties"]:
        for field in ("card", "book", "chapter", "verse", "authority", "statement",
                      "activation", "claim_ids"):
            assert field in party


def test_coverage_carries_the_per_chart_not_triggered_split():
    body = _consult().json()
    for field in ("cards_in_store", "candidates_from_index", "claims_activated",
                  "inert_cards", "out_of_scope", "reference_cards", "not_covered",
                  "loaded_doctrine"):
        assert field in body["coverage"]


def test_chart_carries_houses_and_bodies():
    body = _consult().json()
    chart = body["chart"]
    assert chart["ascendant_sign"]
    assert len(chart["bodies"]) == 9  # nine classical grahas incl. Rahu/Ketu
    assert chart["houses"]["system"] == "whole_sign"


def test_consultation_and_audit_text_are_present():
    body = _consult().json()
    assert isinstance(body["consultation"], str) and body["consultation"]
    assert isinstance(body["audit"], str) and body["audit"]


def test_synthesis_and_sentences_shape():
    body = _consult().json()
    for field in ("concentrations", "themes", "method_note", "total_claims"):
        assert field in body["synthesis"]
    assert body["sentences"]
    for s in body["sentences"][:3]:
        assert "text" in s and "claim_ids" in s and "part" in s
