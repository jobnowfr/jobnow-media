# -*- coding: utf-8 -*-
"""cahier: a page of a French Seyès notebook. Black marker writing, red pen corrections in the
margin, highlighter on the key words, the fix on a Post-it, the date written at the top."""
import datetime
from .base import Style, e, rich, fx, font_face, noise, logo_svg, cv_lines, card_fs, BLUE, LIME, SANS

PAPER, LINE, SUB, MARGIN = '#fdfdfb', '#a9bde8', '#dfe6f5', '#e8483e'
INK, GREY, PEN, RED = '#1d1d1f', '#3a3a3e', '#2645a8', '#de3129'
HAND = "'Shantell Sans', 'Comic Sans MS', sans-serif"
CURSIVE = "'Playwrite FR Trad', cursive"

JOURS = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']
MOIS = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']


def date_fr(iso):
    try:
        d = datetime.date.fromisoformat(iso)
    except (TypeError, ValueError):
        return ''
    return f'{JOURS[d.weekday()].capitalize()} {d.day} {MOIS[d.month - 1]}'


def check_svg(size, color=RED, sw=6):
    size = size if isinstance(size, str) else f'{size}px'
    return (f'<svg viewBox="0 0 48 48" style="display:inline-block;vertical-align:middle;flex:none;width:{size};height:{size};overflow:visible" aria-hidden="true">'
            f'<path d="M5 25 Q 12 30 17 39 Q 27 17 44 6" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def circle_svg(w, h, color=RED, sw=5):
    """Hand-drawn loop around something, slightly open with an overshoot."""
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 200 120" preserveAspectRatio="none" style="position:absolute;left:0;top:0;overflow:visible" aria-hidden="true">'
            f'<path d="M118 8 C 60 2, 8 22, 10 62 C 12 104, 92 116, 150 104 C 196 94, 198 44, 168 22 C 146 6, 96 4, 70 12" '
            f'fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" vector-effect="non-scaling-stroke"/></svg>')


