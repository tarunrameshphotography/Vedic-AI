import fitz, io, asyncio, sys, os, tempfile
from pathlib import Path
from PIL import Image
import winocr

# Resolved from this file's location. Rendered PNGs go to a scratch directory,
# not into the repository; override with VEDIC_OUT_DIR.
ROOT = Path(__file__).resolve().parents[2]
PDF = str(ROOT / "Books" / "uttkalamrita-kalidas-ps-sastri_compress.pdf")
OUT = os.environ.get("VEDIC_OUT_DIR", tempfile.gettempdir())

d = fitz.open(PDF)
for pno in [149, 195]:            # 0-indexed -> printed pages 150, 196
    pg = d[pno]
    pix = pg.get_pixmap(dpi=300)
    png = os.path.join(OUT, f"pg{pno+1}.png")
    pix.save(png)
    img = Image.open(png)
    r = asyncio.run(winocr.recognize_pil(img, 'en'))
    print(f"\n{'='*70}\nPAGE {pno+1}  size={pix.width}x{pix.height}\n{'='*70}")
    print(r.text)
