"""Reference-inspired homepage, shared by the static site and WordPress."""


def _feature(h, icon, title, text):
    return f'<div class="zeya-signature-feature">{h.icon(icon)}<span>{title}<small>{text}</small></span></div>'


def services_section(h, product=''):
    """What the service covers, from first visit to installation.

    Shared by the home page and every product page. On a product page the
    WhatsApp button carries the product name, so the chat opens with context.
    """
    items = ''.join(
        f'<li class="zeya-services__item">{h.icon(icon)}<h3>{title}</h3><p>{text}</p></li>'
        for icon, title, text in [
            ('home', 'Home visits', 'We come to your home or workplace, anywhere in Dubai.'),
            ('swatch', 'Fabric samples', 'Compare textures and colours in your own light.'),
            ('ruler', 'Precise measuring', 'Every window measured for a made-to-measure fit.'),
            ('doc', 'Clear quotation', 'A full specification and price before you commit.'),
            ('tools', 'Installation', 'Fitted and finished by us, from start to finish.'),
            ('gear', 'Motorised solutions', 'Motorised curtains and blinds, set up on site.'),
        ])
    wa_attrs = (f'data-zeya-wa="product" data-zeya-wa-product="{product}"'
                if product else 'data-zeya-wa="general"')
    wa_button = (f'<a class="zeya-btn zeya-btn--whatsapp" {wa_attrs} hidden>'
                 f'{h.icon("whatsapp")}Chat on WhatsApp</a>')
    return f'''<section class="zeya-services" id="services" aria-labelledby="zeya-services-title">
  <div class="zeya-container zeya-services__inner">
    <div class="zeya-services__intro"><p class="zeya-eyebrow">Our service &middot; Across Dubai</p><h2 id="zeya-services-title">From your window to the final installation.</h2><p>We visit your space, bring fabric samples, take precise measurements, help you choose the right finish, provide a quotation, and handle the installation from start to finish.</p><div class="zeya-services__actions">{h.btn('Book a consultation', 'contact.html', 'gold')}{wa_button}</div></div>
    <ol class="zeya-services__list">{items}</ol>
  </div>
</section>'''


def why_band(h):
    """The short "Why ZEYA" band, paired with the "Spaces that feel like you" image."""
    why = ''.join(_feature(h, *row) for row in [
        ('ruler', 'Made-to-measure', 'Cut for every window'), ('swatch', 'Curated fabrics', 'Selected with care'),
        ('tools', 'Professional installation', 'A seamless finish'), ('gear', 'Motorised solutions', 'Effortless control')])
    image = h.img('signature-hero', 'AI interior inspiration: a warmly lit living room',
                  sizes='(max-width:700px) 100vw, 45vw')
    return (f'<section class="zeya-service-band" aria-labelledby="zeya-why-title">'
            f'<div class="zeya-service-band__features"><h2 class="zeya-service-band__title" id="zeya-why-title">Why ZEYA</h2>{why}</div>'
            f'<a class="zeya-service-band__image" href="contact.html">{image}'
            f'<span>Spaces<br>that feel<strong>Like You</strong></span></a></section>')


