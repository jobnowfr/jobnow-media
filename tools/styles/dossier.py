# -*- coding: utf-8 -*-
"""dossier: an application file. A coloured cardboard folder, typed sheets held by a paper clip,
rubber stamps (MYTHE / RÉALITÉ, AVANT / APRÈS...), index dividers as progress, label-maker tape
as the highlight."""
from .base import Style, e, rich, fx, font_face, noise, logo_svg, cv_lines, mix, BLUE, LIME, SANS

PAPER, INK = '#fdfdfa', '#262422'
RED, GREEN, TAPE = '#cc3426', '#24844a', '#cf2a20'
TYPE = "'Courier Prime', 'Courier New', monospace"
ELITE = "'Special Elite', 'Courier New', monospace"
STAMP = "'Anton', 'Impact', sans-serif"
GOOD_TAGS = ('RÉALITÉ', 'APRÈS', 'OUI', 'SUFFIT', 'EN VRAI', 'BIEN', 'MIEUX', 'VRAI')

# grain mask for rubber stamps: mostly opaque with uneven ink and small gaps
STAMP_MASK = ("url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240'>"
              "<filter id='m'><feTurbulence type='fractalNoise' baseFrequency='.55' numOctaves='3' seed='7' stitchTiles='stitch'/>"
              "<feColorMatrix values='0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -2.7 2.75'/></filter>"
              "<rect width='100%' height='100%' filter='url(%23m)'/></svg>\")")


def clip_svg(h, color='#8f969c'):
    w = h * .36
    return (f'<svg viewBox="0 0 36 100" style="position:absolute;width:{w:.0f}px;height:{h}px;overflow:visible" aria-hidden="true">'
            f'<path d="M24 26 V 80 a 10 10 0 0 1 -20 0 V 14 a 12 12 0 0 1 24 0 V 72 a 4 4 0 0 1 -8 0 V 24" fill="none" stroke="{color}" '
            f'stroke-width="4.2" stroke-linecap="round"/><path d="M24 26 V 80 a 10 10 0 0 1 -20 0 V 14" fill="none" stroke="rgba(255,255,255,.5)" '
            f'stroke-width="1.2" stroke-linecap="round" transform="translate(-1,-1)"/></svg>')


def plural(kick, n):
    k = kick.upper()
    return f'{n} {k}S' if n > 1 and not k.endswith('S') else f'{n} {k}'


