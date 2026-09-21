import os, sys
from PIL import Image
src = sys.argv[1]; n = int(sys.argv[2]) if len(sys.argv) > 2 else 3
target_w = int(sys.argv[3]) if len(sys.argv) > 3 else 860
im = Image.open(src).convert('RGB')
sc = target_w / im.width
im = im.resize((target_w, round(im.height*sc)), Image.LANCZOS)
h = im.height // n
out = []
base = os.path.splitext(src)[0]
for i in range(n):
    y0 = i*h; y1 = im.height if i == n-1 else (i+1)*h
    p = f"{base}_s{i+1}.png"
    im.crop((0,y0,im.width,y1)).save(p)
    out.append(p)
print("\n".join(out))
