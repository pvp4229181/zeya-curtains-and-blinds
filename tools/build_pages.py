#!/usr/bin/env python3
"""
Build the five static ZEYA pages from one shared shell.

    python tools/build_pages.py

The shell (head, header, footer band, final CTA, footer) lives here so the
pages can never drift apart. Page bodies live in page_content.py. The output
is plain HTML5 — no build step is required to *serve* the site, only to
regenerate it after editing the shell.
"""
import os
import re

from PIL import Image

import page_content
import catalog

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SITE = os.path.join(ROOT, "zeya-website")
IMAGES = os.path.join(SITE, "assets", "images")
VARIANTS = (640, 1024, 1600)

_size_cache = {}


# --------------------------------------------------------------- helpers ---
def _size(name):
    if name not in _size_cache:
        with Image.open(os.path.join(IMAGES, name + ".webp")) as im:
            _size_cache[name] = im.size
    return _size_cache[name]


def img(name, alt, sizes="100vw", cls="", eager=False, position=None, ratio=None):
    """A responsive <img>, with intrinsic dimensions so nothing shifts on load."""
    w, h = _size(name)
    srcset = []
    for v in VARIANTS:
        if os.path.exists(os.path.join(IMAGES, "%s-%d.webp" % (name, v))) and v < w:
            srcset.append("assets/images/%s-%d.webp %dw" % (name, v, v))
    srcset.append("assets/images/%s.webp %dw" % (name, w))

    attrs = [
        'src="assets/images/%s.webp"' % name,
        'srcset="%s"' % ", ".join(srcset),
        'sizes="%s"' % sizes,
        'width="%d"' % w,
        'height="%d"' % h,
        'alt="%s"' % alt,
    ]
    if cls:
        attrs.insert(0, 'class="%s"' % cls)
    if eager:
        attrs += ['loading="eager"', 'fetchpriority="high"', 'decoding="async"']
    else:
        attrs += ['loading="lazy"', 'decoding="async"']
    style = []
    if position:
        style.append("object-position:%s" % position)
    if ratio:
        style.append("aspect-ratio:%s" % ratio)
    if style:
        attrs.append('style="%s"' % ";".join(style))
    return "<img " + " ".join(attrs) + ">"


def icon(name, cls=""):
    c = ' class="%s"' % cls if cls else ""
    return ('<svg%s aria-hidden="true" focusable="false"><use href="#zeya-i-%s"></use></svg>'
            % (c, name))


def btn(label, href, variant="", cls="", arrow=True):
    classes = ["zeya-btn"]
    if variant:
        classes.append("zeya-btn--" + variant)
    if cls:
        classes.append(cls)
    tail = icon("arrow-right", "zeya-btn__arrow") if arrow else ""
    return '<a class="%s" href="%s">%s%s</a>' % (" ".join(classes), href, label, tail)


class H(object):
    """Namespace handed to page_content."""
    img = staticmethod(img)
    icon = staticmethod(icon)
    btn = staticmethod(btn)


# ----------------------------------------------------------------- shell ---
def sprite():
    with open(os.path.join(SITE, "assets", "icons", "zeya-icons.svg"), encoding="utf-8") as fh:
        svg = fh.read()
    # Strip the XML prolog/comment; keep the <svg> element itself for inlining.
    svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S)
    return svg.strip()


NAV_ITEMS = (
    ("home", "Home", "index.html"),
    ("about", "About", "about.html"),
    ("products", "Products", "products.html"),
    ("process", "Process", "process.html"),
    ("contact", "Contact", "contact.html"),
)


def logo(cls="", tag="a", href="index.html"):
    open_tag = ('<a class="zeya-logo %s" href="%s" aria-label="ZEYA Curtains and Blinds — home">'
                % (cls, href)) if tag == "a" else '<span class="zeya-logo %s">' % cls
    close_tag = "</a>" if tag == "a" else "</span>"
    return (open_tag +
            '<span class="zeya-logo__mark">ZEYA</span>'
            '<span class="zeya-logo__sub">Curtains &amp; Blinds</span>' +
            close_tag)


