# -*- coding: utf-8 -*-
"""Shared machinery for the visual styles.

A style is a subclass of `Style`. The base class holds the slide templates (vertical video,
wide video, YouTube thumbnail, Pinterest pin) written in terms of small overridable parts
(eyebrow, h1, title, body, number, fix box, example pair, job-title card, chips, progress,
CV illustration, background, frame around the main content). The defaults draw the original
blue JobNow look; each style overrides the parts, the CSS and the metrics it needs.

Sizes inside a fit box are written with fx(n) = calc(n px * var(--f)); after the fonts load,
the renderer shrinks --f until the content fits its box, so a long text never overflows.
"""
import html, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # repo root
FONT_DIR = os.path.join(ROOT, 'tools', 'fonts')

FORMATS = {
    'carousel': (1080, 1350),
    'pin': (1000, 1500),
    'vertical': (1080, 1920),
    'wide': (1920, 1080),
    'thumb': (1280, 720),
}
SCALE = {'carousel': 1.0, 'pin': 0.94, 'vertical': 1.06, 'wide': 1.0, 'thumb': 0.72}

BLUE, LIME, INK, LAV, NAVY = '#2b44f0', '#d4f53c', '#111318', '#cdd5ff', '#151b36'
SANS = "'Bricolage Grotesque', system-ui, sans-serif"
MONO = "'JetBrains Mono', ui-monospace, monospace"


def e(s):
    """Escape for HTML; long file names like CV_Prenom_Nom.pdf may break after _ and /."""
    return html.escape(str(s), quote=False).replace('_', '_\u200b').replace('/', '/\u200b')


def rich(s):
    """Escape, then [[...]] -> highlight span, **...** -> bold, keep hyphenated words whole, \\n -> <br>."""
    out = e(s)
    # French spacing: no line break before ? ! : ; » or after «
    out = re.sub(r' ([?!:;»])', ' \\1', out).replace('« ', '« ')
    out = re.sub(r'\[\[(.+?)\]\]', r'<span class="hl">\1</span>', out)
    out = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', out)
    out = re.sub(r"([\wÀ-ÿ']+(?:-[\wÀ-ÿ']+)+)", r'<span class="nw">\1</span>', out)
    return out.replace('\n', '<br>')


def plain(s):
    """Text without the [[ ]] / ** markers."""
    return re.sub(r'\*\*|\[\[|\]\]', '', s)


def fx(n):
    """A length that shrinks with the fit factor of the enclosing fit box."""
    return f'calc({n}px * var(--f, 1))'


def card_fs(text, size, ref=24):
    """Font size for a one-line job-title field: shrink long titles so they stay inside the field."""
    n = len(text)
    return size if n <= ref else max(round(size * .6), round(size * ref / n))


def vis(on):
    return '' if on else 'opacity:0;'


def font_face(family, file, weight='400', style='normal'):
    fmt = 'woff2-variations' if ' ' in str(weight) else 'woff2'
    return (f"@font-face{{font-family:'{family}';src:url('file://{FONT_DIR}/{file}') format('{fmt}');"
            f"font-weight:{weight};font-style:{style};font-display:block}}")


FONT_BRICOLAGE = font_face('Bricolage Grotesque', 'BricolageGrotesque.woff2', '200 800')
FONT_JETBRAINS = font_face('JetBrains Mono', 'JetBrainsMono.woff2', '100 800')

BASE_CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:%(W)spx;height:%(H)spx;overflow:hidden}
body{position:relative;-webkit-font-smoothing:antialiased;text-rendering:geometricPrecision}
.nw{white-space:nowrap}
.abs{position:absolute}
.fitbox{position:absolute;display:flex;flex-direction:column}
.fitbox>.fitin{position:relative;width:100%%}
"""

# ---------------------------------------------------------------------------------- svg bits
NOISE = ("url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='{s}' height='{s}'>"
         "<filter id='n'><feTurbulence type='fractalNoise' baseFrequency='{f}' numOctaves='{o}' seed='{seed}' stitchTiles='stitch'/>"
         "<feColorMatrix values='0 0 0 0 {r}  0 0 0 0 {g}  0 0 0 0 {b}  0 0 0 {a} 0'/></filter>"
         "<rect width='100%' height='100%' filter='url(%23n)'/></svg>\")")


def noise(size=320, freq=0.85, octaves=3, alpha=0.5, rgb=(0, 0, 0), seed=3):
    """CSS background-image of a tiling grain texture."""
    r, g, b = (c / 255 for c in rgb)
    return NOISE.format(s=size, f=freq, o=octaves, a=alpha, r=r, g=g, b=b, seed=seed)


def hexa(h, a):
    """#rrggbb + alpha -> rgba()."""
    h = h.lstrip('#')
    return f'rgba({int(h[0:2], 16)},{int(h[2:4], 16)},{int(h[4:6], 16)},{a})'


