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
             'The Story Behind<br><em>ZEYA</em>', eyebrow='Est. in Dubai',
             sub='Beautifully dressed. Effortlessly lived in.', variant='about')
        + section('<div class="zeya-container zeya-split zeya-split--reverse zeya-about-intro">'
                  '<div class="zeya-split__media">{image}</div>'
                  '<div class="zeya-split__copy"><span class="zeya-story-chapter" aria-hidden="true">01 &mdash; Origin</span>{eyebrow}'
                  '<h2>It started with<br>a simple idea.</h2>'
                  '<p>ZEYA began with a simple belief &mdash; that beautiful spaces should '
                  'feel as effortless to live in as they are to look at.</p>'
                  '<p>We wanted to create spaces that feel clean, chic and thoughtfully put '
                  'together, while making sure the solutions are practical, easy to operate '
                  'and suited to the way people actually live.</p>'
                  '<p>That simple idea became ZEYA.</p>'
                  '<p>Today, we bring together curtains, blinds and motorised window solutions '
                  'designed to enhance a space both visually and practically.</p>'
                  '<p>We take the time to understand what each space needs &mdash; whether it is '
                  'soft natural light, complete blackout, better privacy, reduced glare, heat '
                  'control or effortless motorised operation.</p></div></div>'.format(
                      image=img('intro-living-room',
                                'A calm living room framed by floor-length curtains',
                                sizes='(max-width:700px) 100vw, 50vw'),
                      eyebrow=eyebrow('How it began')))
        + section('<div class="zeya-container zeya-story-details">'
                  '<div><span class="zeya-story-chapter" aria-hidden="true">02 &mdash; Philosophy</span>{eyebrow}<h2>We believe the<br>details matter.</h2>'
                  '<p>For us, creating the right window solution is about more than choosing '
                  'a fabric or a blind. It is about getting the details right.</p></div>'
                  '<ul class="zeya-story-details__list"><li>The right fabric.</li>'
                  '<li>The right finish.</li><li>The right fall.</li>'
                  '<li>The right amount of light.</li>'
                  '<li>The right way for everything to operate.</li></ul>'
                  '<p class="zeya-story-details__close">Every choice should work together to '
                  'make the space feel considered, comfortable and easy to live in.</p>'
                  '</div>'.format(eyebrow=eyebrow('What guides us')),
                  'zeya-section--chocolate')
        + section('<div class="zeya-container zeya-section-heading zeya-story-process">'
                  '<div class="zeya-story-process__label"><span class="zeya-story-chapter" aria-hidden="true">03 &mdash; Experience</span>{eyebrow}</div>'
                  '<div class="zeya-story-copy"><h2>A clear process<br>from start to finish.</h2>'
                  '<p>We believe the experience is just as important as the finished result.</p>'
                  '<p>From the initial consultation and fabric selection to precise measuring, '
                  'specifications, quotation, production and installation, we keep the process '
                  'clear and make sure you know what to expect at every stage.</p>'
                  '<p>We bring fabric samples to your home, take accurate measurements, provide '
                  'clear quotations and ensure the installation is handled professionally.</p>'
                  '<p class="zeya-story-copy__emphasis"><strong>No unnecessary surprises. '
                  'No unclear expectations.</strong></p>'
                  '<p>Just a straightforward, transparent process, with the right information '
                  'to help you make confident decisions for your space.</p>'
                  '</div></div>'.format(eyebrow=eyebrow('The ZEYA experience')))
        + section('<div class="zeya-container zeya-story-finale">'
                  '<span class="zeya-story-chapter" aria-hidden="true">04 &mdash; Purpose</span>{eyebrow}'
                  '<h2>Beautifully dressed.<br><em>Effortlessly lived in.</em></h2>'
                  '<p>For us, ZEYA isn\'t simply about covering a window.</p>'
                  '<p>It is about creating spaces that feel calm, beautiful and easy to live '
                  'with &mdash; while making the entire experience simple, transparent and '
                  'thoughtfully managed.</p><p>That\'s where it all started.<br>And that\'s what '
                  'continues to guide us today.</p>{cta}</div>'.format(
                      eyebrow=eyebrow('Our purpose'),
                      cta=btn('Let’s talk about your space', 'contact.html', 'ivory')),
                  'zeya-section--black')
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
    from home_content import service_areas_section
    form = Path(__file__).with_name('contact-form.html').read_text(encoding='utf8')
    methods = h.contact_methods([('address', 'Studio'), ('hours', 'Hours'), ('email', 'Email')])
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
        + service_areas_section(h)
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

    # ------------------------------------------------------------ review ---
    # The page behind the link ZEYA sends clients after an installation. It
    # greets them with ZEYA's own message, then hands them to Google's review
    # form, which cannot carry a message of its own. Until a review link is
    # configured the Google button stays hidden and the contact page stands in.
    from home_content import REVIEW_MESSAGE, review_button
    review = (
        hero('contact-interior', 'Softly lit sheer curtains in a Dubai apartment',
             'Thank you for<br>choosing ZEYA.',
             eyebrow='Share your experience',
             sub=REVIEW_MESSAGE,
             actions=review_button(h)
             + '<span data-zeya-review-fallback>'
             + btn('Share your feedback', 'contact.html', 'gold') + '</span>',
             variant='product')
        + section('<div class="zeya-container">'
                  + heading('It takes a minute', 'Three quick steps.')
                  + steplist([
                      ('01', 'Open the review form',
                       'Tap &ldquo;Write a Google review&rdquo; and Google opens ZEYA&rsquo;s '
                       'review form. You may be asked to sign in to your Google account.'),
                      ('02', 'Choose your stars',
                       'Rate your experience, from the first visit to the finished '
                       'installation.'),
                      ('03', 'Add a few words',
                       'Tell others what stood out, then tap Post. Thank you &mdash; it '
                       'means a great deal to us.')])
                  + '</div>')
    )

    # --------------------------------------------------------------- faq ---
    faqs = [
        ('Do you provide free measuring and installation?',
         'Yes. ZEYA provides professional measurement and installation as part of our curtain and blind solutions.'),
        ('Can I get a quote from a photo?',
         'Yes. A photo with approximate window dimensions can help us provide a rough estimate. The final price is confirmed after measuring the window and selecting the fabric, style and hardware.'),
        ('Which is more affordable: curtains or roller blinds?',
         'It depends on the size and specification. Basic roller blinds can be a cost-effective option, while made-to-measure curtains may cost more depending on the fabric, fullness, sewing and track system.'),
        ('Are blackout curtains more expensive than sheer curtains?',
         'Not necessarily. The price depends on the fabric quality, lining, size and curtain system. Blackout lining can affect the overall cost.'),
        ('Why choose two layers of curtains?',
         'A sheer and main curtain provide greater flexibility. The sheer allows natural light and daytime privacy, while the main curtain provides additional privacy, light control and insulation.'),
        ('Are curtains and blinds soundproof?',
         'Curtains and blinds are not completely soundproof, but certain fabrics can help absorb and reduce noise. Heavier and denser fabrics generally provide better noise reduction.'),
        ('Can curtains and blinds help reduce electricity consumption?',
         'They can help reduce heat entering through windows, which may reduce the workload on your air conditioner. Actual savings depend on the window, glass, fabric, sunlight exposure and installation.'),
        ('Do blackout curtains or blinds make a room completely dark?',
         'Blackout fabric blocks light through the fabric, but light can still enter around the sides, top and bottom. Correct sizing and installation can help achieve maximum darkness.'),
        ('What is the difference between blackout and dim-out?',
         'Blackout fabrics block most light passing through the fabric, while dim-out fabrics reduce light but allow some light through. The final level of darkness also depends on gaps around the window.'),
        ('How do I clean roller blinds?',
         'Regularly remove dust with a soft cloth, microfibre duster or suitable vacuum attachment. Small marks can usually be gently wiped with a slightly damp cloth. Avoid harsh chemicals and excessive water.'),
        ('How often should curtains be cleaned?',
         'For normal residential use, we generally recommend professional cleaning approximately twice a year. More frequent cleaning may be needed in dusty or high-use environments.'),
        ('Will curtains fade in sunlight?',
         'Prolonged direct sunlight can cause fading over time. Using a sheer curtain can help reduce direct sunlight reaching the main curtain and help protect the fabric and colour.'),
        ('Can curtains help keep a room cooler?',
         'Yes. Certain heavier, lined or coated fabrics can help reduce solar heat entering through windows. However, they cannot completely prevent heat from entering.'),
        ('Can you make curtains for large or unusual windows?',
         'Yes. We can assess the window and recommend suitable fabric, tracks, hardware and operating systems for large, curved or unusually shaped windows.'),
        ('Do you offer flexible curtain tracks?',
         'Yes. We offer flexible curtain tracks that can be customised for curved, bay and uniquely shaped windows.'),
        ('Can flexible curtain tracks be motorised?',
         'Yes. Motorised options are available for selected flexible track systems, depending on the window design and track requirements.'),
        ('Can you provide double curtain tracks?',
         'Yes. Double-track systems are available for combining sheers and blackout or main curtains.'),
        ('Can I use curtains and blinds in the same room?',
         'Yes. Combining blinds and curtains can provide greater flexibility for light control, privacy and insulation, while creating a layered interior look.'),
        ('Can we use our existing curtain tracks?',
         'Yes. In many cases, we can use your existing curtain tracks, provided they are suitable and in good condition. We can assess them before installation.'),
        ('Do you offer motorised curtains and blinds?',
         'Yes. Motorised options are available for selected systems and are particularly useful for large, high or hard-to-reach windows.'),
        ('Can motorised curtains and blinds be automated?',
         'Depending on the system, they can be operated using a remote, wall switch, smartphone or compatible smart-home system. Features depend on the selected motor and control system.'),
        ('Can I see samples before ordering?',
         'Yes. We recommend viewing physical samples to check the actual colour, texture, thickness, transparency and finish before making your final selection.'),
        ('Why is professional measurement important?',
         'Accurate measurement helps ensure the correct fabric quantity, finished curtain dimensions, track or rod length, blind size, mounting position and operating clearance. It also helps identify installation limitations before ordering.'),
        ('Are curtains better than blinds?',
         'Neither is universally better. The right choice depends on light control, privacy, style, maintenance, window type and budget. We can recommend a suitable option based on your space.'),
        ('How do I choose the right curtain or blind?',
         'We consider sunlight, heat, privacy, desired darkness, window size, interior style, maintenance, operation and budget before recommending a suitable solution.'),
        ('What curtains or blinds are suitable for bedrooms?',
         'For bedrooms, we commonly recommend blackout curtains, blackout blinds or layered curtains, depending on the desired level of darkness, privacy and window type.'),
        ('What curtains or blinds are suitable for living rooms?',
         'Living rooms can benefit from sheers, layered curtains, blinds or a combination of curtains and blinds, depending on sunlight, privacy and interior design.'),
    ]

    faq = (
        hero('about-zeya-curtains',
             'Floor-length curtains filtering soft light in a calm Dubai interior',
             'Questions, answered.<br>Choices made simpler.',
             eyebrow='Curtains &amp; blinds advice',
             sub='Clear answers about measuring, materials, light control, care and motorized curtains and blinds.',
             variant='product')
        + section('<div class="zeya-container zeya-faq-layout">'
                  '<aside class="zeya-faq-intro">' + eyebrow('Frequently asked questions') +
                  '<h2>Everything you need to know.</h2>'
                  '<p>Explore the details before your consultation. If your question is not covered, we are happy to help.</p>'
                  + btn('Ask us a question', 'contact.html', 'gold') + '</aside>'
                  '<div class="zeya-faq-list">' + ''.join(
                      '<details class="zeya-faq-item"><summary><span>%02d</span><h3>%s</h3>'
                      '<i aria-hidden="true"></i></summary><div class="zeya-faq-answer"><p>%s</p></div></details>'
                      % (index, question, answer)
                      for index, (question, answer) in enumerate(faqs, 1))
                  + '</div></div>')
    )

    return {'home': home, 'about': about, 'process': process,
            'contact': contact, 'terms': terms, 'review': review, 'faq': faq, 'products': ''}