# Need -> the combination we recommend, the page that shows it, and the
# image that illustrates it. The flag marks what most Dubai homes ask for.
NEEDS = [
    ('sun', 'Block Sunlight', 'Too much brightness entering the room',
     'Blackout Curtains + Light Control Blinds', 'Blocks harsh sunlight, improves comfort, protects furniture',
     'product-blackout-curtains', False,
     'ai-blackout', 'Dark blackout curtains drawn beside a sunlit window'),
    ('drop', 'Reduce Heat', 'Room becomes hot due to the Dubai sun',
     'Blackout Curtains | Sheer Curtains | Screen Blinds | Two-&#8288;Layer Curtains', 'Reduces heat, softens glare, protects interiors',
     'product-sunscreen-blinds', True,
     'ai-sunscreen', 'Sunscreen roller blind softening the view of the Dubai skyline'),
    ('eye', 'Increase Privacy', 'Need privacy without making the room dark',
     'Privacy Curtains + Adjustable Blinds', 'Day &amp; night privacy, flexible light control',
     'product-zebra-blinds', False,
     'ai-zebra', 'Zebra blinds with alternating sheer and solid bands'),
    ('coin', 'Budget Friendly', 'Need an affordable window covering',
     'Practical Curtains &amp; Blinds', 'Affordable, durable, easy maintenance',
     'product-roller-blinds', False,
     'ai-roller', 'Pale roller blind over a window with a city view'),
    ('screen', 'Reduce TV Glare', 'Sunlight reflects on screens',
     'Glare Control Solutions', 'Reduces reflection, improves viewing experience',
     'product-venetian-blinds', False,
     'ai-venetian', 'Venetian blinds tilted to filter afternoon light'),
    ('remote', 'Smart Home Automation', 'Want modern convenience',
     'Motorized Curtains &amp; Blinds', 'Remote control, voice automation, luxury feel',
     'motorized', False,
     'ai-smart', 'Motorised roller shades in a living room'),
    ('moon', 'Better Sleep', 'Light affects sleep quality',
     'Blinds with Side Channels', 'Darker sleeping environment, less light leaking around the edges',
     'blinds', False,
     'ai-blackout-roller', 'Blackout roller blind lowered in a bedroom'),
    ('sparkle', 'Enhance Home D&eacute;cor', 'Want a premium interior look',
     'Designer Window Styling', 'Adds elegance, improves room aesthetics',
     'product-wave-curtains', False,
     'ai-wave', 'Floor-length sheer wave curtains in a bright living room'),
    ('window', 'Large Window Solutions', 'Large glass areas need coverage',
     'Custom Made Solutions', 'Smooth operation, modern finish, better coverage',
     'product-curtain-tracks', False,
     'ai-vertical', 'Vertical blinds covering a wide glass wall'),
]


def needs_section(h):
    """The "find your solution" picker: choose a problem, see the combination
    we recommend with a photograph of it.

    main.js turns the list into tabs and shows one panel at a time. Without
    it the tabs stay hidden and every panel is shown, each one naming its own
    problem, so the section still reads top to bottom.
    """
    flag = (f'<span class="zeya-needs__flag">{h.icon("star-fill")}'
            f'<span>Most requested</span></span>')
    tabs, panels = [], []
    for i, (icon, need, concern, solution, benefit, slug, top, image, alt) in enumerate(NEEDS, 1):
        benefits = ''.join(f'<li>{b[:1].upper()}{b[1:]}</li>' for b in benefit.split(', '))
        tabs.append(
            f'<button class="zeya-needs__tab" type="button" id="zeya-need-tab-{i}" data-zeya-needs-tab="zeya-need-{i}">'
            f'<span class="zeya-needs__num" aria-hidden="true">{i:02d}</span>{h.icon(icon)}'
            f'<span class="zeya-needs__tab-text"><span class="zeya-needs__tab-name">{need}</span>'
            f'<span class="zeya-needs__tab-concern">{concern}</span></span>'
            f'{h.icon("arrow-right", "zeya-needs__tab-arrow")}</button>')
        panels.append(
            f'<article class="zeya-needs__panel" id="zeya-need-{i}" aria-labelledby="zeya-need-title-{i}">'
            f'<div class="zeya-needs__media">{h.img(image, alt, "(max-width:900px) 100vw, 58vw")}</div>'
            f'<div class="zeya-needs__tag">{h.icon(icon)}<span>{need}</span></div>'
            f'{flag if top else ""}'
            f'<div class="zeya-needs__content">'
            f'<p class="zeya-needs__concern">&ldquo;{concern}.&rdquo;</p>'
            f'<p class="zeya-eyebrow">We recommend</p>'
            f'<h3 id="zeya-need-title-{i}">{solution}</h3>'
            f'<ul class="zeya-needs__benefits">{benefits}</ul>'
            f'<div class="zeya-needs__actions">{h.btn("See options", slug + ".html", "gold")}'
            f'{h.btn("Book a consultation", "contact.html", "outline", arrow=False)}</div>'
            f'</div></article>')
    return f'''<section class="zeya-needs" id="find-your-solution" aria-labelledby="zeya-needs-title" data-zeya-needs>
  <div class="zeya-container">
    <div class="zeya-needs__head"><div><p class="zeya-eyebrow">Find your solution</p><h2 id="zeya-needs-title">Start with the problem.</h2></div><p>Choose what bothers you about your window, and we&rsquo;ll show you the combination we recommend.</p></div>
    <div class="zeya-needs__body">
      <div class="zeya-needs__tabs" data-zeya-needs-tabs aria-label="Window problems">{''.join(tabs)}</div>
      <div class="zeya-needs__panels">{''.join(panels)}</div>
    </div>
  </div>
</section>'''


