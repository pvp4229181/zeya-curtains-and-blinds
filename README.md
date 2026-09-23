# ZEYA Curtains & Blinds — website

A premium, editorial brochure site for ZEYA Curtains & Blinds (Dubai, UAE), built with
HTML5, CSS3 and vanilla JavaScript, plus a matching WordPress theme.

No React, Vue, Next.js, jQuery, Bootstrap or Tailwind. No build step is required to
*serve* the site — only to regenerate it after editing shared markup.

```
zeya/
├─ zeya-website/          ← the static site (open index.html and it works)
│  ├─ index.html  about.html  products.html  process.html  contact.html
│  ├─ curtains.html  blinds.html  motorized.html  curtain-accessories.html
│  ├─ product-*.html      38 product detail pages
│  ├─ assets/
│  │  ├─ images/          136 WebP files (base + -640/-1024/-1600 variants)
│  │  ├─ icons/           zeya-icons.svg (sprite), favicon.ico + PNG icons
│  │  └─ fonts/           see fonts/README.md for self-hosting
│  ├─ css/
│  │  ├─ style.css        the four-colour palette, base, components, sections
│  │  ├─ animations.css   hero drift, scroll reveals, reduced-motion
│  │  └─ responsive.css   breakpoints — loaded last
│  └─ js/
│     └─ main.js          nav, reveals, contact config, form validation
│
├─ dist/                  ← the deployable bundle (generated — never edit by hand)
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

The homepage follows the supplied September 23 design reference: a copper-and-cream
palette, curtain-led hero, three solution cards, seven-product collection strip,
fabric feature and service band. Five new images were generated with the built-in
ImageGen tool and saved as `zeya-website/assets/images/signature-*.webp`, with
responsive variants. Exact prompts and original output paths are recorded in
`tools/design/signature-prompts.json`.

All 38 products use locally saved Blinds.com photographs in homepage product links,
collection cards, related products and detail pages. Source URLs and representative
match limitations are recorded in `tools/blindscom_sources.json`. Some photographs
do not demonstrate the exact fabric, lining, motorization or zip-screen construction.
The redesigned layout and AI-generated section imagery remain in place. These images
are references, not verified photographs of completed ZEYA installations.

The static site includes 4 collection pages and 38 unique product detail pages.
(The catalogue lists 39 entries; Motorized Curtains appears in two collections and
resolves to one page.)
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

Every page carries a floating enquiry button in the bottom-right corner. With no
WhatsApp number it is a **Book a consultation** link to the contact page (hidden on the
contact page itself). Once `whatsapp` is set, it is replaced by the WhatsApp bubble, and
the WhatsApp buttons on the home page service section and the product pages appear.

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

### Deploying

`.openai/hosting.json` serves **`dist/`**, not `zeya-website/`, so the bundle has to
exist before a deploy:

```bash
python tools/build_pages.py     # only if you edited the shell or page content
python tools/build_dist.py      # → dist/
```

`dist/` is a copy of `zeya-website/` containing only the files the site actually
references — every page, plus each asset reachable from an `href`/`src`/`srcset` or a
`url()` in a loaded stylesheet. The build prints everything it left out, so a dropped
asset shows up instead of vanishing quietly. It rewrites nothing: the site is already
fully relative, so `dist/` works at any path, exactly like the source folder.

It is deliberately **not** in `.gitignore` — commit it, so a deploy from a clean
checkout has something to serve. Never edit it by hand — `build_dist.py` deletes and rewrites the whole folder.
Current bundle: 38 pages, 121 files, ~12.3 MB.

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

## 6. Design system — "Classic Luxury"

The palette is **four colours**. Everything else in `css/style.css` is a tint or a
shade of one of them, named so it is obvious where it came from.

| Token | Value | Use |
|---|---|---|
| `--zeya-black` | `#1A1A1A` | display type, the CTA band, image backdrops |
| `--zeya-chocolate` | `#432C2A` | alternating dark sections |
| `--zeya-gold` | `#D0A099` | rose gold — primary buttons, rules, accents on dark |
| `--zeya-cream` | `#EDE6DA` | page background |

Derived, in the same file:

| Token | Value | Derived from |
|---|---|---|
| `--zeya-cream-lift` | `#F6F1EE` | cream lightened — cards, raised surfaces |
| `--zeya-cream-line` | `#DCCFCA` | cream darkened — hairlines and borders |
| `--zeya-gold-ink` | `#8A4A45` | rose gold darkened — used as *text* on cream |
| `--zeya-gold-soft` | `#E7C4BD` | rose gold lightened — text on the dark bands |
| `--zeya-espresso` | `#261A19` | chocolate darkened — the footer |
| `--zeya-body` | `#463C3A` | black warmed toward cocoa rose — body copy |
| `--zeya-muted` | `#6B5D5A` | body lightened — captions and meta |

Raw `--zeya-gold` is too light to sit on cream as small text (1.9:1), which is what
`--zeya-gold-ink` is for. **Every text/background pair in the system meets WCAG AA**;
the lowest is muted on cream at 5.07:1.

Type: **Cormorant Garamond** for display, **Inter** for UI. All sizes are `clamp()`-based;
hero titles run to 118px and section headings to 62px.

### The hero

Every page — home, about, the four collections, process, contact and all 38 product
pages — opens on the same component, `build_pages.hero()`: a full-bleed photograph, a
two-stop scrim so display type keeps its contrast whatever the image does, centred
Cormorant title, and an optional eyebrow, sub-line, buttons and breadcrumb bar. Three
sizes: `--tall` (home), default (editorial and collections), `--product`.

