"""`Cases/<slug>/chart.json` -- local, uncommitted test-chart manifests.

Reuses the existing `Cases/` directory convention -- already entirely
`.gitignore`'d, with the reason recorded inline there: case files hold real
people's birth details and do not belong in version control. A saved chart
here is the smallest manifest that reuses `Engine.chart.BirthRecord`'s own
field names rather than inventing a parallel schema; no personal data leaves
the local filesystem and this module never touches git.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASES_ROOT = ROOT / "Cases"

_SLUG_RE = re.compile(r"[^a-z0-9]+")


class CaseError(ValueError):
    """A case label could not be turned into a directory name, or is empty."""


def slugify(label: str) -> str:
    slug = _SLUG_RE.sub("_", label.strip().lower()).strip("_")
    if not slug:
        raise CaseError(f"label {label!r} has no usable characters for a directory name")
    return slug


def list_cases(cases_root: Path | None = None) -> list[dict]:
    cases_root = cases_root if cases_root is not None else DEFAULT_CASES_ROOT
    if not cases_root.exists():
        return []
    out = []
    for d in sorted(p for p in cases_root.iterdir() if p.is_dir()):
        manifest = d / "chart.json"
        if manifest.is_file():
            data = json.loads(manifest.read_text(encoding="utf-8"))
            data["slug"] = d.name
            out.append(data)
    return out


def load_case(slug: str, cases_root: Path | None = None) -> dict | None:
    cases_root = cases_root if cases_root is not None else DEFAULT_CASES_ROOT
    manifest = cases_root / slug / "chart.json"
    if not manifest.is_file():
        return None
    data = json.loads(manifest.read_text(encoding="utf-8"))
    data["slug"] = slug
    return data


def save_case(label: str, notes: str, birth: dict,
              cases_root: Path | None = None) -> dict:
    cases_root = cases_root if cases_root is not None else DEFAULT_CASES_ROOT
    slug = slugify(label)
    d = cases_root / slug
    d.mkdir(parents=True, exist_ok=True)
    manifest = {
        "label": label,
        "notes": notes,
        "birth": birth,
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    (d / "chart.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8",
    )
    data = dict(manifest)
    data["slug"] = slug
    return data
