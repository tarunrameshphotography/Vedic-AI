import fitz, os, sys

pdf = sys.argv[1]
outdir = sys.argv[2]
dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 200
os.makedirs(outdir, exist_ok=True)
d = fitz.open(pdf)
print(f"pages={d.page_count}")
for i in range(d.page_count):
    p = os.path.join(outdir, f"p{i+1:03d}.png")
    if os.path.exists(p):
        continue
    pix = d[i].get_pixmap(dpi=dpi)
    pix.save(p)
    if i < 3 or i % 25 == 0:
        print(f"  p{i+1:03d} {pix.width}x{pix.height} {os.path.getsize(p)//1024}KB")
print("done")
