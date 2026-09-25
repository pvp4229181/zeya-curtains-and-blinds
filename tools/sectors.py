"""The Residential & Commercial collection: the same range, shown by the spaces it serves.

Each space is a card with a photograph, a short description and the solutions
that usually suit it. Each sector closes on a panel that carries its call to
action, sized so the panel completes the grid's last row.
"""
from html import escape

SLUG = 'residential-commercial'
LABEL = 'Residential & Commercial'
INTRO = ('Curtain and blind solutions for homes and for workplaces, chosen for how each '
         'space is used and made to measure for every window.')

# (space, image, description, suggested solutions)
RESIDENTIAL = [
    ('Villas & Luxury Homes', 'ai-residential-project',
     'Full-height glazing and statement rooms, dressed as one considered scheme from room to room.',
     ('Motorised curtains', 'Layered sheers', 'Blackout')),
    ('Apartments', 'ai-roller',
     'Clean, space-saving treatments that tame the Dubai sun and keep the city view.',
     ('Roller blinds', 'Sheer curtains', 'Zebra blinds')),
    ('Living Rooms', 'ai-hero',
     'Soft daylight through the day and privacy by evening, layered for how the room is used.',
     ('Sheer curtains', 'Decorative curtains', 'Motorised')),
    ('Bedrooms', 'ai-blackout-roller',
     'Deep blackout for restful sleep, with a softer layer to welcome the morning light.',
     ('Blackout curtains', 'Roman blinds', 'Sheer curtains')),
    ('Dining Areas', 'ai-faux-wood',
     'Glare kept off the table without losing the warmth of natural light.',
     ('Roman blinds', 'Sheer curtains', 'Zebra blinds')),
    ('Home Offices', 'ai-venetian',
     'Screen-friendly light control that cuts glare but keeps the room bright enough to work.',
     ('Roller blinds', 'Zebra blinds', 'Motorised blinds')),
    ('Majlis & Family Spaces', 'ai-vertical',
     'Generous, elegant drapery for gathering rooms, with privacy the moment guests arrive.',
     ('Decorative curtains', 'Blackout curtains', 'Motorised curtains')),
]

COMMERCIAL = [
    ('Offices', 'ai-commercial-project',
     'Glare-free desks and meeting rooms, with one consistent look across every floor.',
     ('Roller blinds', 'Sunscreen blinds', 'Venetian blinds')),
    ('Hotels', 'ai-wave',
     'Blackout for guest rooms and soft sheers for suites and lobbies, made for daily use.',
     ('Blackout curtains', 'Sheer curtains', 'Motorised systems')),
    ('Restaurants & Cafés', 'ai-linen',
     'Set the mood from lunch to late evening while keeping window tables comfortable.',
     ('Roman blinds', 'Sheer curtains', 'Roller blinds')),
    ('Retail Stores & Showrooms', 'ai-consultation',
     'Keep glare off displays and direct sun off stock, with a storefront that still invites people in.',
     ('Roller blinds', 'Sunscreen blinds', 'Motorised blinds')),
    ('Clinics', 'ai-sunscreen',
     'Privacy for consultation rooms and calm, practical finishes for reception and waiting areas.',
     ('Vertical blinds', 'Roller blinds', 'Venetian blinds')),
]

RESIDENTIAL_SOLUTIONS = [
    ('Sheer Curtains', 'product-sheer-curtains.html'),
    ('Blackout Curtains', 'product-blackout-curtains.html'),
    ('Decorative Curtains', 'curtains.html'),
    ('Roller Blinds', 'product-roller-blinds.html'),
    ('Roman Blinds', 'product-roman-blinds.html'),
    ('Zebra Blinds', 'product-zebra-blinds.html'),
    ('Motorised Curtains &amp; Blinds', 'motorized.html'),
]


def _space(h, name, image, text, uses):
    tags = ''.join(f'<li>{u}</li>' for u in uses)
    return (f'<article class="zeya-space">'
            f'<div class="zeya-space__image">'
            f'{h.img(image, "Interior inspiration: " + escape(name), sizes="(max-width:700px) 100vw, (max-width:900px) 50vw, 33vw")}'
            f'</div><div class="zeya-space__copy"><h3>{escape(name)}</h3><p>{text}</p>'
            f'<ul class="zeya-space__uses" aria-label="Suited to">{tags}</ul></div></article>')


