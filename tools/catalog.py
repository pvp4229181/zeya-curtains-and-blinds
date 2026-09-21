"""Product copy transcribed from the supplied ZEYA chart; static page rendering."""
from html import escape
import re

def slug(s): return re.sub('[^a-z0-9]+','-',s.lower()).strip('-')
CURTAINS=[
('Sheer Curtains','Soft, light-filtering curtains that create a bright and airy atmosphere.'),
('Blackout Curtains','Maximum light control for better sleep and complete privacy.'),
('Linen Curtains','Natural texture and effortless elegance for modern interiors.'),
('Velvet Curtains','A luxurious feel with rich texture and superior drape.'),
('Wave Curtains','A sleek, modern look with smooth, continuous folds.'),
('Pinch Pleat Curtains','A classic, tailored style that adds sophistication to any space.'),
('Double / Layered Curtains','Combine sheers and blackout fabrics for versatility and style.'),
('Motorized Curtains','Convenience and luxury with automated control at your fingertips.')]
BLINDS=[
('Roller Blinds','A clean and minimal design, perfect for modern spaces.'),
('Zebra Blinds','Adjustable light and privacy with a stylish dual-layer design.'),
('Roman Blinds','A timeless, elegant look that adds warmth to any room.'),
('Venetian Blinds','Classic and versatile with precise light control.'),
('Wooden Blinds','Natural beauty and durability for a warm, sophisticated look.'),
('Faux Wood Blinds','The look of wood with added durability and moisture resistance.'),
('Vertical Blinds','A practical solution for large windows and sliding doors.'),
('Honeycomb Blinds','Energy-efficient design that helps insulate your space.'),
('Sunscreen Blinds','Reduce glare while maintaining your view and natural light.'),
('Motorized Blinds','Effortless control with smart automation for modern living.'),
('Outdoor / Zip Screen Blinds','Durable weather protection for patios, balconies and outdoor spaces.')]
MOTORIZED=[
('Motorized Curtains','Effortlessly open and close full-height curtains with smooth automated movement.'),
('Motorized Roller Blinds','Minimal, contemporary roller blinds with convenient powered operation.'),
('Motorized Zebra Blinds','Flexible light control with the distinctive layered design and automated operation.'),
('Motorized Roman Blinds','Classic fabric styling with modern convenience.'),
('Motorized Blackout Blinds','Convenient powered shading for better light control and privacy.'),
('Motorized Sheer Curtains','Beautifully diffused daylight with effortless operation.'),
('Motorized Double Curtains','Control sheer and blackout layers independently.'),
('Motorized Venetian Blinds','Clean, architectural look with automated adjustment.'),
('Motorized Vertical Blinds','A practical solution for wide windows and large areas.'),
('Motorized Outdoor / Zip Screens','Powered exterior screens for patios, terraces and balconies.'),
('Motorized Curtain Tracks','Discreet powered tracks for smooth and silent movement.'),
('Smart Window Automation','Convenient control of multiple curtains and blinds.')]
GROUPS={
'curtains':[(n,d,(218+i*123.3,132,331+i*123.3,343)) for i,(n,d) in enumerate(CURTAINS)],
'blinds':[(n,d,(218+i*82.3,491,292+i*82.3,682)) for i,(n,d) in enumerate(BLINDS)],
'motorized':[(n,d,(218+(i%6)*165,817+(i//6)*225,377+(i%6)*165,953+(i//6)*225)) for i,(n,d) in enumerate(MOTORIZED)]}
# The chart repeats Motorized Blinds; use its phone-control image.
GROUPS['blinds'][9]=(*BLINDS[9],(1125,491,1199,682))
LABELS={'curtains':'Curtains','blinds':'Blinds','motorized':'Motorized Window Solutions'}
INTROS={'curtains':'Elegant fabrics for every space. Explore custom-made curtains in a range of textures, styles and finishes.', 'blinds':'Modern, versatile options. Find the balance of light, privacy and style for your home or workplace.', 'motorized':'Smart living. Made simple. Explore powered curtains and blinds for effortless everyday comfort.'}

def cards(h,group):
    return '<div class="zeya-catalog-grid">'+''.join(f'<a class="zeya-product" href="product-{slug(n)}.html">{h.img("product-"+slug(n),n+" window treatment",sizes="(max-width:600px) 100vw, (max-width:1000px) 50vw, 25vw")}<div class="zeya-product__copy"><h3>{escape(n)}</h3><p>{escape(d)}</p><span>View details &rarr;</span></div></a>' for n,d,b in GROUPS[group])+'</div>'

def heading(title,desc,group=None):
    crumb='<a href="products.html">Products</a>'
    if group: crumb+=f' / <a href="{group}.html">{LABELS[group]}</a>'
    return f'<section class="zeya-catalog-head zeya-container"><nav class="zeya-crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> / {crumb}</nav><p class="zeya-eyebrow">ZEYA CURTAINS &amp; BLINDS</p><h1>{escape(title)}</h1><p>{escape(desc)}</p></section>'

def render(h):
    pages={}
    sections=[]
    for g,label in LABELS.items():
        section=f'<section class="zeya-container zeya-catalog-section" id="{g}"><div class="zeya-catalog-label"><div><p class="zeya-eyebrow">MADE FOR YOUR SPACE</p><h2>{label}</h2><p>{INTROS[g]}</p></div>{h.btn("Explore "+label,g+".html","gold")}</div>{cards(h,g)}</section>'
        sections.append(section)
        pages[g]=heading(label,INTROS[g])+f'<section class="zeya-container zeya-catalog-section"><h2 class="zeya-sr-only">Explore {label}</h2>{cards(h,g)}</section>'
        for n,d,b in GROUPS[g]:
            key='product-'+slug(n)
            pages[key]=heading(n,d,g)+f'<section class="zeya-container zeya-product-detail"><div>{h.img(key,n+" interior detail",eager=True)}</div><div><p class="zeya-eyebrow">MEASURED. DESIGNED. INSTALLED.</p><h2>Made to suit your space</h2><p>{escape(d)}</p><p>Choose your finish and discuss light, privacy and fitting requirements with ZEYA. We will confirm the right specification for your windows during your consultation.</p><ul class="zeya-list"><li>Made to your window measurements</li><li>Guidance on fabrics, colours and finishes</li><li>Professional installation</li></ul>{h.btn("Enquire about this product","contact.html?product="+slug(n),"gold")}<a class="zeya-back-link" href="{g}.html">&larr; Browse {label}</a></div></section><section class="zeya-container zeya-catalog-section"><h2>Explore the collection</h2>{cards(h,g)}</section>'
    pages['products']=heading('Our Products','Premium window solutions for every space.')+'<nav class="zeya-collection-nav zeya-container" aria-label="Product categories">'+''.join(f'<a href="{g}.html">{l} &rarr;</a>' for g,l in LABELS.items())+'</nav>'+''.join(sections)
    return pages
