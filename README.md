# ZEYA Curtains & Blinds — website

A premium, editorial brochure site for ZEYA Curtains & Blinds (Dubai, UAE), built with
HTML5, CSS3 and vanilla JavaScript, plus a matching WordPress theme.

No React, Vue, Next.js, jQuery, Bootstrap or Tailwind. No build step is required to
*serve* the site — only to regenerate it after editing shared markup.

```
zeya/
├─ zeya-website/          ← the static site (open index.html and it works)
│  ├─ index.html  about.html  products.html  process.html  contact.html
│  ├─ assets/
│  │  ├─ images/          45 WebP files (base + -640/-1024/-1600 variants)
│  │  ├─ icons/           zeya-icons.svg (sprite), favicon.svg
│  │  └─ fonts/           see fonts/README.md for self-hosting
│  ├─ css/
│  │  ├─ style.css        design tokens, base, components, all sections
│  │  ├─ animations.css   scroll reveals, parallax, reduced-motion
│  │  └─ responsive.css   breakpoints — loaded last
│  └─ js/
│     ├─ main.js          nav, contact config, form validation
│     └─ animations.js    IntersectionObserver reveals + parallax
│
├─ zeya-theme/            ← the WordPress theme (drop into wp-content/themes/)
│  ├─ style.css  functions.php  header.php  footer.php
│  ├─ front-page.php  page-about.php  page-products.php
│  ├─ page-process.php  page-contact.php
│  ├─ index.php  page.php  404.php  screenshot.png
│  ├─ inc/icons.php       inline icon sprite
│  └─ assets/             css, js, images, icons (copied from zeya-website)
│
└─ tools/                 ← generators and tests (not deployed)
```

---

## 1. Product catalogue and supplied artwork

The static site includes three collection pages and 30 unique product detail pages.
The homepage cards, Products submenu, catalogue cards and product enquiry links are connected.
Product copy is transcribed from the supplied chart in `tools/catalog.py`.

Images were cropped from the supplied flattened PDF and product chart, then saved as WebP.
The sources are low resolution; large banners will appear soft. They are reference artwork,
not verified photographs of completed ZEYA installations.

Rebuild: `python tools/build_pages.py` and `python tools/build_theme.py`.
Validate: `python tools/check_links.py`, `node tools/check.js`, `node tools/interact.js`.
Re-extract: `python tools/extract_assets.py PATH_TO_PDF PATH_TO_PRODUCT_CHART`.
The source PDF and chart remain in Downloads. The old placeholder generator was removed.

For WordPress, create pages for the collection and product slugs to activate the corresponding
`page-*.php` templates. The static site needs no setup or build step to serve.

---

## 2. Contact details are deliberately empty

No phone number, WhatsApp number, email address or social URL has been invented.
Every contact element renders as a **plain, unlinked label** until a real value is
configured — which is exactly how the reference design shows them.

**Static site** — edit the `CONTACT` object at the top of `zeya-website/js/main.js`:

```js
var CONTACT = window.ZEYA_CONTACT || {
  address:       "Dubai, UAE",
  addressLine:   "",   // optional second line, e.g. a street address
  addressUrl:    "",   // e.g. a Google Maps link
  whatsapp:      "",   // digits only, e.g. "971500000000"
  whatsappLabel: "",   // display form, e.g. "+971 50 000 0000"
  phone:         "",   // e.g. "+971 4 000 0000"
  email:         "",   // e.g. "hello@example.com"
  instagram:     "",   // full profile URL
  facebook:      "",   // full profile URL
  formEndpoint:  ""    // POST target for the contact form
};
```

**WordPress** — *Appearance → Customize → ZEYA Contact Details*, or edit the defaults
in `zeya_contact_details()` in `functions.php`, or filter them:

```php
add_filter( 'zeya_contact_details', function ( $details ) {
    $details['phone'] = '+971 4 000 0000';
    return $details;
} );
```

Filled values become real `tel:`, `mailto:` and `https://wa.me/` links automatically.
Empty ones stay as labels and are marked `aria-disabled`.

---

## 3. The contact form does not send email yet

The form validates in the browser (required fields, email format, phone length,
message length, plus a honeypot) and is keyboard- and screen-reader-accessible. It
**does not claim to have sent anything**: with no handler configured it tells the
visitor plainly that the form is not connected and points them at the contact details.

Field names follow the Contact Form 7 / WPForms convention (`your-name`, `your-email`,
`your-phone`, `your-message`), so there are three ways to make it live:

1. **Contact Form 7 / WPForms** — the theme hands the form over to the plugin:
   ```php
   add_filter( 'zeya_contact_form_shortcode', function () {
       return '[contact-form-7 id="123" title="ZEYA enquiry"]';
   } );
   ```
   Plugin-rendered fields inherit the ZEYA styling (see §18 of `style.css`).

2. **Any endpoint** — set `formEndpoint` (Customizer or the `CONTACT` object). The form
   POSTs `FormData` there and reports success or failure honestly.

3. **Your own handler** — the markup is a plain `<form method="post">`; give it an
   `action` and it submits normally.

---

## 4. Running the static site

Open `zeya-website/index.html` directly, or serve the folder:

```bash
cd zeya-website
python -m http.server 8000     # → http://localhost:8000
```

