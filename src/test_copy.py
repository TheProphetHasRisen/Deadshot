# -*- coding: utf-8 -*-
"""House rules for the words on the page. No browser needed.

    python3 test_copy.py

RULE 1 -- NO EM DASHES IN THE WRITING
-------------------------------------
Brian asked for copy that is "cleaner, more professional and no em dash" and had every one
removed in September 2026. By 12 October about 85 had crept back, nearly all of them in
copy written afterwards (the League rules card, the Power Index explainer, the Wrapped
slides, the link-preview text). Nothing was checking, so nothing noticed.

An em dash standing alone as the "no value" mark in a table cell is not writing and is
allowed: that is the `'—'` in f(), pct() and friends. What fails is one used inside a
sentence, a heading, a label or a tooltip -- anything with a word or a space next to it.
Rewrite with a full stop, a colon, a comma, brackets or a middle dot.

Comments are skipped: they are notes to the next person, not words a reader sees.
"""
import io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
FILES = ['page/body.html', 'page/site.js', 'page/shell.html', 'page/head.html',
         'mkog.js', 'manifest.webmanifest']

# what may sit immediately either side of a lone placeholder dash
# the '/' pair lets through the one regex that decodes entities for the share cards
OPEN = set('\'"`>(:?,=[/')
CLOSE = set('\'"`<);,:]/')


def uncommented(text):
    """Blank out /* */ , <!-- --> and whole-line // comments, keeping line numbers."""
    def blank(m):
        return re.sub(r'[^\n]', ' ', m.group(0))
    text = re.sub(r'/\*.*?\*/', blank, text, flags=re.S)
    text = re.sub(r'<!--.*?-->', blank, text, flags=re.S)
    return '\n'.join('' if l.lstrip().startswith('//') else l for l in text.split('\n'))


def em_dashes(path):
    with io.open(os.path.join(HERE, path), encoding='utf-8') as f:
        text = uncommented(f.read())
    out = []
    for n, line in enumerate(text.split('\n'), 1):
        for m in re.finditer(u'—|&mdash;|&#8212;|&#x2014;', line):
            before, after = line[max(0, m.start() - 1):m.start()], line[m.end():m.end() + 1]
            if before in OPEN and after in CLOSE:
                continue                      # a lone placeholder, not writing
            out.append((path, n, line[max(0, m.start() - 45):m.end() + 45].strip()))
    return out


def main():
    bad = []
    for p in FILES:
        if os.path.exists(os.path.join(HERE, p)):
            bad += em_dashes(p)
    if bad:
        print("%d em dash(es) in the writing. Brian does not want them; rewrite with a full\n"
              "stop, a colon, a comma, brackets or a middle dot.\n" % len(bad))
        for path, n, ctx in bad[:40]:
            print("  %s:%d   ...%s..." % (path, n, ctx))
        return 1
    print("OK - no em dashes in the writing (%d files checked)" % len(FILES))
    return 0


if __name__ == '__main__':
    sys.exit(main())
