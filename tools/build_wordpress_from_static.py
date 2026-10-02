"""Package the current static website as the ZEYA WordPress theme."""
from pathlib import Path
import re
import zipfile

import build_theme

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'zeya-website'
THEME = ROOT / 'zeya-theme'


def convert(html):
    html = build_theme.to_php(html)
    return re.sub(
        r'assets/([\w/.-]+)',
        lambda match: "<?php echo esc_url( zeya_asset( '%s' ) ); ?>" % match.group(1),
        html,
    )


def main():
    package = ROOT / 'wordpress-deployment' / 'zeya-theme.zip'
    # Keep the installed-package source available for rollback.
    backup = package.with_name('zeya-theme-before-reupload.zip')
    if package.exists() and not backup.exists():
        backup.write_bytes(package.read_bytes())

    build_theme.copy_assets()
    home = (SITE / 'index.html').read_text(encoding='utf-8')
    for page in SITE.glob('*.html'):
        html = page.read_text(encoding='utf-8')
        assert html.count('<main id="zeya-main">') == 1, page.name
        body = html.split('<main id="zeya-main">', 1)[1].split('</main>', 1)[0]
        slug = 'home' if page.stem == 'index' else page.stem
        if slug == 'contact':
            body = build_theme.contact_form_wrapper(body)
        filename = 'front-page.php' if slug == 'home' else 'page-' + slug + '.php'
        existing = (THEME / filename).read_text(encoding='utf-8')
        prefix = existing.split('?>', 1)[0] + '?>\n'
        (THEME / filename).write_text(prefix + convert(body) + '\n<?php get_footer(); ?>\n', encoding='utf-8')

    header = (THEME / 'header.php').read_text(encoding='utf-8')
    header = header.split('<div class="zeya-topbar"', 1)[0]
    header = re.sub(r"<\?php \$zeya_images = zeya_asset\( 'images/' \); \?>\s*", '', header)
    navigation = home[home.index('<div class="zeya-topbar"'):home.index('<main id="zeya-main">')]
    header += "<?php $zeya_images = zeya_asset( 'images/' ); ?>\n" + convert(navigation) + '<main id="zeya-main">\n'
    assert 'zeya-menu-category' in header
    (THEME / 'header.php').write_text(header, encoding='utf-8')

    footer = home.split('</main>', 1)[1].split('<script src=', 1)[0]
    footer = re.sub(r'</body>\s*</html>\s*$', '', footer)
    footer = "<?php\nif (!defined('ABSPATH')) { exit; }\n$zeya_images = zeya_asset('images/');\n?>\n</main>\n" + convert(footer) + '\n<?php wp_footer(); ?>\n</body>\n</html>\n'
    (THEME / 'footer.php').write_text(footer, encoding='utf-8')

    assert 'zeya-collection-products' not in (THEME / 'front-page.php').read_text(encoding='utf-8')
    assert 'Select your area to enquire' in (THEME / 'front-page.php').read_text(encoding='utf-8')
    assert 'Maximum light control, privacy and comfort.' in (THEME / 'page-curtains.php').read_text(encoding='utf-8')
    with zipfile.ZipFile(package, 'w', zipfile.ZIP_DEFLATED) as archive:
        for path in THEME.rglob('*'):
            if path.is_file():
                archive.write(path, path.relative_to(ROOT).as_posix())
    print('Updated theme and packaged:', package)


if __name__ == '__main__':
    main()
