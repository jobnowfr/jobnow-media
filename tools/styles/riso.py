# -*- coding: utf-8 -*-
"""riso: a two-ink risograph print. Off-white paper, one dark ink for the text and one bright ink
for shapes, halftone dot fields, grain, overprinting where the inks cross, and a slight
misregistration between the two inks."""
from .base import Style, e, rich, fx, font_face, noise, logo_svg, cv_lines, card_fs, SANS

PAPER = '#f6f4ee'
DISP = "'Syne', system-ui, sans-serif"


class Riso(Style):
    key = 'riso'
    label_case = 'sentence'
    trans_item = 'dissolve'
    palettes = [
        dict(i1='#00777e', i2='#ff48b0'),   # sarcelle + rose fluo
        dict(i1='#3f6b5c', i2='#ffe100'),   # vert chasseur + jaune
        dict(i1='#6c4fa3', i2='#ffad0f'),   # violet + tournesol
        dict(i1='#8d3f68', i2='#4fc3e3'),   # bordeaux + aqua
    ]

    def fonts(self):
        return font_face('Syne', 'Syne.woff2', '400 800') + font_face('Bricolage Grotesque', 'BricolageGrotesque.woff2', '200 800')

    def css(self, W, H, fmt, k):
        p = self.p
        dot = round(20 * k)
        return f"""
html,body{{background:{PAPER}}}
body{{font-family:{DISP};color:{p['i1']};--i1:{p['i1']};--i2:{p['i2']}}}
.bg{{position:absolute;inset:0;background:{PAPER}}}
.grain{{position:absolute;inset:0;background-image:{noise(260, .95, 2, .10)};mix-blend-mode:multiply;z-index:20;pointer-events:none}}
.speck{{position:absolute;inset:0;background-image:{noise(300, .7, 3, .35, (246, 244, 238), 9)};z-index:19;pointer-events:none;opacity:.55}}
.blob{{position:absolute;border-radius:50%;background:{p['i2']};mix-blend-mode:multiply}}
.tone{{position:absolute;background-image:radial-gradient(circle, {p['i2']} 34%, transparent 36%);background-size:{dot}px {dot}px;mix-blend-mode:multiply}}
.tone1{{position:absolute;background-image:radial-gradient(circle, {p['i1']} 26%, transparent 28%);background-size:{dot}px {dot}px;mix-blend-mode:multiply;opacity:.9}}
.hl{{background:{p['i2']};padding:0 .1em;box-decoration-break:clone;-webkit-box-decoration-break:clone}}
.h1 .hl,.title .hl{{background:linear-gradient({p['i2']},{p['i2']}) 0 62% / 100% 70% no-repeat}}
b{{font-weight:800}}
.ink{{mix-blend-mode:multiply}}
.eyebrow,.kicker{{font-weight:700;letter-spacing:.01em;display:inline-block;padding-bottom:.18em;border-bottom:.16em solid {p['i2']}}}
.h1{{font-weight:800;line-height:1.02;letter-spacing:-.025em;text-shadow:.045em .035em 0 {p['i2']};mix-blend-mode:multiply}}
.title{{font-weight:800;line-height:1.04;letter-spacing:-.02em;text-shadow:.04em .03em 0 {p['i2']};mix-blend-mode:multiply}}
.body{{font-weight:500;line-height:1.38;mix-blend-mode:multiply}}
.num{{position:relative;font-weight:800;line-height:.8;letter-spacing:-.04em;height:.82em}}
.num .a{{position:absolute;left:.05em;top:.04em;color:{p['i2']};mix-blend-mode:multiply}}
.num .b{{position:relative;color:{p['i1']};mix-blend-mode:multiply}}
.fix{{position:relative;mix-blend-mode:multiply}}
.fix .fill{{position:absolute;inset:0;background:{p['i2']}}}
.fix .fill::after{{content:'';position:absolute;inset:0;background-image:radial-gradient(circle, rgba(255,255,255,.16) 18%, transparent 20%);background-size:{round(dot * .7)}px {round(dot * .7)}px}}
.fix .line{{position:absolute;inset:0;border:{fx(4)} solid {p['i1']};transform:translate({fx(-9)},{fx(-8)})}}
.fix .lab{{position:relative;display:inline-block;background:{p['i1']};color:{PAPER};font-weight:700;padding:.12em .55em .16em;border-radius:999px}}
.fix .txt{{position:relative;font-weight:700;line-height:1.3}}
.ex{{position:relative;display:flex;align-items:center;mix-blend-mode:multiply}}
.ex.bad{{border:{fx(4)} solid {p['i1']}}}
.ex.good{{background:{p['i2']}}}
.ex.good::after{{content:'';position:absolute;inset:0;border:{fx(4)} solid {p['i1']};transform:translate({fx(7)},{fx(6)})}}
.ex .tag{{background:{p['i1']};color:{PAPER};font-weight:700;border-radius:999px;flex:none;line-height:1.1}}
.ex .v{{font-weight:700;line-height:1.22}}
.ex.bad .v{{text-decoration:line-through;text-decoration-color:{p['i2']};text-decoration-thickness:.16em}}
.chip{{border:{fx(4)} solid {p['i1']};border-radius:999px;font-weight:700;mix-blend-mode:multiply}}
.li .n{{position:relative;font-weight:800;color:{p['i1']};display:flex;align-items:center;justify-content:center;flex:none;border-radius:50%;
  border:{fx(4)} solid {p['i1']};line-height:1}}
.li .n::before{{content:'';position:absolute;inset:0;border-radius:50%;background:{p['i2']};transform:translate(14%,10%);mix-blend-mode:multiply;z-index:-1}}
.li .t{{font-weight:700;line-height:1.16;mix-blend-mode:multiply}}
.li .s{{font-weight:500;line-height:1.3;mix-blend-mode:multiply}}
.dots{{display:flex}}
.dots i{{display:block;border-radius:50%;border:{round(4 * k)}px solid {p['i1']}}}
.dots i.done{{background:{p['i2']};border-color:{p['i2']}}}
.dots i.cur{{background:{p['i1']}}}
.url{{font-weight:800;letter-spacing:-.02em;mix-blend-mode:multiply}}
.foot{{font-weight:800}}
.pinfoot{{font-weight:600}}
"""

    def bg(self, fmt, tpl, ctx):
        W, H = {'vertical': (1080, 1920), 'wide': (1920, 1080), 'thumb': (1280, 720), 'pin': (1000, 1500)}.get(fmt, (1080, 1920))
        i = ctx.get('i') or 0
        out = '<div class="bg"></div>'
        if fmt == 'vertical':
            spots = [(560, -180, 760), (-260, 120, 700), (520, 980, 820)]
            if tpl == 'hook':
                out += f'<div class="blob" style="left:420px;top:150px;width:860px;height:860px"></div>'
                out += f'<div class="tone" style="left:-40px;top:1240px;width:1160px;height:520px"></div>'
            elif tpl == 'item':
                x, y, d = spots[i % 3]
                out += f'<div class="blob" style="left:{x}px;top:{y}px;width:{d}px;height:{d}px;opacity:.9"></div>'
                out += f'<div class="tone" style="left:0;top:1480px;width:1080px;height:440px;opacity:.8"></div>'
            elif tpl == 'outro':
                out += f'<div class="blob" style="left:-200px;top:1100px;width:900px;height:900px"></div>'
                out += f'<div class="tone" style="left:560px;top:-60px;width:600px;height:600px;border-radius:50%"></div>'
        elif fmt == 'wide':
            if tpl in ('title', 'outro'):
                out += f'<div class="blob" style="left:1180px;top:120px;width:840px;height:840px"></div>'
            elif tpl == 'slide':
                out += f'<div class="blob" style="left:{1400 - (i % 2) * 80}px;top:{-260 + (i % 3) * 60}px;width:700px;height:700px;opacity:.85"></div>'
            else:
                out += f'<div class="blob" style="left:1300px;top:420px;width:760px;height:760px;opacity:.85"></div>'
            out += f'<div class="tone" style="left:0;top:0;width:1920px;height:44px;opacity:.7"></div>'
        elif fmt == 'thumb':
            out += f'<div class="blob" style="left:760px;top:-120px;width:640px;height:640px"></div>'
            out += f'<div class="tone" style="left:640px;top:612px;width:640px;height:108px"></div>'
        elif fmt == 'pin':
            out += f'<div class="blob" style="left:520px;top:-200px;width:660px;height:660px"></div>'
            out += f'<div class="tone" style="left:0;top:0;width:520px;height:40px"></div>'
        return out

    def page(self, fmt, tpl, inner, ctx=None):
        html = super().page(fmt, tpl, inner, ctx)
        return html.replace('</body>', '<div class="speck"></div><div class="grain"></div></body>')

    # ------------------------------------------------------------------ parts
    def logo_colors(self):
        return (self.p['i1'], PAPER, self.p['i2'])

    def wordmark_css(self):
        return f'color:{self.p["i1"]};mix-blend-mode:multiply'

    def eyebrow(self, s, fs, extra=''):
        return f'<div><div class="eyebrow ink" style="font-size:{fs};{extra}">{e(s)}</div></div>'

    def kicker(self, s, fs, extra=''):
        return f'<div><div class="kicker ink" style="font-size:{fs};{extra}">{e(self.lab(s))}</div></div>'

    def item_head(self, it, i, n, fmt, S):
        fs = S['title_long'] if len(it['title']) > 24 else S['title']
        k = str(int(it['n']))
        return (f'<div class="num" style="font-size:{fx(S["num"])}"><span class="a">{k}</span><span class="b">{k}</span></div>' +
                self.title(it['title'], fx(fs), f'margin-top:{fx(S["gap_num"])}'))

    def fix(self, lab, txt, fs, labfs, pad, extra=''):
        return (f'<div class="fix" style="padding:{pad};{extra}"><div class="fill"></div><div class="line"></div>'
                f'<div class="lab" style="font-size:{labfs}">{e(self.lab(lab))}</div>'
                f'<div class="txt" style="font-size:{fs};margin-top:{fx(16)}">{rich(txt)}</div></div>')

    def example(self, ex, k, width, extra=''):
        fs = fx(round(36 * k))
        pad = f'{fx(round(20 * k))} {fx(round(24 * k))}'
        tg = f'font-size:{fx(round(24 * k))};padding:{fx(round(8 * k))} {fx(round(14 * k))}'
        return (f'<div style="display:flex;flex-direction:column;gap:{fx(round(22 * k))};width:{width};{extra}">'
                f'<div class="ex bad" style="padding:{pad};gap:{fx(round(18 * k))}"><span class="tag" style="{tg}">{e(self.lab(ex.get("badtag", "NON")))}</span>'
                f'<span class="v" style="font-size:{fs}">{e(ex["bad"])}</span></div>'
                f'<div class="ex good" style="padding:{pad};gap:{fx(round(18 * k))}"><span class="tag" style="{tg}">{e(self.lab(ex.get("goodtag", "OUI")))}</span>'
                f'<span class="v" style="font-size:{fs}">{e(ex["good"])}</span></div></div>')

    def card_inner(self, text):
        p = self.p
        return (f'<div style="position:absolute;inset:0;padding:26px 26px 0;background:{PAPER};border:4px solid {p["i1"]};mix-blend-mode:multiply">'
                f'<div style="position:absolute;inset:0;border:4px solid {p["i2"]};transform:translate(9px,8px)"></div>'
                f'<div style="font-weight:700;font-size:24px;line-height:1">Titre de poste</div>'
                f'<div style="margin-top:14px;height:72px;border:4px solid {p["i1"]};display:flex;align-items:center;padding-left:18px;'
                f'font-weight:700;font-size:{card_fs(text, 27, 22)}px;white-space:nowrap">{e(text)}<span style="display:inline-block;width:5px;height:36px;margin-left:4px;background:{p["i2"]}"></span></div></div>')

    def chips(self, chips, fs, pad, gap, extra=''):
        cs = ''.join(f'<span class="chip" style="font-size:{fs};padding:{pad}">{e(c)}</span>' for c in chips)
        return f'<div style="display:flex;flex-wrap:wrap;gap:{gap};{extra}">{cs}</div>'

    def progress(self, i, n, x, y, w, fmt, right=False):
        sz = 26 if fmt == 'vertical' else 22
        ds = ''.join(f'<i class="{"done" if j < i else ("cur" if j == i else "")}" style="width:{sz}px;height:{sz}px"></i>' for j in range(n))
        pos = f'right:{x}px' if right else f'left:{x}px'
        return f'<div class="dots abs" style="{pos};top:{y}px;gap:{round(sz * .6)}px;mix-blend-mode:multiply">{ds}</div>'

    def url(self, fs, extra=''):
        return f'<div class="url" style="font-size:{fs};{extra}">jobnow.fr</div>'

    def sheet(self, x, y, w, h, rot, kind, z=1):
        p = self.p
        c = dict(head=p['i1'], accent=p['i1'], text=p['i1'], side=p['i1'], sidetext=PAPER, band=p['i2'], bandtext=p['i1'])
        lines = cv_lines(kind, w, h, c)
        return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg);z-index:{z};mix-blend-mode:multiply">'
                f'<div style="position:absolute;inset:0;background:{p["i2"]};transform:translate(14px,12px);opacity:.9"></div>'
                f'<div style="position:absolute;inset:0;background:{PAPER};border:4px solid {p["i1"]};overflow:hidden;opacity:.97">'
                f'<div style="position:absolute;inset:0;opacity:.55">{lines}</div></div></div>')

    def illus(self, x, y, s, fmt, tpl, ctx=None):
        inner = self.sheet(60, 70, 290, 400, -8, 'center', 1) + self.sheet(230, 40, 300, 420, 6, 'band', 2)
        return f'<div class="illus abs" style="left:{x}px;top:{y}px;width:600px;height:520px;transform-origin:0 0;transform:scale({s})">{inner}</div>'

    def list_item(self, it, nsize, tfs, sfs, gap, sub=True):
        s = f'<div class="s" style="font-size:{sfs};margin-top:{fx(8)}">{rich(it["fix_short"])}</div>' if sub else ''
        return (f'<div class="li" style="display:flex;align-items:{"flex-start" if sub else "center"};gap:{gap};isolation:isolate">'
                f'<div class="n" style="width:{nsize};height:{nsize};font-size:calc({nsize} * .56)">{int(it["n"])}</div>'
                f'<div style="flex:1;min-width:0"><div class="t fw" style="font-size:{tfs}">{rich(it["short"])}</div>{s}</div></div>')

    # ------------------------------------------------------------------ metrics
    def metrics(self, fmt):
        M = super().metrics(fmt)
        if fmt == 'vertical':
            M.update(brand=(80, 116, 50, None), prog=(80, 226, 0), hook_box=(80, 300, 900, 900), illus_hook=(470, 1220, .95),
                     eb=40, hook_h1=128, hook_sub=54, item_box=(80, 300, 860, 1210), num=270, gap_num=34,
                     title=104, title_long=94, body=52, ex_k=1.2, card_s=1.25, fix=50, fixlab=34, fixpad=(40, 46), gap_fix=64)
        elif fmt == 'wide':
            M.update(eb=34, w_h1=108, kick=34, title=88, body=42, fix=42, fixlab=30, fixpad=(32, 40), prog_y=96,
                     outro_box=(110, 220, 1080, 760), illus_outro=(1330, 380, .95))
        elif fmt == 'thumb':
            M.update(box=(64, 60, 760, 520), h1=108, illus=(810, 150, .85), brand=(64, 620, 50, 42))
        return M

    def thumb(self, d):
        M = self.metrics('thumb')
        ctx = dict(d=d)
        inner = self.illus(*M['illus'], 'thumb', 'thumb', ctx)
        inner += self.frame('thumb', 'thumb', M['box'], self.h1(d['thumb_text'], fx(M['h1']), 'line-height:1.0'), ctx, align='center')
        inner += self.brand(*M['brand'])
        return self.page('thumb', 'thumb', inner, ctx)
