# Fonts

The site loads **Cormorant Garamond** (display) and **Inter** (UI) from Google Fonts,
with `preconnect` hints and `display=swap`:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500&family=Inter:wght@300;400;500;600&display=swap">
```

In WordPress the same stylesheet is registered as the `zeya-fonts` handle in
`functions.php`.

## Self-hosting (recommended for production)

Self-hosting removes a third-party request, improves the largest-contentful-paint
path, and is the safer option for GDPR/PDPL compliance.

1. Download the two families (e.g. with `google-webfonts-helper`) as **woff2**:
   - Cormorant Garamond — 300, 400, 500 (latin, latin-ext)
   - Inter — 300, 400, 500, 600 (latin, latin-ext)
2. Put the `.woff2` files in this folder.
3. Replace the Google Fonts `<link>` with a local `@font-face` block, e.g.:

```css
@font-face {
  font-family: "Cormorant Garamond";
  font-style: normal;
  font-weight: 300 500;          /* variable, or one block per weight */
  font-display: swap;
  src: url("../assets/fonts/cormorant-garamond-latin.woff2") format("woff2");
}

@font-face {
  font-family: "Inter";
  font-style: normal;
  font-weight: 300 600;
  font-display: swap;
  src: url("../assets/fonts/inter-latin.woff2") format("woff2");
}
```

4. Preload the two files actually used above the fold:

```html
<link rel="preload" as="font" type="font/woff2" crossorigin
      href="assets/fonts/cormorant-garamond-latin.woff2">
```

5. In WordPress, drop the `zeya-fonts` enqueue from `functions.php` — the `@font-face`
   rules travel with `assets/css/style.css`, and paths stay relative so they resolve
   from the theme directory without change.

No token changes are needed: the stacks are defined once as `--zeya-serif` and
`--zeya-sans` in `css/style.css`, and both already fall back to Georgia and the system
UI stack respectively.
