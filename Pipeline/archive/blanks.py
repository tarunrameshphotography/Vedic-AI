import os, sys
from PIL import Image

d = sys.argv[1]
files = sorted(f for f in os.listdir(d) if f.endswith(".png"))
blank, faint, normal = [], [], []
for f in files:
    im = Image.open(os.path.join(d, f)).convert("L").resize((300, 450))
    px = list(im.getdata())
    dark = sum(1 for p in px if p < 140) / len(px)
    if dark < 0.005:
        blank.append(f)
    elif dark < 0.02:
        faint.append((f, round(dark, 4)))
    else:
        normal.append(f)
print(f"total={len(files)}  blank={len(blank)}  faint={len(faint)}  normal={len(normal)}")
print("BLANK:", [b[:-4] for b in blank])
print("FAINT:", [(a[:-4], b) for a, b in faint])
