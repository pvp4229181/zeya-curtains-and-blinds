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
import json
from pathlib import Path

from PIL import Image

import page_content
import catalog
from asset_map import IMAGES as IMAGE_ALIASES

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SITE = os.path.join(ROOT, "zeya-website")
IMAGES = os.path.join(SITE, "assets", "images")
VARIANTS = (640, 1024, 1600)
PRODUCT_PHOTOS = json.loads(Path(ROOT, 'tools', 'blindscom_sources.json').read_text(encoding='utf-8'))
SIGNATURE_PHOTOS = {
    'hero-luxury-curtains': 'signature-hero',
    'intro-living-room': 'signature-hero',
    'about-zeya-curtains': 'signature-curtains',
    'curtains-category': 'signature-curtains',
    'blinds-category': 'signature-blinds',
    'motorized-solutions': 'signature-motorized',
    'fabric-consultation': 'signature-fabric',
    'contact-interior': 'signature-curtains',
    'cta-consultation': 'signature-hero',
}

_size_cache = {}


# --------------------------------------------------------------- helpers ---
def _size(name):
    if name not in _size_cache:
        with Image.open(os.path.join(IMAGES, name + ".webp")) as im:
            _size_cache[name] = im.size
    return _size_cache[name]


def img(name, alt, sizes="100vw", cls="", eager=False, position=None, ratio=None):
    """A responsive <img>, with intrinsic dimensions so nothing shifts on load."""
    # Prefer the curated AI catalogue art whenever an alias exists.  The
    # extracted supplier photography remains available as a fallback only.
    if name in IMAGE_ALIASES:
        name = "ai-" + IMAGE_ALIASES[name]
    elif name in PRODUCT_PHOTOS:
        name = PRODUCT_PHOTOS[name]['asset']
    else:
        name = SIGNATURE_PHOTOS.get(name, name)
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
    ("products", "Collections", "products.html"),
    ("about", "About Us", "about.html"),
    ("process", "Our Process", "process.html"),
    ("faq", "FAQs", "faq.html"),
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
            'sizes="(max-width: 640px) 180px, 260px" width="720" height="240" '
            'alt="ZEYA Curtains &amp; Blinds" %(l)s decoding="async">'
            % {"v": variant, "l": loading} +
            close_tag)


def product_menu(page=None):
    """The Collections dropdown panel.

    The four product collections sit in a 2x2 grid; the sector page, which
    shows the same range by space rather than by product, gets its own row.
    Thumbnails are decorative (the name beside each one is the link text),
    so they carry an empty alt and stay out of the accessible name.
    """
    def item(g, wide=False):
        image, note = catalog.MENU_NOTES[g]
        current = ' aria-current="page"' if g == page else ""
        return ('<a class="zeya-product-menu__item%s" href="%s.html"%s>'
                '<span class="zeya-product-menu__thumb">%s</span>'
                '<span class="zeya-product-menu__text">'
                '<span class="zeya-product-menu__name">%s</span>'
                '<span class="zeya-product-menu__note">%s</span></span></a>'
                % (" zeya-product-menu__item--wide" if wide else "", g, current,
                   img(image, "", sizes="96px"), esc(catalog.MENU[g]), esc(note)))

    by_space = [g for g in catalog.MENU if g not in catalog.LABELS]
    return (
        '<div class="zeya-product-menu__panel">'
        '<p class="zeya-product-menu__label">By product</p>'
        '<div class="zeya-product-menu__grid">'
        + "".join(item(g) for g in catalog.LABELS) +
        '</div>'
        '<p class="zeya-product-menu__label">By space</p>'
        + "".join(item(g, wide=True) for g in by_space) +
        '<div class="zeya-product-menu__foot">'
        '<a href="products.html">View all collections <span aria-hidden="true">&rarr;</span></a>'
        '<span>Made to measure &middot; Installed across Dubai</span></div>'
        '</div>')