def mix(h1, h2, t):
    """Blend two #rrggbb colours, t=0 -> h1, t=1 -> h2."""
    a = [int(h1.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4)]
    b = [int(h2.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4)]
    return '#' + ''.join(f'{round(x + (y - x) * t):02x}' for x, y in zip(a, b))


def logo_svg(size, doc='#fff', bar=BLUE, dot=LIME, cut=True):
    """The JobNow mark (document + bars + dot) at height `size`."""
    w = size * 125 / 130
    mask = ('<defs><mask id="jn-cut" maskUnits="userSpaceOnUse" x="-10" y="-10" width="150" height="150">'
            '<rect x="-10" y="-10" width="150" height="150" fill="#fff"/><circle cx="104.5" cy="104.5" r="30" fill="#000"/></mask></defs>') if cut else ''
    m = ' mask="url(#jn-cut)"' if cut else ''
    return (f'<svg width="{w:.0f}" height="{size}" viewBox="0 0 125 130" style="display:block;overflow:visible;flex:none" aria-hidden="true">{mask}'
            f'<rect x="0" y="0" width="110" height="130" rx="18" fill="{doc}"{m}/>'
            f'<rect x="25" y="35" width="60" height="10" rx="5" fill="{bar}"/><rect x="25" y="60" width="60" height="10" rx="5" fill="{bar}"/>'
            f'<rect x="25" y="85" width="39" height="10" rx="5" fill="{bar}"/><circle cx="104.5" cy="104.5" r="20" fill="{dot}"/></svg>')


def bar(x, y, w, h, color, r=None):
    r = h / 2 if r is None else r
    return f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{color};border-radius:{r}px"></div>'


def cv_lines(kind, W, H, c):
    """Placeholder content of a CV page, as bars. c: dict(head, accent, text, side, sidetext, band, bandtext)."""
    t = c['text']
    if kind == 'side':          # dark sidebar on the left
        sw = round(W * 0.36)
        out = bar(0, 0, sw, H, c['side'], 0)
        out += f'<div style="position:absolute;left:{sw * .18:.0f}px;top:{H * .07:.0f}px;width:{sw * .38:.0f}px;height:{sw * .38:.0f}px;border-radius:50%;background:{c["sidetext"]};opacity:.55"></div>'
        for j, ww in enumerate((.72, .55, .63, .47)):
            out += bar(round(sw * .16), round(H * (.24 + .045 * j)), round(sw * ww), max(5, round(H * .02)), c['sidetext'])
        x0 = sw + round(W * .06)
        out += bar(x0, round(H * .07), round(W * .38), round(H * .034), c['head'], 3)
        out += bar(x0, round(H * .13), round(W * .22), round(H * .017), c['accent'])
        for j, ww in enumerate((.5, .44, .52, .4, .48, .36)):
            out += bar(x0, round(H * (.21 + .055 * j)), round(W * ww), round(H * .017), t)
        return out
    if kind == 'center':        # centred name, rule, sections
        out = bar(round(W * .22), round(H * .06), round(W * .56), round(H * .034), c['head'], 3)
        out += bar(round(W * .37), round(H * .115), round(W * .26), round(H * .017), c['accent'])
        out += bar(round(W * .06), round(H * .16), round(W * .88), 2, c['head'], 0)
        y = .2
        for sec in ((.74, .7, .62), (.78, .71, .66, .6), (.7, .64)):
            out += bar(round(W * .06), round(H * y), round(W * .3), round(H * .017), c['accent'])
            y += .036
            for ww in sec:
                out += bar(round(W * .06), round(H * y), round(W * ww), round(H * .016), t)
                y += .034
            y += .03
        return out
    # 'band': coloured header band
    out = bar(0, 0, W, round(H * .215), c['band'], 0)
    out += bar(round(W * .067), round(H * .08), round(W * .65), round(H * .027), c['bandtext'])
    out += bar(round(W * .067), round(H * .134), round(W * .41), round(H * .016), c['bandtext'], None)
    y = .27
    for sec in ((.86, .81, .84), (.85, .65)):
        out += bar(round(W * .067), round(H * y), round(W * .31), round(H * .016), c['accent'])
        y += .038
        for ww in sec:
            out += bar(round(W * .067), round(H * y), round(W * ww), round(H * .016), t)
            y += .035
        y += .035
    return out


