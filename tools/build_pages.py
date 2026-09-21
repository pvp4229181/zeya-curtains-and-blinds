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
from asset_map import IMAGES as IMAGE_ALIASES

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
    name = "ai-" + IMAGE_ALIASES[name] if name in IMAGE_ALIASES else name
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


def hero(image, alt, title, eyebrow="", sub="", actions="", crumbs="",
         variant="", position=None):
    """The full-bleed image hero that opens every page.

    One component, three sizes: the home page runs tall, collection and
    editorial pages run standard, product pages run compact. The image sits
    behind a two-stop scrim so the display type keeps its contrast whatever
    the photograph does, and the title is always the page's single <h1>.
    """
    classes = ["zeya-hero"]
    if variant:
        classes.append("zeya-hero--" + variant)
    return (
        '<section class="%s">' % " ".join(classes) +
        '<div class="zeya-hero__media">%s</div>'
        % img(image, alt, sizes="100vw", eager=True, position=position) +
        '<div class="zeya-hero__scrim" aria-hidden="true"></div>' +
        '<div class="zeya-hero__inner zeya-container">' +
        ('<p class="zeya-hero__eyebrow">%s</p>' % eyebrow if eyebrow else "") +
        '<h1 class="zeya-hero__title">%s</h1>' % title +
        ('<p class="zeya-hero__sub">%s</p>' % sub if sub else "") +
        ('<div class="zeya-hero__actions">%s</div>' % actions if actions else "") +
        "</div>" +
        ('<div class="zeya-hero__crumbs"><div class="zeya-container">%s</div></div>'
         % crumbs if crumbs else "") +
        "</section>"
    )


class H(object):
    """Namespace handed to page_content."""
    img = staticmethod(img)
    icon = staticmethod(icon)
    btn = staticmethod(btn)
    hero = staticmethod(hero)


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


def logo(cls="", tag="a", href="index.html", eager=False, variant=""):
    """The ZEYA wordmark image, wrapped in the same lockup element as before.
    `variant` picks an alternate file — the footer uses the transparent gold
    artwork so it can sit on the dark band without being knocked out to white."""
    open_tag = ('<a class="zeya-logo %s" href="%s" aria-label="ZEYA Curtains and Blinds — home">'
                % (cls, href)) if tag == "a" else '<span class="zeya-logo %s">' % cls
    close_tag = "</a>" if tag == "a" else "</span>"
    loading = ('loading="eager" fetchpriority="high"' if eager else 'loading="lazy"')
    return (open_tag +
            '<img class="zeya-logo__img" src="assets/images/zeya-logo%(v)s.webp" '
            'srcset="assets/images/zeya-logo%(v)s-360.webp 360w, '
            'assets/images/zeya-logo%(v)s.webp 720w" '
            'sizes="(max-width: 640px) 180px, 260px" width="720" height="238" '
            'alt="ZEYA Curtains &amp; Blinds" %(l)s decoding="async">'
            % {"v": variant, "l": loading} +
            close_tag)


