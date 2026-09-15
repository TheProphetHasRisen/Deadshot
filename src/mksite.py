# -*- coding: utf-8 -*-
import io, os, json as _json, hashlib as _hashlib, re as _re

HERE = os.path.dirname(os.path.abspath(__file__))
# site_data.json is stored readable (one field per line) so changes to it are
# legible in git and by eye. The page gets the compact form -- pretty-printing
# inside index.html would add ~100KB to every visitor's download for no benefit.
# json.dumps leaves "<" alone, so a team called "</script>..." closes the tag the data is
# sitting inside and blanks the whole page. Team names come from Yahoo and are whatever a
# manager typed, so this has to be escaped here, at the embed. \u003c is still valid JSON
# and parses back to the same string.
_D=_json.load(open('site_data.json'))
DATA=(_json.dumps(_D,separators=(',',':'))
      .replace('<','\\u003c').replace('\u2028','\\u2028').replace('\u2029','\\u2029'))

# ---- counts that used to be typed into the prose ---------------------------------
# "ten seasons", "twenty managers", "410 games logged" and "all 55 playoff games" were
# written out by hand in the page copy, the meta tags, the manifest and the link-preview
# cards. Every one of them starts lying the day a new season lands. They are placeholders
# now, filled in from the data at build time, so the page cannot disagree with itself.
# Spelled out, because that is how the copy already reads; digits past twenty.
_WORDS={1:'one',2:'two',3:'three',4:'four',5:'five',6:'six',7:'seven',8:'eight',9:'nine',
        10:'ten',11:'eleven',12:'twelve',13:'thirteen',14:'fourteen',15:'fifteen',
        16:'sixteen',17:'seventeen',18:'eighteen',19:'nineteen',20:'twenty'}
def _word(n): return _WORDS.get(n,str(n))
_SEA=_D['seasons']
# same sum as the masthead's fourth figure: every playoff game plus every regular-season
# game in the years whose weekly log is loaded. If that formula moves, move this with it.
_LOGGED=len(_D['games'])+sum(
    len([g for g in _D['wk'][str(y)]['games'] if g['br']=='']) for y in _D['wkYears'])
COUNTS={
 '__NSEASONS__'  : str(len(_SEA)),        '__NSEASONSW__' : _word(len(_SEA)),
 '__NSEASONSWC__': _word(len(_SEA)).capitalize(),
 '__FIRSTYEAR__' : str(_SEA[0]),          '__LASTYEAR__'  : str(_SEA[-1]),
 '__NMGRS__'     : str(len(_D['mgrs'])),  '__NMGRSW__'    : _word(len(_D['mgrs'])),
 '__NTEAMSZN__'  : str(len(_D['rows'])),  '__NLOGGED__'   : str(_LOGGED),
}
def _fill(s):
    for k,v in COUNTS.items(): s=s.replace(k,v)
    return s

# ---- the page itself lives in page/, as real .css / .js / .html files -------------
# It used to be five giant raw strings right here: ~97KB of CSS and ~284KB of JavaScript
# with no syntax highlighting, no autocomplete and nothing a linter could read. Same
# bytes, same output -- the build asserts the page is byte-identical either way -- but
# now an editor understands them and `npm run lint` can find real bugs in the JavaScript.
#
#   page/shell.html    doctype, <html>, meta tags
#   page/head.html     <title>, font links, and __CSS__
#   page/site.css      every rule for all six themes
#   page/body.html     the markup, and __DATA__
#   page/scripts.html  the <script> wrapper, and __JS__
#   page/site.js       the whole page's behaviour
#   page/sw.js         the offline worker, with __VERSION__
PAGE = os.path.join(HERE, 'page')


def _part(name):
    with io.open(os.path.join(PAGE, name), encoding='utf-8') as f:
        return f.read()


HEAD = _part('head.html').replace('__CSS__', _part('site.css'))
BODY = _part('body.html')
JS = _part('scripts.html').replace('__JS__', _part('site.js'))
SHELL_TOP = _part('shell.html')
SW = _part('sw.js')

_shell, _head, _body, _js = _fill(SHELL_TOP), _fill(HEAD), _fill(BODY), _fill(JS)
# A mistyped placeholder is silent otherwise -- it ships as a literal __NSEASONSW__ sitting
# in the middle of a sentence, and nothing else on the way to the live site would catch it.
_left = set(_re.findall(r'__[A-Z][A-Z0-9_]*__', _shell + _head + _body + _js)) - {'__DATA__'}
assert not _left, 'unfilled placeholder(s) in the page: ' + ', '.join(sorted(_left))
# the counts go in before the data does, so a team name that happens to contain a
# placeholder can never be rewritten
out = _shell + _head + '</head>\n<body>\n' + _body.replace('__DATA__', DATA) + _js + '\n</body>\n</html>\n'
open('index.html','w').write(out)
# A length is not a fingerprint: two builds of equal length produced a byte-identical
# sw.js, so the browser saw no change and every stored icon and font stayed pinned to the
# old build. A content hash changes whenever anything changes.
_blob = out.encode('utf-8')
open('sw.js','w').write(SW.replace('__VERSION__', _hashlib.sha1(_blob).hexdigest()[:12]))
print("bytes", len(_blob))