class Style:
    key = 'bleu'
    palettes = [{}]
    label_case = 'upper'          # 'upper' keeps tags as written (À FAIRE), 'sentence' -> À faire
    trans_item = 'slideleft'      # transition between items / sections in videos
    trans_reveal = 'fade'         # transition between reveal steps of the same slide

    def __init__(self, pal=0, date=None):
        self.pi = pal % len(self.palettes)
        self.p = self.palettes[self.pi]
        self.date = date

    # ------------------------------------------------------------------ page
    def fonts(self):
        return FONT_BRICOLAGE + FONT_JETBRAINS

    def css(self, W, H, fmt, k):
        return ''

    def bg(self, fmt, tpl, ctx):
        return '<div class="bg"></div>'

    def page(self, fmt, tpl, inner, ctx=None):
        W, H = FORMATS[fmt]
        k = SCALE[fmt]
        return (f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><style>{self.fonts()}'
                f'{BASE_CSS % {"W": W, "H": H}}{self.css(W, H, fmt, k)}</style></head>'
                f'<body class="st-{self.key} fmt-{fmt} tpl-{tpl}">{self.bg(fmt, tpl, ctx or {})}{inner}</body></html>')

    def fitbox(self, x, y, w, h, inner, align='center', cls='', extra=''):
        jc = 'safe center' if align == 'center' else ('flex-end' if align == 'end' else 'flex-start')
        return (f'<div class="fitbox {cls}" data-fit style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
                f'justify-content:{jc};{extra}"><div class="fitin">{inner}</div></div>')

    def frame(self, fmt, tpl, box, inner, ctx, align='center'):
        """Main content area. box = (x, y, w, h). Styles wrap it (window, sheet of paper...)."""
        return self.fitbox(*box, inner, align)

    def lab(self, s):
        return s[:1].upper() + s[1:].lower() if self.label_case == 'sentence' else s

    # ------------------------------------------------------------------ parts
    def logo_colors(self):
        return ('#fff', BLUE, LIME)

    def logo(self, size):
        return logo_svg(size, *self.logo_colors())

    def wordmark_css(self):
        return 'color:#fff'

    def brand(self, x, y, size=48, fs=None, right=False):
        fs = fs or round(size * .82)
        pos = f'right:{x}px' if right else f'left:{x}px'
        return (f'<div class="brand abs" style="{pos};top:{y}px;display:flex;align-items:center;gap:{round(size * .27)}px">'
                f'{self.logo(size)}<div class="wm" style="font-family:{SANS};font-weight:800;font-size:{fs}px;'
                f'letter-spacing:-.04em;line-height:1;{self.wordmark_css()}">JobNow</div></div>')

    def lockup(self, size, fs, extra=''):
        """Big logo + wordmark for outros (inside a fit box)."""
        return (f'<div style="display:flex;align-items:center;gap:{fx(round(size * .2))};{extra}">{self.logo(size)}'
                f'<div class="wm" style="font-family:{SANS};font-weight:800;font-size:{fx(fs)};letter-spacing:-.045em;line-height:1;'
                f'{self.wordmark_css()}">JobNow</div></div>')

    def eyebrow(self, s, fs, extra=''):
        return f'<div class="eyebrow" style="font-size:{fs};{extra}">{e(s)}</div>'

    def h1(self, s, fs, extra=''):
        return f'<div class="h1 fw" style="font-size:{fs};{extra}">{rich(s)}</div>'

    def title(self, s, fs, extra=''):
        return f'<div class="title fw" style="font-size:{fs};{extra}">{rich(s)}</div>'

    def body(self, s, fs, extra=''):
        return f'<div class="body" style="font-size:{fs};{extra}">{rich(s)}</div>'

    def num(self, it, i, n, fs, extra=''):
        return f'<div class="num" style="font-size:{fs};{extra}">{e(it["n"])}</div>'

    def item_head(self, it, i, n, fmt, S):
        """Number + title of an item. S = sizes dict for the format."""
        return (self.num(it, i, n, fx(S['num'])) +
                self.title(it['title'], fx(S['title_long'] if len(it['title']) > 24 else S['title']), f'margin-top:{fx(S["gap_num"])}'))

    def kicker(self, s, fs, extra=''):
        return f'<div class="kicker" style="font-size:{fs};{extra}">{e(self.lab(s))}</div>'

    def fix(self, lab, txt, fs, labfs, pad, extra=''):
        return (f'<div class="fix" style="padding:{pad};{extra}"><div class="lab" style="font-size:{labfs}">{e(self.lab(lab))}</div>'
                f'<div class="txt" style="font-size:{fs};margin-top:{fx(14)}">{rich(txt)}</div></div>')

    def example(self, ex, k, width, extra=''):
        fs = fx(round(34 * k))
        pad = f'{fx(round(22 * k))} {fx(round(26 * k))}'
        return (f'<div class="pair" style="display:flex;flex-direction:column;gap:{fx(round(14 * k))};width:{width};{extra}">'
                f'<div class="ex bad" style="padding:{pad};gap:{fx(round(18 * k))}"><span class="tag" style="font-size:{fx(round(22 * k))};padding:{fx(round(8 * k))} {fx(round(14 * k))}">{e(self.lab(ex.get("badtag", "NON")))}</span>'
                f'<span class="v" style="font-size:{fs}">{e(ex["bad"])}</span></div>'
                f'<div class="ex good" style="padding:{pad};gap:{fx(round(18 * k))}"><span class="tag" style="font-size:{fx(round(22 * k))};padding:{fx(round(8 * k))} {fx(round(14 * k))}">{e(self.lab(ex.get("goodtag", "OUI")))}</span>'
                f'<span class="v" style="font-size:{fs}">{e(ex["good"])}</span></div></div>')

    def card(self, text, s, rot=-3, extra=''):
        """Job-title input card as a block (height reserved in the flow)."""
        h = round(168 * s + 60)
        return (f'<div style="position:relative;height:{fx(h)};{extra}"><div style="position:absolute;left:0;top:{fx(30)};width:445px;height:168px;'
                f'transform-origin:0 0;transform:rotate({rot}deg) scale(calc({s} * var(--f, 1)))">{self.card_inner(text)}</div></div>')

    def card_inner(self, text):
        return (f'<div style="position:absolute;inset:0;padding:28px 26px 0;background:#fff;border-radius:28px;'
                f'box-shadow:0 26px 50px rgba(9,17,92,.42),0 4px 10px rgba(9,17,92,.18)">'
                f'<div style="font-family:{SANS};font-weight:600;font-size:23px;line-height:1;color:#464a55">Titre de poste</div>'
                f'<div style="margin-top:14px;height:70px;border:2.5px solid {BLUE};border-radius:13px;box-shadow:0 0 0 6px #e2e6fd;'
                f'display:flex;align-items:center;padding-left:18px;font-family:{MONO};font-weight:500;font-size:{card_fs(text, 22, 27)}px;color:{INK};white-space:nowrap">'
                f'{e(text)}<span style="display:inline-block;width:3px;height:30px;margin-left:3px;background:{BLUE};border-radius:1px"></span></div></div>')

    def chips(self, chips, fs, pad, gap, extra=''):
        cs = ''.join(f'<span class="chip" style="font-size:{fs};padding:{pad}">{e(c)}</span>' for c in chips)
        return f'<div class="chips" style="display:flex;flex-wrap:wrap;gap:{gap};{extra}">{cs}</div>'

    def progress(self, i, n, x, y, w, fmt, right=False):
        g = 10 if fmt != 'wide' else 10
        bw = (w - g * (n - 1)) / n
        bars = ''.join(f'<i class="{"on" if j <= i else ""}" style="width:{bw:.0f}px"></i>' for j in range(n))
        pos = f'right:{x}px' if right else f'left:{x}px'
        return f'<div class="progress abs" style="{pos};top:{y}px;display:flex;gap:{g}px">{bars}</div>'

    def url(self, fs, extra=''):
        return f'<div class="url" style="font-size:{fs};{extra}">jobnow.fr</div>'

    def foot(self, x, bottom, fs):
        return f'<div class="foot abs" style="left:{x}px;bottom:{bottom}px;font-size:{fs}px">jobnow.fr</div>'

    def illus(self, x, y, s, fmt, tpl, ctx=None):
        """CV illustration (three tilted pages) placed at (x, y) with scale s. Frame 600x520."""
        import gen
        return (f'<div class="illus abs" style="left:{x}px;top:{y}px;width:600px;height:520px;transform-origin:0 0;'
                f'transform:scale({s})">{gen.stack()}</div>')

    def list_item(self, it, nsize, tfs, sfs, gap, sub=True):
        """Row of a list (pin, recap): number badge + short title (+ fix_short)."""
        s = f'<div class="s" style="font-size:{sfs};margin-top:{fx(10)}">{rich(it["fix_short"])}</div>' if sub else ''
        return (f'<div class="li" style="display:flex;align-items:{"flex-start" if sub else "center"};gap:{gap}">'
                f'<div class="n" style="width:{nsize};height:{nsize};font-size:calc({nsize} * .44)">{e(it["n"])}</div>'
                f'<div><div class="t fw" style="font-size:{tfs}">{rich(it["short"])}</div>{s}</div></div>')

    # ------------------------------------------------------------------ metrics
    def metrics(self, fmt):
        return {
            'vertical': dict(x=80, w=840, brand=(80, 120, 52, None), prog=(80, 230, 840),
                             hook_box=(80, 300, 900, 860), illus_hook=(400, 1180, 1.05),
                             eb=32, hook_h1=128, hook_sub=56, item_box=(80, 290, 840, 1230),
                             num=170, title=112, title_long=104, gap_num=34, body=54, ex_k=1.22, card_s=1.3,
                             fix=54, fixlab=28, fixpad=(42, 48), gap_fix=56,
                             outro_box=(80, 250, 900, 1270), lock=(140, 160), cta=72, chip=34, url=84),
            'wide': dict(x=110, brand=(110, 80, 50, 40), brand_title=(110, 90, 56, 46), prog_w=90 * 5,
                         title_box=(110, 290, 1080, 640), eb=30, w_h1=112, w_sub=42, illus_title=(1240, 300, 1.15),
                         slide_top=230, slide_w=1020, slide_w_full=1500, slide_h=700, kick=28, title=92, body=44,
                         fix=44, fixlab=24, fixpad=(34, 42), side_ex=(1220, 330, 590, 1.12), side_card=(1200, 400, 1.32),
                         illus_slide=(1280, 300, 1.05), recap_box=(110, 220, 1100, 760), illus_recap=(1280, 330, 1.0),
                         outro_box=(110, 220, 1300, 760), illus_outro=(1300, 360, 1.0), foot=(110, 70, 28)),
            'thumb': dict(box=(64, 70, 760, 500), h1=112, illus=(760, 120, .95), brand=(64, 610, 54, 44)),
            'pin': dict(brand=(70, 70, 50, None), box=(70, 190, 860, 1150), eb=26),
        }[fmt]

    # ================================================================== templates
    # ---- vertical video (1080x1920). Safe zone for text: x 80..920, y 240..1450.
    def v_hook(self, d, reveal=2):
        M = self.metrics('vertical')
        parts = (self.eyebrow(d['eyebrow'], fx(M['eb'])) +
                 self.h1(d['v_hook'], fx(M['hook_h1']), f'margin-top:{fx(40)}') +
                 self.body(d['v_hook_sub'], fx(M['hook_sub']), f'margin-top:{fx(52)};{vis(reveal >= 2)}'))
        ctx = dict(d=d)
        inner = self.brand(*M['brand'], right=M.get('brand_right', False))
        inner += self.illus(*M['illus_hook'], 'vertical', 'hook', ctx)
        inner += self.frame('vertical', 'hook', M['hook_box'], parts, ctx, align='start')
        return self.page('vertical', 'hook', inner, ctx)

    def v_item(self, d, it, i, n, reveal=3):
        M = self.metrics('vertical')
        ctx = dict(d=d, it=it, i=i, n=n)
        blocks = self.item_head(it, i, n, 'vertical', M)
        blocks += self.body(it['body_short'], fx(M['body']), f'margin-top:{fx(40)};{vis(reveal >= 2)}')
        if it.get('example'):
            blocks += self.example(it['example'], M['ex_k'], '100%', f'margin-top:{fx(48)};{vis(reveal >= 2)}')
        if it.get('card'):
            blocks += self.card(it['card'], M['card_s'], -3, f'margin-top:{fx(36)};{vis(reveal >= 2)}')
        p1, p2 = M['fixpad']
        blocks += self.fix(it.get('fixlab', 'À FAIRE'), it['fix'], fx(M['fix']), fx(M['fixlab']), f'{fx(p1)} {fx(p2)}',
                           f'margin-top:{fx(M["gap_fix"])};{vis(reveal >= 3)}')
        inner = self.brand(*M['brand'], right=M.get('brand_right', False))
        inner += self.progress(i, n, *M['prog'], 'vertical', right=M.get('prog_right', False))
        inner += self.frame('vertical', 'item', M['item_box'], blocks, ctx)
        return self.page('vertical', 'item', inner, ctx)

    def v_outro(self, d):
        M = self.metrics('vertical')
        ctx = dict(d=d)
        lsz, lfs = M['lock']
        parts = (self.lockup(lsz, lfs) +
                 self.h1(d['cta_headline'], fx(M['cta']), f'margin-top:{fx(84)}') +
                 self.chips(d['chips'], fx(M['chip']), f'{fx(18)} {fx(28)}', fx(18), f'margin-top:{fx(64)}') +
                 self.url(fx(M['url']), f'margin-top:{fx(96)}'))
        inner = self.frame('vertical', 'outro', M['outro_box'], parts, ctx)
        return self.page('vertical', 'outro', inner, ctx)

    # ---- wide video (1920x1080)
    def w_title(self, d):
        M = self.metrics('wide')
        ctx = dict(d=d)
        parts = (self.eyebrow(d['eyebrow'], fx(M['eb'])) +
                 self.h1(d['w_title'], fx(M['w_h1']), f'margin-top:{fx(36)}') +
                 self.body(d['sub'], fx(M['w_sub']), f'margin-top:{fx(40)};max-width:{fx(960)}'))
        inner = self.brand(*M['brand_title'], right=M.get('brand_right', False))
        inner += self.illus(*M['illus_title'], 'wide', 'title', ctx)
        inner += self.frame('wide', 'title', M['title_box'], parts, ctx, align='start')
        inner += self.foot(M['x'], *M['foot'][1:])
        return self.page('wide', 'title', inner, ctx)

    def w_slide(self, d, kicker, title, body=None, fix=None, example=None, card=None, side=None, idx=None, n=None, fixlab='À FAIRE'):
        M = self.metrics('wide')
        ctx = dict(d=d, i=idx, n=n, side=side, example=example, card=card, kicker=kicker, why=fix is None)
        blocks = self.kicker(kicker, fx(M['kick']))
        blocks += self.title(title, fx(M['title']), f'margin-top:{fx(26)}')
        if body:
            blocks += self.body(body, fx(M['body']), f'margin-top:{fx(34)}')
        if fix:
            p1, p2 = M['fixpad']
            blocks += self.fix(fixlab, fix, fx(M['fix']), fx(M['fixlab']), f'{fx(p1)} {fx(p2)}', f'margin-top:{fx(44)}')
        width = M['slide_w'] if (example or card or side) else M['slide_w_full']
        inner = self.brand(*M['brand'], right=M.get('brand_right', False))
        if idx is not None:
            inner += self.progress(idx, n, M.get('prog_x', M['x']), M.get('prog_y', 98), M['prog_w'], 'wide', right=True)
        inner += self.w_side(example, card, side, ctx)
        inner += self.frame('wide', 'slide', (M['x'], M['slide_top'], width, M['slide_h']), blocks, ctx, align='start')
        inner += self.foot(M['x'], *M['foot'][1:])
        return self.page('wide', 'slide', inner, ctx)

    def w_side(self, example, card, side, ctx):
        M = self.metrics('wide')
        if example:
            x, y, w, k = M['side_ex']
            return f'<div class="abs" style="left:{x}px;top:{y}px;width:{w}px">{self.example(example, k, f"{w}px")}</div>'
        if card:
            x, y, s = M['side_card']
            return f'<div class="abs" style="left:{x}px;top:{y}px;width:700px">{self.card(card, s, -4)}</div>'
        if side == 'stack':
            return self.illus(*M['illus_slide'], 'wide', 'slide', ctx)
        return ''

    def w_recap(self, d, items, heading):
        M = self.metrics('wide')
        ctx = dict(d=d, items=items)
        lis = ''.join(self.list_item(it, fx(64), fx(46), None, fx(26), sub=False) for it in items)
        parts = (self.kicker('RÉCAP', fx(28)) + self.title(heading, fx(84), f'margin-top:{fx(22)}') +
                 f'<div class="list" style="display:flex;flex-direction:column;gap:{fx(30)};margin-top:{fx(54)}">{lis}</div>')
        inner = self.brand(*M['brand'], right=M.get('brand_right', False))
        inner += self.illus(*M['illus_recap'], 'wide', 'recap', ctx)
        inner += self.frame('wide', 'recap', M['recap_box'], parts, ctx, align='start')
        inner += self.foot(M['x'], *M['foot'][1:])
        return self.page('wide', 'recap', inner, ctx)

    def w_outro(self, d):
        M = self.metrics('wide')
        ctx = dict(d=d)
        parts = (self.lockup(130, 150) +
                 self.h1(d['cta_headline'], fx(80), f'margin-top:{fx(64)}') +
                 self.chips(d['chips'], fx(32), f'{fx(16)} {fx(28)}', fx(18), f'margin-top:{fx(54)}') +
                 self.url(fx(72), f'margin-top:{fx(70)}'))
        inner = self.illus(*M['illus_outro'], 'wide', 'outro', ctx)
        inner += self.frame('wide', 'outro', M['outro_box'], parts, ctx, align='start')
        return self.page('wide', 'outro', inner, ctx)

    # ---- YouTube thumbnail (1280x720)
    def thumb(self, d):
        M = self.metrics('thumb')
        ctx = dict(d=d)
        inner = self.illus(*M['illus'], 'thumb', 'thumb', ctx)
        inner += self.frame('thumb', 'thumb', M['box'], self.h1(d['thumb_text'], fx(M['h1']), 'line-height:1.02'), ctx, align='start')
        inner += self.brand(*M['brand'], right=M.get('brand_right', False))
        return self.page('thumb', 'thumb', inner, ctx)

    # ---- Pinterest pin (1000x1500)
    def pin(self, d):
        M = self.metrics('pin')
        ctx = dict(d=d)
        n = len(d['items'])
        ts, ss, gap, hs = {3: (52, 36, 64, 92), 4: (50, 35, 56, 88), 5: (49, 34, 50, 84), 6: (44, 31, 38, 80)}.get(n, (40, 28, 30, 76))
        lis = ''.join(self.list_item(it, fx(72), fx(ts), fx(ss), fx(28)) for it in d['items'])
        parts = (self.eyebrow(d['eyebrow'], fx(M['eb'])) + self.h1(d['pin_headline'], fx(hs), f'margin-top:{fx(26)}') +
                 f'<div class="list" style="display:flex;flex-direction:column;gap:{fx(gap)};margin-top:{fx(70)}">{lis}</div>')
        inner = self.brand(*M['brand'], right=M.get('brand_right', False))
        inner += self.frame('pin', 'pin', M['box'], parts, ctx, align='start')
        inner += self.pin_foot(d)
        return self.page('pin', 'pin', inner, ctx)

    def pin_foot(self, d):
        return (f'<div class="abs" style="left:70px;right:70px;bottom:64px;display:flex;justify-content:space-between;align-items:center">'
                f'<div class="url" style="font-size:40px">jobnow.fr</div><div class="pinfoot" style="font-size:24px">{e(d["pin_foot"])}</div></div>')
