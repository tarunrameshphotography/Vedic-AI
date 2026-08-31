"""The API must not diverge from the CLI on the same input (§25/§26/§27).

Both are run live in this one test, not compared against a static fixture --
`Cases/demo/trace.json` is already known stale (a 9-claim snapshot from an
earlier milestone; the live engine produces 105+ today), so pinning against
it would assert agreement with something already wrong. This is the real
end-to-end comparison the master prompt's regression sections ask for,
automated rather than left as a one-time manual check.
"""

from __future__ import annotations

import json

from fastapi.testclient import TestClient

from Api.app import app
from Engine.cli import main as cli_main

client = TestClient(app)

DEMO_BIRTH = {
    "date": "1987-03-14", "time": "04:22", "timezone": "Asia/Kolkata",
    "latitude": 10.787, "longitude": 79.1378,
    "place_name": "Thanjavur, Tamil Nadu, India",
    "time_precision": "minute", "time_source": "certificate",
}


def test_api_claims_and_verification_match_the_cli_exactly(tmp_path):
    json_path = tmp_path / "trace.json"
    exit_code = cli_main([
        "--date", DEMO_BIRTH["date"], "--time", DEMO_BIRTH["time"],
        "--tz", DEMO_BIRTH["timezone"],
        "--lat", str(DEMO_BIRTH["latitude"]), "--lon", str(DEMO_BIRTH["longitude"]),
        "--place", DEMO_BIRTH["place_name"],
        "--precision", DEMO_BIRTH["time_precision"], "--source", DEMO_BIRTH["time_source"],
        "--json", str(json_path),
    ])
    assert exit_code == 0
    cli_trace = json.loads(json_path.read_text(encoding="utf-8"))

    api_response = client.post("/consult", json=DEMO_BIRTH)
    assert api_response.status_code == 200
    api_body = api_response.json()

    cli_claim_ids = {c["claim_id"] for c in cli_trace["claims"]}
    api_claim_ids = {c["claim_id"] for c in api_body["claims"]}
    assert cli_claim_ids == api_claim_ids
    assert cli_claim_ids, "the demo chart is known to activate claims today"

    cli_rule_cards = sorted(c["derived"]["rule_card"] for c in cli_trace["claims"])
    api_rule_cards = sorted(c["derived"]["rule_card"] for c in api_body["claims"])
    assert cli_rule_cards == api_rule_cards

    assert cli_trace["chart"]["bundle_id"] == api_body["chart"]["bundle_id"]
    assert cli_trace["verification"]["ok"] == api_body["verification"]["ok"] is True
    assert cli_trace["coverage"]["claims_activated"] == api_body["coverage"]["claims_activated"]
    assert cli_trace["coverage"]["inert_cards"] == api_body["coverage"]["inert_cards"]
    assert cli_trace["coverage"]["reference_cards"] == api_body["coverage"]["reference_cards"]

    # Every claim the API's own dasa timeline attaches to a period must be a
    # real claim the CLI also produced -- the timeline grouping invents
    # nothing beyond Claim.window, which both already agree on above.
    timeline_claim_ids = {cid for p in api_body["dasa_timeline"] for cid in p["claim_ids"]}
    assert timeline_claim_ids <= api_claim_ids
    assert timeline_claim_ids, "at least one dasa claim fires on this chart"
