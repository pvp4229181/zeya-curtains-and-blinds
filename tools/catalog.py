"""Product copy transcribed from the supplied ZEYA chart; static page rendering."""
from html import escape
from home_content import services_section, why_band
import sectors
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
('Motorized Blinds','Effortless control with smart automation for modern living.')]
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
# Not on the supplied chart, so these carry no crop box; extract_assets skips
# them and asset_map points each one at an existing generated visual.
ACCESSORIES=[
('Curtain Rods & Poles','Finished metal and wooden poles sized and fitted to your window.'),
('Curtain Tracks','Slim, quiet tracks for straight runs, bay windows and ceiling fixing.'),
('Tiebacks & Holdbacks','Fabric ties, tassels and metal holdbacks that shape the drape.'),
('Curtain Rings & Hooks','The fittings behind a clean heading and a smooth glide.'),
('Finials & End Caps','The finishing detail at each end of the pole, in matching finishes.'),
('Pelmets & Valances','A tailored top treatment that conceals the track and frames the window.'),
('Curtain Linings','Blackout, thermal and dim-out linings that change how a curtain performs.'),
('Motorized Accessories','Remotes, wall switches, chargers and brackets for powered systems.')]
GROUPS={
'curtains':[(n,d,(218+i*123.3,132,331+i*123.3,343)) for i,(n,d) in enumerate(CURTAINS)],
'blinds':[(n,d,(218+i*82.3,491,292+i*82.3,682)) for i,(n,d) in enumerate(BLINDS)],
'motorized':[(n,d,(218+(i%6)*165,817+(i//6)*225,377+(i%6)*165,953+(i//6)*225)) for i,(n,d) in enumerate(MOTORIZED)],
'curtain-accessories':[(n,d,None) for n,d in ACCESSORIES]}
# The chart repeats Motorized Blinds; use its phone-control image.
GROUPS['blinds'][9]=(*BLINDS[9],(1125,491,1199,682))
LABELS={'curtains':'Curtains','blinds':'Blinds','motorized':'Motorized Window Solutions','curtain-accessories':'Curtain Accessories'}
# Everything the Collections menu lists: the product collections, then the
# sector page, which shows the same range by the spaces it serves.
MENU={**LABELS,sectors.SLUG:sectors.LABEL}
# The Collections dropdown: a thumbnail and one line per entry. The thumbnails
# are the small encodes of each collection's cover, as they render at 64px.
MENU_NOTES={'curtains':('signature-curtains-640','Sheer, blackout, linen, velvet & wave'),
 'blinds':('signature-blinds-640','Roller, zebra, Roman, Venetian & wooden'),
 'motorized':('signature-motorized-640','Smart control for curtains & blinds'),
 'curtain-accessories':('ai-tracks-640','Poles, tracks, tiebacks & linings'),
 sectors.SLUG:('signature-hero-640','Solutions for homes, offices, hotels, cafés & clinics')}
INTROS={'curtains':'Elegant fabrics for every space. Explore custom-made curtains in a range of textures, styles and finishes.', 'blinds':'Modern, versatile options. Find the balance of light, privacy and style for your home or workplace.', 'motorized':'Smart living. Made simple. Explore powered curtains and blinds for effortless everyday comfort.', 'curtain-accessories':'The details that finish the window. Poles, tracks, linings and fittings chosen to match your curtains.'}
# The hero photograph that opens each collection page.
COVERS={'curtains':'curtains-category','blinds':'blinds-category','motorized':'motorized-solutions','curtain-accessories':'accessories-category'}


def cards(h,group,exclude=None,limit=None):
    """The product grid. Each card is a full-bleed image with the name and the
    one-line description sitting over it, so a row of cards reads as a set of
    photographs rather than a table of boxes."""
    products=[p for p in GROUPS[group] if p[0]!=exclude]
    if limit: products=products[:limit]
    return '<div class="zeya-catalog-grid">'+''.join(
        '<a class="zeya-product" href="product-{slug}.html">'
        '<div class="zeya-product__image">{image}'
        '<span class="zeya-product__veil" aria-hidden="true"></span></div>'
        '<div class="zeya-product__copy"><h3>{name}</h3><p>{desc}</p>'
        '<span class="zeya-product__action">Discover the details'
        '<span aria-hidden="true">&#8594;</span></span></div></a>'.format(
            slug=slug(n), name=escape(n), desc=escape(d),
            image=h.img("product-"+slug(n),"Interior inspiration: "+n,
                        sizes="(max-width:600px) 100vw, (max-width:1000px) 50vw, 33vw"))
        for n,d,b in products)+'</div>'


def motion_section(h):
    """The motorized page's hero: the film full-bleed behind the smart-home copy.

    It stands in for the image hero, so it carries the page's <h1> and clears
    the transparent header like the hero does.

    Like the home hero, the markup ships only a poster: main.js loads the film
    once it scrolls into view (the light encode on phones), plays it while in
    view, and never fetches it for reduced-motion visitors unless they press
    play. The toggle is the pause control for a loop that runs past 5s.
    """
    works=''.join(f'<li>{name}</li>' for name in
                  ('Amazon Alexa','Google Home','Somfy','Tuya'))
    play='<svg class="zeya-motion__play" viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path d="M4 2.5v11l9.5-5.5z"/></svg>'
    pause='<svg class="zeya-motion__pause" viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path d="M3.5 2.5h3v11h-3zM9.5 2.5h3v11h-3z"/></svg>'
    return (f'<section class="zeya-section--chocolate zeya-motion" aria-labelledby="zeya-motion-title">'
            f'<div class="zeya-motion__media">'
            f'<video class="zeya-motion__video" data-zeya-motion-video'
            f' data-src="assets/videos/motorized-in-operation.mp4"'
            f' data-src-sm="assets/videos/motorized-in-operation-854.mp4"'
            f' poster="assets/images/motorized-in-operation-poster.webp"'
            f' width="1280" height="720" muted loop playsinline preload="none"'
            f' aria-hidden="true" tabindex="-1"></video></div>'
            f'<div class="zeya-motion__scrim" aria-hidden="true"></div>'
            f'<button class="zeya-motion__toggle" type="button" data-zeya-motion-toggle'
            f' aria-label="Play video" hidden>{play}{pause}</button>'
            f'<div class="zeya-container zeya-motion__inner">'
            f'<div class="zeya-motion__copy">'
            f'<p class="zeya-eyebrow zeya-motion__eyebrow">Motorized Window Solutions</p>'
            f'<h1 id="zeya-motion-title">Effortless control.<br><em>Intelligent comfort.</em></h1>'
            f'<p class="zeya-motion__lead">We offer motorised curtain solutions that seamlessly '
            f'integrate with Amazon Alexa, Google Home, Somfy, Tuya and more, bringing effortless '
            f'control and intelligent comfort to your home.</p>'
            f'<div class="zeya-motion__works"><span>Works with</span>'
            f'<ul aria-label="Works with">{works}<li>And more</li></ul></div>'
            f'<div class="zeya-motion__actions">'
            f'{h.btn("Ask about smart control","contact.html?product=smart-window-automation","gold")}'
            f'{h.btn("Browse the range","#range","outline")}</div></div>'
            f'</div></section>')


def crumbs(title,group=None):
    links='<a href="index.html">Home</a><span aria-hidden="true">/</span><a href="products.html">Products</a>'
    if group: links+=f'<span aria-hidden="true">/</span><a href="{group}.html">{LABELS[group]}</a>'
    return f'<nav class="zeya-crumbs" aria-label="Breadcrumb">{links}<span aria-hidden="true">/</span><span aria-current="page">{escape(title)}</span></nav>'


def render(h):
    pages={}; sections=[]
    for g,label in LABELS.items():
        section=(f'<section class="zeya-section zeya-container zeya-catalog-section" id="{g}">'
                 f'<div class="zeya-section-heading">'
                 f'<p class="zeya-eyebrow">{len(GROUPS[g]):02d} ways to make it yours</p>'
                 f'<div><div class="zeya-section-heading__row"><h2>{label}</h2>'
                 f'{h.btn("Explore collection",g+".html","outline")}</div>'
                 f'<p>{INTROS[g]}</p></div></div>'
                 f'{cards(h,g,limit=3)}</section>')
        sections.append(section)

        # ---- the collection page -----------------------------------------
        # The motorized page opens on its film instead of the image hero.
        opener=(motion_section(h) if g=='motorized' else
                h.hero(COVERS[g],label+' in a considered Dubai interior',escape(label),
                       eyebrow='The ZEYA collection',sub=INTROS[g],
                       crumbs=crumbs(label)))
        pages[g]=(opener
                  +f'<section class="zeya-section zeya-container zeya-catalog-section" id="range">'
                   f'<div class="zeya-catalog-toolbar"><h2>Explore the collection</h2>'
                   f'<span>{len(GROUPS[g])} options &middot; Made to measure</span></div>'
                   f'{cards(h,g)}</section>')

        # ---- one detail page per product ---------------------------------
        for n,d,b in GROUPS[g]:
            key='product-'+slug(n)
            operation='Motorized operation' if g=='motorized' or n.startswith('Motorized') else 'Discuss manual or motorized options'
            pages[key]=(
                h.hero(key,'Interior inspiration: '+n,escape(n),
                       eyebrow=escape(label)+' &middot; Made to measure',
                       sub=escape(d),
                       actions=h.btn('Enquire about this product',
                                     'contact.html?product='+slug(n),'gold'),
                       crumbs=crumbs(n,g),variant='product')
                +f'<section class="zeya-section zeya-container zeya-product-detail">'
                 f'<figure class="zeya-product-detail__media">'
                 f'{h.img(key,"Interior inspiration: "+n,sizes="(max-width:700px) 100vw, 50vw")}'
                 f'</figure>'
                 f'<div class="zeya-detail-copy"><p class="zeya-eyebrow">About this product</p>'
                 f'<h2>{escape(n)}</h2><p class="zeya-detail-lead">{escape(d)}</p>'
                 f'<p>Thoughtfully selected for your windows. We’ll help you choose the '
                 f'right finish, proportion and fitting for your space.</p>'
                 f'<dl class="zeya-specs">'
                 f'<div><dt>Made for</dt><dd>Your window measurements</dd></div>'
                 f'<div><dt>Finish</dt><dd>Selected during consultation</dd></div>'
                 f'<div><dt>Control</dt><dd>{operation}</dd></div>'
                 f'<div><dt>Service</dt><dd>Measured, designed &amp; installed</dd></div></dl>'
                 f'<div class="zeya-enquire">'
                 f'<p class="zeya-enquire__title">Interested in {escape(n)}?</p>'
                 f'<p class="zeya-enquire__note">Home visit, fabric samples and a clear '
                 f'quotation, anywhere in Dubai.</p>'
                 f'<div class="zeya-enquire__actions">'
                 f'{h.btn("Enquire now","contact.html?product="+slug(n),"gold")}'
                 f'<a class="zeya-btn zeya-btn--whatsapp" data-zeya-wa="product" '
                 f'data-zeya-wa-product="{escape(n)}" hidden>'
                 f'<svg aria-hidden="true" focusable="false"><use href="#zeya-i-whatsapp"></use></svg>'
                 f'Chat on WhatsApp</a></div></div>'
                 f'<a class="zeya-back-link" href="{g}.html">Browse all {label.lower()} &rarr;</a>'
                 f'</div></section>'
                 f'<section class="zeya-section zeya-section--chocolate">'
                 f'<div class="zeya-container zeya-catalog-section">'
                 f'<div class="zeya-catalog-toolbar"><h2>You may also like</h2>'
                 f'<a class="zeya-back-link" href="{g}.html">View collection &rarr;</a></div>'
                 f'{cards(h,g,exclude=n,limit=3)}</div></section>'
                +services_section(h,product=escape(n))
                +why_band(h))

    pages['products']=(
        h.hero('hero-luxury-curtains','Curtains and blinds in a sunlit Dubai interior',
               'Find your kind of light.',eyebrow='The ZEYA collection',
               sub='Curtains, blinds, motorized solutions and the accessories that finish them. '
                   'Four collections, made around you.',
               crumbs=crumbs('Products'))
        +'<nav class="zeya-collection-nav zeya-container" aria-label="Product categories">'
        +''.join(f'<a href="#{g}">{escape(l)}<span aria-hidden="true">&#8595;</span></a>' for g,l in MENU.items())
        +'</nav>'+''.join(sections)+sectors.teaser(h))
    pages[sectors.SLUG]=sectors.page(h,crumbs)
    return pages