def header(page, solid):
    links = "".join(
        '<li><a class="zeya-nav__link" data-zeya-nav-item="%s" href="%s">%s</a></li>'
        % (key, href, label)
        for key, label, href in NAV_ITEMS
    )
    links = links.replace('<li><a class="zeya-nav__link" data-zeya-nav-item="products" href="products.html">Products</a></li>', '<li class="zeya-nav-products"><a class="zeya-nav__link" data-zeya-nav-item="products" href="products.html">Products</a><details class="zeya-product-menu"><summary aria-label="Product categories">?</summary><div>' + ''.join('<a href="%s.html">%s</a>' % (g,l) for g,l in catalog.LABELS.items()) + '</div></details></li>')
    return """
<header class="zeya-header{solid}" data-zeya-header>
  <div class="zeya-container zeya-container--wide zeya-header__inner">
    {logo}
    <nav class="zeya-nav" id="zeya-nav" data-zeya-nav aria-label="Primary">
      <ul class="zeya-nav__list">{links}</ul>
      <a class="zeya-btn zeya-btn--ivory zeya-nav__cta" href="contact.html">Book a Consultation</a>
    </nav>
    <button class="zeya-burger" type="button" data-zeya-burger
            aria-expanded="false" aria-controls="zeya-nav" aria-label="Open menu">
      <span class="zeya-burger__bar"></span>
      <span class="zeya-burger__bar"></span>
      <span class="zeya-burger__bar"></span>
    </button>
  </div>
</header>""".format(
        solid=" zeya-header--solid" if solid else "",
        logo=logo(),
        links=links,
    )


def footer():
    links = "".join(
        '<a class="zeya-footer__link" data-zeya-nav-item="%s" href="%s">%s</a>' % (key, href, label)
        for key, label, href in NAV_ITEMS
    )
    return """
<section class="zeya-footer-band">
  <div class="zeya-container zeya-footer-band__inner">
    <div class="zeya-reveal">
      {logo}
      <p class="zeya-footer-band__tag">Measured. Designed. Installed.</p>
    </div>
    <p class="zeya-footer-band__line zeya-reveal">Making Spaces<br>More Beautiful, Together.</p>
  </div>
</section>

<section class="zeya-cta">
  <div class="zeya-cta__media" data-zeya-parallax="0.1">
    {cta_img}
  </div>
  <div class="zeya-container zeya-cta__inner">
    {cta_logo}
    <p class="zeya-cta__tag zeya-reveal">Measured. Designed. Installed.</p>
    <div class="zeya-cta__actions zeya-reveal">
      {cta_btn}
    </div>
  </div>
</section>

<footer class="zeya-footer">
  <div class="zeya-container zeya-container--wide zeya-footer__inner">
    <nav class="zeya-footer__nav" aria-label="Footer">{links}</nav>

    <ul class="zeya-footer__contact">
      <li><a data-zeya-contact="address">{i_pin}<span>Dubai, UAE</span></a></li>
      <li><a data-zeya-contact="whatsapp">{i_wa}<span>WhatsApp</span></a></li>
      <li><a data-zeya-contact="phone">{i_ph}<span>Phone</span></a></li>
      <li><a data-zeya-contact="email">{i_ml}<span>Email</span></a></li>
    </ul>

    <ul class="zeya-footer__social">
      <li><a class="zeya-social-link" data-zeya-social="instagram" aria-label="ZEYA on Instagram">{i_ig}</a></li>
      <li><a class="zeya-social-link" data-zeya-social="facebook" aria-label="ZEYA on Facebook">{i_fb}</a></li>
      <li><a class="zeya-social-link" data-zeya-social="whatsapp" aria-label="ZEYA on WhatsApp">{i_wa}</a></li>
    </ul>
  </div>

  <div class="zeya-container zeya-container--wide zeya-footer__bar">
    <p>&copy; <span data-zeya-year>2026</span> ZEYA Curtains &amp; Blinds. All Rights Reserved.</p>
    <p>Dubai, UAE</p>
  </div>
</footer>""".format(
        logo=logo(),
        cta_img=img("cta-dubai-interior", "Luxury Dubai apartment interior at dusk with full-height "
                                          "curtains framing the city skyline",
                    sizes="100vw"),
        cta_logo=logo("zeya-logo--lg zeya-logo--center zeya-reveal", tag="span"),
        cta_btn=btn("Book a Free Consultation", "contact.html", "gold"),
        links=links,
        i_pin=icon("pin"), i_wa=icon("whatsapp"), i_ph=icon("phone"),
        i_ml=icon("mail"), i_ig=icon("instagram"), i_fb=icon("facebook"),
    )


