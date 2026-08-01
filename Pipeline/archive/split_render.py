import fitz, os, sys

pdf, outdir = sys.argv[1], sys.argv[2]
dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 300
ov = 0.02  # 2% overlap across the gutter so nothing is clipped
os.makedirs(outdir, exist_ok=True)
d = fitz.open(pdf)
n = 0
for i in range(d.page_count):
    pg = d[i]
    r = pg.rect
    mid = r.x0 + r.width / 2
    halves = [
        ("a", fitz.Rect(r.x0, r.y0, mid + r.width * ov, r.y1)),
        ("b", fitz.Rect(mid - r.width * ov, r.y0, r.x1, r.y1)),
    ]
    for tag, clip in halves:
        p = os.path.join(outdir, f"s{i+1:03d}{tag}.png")
        n += 1
        if os.path.exists(p):
            continue
        pix = pg.get_pixmap(dpi=dpi, clip=clip)
        pix.save(p)
print(f"spreads={d.page_count} half_images={n}")
