"""Publish ZEYA page records using local WordPress Application Password credentials."""
import base64
import json
from pathlib import Path
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def main():
    config = {}
    for line in (ROOT / '.env.wordpress').read_text(encoding='utf-8-sig').splitlines():
        if '=' in line and not line.lstrip().startswith('#'):
            key, value = line.split('=', 1)
            config[key.strip()] = value.strip().strip('\"').strip("'")
    base = config['WP_SITE_URL'].rstrip('/')
    auth = base64.b64encode((config['WP_USERNAME'] + ':' + config['WP_APPLICATION_PASSWORD']).encode()).decode()

    def api(route, payload=None):
        request = urllib.request.Request(
            base + '/wp-json/wp/v2/' + route,
            data=json.dumps(payload).encode() if payload is not None else None,
            headers={'Authorization': 'Basic ' + auth, 'Content-Type': 'application/json'},
        )
        try:
            with urllib.request.urlopen(request, timeout=45) as response:
                return json.load(response)
        except urllib.error.HTTPError as error:
            raise RuntimeError(f'WordPress API {route}: HTTP {error.code}: {error.read().decode()[:400]}') from None

    pages = api('pages?per_page=100&context=edit')
    settings = api('settings')
    backup = ROOT / 'wordpress-deployment' / 'wordpress-before-reupload.json'
    if not backup.exists():
        backup.write_text(json.dumps({'pages': pages, 'settings': settings}, indent=2), encoding='utf-8')
    user = api('users/me')
    ns = {'wp': 'http://wordpress.org/export/1.2/'}
    items = ET.parse(ROOT / 'wordpress-deployment' / 'zeya-pages.xml').findall('./channel/item')
    assert len(items) == 50
    existing = {page['slug']: page for page in pages}
    imported = {}
    for index, item in enumerate(items, 1):
        slug = item.findtext('wp:post_name', namespaces=ns)
        template = item.findtext('wp:postmeta/wp:meta_value', namespaces=ns)
        payload = {
            'title': 'Home' if slug == 'home' else item.findtext('title'),
            'slug': slug, 'status': 'publish', 'author': user['id'],
            'template': '' if template == 'default' else template,
            'menu_order': int(item.findtext('wp:menu_order', namespaces=ns)),
            'comment_status': 'closed', 'ping_status': 'closed',
        }
        route = 'pages/' + str(existing[slug]['id']) if slug in existing else 'pages'
        page = api(route, payload)
        assert page['slug'] == slug and page['status'] == 'publish', slug
        imported[slug] = page['id']
        print(f'{index}/50 published: {slug}', flush=True)

    api('settings', {
        'show_on_front': 'page', 'page_on_front': imported['home'],
        'title': 'ZEYA Curtains & Blinds',
        'description': 'Bespoke and motorized curtains and blinds in Dubai, UAE.',
    })
    live = {page['slug']: page for page in api('pages?per_page=100&context=edit')}
    assert all(slug in live and live[slug]['status'] == 'publish' for slug in imported)
    verified_settings = api('settings')
    assert verified_settings['show_on_front'] == 'page'
    assert verified_settings['page_on_front'] == imported['home']
    print('Verified all 50 page records and static homepage settings.')


if __name__ == '__main__':
    main()
