# -*- coding: utf-8 -*-
"""Fetch the page's typefaces from Google Fonts once, and write page/fonts.css.

    python3 mkfonts.py

Not part of the build. Run it once, and again only when a typeface should be refreshed.

WHY
---
Until 25 Sep 2026 the page linked Google's font stylesheet. Browsers block first paint on
that stylesheet, so with fonts.googleapis.com slow the whole page was blank -- measured
at 4.3 s to first paint with that one response delayed 4 s -- and a first-install offline
copy had no typefaces at all, because the offline worker cannot see font requests until
the second visit. Self-hosting the same six files (same bytes Google serves) removes both:
they come from our own origin, are precached by the worker on install, and the page paints
in system faces immediately while they swap in.

WHAT IT DOES
------------
Asks Google for the css2 stylesheet exactly as Chrome would (Google serves woff2 and
per-script unicode-range only to modern user agents), keeps the `/* latin */` blocks, and
de-duplicates by file URL -- the variable families (Plex Sans, Fraunces, Big Shoulders)
repeat one URL under several weight blocks, so the weights collapse into one range.
Downloads each file into fonts/, named with Google's version segment so a refreshed font
is a new filename and the immutable cache header on /fonts/ is safe. Fetches each family's
OFL.txt: all four are SIL Open Font License 1.1, which permits bundling as long as the
licence travels with the files. Writes page/fonts.css with relative URLs (so index.html
opened off disk still finds them) and Google's unicode-range copied verbatim, so any
non-latin glyph falls back per glyph exactly as it does today.

Asserts exactly six files, each a real woff2, and fails loudly on any miss.
"""
import io, os, re, ssl, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, 'fonts')
OUT = os.path.join(HERE, 'page', 'fonts.css')

# Press Start 2P used to be in this list; nothing in page/ uses it.
CSS_URL = ('https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@700;800;900'
           '&family=Fraunces:opsz,wght@9..144,600;9..144,700;9..144,900'
           '&family=IBM+Plex+Mono:wght@400;500;600'
           '&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap')
UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36')
SLUG = {'IBM Plex Sans': 'plex-sans', 'IBM Plex Mono': 'plex-mono',
        'Fraunces': 'fraunces', 'Big Shoulders Display': 'big-shoulders-display'}
EXPECT_FILES = 6
OFL = 'https://raw.githubusercontent.com/google/fonts/main/ofl/%s/OFL.txt'


def _ctx():
    try:
        ssl.create_default_context().load_default_certs()
        c = ssl.create_default_context()
        if c.cert_store_stats()['x509_ca']:
            return c
    except Exception:
        pass
    import certifi  # python.org builds ship an empty trust store; see yahoo_api.py
    return ssl.create_default_context(cafile=certifi.where())


CTX = _ctx()


def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, context=CTX, timeout=30) as r:
        return r.read()


def main():
    css = fetch(CSS_URL).decode('utf-8')
    blocks = re.findall(r'/\* latin \*/\s*@font-face\s*\{([^}]*)\}', css)
    assert blocks, 'Google returned no latin @font-face blocks -- wrong user agent?'
    faces = {}  # url -> record
    for b in blocks:
        prop = dict((k.strip(), v.strip()) for k, v in
                    (line.split(':', 1) for line in b.strip().rstrip(';').split(';\n')))
        fam = prop['font-family'].strip("'\"")
        url = re.search(r'url\((\S+?)\)', prop['src']).group(1)
        w = int(prop['font-weight'])
        rec = faces.setdefault(url, dict(fam=fam, weights=set(), style=prop['font-style'],
                                          stretch=prop.get('font-stretch'),
                                          urange=prop['unicode-range']))
        assert rec['fam'] == fam
        rec['weights'].add(w)
    assert len(faces) == EXPECT_FILES, 'expected %d files, Google listed %d' % (EXPECT_FILES, len(faces))

    os.makedirs(FONTS, exist_ok=True)
    rules, dirs = [], set()
    for url, rec in sorted(faces.items(), key=lambda kv: (kv[1]['fam'], min(kv[1]['weights']))):
        m = re.search(r'/s/([a-z0-9]+)/(v\d+)/', url)
        gdir, ver = m.group(1), m.group(2)
        dirs.add(gdir)
        ws = sorted(rec['weights'])
        variable = len(ws) > 1
        name = '%s-%s%s-latin.woff2' % (SLUG[rec['fam']], ver, '' if variable else '-%d' % ws[0])
        data = fetch(url)
        assert data[:4] == b'wOF2' and len(data) > 5000, '%s is not a woff2 (%d bytes)' % (name, len(data))
        with open(os.path.join(FONTS, name), 'wb') as f:
            f.write(data)
        print('  %-42s %7d bytes  weights %s' % (name, len(data), ws))
        weight = '%d %d' % (ws[0], ws[-1]) if variable else str(ws[0])
        stretch = ';font-stretch:%s' % rec['stretch'] if rec['stretch'] else ''
        rules.append('@font-face{font-family:"%s";font-style:%s;font-weight:%s%s;font-display:swap;'
                     'src:url(fonts/%s) format("woff2");unicode-range:%s}'
                     % (rec['fam'], rec['style'], weight, stretch, name, rec['urange']))

    for gdir in sorted(dirs):
        txt = fetch(OFL % gdir)
        assert b'SIL OPEN FONT LICENSE' in txt.upper(), gdir
        with open(os.path.join(FONTS, 'OFL-%s.txt' % gdir), 'wb') as f:
            f.write(txt)
    print('  %d licence files' % len(dirs))

    with io.open(OUT, 'w', encoding='utf-8') as f:
        f.write('/* generated by mkfonts.py -- do not hand-edit. The six typefaces the page uses, '
                'self-hosted from fonts/. SIL Open Font License 1.1; see fonts/OFL-*.txt */\n')
        f.write('\n'.join(rules) + '\n')
    print('wrote', os.path.relpath(OUT, HERE), 'with', len(rules), 'faces')


if __name__ == '__main__':
    sys.exit(main())