SHELL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="theme-color" content="#211B16">
<meta name="robots" content="index, follow">

<meta property="og:type" content="website">
<meta property="og:site_name" content="ZEYA Curtains &amp; Blinds">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="assets/images/zeya-og-image.webp">
<meta name="twitter:card" content="summary_large_image">

<link rel="icon" href="assets/icons/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500&amp;family=Inter:wght@300;400;500;600&amp;display=swap">
{preload}
<link rel="stylesheet" href="css/style.css">
<link rel="stylesheet" href="css/animations.css">
<link rel="stylesheet" href="css/responsive.css">
<script>document.documentElement.classList.add('zeya-js');</script>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"HomeAndConstructionBusiness",
"name":"ZEYA Curtains & Blinds",
"description":"Custom-made curtains, blinds and motorized window solutions in Dubai, UAE.",
"areaServed":{{"@type":"City","name":"Dubai"}},
"address":{{"@type":"PostalAddress","addressLocality":"Dubai","addressCountry":"AE"}}}}
</script>
</head>
<body class="zeya-body zeya-page--{page}" data-zeya-page="{page}">
<a class="zeya-skip" href="#zeya-main">Skip to content</a>

{sprite}
{header}

<main id="zeya-main">
{body}
</main>

{footer}

<script src="js/main.js" defer></script>
<script src="js/animations.js" defer></script>
</body>
</html>
"""

PAGES = {
    "index.html": dict(
        page="home",
        solid=False,
        title="ZEYA Curtains & Blinds | Custom Curtains, Blinds & Motorized Window Solutions in Dubai",
        description="Custom-made curtains, blinds and motorized window solutions in Dubai. "
                    "Elegant, functional and made for your space — measured, designed and installed by ZEYA.",

    ),
    "about.html": dict(
        page="about", solid=True,
        title="About ZEYA | More Than Just Window Coverings | Dubai",
        description="ZEYA creates custom-made curtains, blinds and motorized window solutions in Dubai — "
                    "from fabric and colour selection through measurement to professional installation.",
    ),
    "products.html": dict(
        page="products", solid=True,
        title="Curtains, Blinds & Motorized Solutions | ZEYA Dubai",
        description="Sheer, blackout, linen, velvet and wave curtains, roller, zebra, Roman, Venetian and "
                    "motorized blinds, plus smart motorized window systems for homes and businesses in Dubai.",
    ),
    "process.html": dict(
        page="process", solid=True,
        title="Our Process | Consultation to Installation | ZEYA Dubai",
        description="A simple six-step process: free consultation, a visit to your space, your choice of "
                    "solution, accurate measurement, a clear quotation and professional installation.",
    ),
    "contact.html": dict(
        page="contact", solid=True,
        title="Contact ZEYA Curtains & Blinds | Dubai, UAE",
        description="Book a consultation with ZEYA Curtains & Blinds in Dubai. Tell us about your space and "
                    "we will bring fabric, colour and functionality options to you.",
    ),
}


def esc(value):
    return value.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")


def main():
    bodies = page_content.render(H)
    bodies.update(catalog.render(H))
    for key in bodies:
        if key not in ('home','about','products','process','contact'):
            title = catalog.LABELS.get(key, key.removeprefix('product-').replace('-', ' ').title())
            PAGES[key+'.html'] = dict(page=key, solid=True, title=title+' | ZEYA Dubai', description='Explore '+title+' from ZEYA Curtains & Blinds in Dubai.')
    sprite_markup = sprite()
    foot = footer()

    for filename, meta in PAGES.items():
        html = SHELL.format(
            title=esc(meta["title"]),
            description=esc(meta["description"]),
            preload=meta.get("preload", ""),
            page=meta["page"],
            sprite=sprite_markup,
            header=header(meta["page"], meta["solid"]),
            body=bodies[meta["page"]],
            footer=foot,
        )
        path = os.path.join(SITE, filename)
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(html)
        print("  %-14s %6.1f KB" % (filename, len(html) / 1024.0))

    print("\nBuilt -> zeya-website/")


if __name__ == "__main__":
    main()