class Dossier(Style):
    key = 'dossier'
    label_case = 'upper'
    trans_item = 'coverup'
    palettes = [
        dict(folder='#cda578', edge='#a9814f'),   # kraft
        dict(folder='#f1c84c', edge='#c99f22'),   # chemise jaune
        dict(folder='#93c99e', edge='#6aa477'),   # chemise verte
        dict(folder='#f2a9be', edge='#cf8299'),   # chemise rose
    ]

    def fonts(self):
        return (font_face('Courier Prime', 'CourierPrime-Regular.woff2', '400') + font_face('Courier Prime', 'CourierPrime-Bold.woff2', '700') +
                font_face('Special Elite', 'SpecialElite.woff2', '400') + font_face('Anton', 'Anton.woff2', '400') +
                font_face('Bricolage Grotesque', 'BricolageGrotesque.woff2', '200 800'))

    def css(self, W, H, fmt, k):
        p = self.p
        return f"""
html,body{{background:{p['folder']}}}
body{{font-family:{TYPE};color:{INK}}}
.bg{{position:absolute;inset:0;background-color:{p['folder']};
  background-image:radial-gradient(ellipse at 50% 40%, rgba(255,255,255,.10), rgba(0,0,0,.10) 100%)}}
.grain{{position:absolute;inset:0;background-image:{noise(280, .65, 4, .22, (90, 60, 20), 11)};mix-blend-mode:multiply;opacity:.55}}
.fibers{{position:absolute;inset:0;background-image:{noise(500, .012, 2, .10, (60, 40, 10), 5)};mix-blend-mode:multiply}}
.sheet{{position:absolute;background:{PAPER};box-shadow:0 2px 3px rgba(0,0,0,.12), 0 28px 50px -28px rgba(40,25,0,.55)}}
.sheet::after{{content:'';position:absolute;inset:0;background-image:{noise(300, .8, 2, .05)};mix-blend-mode:multiply;pointer-events:none}}
.hl{{background:{TAPE};color:#fff;font-family:{TYPE};font-weight:700;text-transform:uppercase;letter-spacing:.05em;font-size:.86em;
  padding:.04em .32em .02em;border-radius:.12em;box-decoration-break:clone;-webkit-box-decoration-break:clone;
  text-shadow:0 .03em 0 rgba(0,0,0,.35), 0 -.02em 0 rgba(255,255,255,.25);box-shadow:inset 0 -.06em 0 rgba(0,0,0,.18)}}
b{{font-weight:700}}
.eyebrow,.kicker{{font-family:{TYPE};font-weight:700;letter-spacing:.02em}}
.h1{{font-family:{ELITE};line-height:1.12;letter-spacing:-.01em}}
.title{{font-family:{ELITE};line-height:1.12;letter-spacing:-.01em}}
.body{{font-weight:400;line-height:1.42}}
.rule{{height:0;border-top:2px solid {INK};opacity:.75}}
.stamp{{display:inline-block;font-family:{STAMP};text-transform:uppercase;letter-spacing:.07em;color:var(--sc);line-height:1;white-space:nowrap;
  border:.085em solid var(--sc);border-radius:.14em;padding:.14em .32em .1em;outline:.035em solid var(--sc);outline-offset:-.2em;
  -webkit-mask-image:{STAMP_MASK};-webkit-mask-size:220px 220px;mix-blend-mode:multiply;opacity:.9}}
.card{{position:relative;background:#fff;box-shadow:0 2px 3px rgba(0,0,0,.12), 0 22px 30px -20px rgba(40,25,0,.5);
  background-image:linear-gradient(transparent calc(100% - 1.5px), #b9c9ea 1.5px);background-size:100% 1.5em;background-position:0 1.35em}}
.card::before{{content:'';position:absolute;left:0;right:0;top:1.3em;border-top:2.5px solid {RED};opacity:.85}}
.card .lab{{position:relative}}
.card .txt{{font-weight:700;line-height:1.5}}
.exl{{display:flex;align-items:center}}
.exl .v{{line-height:1.3}}
.exl.bad .v{{text-decoration:line-through;text-decoration-thickness:.1em;text-decoration-color:{INK}}}
.exl.good .v{{font-weight:700}}
.chk{{display:flex;align-items:baseline;font-weight:700;line-height:1.35}}
.chk i{{font-style:normal;flex:none;margin-right:.5em}}
.li .t{{font-weight:700;line-height:1.25}}
.li .s{{font-weight:400;line-height:1.35}}
.url{{font-family:{TYPE};font-weight:700}}
.foot{{font-family:{TYPE};font-weight:700}}
.label{{position:absolute;background:#fff;border-radius:10px;box-shadow:0 2px 3px rgba(0,0,0,.15), 0 14px 20px -14px rgba(0,0,0,.4)}}
.tabs{{position:absolute;display:flex;align-items:flex-end}}
.tabs .tb{{display:flex;align-items:flex-start;justify-content:center;border-radius:12px 12px 0 0;font-family:{TYPE};font-weight:700;
  box-shadow:0 -1px 2px rgba(0,0,0,.12)}}
"""

    def bg(self, fmt, tpl, ctx):
        return '<div class="bg"></div><div class="fibers"></div><div class="grain"></div>'

    # ------------------------------------------------------------------ parts
    def logo_colors(self):
        return (BLUE, '#fff', LIME)

    def wordmark_css(self):
        return f'color:{INK}'

    def brand(self, x, y, size=48, fs=None, right=False):
        fs = fs or round(size * .82)
        pos = f'right:{x}px' if right else f'left:{x}px'
        pad = round(size * .3)
        return (f'<div class="label" style="{pos};top:{y}px;padding:{pad}px {round(pad * 1.3)}px;display:flex;align-items:center;gap:{round(size * .27)}px;transform:rotate(-1.5deg)">'
                f'{self.logo(size)}<div style="font-family:{SANS};font-weight:800;font-size:{fs}px;letter-spacing:-.04em;line-height:1;color:{INK}">JobNow</div></div>')

    def stamp(self, text, fs, color=RED, rot=-7, extra=''):
        return f'<span class="stamp" style="--sc:{color};font-size:{fs};transform:rotate({rot}deg);{extra}">{e(text)}</span>'

    def eyebrow(self, s, fs, extra=''):
        return f'<div class="eyebrow" style="font-size:{fs};{extra}">Objet : {e(s)}</div>'

    def kicker(self, s, fs, extra=''):
        return f'<div class="kicker" style="font-size:{fs};{extra}">{e(s)}</div>'

    def item_head(self, it, i, n, fmt, S):
        fs = S['title_long'] if len(it['title']) > 24 else S['title']
        kick = (S.get('kick_word') or 'POINT')
        return (f'<div style="display:flex;justify-content:space-between;align-items:center">'
                f'<div class="eyebrow" style="font-size:{fx(S["head"])}">Pièce n° {int(it["n"])} / {n}</div>'
                f'{"" if it.get("example") else self.stamp(kick, fx(S["stamp"]), RED, -6)}</div>'
                f'<div class="rule" style="margin-top:{fx(18)}"></div>' +
                self.title(it['title'], fx(fs), f'margin-top:{fx(S["gap_num"])}'))

    def fix(self, lab, txt, fs, labfs, pad, extra=''):
        return (f'<div class="card" style="font-size:{fs};padding:{fx(10)} {fx(36)} {fx(26)};transform:rotate(.7deg);{extra}">'
                f'<div style="position:absolute;left:{fx(40)};top:{fx(-34)}">{clip_svg(96)}</div>'
                f'<div class="lab" style="height:1.5em;display:flex;align-items:center;justify-content:flex-end">'
                f'{self.stamp(lab, f"calc({labfs} * 1.05)", GREEN, -3, "position:relative;top:-.15em")}</div>'
                f'<div class="txt" style="margin-top:.1em">{rich(txt)}</div></div>')

    def example(self, ex, k, width, extra=''):
        fs = fx(round(36 * k))
        sfs = fx(round(36 * k))
        bad_t, good_t = ex.get('badtag', 'NON'), ex.get('goodtag', 'OUI')
        gcol = GREEN if good_t.upper() in GOOD_TAGS or True else RED
        sw = fx(round(240 * k))
        return (f'<div style="display:flex;flex-direction:column;gap:{fx(round(22 * k))};width:{width};{extra}">'
                f'<div class="exl bad" style="gap:{fx(round(22 * k))}"><div style="width:{sw};flex:none;text-align:center">{self.stamp(bad_t, sfs, RED, -8)}</div>'
                f'<span class="v" style="font-size:{fs}">{e(ex["bad"])}</span></div>'
                f'<div class="exl good" style="gap:{fx(round(22 * k))}"><div style="width:{sw};flex:none;text-align:center">{self.stamp(good_t, sfs, gcol, 5)}</div>'
                f'<span class="v" style="font-size:{fs}">{e(ex["good"])}</span></div></div>')

    def card(self, text, s, rot=-1, extra=''):
        """A form field: 'Titre de poste' with the typed value on a dotted line."""
        return (f'<div style="font-size:{fx(round(34 * s))};padding:{fx(26)} {fx(30)};border:2px solid {INK};background:#fff;{extra}">'
                f'<div style="font-weight:700;letter-spacing:.02em">Titre de poste :</div>'
                f'<div style="margin-top:.35em;padding-bottom:.15em;border-bottom:3px dotted {INK};font-family:{ELITE};font-size:1.25em;line-height:1.25">{e(text)}</div></div>')

    def chips(self, chips, fs, pad, gap, extra=''):
        cs = ''.join(f'<div class="chk" style="font-size:{fs}"><i>[x]</i><span>{e(c)}</span></div>' for c in chips)
        return f'<div style="display:flex;flex-direction:column;gap:{fx(10)};{extra}">{cs}</div>'

    def progress(self, i, n, x, y, w, fmt, right=False):
        tw, th = (118, 64) if fmt == 'vertical' else (96, 52)
        tabs = ''
        for j in range(n):
            cur = j == i
            bgc = PAPER if cur else (mix(PAPER, self.p['folder'], .35) if j < i else mix(self.p['edge'], '#ffffff', .25))
            tabs += (f'<div class="tb" style="width:{tw}px;height:{th + (10 if cur else 0)}px;background:{bgc};font-size:{round(th * .5)}px;'
                     f'padding-top:{round(th * .14)}px;margin-right:6px">{j + 1}</div>')
        pos = f'right:{x}px' if right else f'left:{x}px'
        return f'<div class="tabs" style="{pos};top:{y - 10}px;height:{th + 10}px">{tabs}</div>'

    def url(self, fs, extra=''):
        return f'<div class="url" style="font-size:{fs};{extra}">jobnow.fr</div>'

    def cv_sheet(self, x, y, w, h, rot, kind, z=1):
        c = dict(head=INK, accent=RED, text='#cfccc6', side='#3b3734', sidetext='#ffffff', band=self.p['edge'], bandtext='#ffffff')
        return (f'<div class="sheet" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg);z-index:{z}">'
                f'{cv_lines(kind, w, h, c)}</div>')

    def illus(self, x, y, s, fmt, tpl, ctx=None):
        inner = (self.cv_sheet(70, 60, 290, 400, -7, 'center', 1) + self.cv_sheet(230, 40, 300, 420, 5, 'side', 2) +
                 f'<div style="position:absolute;left:300px;top:6px;z-index:3">{clip_svg(120)}</div>' +
                 f'<div style="position:absolute;left:250px;top:330px;z-index:4">{self.stamp("CV", "64px", RED, -12)}</div>')
        return f'<div class="illus abs" style="left:{x}px;top:{y}px;width:600px;height:520px;transform-origin:0 0;transform:scale({s})">{inner}</div>'

    def list_item(self, it, nsize, tfs, sfs, gap, sub=True):
        s = f'<div class="s" style="font-size:{sfs};margin-top:{fx(6)}">{rich(it["fix_short"])}</div>' if sub else ''
        return (f'<div class="li" style="display:flex;align-items:baseline;gap:{gap}">'
                f'<div style="font-weight:700;font-size:{tfs};flex:none">[{int(it["n"])}]</div>'
                f'<div style="flex:1;min-width:0"><div class="t fw" style="font-size:{tfs}">{rich(it["short"])}</div>{s}</div></div>')

    # ------------------------------------------------------------------ frame: a typed sheet with a clip
    def frame(self, fmt, tpl, box, inner, ctx, align='center'):
        x, y, w, h = box
        if tpl in ('thumb',):
            return self.fitbox(x, y, w, h, inner, align)
        px, pt, pb = (56, 76, 70) if fmt in ('vertical', 'pin') else (50, 60, 56)
        rot = {'hook': -.8, 'item': .4, 'outro': -.6, 'title': -.5, 'slide': .3, 'recap': -.4, 'pin': .3}.get(tpl, 0)
        sheet = (f'<div class="sheet" style="left:{x - px}px;top:{y - pt}px;width:{w + 2 * px}px;height:{h + pt + pb}px;transform:rotate({rot}deg)">'
                 f'<div style="position:absolute;{"right:120px" if fmt in ("vertical", "pin") else "left:60px"};top:-40px">{clip_svg(120 if fmt != "wide" else 100)}</div></div>')
        return sheet + self.fitbox(x, y, w, h, inner, align, extra=f'transform:rotate({rot}deg)')

    # ------------------------------------------------------------------ metrics
    def metrics(self, fmt):
        M = super().metrics(fmt)
        if fmt == 'vertical':
            M.update(brand=(70, 96, 46, None), prog=(124, 222, 0), hook_box=(126, 330, 800, 1030), illus_hook=(560, 1390, .7),
                     eb=40, hook_h1=104, hook_sub=46, item_box=(126, 350, 812, 1110), head=38, stamp=56, num=0, gap_num=34,
                     title=88, title_long=80, body=44, ex_k=1.15, card_s=1.15, fix=44, fixlab=40, gap_fix=60,
                     outro_box=(126, 260, 812, 1180), lock=(110, 120), cta=70, chip=44, url=60)
        elif fmt == 'wide':
            M.update(brand=(90, 52, 44, 36), brand_title=(90, 52, 44, 36), prog_x=110, prog_y=74, prog_w=0,
                     title_box=(150, 250, 1020, 640), eb=32, w_h1=92, w_sub=36, illus_title=(1290, 280, 1.05),
                     slide_top=230, slide_w=1000, slide_w_full=1520, slide_h=700, kick=32, title=74, body=36,
                     fix=36, fixlab=34, side_ex=(1250, 360, 560, 1.0), side_card=(1250, 420, 1.0), illus_slide=(1300, 300, 1.0),
                     recap_box=(150, 220, 1040, 740), illus_recap=(1300, 320, 1.0), outro_box=(150, 230, 1100, 720),
                     illus_outro=(1320, 330, 1.0), foot=(150, 50, 28))
        elif fmt == 'thumb':
            M.update(box=(84, 84, 700, 470), h1=96, illus=(820, 120, .82), brand=(60, 612, 42, 34))
        elif fmt == 'pin':
            M.update(brand=(60, 52, 44, None), box=(110, 230, 780, 1090), eb=30)
        return M

    # ------------------------------------------------------------------ templates that differ
    def v_hook(self, d, reveal=2):
        M = self.metrics('vertical')
        ctx = dict(d=d)
        n = len(d['items'])
        parts = (self.eyebrow(d['eyebrow'], fx(M['eb'])) + f'<div class="rule" style="margin-top:{fx(18)}"></div>' +
                 self.h1(d['v_hook'], fx(M['hook_h1']), f'margin-top:{fx(44)}') +
                 self.body(d['v_hook_sub'], fx(M['hook_sub']), f'margin-top:{fx(44)};{"" if reveal >= 2 else "opacity:0"}') +
                 f'<div style="margin-top:{fx(70)};{"" if reveal >= 2 else "opacity:0"}">{self.stamp(plural(d.get("kick", "POINT"), n), fx(120), RED, -9)}</div>')
        inner = self.brand(*M['brand'])
        inner += self.illus(*M['illus_hook'], 'vertical', 'hook', ctx)
        inner += self.frame('vertical', 'hook', M['hook_box'], parts, ctx, align='start')
        return self.page('vertical', 'hook', inner, ctx)

    def v_item(self, d, it, i, n, reveal=3):
        M = dict(self.metrics('vertical'), kick_word=d.get('kick', 'POINT'))
        ctx = dict(d=d, it=it, i=i, n=n)
        blocks = self.item_head(it, i, n, 'vertical', M)
        blocks += self.body(it['body_short'], fx(M['body']), f'margin-top:{fx(34)};{"" if reveal >= 2 else "opacity:0"}')
        if it.get('example'):
            blocks += self.example(it['example'], M['ex_k'], '100%', f'margin-top:{fx(44)};{"" if reveal >= 2 else "opacity:0"}')
        if it.get('card'):
            blocks += self.card(it['card'], M['card_s'], 0, f'margin-top:{fx(40)};{"" if reveal >= 2 else "opacity:0"}')
        blocks += self.fix(it.get('fixlab', 'À FAIRE'), it['fix'], fx(M['fix']), fx(M['fixlab']), '',
                           f'margin-top:{fx(M["gap_fix"])};{"" if reveal >= 3 else "opacity:0"}')
        inner = self.brand(*M['brand']) + self.progress(i, n, *M['prog'], 'vertical')
        inner += self.frame('vertical', 'item', M['item_box'], blocks, ctx)
        return self.page('vertical', 'item', inner, ctx)

    def v_outro(self, d):
        M = self.metrics('vertical')
        ctx = dict(d=d)
        lsz, lfs = M['lock']
        parts = (self.lockup(lsz, lfs) + f'<div class="rule" style="margin-top:{fx(34)}"></div>' +
                 self.h1(d['cta_headline'], fx(M['cta']), f'margin-top:{fx(44)}') +
                 self.chips(d['chips'], fx(M['chip']), '', '', f'margin-top:{fx(50)}') +
                 f'<div style="margin-top:{fx(70)}">{self.stamp("jobnow.fr", fx(110), RED, -6)}</div>')
        inner = self.frame('vertical', 'outro', M['outro_box'], parts, ctx)
        return self.page('vertical', 'outro', inner, ctx)

    def lockup(self, size, fs, extra=''):
        return (f'<div style="display:flex;align-items:center;gap:{fx(round(size * .2))};{extra}">{self.logo(size)}'
                f'<div style="font-family:{SANS};font-weight:800;font-size:{fx(fs)};letter-spacing:-.045em;line-height:1;color:{INK}">JobNow</div></div>')

    def w_slide(self, d, kicker, title, body=None, fix=None, example=None, card=None, side=None, idx=None, n=None, fixlab='À FAIRE'):
        M = self.metrics('wide')
        ctx = dict(d=d, i=idx, n=n)
        head = (f'<div style="display:flex;justify-content:space-between;align-items:center">'
                f'<div class="kicker" style="font-size:{fx(M["kick"])}">Pièce n° {idx + 1} / {n}</div>'
                f'{self.stamp(d.get("kick", "POINT"), fx(48), RED, -5) if not example else ""}</div>'
                f'<div class="rule" style="margin-top:{fx(14)}"></div>') if idx is not None else self.kicker(kicker, fx(M['kick']))
        blocks = head + self.title(title, fx(M['title']), f'margin-top:{fx(26)}')
        if body:
            blocks += self.body(body, fx(M['body']), f'margin-top:{fx(28)}')
        if fix:
            blocks += self.fix(fixlab, fix, fx(M['fix']), fx(M['fixlab']), '', f'margin-top:{fx(50)}')
        width = M['slide_w'] if (example or card or side) else M['slide_w_full']
        inner = self.brand(*M['brand'])
        if idx is not None:
            inner += self.progress(idx, n, 1810 - n * 102, 78, 0, 'wide')
        inner += self.w_side(example, card, side, ctx)
        inner += self.frame('wide', 'slide', (150, M['slide_top'], width, M['slide_h']), blocks, ctx, align='start')
        return self.page('wide', 'slide', inner, ctx)

    def w_side(self, example, card, side, ctx):
        M = self.metrics('wide')
        if example:
            x, y, w, k = M['side_ex']
            return (f'<div class="sheet" style="left:{x - 40}px;top:{y - 50}px;width:{w + 80}px;height:330px;transform:rotate(2deg)"></div>'
                    f'<div class="abs" style="left:{x}px;top:{y + 10}px;width:{w}px;transform:rotate(2deg)">{self.example(example, k, f"{w}px")}</div>')
        if card:
            x, y, s = M['side_card']
            return f'<div class="abs" style="left:{x}px;top:{y}px;width:560px;transform:rotate(2deg)">{self.card(card, s)}</div>'
        if side == 'stack':
            return self.illus(*M['illus_slide'], 'wide', 'slide', ctx)
        return ''

    def w_recap(self, d, items, heading):
        M = self.metrics('wide')
        ctx = dict(d=d, items=items)
        lis = ''.join(self.list_item(it, None, fx(40), None, fx(20), sub=False) for it in items)
        parts = (self.kicker('Récapitulatif', fx(32)) + f'<div class="rule" style="margin-top:{fx(14)}"></div>' +
                 self.title(heading, fx(76), f'margin-top:{fx(26)}') +
                 f'<div style="display:flex;flex-direction:column;gap:{fx(22)};margin-top:{fx(44)}">{lis}</div>')
        inner = self.brand(*M['brand'])
        inner += self.illus(*M['illus_recap'], 'wide', 'recap', ctx)
        inner += self.frame('wide', 'recap', M['recap_box'], parts, ctx, align='start')
        return self.page('wide', 'recap', inner, ctx)

    def w_title(self, d):
        M = self.metrics('wide')
        ctx = dict(d=d)
        n = len(d['items'])
        parts = (self.eyebrow(d['eyebrow'], fx(M['eb'])) + f'<div class="rule" style="margin-top:{fx(14)}"></div>' +
                 self.h1(d['w_title'], fx(M['w_h1']), f'margin-top:{fx(34)}') +
                 self.body(d['sub'], fx(M['w_sub']), f'margin-top:{fx(30)}') +
                 f'<div style="margin-top:{fx(40)}">{self.stamp(plural(d.get("kick", "POINT"), n), fx(84), RED, -6)}</div>')
        inner = self.brand(*M['brand_title'])
        inner += self.illus(*M['illus_title'], 'wide', 'title', ctx)
        inner += self.frame('wide', 'title', M['title_box'], parts, ctx, align='start')
        return self.page('wide', 'title', inner, ctx)

    def w_outro(self, d):
        M = self.metrics('wide')
        ctx = dict(d=d)
        parts = (self.lockup(100, 110) + f'<div class="rule" style="margin-top:{fx(28)}"></div>' +
                 self.h1(d['cta_headline'], fx(68), f'margin-top:{fx(36)}') +
                 f'<div style="display:flex;align-items:center;justify-content:space-between;margin-top:{fx(40)}">'
                 f'{self.chips(d["chips"], fx(36), "", "")}{self.stamp("jobnow.fr", fx(84), RED, -7, "margin-right:" + fx(30))}</div>')
        inner = self.illus(*M['illus_outro'], 'wide', 'outro', ctx)
        inner += self.frame('wide', 'outro', M['outro_box'], parts, ctx, align='center')
        return self.page('wide', 'outro', inner, ctx)

    def thumb(self, d):
        M = self.metrics('thumb')
        ctx = dict(d=d)
        n = len(d['items'])
        x, y, w, h = M['box']
        inner = self.illus(*M['illus'], 'thumb', 'thumb', ctx)
        inner += f'<div class="sheet" style="left:{x - 40}px;top:{y - 44}px;width:{w + 80}px;height:{h + 80}px;transform:rotate(-1deg)"></div>'
        inner += self.fitbox(x, y, w, h, self.h1(d['thumb_text'], fx(M['h1']), 'line-height:1.08'), 'center', extra='transform:rotate(-1deg)')
        inner += f'<div class="abs" style="left:560px;top:572px">{self.stamp(plural(d.get("kick", "POINT"), n), "58px", RED, -6)}</div>'
        inner += self.brand(*M['brand'])
        return self.page('thumb', 'thumb', inner, ctx)

    def pin(self, d):
        M = self.metrics('pin')
        ctx = dict(d=d)
        n = len(d['items'])
        ts, ss, gap, hs = {3: (40, 32, 52, 76), 4: (38, 31, 44, 72), 5: (36, 29, 36, 70), 6: (33, 27, 28, 66)}.get(n, (30, 25, 22, 62))
        lis = ''.join(self.list_item(it, None, fx(ts), fx(ss), fx(18)) for it in d['items'])
        parts = (self.eyebrow(d['eyebrow'], fx(M['eb'])) + f'<div class="rule" style="margin-top:{fx(14)}"></div>' +
                 self.h1(d['pin_headline'], fx(hs), f'margin-top:{fx(30)}') +
                 f'<div style="display:flex;flex-direction:column;gap:{fx(gap)};margin-top:{fx(50)}">{lis}</div>' +
                 f'<div style="margin-top:{fx(40)};font-size:{fx(28)}">{e(d["pin_foot"])}</div>')
        inner = self.brand(*M['brand'])
        inner += self.frame('pin', 'pin', M['box'], parts, ctx, align='start')
        inner += f'<div class="abs" style="right:70px;bottom:60px">{self.stamp("jobnow.fr", "70px", RED, -7)}</div>'
        return self.page('pin', 'pin', inner, ctx)
