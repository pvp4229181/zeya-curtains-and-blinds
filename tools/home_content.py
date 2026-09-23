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
            ('curtains', 'signature-curtains', 'Curtains', 'Timeless elegance', 'AI interior concept: bronze curtains and ivory sheers in a sunlit bedroom'),
            ('blinds', 'signature-blinds', 'Blinds', 'Modern functionality', 'AI interior concept: warm wooden Venetian blinds filtering golden sunlight'),
            ('motorized', 'signature-motorized', 'Motorised Solutions', 'Smart living', 'AI interior concept: automated roller shades overlooking Dubai'),
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
    <h1 class="zeya-hero__title"><span>Dress Your<br>Windows.</span><br>Define Your Space.</h1>
    <p class="zeya-hero__sub">Bespoke curtains, blinds and automated window<br class="zeya-desktop-break"> solutions crafted for exceptional interiors.</p>
    <div class="zeya-hero__actions">{h.btn('Explore collection', '#solutions', 'gold')}{h.btn('Book consultation', 'contact.html', 'outline')}</div>
    <div class="zeya-hero-promises"><div class="zeya-hero-promises__item"><svg class="zeya-hero-promises__icon" aria-hidden="true" focusable="false"><use href="#zeya-i-swatch"></use></svg><span>Beautiful<small>Fabrics</small></span></div><div class="zeya-hero-promises__item"><svg class="zeya-hero-promises__icon" aria-hidden="true" focusable="false"><use href="#zeya-i-grid"></use></svg><span>Custom<small>Solutions</small></span></div><div class="zeya-hero-promises__item"><svg class="zeya-hero-promises__icon" aria-hidden="true" focusable="false"><use href="#zeya-i-pencil"></use></svg><span>Thoughtful<small>Design</small></span></div><div class="zeya-hero-promises__item"><svg class="zeya-hero-promises__icon" aria-hidden="true" focusable="false"><use href="#zeya-i-tools"></use></svg><span>End-to-end<small>Service</small></span></div></div>
    <a class="zeya-scroll-cue" href="#solutions"><span class="zeya-circle-arrow">{h.icon('arrow-right')}</span>Scroll to discover</a>
  </div>
</section>
<section class="zeya-solutions" id="solutions">
  <div class="zeya-container">
    <div class="zeya-signature-heading"><div><p class="zeya-eyebrow">Made for your space</p><h2>Explore Our Solutions</h2></div><p>From elegant curtains to modern blinds and smart automation,<br class="zeya-desktop-break"> ZEYA brings style, comfort and functionality to every space.</p><a class="zeya-text-link" href="products.html">View all products {h.icon('arrow-right')}</a></div>
    <div class="zeya-solution-grid">{solutions}</div>
  </div>
</section>
<section class="zeya-signature-collection" id="collection">
  <div class="zeya-container">
    <div class="zeya-signature-heading"><div><h2>The ZEYA Collection</h2><p class="zeya-eyebrow">A curated range for every style, every space.</p></div><a class="zeya-text-link" href="products.html">View all collections {h.icon('arrow-right')}</a></div>
    <div class="zeya-mini-grid">{products}</div>
  </div>
</section>
<section class="zeya-art" id="why-zeya">
  <div class="zeya-art__media">{photo('signature-fabric', 'AI textile study: bronze linen and luminous ivory sheer curtain folds', '(max-width:700px) 100vw, 54vw')}<p>More than<br><span>Window Coverings</span></p></div>
  <div class="zeya-art__copy"><p class="zeya-eyebrow">The ZEYA difference <span aria-hidden="true"></span></p><h2>The Art of Light</h2><p>We don’t just cover windows, we transform spaces.<br>At ZEYA, every fabric, texture and detail is chosen<br class="zeya-desktop-break"> to bring harmony, comfort and style to your home or workspace.</p><div class="zeya-quality-grid">{qualities}</div>{h.btn('Discover our story', 'about.html', 'gold')}</div>
</section>
{services_section(h)}
{why_band(h)}
'''
