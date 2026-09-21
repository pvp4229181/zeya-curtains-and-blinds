"""Import generated source images into optimized, responsive website assets."""
import json,re
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'zeya-website/assets/images'
records=json.loads((ROOT/'tools/design/ai-images.json').read_text(encoding='utf-8-sig'))
for record in records:
    source=Path(re.search(r' as (.+?\.png) by default',record['hint']).group(1))
    with Image.open(source) as im:
        im.convert('RGB').save(OUT/f"ai-{record['name']}.webp",quality=88,method=6)
        for width in (640,1024):
            if im.width>width:
                im.resize((width,round(im.height*width/im.width)),Image.Resampling.LANCZOS).convert('RGB').save(OUT/f"ai-{record['name']}-{width}.webp",quality=84,method=6)
    print(record['name'])
