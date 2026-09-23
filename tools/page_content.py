"""Editorial page layouts shared by the static site and WordPress theme.

Every page opens on the same full-bleed hero (build_pages.hero) and then
composes the same small set of sections, so the five editorial pages and the
five PHP templates cannot drift apart.
"""
from pathlib import Path


def render(h):
    img, btn, hero = h.img, h.btn, h.hero

    def eyebrow(text):
        return '<p class="zeya-eyebrow">%s</p>' % text

    def section(inner, cls=""):
        return '<section class="zeya-section %s">%s</section>' % (cls, inner)

    def heading(label, title, text="", action=""):
        return ('<div class="zeya-section-heading">' + eyebrow(label) +
                '<div><h2>%s</h2>%s%s</div></div>'
                % (title, '<p>%s</p>' % text if text else "", action))

    def collection(name, label, text, number):
        key = {"curtains": "curtains-category", "blinds": "blinds-category",
               "motorized": "motorized-solutions"}[name]
        return (
            '<a class="zeya-collection" href="{name}.html">'
            '<div class="zeya-collection__image">{image}'
            '<span class="zeya-collection__veil" aria-hidden="true"></span>'
            '<span class="zeya-collection__number">{number}</span></div>'
            '<div class="zeya-collection__title"><h3>{label}</h3>'
            '<span class="zeya-collection__arrow" aria-hidden="true">&#8599;</span></div>'
            '<p>{text}</p></a>'
        ).format(name=name, number=number, label=label, text=text,
                 image=img(key, label + " in a considered interior",
                           sizes="(max-width:700px) 100vw, 33vw"))

    steps = [
        ('01', 'A conversation',
         'Tell us about your space, your style and the way you want to live.'),
        ('02', 'A visit to your space',
         'We bring relevant samples and recommendations to your home or workplace.'),
        ('03', 'Your perfect combination',
         'Choose your fabric, finish, light control and operating system.'),
        ('04', 'Measured with care',
         'We take precise window measurements and plan the fitting details.'),
        ('05', 'A clear quotation',
         'Review the specification and quotation before you approve your order.'),
        ('06', 'The finishing touch',
         'Your curtains or blinds are prepared and professionally installed.'),
    ]

    def marquee(items, runs=4):
        """The scrolling service line.

        The run of items is repeated `runs` times and the track is animated
        by exactly half its width, so the second half lands where the first
        began and the loop is seamless. Four runs keeps the track wider than
        any realistic viewport, so there is never a gap at the tail. Only the
        first run is exposed to assistive tech; the repeats are decoration.
        """
        run = ''.join('<span>%s</span>' % text for text in items)
        copies = ''.join(
            '<div class="zeya-marquee__run"%s>%s</div>'
            % ('' if i == 0 else ' aria-hidden="true"', run)
            for i in range(runs))
        return ('<div class="zeya-marquee">'
                '<div class="zeya-marquee__track">%s</div></div>' % copies)

    def steplist(rows):
        return ('<div class="zeya-steps">' + ''.join(
            '<article class="zeya-step"><span class="zeya-step__num">%s</span>'
            '<h3>%s</h3><p>%s</p></article>' % row for row in rows) + '</div>')

    # Shared reference-inspired homepage.
    from home_content import render as render_home
    home = render_home(h)

    # ------------------------------------------------------------- about ---
    about = (
        hero('about-zeya-curtains',
             'Warm linen drapes beside natural stone in a Dubai interior',
             'A considered finish.<br>A more beautiful everyday.',
             eyebrow='The ZEYA story',
             sub='Custom curtains, blinds and motorized window solutions, thoughtfully '
                 'designed for homes and workplaces in Dubai.')
        + section('<div class="zeya-container zeya-split zeya-split--reverse">'
                  '<div class="zeya-split__media">{image}</div>'
                  '<div class="zeya-split__copy">{eyebrow}'
                  '<h2>Designed to feel<br>like you.</h2>'
                  '<p>At ZEYA, we believe a well-designed window can transform the way a '
                  'room feels. Softness, shade, privacy and proportion all have a part to '
                  'play.</p>'
                  '<p>We take time to understand how you use your space before recommending '
                  'the right fabric, style or operating system. Every decision is made '
                  'around your needs.</p>'
                  '<p>From your first fabric sample to the final installation, we keep the '
                  'process clear, personal and carefully considered.</p>'
                  '{cta}</div></div>'.format(
                      image=img('intro-living-room',
                                'A calm living room framed by floor-length curtains',
                                sizes='(max-width:700px) 100vw, 50vw'),
                      eyebrow=eyebrow('More than window coverings'),
                      cta=btn('Let’s talk about your space', 'contact.html', 'gold')))
        + section('<div class="zeya-container">'
                  + heading('Our values', 'Care in every detail.')
                  + steplist([
                      ('01', 'Personal guidance',
                       'Options chosen around your light, privacy and daily life.'),
                      ('02', 'Considered materials',
                       'Textures and finishes that bring your interior together.'),
                      ('03', 'A precise finish',
                       'Accurate measurement and professional installation.')])
                  + '</div>', 'zeya-section--chocolate')
    )

    # ----------------------------------------------------------- process ---
    process = (
        hero('process-consultation',
             'Fabric selection during an interior design consultation',
             'A beautiful result.<br>A simple journey.',
             eyebrow='From first idea to final installation',
             sub='We guide you through every decision, so choosing your curtains and '
                 'blinds feels as good as the finished space.')
        + section('<div class="zeya-container"><ol class="zeya-process">'
                  + ''.join('<li class="zeya-process__step">'
                            '<span class="zeya-process__num">%s</span>'
                            '<div><h2>%s</h2><p>%s</p></div></li>' % row for row in steps)
                  + '</ol></div>')
        + section('<div class="zeya-container zeya-split">'
                  '<div class="zeya-split__copy">{eyebrow}'
                  '<h2>See it. Feel it.<br>Make it yours.</h2>'
                  '<p>Explore colour, texture and light together. We will help you find a '
                  'combination that feels right in your own space.</p>{cta}</div>'
                  '<div class="zeya-split__media">{image}</div></div>'.format(
                      eyebrow=eyebrow('The details make the difference'),
                      cta=btn('Book a consultation', 'contact.html', 'gold'),
                      image=img('fabric-consultation',
                                'Linen, sheer and velvet fabric samples',
                                sizes='(max-width:700px) 100vw, 50vw')),
                  'zeya-section--chocolate')
    )

    # ----------------------------------------------------------- contact ---
    form = Path(__file__).with_name('contact-form.html').read_text(encoding='utf8')
    methods = ''.join(
        '<a class="zeya-method" data-zeya-contact="%s"><span>%s</span>'
        '<span data-zeya-contact-value></span></a>' % (key, label)
        for key, label in [('address', 'Studio'), ('phone', 'Phone'),
                           ('whatsapp', 'WhatsApp'), ('email', 'Email')])
    contact = (
        hero('contact-interior', 'Softly lit sheer curtains in a Dubai apartment',
             'Your space.<br>Our next conversation.',
             eyebrow='Let’s create something beautiful',
             sub='Tell us what you have in mind. We’ll help you explore the fabrics, '
                 'finishes and window solutions that suit your space.')
        + section('<div class="zeya-container zeya-contact">'
                  '<div class="zeya-contact__aside">{image}'
                  '<div class="zeya-contact__info">'
                  '<h2>Based in Dubai.<br>Designed around you.</h2>'
                  '<p>Home, office or commercial space — we begin with your needs.</p>'
                  '<div class="zeya-methods">{methods}</div></div></div>'
                  '<div class="zeya-formcard">{eyebrow}'
                  '<h2>Tell us about your space.</h2>'
                  '<p class="zeya-form-intro">Share a few details and the products '
                  'you’re considering.</p>{form}</div></div>'.format(
                      image=img('contact-interior',
                                'Sheer curtains diffusing afternoon light',
                                sizes='(max-width:700px) 100vw, 45vw'),
                      methods=methods, eyebrow=eyebrow('Start your project'), form=form))
    )


    # ------------------------------------------------------------- terms ---
    # The clauses supplied by ZEYA, renumbered 01-06 (the source document
    # skipped a number). Each clause is a heading plus its bullet points.
    clauses = [
        ('01', 'Pricing &amp; Payment', [
            'All prices are in AED unless otherwise agreed in writing.',
            'Payment can be made by bank transfer, cash, cheque, payment link, '
            'Visa or MasterCard.',
            'Cheques are considered payment only after successful clearance.',
            'Any changes to the confirmed order may result in additional charges.']),
        ('02', 'Custom-Made Products', [
            'Curtains and blinds are made according to the customer’s confirmed '
            'measurements, selections and specifications.',
            'Once production has started, customised items cannot normally be '
            'cancelled, returned or exchanged.',
            'Changes requested after production or installation may be treated as '
            'a new order.',
            'Natural variations in fabric colour, texture, weave and drape are '
            'normal characteristics of textile products.']),
        ('03', 'Installation Conditions', [
            'The customer is responsible for ensuring that the property is '
            'accessible and that any required building or management approvals are '
            'obtained before installation.',
            'The installation team will take reasonable care when drilling and '
            'fitting products.',
            'Walls and ceilings may contain concealed wiring, plumbing, HVAC '
            'services or weak substrates that cannot be identified through a visual '
            'inspection.',
            'Minor marks or touch-ups may occasionally be required during '
            'installation.',
            'Existing damage should be brought to the Company’s attention before '
            'installation.']),
        ('04', 'Motorized Products', [
            'Motorized curtains and blinds require a suitable and stable power '
            'supply.',
            'ZEYA Curtains &amp; Blinds is not responsible for faults caused by '
            'power fluctuations, surges, incorrect electrical connections or '
            'unsuitable electrical infrastructure.',
            'Any required electrical work or surge protection should be arranged by '
            'the customer through a qualified electrician.']),
        ('05', 'Warranty', [
            'A 12-month warranty is provided on eligible mechanisms and hardware '
            'against manufacturing or workmanship defects.',
            'The warranty does not cover normal wear and tear, fabric, misuse, '
            'accidental damage, incorrect operation, unauthorised alterations or '
            'electrical issues.',
            'Repairs or replacements will be provided where the issue is confirmed '
            'to be covered by the warranty and subject to parts availability.']),
        ('06', 'Confirmation', [
            'Once the quotation is approved or payment is made, the order is '
            'considered confirmed and these Terms &amp; Conditions are accepted.']),
    ]

    def clauselist(rows):
        return ('<div class="zeya-legal">' + ''.join(
            '<article class="zeya-legal__clause" id="clause-%s">'
            '<span class="zeya-legal__num">%s</span>'
            '<div><h2>%s</h2><ul class="zeya-legal__points">%s</ul></div></article>'
            % (num, num, title,
               ''.join('<li>%s</li>' % point for point in points))
            for num, title, points in rows) + '</div>')

    terms = (
        hero('about-zeya-curtains',
             'Floor-length curtains in a calm Dubai interior',
             'Clear terms.<br>Confident decisions.',
             eyebrow='Terms &amp; Conditions',
             sub='These terms apply to all quotations, orders, supply and installation '
                 'services provided by ZEYA Curtains &amp; Blinds.',
             variant='product')
        + section('<div class="zeya-container">'
                  '<p class="zeya-legal__intro">By approving a quotation or making '
                  'payment, the customer confirms acceptance of these terms.</p>'
                  + clauselist(clauses) + '</div>')
        + section('<div class="zeya-container zeya-split">'
                  '<div class="zeya-split__copy">{eyebrow}'
                  '<h2>Questions before<br>you approve?</h2>'
                  '<p>We are happy to walk you through your quotation, the '
                  'specification and anything in these terms before your order is '
                  'confirmed.</p>{cta}</div>'
                  '<div class="zeya-split__media">{image}</div></div>'.format(
                      eyebrow=eyebrow('Measure • Supply • Install'),
                      cta=btn('Talk to us', 'contact.html', 'gold'),
                      image=img('fabric-consultation',
                                'Fabric samples reviewed during a consultation',
                                sizes='(max-width:700px) 100vw, 50vw')),
                  'zeya-section--chocolate')
    )

    return {'home': home, 'about': about, 'process': process,
            'contact': contact, 'terms': terms, 'products': ''}