# The communities we visit most. Each chip opens a WhatsApp chat that names
# the community; until a number is configured it falls back to the contact page.
SERVICE_AREAS = [
    'Arabian Ranches', 'Downtown Dubai', 'JLT', 'JBR', 'The Springs', 'The Meadows',
    'DAMAC Hills', 'Al Barsha', 'Mirdif', 'Silicon Oasis', 'Motor City', 'Tilal Al Ghaf',
    'Meydan', 'Dubai Creek Harbour', 'Emirates Hills', 'Dubai Marina', 'DAMAC Hills 1',
    'Town Square', 'Jumeirah Golf Estates', 'Jumeirah Village Circle (JVC)', 'Palm Jumeirah',
    'Jumeirah Islands', 'Jumeirah Park', 'Mira &amp; Mira Oasis', 'The Lakes', 'Business Bay',
    'Dubai Hills', 'Mudon', 'Dubai Sports City',
]


def service_areas_section(h):
    """The "Service Areas We Cover" band: one chip per community."""
    chips = ''.join(
        f'<li><a class="zeya-areas__chip" href="contact.html" data-zeya-wa="area" '
        f'data-zeya-wa-area="{area}">{area}</a></li>'
        for area in SERVICE_AREAS)
    return f'''<section class="zeya-areas" id="service-areas" aria-labelledby="zeya-areas-title">
  <div class="zeya-container">
    <div class="zeya-areas__top">
      <div class="zeya-areas__copy">
        <p class="zeya-eyebrow">We come to you</p>
        <h2 id="zeya-areas-title">Service Areas<br>We Cover</h2>
        <p class="zeya-areas__lead">From waterfront apartments to family villas, our team brings samples, advice and precise measuring directly to your space.</p>
        <p class="zeya-areas__note"><strong>{len(SERVICE_AREAS)}</strong><span>Dubai communities<br>and the wider UAE</span></p>
      </div>
      <div class="zeya-areas__media">
        <video class="zeya-areas__video" data-zeya-motion-video data-src="assets/videos/zeya-brand-film.mp4" poster="assets/images/zeya-brand-film-poster.webp" muted loop playsinline preload="none" aria-hidden="true" tabindex="-1"></video>
        <span class="zeya-areas__film-label">Across Dubai</span>
        <button class="zeya-areas__toggle" type="button" data-zeya-motion-toggle aria-label="Play video" hidden>
          <svg class="zeya-motion__play" viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path d="M4 2.5v11l9.5-5.5z"/></svg>
          <svg class="zeya-motion__pause" viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path d="M3.5 2.5h3v11h-3zM9.5 2.5h3v11h-3z"/></svg>
        </button>
      </div>
    </div>
    <div class="zeya-areas__directory"><p>Choose your community to enquire</p><span aria-hidden="true"></span></div>
    <ul class="zeya-areas__list">{chips}</ul>
  </div>
</section>'''


