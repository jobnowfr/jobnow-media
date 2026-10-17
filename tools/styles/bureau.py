# -*- coding: utf-8 -*-
"""bureau: a retro computer desktop. Pastel desktop, bevelled grey windows with a coloured title
bar, pixel font, warning dialogs, the fix in a yellow tooltip, the progress in the status bar,
and the highlight drawn as selected text."""
from .base import Style, e, rich, fx, font_face, logo_svg, cv_lines, BLUE, LIME, SANS

FACE, LIGHT, SHADE, DARK = '#dcd9d0', '#ffffff', '#8d8a82', '#26251f'
PIX = "'Jersey 10', monospace"
PIXB = "'Jersey 15', monospace"


def pix(grid, colors, px):
    """ASCII pixel art -> svg. grid: list of strings, '.' transparent; px: pixel size in px."""
    h, w = len(grid), max(len(r) for r in grid)
    rects = []
    for y, row in enumerate(grid):
        x = 0
        while x < len(row):
            c = row[x]
            if c == '.':
                x += 1
                continue
            x2 = x
            while x2 + 1 < len(row) and row[x2 + 1] == c:
                x2 += 1
            rects.append(f'<rect x="{x}" y="{y}" width="{x2 - x + 1}" height="1" fill="{colors[c]}"/>')
            x = x2 + 1
    return (f'<svg viewBox="0 0 {w} {h}" shape-rendering="crispEdges" style="display:block;flex:none;width:{px * w}px;height:{px * h}px" '
            f'aria-hidden="true">{"".join(rects)}</svg>')


WARN = ["......KK......", ".....KYYK.....", ".....KYYK.....", "....KYYYYK....", "....KYKKYK....", "...KYYKKYYK...",
        "...KYYKKYYK...", "..KYYYKKYYYK..", "..KYYYKKYYYK..", ".KYYYYYYYYYYK.", ".KYYYYKKYYYYK.", "KYYYYYKKYYYYYK",
        "KKKKKKKKKKKKKK"]
INFO = ["....KKKKK....", "..KKBBBBBKK..", ".KBBBBWWBBBK.", ".KBBBBWWBBBK.", "KBBBBBBBBBBBK", "KBBBBWWWBBBBK", "KBBBBBWWBBBBK",
        "KBBBBBWWBBBBK", "KBBBBBWWBBBBK", ".KBBBBWWBBBK.", ".KBBBWWWWBBK.", "..KKBBBBBKK..", "....KKKKK...."]
QUEST = ["....KKKKK....", "..KKBBBBBKK..", ".KBBWWWWWBBK.", ".KBWWBBBWWBK.", "KBBBBBBBWWBBK", "KBBBBBBWWBBBK", "KBBBBBWWBBBBK",
         "KBBBBBWWBBBBK", "KBBBBBBBBBBBK", ".KBBBBWWBBBK.", ".KBBBBWWBBBK.", "..KKBBBBBKK..", "....KKKKK...."]
CHECK = ["...........GG", "..........GGG", ".........GGG.", "........GGG..", "GG.....GGG...", "GGG...GGG....", ".GGG.GGG.....",
         "..GGGGG......", "...GGG.......", "....G........"]
CROSS = ["RR.......RR", "RRR.....RRR", ".RRR...RRR.", "..RRR.RRR..", "...RRRRR...", "....RRR....", "...RRRRR...",
         "..RRR.RRR..", ".RRR...RRR.", "RRR.....RRR", "RR.......RR"]
CURSOR = ["K...........", "KK..........", "KWK.........", "KWWK........", "KWWWK.......", "KWWWWK......", "KWWWWWK.....",
          "KWWWWWWK....", "KWWWWWWWK...", "KWWWWWWWWK..", "KWWWWWWWWWK.", "KWWWWWWKKKKK", "KWWWKWWK....", "KWWKKWWK....",
          "KWK..KWWK...", "KK...KWWK...", "K.....KWWK..", "......KWWK..", ".......KK..."]
DOCI = ["KKKKKKKKK....", "KWWWWWWWKK...", "KWWWWWWWKWK..", "KWWWWWWWKKKK.", "KWKKKKKWWWWK.", "KWWWWWWWWWWK.", "KWKKKKKKKWWK.",
        "KWWWWWWWWWWK.", "KWKKKKKKWWWK.", "KWWWWWWWWWWK.", "KWAAAAAAAAWK.", "KWAAAAAAAAWK.", "KWWWWWWWWWWK.", "KKKKKKKKKKKK."]
