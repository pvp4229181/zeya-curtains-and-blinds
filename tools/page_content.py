#!/usr/bin/env python3
"""Page bodies for the ZEYA static site. Consumed by build_pages.py."""


def render(h):
    img, icon, btn = h.img, h.icon, h.btn

    # ---------------------------------------------------------------- bits --
    def benefit(icon_name, title):
        return (
            '<article class="zeya-benefit zeya-reveal">'
            '<span class="zeya-benefit__icon">%s</span>'
            '<h3 class="zeya-benefit__title">%s</h3>'
            "</article>" % (icon(icon_name), title)
        )

    def benefits_strip(items, heading, dark=False):
        # The strip carries a named (visually hidden) heading so the H3 item
        # labels below it never jump a level in the document outline.
        return (
            '<section class="zeya-benefits%s" aria-labelledby="%s">'
            '<h2 class="zeya-sr-only" id="%s">%s</h2>'
            '<div class="zeya-container zeya-container--wide zeya-benefits__grid zeya-stagger">%s</div>'
            "</section>" % (" zeya-benefits--dark" if dark else "",
                            heading[1], heading[1], heading[0],
                            "".join(benefit(*item) for item in items))
        )

    def crumbs(label):
        return (
            '<nav class="zeya-crumbs" aria-label="Breadcrumb">'
            '<a href="index.html">Home</a>'
            '<span class="zeya-crumbs__sep" aria-hidden="true">/</span>'
            '<span aria-current="page">%s</span>'
            "</nav>" % label
        )

    def pagehead(title, label, lead, text):
        return """
<section class="zeya-pagehead">
  <div class="zeya-container zeya-pagehead__grid">
    <div class="zeya-pagehead__left zeya-reveal">
      <h1 class="zeya-pagehead__title">%s</h1>
      <span class="zeya-rule"></span>
      %s
    </div>
    <div class="zeya-pagehead__right zeya-reveal" style="--zeya-delay:120ms">
      <h2 class="zeya-pagehead__lead">%s</h2>
      <p class="zeya-pagehead__text">%s</p>
    </div>
  </div>
</section>""" % (title, crumbs(label), lead, text)

    def value(icon_name, title):
        return (
            '<article class="zeya-value">'
            '<span class="zeya-value__icon">%s</span>'
            '<h3 class="zeya-value__title">%s</h3>'
            "</article>" % (icon(icon_name), title)
        )

    def card(image, alt, title, text, href, wide=False):
        return """
<article class="zeya-card%s zeya-reveal">
  <a class="zeya-card__link" href="%s">
    %s
    <span class="zeya-card__veil" aria-hidden="true"></span>
    <div class="zeya-card__body">
      <div>
        <h3 class="zeya-card__title">%s</h3>
        <p class="zeya-card__text">%s</p>
      </div>
      <span class="zeya-arrow-btn" aria-hidden="true">%s</span>
    </div>
  </a>
</article>""" % (" zeya-card--wide" if wide else "", href,
                 img(image, alt, sizes="(max-width: 560px) 100vw, (max-width: 860px) 50vw, 33vw",
                     cls="zeya-card__img"),
                 title, text, icon("arrow-right"))

    def listing(items):
        return '<ul class="zeya-list">%s</ul>' % "".join("<li>%s</li>" % i for i in items)

    def step(number, icon_name, title, text):
        return """
<li class="zeya-step">
  <span class="zeya-step__icon">%s</span>
  <span class="zeya-step__num">%s</span>
  <h3 class="zeya-step__title">%s</h3>
  <p class="zeya-step__text">%s</p>
</li>""" % (icon(icon_name), number, title, text)

    def method(icon_name, label, key):
        return """
<a class="zeya-method" data-zeya-contact="%s">
  <span class="zeya-method__icon">%s</span>
  <span>
    <span class="zeya-method__label">%s</span>
    <span class="zeya-method__value" data-zeya-contact-value></span>
  </span>
</a>""" % (key, icon(icon_name), label)

    def quote_banner():
        return """
<section class="zeya-quote">
  <div class="zeya-quote__media" data-zeya-parallax="0.09">
    %s
  </div>
  <div class="zeya-container zeya-quote__grid">
    <blockquote class="zeya-quote__text" data-zeya-lines>&ldquo;Beautiful Spaces<br>Start at the Window&rdquo;</blockquote>
    <div class="zeya-quote__note zeya-reveal">
      <p>&ldquo;Our mission is to bring style, comfort and innovation to every space we touch.&rdquo;</p>
      <cite class="zeya-quote__cite">&mdash; ZEYA Curtains &amp; Blinds</cite>
    </div>
  </div>
</section>""" % img("quote-banner-fabric",
                    "Close detail of softly folded curtain fabric catching warm side light",
                    sizes="100vw")

    # ================================================================= HOME ==
    home = """
<section class="zeya-hero" data-zeya-hero>
  <div class="zeya-hero__media" data-zeya-parallax="0.07">
    {hero}
  </div>
  <div class="zeya-hero__overlay" aria-hidden="true"></div>

  <div class="zeya-container zeya-container--wide zeya-hero__inner">
    <div class="zeya-hero__copy">
      <h1 class="zeya-hero__title" data-zeya-lines>Custom Curtains,<br>Blinds &amp; Motorized<br>Window Solutions<br>in Dubai</h1>
      <p class="zeya-hero__sub">Elegant. Functional. Made for Your Space.</p>
      <div class="zeya-hero__actions">
        {cta}
      </div>
    </div>
  </div>

  <div class="zeya-container zeya-container--wide zeya-hero__foot">
    <ol class="zeya-hero__slides" role="presentation">
      <li class="zeya-hero__slide is-active" data-zeya-hero-mark>01</li>
      <li class="zeya-hero__slide" data-zeya-hero-mark>02</li>
      <li class="zeya-hero__slide" data-zeya-hero-mark>03</li>
    </ol>
    <p class="zeya-hero__tag">Transforming Spaces<br>Through Beautiful Windows</p>
  </div>
</section>

{benefits}

<section class="zeya-section zeya-split zeya-split--bleed zeya-split--bleed-left">
  <div class="zeya-container zeya-split__grid">
    <figure class="zeya-split__media zeya-split__media--bleed-left zeya-figure zeya-reveal-mask">
      {intro_img}
    </figure>
    <div class="zeya-split__copy">
      <h2 class="zeya-h2 zeya-split__title" data-zeya-lines>Beautiful Windows<br>Brighter Living</h2>
      <p class="zeya-text zeya-lead zeya-reveal">At ZEYA, we create custom-made curtains and blinds that bring
        elegance, comfort and functionality to your home or workspace.</p>
      <p class="zeya-text zeya-reveal">Every project starts with your space. We guide you through fabrics,
        colours, styles and light control, then measure accurately and install professionally &mdash; so the
        finished result looks considered and works effortlessly, every day.</p>
      <div class="zeya-reveal">{explore}</div>
    </div>
  </div>
</section>

<section class="zeya-section zeya-section--cream">
  <div class="zeya-container">
    <div class="zeya-center zeya-measure zeya-mx-auto zeya-reveal">
      <span class="zeya-label">What We Do</span>
      <h2 class="zeya-h2 zeya-mt-sm">Complete Curtains &amp; Blinds Solutions</h2>
      <p class="zeya-text zeya-mx-auto zeya-mt-sm">From timeless curtains to modern automated blinds, ZEYA
        offers a range of window solutions for different interiors, requirements and budgets.</p>
    </div>
    <div class="zeya-cards zeya-mt zeya-stagger">
      {cards}
    </div>
  </div>
</section>

{quote}
""".format(
        hero=img("hero-luxury-curtains",
                 "Sunlit Dubai living room with floor-to-ceiling windows, layered sheer and blackout "
                 "curtains and the city skyline beyond",
                 sizes="100vw", eager=True),
        cta=btn("Book a Free Consultation", "contact.html", "gold"),
        benefits=benefits_strip((
            ("diamond", "Premium Quality<br>Materials"),
            ("home", "Custom Made<br>for Your Space"),
            ("gear", "Motorized<br>Solutions"),
            ("heart", "Elegant &amp; Functional<br>Designs"),
        ), ("Why clients choose ZEYA", "zeya-benefits-heading")),
        intro_img=img("intro-living-room",
                      "Bright neutral living room with sheer curtains diffusing daylight across a linen sofa",
                      sizes="(max-width: 1024px) 100vw, 52vw"),
        explore=btn("Explore Our Products", "products.html", "gold"),
        cards="".join([
            card("curtains-category", "Layered curtains in warm neutral fabric beside a sunlit window",
                 "Curtains", "Elegant fabrics for every space", "curtains.html"),
            card("blinds-category", "Horizontal slat blinds filtering daylight in a modern interior",
                 "Blinds", "Modern &amp; versatile options", "blinds.html"),
            card("motorized-solutions", "Motorized blind lowering over a city view, controlled from a phone",
                 "Motorized Solutions", "Smart living made simple", "motorized.html"),
        ]),
        quote=quote_banner(),
    )

    # ================================================================ ABOUT ==
    about = """
<section class="zeya-abouthero">
  <div class="zeya-container zeya-container--wide zeya-abouthero__grid">
    <figure class="zeya-abouthero__media zeya-reveal-mask">
      {about_img}
    </figure>
    <div class="zeya-abouthero__copy">
      <h1 class="zeya-pagehead__title zeya-reveal">About Us</h1>
      <span class="zeya-rule zeya-reveal" style="--zeya-delay:80ms"></span>
      {crumbs}
      <h2 class="zeya-h2" data-zeya-lines>More Than<br>Just Window Coverings</h2>
      <p class="zeya-text zeya-lead zeya-reveal">At ZEYA Curtains &amp; Blinds, we believe windows should be
        more than just covered &mdash; they should be beautifully designed to enhance the way you live and work.</p>
      <p class="zeya-text zeya-reveal">We create custom-made curtains, blinds and motorized window solutions
        that bring together elegance, comfort, privacy and effortless functionality.</p>
      <p class="zeya-text zeya-reveal">From choosing the perfect fabric and style to precise measurement and
        professional installation, we make every step simple, seamless and tailored to your space.</p>
      <p class="zeya-text zeya-reveal">We take the time to understand your space, your style and your practical
        requirements before recommending a suitable solution. Our team guides you through fabrics, colours,
        designs and functionality, followed by accurate measurement and professional installation.</p>
    </div>
  </div>
</section>

<section class="zeya-section zeya-section--sm">
  <div class="zeya-container">
    <div class="zeya-values zeya-stagger">
      {values}
    </div>
  </div>
</section>

{quote}

<section class="zeya-section zeya-split zeya-split--bleed zeya-split--bleed-right">
  <div class="zeya-container zeya-split__grid">
    <div class="zeya-split__copy">
      <span class="zeya-label zeya-reveal">How We Work</span>
      <h2 class="zeya-h2" data-zeya-lines>Considered at<br>Every Step</h2>
      <p class="zeya-text zeya-reveal">Fabric selection, colour selection, curtain and blind styles,
        measurement, recommendations and professional installation &mdash; each stage is handled by our own
        team, so nothing is left to chance between the first consultation and the finished window.</p>
      <ul class="zeya-list zeya-reveal">
        <li>Fabric selection guided by light, privacy and wear</li>
        <li>Colour and finish matched to your interior</li>
        <li>Curtain and blind styles suited to the room</li>
        <li>On-site measurement by our own team</li>
        <li>Clear recommendations before you commit</li>
        <li>Professional installation and final adjustment</li>
      </ul>
      <div class="zeya-reveal">{process_btn}</div>
    </div>
    <figure class="zeya-split__media zeya-split__media--bleed-right zeya-figure zeya-reveal-mask">
      {process_img}
    </figure>
  </div>
</section>
""".format(
        about_img=img("about-zeya-curtains",
                      "Dining area with full-height sheer curtains, an olive tree and soft morning light",
                      sizes="(max-width: 1024px) 100vw, 46vw"),
        crumbs=crumbs("About"),
        values="".join([
            value("diamond", "Quality Craftsmanship"),
            value("people", "Personalized Service"),
            value("gear", "Modern Solutions"),
            value("heart", "Customer Satisfaction"),
        ]),
        quote=quote_banner(),
        process_btn=btn("See Our Process", "process.html", "outline"),
        process_img=img("fabric-consultation",
                        "Stacked curtain fabric samples in warm neutral tones",
                        sizes="(max-width: 1024px) 100vw, 50vw"),
    )

    # ============================================================= PRODUCTS ==
    curtain_types = [
        "Sheer Curtains", "Blackout Curtains", "Linen Curtains", "Velvet Curtains",
        "Wave Curtains", "Pinch Pleat Curtains", "Double / Layered Curtains", "Motorized Curtains",
    ]
    blind_types = [
        "Roller Blinds", "Zebra Blinds", "Roman Blinds", "Venetian Blinds", "Wooden Blinds",
        "Faux Wood Blinds", "Vertical Blinds", "Honeycomb Blinds", "Sunscreen Blinds",
        "Motorized Blinds", "Outdoor / Zip Screen Blinds",
    ]

    products = """
{head}

<section class="zeya-section zeya-section--sm">
  <div class="zeya-container">
    <div class="zeya-cards zeya-stagger">
      {cards}
    </div>
  </div>
</section>

<section class="zeya-section zeya-section--sm zeya-section--cream">
  <div class="zeya-container">
    <div class="zeya-types zeya-stagger">

      <article class="zeya-type zeya-reveal" id="curtains">
        <h2 class="zeya-type__title">Curtain Types</h2>
        {curtain_list}
        <figure class="zeya-type__media">
          <div class="zeya-figure zeya-ratio-4x3">{curtain_img}</div>
        </figure>
      </article>

      <article class="zeya-type zeya-reveal" id="blinds">
        <h2 class="zeya-type__title">Blind Types</h2>
        {blind_list}
        <figure class="zeya-type__media">
          <div class="zeya-figure zeya-ratio-4x3">{blind_img}</div>
        </figure>
      </article>

      <article class="zeya-type zeya-type--wide zeya-reveal" id="motorized">
        <h2 class="zeya-type__title">Motorized Solutions</h2>
        <p class="zeya-type__text">Smart curtain and blind systems designed for modern homes and
          commercial spaces. Operate a single window or a whole room by remote or from your phone,
          set opening and closing times, and keep heavy or hard-to-reach coverings moving smoothly
          without pulling a cord.</p>
        <p class="zeya-type__text zeya-mt-sm">Motorization can be specified for most of our curtain
          and blind ranges, including outdoor zip screen blinds. We confirm the right system for your
          windows and power arrangement during the site visit.</p>
        <figure class="zeya-type__media zeya-type__media--full">
          <div class="zeya-figure zeya-ratio-4x3">{motor_img}</div>
        </figure>
      </article>

    </div>
  </div>
</section>

{strip}
""".format(
        head=pagehead(
            "What We Do", "Products",
            "Complete Curtains &amp; Blinds Solutions",
            "From timeless curtains to modern automated blinds, ZEYA offers a range of window solutions "
            "for different interiors, requirements and budgets.",
        ),
        cards="".join([
            card("curtains-category", "Layered curtains in warm neutral fabric beside a sunlit window",
                 "Curtains", "Elegant fabrics for every space", "#curtains"),
            card("blinds-category", "Horizontal slat blinds filtering daylight in a modern interior",
                 "Blinds", "Modern &amp; versatile options", "#blinds"),
            card("motorized-solutions", "Motorized blind lowering over a city view, controlled from a phone",
                 "Motorized Solutions", "Smart living made simple", "#motorized"),
        ]),
        curtain_list=listing(curtain_types),
        blind_list=listing(blind_types),
        curtain_img=img("curtain-types", "Detail of floor-length curtain folds in a soft natural weave",
                        sizes="(max-width: 768px) 60vw, 20vw"),
        blind_img=img("blind-types", "Detail of slatted blinds with daylight filtering between the slats",
                      sizes="(max-width: 768px) 60vw, 20vw"),
        motor_img=img("motorized-app-control",
                      "Motorized blind being adjusted from a smartphone app in a darkened room",
                      sizes="(max-width: 768px) 60vw, 30vw"),
        strip=benefits_strip((
            ("grid", "Wide Range<br>of Options"),
            ("pencil", "Custom<br>Made"),
            ("diamond", "Premium<br>Materials"),
            ("doc", "For Homes<br>&amp; Businesses"),
        ), ("What every ZEYA solution includes", "zeya-products-strip-heading"), dark=True),
    )

    # ============================================================== PROCESS ==
    process = """
{head}

<section class="zeya-section zeya-section--sm" style="padding-top:0">
  <div class="zeya-container">
    <figure class="zeya-process__hero zeya-reveal-mask">
      {consult_img}
    </figure>

    <ol class="zeya-timeline zeya-mt zeya-stagger">
      {steps}
    </ol>

    <div class="zeya-gallery zeya-mt zeya-stagger">
      <figure class="zeya-figure zeya-reveal">{g1}</figure>
      <figure class="zeya-figure zeya-reveal">{g2}</figure>
      <figure class="zeya-figure zeya-reveal">{g3}</figure>
    </div>

    <p class="zeya-closing zeya-mt zeya-measure zeya-mx-auto" data-zeya-lines>You choose the look.<br>We take care of the details.</p>
  </div>
</section>
""".format(
        head=pagehead(
            "Our Process", "Process",
            "A simple process designed<br>around your convenience.",
            "Six clear steps from first enquiry to the final fitting, handled end to end by the ZEYA team.",
        ),
        consult_img=img("process-consultation",
                        "ZEYA consultant showing curtain fabric samples to a customer at a table",
                        sizes="(max-width: 1320px) 100vw, 1320px"),
        steps="".join([
            step("01", "calendar", "Book a Free Consultation",
                 "Contact us through WhatsApp, phone or our enquiry form."),
            step("02", "home", "We Visit Your Space",
                 "Our team visits your home, office or project with relevant samples and recommendations."),
            step("03", "swatch", "Choose Your Solution",
                 "Select your preferred fabric, colour, curtain style, blind or motorized system."),
            step("04", "ruler", "Accurate Measurement",
                 "We take precise measurements for your windows."),
            step("05", "doc", "Quotation &amp; Approval",
                 "You receive a clear quotation based on your selected solution."),
            step("06", "tools", "Professional Installation",
                 "Once approved, our team prepares and installs your curtains or blinds."),
        ]),
        g1=img("fabric-consultation", "Curtain fabric samples fanned out in warm neutral tones",
               sizes="(max-width: 560px) 100vw, (max-width: 860px) 100vw, 33vw"),
        g2=img("window-measurement", "ZEYA team member measuring a full-height window",
               sizes="(max-width: 860px) 50vw, 33vw"),
        g3=img("curtain-installation", "ZEYA installer fitting a curtain track above a bright window",
               sizes="(max-width: 860px) 50vw, 33vw"),
    )

    # ============================================================== CONTACT ==
    contact = """
<section class="zeya-contact">
  <div class="zeya-container zeya-container--wide zeya-contact__grid">

    <div class="zeya-contact__copy">
      <h1 class="zeya-pagehead__title zeya-reveal">Contact Us</h1>
      <span class="zeya-rule zeya-reveal" style="--zeya-delay:80ms"></span>
      {crumbs}
      <h2 class="zeya-h2" data-zeya-lines>Let&rsquo;s Transform<br>Your Windows</h2>
      <p class="zeya-text zeya-lead zeya-reveal">Not sure which curtains or blinds are right for your space?</p>
      <p class="zeya-text zeya-reveal">Our team can help you select the right combination of style, fabric,
        privacy, light control and functionality.</p>
      <p class="zeya-text zeya-reveal">Book a consultation and let us bring the options to you.</p>

      <div class="zeya-methods zeya-reveal">
        {methods}
      </div>

      <div class="zeya-contact__actions zeya-reveal">
        {cta}
      </div>
    </div>

    <div class="zeya-contact__panel">
      <div class="zeya-contact__panel-media" aria-hidden="true">
        {panel_img}
      </div>

      <div class="zeya-formcard zeya-reveal">
        <h2 class="zeya-formcard__title">Send Us a Message</h2>

        <!-- Field names follow the Contact Form 7 / WPForms convention so this
             markup can be swapped for a plugin-rendered form without restyling.
             `action` is intentionally empty until a real handler is connected. -->
        <form class="zeya-form" data-zeya-form action="" method="post" novalidate>
          <p class="zeya-hp" aria-hidden="true">
            <label>Leave this field empty<input type="text" name="zeya-website-url" tabindex="-1"
                   autocomplete="off" data-zeya-hp></label>
          </p>

          <div class="zeya-field">
            <label class="zeya-field__label" for="zeya-name">Your Name</label>
            <input class="zeya-input" id="zeya-name" name="your-name" type="text"
                   autocomplete="name" placeholder="Your Name" required>
            <p class="zeya-field__error" id="zeya-name-error" role="alert"></p>
          </div>

          <div class="zeya-field">
            <label class="zeya-field__label" for="zeya-email">Your Email</label>
            <input class="zeya-input" id="zeya-email" name="your-email" type="email"
                   autocomplete="email" placeholder="Your Email" required>
            <p class="zeya-field__error" id="zeya-email-error" role="alert"></p>
          </div>

          <div class="zeya-field">
            <label class="zeya-field__label" for="zeya-phone">Your Phone</label>
            <input class="zeya-input" id="zeya-phone" name="your-phone" type="tel"
                   autocomplete="tel" placeholder="Your Phone" required>
            <p class="zeya-field__error" id="zeya-phone-error" role="alert"></p>
          </div>

          <div class="zeya-field">
            <label class="zeya-field__label" for="zeya-message">Your Message</label>
            <textarea class="zeya-textarea" id="zeya-message" name="your-message" rows="4"
                      placeholder="Tell us about your space" required></textarea>
            <p class="zeya-field__error" id="zeya-message-error" role="alert"></p>
          </div>

          <button class="zeya-btn zeya-btn--gold zeya-btn--block" type="submit">
            Send Message {arrow}
          </button>

          <p class="zeya-form__status" data-zeya-form-status data-state="info" role="status" aria-live="polite"></p>
        </form>
      </div>
    </div>

  </div>
</section>
""".format(
        crumbs=crumbs("Contact"),
        methods="".join([
            method("pin", "Dubai, UAE", "address"),
            method("whatsapp", "WhatsApp", "whatsapp"),
            method("phone", "Phone", "phone"),
            method("mail", "Email", "email"),
        ]),
        cta=btn("Book a Free Consultation", "#zeya-name", "gold"),
        panel_img=img("contact-interior",
                      "Dubai apartment interior with sheer curtains and skyline views",
                      sizes="(max-width: 1024px) 100vw, 46vw"),
        arrow=icon("arrow-right", "zeya-btn__arrow"),
    )

    return {"home": home, "about": about, "products": products,
            "process": process, "contact": contact}
