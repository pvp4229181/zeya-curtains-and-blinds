from pathlib import Path
from PIL import Image
import pymupdf
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'zeya-website/assets/images'
def save(im,name):
    im.convert('RGB').save(OUT/(name+'.webp'),quality=90)
    for w in (640,1024,1600):
        p=OUT/f'{name}-{w}.webp'
        if im.width>w:
            im.resize((w,round(im.height*w/im.width)),Image.Resampling.LANCZOS).convert('RGB').save(p,quality=85)
        elif p.exists(): p.unlink()
def extract(pdf,chart):
    d=pymupdf.open(pdf)
    import io
    source=Image.open(io.BytesIO(d.extract_image(d[0].get_images()[0][0])['image']))
    # Coordinates refer to the single 1024 x 1536 flattened reference page.
    boxes={
      'hero-luxury-curtains':(218,40,508,339), 'intro-living-room':(10,454,288,598),
      'about-zeya-curtains':(517,42,759,376), 'curtains-category':(16,717,170,835),
      'blinds-category':(180,717,333,835), 'motorized-solutions':(343,717,495,835),
      'curtain-types':(118,909,168,1040), 'blind-types':(281,910,349,1040),
      'motorized-app-control':(364,950,495,1040), 'process-consultation':(532,715,1006,839),
      'fabric-consultation':(533,1002,681,1099), 'window-measurement':(692,1002,842,1099),
      'curtain-installation':(853,1002,1004,1099), 'quote-banner-fabric':(518,471,1009,506),
      'contact-interior':(405,1172,506,1428), 'cta-dubai-interior':(516,1369,1021,1454),
      'zeya-og-image':(10,454,288,598)}
    for name,box in boxes.items(): save(source.crop(box),name)
    from catalog import GROUPS
    chart=Image.open(chart)
    for group,products in GROUPS.items():
        for name,desc,box in products: save(chart.crop(box),'product-'+slug(name))
    # Use the larger, unobstructed reference chart interiors for broad hero areas.
    for name,box in {'hero-luxury-curtains':(218,817,378,953),'cta-dubai-interior':(1043,817,1198,953),'contact-interior':(957,132,1073,343)}.items(): save(chart.crop(box),name)
def slug(s):
    import re
    return re.sub('[^a-z0-9]+','-',s.lower()).strip('-')
if __name__=='__main__':
    import sys
    extract(*sys.argv[1:])