Everything is relative — no absolute URLs anywhere — so the folder can be dropped at
any path or subdirectory.

---

## 5. Installing the WordPress theme

1. Copy `zeya-theme/` into `wp-content/themes/` and activate it.
2. Create five pages with these **exact slugs**: `about`, `products`, `process`,
   `contact`, plus any page for the home page.
   The slugs drive `page-about.php` … `page-contact.php` and the active-nav state.
3. *Settings → Reading* → "Your homepage displays: A static page" → pick the home page.
   `front-page.php` renders it.
4. *Appearance → Menus* → create a menu with those five pages and assign it to
   **Primary Navigation** (and optionally **Footer Navigation**). Without a menu the
   theme falls back to its own built-in navigation, so nothing breaks.
5. *Appearance → Customize → ZEYA Contact Details* → fill in the real details.

The page templates carry `Template Name:` headers too, so they can be assigned
manually to pages with different slugs.

**Requires WordPress 6.3+** (for `wp_enqueue_script()`'s `strategy => defer`) and PHP 7.4+.

### WordPress conventions used
`get_header()` · `get_footer()` · `wp_head()` · `wp_body_open()` · `wp_footer()` ·
`wp_enqueue_style()` · `wp_enqueue_script()` · `wp_localize_script()` ·
`get_template_directory_uri()` · `wp_nav_menu()` with fallbacks ·
`register_nav_menus()` · `add_theme_support()` · `body_class()` · Customizer settings
with `sanitize_callback` · `esc_url()` / `esc_html()` / `esc_attr()` on every dynamic
value · all CSS and JS enqueued from `functions.php`, never inlined in a template.

The reset is scoped with `:where(.zeya-body)` so it carries zero specificity and cannot
leak into the admin bar, the block editor or plugin widgets. Every custom class is
prefixed `zeya-`.

---

## 6. Design system

Tokens live at the top of `css/style.css`:

| Token | Value | Use |
|---|---|---|
| `--zeya-ivory` | `#F7F4EE` | page background |
| `--zeya-cream` | `#EFE9DF` | alternating sections, cards |
| `--zeya-beige` | `#D6C4A5` | selection, accents |
| `--zeya-gold` | `#B89458` | buttons, icons, rules |
| `--zeya-espresso` | `#211B16` | nav, footer, dark sections |
| `--zeya-charcoal` | `#292622` | image backdrops |

Type: **Cormorant Garamond** (300/400/500) for display, **Inter** (300–600) for UI.
All sizes are `clamp()`-based; desktop headings land between 52px and 76px.

Spacing, radii, shadows and easing are all tokenised — change a token, not a rule.

---

## 7. Motion

All reveals are driven by `IntersectionObserver`, never scroll handlers. Parallax uses
a single `requestAnimationFrame` loop that only runs while a parallax layer is actually
on screen. Durations sit between 400ms and 900ms.

Included: navbar transition, hero slow zoom (Ken Burns), parallax on hero/quote/CTA,
fade-up section reveals, staggered cards, line-by-line text reveal, image-mask reveal,
button hover lift, arrow slide, image zoom on hover, timeline draw-in, and the animated
mobile menu.

`prefers-reduced-motion: reduce` switches every non-essential effect off — reveals show
immediately, the hero zoom and parallax stop, and hover transforms are removed.

---

## 8. Performance and accessibility

- Responsive `srcset`/`sizes` on every image, with `width`/`height` set so nothing shifts.
- The hero is preloaded and is the only image not lazy-loaded.
- Scripts are deferred; there are no third-party libraries.
- Icons are one inline SVG sprite — no extra request, no `<use>` cross-document issues.
- Semantic `header`/`nav`/`main`/`section`/`article`/`footer`, one `h1` per page, no
  skipped heading levels, descriptive `alt` on every image, skip link, visible focus
  states, keyboard-accessible nav with a focus trap and Escape-to-close, `aria-current`
  on the active link, `role="status"` on form feedback.

---

## 9. Tools (development only, not deployed)

| Command | What it does |
|---|---|
| `python tools/build_pages.py` | Rebuild the five static pages from the shared shell |
| `python tools/build_theme.py` | Rebuild the WordPress theme from the same source |
| `node tools/shoot.js 1440 desktop index about …` | Full-page screenshots via headless Chrome |
| `node tools/check.js` | Overflow / alt / heading-order / tap-target audit at 6 widths |
| `node tools/interact.js` | Mobile menu, header scroll, form validation, reduced motion |

`tools/build_pages.py` holds the shared shell (head, header, footer band, CTA, footer)
and `tools/page_content.py` holds the page bodies, so the five pages and the five PHP
templates cannot drift apart. Edit those, then re-run both build scripts.

### Verified
`node tools/check.js` passes on all five pages at **1440 / 1200 / 1024 / 768 / 480 /
390px**: no horizontal overflow, no broken images, no missing `alt`, no heading-level
jumps, no undersized tap targets. `node tools/interact.js` passes all 23 interaction
checks.

**Not verified here:** the WordPress theme has not been run against a live WordPress
install — PHP was not available in this environment. The templates are generated
mechanically from the same markup as the static pages (which *is* verified in a
browser), and were checked for balanced tags, matching `if:`/`endif`, and that every
function called is defined. Please smoke-test it on a staging site before launch.
