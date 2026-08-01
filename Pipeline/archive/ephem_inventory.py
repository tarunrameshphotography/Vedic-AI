import os, re, hashlib, fitz
from pathlib import Path

# Resolved from this file's location, so the script runs from any working
# directory and on any machine. Pipeline/archive/ -> repository root.
E = Path(__file__).resolve().parents[2] / "Ephemeris"
files = sorted(os.listdir(E))
years, rows, hashes = [], [], {}
for f in files:
    p = os.path.join(E, f)
    h = hashlib.md5(open(p, "rb").read()).hexdigest()
    hashes.setdefault(h, []).append(f)
    m = re.search(r"ae_(\d{4})", f)
    y = int(m.group(1)) if m else None
    if y and "(1)" not in f:
        years.append(y)
    d = fitz.open(p)
    rows.append((f, y, d.page_count, os.path.getsize(p)))
    d.close()

print(f"files={len(files)}  distinct_years={len(set(years))}")
print(f"range={min(years)}-{max(years)}")
missing = sorted(set(range(min(years), max(years) + 1)) - set(years))
print(f"MISSING YEARS: {missing if missing else 'none'}")
dups = {k: v for k, v in hashes.items() if len(v) > 1}
print(f"BYTE-IDENTICAL DUPLICATES: {list(dups.values())}")
print(f"total pages across ephemeris: {sum(r[2] for r in rows)}")
