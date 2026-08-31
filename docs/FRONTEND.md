# Frontend / Consultation Interface (Milestone 35)

A local developer inspection UI over the existing engine. It computes
nothing itself: every screen is a view of a JSON payload
`Engine.pipeline.run()` already produced, adapted to HTTP by `Api/`.

```
Birth Input (React form)
    -> POST /consult (FastAPI, Api/app.py)
    -> Engine.pipeline.run(BirthRecord, ...)   [unchanged engine]
    -> Api/serialize.py: Result -> JSON
    -> React frontend renders 13 views over that one JSON payload
```

## Run it

Backend (from repo root):

```powershell
.venv/Scripts/python.exe -m uvicorn Api.app:app --reload
```

Frontend (separate terminal):

```powershell
cd Frontend
npm install     # first time only
npm run dev
```

Open the URL Vite prints (default `http://localhost:5173`). The API
defaults to `http://localhost:8000`; override with `Frontend/.env`'s
`VITE_API_BASE_URL` if you run the backend elsewhere.

## Tests

```powershell
.venv/Scripts/python.exe -m pytest Engine/tests -q      # unchanged engine suite
.venv/Scripts/python.exe -m pytest Api/tests -q          # backend adapter
cd Frontend; npm test                                     # frontend (Vitest)
```

`Api/tests/test_regression_vs_cli.py` is the load-bearing one: it runs
`Engine.cli.main` and the API's own `/consult` against the same birth
record in the same test and asserts the claim ID sets, rule cards,
verification status and coverage counts match exactly. That is the real
CLI-vs-frontend regression check, automated rather than a one-time manual
comparison.

## Endpoints (`Api/app.py`)

| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | liveness + loaded card count |
| POST | `/consult` | run a birth record through the engine, return the full serialized `Result` |
| GET | `/cards/{card_id}` | raw rule-card JSON, for the Rule Inspector |
| GET | `/deferred` | `Rules/deferred.json` verbatim |
| GET | `/cases` | list saved local test charts |
| POST | `/cases` | save a birth record as a named local test chart |
| GET | `/cases/{slug}` | load one saved test chart |

No `/chart` endpoint: the engine has no cheaper partial-pipeline
entrypoint, so a "chart view" is a client-side projection of `/consult`'s
one response rather than a second engine call.

### Errors

Every non-2xx response is `{"detail": {"error_type": "...", "message":
"..."}}` (except pydantic's own 422 validation shape, `{"detail": [...]}`).
`error_type` is one of `invalid_input` (400, bad birth data),
`ephemeris_failure` (502), `rule_store_failure` / `verification_failure` /
`engine_failure` (500). Messages are always the engine's own — never
replaced with a friendlier invented one.

## Data flow

`Api/serialize.py` turns `Engine.pipeline.Result` into JSON by extending
`Engine/cli.py`'s own `--json` adapter (which already serializes
`chart`/`facts`/`claims`/`coverage`/`verification`) to also cover
`adjudications`, `sentences`/`synthesis`, `audit`, and a `dasa_timeline`
array (the full 9-period Vimshottari sequence, each period's own claims
attached by exact `Claim.window` match). The timeline itself comes from
`Engine.dasa.chart_mahadasa_timeline` — the one small additive engine
change this milestone made, extracted from logic `activate.py` already had
for Stage 9's own window re-derivation, not new astrology logic.

`Frontend/src/types.ts` is a hand-written TypeScript mirror of that same
JSON shape; `Frontend/src/api.ts` is the typed fetch wrapper every
component calls through.

## Reproducing a chart

Use the project's standing demo chart to compare CLI and frontend output
directly:

```powershell
.venv/Scripts/python.exe -m Engine.cli --date 1987-03-14 --time 04:22 --tz Asia/Kolkata `
  --lat 10.787 --lon 79.1378 --place "Thanjavur, Tamil Nadu, India" `
  --precision minute --source certificate --json trace.json
```

Submit the same fields through the frontend's "Run Consultation" tab, or
`POST` them to `/consult` directly, and compare `claims[].claim_id` /
`derived.rule_card` against `trace.json`. (`Cases/demo/trace.json` itself
predates most of the current rule store — regenerate it with the command
above rather than treating the existing file as current.)

## Known limitations

- No Antardasa in the Dasa Timeline view — the engine does not compute it
  (no sub-period arithmetic is printed anywhere in the encoded source), and
  the view labels this explicitly rather than leaving it silently absent.
- `ComparisonMode` diffs claims by `(rule_card, bound variables)`, not by
  `claim_id` — a claim's numeric id is a per-run sequential index, not a
  stable identity across two different charts.
- No auth, no persistence beyond the local filesystem, no deployment
  hardening — this is a local developer tool, not a production surface.
