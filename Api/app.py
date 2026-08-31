"""Thin JSON adapter over the existing engine.

Every route either (a) invokes `Engine.pipeline.run` and serializes the
`Result` it returns, or (b) reads a file the engine already writes/reads
(`Rules/deferred.json`, a rule card's own JSON, a saved `Cases/` manifest).
No astrology decision is made anywhere in this module -- see
`Api/serialize.py` and `Api/cases.py` for the same discipline.

Run:  .venv/Scripts/python.exe -m uvicorn Api.app:app --reload
"""

from __future__ import annotations

import json
import logging
import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from Engine.chart import BirthDataError, BirthRecord, ENGINE_VERSION
from Engine.ephemeris import EphemerisError
from Engine.pipeline import DEFAULT_CORPUS, DEFAULT_RULES, PipelineError, run
from Engine.rules import load_cards

from .cases import CaseError, list_cases, load_case, save_case
from .schemas import BirthInput, CaseInput
from .serialize import serialize_result

# The report contains degree signs, em-dashes and Devanagari -- Engine/cli.py
# reconfigures stdout/stderr for exactly this reason, and this process must
# not be able to die on a console that cannot encode them either.
for stream in (sys.stdout, sys.stderr):
    try:
        stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass

logger = logging.getLogger("vedic_ai.api")

RULES_DIR = DEFAULT_RULES
CORPUS_DIR = DEFAULT_CORPUS

app = FastAPI(title="VEDIC-AI Consultation API")

# Local development only (§24): the frontend dev server runs on a different
# port (Vite's default 5173) than this API (8000), so the browser needs CORS
# to call across them. Restricted to localhost -- this is not meant to be
# reachable from anywhere else.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", "http://127.0.0.1:5173",
        "http://localhost:4173", "http://127.0.0.1:4173",
    ],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


def _error(status: int, error_type: str, message: str) -> HTTPException:
    return HTTPException(status_code=status, detail={"error_type": error_type, "message": message})


@app.get("/health")
def health():
    cards = load_cards(RULES_DIR)
    return {"status": "ok", "engine_version": ENGINE_VERSION, "card_count": len(cards)}


@app.post("/consult")
def consult(payload: BirthInput):
    record = BirthRecord(
        date=payload.date, time=payload.time, timezone=payload.timezone,
        latitude=payload.latitude, longitude=payload.longitude,
        place_name=payload.place_name, name=payload.name,
        time_precision=payload.time_precision, time_source=payload.time_source,
        sex=payload.sex,
    )
    cards = load_cards(RULES_DIR)

    try:
        result = run(
            record, ayanamsa=payload.ayanamsa, house_system=payload.house_system,
            rules_dir=RULES_DIR, corpus_dir=CORPUS_DIR,
        )
    except BirthDataError as exc:
        raise _error(400, "invalid_input", str(exc)) from exc
    except EphemerisError as exc:
        raise _error(502, "ephemeris_failure", str(exc)) from exc
    except PipelineError as exc:
        msg = str(exc)
        if msg.startswith("rule store failed verification"):
            error_type = "rule_store_failure"
        elif msg.startswith("groundedness verification failed"):
            error_type = "verification_failure"
        else:
            error_type = "engine_failure"
        raise _error(500, error_type, msg) from exc
    except Exception as exc:  # noqa: BLE001 -- never swallowed, always surfaced (§19)
        logger.exception("unexpected engine failure")
        raise _error(500, "engine_failure", str(exc)) from exc

    return serialize_result(result, cards)


@app.get("/cards/{card_id}")
def get_card(card_id: str):
    for card in load_cards(RULES_DIR):
        if card.id == card_id:
            return card.raw
    raise _error(404, "not_found", f"no rule card {card_id!r} in the store")


@app.get("/deferred")
def deferred():
    path = Path(RULES_DIR) / "deferred.json"
    return json.loads(path.read_text(encoding="utf-8"))


@app.get("/cases")
def cases_index():
    return list_cases()


@app.get("/cases/{slug}")
def cases_get(slug: str):
    case = load_case(slug)
    if case is None:
        raise _error(404, "not_found", f"no saved case {slug!r}")
    return case


@app.post("/cases", status_code=201)
def cases_save(payload: CaseInput):
    try:
        return save_case(payload.label, payload.notes, payload.birth.model_dump())
    except CaseError as exc:
        raise _error(400, "invalid_input", str(exc)) from exc
