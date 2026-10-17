# -*- coding: utf-8 -*-
"""affiche: a bright street poster. One flat loud colour, black ink, huge condensed capitals,
hard offset shadows, a giant tone-on-tone number, and tear-off tabs with jobnow.fr at the end."""
from .base import Style, e, rich, fx, font_face, noise, logo_svg, cv_lines, mix, plain, card_fs, SANS

INK, PAPER = '#000000', '#ffffff'
DISPLAY = "'Anton', 'Impact', sans-serif"
TEXT = "'Archivo', system-ui, sans-serif"


class Affiche(Style):
    key = 'affiche'
    label_case = 'sentence'
    trans_item = 'wipeleft'
    palettes = [
        dict(bg='#ff5b1f', acc='#ffe24a'),   # orange, jaune
        dict(bg='#ffd60a', acc='#ff4f9a'),   # jaune, rose
        dict(bg='#ff8fca', acc='#fff04d'),   # rose, jaune
        dict(bg='#2ed47a', acc='#fff04d'),   # vert, jaune
    ]

    def fonts(self):
        return (font_face('Anton', 'Anton.woff2', '400') + font_face('Archivo', 'Archivo.woff2', '100 900') +
                font_face('Bricolage Grotesque', 'BricolageGrotesque.woff2', '200 800'))

    def css(self, W, H, fmt, k):
        p = self.p
        tone = mix(p['bg'], INK, .09)
        return f"""
html,body{{background:{p['bg']}}}
body{{font-family:{TEXT};color:{INK}}}
.bg{{position:absolute;inset:0;background-color:{p['bg']}}}
.grain{{position:absolute;inset:0;background-image:{noise(260, .75, 3, .09)};mix-blend-mode:multiply}}
.giant{{position:absolute;font-family:{DISPLAY};color:{tone};line-height:.8;white-space:nowrap}}
.hl{{background:{INK};color:{p['acc']};padding:0 .1em;box-decoration-break:clone;-webkit-box-decoration-break:clone}}
.h1 .hl,.title .hl{{background:linear-gradient({INK},{INK}) 0 48.7% / 100% 66.4% no-repeat;padding:0 .08em;margin:0 -.02em}}
b{{font-weight:800}}
.eyebrow,.kicker{{display:inline-block;background:{INK};color:{p['acc']};font-family:{TEXT};font-weight:800;font-stretch:88%;
  padding:.28em .55em .32em;transform:rotate(-1.5deg);transform-origin:0 50%;line-height:1.1}}
.h1,.title{{font-family:{DISPLAY};font-weight:400;text-transform:uppercase;line-height:1.04;letter-spacing:.004em}}
.body{{font-weight:500;line-height:1.36;letter-spacing:-.005em}}
.num{{font-family:{DISPLAY};line-height:.86;display:flex;align-items:flex-end}}
.num small{{font-size:.36em;margin-left:.12em;padding-bottom:.08em;opacity:.55}}
.fix{{background:{INK};color:{PAPER};box-shadow:{fx(14)} {fx(14)} 0 {p['acc']};transform:rotate(-1deg)}}
.fix .lab{{display:inline-block;background:{p['acc']};color:{INK};font-weight:800;font-stretch:90%;padding:.18em .5em .22em;line-height:1.1}}
.fix .txt{{font-weight:700;line-height:1.3;letter-spacing:-.01em}}
.ex{{display:flex;align-items:center;border:{fx(5)} solid {INK}}}
.ex.bad{{background:{PAPER}}}
.ex.good{{background:{p['acc']};box-shadow:{fx(10)} {fx(10)} 0 {INK}}}
.ex .tag{{background:{INK};color:{PAPER};font-weight:800;font-stretch:88%;flex:none;line-height:1.1}}
.ex.good .tag{{color:{p['acc']}}}
.ex .v{{font-weight:700;line-height:1.22}}
.ex.bad .v{{text-decoration:line-through;text-decoration-thickness:.12em;text-decoration-color:{INK}}}
.chip{{background:{PAPER};border:{fx(4)} solid {INK};font-weight:700;border-radius:999px;box-shadow:{fx(5)} {fx(5)} 0 {INK}}}
.li .n{{font-family:{DISPLAY};background:{INK};color:{p['bg']};display:flex;align-items:center;justify-content:center;flex:none;line-height:1}}
.li .t{{font-weight:800;font-stretch:92%;line-height:1.12;letter-spacing:-.01em}}
.li .s{{font-weight:500;line-height:1.3}}
.progress i{{display:block;height:{round(14 * k)}px;background:{INK};opacity:.18}}
.progress i.on{{opacity:1}}
.url{{font-family:{TEXT};font-weight:900;font-stretch:100%;letter-spacing:-.02em}}
.foot{{font-weight:900;letter-spacing:-.01em}}
.pinfoot{{font-weight:600}}
.flyer{{position:absolute;background:{PAPER};box-shadow:0 30px 50px -30px rgba(0,0,0,.45)}}
.tape{{position:absolute;background:rgba(255,255,255,.55);border:1px solid rgba(0,0,0,.08);box-shadow:0 2px 4px rgba(0,0,0,.08)}}
.tabs{{position:absolute;display:flex}}
.tabs .tab{{flex:1;background:{PAPER};border-left:3px dashed rgba(0,0,0,.45);display:flex;align-items:center;justify-content:center}}
.tabs .tab:first-child{{border-left:0}}
.tabs .tab span{{writing-mode:vertical-rl;transform:rotate(180deg);font-weight:900;letter-spacing:-.01em;white-space:nowrap}}
.tabs .tab.gone{{background:transparent;border-left:3px dashed transparent}}
.cut{{position:absolute;height:0;border-top:3px dashed rgba(0,0,0,.45)}}
"""

    # ------------------------------------------------------------------ decor
    def bg(self, fmt, tpl, ctx):
        out = '<div class="bg"></div>'
        W = {'vertical': 1080, 'wide': 1920, 'thumb': 1280, 'pin': 1000}.get(fmt, 1080)
        glyph = None
        if tpl == 'item' and ctx.get('it'):
            glyph = str(int(ctx['it']['n']))
        elif tpl == 'slide' and ctx.get('i') is not None:
            glyph = str(ctx['i'] + 1)
        elif tpl in ('hook', 'thumb', 'title'):
            d = ctx.get('d') or {}
            txt = d.get('v_hook', '') if tpl == 'hook' else d.get('thumb_text' if tpl == 'thumb' else 'w_title', '')
            glyph = '?' if '?' in txt else '!'
        if glyph:
            if fmt == 'vertical':
                out += f'<div class="giant" style="right:-70px;bottom:-120px;font-size:1500px">{glyph}</div>'
            elif fmt == 'wide':
                out += f'<div class="giant" style="right:-60px;bottom:-140px;font-size:1250px">{glyph}</div>'
            elif fmt == 'thumb':
                out += f'<div class="giant" style="right:300px;bottom:-110px;font-size:900px">{glyph}</div>'
        return out + '<div class="grain"></div>'

    # ------------------------------------------------------------------ parts
    def logo_colors(self):
        return (INK, self.p['bg'], INK)

    def wordmark_css(self):
        return f'color:{INK}'

    def eyebrow(self, s, fs, extra=''):
        return f'<div><div class="eyebrow" style="font-size:{fs};{extra}">{e(s)}</div></div>'

    def kicker(self, s, fs, extra=''):
        return f'<div><div class="kicker" style="font-size:{fs};{extra}">{e(self.lab(s))}</div></div>'

    def item_head(self, it, i, n, fmt, S):
        fs = S['title_long'] if len(it['title']) > 24 else S['title']
        return (f'<div class="num" style="font-size:{fx(S["num"])}">{int(it["n"])}<small>/{n}</small></div>' +
                self.title(it['title'], fx(fs), f'margin-top:{fx(S["gap_num"])}'))

    def fix(self, lab, txt, fs, labfs, pad, extra=''):
        return (f'<div class="fix" style="padding:{pad};{extra}"><div class="lab" style="font-size:{labfs}">{e(self.lab(lab))}</div>'
                f'<div class="txt" style="font-size:{fs};margin-top:{fx(18)}">{rich(txt)}</div></div>')

    def example(self, ex, k, width, extra=''):
        fs = fx(round(36 * k))
        pad = f'{fx(round(20 * k))} {fx(round(24 * k))}'
        tg = f'font-size:{fx(round(24 * k))};padding:{fx(round(8 * k))} {fx(round(12 * k))}'
        return (f'<div style="display:flex;flex-direction:column;gap:{fx(round(20 * k))};width:{width};{extra}">'
                f'<div class="ex bad" style="padding:{pad};gap:{fx(round(18 * k))}"><span class="tag" style="{tg}">{e(self.lab(ex.get("badtag", "NON")))}</span>'
                f'<span class="v" style="font-size:{fs}">{e(ex["bad"])}</span></div>'
                f'<div class="ex good" style="padding:{pad};gap:{fx(round(18 * k))}"><span class="tag" style="{tg}">{e(self.lab(ex.get("goodtag", "OUI")))}</span>'
                f'<span class="v" style="font-size:{fs}">{e(ex["good"])}</span></div></div>')

    def card_inner(self, text):
        return (f'<div style="position:absolute;inset:0;padding:26px 26px 0;background:{PAPER};border:5px solid {INK};box-shadow:14px 14px 0 {INK}">'
                f'<div style="font-weight:800;font-size:24px;line-height:1">Titre de poste</div>'
                f'<div style="margin-top:14px;height:72px;border:4px solid {INK};background:{self.p["acc"]};display:flex;align-items:center;padding-left:18px;'
                f'font-weight:800;font-size:{card_fs(text, 28)}px;white-space:nowrap">{e(text)}<span style="display:inline-block;width:4px;height:36px;margin-left:4px;background:{INK}"></span></div></div>')

    def chips(self, chips, fs, pad, gap, extra=''):
        cs = ''.join(f'<span class="chip" style="font-size:{fs};padding:{pad}">{e(c)}</span>' for c in chips)
        return f'<div style="display:flex;flex-wrap:wrap;gap:{gap};{extra}">{cs}</div>'

    def progress(self, i, n, x, y, w, fmt, right=False):
        g = 12
        bw = (w - g * (n - 1)) / n
        bars = ''.join(f'<i class="{"on" if j <= i else ""}" style="width:{bw:.0f}px"></i>' for j in range(n))
        pos = f'right:{x}px' if right else f'left:{x}px'
        return f'<div class="progress abs" style="{pos};top:{y}px;display:flex;gap:{g}px">{bars}</div>'

    def page_sheet(self, x, y, w, h, rot, kind, z=1):
        c = dict(head=INK, accent=self.p['bg'], text='#c9c9c9', side=INK, sidetext='#ffffff', band=self.p['acc'], bandtext=INK)
        return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg);z-index:{z};'
                f'background:{PAPER};border:5px solid {INK};box-shadow:14px 14px 0 {INK};overflow:hidden">{cv_lines(kind, w - 10, h - 10, c)}</div>')

    def illus(self, x, y, s, fmt, tpl, ctx=None):
        inner = (self.page_sheet(60, 70, 280, 390, -9, 'side', 1) + self.page_sheet(240, 40, 300, 420, 6, 'band', 2))
        return f'<div class="illus abs" style="left:{x}px;top:{y}px;width:600px;height:520px;transform-origin:0 0;transform:scale({s})">{inner}</div>'

    def url(self, fs, extra=''):
        return f'<div class="url" style="font-size:{fs};{extra}">jobnow.fr</div>'

    def list_item(self, it, nsize, tfs, sfs, gap, sub=True):
        s = f'<div class="s" style="font-size:{sfs};margin-top:{fx(8)}">{rich(it["fix_short"])}</div>' if sub else ''
        return (f'<div class="li" style="display:flex;align-items:{"flex-start" if sub else "center"};gap:{gap}">'
                f'<div class="n" style="width:{nsize};height:{nsize};font-size:calc({nsize} * .62)">{int(it["n"])}</div>'
                f'<div style="flex:1;min-width:0"><div class="t fw" style="font-size:{tfs}">{rich(it["short"])}</div>{s}</div></div>')

    def tabs(self, x, y, w, h, n=7, fs=34, gone=(4,)):
        ts = ''.join(f'<div class="tab{" gone" if j in gone else ""}"><span style="font-size:{fs}px">{"" if j in gone else "jobnow.fr"}</span></div>' for j in range(n))
        return f'<div class="cut" style="left:{x}px;top:{y}px;width:{w}px"></div><div class="tabs" style="left:{x}px;top:{y + 3}px;width:{w}px;height:{h}px">{ts}</div>'

    # ------------------------------------------------------------------ metrics
    def metrics(self, fmt):
        M = super().metrics(fmt)
        if fmt == 'vertical':
            M.update(brand=(80, 118, 50, None), prog=(80, 220, 840), hook_box=(80, 290, 900, 900), illus_hook=(470, 1240, .95),
                     eb=40, hook_h1=158, hook_sub=54, item_box=(80, 290, 860, 1210), num=230, gap_num=6,
                     title=124, title_long=112, body=52, ex_k=1.22, card_s=1.25, fix=50, fixlab=34, fixpad=(40, 46), gap_fix=60)
        elif fmt == 'wide':
            M.update(eb=34, w_h1=124, kick=32, title=104, body=44, fix=44, fixlab=30, fixpad=(34, 42),
                     side_ex=(1230, 350, 590, 1.1), side_card=(1230, 400, 1.3), illus_title=(1260, 300, 1.1), illus_slide=(1290, 320, 1.0))
        elif fmt == 'thumb':
            M.update(box=(60, 50, 820, 540), h1=128, illus=(820, 150, .85), brand=(60, 622, 50, 42))
        return M

    # ------------------------------------------------------------------ templates that differ
    def thumb(self, d):
        M = self.metrics('thumb')
        ctx = dict(d=d)
        inner = self.illus(*M['illus'], 'thumb', 'thumb', ctx)
        inner += self.frame('thumb', 'thumb', M['box'], self.h1(d['thumb_text'], fx(M['h1']), 'line-height:.96'), ctx, align='center')
        inner += self.brand(*M['brand'])
        return self.page('thumb', 'thumb', inner, ctx)

    def v_outro(self, d):
        ctx = dict(d=d)
        fx0, fy, fw, fh = 70, 170, 940, 1290
        tab_h = 300
        inner = (f'<div class="flyer" style="left:{fx0}px;top:{fy}px;width:{fw}px;height:{fh - tab_h}px;transform:rotate(-1deg);transform-origin:50% 100%">'
                 f'<div class="tape" style="left:-30px;top:-14px;width:150px;height:46px;transform:rotate(-35deg)"></div>'
                 f'<div class="tape" style="right:-30px;top:-14px;width:150px;height:46px;transform:rotate(35deg)"></div>'
                 f'{self.fitbox(64, 70, fw - 128, fh - tab_h - 120, self.outro_parts(d, 1.0), "center")}'
                 f'{self.tabs(0, fh - tab_h, fw, tab_h, 7, 40)}</div>')
        return self.page('vertical', 'outro', inner, ctx)

    def outro_parts(self, d, k):
        return (self.lockup(round(110 * k), round(130 * k)) +
                self.h1(d['cta_headline'], fx(round(96 * k)), f'margin-top:{fx(round(56 * k))}') +
                self.chips(d['chips'], fx(round(34 * k)), f'{fx(14)} {fx(26)}', fx(16), f'margin-top:{fx(round(56 * k))}'))

    def w_outro(self, d):
        ctx = dict(d=d)
        fx0, fy, fw, fh = 150, 90, 1240, 920
        tab_h = 250
        inner = self.illus(1380, 400, 1.0, 'wide', 'outro', ctx)
        inner += (f'<div class="flyer" style="left:{fx0}px;top:{fy}px;width:{fw}px;height:{fh - tab_h}px;transform:rotate(-.8deg);transform-origin:50% 100%">'
                  f'<div class="tape" style="left:-30px;top:-14px;width:150px;height:46px;transform:rotate(-35deg)"></div>'
                  f'<div class="tape" style="right:-30px;top:-14px;width:150px;height:46px;transform:rotate(35deg)"></div>'
                  f'{self.fitbox(70, 56, fw - 140, fh - tab_h - 100, self.outro_parts(d, .95), "center")}'
                  f'{self.tabs(0, fh - tab_h, fw, tab_h, 10, 34, gone=(3, 7))}</div>')
        return self.page('wide', 'outro', inner, ctx)

    def pin(self, d):
        ctx = dict(d=d)
        n = len(d['items'])
        ts, ss, gap, hs = {3: (50, 34, 50, 112), 4: (48, 33, 42, 106), 5: (44, 31, 34, 100), 6: (40, 28, 26, 94)}.get(n, (36, 26, 20, 88))
        lis = ''.join(self.list_item(it, fx(76), fx(ts), fx(ss), fx(26)) for it in d['items'])
        parts = (self.eyebrow(d['eyebrow'], fx(32)) + self.h1(d['pin_headline'], fx(hs), f'margin-top:{fx(28)}') +
                 f'<div style="display:flex;flex-direction:column;gap:{fx(gap)};margin-top:{fx(56)}">{lis}</div>')
        fx0, fy, fw, fh = 44, 44, 912, 1412
        tab_h = 210
        inner = (f'<div class="flyer" style="left:{fx0}px;top:{fy}px;width:{fw}px;height:{fh - tab_h}px">'
                 f'<div class="abs" style="left:52px;top:46px">{self.brand_inline(46)}</div>'
                 f'{self.fitbox(52, 140, fw - 104, fh - tab_h - 180, parts, "start")}'
                 f'<div class="pinfoot abs" style="left:52px;bottom:30px;font-size:26px">{e(d["pin_foot"])}</div>'
                 f'{self.tabs(0, fh - tab_h, fw, tab_h, 8, 32, gone=(5,))}</div>')
        return self.page('pin', 'pin', inner, ctx)

    def brand_inline(self, size):
        return (f'<div style="display:flex;align-items:center;gap:{round(size * .27)}px">{logo_svg(size, INK, PAPER, self.p["bg"])}'
                f'<div style="font-family:{SANS};font-weight:800;font-size:{round(size * .82)}px;letter-spacing:-.04em;line-height:1">JobNow</div></div>')