# The line ZEYA asked to greet clients with when they are invited to review.
REVIEW_MESSAGE = ('We&rsquo;d love to hear about your experience with us. Your feedback means '
                  'a lot to our team and encourages us to keep delivering exceptional service.')


def review_button(h, variant='gold'):
    """The "Write a Google review" button. main.js links it, and shows it, once
    CONTACT.googleReview is configured, so it never points at nothing."""
    return (f'<a class="zeya-btn zeya-btn--{variant} zeya-btn--review" data-zeya-review hidden>'
            f'{h.icon("star")}Write a Google review</a>')


# PLACEHOLDER: sample cards to show the layout until real Google reviews are
# chosen. Each card says "Sample review" on the page, so none of them can pass
# for a real client's words. Replace with genuine reviews (quoted with the
# client's permission) or remove before launch.
SAMPLE_REVIEWS = [
    ('Client name', 'Blackout curtains &middot; Villa',
     'From the first visit to the final fitting, everything was clear and on time. '
     'The blackout curtains fit perfectly and the bedroom finally stays dark.'),
    ('Client name', 'Motorised blinds &middot; Apartment',
     'They explained every option without any pressure. The motorised blinds work '
     'with our phones and the installation was spotless.'),
    ('Client name', 'Sheer &amp; wave curtains &middot; Living room',
     'We compared fabric samples in our own light, which made choosing easy. '
     'The sheers soften the afternoon sun beautifully.'),
    ('Client name', 'Roller blinds &middot; Office',
     'Measured, quoted and installed across the whole office with no disruption. '
     'Clean lines and exactly the light control we needed.'),
    ('Client name', 'Roman blinds &middot; Majlis',
     'The team helped us pick a fabric that suits the room perfectly. '
     'Careful installers who left everything tidy.'),
    ('Client name', 'Curtain tracks &middot; Penthouse',
     'Precise measuring on very tall windows and a flawless finish. '
     'Friendly, professional and easy to deal with.'),
]


def _review_card(h, name, meta, text):
    stars = ''.join(h.icon('star-fill') for _ in range(5))
    return (f'<figure class="zeya-review-card">'
            f'<div class="zeya-review-card__top"><span class="zeya-review-card__stars" '
            f'role="img" aria-label="5 out of 5 stars">{stars}</span>'
            f'<span class="zeya-review-card__tag">Sample review</span></div>'
            f'<blockquote><p>&ldquo;{text}&rdquo;</p></blockquote>'
            f'<figcaption><strong>{name}</strong><span>{meta}</span></figcaption></figure>')


def reviews_section(h):
    """The Google Reviews band that closes the home page.

    The review cards drift sideways on a loop: the track holds two identical
    runs and travels half its width, so the second run lands where the first
    began. Only the first run is exposed to assistive tech. The band stays
    hidden until a review link is configured.
    """
    stars = ''.join(h.icon('star') for _ in range(5))
    run = ''.join(_review_card(h, *row) for row in SAMPLE_REVIEWS)
    track = (f'<div class="zeya-reviews__run">{run}</div>'
             f'<div class="zeya-reviews__run" aria-hidden="true">{run}</div>')
    return f'''<section class="zeya-reviews" id="reviews" aria-labelledby="zeya-reviews-title" data-zeya-review-section hidden>
  <div class="zeya-container zeya-reviews__inner">
    <p class="zeya-eyebrow">Google Reviews</p>
    <div class="zeya-reviews__stars" aria-hidden="true">{stars}</div>
    <h2 id="zeya-reviews-title">Tell us how we did.</h2>
    <p>{REVIEW_MESSAGE}</p>
  </div>
  <div class="zeya-reviews__marquee" role="region" tabindex="0" aria-label="Client reviews">
    <div class="zeya-reviews__track">{track}</div>
  </div>
  <div class="zeya-container zeya-reviews__actions">{review_button(h)}</div>
</section>'''