def header(page, solid):
    """The navigation bar. It rides transparent over the hero and swaps to the
    solid shell once the hero has scrolled away — the transition is driven from
    main.js, so the markup carries only the hooks."""
    items = []
    for key, label, href in NAV_ITEMS:
        if key == "products":
            items.append(
                '<li class="zeya-nav-products">'
                '<a class="zeya-nav__link" data-zeya-nav-item="products" '
                'href="products.html">Collections</a>'
                '<details class="zeya-product-menu">'
                '<summary>Browse collections'
                '<svg aria-hidden="true" focusable="false"><use href="#zeya-i-arrow-right"></use></svg>'
                '</summary>%s</details></li>' % product_menu(page))
        else:
            items.append('<li><a class="zeya-nav__link" data-zeya-nav-item="%s" '
                         'href="%s">%s</a></li>' % (key, href, label))

    return u"""
<header class="zeya-header{solid}" data-zeya-header>
  <div class="zeya-container zeya-container--wide zeya-header__inner">
    {logo}
    <nav class="zeya-nav" id="zeya-nav" data-zeya-nav aria-label="Primary">
      <ul class="zeya-nav__list">{links}</ul>
      <a class="zeya-btn zeya-btn--line zeya-nav__cta" href="contact.html">Book a Consultation <span aria-hidden="true">&#8594;</span></a>
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
    """The closing band: an invitation, four columns and a legal line.

    The invitation is the page's last call to action (the home page hides it,
    since it closes on one of its own). The columns carry navigation, the
    collections and the contact methods; the methods and social icons ship
    without an href and main.js links them once real details are configured,
    so the footer never points at an invented number or an empty profile.
    """
    links = "".join('<a class="zeya-footer__link" data-zeya-nav-item="%s" href="%s">%s</a>'
                    % (k, u, l) for k, l, u in NAV_ITEMS)
    collections = "".join('<a class="zeya-footer__link" href="%s.html">%s</a>' % (g, esc(l))
                          for g, l in catalog.MENU.items())
    methods = "".join('<a class="zeya-method" data-zeya-contact="%s"><span>%s</span>'
                      '<span data-zeya-contact-value></span></a>' % (k, l)
                      for k, l in (("phone", "Phone"), ("whatsapp", "WhatsApp"),
                                   ("email", "Email"), ("address", "Studio")))
    socials = "".join(
        '<a class="zeya-social__link" %s aria-label="%s">%s</a>' % (attr, label, icon(name))
        for attr, label, name in (
            ('data-zeya-social="instagram"', "ZEYA on Instagram", "instagram"),
            ('data-zeya-social="facebook"', "ZEYA on Facebook", "facebook")))

    def column(label, body, tag="div", extra=""):
        return ('<%s class="zeya-footer__col%s"%s>'
                '<p class="zeya-eyebrow">%s</p>%s</%s>'
                % (tag, extra, ' aria-label="Footer"' if tag == "nav" else "",
                   label, body, tag))

    return (
        '<footer class="zeya-footer">'
        '<div class="zeya-container zeya-footer__invitation">'
        '<div><p class="zeya-eyebrow">Your next chapter starts here</p>'
        '<h2>Let&rsquo;s frame something<br><em>beautiful.</em></h2></div>'
        '<div class="zeya-footer__invitation-action">'
        '<p>Your space. Your style. Our attention to every detail.</p>'
        + btn('Book a consultation', 'contact.html', 'ivory') +
        '</div></div>'
        '<div class="zeya-container zeya-footer__grid">'
        '<div class="zeya-footer__brand">' + logo(variant="-footer") +
        '<p class="zeya-footer__line">Measured. Designed. Installed.</p>'
        '<p class="zeya-footer__note">Bespoke curtains, blinds and motorized window '
        'solutions for homes and workplaces across Dubai, UAE.</p>'
        '<div class="zeya-social">' + socials + '</div></div>'
        + column('Explore', links, tag="nav")
        + column('Collections', collections)
        + column('Get in touch',
                 '<p class="zeya-footer__location">Dubai, UAE</p>'
                 '<p class="zeya-footer__note">We bring the fabrics, finishes and '
                 'measurements to you, across homes and workplaces in the Emirates.</p>'
                 + methods +
                 '<a class="zeya-footer__enquiry" href="contact.html">Start your project '
                 '<span aria-hidden="true">&rarr;</span></a>',
                 extra=' zeya-footer__contact')
        + '</div>'
        '<div class="zeya-container zeya-footer__bar">'
        '<p>&copy; <span data-zeya-year>2026</span> ZEYA Curtains &amp; Blinds. '
        'All rights reserved.</p>'
        '<p class="zeya-footer__legal"><a href="faq.html">FAQs</a><span aria-hidden="true"> &middot; </span><a href="terms.html">Terms &amp; Conditions</a></p>'
        '</div></footer>')


def floating_cta():
    """The enquiry button that stays on screen on every page.

    Until a WhatsApp number is configured it is a consultation link to the
    contact page; main.js swaps it for the WhatsApp bubble once a number
    exists, so the float can never open an empty chat.
    """
    return (
        '<a class="zeya-consult-float" data-zeya-consult-float href="contact.html">'
        + icon("calendar", "zeya-consult-float__icon") +
        '<span>Book a consultation</span></a>\n'
        '<a class="zeya-wa-float" data-zeya-wa="general" '
        'aria-label="Chat on WhatsApp" hidden>'
        + icon("whatsapp", "zeya-wa-float__icon") + '</a>')


SHELL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="theme-color" content="#171411">
<meta name="robots" content="{robots}">

<meta property="og:type" content="website">
<meta property="og:site_name" content="ZEYA Curtains &amp; Blinds">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="assets/images/signature-hero.webp">
<meta name="twitter:card" content="summary_large_image">

<link rel="icon" href="assets/icons/favicon.ico?v=4" sizes="32x32">
<link rel="icon" href="assets/icons/favicon-32.png?v=4" type="image/png" sizes="32x32">
<link rel="icon" href="assets/icons/favicon-192.png?v=4" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="assets/icons/apple-touch-icon.png?v=4">
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

{floating}

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
    "residential-commercial.html": dict(
        page="residential-commercial", solid=False,
        title="Residential & Commercial Curtains and Blinds | ZEYA Dubai",
        description="Curtains and blinds for villas, apartments, bedrooms and majlis, and for offices, "
                    "hotels, restaurants, showrooms and clinics across Dubai — measured, supplied "
                    "and installed by ZEYA.",
    ),
    "terms.html": dict(
        page="terms", solid=False,
        title="Terms & Conditions | ZEYA Curtains & Blinds Dubai",
        description="The terms that apply to quotations, orders, supply and installation by ZEYA "
                    "Curtains & Blinds in Dubai — pricing and payment, custom-made products, "
                    "installation conditions, motorized products and warranty.",
    ),
    "faq.html": dict(
        page="faq", solid=False,
        title="Frequently Asked Questions | Curtains & Blinds | ZEYA Dubai",
        description="Answers to frequently asked questions about made-to-measure curtains, blinds, blackout fabrics, measuring, installation, care and motorised systems in Dubai.",
    ),
    # The link ZEYA shares with clients to invite a Google review. It is kept
    # out of search results: it is an invitation, not a page to be found.
    "review.html": dict(
        page="review", solid=False, robots="noindex, follow",
        title="Share Your Experience | ZEYA Curtains & Blinds Dubai",
        description="We'd love to hear about your experience with ZEYA Curtains & Blinds. "
                    "Leave us a Google review.",
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
        if key not in ('home','about','products','process','contact','terms','review','faq'):
            title = catalog.LABELS.get(key, key.removeprefix('product-').replace('-', ' ').title())
            PAGES.setdefault(key+'.html', dict(page=key, solid=False, title=title+' | ZEYA Dubai', description='Explore '+title+' from ZEYA Curtains & Blinds in Dubai.'))
    sprite_markup = sprite()
    foot = footer()

    for filename, meta in PAGES.items():
        html = SHELL.format(
            title=esc(meta["title"]),
            description=esc(meta["description"]),
            preload=meta.get("preload", ""),
            robots=meta.get("robots", "index, follow"),
            page=meta["page"],
            sprite=sprite_markup,
            header=header(meta["page"], meta["solid"]),
            body=bodies[meta["page"]],
            footer=foot,
            floating=floating_cta(),
        )
        path = os.path.join(SITE, filename)
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(html)
        print("  %-14s %6.1f KB" % (filename, len(html) / 1024.0))

    print("\nBuilt -> zeya-website/")


if __name__ == "__main__":
    main()
