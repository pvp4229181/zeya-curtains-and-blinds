# ZEYA verification — 2 October 2026

Read-only live-site audit. No WordPress content or settings were changed.

## Findings

1. Administrator API authentication succeeds, and the ZEYA theme is active.
2. WordPress contains no pages; no trashed pages were found. All 49 expected inner-page URLs return HTTP 404. The homepage returns HTTP 200 and renders the ZEYA hero.
3. Homepage settings remain `show_on_front=posts`, `page_on_front=0`. Create/import the 50 pages and select Home as the static homepage.
4. The WordPress package is behind the static website: the static JavaScript includes category-panel menu switching and the ARZOO office address, while the theme JavaScript lacks those updates. The live contact configuration also lacks the office address and Maps URL. The ZIP matches the local theme code, so uploading the current ZIP alone will not include these newer static changes.
5. Live WhatsApp is the test number +971 50 000 0000. Google reviews use ZEYA_GOOGLE_PLACE_ID. Phone, email, social links and form endpoint are empty; opening hours are marked as placeholders in source.
6. No Contact Form 7 or WPForms plugin is installed. The fallback form validates input but cannot send enquiries without a handler.
7. Live site title is the temporary hosting hostname; description is empty.
8. Responsive smoke testing flags homepage horizontal overflow of approximately 2–7 pixels at several widths, an About-page overflow at 1024 pixels, and small product-link tap targets. The script reports 12 affected page/width combinations. Some measurements include animated or intentionally clipped elements; investigate before treating every listed element as a defect.
9. Interaction tests report five failures. The homepage-width failure is also flagged by responsive testing. The phone checks target a removed `phone` element (current markup uses `call`); the reduced-motion hero check targets an image although the hero now uses video; the collection-menu comparison assumes older markup. Update these tests before interpreting those failures as product defects.

## Passed checks

- Corrected XML parses successfully: 50 pages, one author, all pages referencing that author.
- All explicit XML page templates exist in the ZIP; Home uses WordPress's `default` template value and the theme's front-page.php.
- ZIP PHP/CSS/JavaScript files match the local theme.
- All 50 static pages pass local link, image-alt-presence and product-count checks.
- Theme JavaScript passes syntax validation.
- All 33 live homepage theme assets sampled return HTTP 200; both hero videos return HTTP 200.
- Mobile menu opening, focus movement, Escape handling and scroll locking pass.
- Header scroll behavior, form validation, product enquiry selection, card tilt and several reduced-motion checks pass.
- Static homepage matches dist/index.html; static and theme CSS match.
- .env.wordpress is excluded from Git.

## Limits

PHP CLI is unavailable, so PHP linting was not performed. Responsive browser checks cover 13 representative static pages at six widths, not all 50 live pages. Live inner-page behavior and enquiry delivery cannot be verified while pages and a form handler are absent. This is not an exhaustive security audit.