def render(h):
    def photo(name, alt, sizes='100vw', eager=False):
        return h.img(name, alt, sizes=sizes, eager=eager)

    def feature(icon, title, text):
        return f'<div class="zeya-signature-feature">{h.icon(icon)}<span>{title}<small>{text}</small></span></div>'

    solutions = ''.join(
        f'<a class="zeya-solution" href="{slug}.html">'
        f'{photo(image, alt, "(max-width:700px) 100vw, 33vw")}'
        f'<div class="zeya-solution__caption"><div><h3>{title}</h3><p>{caption}</p></div>'
        f'<span class="zeya-circle-arrow" aria-hidden="true">{h.icon("arrow-right")}</span></div></a>'
        for slug, image, title, caption, alt in [
            ('curtains', 'ai-collection-curtains-v2', 'Curtains', 'Timeless elegance', 'Layered ivory sheers and warm taupe curtains in a luxury Dubai living room'),
            ('blinds', 'ai-collection-blinds-v2', 'Blinds', 'Modern functionality', 'Made-to-measure Roman and sunscreen blinds overlooking Dubai'),
            ('motorized', 'ai-motorized-curtains', 'Motorized Curtains &amp; Blinds', 'Smart living', 'Phone app controlling motorized curtains in a Dubai living room'),
        ])
    products = ''.join(
        f'<a class="zeya-mini-product" href="product-{slug}.html">'
        f'{photo("product-"+slug, "Product inspiration: "+title, "(max-width:700px) 43vw, 14vw")}'
        f'<h3>{title}</h3><p>{caption}</p></a>'
        for slug, title, caption in [
            ('sheer-curtains', 'Sheer Curtains', 'Light &amp; airy'),
            ('blackout-curtains', 'Blackout Curtains', 'Complete privacy'),
            ('roman-blinds', 'Roman Blinds', 'Classic appeal'),
            ('roller-blinds', 'Roller Blinds', 'Sleek &amp; versatile'),
            ('zebra-blinds', 'Zebra Blinds', 'Light control'),
            ('vertical-blinds', 'Vertical Blinds', 'Modern spaces'),
            ('smart-window-automation', 'Motorised Systems', 'Effortless living'),
        ])
    qualities = ''.join(feature(*row) for row in [
        ('diamond', 'Premium', 'Quality'), ('grid', 'Custom', 'Made'),
        ('ruler', 'Expert', 'Installation'), ('heart', 'Considered', 'Details')])
    # The hero film. The poster frame carries the hero on its own until
    # main.js decides whether to load the video at all — it skips it for
    # reduced-motion visitors and picks the light file on small screens, so
    # nothing but the poster is fetched before that choice is made.
    hero_video = (
        '<video class="zeya-hero__video" data-zeya-hero-video'
        ' data-src="assets/videos/hero-city-lights.mp4"'
        ' data-src-sm="assets/videos/hero-city-lights-854.mp4"'
        ' poster="assets/images/hero-city-lights-poster.webp"'
        ' width="1136" height="720" autoplay muted loop playsinline'
        ' preload="none" aria-hidden="true" tabindex="-1"></video>')

    return f'''
<section class="zeya-hero zeya-signature-hero">
  <div class="zeya-hero__media">{hero_video}</div>
  <div class="zeya-hero__scrim" aria-hidden="true"></div>
  <div class="zeya-container zeya-hero__inner">
    <p class="zeya-hero__eyebrow">Windows that inspire</p>
    <h1 class="zeya-hero__title zeya-hero__title--steps"><span class="zeya-hero__step"><span class="zeya-hero__word">Measured<span class="zeya-hero__dot">.</span></span></span> <span class="zeya-hero__step"><span class="zeya-hero__word">Designed<span class="zeya-hero__dot">.</span></span></span> <span class="zeya-hero__step"><em class="zeya-hero__word">Installed.</em></span></h1>
    <p class="zeya-hero__sub">Bespoke and motorized curtains and blinds<br class="zeya-desktop-break"> for homes and workplaces across Dubai, UAE.</p>
    <div class="zeya-hero__actions">{h.btn('Explore collection', '#solutions', 'gold')}{h.btn('Book consultation', 'contact.html', 'outline')}</div>
    <div class="zeya-hero-promises"><div class="zeya-hero-promises__item"><svg class="zeya-hero-promises__icon" aria-hidden="true" focusable="false"><use href="#zeya-i-swatch"></use></svg><span>Beautiful<small>Fabrics</small></span></div><div class="zeya-hero-promises__item"><svg class="zeya-hero-promises__icon" aria-hidden="true" focusable="false"><use href="#zeya-i-grid"></use></svg><span>Custom<small>Solutions</small></span></div><div class="zeya-hero-promises__item"><svg class="zeya-hero-promises__icon" aria-hidden="true" focusable="false"><use href="#zeya-i-pencil"></use></svg><span>Thoughtful<small>Design</small></span></div><div class="zeya-hero-promises__item"><svg class="zeya-hero-promises__icon" aria-hidden="true" focusable="false"><use href="#zeya-i-tools"></use></svg><span>End-to-end<small>Service</small></span></div></div>
    <a class="zeya-scroll-cue" href="#solutions"><span class="zeya-circle-arrow">{h.icon('arrow-right')}</span>Scroll to discover</a>
  </div>
</section>
<section class="zeya-solutions" id="solutions">
  <div class="zeya-container">
    <div class="zeya-signature-heading"><div><p class="zeya-eyebrow">Made for your space</p><h2>Explore Our Solutions</h2></div><p>From elegant curtains to modern blinds and smart automation,<br class="zeya-desktop-break"> ZEYA brings style, comfort and functionality to every space.</p><a class="zeya-text-link" href="products.html">View all products {h.icon('arrow-right')}</a></div>
    <p class="zeya-swipe-hint" aria-hidden="true">Swipe to explore <span>&rarr;</span></p>
    <div class="zeya-solution-grid" aria-label="Explore our solutions">{solutions}</div>
  </div>
</section>
<section class="zeya-signature-collection" id="collection">
  <div class="zeya-container">
    <div class="zeya-signature-heading"><div><h2>The ZEYA Collection</h2><p class="zeya-eyebrow">A curated range for every style, every space.</p></div><a class="zeya-text-link" href="products.html">View all collections {h.icon('arrow-right')}</a></div>
    <p class="zeya-swipe-hint" aria-hidden="true">Swipe through the collection <span>&rarr;</span></p>
    <div class="zeya-mini-grid" aria-label="The ZEYA collection">{products}</div>
  </div>
</section>
<section class="zeya-art" id="why-zeya">
  <div class="zeya-art__media">{photo('signature-fabric', 'AI textile study: bronze linen and luminous ivory sheer curtain folds', '(max-width:700px) 100vw, 54vw')}<p>More than<br><span>Window Coverings</span></p></div>
  <div class="zeya-art__copy"><p class="zeya-eyebrow">The ZEYA difference <span aria-hidden="true"></span></p><h2>The Art of Light</h2><p>We don’t just cover windows, we transform spaces.<br>At ZEYA, every fabric, texture and detail is chosen<br class="zeya-desktop-break"> to bring harmony, comfort and style to your home or workspace.</p><div class="zeya-quality-grid">{qualities}</div><div class="zeya-art__actions">{h.btn('Discover our story', 'about.html', 'gold')}{h.btn('Terms &amp; Conditions', 'terms.html', 'line')}</div></div>
</section>
{needs_section(h)}
{service_areas_section(h)}
{services_section(h)}
{why_band(h)}
{reviews_section(h)}
'''