def _sector(h, key, number, eyebrow, title, intro, spaces, panel, dark=False):
    tone = ' zeya-section--chocolate' if dark else ''
    return (f'<section class="zeya-section zeya-sector{tone}" id="{key}" aria-labelledby="zeya-{key}-title">'
            f'<div class="zeya-container">'
            f'<div class="zeya-section-heading"><p class="zeya-eyebrow">{number} &middot; {eyebrow}</p>'
            f'<div><h2 id="zeya-{key}-title">{title}</h2><p>{intro}</p></div></div>'
            f'<div class="zeya-catalog-grid zeya-sector__grid zeya-sector__grid--{key}">'
            + ''.join(_space(h, *s) for s in spaces) + panel +
            f'</div></div></section>')


def page(h, crumbs):
    residential_panel = (
        '<div class="zeya-sector__panel zeya-sector__panel--wide">'
        '<p class="zeya-eyebrow">Residential solutions</p>'
        '<h3>Every window in the home, made to measure.</h3>'
        '<ul class="zeya-sector__solutions">'
        + ''.join(f'<li><a href="{href}">{name}<span aria-hidden="true">&#8594;</span></a></li>'
                  for name, href in RESIDENTIAL_SOLUTIONS) +
        '</ul>'
        + h.btn('Book a Home Consultation', 'contact.html?product=home-consultation', 'gold') +
        '</div>')
    commercial_panel = (
        '<div class="zeya-sector__panel">'
        '<p class="zeya-eyebrow">Commercial projects</p>'
        '<h3>One partner from survey to handover.</h3>'
        '<p>From a single office floor to a full hotel fit-out, we measure on site, '
        'specify each space and install around your programme.</p>'
        + h.btn('Discuss Your Project', 'contact.html?product=commercial-project', 'gold') +
        '</div>')

    return (
        h.hero('signature-motorized', 'Made-to-measure blinds overlooking the Dubai skyline',
               escape(LABEL), eyebrow='The ZEYA collection', sub=INTRO,
               crumbs=crumbs(LABEL))
        + '<nav class="zeya-collection-nav zeya-container" aria-label="Sectors">'
          '<a href="#residential">Residential<span aria-hidden="true">&#8595;</span></a>'
          '<a href="#commercial">Commercial<span aria-hidden="true">&#8595;</span></a></nav>'
        + _sector(h, 'residential', '01', 'For the home', 'Residential',
                  'Villas, apartments and every room in between. We look at the light, the view '
                  'and how each room is lived in, then bring the fabrics and finishes to suit.',
                  RESIDENTIAL, residential_panel)
        + _sector(h, 'commercial', '02', 'For business', 'Commercial',
                  'Workplaces and hospitality spaces that need to look right and work hard every day, '
                  'fitted with minimal disruption to your operation.',
                  COMMERCIAL, commercial_panel, dark=True))


def teaser(h):
    """The products-page section that leads to the sector page."""
    cards = ''.join(
        f'<a class="zeya-product" href="{SLUG}.html#{key}">'
        f'<div class="zeya-product__image">'
        f'{h.img(image, "Interior inspiration: " + title, sizes="(max-width:700px) 100vw, 50vw")}'
        f'<span class="zeya-product__veil" aria-hidden="true"></span></div>'
        f'<div class="zeya-product__copy"><h3>{title}</h3><p>{text}</p>'
        f'<span class="zeya-product__action">Explore the spaces'
        f'<span aria-hidden="true">&#8594;</span></span></div></a>'
        for key, image, title, text in [
            ('residential', 'ai-residential-project', 'Residential',
             'Villas, apartments, bedrooms, majlis and every room in between.'),
            ('commercial', 'ai-commercial-project', 'Commercial',
             'Offices, hotels, restaurants, showrooms and clinics.'),
        ])
    return (f'<section class="zeya-section zeya-container zeya-catalog-section" id="{SLUG}">'
            f'<div class="zeya-section-heading">'
            f'<p class="zeya-eyebrow">Homes &amp; workplaces</p>'
            f'<div><div class="zeya-section-heading__row"><h2>{escape(LABEL)}</h2>'
            f'{h.btn("Explore collection", SLUG + ".html", "outline")}</div>'
            f'<p>{INTRO}</p></div></div>'
            f'<div class="zeya-catalog-grid zeya-catalog-grid--two">{cards}</div></section>')