class Cahier(Style):
    key = 'cahier'
    label_case = 'sentence'
    trans_item = 'smoothleft'
    palettes = [
        dict(hl='#fff04d', post='#ffa6d2', post2='#9fe3ff', post3='#c3f59a'),   # stabilo jaune, post-it rose
        dict(hl='#ffacd6', post='#fff27a', post2='#9fe3ff', post3='#ffcf7f'),   # stabilo rose, post-it jaune
        dict(hl='#a8f58c', post='#ffd27f', post2='#ffa6d2', post3='#fff27a'),   # stabilo vert, post-it orange
    ]

    def fonts(self):
        return (font_face('Shantell Sans', 'ShantellSans.woff2', '300 800') +
                font_face('Playwrite FR Trad', 'PlaywriteFRTrad.woff2', '100 400') +
                font_face('Bricolage Grotesque', 'BricolageGrotesque.woff2', '200 800'))

    # page grid per format: (line spacing, margin x)
    GRID = {'vertical': (64, 140), 'wide': (56, 150), 'thumb': (44, 92), 'pin': (56, 108), 'carousel': (60, 130)}

    def css(self, W, H, fmt, k):
        L, mx = self.GRID[fmt]
        p = self.p
        return f"""
html,body{{background:{PAPER}}}
body{{font-family:{HAND};color:{INK};font-variation-settings:'INFM' 35,'BNCE' 0}}
.bg{{position:absolute;inset:0;background-color:{PAPER};
  background-image:linear-gradient(0deg, {LINE} 2px, transparent 2px), linear-gradient(0deg, {SUB} 1.2px, transparent 1.2px),
    linear-gradient(90deg, {SUB} 1.2px, transparent 1.2px);
  background-size:100% {L}px, 100% {L / 4}px, {L}px 100%;
  background-position:0 {L - 18}px, 0 {L - 18}px, {mx + L * .5}px 0}}
.grain{{position:absolute;inset:0;background-image:{noise(300, .9, 2, .05)};mix-blend-mode:multiply}}
.margin{{position:absolute;top:0;bottom:0;left:{mx}px;width:3px;background:{MARGIN};opacity:.9}}
.hl{{background-image:linear-gradient(100deg, transparent .2em, {p['hl']} .3em, {p['hl']} calc(100% - .25em), transparent calc(100% - .12em));
  background-size:100% 74%;background-position:0 62%;background-repeat:no-repeat;padding:0 .14em;margin:0 -.04em;
  box-decoration-break:clone;-webkit-box-decoration-break:clone}}
b{{font-weight:800}}
.cur{{font-family:{CURSIVE};font-weight:400;-webkit-text-stroke:.022em currentColor;line-height:1.5}}
.date{{color:{PEN}}}
.eyebrow{{font-family:{CURSIVE};font-weight:400;color:{RED};-webkit-text-stroke:.025em {RED};line-height:1.6}}
.kicker{{font-family:{CURSIVE};font-weight:400;color:{RED};-webkit-text-stroke:.025em {RED};line-height:1.6}}
.h1{{font-weight:800;font-variation-settings:'INFM' 55,'BNCE' 8;line-height:1.08;letter-spacing:-.01em}}
.title{{font-weight:800;font-variation-settings:'INFM' 55,'BNCE' 8;line-height:1.12;letter-spacing:-.01em}}
.title .u{{text-decoration:underline;text-decoration-color:{RED};text-decoration-thickness:.07em;text-underline-offset:.2em;text-decoration-skip-ink:none}}
.body{{font-weight:500;color:{GREY};line-height:1.42}}
.mnum{{position:absolute;display:flex;align-items:center;justify-content:center;font-family:{CURSIVE};color:{RED};-webkit-text-stroke:.045em {RED};line-height:1}}
.post{{position:relative;background:var(--pc);color:{INK};
  background-image:linear-gradient(170deg, rgba(255,255,255,.35), rgba(255,255,255,0) 40%, rgba(0,0,0,.04));
  border-radius:3px 3px 22px 3px;box-shadow:0 26px 30px -20px rgba(40,30,0,.45), 0 3px 6px rgba(0,0,0,.08)}}
.post .lab{{font-family:{CURSIVE};color:{RED};-webkit-text-stroke:.025em {RED};line-height:1.5}}
.post .txt{{font-weight:700;font-variation-settings:'INFM' 45;line-height:1.3}}
.tape{{position:absolute;background:rgba(255,255,255,.62);border:1px solid rgba(0,0,0,.06);box-shadow:0 1px 3px rgba(0,0,0,.08)}}
.exr{{line-height:1.45}}
.exr .tag{{font-family:{CURSIVE};color:{RED};-webkit-text-stroke:.025em {RED};line-height:1}}
.exr.bad .v{{font-weight:600;color:{GREY};text-decoration:line-through;text-decoration-color:{RED};text-decoration-thickness:.12em}}
.exr.good .v{{font-weight:800}}
.chip{{display:inline-block;background:var(--pc);font-weight:700;color:{INK};border-radius:2px 2px 12px 2px;
  box-shadow:0 12px 14px -10px rgba(40,30,0,.45), 0 2px 3px rgba(0,0,0,.06)}}
.url{{font-weight:800;font-variation-settings:'INFM' 55;text-decoration:underline;text-decoration-color:{RED};text-decoration-thickness:.08em;text-underline-offset:.18em}}
.foot{{font-weight:800;font-variation-settings:'INFM' 55}}
.pinfoot{{font-family:{CURSIVE};color:{RED};-webkit-text-stroke:.025em {RED}}}
.li .t{{font-weight:800;font-variation-settings:'INFM' 50;line-height:1.15}}
.li .s{{font-weight:500;color:{GREY};line-height:1.32}}
.box{{position:relative;display:inline-block;border:2.5px solid {INK};border-radius:4px 6px 3px 5px}}
"""

    def bg(self, fmt, tpl, ctx):
        out = '<div class="bg"></div><div class="margin"></div><div class="grain"></div>'
        d = ctx.get('d') or {}
        L, mx = self.GRID[fmt]
        date = date_fr(self.date)
        if date and fmt == 'vertical' and tpl in ('hook', 'item'):
            out += f'<div class="abs cur date" style="left:{mx + 46}px;top:96px;font-size:50px">{e(date)}</div>'
        if date and fmt == 'wide' and tpl in ('title', 'slide', 'recap'):
            out += f'<div class="abs cur date" style="left:{mx + 46}px;top:52px;font-size:40px">{e(date)}</div>'
        return out

    # ------------------------------------------------------------------ parts
    def logo_colors(self):
        return (BLUE, '#fff', LIME)

    def wordmark_css(self):
        return f'color:{INK}'

    def eyebrow(self, s, fs, extra=''):
        return f'<div class="eyebrow" style="font-size:{fs};{extra}">{e(s)}</div>'

    def title(self, s, fs, extra=''):
        return f'<div class="title fw" style="font-size:{fs};{extra}"><span class="u">{rich(s)}</span></div>'

    def margin_num(self, label, size, mx, x0):
        """Circled number written in the margin. x0 = left of the content box."""
        c = round(size * 1.12)
        left = mx / 2 - x0 - c / 2
        return (f'<div class="mnum" style="left:{left:.0f}px;top:{-round(size * .1)}px;width:{c}px;height:{round(c * .86)}px;font-size:{round(size * .62)}px">'
                f'{circle_svg(c, round(c * .86), RED, 5.5)}<span style="position:relative;top:{round(size * .04)}px">{e(label)}</span></div>')

    def item_head(self, it, i, n, fmt, S):
        L, mx = self.GRID[fmt]
        num = self.margin_num(str(int(it['n'])), S['mnum'], mx, S['x'])
        fs = S['title_long'] if len(it['title']) > 24 else S['title']
        return f'<div style="position:relative">{num}{self.title(it["title"], fx(fs))}</div>'

    def kicker(self, s, fs, extra=''):
        return f'<div class="kicker" style="font-size:{fs};{extra}">{e(self.lab(s))}</div>'

    def fix(self, lab, txt, fs, labfs, pad, extra=''):
        return (f'<div class="post" style="--pc:{self.p["post"]};padding:{pad};transform:rotate(-1.3deg);{extra}">'
                f'<div class="tape" style="left:42%;top:{fx(-22)};width:{fx(170)};height:{fx(42)};transform:rotate(3deg)"></div>'
                f'<div class="lab" style="font-size:{labfs}">{e(self.lab(lab))}</div>'
                f'<div class="txt" style="font-size:{fs};margin-top:{fx(6)}">{rich(txt)}</div></div>')

    def example(self, ex, k, width, extra=''):
        fs = fx(round(40 * k))
        tfs = fx(round(30 * k))
        return (f'<div style="width:{width};display:flex;flex-direction:column;gap:{fx(round(14 * k))};{extra}">'
                f'<div class="exr bad" style="font-size:{fs}"><span class="tag" style="font-size:{tfs}">{e(self.lab(ex.get("badtag", "NON")))} :</span> '
                f'<span class="v">{e(ex["bad"])}</span></div>'
                f'<div class="exr good" style="font-size:{fs}"><span class="tag" style="font-size:{tfs}">{e(self.lab(ex.get("goodtag", "OUI")))} :</span> '
                f'<span class="v"><span class="hl">{e(ex["good"])}</span></span>&nbsp;{check_svg(fx(round(44 * k)))}</div></div>')

    def card(self, text, s, rot=-2, extra=''):
        """Index card (fiche bristol) with the job title written on it."""
        w, h = 460, 190
        lines = ''.join(f'<div style="position:absolute;left:0;right:0;top:{y}px;height:1.5px;background:#b7c7ea"></div>' for y in (92, 128, 164))
        inner = (f'<div style="position:absolute;inset:0;background:#fff;border-radius:3px;box-shadow:0 22px 26px -18px rgba(0,0,0,.4),0 2px 5px rgba(0,0,0,.08)">'
                 f'<div style="position:absolute;left:0;right:0;top:56px;height:2.5px;background:{RED}"></div>{lines}'
                 f'<div class="cur" style="position:absolute;left:22px;top:6px;font-size:24px;color:{RED}">Titre de poste</div>'
                 f'<div style="position:absolute;left:24px;top:74px;font-weight:700;font-size:{card_fs(text, 38, 20)}px;font-variation-settings:\'INFM\' 60;white-space:nowrap">{e(text)}</div>'
                 f'<div class="tape" style="left:-18px;top:-10px;width:90px;height:32px;transform:rotate(-32deg)"></div></div>')
        hh = round(h * s + 50)
        return (f'<div style="position:relative;height:{fx(hh)};{extra}"><div style="position:absolute;left:{fx(6)};top:{fx(26)};width:{w}px;height:{h}px;'
                f'transform-origin:0 0;transform:rotate({rot}deg) scale(calc({s} * var(--f, 1)))">{inner}</div></div>')

    def chips(self, chips, fs, pad, gap, extra=''):
        cols = [self.p['post'], self.p['post2'], self.p['post3']]
        rots = [-2.2, 1.6, -1.1, 2.0]
        cs = ''.join(f'<span class="chip" style="--pc:{cols[j % 3]};font-size:{fs};padding:{pad};transform:rotate({rots[j % 4]}deg)">{e(c)}</span>'
                     for j, c in enumerate(chips))
        return f'<div style="display:flex;flex-wrap:wrap;gap:{gap};{extra}">{cs}</div>'

    def progress(self, i, n, x, y, w, fmt, right=False):
        sz = 34 if fmt == 'vertical' else 28
        boxes = ''
        for j in range(n):
            mark = f'<div style="position:absolute;left:2px;top:-12px">{check_svg(sz + 8, RED, 6)}</div>' if j <= i else ''
            boxes += f'<div class="box" style="width:{sz}px;height:{sz}px;transform:rotate({(-1) ** j * 2}deg)">{mark}</div>'
        pos = f'right:{x}px' if right else f'left:{x}px'
        return f'<div class="abs" style="{pos};top:{y}px;display:flex;gap:{round(sz * .55)}px">{boxes}</div>'

    def url(self, fs, extra=''):
        return f'<div class="url" style="font-size:{fs};{extra}">jobnow.fr</div>'

    def foot(self, x, bottom, fs):
        L, mx = self.GRID['wide']
        return f'<div class="foot abs" style="left:{mx + 46}px;bottom:{bottom}px;font-size:{fs + 4}px">jobnow.fr</div>'

    def list_item(self, it, nsize, tfs, sfs, gap, sub=True, fmt='pin'):
        L, mx = self.GRID[fmt]
        x0 = self.metrics(fmt).get('x', 0)
        num = self.margin_num(str(int(it['n'])), 64 if fmt == 'pin' else 58, mx, x0)
        s = f'<div class="s" style="font-size:{sfs};margin-top:{fx(6)}">{rich(it["fix_short"])}</div>' if sub else ''
        return f'<div class="li" style="position:relative">{num}<div class="t fw" style="font-size:{tfs}">{rich(it["short"])}</div>{s}</div>'

    def sheet(self, x, y, w, h, rot, kind, z=1, marks=True):
        c = dict(head=INK, accent=RED if kind == 'center' else '#6b6b70', text='#cfcfd4', side='#2b2b30', sidetext='#ffffff', band=self.p['hl'], bandtext=INK)
        inner = cv_lines(kind, w, h, c)
        extra = ''
        if marks:
            extra = (f'<div style="position:absolute;left:{w * .03:.0f}px;top:{h * .58:.0f}px;width:{w * .62:.0f}px;height:{h * .14:.0f}px">{circle_svg(round(w * .62), round(h * .14), RED, 4)}</div>'
                     f'<div style="position:absolute;right:{w * .06:.0f}px;top:{h * .76:.0f}px">{check_svg(round(w * .2), RED, 7)}</div>')
        return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg);z-index:{z};background:#fff;'
                f'border:1px solid #e4e4e8;box-shadow:0 30px 40px -24px rgba(0,0,0,.45),0 3px 8px rgba(0,0,0,.08)">{inner}{extra}'
                f'<div class="tape" style="left:{w * .38:.0f}px;top:-16px;width:{w * .26:.0f}px;height:34px;transform:rotate(-4deg)"></div></div>')

    def illus(self, x, y, s, fmt, tpl, ctx=None):
        post = self.p['post']
        inner = (self.sheet(40, 70, 300, 410, -8, 'side', 1, marks=False) +
                 self.sheet(210, 30, 320, 440, 5, 'band', 2) +
                 f'<div class="post" style="--pc:{post};position:absolute;left:0;top:300px;width:200px;height:180px;transform:rotate(-6deg);z-index:3;padding:22px">'
                 f'<div class="cur" style="font-size:30px;color:{RED};line-height:1.4">Relire</div>'
                 f'<div class="cur" style="font-size:30px;color:{RED};line-height:1.4">avant d’envoyer</div></div>')
        return (f'<div class="illus abs" style="left:{x}px;top:{y}px;width:600px;height:520px;transform-origin:0 0;transform:scale({s})">{inner}</div>')

    # ------------------------------------------------------------------ metrics
    def metrics(self, fmt):
        M = super().metrics(fmt)
        L, mx = self.GRID[fmt]
        x = mx + 46
        if fmt == 'vertical':
            M.update(x=x, w=946 - x, brand=(70, 104, 46, None), brand_right=True, prog=(x, 196, 0),
                     hook_box=(x, 300, 960 - x, 840), illus_hook=(430, 1190, 1.0), eb=46, hook_h1=116, hook_sub=54,
                     item_box=(x, 300, 950 - x, 1220), mnum=104, num=0, title=96, title_long=90, body=52, ex_k=1.2, card_s=1.32,
                     fix=50, fixlab=46, fixpad=(36, 44), gap_fix=64, outro_box=(x, 250, 960 - x, 1270), lock=(120, 136), cta=72, chip=40, url=80)
        elif fmt == 'wide':
            M.update(x=x, brand=(110, 52, 46, 38), brand_title=(110, 52, 46, 38), brand_right=True, prog_x=110, prog_y=132, title_box=(x, 250, 1060, 700), eb=40, w_h1=104,
                     slide_top=200, slide_w=1000, slide_w_full=1520, slide_h=760, kick=42, title=90, body=45, mnum=96,
                     fix=44, fixlab=42, fixpad=(32, 42), side_ex=(1250, 380, 560, 1.05), side_card=(1260, 420, 1.25),
                     illus_title=(1280, 300, 1.05), illus_slide=(1300, 330, .98), recap_box=(x, 190, 1060, 800), illus_recap=(1300, 330, .98),
                     outro_box=(x, 200, 1200, 780), illus_outro=(1300, 380, .98))
        elif fmt == 'thumb':
            M.update(x=x, box=(x, 54, 650, 520), h1=104, illus=(800, 150, .82), brand=(x, 618, 46, 38))
        elif fmt == 'pin':
            M.update(x=x, brand=(x, 66, 46, None), box=(x, 168, 1000 - x - 60, 1130), eb=38)
        return M

    # ------------------------------------------------------------------ templates that differ
    def w_recap(self, d, items, heading):
        M = self.metrics('wide')
        ctx = dict(d=d, items=items)
        lis = ''.join(self.list_item(it, None, fx(46), None, None, sub=False, fmt='wide') for it in items)
        parts = (self.kicker('Récap', fx(40)) + self.title(heading, fx(78), f'margin-top:{fx(6)}') +
                 f'<div style="display:flex;flex-direction:column;gap:{fx(30)};margin-top:{fx(50)}">{lis}</div>')
        inner = self.brand(*M['brand'], right=True)
        inner += self.illus(*M['illus_recap'], 'wide', 'recap', ctx)
        inner += self.frame('wide', 'recap', M['recap_box'], parts, ctx, align='start')
        inner += self.foot(M['x'], *M['foot'][1:])
        return self.page('wide', 'recap', inner, ctx)

    def pin(self, d):
        M = self.metrics('pin')
        ctx = dict(d=d)
        n = len(d['items'])
        ts, ss, gap, hs = {3: (50, 36, 60, 88), 4: (48, 34, 52, 84), 5: (46, 33, 44, 80), 6: (42, 30, 36, 76)}.get(n, (38, 27, 28, 72))
        lis = ''.join(self.list_item(it, None, fx(ts), fx(ss), None, fmt='pin') for it in d['items'])
        parts = (self.eyebrow(d['eyebrow'], fx(M['eb'])) + self.h1(d['pin_headline'], fx(hs), f'margin-top:{fx(10)}') +
                 f'<div style="display:flex;flex-direction:column;gap:{fx(gap)};margin-top:{fx(64)}">{lis}</div>')
        inner = self.brand(*M['brand'])
        inner += self.frame('pin', 'pin', M['box'], parts, ctx, align='start')
        x = M['x']
        inner += (f'<div class="abs" style="left:{x}px;right:60px;bottom:52px">'
                  f'<div class="pinfoot" style="font-size:30px;white-space:nowrap">{e(d["pin_foot"])}</div>'
                  f'<div class="url" style="font-size:50px;margin-top:6px">jobnow.fr</div></div>')
        return self.page('pin', 'pin', inner, ctx)