The header rides transparent over it and swaps to the solid cream bar once the hero has
scrolled away — on every page, not just the home page.

Light panels (`.zeya-product`, `.zeya-formcard`, `.zeya-specs`, `.zeya-methods`) declare
their own colours, so dropping a product grid into a `--chocolate` band cannot wash the
card text out.

Base element rules are wrapped in `:where()` so they carry **zero specificity** and any
component colour wins without `!important`.

---

## 7. Motion — 3D and scroll

There is no `js/animations.js` and no animation library. Motion lives in
`css/animations.css` plus the `motion()` module at the foot of `js/main.js`, and it is
built on one rule: **JS writes custom properties, CSS composes the transform.** Because
every animated element builds its `transform` out of variables, two systems can drive the
same node without overwriting each other — the hover lift and the pointer tilt share one
transform, and so do the scroll drift and the hover zoom.

| System | JS writes | What it does |
|---|---|---|
| 3D reveals | `.is-revealed` | Sections rise, un-rotate on X and settle from `scale(.972)` |
| Depth reveals | `.zeya-reveal--depth` | Images arrive from `-90px` in Z, so they settle *into* the page |
| Staggered grids | `.is-revealed` | Card rows arrive one by one, each from `-60px` in Z |
| Pointer tilt | `--zeya-rx` `--zeya-ry` `--zeya-mx` `--zeya-my` | Cards rotate up to 5.5° toward the cursor, copy lifts 30px in Z, a gold specular tracks the pointer |
| Hero parallax | `--zeya-p` (0→1 over the hero) | Photograph sinks 12% and grows 14% while the title lifts 70px and fades |
| Image drift | `--zeya-shift` (−1→1) | Editorial images — split sections, product detail, contact, the closing CTA — drift against the scroll inside their frame |
| Scroll progress | `--zeya-progress` | A gold rule fills along the bottom edge of the header |
| Service marquee | — (pure CSS) | The service line scrolls continuously, pausing on hover or focus |

Also: the header's transparent→solid transition, the hero's 16s entry drift (Ken Burns),
button hover lift, arrow slide, and the animated mobile menu.

### The marquee

The service line under the hero is the one effect with no JavaScript at all. The track
holds **four identical runs** and travels **exactly half its own width**, so run 3 lands
where run 1 began and the loop never shows a seam. Four runs keeps the track wider than
any realistic viewport (3824px at 1440px wide), so the tail can never scroll into view.
Only the first run is exposed to assistive tech — the repeats carry `aria-hidden`. The
strip clips its own overflow, so the over-wide track cannot widen the page. It pauses on
hover and on `:focus-within`, and under reduced motion it stands still and lays a single
run out across the width, the way a static service line would read.

### How it stays cheap

One `rAF` loop serves every scroll-driven effect, and it exits early on any frame where
`pageYOffset` has not changed. Editorial frames are only written to while an
`IntersectionObserver` says they are on screen. Pointer tilt coalesces to at most one
write per frame and reads the card's box once on `pointerenter` rather than per move.
`will-change` is set on the hero only while the hero is still in view. Nothing animates a
property that triggers layout — transforms and opacity only.

### What is deliberately off

Tilt is gated behind `(hover: hover) and (pointer: fine)`, so touch devices never get it —
a finger has no hover state, and tilting under a fingertip just hides the card. The card's
Z-depth applies on hover only, so a card at rest is flat and a lifted layer can never push
past its own edges.

`prefers-reduced-motion: reduce` switches the whole thing off: `motion()` returns before
installing tilt or the scroll loop, the progress rule is never injected, reveals are marked
revealed immediately, the hero drift and parallax stop, and all transitions collapse to
0.01ms. The hero scrim is deliberately left out of the parallax — it is what keeps the
title legible, so it stays at full strength at every scroll position.

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
| `python tools/build_dist.py` | Rebuild `dist/`, the bundle the host serves |
| `node tools/shoot.js 1440 desktop index about …` | Full-page screenshots via headless Chrome |
| `node tools/check.js` | Overflow / alt / heading-order / tap-target audit at 6 widths |
| `node tools/interact.js` | Mobile menu, header scroll, form validation, reduced motion |

`tools/build_pages.py` holds the shared shell (head, header, footer band, CTA, footer)
and `tools/page_content.py` holds the page bodies, so the five pages and the five PHP
templates cannot drift apart. Edit those, then re-run both build scripts.

### Verified
`node tools/check.js` passes at **1440 / 1200 / 1024 / 768 / 480 / 390px**: no
horizontal overflow, no broken images, no missing `alt`, no heading-level jumps, no
undersized tap targets. `node tools/interact.js` passes all 50 interaction checks
(mobile menu and focus trap, header scroll state, contact-form validation, product
navigation, the 3D/scroll motion system, and the reduced-motion fallback). `python tools/check_links.py` resolves every local
`href`/`src` across all 47 pages. Every text/background pair in the palette meets
WCAG AA.

**Not verified here:** the WordPress theme has not been run against a live WordPress
install — PHP was not available in this environment. The templates are generated
mechanically from the same markup as the static pages (which *is* verified in a
browser), and were checked for balanced tags, matching `if:`/`endif`, and that every
function called is defined. Please smoke-test it on a staging site before launch.