def header(page, solid):
    """The navigation bar. It rides transparent over the hero and swaps to the
    solid shell once the hero has scrolled away — the transition is driven from
    main.js, so the markup carries only the hooks."""
    items = []
    for key, label, href in NAV_ITEMS:
        if key == "products":
            sub = "".join('<a href="%s.html">%s</a>' % (g, l)
                          for g, l in catalog.LABELS.items())
            items.append(
                '<li class="zeya-nav-products">'
                '<a class="zeya-nav__link" data-zeya-nav-item="products" '
                'href="products.html">Products</a>'
                '<details class="zeya-product-menu">'
                '<summary aria-label="Product categories">'
                '<svg aria-hidden="true" focusable="false"><use href="#zeya-i-arrow-right"></use></svg>'
                '</summary><div>%s</div></details></li>' % sub)
        else:
            items.append('<li><a class="zeya-nav__link" data-zeya-nav-item="%s" '
                         'href="%s">%s</a></li>' % (key, href, label))

    return u"""
<header class="zeya-header{solid}" data-zeya-header>
  <div class="zeya-container zeya-container--wide zeya-header__inner">
    {logo}
    <nav class="zeya-nav" id="zeya-nav" data-zeya-nav aria-label="Primary">
      <ul class="zeya-nav__list">{links}</ul>
      <a class="zeya-btn zeya-btn--line zeya-nav__cta" href="contact.html">Let’s talk</a>
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
        logo=logo(eager=True, variant="-footer"),
        links="".join(items),
    )


def footer():
    links = "".join('<a data-zeya-nav-item="%s" href="%s">%s</a>' % (k, u, l)
                    for k, l, u in NAV_ITEMS)
    collections = "".join('<a href="%s.html">%s</a>' % (g, l)
                          for g, l in catalog.LABELS.items())
    return (
        u'<section class="zeya-footer-cta">'
        u'<div class="zeya-footer-cta__media">%s</div>'
        % img('cta-consultation', 'Sunset over Dubai through sheer curtains in a '
              'contemporary living room', sizes='100vw') +
        u'<div class="zeya-footer-cta__scrim" aria-hidden="true"></div>'
        u'<div class="zeya-container zeya-footer-cta__inner">'
        u'<p class="zeya-eyebrow">Let’s transform your windows</p>'
        u'<h2>Beautiful living<br>starts with a conversation.</h2>'
        u'<p>Tell us about your space and we’ll bring the fabrics, finishes and '
        u'light‑control options to you.</p>'
        + btn("Book a consultation", "contact.html", "ivory") +
        u'</div></section>'
        u'<footer class="zeya-footer"><div class="zeya-container zeya-footer__grid">'
        u'<div class="zeya-footer__brand">' + logo(variant="-footer") +
        u'<p class="zeya-footer__line">Measured. Designed. Installed.</p>'
        u'<p class="zeya-footer__note">Bespoke curtains, blinds and motorized window '
        u'solutions in Dubai, UAE.</p></div>'
        u'<nav class="zeya-footer__col" aria-label="Footer">'
        u'<p class="zeya-eyebrow">Explore</p>' + links + u'</nav>'
        u'<div class="zeya-footer__col"><p class="zeya-eyebrow">Collections</p>'
        + collections + u'</div>'
        u'<div class="zeya-footer__col zeya-footer__contact">'
        u'<p class="zeya-eyebrow">Get in touch</p>'
        + "".join(u'<a class="zeya-method" data-zeya-contact="%s"><span>%s</span>'
                  u'<span data-zeya-contact-value></span></a>' % (k, l)
                  for k, l in (("phone", "Phone"), ("whatsapp", "WhatsApp"),
                               ("email", "Email"), ("address", "Studio")))
        + u'</div></div>'
        u'<div class="zeya-container zeya-footer__bar">'
        u'<p>© <span data-zeya-year>2026</span> ZEYA Curtains &amp; Blinds.</p>'
        u'<p>Interior imagery is AI‑generated for inspiration.</p>'
        u'<p class="zeya-footer__credit">Made by '
        u'<a href="https://www.nexmogen.com" target="_blank" rel="noopener">Nexmogen</a></p>'
        u'</div></footer>')


SHELL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="theme-color" content="#191713">
<meta name="robots" content="index, follow">

<meta property="og:type" content="website">
<meta property="og:site_name" content="ZEYA Curtains &amp; Blinds">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="assets/images/ai-hero.webp">
<meta name="twitter:card" content="summary_large_image">

<link rel="icon" href="assets/icons/favicon.ico" sizes="32x32">
<link rel="icon" href="assets/icons/favicon-32.png" type="image/png" sizes="32x32">
<link rel="icon" href="assets/icons/favicon-192.png" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="assets/icons/apple-touch-icon.png">
<link rel="stylesheet" href="assets/fonts/fonts.css">
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
        page="about", solid=False,
        title="About ZEYA | More Than Just Window Coverings | Dubai",
        description="ZEYA creates custom-made curtains, blinds and motorized window solutions in Dubai — "
                    "from fabric and colour selection through measurement to professional installation.",
    ),
    "products.html": dict(
        page="products", solid=False,
        title="Curtains, Blinds & Motorized Solutions | ZEYA Dubai",
        description="Sheer, blackout, linen, velvet and wave curtains, roller, zebra, Roman, Venetian and "
                    "motorized blinds, smart motorized window systems and curtain accessories — poles, "
                    "tracks, tiebacks and linings — for homes and businesses in Dubai.",
    ),
    "process.html": dict(
        page="process", solid=False,
        title="Our Process | Consultation to Installation | ZEYA Dubai",
        description="A simple six-step process: free consultation, a visit to your space, your choice of "
                    "solution, accurate measurement, a clear quotation and professional installation.",
    ),
    "contact.html": dict(
        page="contact", solid=False,
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
            PAGES[key+'.html'] = dict(page=key, solid=False, title=title+' | ZEYA Dubai', description='Explore '+title+' from ZEYA Curtains & Blinds in Dubai.')
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