FOLD = ["...KKKKK.....", "..KYYYYYK....", "KKKKKKKKKKKKK", "KYYYYYYYYYYYK", "KYYYYYYYYYYYK", "KYYYYYYYYYYYK", "KYYYYYYYYYYYK",
        "KYYYYYYYYYYYK", "KYYYYYYYYYYYK", "KKKKKKKKKKKKK"]
MIN = ["........", "........", "........", "........", "........", ".KKKKKK.", ".KKKKKK."]
MAX = ["KKKKKKKK", "KKKKKKKK", "K......K", "K......K", "K......K", "K......K", "KKKKKKKK"]
CLOSE = ["KK....KK", ".KK..KK.", "..KKKK..", "...KK...", "..KKKK..", ".KK..KK.", "KK....KK"]

OUT = f'box-shadow:inset -3px -3px 0 {DARK}, inset 3px 3px 0 {LIGHT}, inset -6px -6px 0 {SHADE}, inset 6px 6px 0 #ecebe5'
IN = f'box-shadow:inset 3px 3px 0 {SHADE}, inset -3px -3px 0 {LIGHT}, inset 6px 6px 0 {DARK}, inset -6px -6px 0 #ecebe5'


class Bureau(Style):
    key = 'bureau'
    label_case = 'sentence'
    trans_item = 'pixelize'
    palettes = [
        dict(desk='#86cfbd', t1='#a3195b', t2='#df5b9c'),   # bureau menthe, barre magenta
        dict(desk='#f4a48e', t1='#0b6e69', t2='#2aa79a'),   # bureau saumon, barre sarcelle
        dict(desk='#bcaef3', t1='#b93f0c', t2='#f29a1d'),   # bureau lilas, barre orange
        dict(desk='#f2d77c', t1='#4c1d95', t2='#7c4ae8'),   # bureau beurre, barre violette
    ]

    def fonts(self):
        return (font_face('Jersey 10', 'Jersey10.woff2', '400') + font_face('Jersey 15', 'Jersey15.woff2', '400') +
                font_face('Bricolage Grotesque', 'BricolageGrotesque.woff2', '200 800'))

    def css(self, W, H, fmt, k):
        p = self.p
        return f"""
html,body{{background:{p['desk']}}}
body{{font-family:{PIX};color:#000;-webkit-font-smoothing:none;font-weight:400}}
.bg{{position:absolute;inset:0;background:{p['desk']}}}
.hl{{background:{p['t1']};color:#fff;padding:0 .08em;box-decoration-break:clone;-webkit-box-decoration-break:clone}}
b{{font-family:{PIXB};font-weight:400}}
.win{{position:absolute;background:{FACE};{OUT};padding:6px}}
.tb{{display:flex;align-items:center;background:linear-gradient(90deg,{p['t1']},{p['t2']});color:#fff;font-family:{PIXB};white-space:nowrap;overflow:hidden;letter-spacing:.02em}}
.tb .tt{{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis}}
.tbtn{{display:flex;align-items:center;justify-content:center;background:{FACE};{OUT};flex:none}}
.sunk{{background:#fff;{IN}}}
.btn{{display:inline-flex;align-items:center;justify-content:center;background:{FACE};{OUT};font-family:{PIXB};white-space:nowrap}}
.btn.def{{outline:3px solid #000;outline-offset:0}}
.eyebrow,.kicker{{font-family:{PIXB}}}
.h1{{font-family:{PIXB};line-height:1.0;letter-spacing:.01em}}
.title{{font-family:{PIXB};line-height:1.0;letter-spacing:.01em}}
.body{{line-height:1.12;letter-spacing:.01em}}
.tip{{position:relative;background:#ffffe1;border:3px solid #000;border-radius:18px}}
.tip::before{{content:'';position:absolute;left:60px;top:-30px;border:15px solid transparent;border-bottom-color:#000}}
.tip::after{{content:'';position:absolute;left:64px;top:-21px;border:11px solid transparent;border-bottom-color:#ffffe1}}
.tip .lab{{font-family:{PIXB};display:flex;align-items:center;gap:.4em}}
.tip .txt{{line-height:1.1}}
.row{{display:flex;align-items:center}}
.row .v{{line-height:1.05}}
.row .tag{{font-family:{PIXB};flex:none}}
.status{{display:flex;gap:6px}}
.status .cell{{{IN.replace('6px 6px 0 ' + DARK, '4px 4px 0 ' + SHADE)};background:{FACE};display:flex;align-items:center;padding:0 14px;white-space:nowrap}}
.blocks{{display:flex;gap:4px}}
.blocks i{{display:block;background:{p['t1']}}}
.chk{{display:flex;align-items:center}}
.cb{{background:#fff;{IN};display:flex;align-items:center;justify-content:center;flex:none}}
.li .t{{font-family:{PIXB};line-height:1.0}}
.li .s{{line-height:1.08}}
.url{{font-family:{PIXB}}}
.foot{{font-family:{PIXB}}}
.icon{{display:flex;flex-direction:column;align-items:center;position:absolute;text-align:center}}
.icon .il{{margin-top:8px;padding:2px 8px;color:#000}}
"""

    def bg(self, fmt, tpl, ctx):
        return '<div class="bg"></div>'

    # ------------------------------------------------------------------ window chrome
    def window(self, x, y, w, h, title, inner='', icon=None, tbh=60, fs=34, z=1, extra='', status=None):
        btn = round(tbh * .66)
        btns = ''.join(f'<div class="tbtn" style="width:{round(btn * 1.12)}px;height:{btn}px;margin-left:{4 if j else 0}px">{pix(g, {"K": "#000"}, max(2, round(btn / 13)))}</div>'
                       for j, g in enumerate((MIN, MAX, CLOSE)))
        ic = f'<div style="margin-right:12px">{icon}</div>' if icon else ''
        st = ''
        if status:
            st = f'<div class="status" style="position:absolute;left:6px;right:6px;bottom:6px;height:{round(tbh * .85)}px;font-size:{round(fs * .9)}px">{status}</div>'
        return (f'<div class="win" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;z-index:{z};{extra}">'
                f'<div class="tb" style="height:{tbh}px;padding:0 8px 0 14px;font-size:{fs}px">{ic}<div class="tt">{e(title)}</div>{btns}</div>'
                f'{inner}{st}</div>')

    def frame(self, fmt, tpl, box, inner, ctx, align='center'):
        x, y, w, h = box
        title = ctx.get('wtitle', '')
        tbh, fs = (64, 44) if fmt == 'vertical' else ((54, 38) if fmt in ('wide', 'pin') else (44, 32))
        status = ctx.get('status')
        pad = 34 if fmt != 'thumb' else 22
        st_h = round(tbh * .85) + 10 if status else 0
        win = self.window(x - pad, y - pad - tbh - 6, w + 2 * pad, h + 2 * pad + tbh + 6 + st_h, title,
                          icon=ctx.get('wicon'), tbh=tbh, fs=fs, status=status, z=2)
        return win + self.fitbox(x, y, w, h, inner, align, extra='z-index:3')

    # ------------------------------------------------------------------ parts
    def logo_colors(self):
        return (BLUE, '#fff', LIME)

    def wordmark_css(self):
        return 'color:#000'

    def kind_icon(self, d, px):
        cat = d.get('category', '')
        if cat in ('erreurs', 'mythes'):
            return pix(WARN, {'K': '#000', 'Y': '#ffd23f'}, px)
        return pix(INFO, {'K': '#000', 'B': self.p['t1'], 'W': '#fff'}, px)

    def item_head(self, it, i, n, fmt, S):
        fs = S['title_long'] if len(it['title']) > 24 else S['title']
        return self.title(it['title'], fx(fs))

    def fix(self, lab, txt, fs, labfs, pad, extra=''):
        ic = pix(INFO, {'K': '#000', 'B': self.p['t1'], 'W': '#fff'}, 3)
        return (f'<div class="tip" style="padding:{pad};{extra}"><div class="lab" style="font-size:{labfs}">{ic}{e(self.lab(lab))}</div>'
                f'<div class="txt" style="font-size:{fs};margin-top:{fx(10)}">{rich(txt)}</div></div>')

    def example(self, ex, k, width, extra=''):
        fs = fx(round(42 * k))
        ck = pix(CHECK, {'G': '#1f8f3a'}, max(3, round(3.4 * k)))
        cr = pix(CROSS, {'R': '#d0281e'}, max(3, round(3.4 * k)))
        pad = f'{fx(round(14 * k))} {fx(round(20 * k))}'
        return (f'<div class="sunk" style="width:{width};padding:{fx(12)};{extra}">'
                f'<div class="row" style="gap:{fx(16)};padding:{pad};font-size:{fs}">{cr}<span class="tag">{e(self.lab(ex.get("badtag", "NON")))} :</span>'
                f'<span class="v" style="text-decoration:line-through;text-decoration-thickness:.1em">{e(ex["bad"])}</span></div>'
                f'<div class="row" style="gap:{fx(16)};padding:{pad};font-size:{fs};background:{self.p["t1"]};color:#fff">{ck}<span class="tag">{e(self.lab(ex.get("goodtag", "OUI")))} :</span>'
                f'<span class="v">{e(ex["good"])}</span></div></div>')

    def card(self, text, s, rot=0, extra=''):
        return (f'<div style="font-size:{fx(round(40 * s))};{extra}"><div style="font-family:{PIXB}">Titre de poste :</div>'
                f'<div class="sunk" style="margin-top:.3em;padding:.35em .5em;font-weight:600;white-space:nowrap;overflow:hidden">{e(text)}'
                f'<span style="display:inline-block;width:.12em;height:1em;background:#000;vertical-align:-.12em;margin-left:.06em"></span></div></div>')

    def chips(self, chips, fs, pad, gap, extra=''):
        ck = pix(CHECK, {'G': '#000'}, 3)
        cs = ''.join(f'<div class="chk" style="font-size:{fs};gap:{fx(16)}"><div class="cb" style="width:{fx(48)};height:{fx(48)}">{ck}</div>{e(c)}</div>' for c in chips)
        return f'<div style="display:flex;flex-direction:column;gap:{fx(16)};{extra}">{cs}</div>'

    def progress_cells(self, i, n, fs, label):
        total = 20
        on = round(total * (i + 1) / n)
        blocks = ''.join(f'<i style="width:14px;height:{round(fs * .9)}px;{"" if j < on else "visibility:hidden"}"></i>' for j in range(total))
        return (f'<div class="cell" style="flex:1">{e(label)}</div>'
                f'<div class="cell" style="padding:0 10px"><div class="blocks">{blocks}</div></div>')

    def progress(self, i, n, x, y, w, fmt, right=False):
        return ''

    def url(self, fs, extra=''):
        return f'<div class="url" style="font-size:{fs};{extra}">jobnow.fr</div>'

    def desk_icon(self, x, y, grid, colors, label, px=6, fs=36):
        return (f'<div class="icon" style="left:{x}px;top:{y}px;width:{len(grid[0]) * px + 80}px">{pix(grid, colors, px)}'
                f'<div class="il" style="font-size:{fs}px">{e(label)}</div></div>')

    def illus(self, x, y, s, fmt, tpl, ctx=None):
        c = dict(head='#000', accent=self.p['t1'], text='#c8c8c8', side='#3a3a3a', sidetext='#ffffff', band=self.p['t1'], bandtext='#ffffff')
        page = f'<div style="position:absolute;left:150px;top:96px;width:280px;height:396px;background:#fff;overflow:hidden">{cv_lines("side", 280, 396, c)}</div>'
        win = self.window(110, 10, 360, 520, 'Aperçu A4', '', tbh=44, fs=24, z=1)
        cur = f'<div style="position:absolute;left:350px;top:330px;z-index:3">{pix(CURSOR, {"K": "#000", "W": "#fff"}, 5)}</div>'
        inner = win + f'<div class="sunk" style="position:absolute;left:126px;top:72px;width:328px;height:444px;z-index:2"></div>' + page.replace('position:absolute;', 'position:absolute;z-index:2;', 1) + cur
        return f'<div class="illus abs" style="left:{x}px;top:{y}px;width:600px;height:540px;transform-origin:0 0;transform:scale({s})">{inner}</div>'

    def list_item(self, it, nsize, tfs, sfs, gap, sub=True):
        ck = pix(CHECK, {'G': '#000'}, 3)
        s = f'<div class="s" style="font-size:{sfs};margin-top:{fx(4)}">{rich(it["fix_short"])}</div>' if sub else ''
        return (f'<div class="li" style="display:flex;align-items:flex-start;gap:{gap}">'
                f'<div class="cb" style="width:{nsize};height:{nsize};margin-top:{fx(4)}">{ck}</div>'
                f'<div style="flex:1;min-width:0"><div class="t fw" style="font-size:{tfs}">{rich(it["short"])}</div>{s}</div></div>')

    # ------------------------------------------------------------------ metrics
    def metrics(self, fmt):
        M = super().metrics(fmt)
        if fmt == 'vertical':
            M.update(brand=(70, 92, 48, None), hook_box=(110, 420, 860, 760), item_box=(100, 330, 880, 1080),
                     title=124, title_long=112, body=64, ex_k=1.45, card_s=1.5, fix=60, fixlab=56, fixpad=(30, 36), gap_fix=70)
        elif fmt == 'wide':
            M.update(brand=(80, 40, 44, 36), brand_title=(80, 40, 44, 36), title=104, body=52, fix=50, fixlab=46, fixpad=(24, 30), kick=40)
        return M

    # ------------------------------------------------------------------ templates
    def v_hook(self, d, reveal=2):
        ctx = dict(d=d)
        n = len(d['items'])
        kick = d.get('kick', 'POINT').lower()
        big = pix(QUEST if '?' in d['v_hook'] else WARN, {'K': '#000', 'Y': '#ffd23f', 'B': self.p['t1'], 'W': '#fff'}, 9)
        vis2 = '' if reveal >= 2 else 'opacity:0;'
        parts = (f'<div style="display:flex;gap:{fx(34)};align-items:flex-start">{big}'
                 f'<div style="flex:1;min-width:0">{self.h1(d["v_hook"], fx(136))}</div></div>'
                 f'{self.body(d["v_hook_sub"], fx(66), "margin-top:" + fx(40) + ";" + vis2)}'
                 f'<div style="display:flex;justify-content:flex-end;gap:{fx(20)};margin-top:{fx(60)};{vis2}">'
                 f'<div class="btn def" style="position:relative;font-size:{fx(52)};padding:{fx(16)} {fx(34)}">Voir les {n} {kick}s'
                 f'<div style="position:absolute;right:{fx(-66)};bottom:{fx(-58)}">{pix(CURSOR, {"K": "#000", "W": "#fff"}, 6)}</div></div>'
                 f'<div class="btn" style="font-size:{fx(52)};padding:{fx(16)} {fx(34)}">Ignorer</div></div>')
        x, y, w, h = 104, 380, 872, 820
        inner = self.brand(70, 92, 48)
        inner += self.window(560, 170, 470, 300, 'CV_final_v3_OK.doc', tbh=50, fs=26, z=1)
        inner += self.desk_icon(80, 1290, DOCI, {'K': '#000', 'W': '#fff', 'A': self.p['t1']}, 'CV.pdf')
        inner += self.desk_icon(300, 1290, FOLD, {'K': '#000', 'Y': '#ffd23f'}, 'Candidatures')
        inner += self.frame('vertical', 'hook', (x, y, w, h), parts, dict(ctx, wtitle=d['eyebrow']), align='center')
        return self.page('vertical', 'hook', inner, ctx)

    def v_item(self, d, it, i, n, reveal=3):
        M = self.metrics('vertical')
        ctx = dict(d=d, it=it, i=i, n=n)
        kick = d.get('kick', 'POINT').capitalize()
        blocks = (f'<div style="display:flex;gap:{fx(28)};align-items:flex-start">{self.kind_icon(d, 7)}'
                  f'<div style="flex:1;min-width:0">{self.item_head(it, i, n, "vertical", M)}</div></div>')
        blocks += self.body(it['body_short'], fx(M['body']), f'margin-top:{fx(36)};{"" if reveal >= 2 else "opacity:0"}')
        if it.get('example'):
            blocks += self.example(it['example'], M['ex_k'], '100%', f'margin-top:{fx(40)};{"" if reveal >= 2 else "opacity:0"}')
        if it.get('card'):
            blocks += self.card(it['card'], M['card_s'], 0, f'margin-top:{fx(40)};{"" if reveal >= 2 else "opacity:0"}')
        p1, p2 = M['fixpad']
        blocks += self.fix(it.get('fixlab', 'À FAIRE'), it['fix'], fx(M['fix']), fx(M['fixlab']), f'{fx(p1)} {fx(p2)}',
                           f'margin-top:{fx(M["gap_fix"])};{"" if reveal >= 3 else "opacity:0"}')
        status = self.progress_cells(i, n, 36, f'{kick} {i + 1} sur {n}')
        inner = self.brand(*M['brand'])
        inner += self.window(600, 150, 430, 220, 'Candidatures', tbh=48, fs=24, z=1)
        inner += self.frame('vertical', 'item', M['item_box'], blocks, dict(ctx, wtitle=d['eyebrow'], status=status))
        return self.page('vertical', 'item', inner, ctx)

    def v_outro(self, d):
        ctx = dict(d=d)
        parts = (self.lockup(110, 124) + self.h1(d['cta_headline'], fx(96), f'margin-top:{fx(56)}') +
                 self.chips(d['chips'], fx(56), '', '', f'margin-top:{fx(50)}') +
                 f'<div style="display:flex;justify-content:flex-end;margin-top:{fx(60)}"><div class="btn def" style="position:relative;font-size:{fx(58)};padding:{fx(18)} {fx(38)}">Ouvrir jobnow.fr'
                 f'<div style="position:absolute;right:{fx(-66)};bottom:{fx(-58)}">{pix(CURSOR, {"K": "#000", "W": "#fff"}, 6)}</div></div></div>')
        inner = self.frame('vertical', 'outro', (110, 300, 860, 1060), parts, dict(ctx, wtitle='jobnow.fr'))
        return self.page('vertical', 'outro', inner, ctx)

    def lockup(self, size, fs, extra=''):
        return (f'<div style="display:flex;align-items:center;gap:{fx(round(size * .2))};{extra}">{self.logo(size)}'
                f'<div style="font-family:{SANS};font-weight:800;font-size:{fx(fs)};letter-spacing:-.045em;line-height:1;color:#000">JobNow</div></div>')

    def w_title(self, d):
        ctx = dict(d=d)
        big = pix(QUEST if '?' in d['w_title'] else INFO, {'K': '#000', 'B': self.p['t1'], 'W': '#fff', 'Y': '#ffd23f'}, 8)
        parts = (f'<div style="display:flex;gap:{fx(34)};align-items:flex-start">{big}<div style="flex:1;min-width:0">'
                 f'{self.h1(d["w_title"], fx(92))}{self.body(d["sub"], fx(38), "margin-top:" + fx(30))}</div></div>')
        inner = self.brand(80, 40, 44, 36)
        inner += self.illus(1290, 260, 1.05, 'wide', 'title', ctx)
        inner += self.frame('wide', 'title', (150, 260, 1020, 560), parts, dict(ctx, wtitle=d['eyebrow']), align='center')
        return self.page('wide', 'title', inner, ctx)

    def w_slide(self, d, kicker, title, body=None, fix=None, example=None, card=None, side=None, idx=None, n=None, fixlab='À FAIRE'):
        M = self.metrics('wide')
        ctx = dict(d=d, i=idx, n=n)
        blocks = (f'<div style="display:flex;gap:{fx(26)};align-items:flex-start">{self.kind_icon(d, 6)}'
                  f'<div style="flex:1;min-width:0">{self.title(title, fx(M["title"]))}</div></div>')
        if body:
            blocks += self.body(body, fx(M['body']), f'margin-top:{fx(28)}')
        if fix:
            p1, p2 = M['fixpad']
            blocks += self.fix(fixlab, fix, fx(M['fix']), fx(M['fixlab']), f'{fx(p1)} {fx(p2)}', f'margin-top:{fx(56)}')
        wide = not (example or card or side)
        w = 1500 if wide else 1000
        status = self.progress_cells(idx, n, 26, self.lab(kicker).replace(' / ', ' sur ')) if idx is not None else None
        inner = self.brand(*M['brand'])
        if example:
            inner += self.window(1200, 300, 640, 420, 'Exemple', f'<div style="position:absolute;left:30px;top:90px;width:580px">{self.example(example, 1.0, "580px")}</div>', tbh=50, fs=28, z=4)
        elif card:
            inner += self.window(1220, 330, 600, 300, 'Propriétés', f'<div style="position:absolute;left:34px;top:96px;width:530px">{self.card(card, 1.05)}</div>', tbh=50, fs=28, z=4)
        elif side == 'stack':
            inner += self.illus(1300, 250, 1.0, 'wide', 'slide', ctx)
        inner += self.frame('wide', 'slide', (140, 210, w, 680), blocks, dict(ctx, wtitle=d['eyebrow'], status=status), align='start')
        return self.page('wide', 'slide', inner, ctx)

    def w_recap(self, d, items, heading):
        ctx = dict(d=d, items=items)
        lis = ''.join(self.list_item(it, fx(48), fx(54), None, fx(22), sub=False) for it in items)
        parts = (self.title(heading, fx(100)) + f'<div style="display:flex;flex-direction:column;gap:{fx(22)};margin-top:{fx(44)}">{lis}</div>')
        inner = self.brand(80, 40, 44, 36)
        inner += self.illus(1300, 260, 1.0, 'wide', 'recap', ctx)
        inner += self.frame('wide', 'recap', (150, 210, 1040, 700), parts, dict(ctx, wtitle='Récap'), align='start')
        return self.page('wide', 'recap', inner, ctx)

    def w_outro(self, d):
        ctx = dict(d=d)
        parts = (self.lockup(100, 110) + self.h1(d['cta_headline'], fx(88), f'margin-top:{fx(40)}') +
                 f'<div style="display:flex;align-items:flex-end;justify-content:space-between;margin-top:{fx(40)}">'
                 f'{self.chips(d["chips"], fx(50), "", "")}<div class="btn def" style="font-size:{fx(52)};padding:{fx(16)} {fx(34)}">Ouvrir jobnow.fr</div></div>')
        inner = self.illus(1330, 300, 1.0, 'wide', 'outro', ctx)
        inner += self.frame('wide', 'outro', (160, 200, 1080, 700), parts, dict(ctx, wtitle='jobnow.fr'), align='center')
        return self.page('wide', 'outro', inner, ctx)

    def thumb(self, d):
        ctx = dict(d=d)
        big = pix(QUEST if '?' in d['thumb_text'] else WARN, {'K': '#000', 'Y': '#ffd23f', 'B': self.p['t1'], 'W': '#fff'}, 7)
        parts = (f'<div style="display:flex;gap:{fx(26)};align-items:flex-start">{big}'
                 f'<div style="flex:1;min-width:0">{self.h1(d["thumb_text"], fx(116), "line-height:.98")}</div></div>')
        inner = self.illus(860, 120, .8, 'thumb', 'thumb', ctx)
        inner += self.frame('thumb', 'thumb', (70, 104, 780, 470), parts, dict(ctx, wtitle=d['eyebrow']), align='center')
        inner += f'<div class="abs" style="left:720px;top:520px;z-index:5">{pix(CURSOR, {"K": "#000", "W": "#fff"}, 5)}</div>'
        inner += self.brand(900, 640, 40, 34)
        return self.page('thumb', 'thumb', inner, ctx)

    def pin(self, d):
        ctx = dict(d=d)
        n = len(d['items'])
        ts, ss, gap, hs = {3: (62, 46, 48, 112), 4: (58, 44, 40, 106), 5: (56, 42, 32, 100), 6: (50, 38, 26, 94)}.get(n, (46, 34, 20, 88))
        lis = ''.join(self.list_item(it, fx(48), fx(ts), fx(ss), fx(22)) for it in d['items'])
        parts = (self.h1(d['pin_headline'], fx(hs)) + f'<div style="display:flex;flex-direction:column;gap:{fx(gap)};margin-top:{fx(50)}">{lis}</div>')
        status = f'<div class="cell" style="flex:1">{e(d["pin_foot"])}</div>'
        inner = self.brand(60, 50, 46, None)
        inner += self.frame('pin', 'pin', (96, 230, 808, 1050), parts, dict(ctx, wtitle=d['eyebrow'], status=status), align='start')
        inner += f'<div class="abs url" style="right:60px;bottom:44px;font-size:48px">jobnow.fr</div>'
        return self.page('pin', 'pin', inner, ctx)
