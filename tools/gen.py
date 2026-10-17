"""Generate the JobNow banner as HTML.

Components are authored at the ORIGINAL YouTube-banner scale (2560x1440) and
placed on any canvas with a translate + scale wrapper, so the same parts can
render a 1:1 replica (to calibrate against the source) or the Facebook layout.
"""
import sys, json

BLUE = "#2b44f0"
LIME = "#d4f53c"
INK = "#111318"
NAVY = "#151b36"
LAV = "#cdd5ff"
GRAYL = "#dadde4"

SANS = "'Bricolage Grotesque', system-ui, sans-serif"
MONO = "'JetBrains Mono', ui-monospace, monospace"


def style(**kw):
    return "; ".join(f"{k.replace('_', '-')}: {v}" for k, v in kw.items())


# ---------------------------------------------------------------- pieces
def logo_svg():
    # doc 110x130 r18 at (0,0); bars; dot r20 at (104.5,104.5) with r30 cut-out
    return (
        '<svg width="125" height="130" viewBox="0 0 125 130" style="display: block; overflow: visible" aria-hidden="true">'
        '<defs><mask id="jn-cut" maskUnits="userSpaceOnUse" x="-10" y="-10" width="150" height="150">'
        '<rect x="-10" y="-10" width="150" height="150" fill="#fff"></rect>'
        '<circle cx="104.5" cy="104.5" r="30" fill="#000"></circle></mask></defs>'
        '<rect x="0" y="0" width="110" height="130" rx="18" fill="#fff" mask="url(#jn-cut)"></rect>'
        f'<rect x="25" y="35" width="60" height="10" rx="5" fill="{BLUE}"></rect>'
        f'<rect x="25" y="60" width="60" height="10" rx="5" fill="{BLUE}"></rect>'
        f'<rect x="25" y="85" width="39" height="10" rx="5" fill="{BLUE}"></rect>'
        f'<circle cx="104.5" cy="104.5" r="20" fill="{LIME}"></circle>'
        '</svg>'
    )


def lockup(p):
    """Logo + wordmark + divider + tagline. Frame: 1480x260, origin = orig (540,590)."""
    wm = p["wm"]
    return f'''<div style="{style(position='absolute', left='0px', top='0px', width='1480px', height='260px', display='flex', align_items='center', padding_left='27px', box_sizing='border-box')}">
<div style="{style(flex='none', width='125px', height='130px')}">{logo_svg()}</div>
<div style="{style(flex='none', margin_left=f"{p['g1']}px", font_family=SANS, font_weight='800', font_size=f"{wm['size']}px", letter_spacing=f"{wm['ls']}em", line_height='1', color='#fff', white_space='nowrap', position='relative', top=f"{wm['dy']}px")}">JobNow</div>
<div style="{style(flex='none', margin_left=f"{p['g2']}px", width='2px', height='230px', background='rgba(255,255,255,0.35)')}"></div>
<div style="{style(flex='none', margin_left=f"{p['g3']}px", display='flex', flex_direction='column', align_items='flex-start', position='relative', top=f"{p['tag_dy']}px")}">
<div style="{style(position='relative', top=f"{p['eb_dy']}px", font_family=MONO, font_weight='400', font_size=f"{p['eb_size']}px", letter_spacing=f"{p['eb_ls']}px", line_height='1', color=LAV, text_transform='uppercase', white_space='nowrap')}">Créateur de CV en français</div>
<div style="{style(margin_top=f"{p['h_mt']}px", font_family=SANS, font_weight=str(p['h_w']), font_size=f"{p['h_size']}px", letter_spacing=f"{p['h_ls']}em", line_height='1', color='#fff', white_space='nowrap')}">Un CV propre,</div>
<div style="{style(margin_top=f"{p['hl_mt']}px", margin_left=f"-{p['hl_px']}px", padding=f"{p['hl_pt']}px {p['hl_px']}px {p['hl_pb']}px {p['hl_px']}px", background=LIME, border_radius='9px', font_family=SANS, font_weight=str(p['h_w']), font_size=f"{p['h_size']}px", letter_spacing=f"{p['h_ls']}em", line_height='1', color=INK, white_space='nowrap')}">sans y passer la soirée.</div>
<div style="{style(margin_top=f"{p['f_mt']}px", font_family=MONO, font_weight='400', font_size=f"{p['f_size']}px", line_height='1', color=LAV, white_space='nowrap')}"><span style="{style(font_weight='700', color='#fff')}">jobnow.fr</span> · 14 modèles · PDF et Word</div>
</div>
</div>'''


def card():
    """Job-title input card, 445x168 (unrotated)."""
    return f'''<div style="{style(position='absolute', left='0px', top='0px', width='445px', height='168px', box_sizing='border-box', padding='28px 26px 0 26px', background='#fff', border_radius='28px', box_shadow='0 26px 50px rgba(9, 17, 92, 0.42), 0 4px 10px rgba(9, 17, 92, 0.18)')}">
<div style="{style(font_family=SANS, font_weight='600', font_size='23px', line_height='1', color='#464a55', letter_spacing='-0.005em')}">Titre de poste</div>
<div style="{style(margin_top='14px', height='70px', box_sizing='border-box', border=f'2.5px solid {BLUE}', border_radius='13px', box_shadow='0 0 0 6px #e2e6fd', display='flex', align_items='center', padding='0 0 0 18px', font_family=MONO, font_weight='500', font_size='22px', color=INK, white_space='nowrap')}">Chargée de projet marketing<span style="{style(display='inline-block', width='3px', height='30px', margin_left='3px', background=BLUE, border_radius='1px')}"></span></div>
</div>'''


def pill():
    """'Aperçu A4 en direct' chip, 300x56."""
    return f'''<div style="{style(position='absolute', left='0px', top='0px', width='300px', height='56px', box_sizing='border-box', padding='0 0 0 17px', background=INK, border_radius='28px', display='flex', align_items='center', gap='13px', box_shadow='0 18px 36px rgba(9, 17, 92, 0.40)')}">
<span style="{style(flex='none', width='14px', height='14px', border_radius='50%', background=LIME, box_shadow='0 0 0 6px rgba(212, 245, 60, 0.25)')}"></span>
<span style="{style(font_family=SANS, font_weight='600', font_size='24px', line_height='1', color='#fff', white_space='nowrap', letter_spacing='-0.01em')}">Aperçu A4 en direct</span>
</div>'''


def bar(x, y, w, h, color, r=None):
    r = h / 2 if r is None else r
    return f'<div style="{style(position="absolute", left=f"{x}px", top=f"{y}px", width=f"{w}px", height=f"{h}px", background=color, border_radius=f"{r}px")}"></div>'


def page(cx, cy, w, h, rot, inner, bg="#fff", z=1, shadow="0 34px 60px rgba(9, 17, 92, 0.45), 0 6px 14px rgba(9, 17, 92, 0.20)", radius=10):
    return (f'<div style="{style(position="absolute", left=f"{cx - w / 2:.1f}px", top=f"{cy - h / 2:.1f}px", width=f"{w}px", height=f"{h}px", transform=f"rotate({rot}deg)", background=bg, border_radius=f"{radius}px", box_shadow=shadow, overflow="hidden", z_index=str(z))}">'
            + inner + '</div>')


def stack():
    """Three tilted CV pages. Frame origin = orig (2060,500)."""
    gl = GRAYL
    back = (bar(0, 0, 108, 354, NAVY, 0)
            + f'<div style="{style(position="absolute", left="17px", top="22px", width="38px", height="38px", border_radius="50%", background="#4f5468")}"></div>'
            + bar(17, 78, 75, 7, "rgba(255,255,255,0.62)") + bar(17, 92, 57, 7, "rgba(255,255,255,0.32)")
            + bar(17, 112, 65, 7, "rgba(255,255,255,0.32)") + bar(17, 126, 49, 7, "rgba(255,255,255,0.32)")
            + bar(126, 24, 96, 12, INK, 3) + bar(126, 44, 56, 6, BLUE) + bar(126, 62, 110, 6, gl) + bar(126, 74, 96, 6, gl))
    mid = (bar(60, 21, 164, 13, INK, 3) + bar(105, 43, 75, 6, BLUE)
           + bar(16, 61, 253, 1.5, INK, 0)
           + bar(16, 77, 85, 6, BLUE) + bar(16, 91, 205, 6, gl) + bar(16, 104, 190, 6, gl)
           + bar(16, 125, 85, 6, BLUE) + bar(16, 139, 210, 6, gl) + bar(16, 152, 196, 6, gl) + bar(16, 165, 180, 6, gl)
           + bar(16, 185, 85, 6, BLUE) + bar(16, 199, 200, 6, gl))
    front = (bar(0, 0, 270, 80, BLUE, 0)
             + bar(18, 30, 176, 10, "#fff") + bar(18, 50, 112, 6, "#aab4f9")
             + bar(18, 102, 84, 6, BLUE) + bar(18, 116, 232, 6, gl) + bar(18, 129, 220, 6, gl) + bar(18, 142, 226, 6, gl)
             + bar(18, 166, 84, 6, BLUE) + bar(18, 180, 230, 6, gl) + bar(18, 193, 176, 6, gl))
    return (page(189, 243.6, 253, 354, -11, back, z=1)
            + page(298, 237.5, 285, 394, 2.7, mid, z=2)
            + page(396, 274, 270, 372, 12, front, z=3))


def thumb(cx, cy, w, h, rot, kind):
    gl = GRAYL
    lines = lambda x, y0, ws, step=11, hh=5: "".join(bar(x, y0 + i * step, wv, hh, gl) for i, wv in enumerate(ws))
    if kind == "title_blue":
        inner = bar(14, 16, 84, 8, INK, 2) + bar(14, 30, 55, 6, BLUE) + lines(14, 45, [110, 95, 104, 77])
    elif kind == "band":  # handled by color in tuple
        raise ValueError
    elif kind.startswith("band:"):
        c = kind.split(":")[1]
        inner = bar(0, 0, w, 42, c, 0) + lines(14, 54, [110, 95, 102, 75])
    elif kind.startswith("side:"):
        c = kind.split(":")[1]
        sw = round(w * 0.36)
        inner = bar(0, 0, sw, h, c, 0) + bar(sw + 10, 16, 52, 7, INK, 2) + lines(sw + 10, 30, [60, 46, 56])
    elif kind == "title_green_cols":
        inner = (bar(14, 14, 84, 8, INK, 2) + bar(14, 27, 55, 6, "#1e6b4f")
                 + lines(14, 43, [30, 24], 11) + lines(52, 43, [72, 66, 72], 11))
    elif kind.startswith("title_rule:"):
        c = kind.split(":")[1]
        inner = (bar(14, 16, 84, 8, INK, 2) + bar(14, 30, 55, 6, c) + bar(14, 45, 2.5, 26, c, 1)
                 + lines(24, 45, [96, 78, 92]))
    elif kind == "title_dense":
        inner = bar(14, 16, 84, 8, INK, 2) + lines(14, 31, [104, 96, 102, 98, 90, 100], 10)
    else:
        raise ValueError(kind)
    return page(cx, cy, w, h, rot, inner, radius=8, shadow="0 20px 34px rgba(9, 17, 92, 0.40), 0 4px 8px rgba(9, 17, 92, 0.16)")


THUMBS_LEFT = [  # orig coords relative to frame origin (150,1060)
    (100, 146, 138, 193, -3.5, "title_blue"),
    (260, 120, 140, 186, 2.5, "band:#7a1f33"),
    (409, 138, 118, 168, -2, "side:#3a3f4b"),
    (580, 132, 138, 194, 4, "title_green_cols"),
    (739, 152, 140, 193, -2.5, "title_rule:#b45d12"),
]
THUMBS_RIGHT = [  # relative to frame origin (1590,1060)
    (101, 137, 140, 187, 2, "band:#111318"),
    (260, 126, 140, 195, -3, "title_rule:#2b44f0"),
    (410, 138, 118, 168, 2, "side:#151b36"),
    (580, 135, 140, 195, -2.5, "title_dense"),
    (740, 142, 140, 186, 3, "band:#2b44f0"),
]


def thumbs(lst):
    return "".join(thumb(*t) for t in lst)


def place(inner, x, y, s, w, h, extra=""):
    """Wrapper: frame of size w x h (orig units) placed at canvas (x,y), scaled by s from its top-left."""
    return f'<div style="{style(position="absolute", left=f"{x:.1f}px", top=f"{y:.1f}px", width=f"{w}px", height=f"{h}px", transform_origin="0 0", transform=f"scale({s})")}{extra}">{inner}</div>'


def place_rot(inner, cx, cy, s, w, h, rot):
    """Wrapper for a single rotated piece centred at canvas (cx,cy)."""
    return f'<div style="{style(position="absolute", left=f"{cx - w / 2:.1f}px", top=f"{cy - h / 2:.1f}px", width=f"{w}px", height=f"{h}px", transform=f"rotate({rot}deg) scale({s})")}">{inner}</div>'


def ring(cx, cy, s):
    d = 640 * s
    bw = 110 * s
    return f'<div style="{style(position="absolute", left=f"{cx - d / 2:.1f}px", top=f"{cy - d / 2:.1f}px", width=f"{d:.1f}px", height=f"{d:.1f}px", box_sizing="border-box", border=f"{bw:.1f}px solid {LIME}", border_radius="50%")}"></div>'


def background(W, H, cell, off, line_alpha, line_w):
    g = f"rgba(255, 255, 255, {line_alpha})"
    vig = "radial-gradient(ellipse farthest-corner at 50% 50%, rgba(13, 22, 120, 0) 45%, rgba(13, 22, 120, 0.30) 69%, rgba(13, 22, 120, 0.47) 100%)"
    return style(
        position="relative", width=f"{W}px", height=f"{H}px", overflow="hidden", background_color=BLUE,
        background_image=f"{vig}, linear-gradient(90deg, {g} {line_w}px, transparent {line_w}px), linear-gradient(0deg, {g} {line_w}px, transparent {line_w}px)",
        background_size=f"100% 100%, {cell}px {cell}px, {cell}px {cell}px",
        background_position=f"0 0, {off}px 0, 0 {off}px",
    )


LOCKUP_P = dict(
    wm=dict(size=151, ls=-0.04, dy=0), g1=40, g2=61, g3=59, tag_dy=-3,
    eb_size=26, eb_ls=2.7, eb_dy=5, h_mt=27, h_w=800, h_size=50, h_ls=-0.006,
    hl_mt=4, hl_px=13, hl_pt=7, hl_pb=8, f_mt=16, f_size=30,
)


ALL_THUMBS = THUMBS_LEFT + THUMBS_RIGHT


def thumb_row(idx, gap=160):
    """A row of thumbnails picked by index from ALL_THUMBS, re-spaced every `gap` units (frame-relative)."""
    out = []
    for i, k in enumerate(idx):
        cx, cy, w, h, rot, kind = ALL_THUMBS[k]
        out.append((100 + i * gap, cy, w, h, rot, kind))
    return out


def build(layout, W, H, font_css, P=LOCKUP_P):
    L = layout
    parts = []
    if "ring" in L:
        parts.append(ring(*L["ring"][:3]))
    if "stack" in L:
        parts.append(place(stack(), *L["stack"][:3], 600, 520))
    if "thumbs_left" in L:
        parts.append(place(thumbs(THUMBS_LEFT), *L["thumbs_left"][:3], 840, 280))
    if "thumbs_right" in L:
        parts.append(place(thumbs(THUMBS_RIGHT), *L["thumbs_right"][:3], 840, 280))
    for row in L.get("rows", []):
        x, y, s, idx = row
        lst = thumb_row(idx)
        parts.append(place(thumbs(lst), x, y, s, 100 + 160 * (len(idx) - 1) + 100, 280))
    if "card" in L:
        parts.append(place_rot(card(), *L["card"][:3], 445, 168, L["card"][3] if len(L["card"]) > 3 else -5))
    if "pill" in L:
        parts.append(place_rot(pill(), *L["pill"][:3], 300, 56, L["pill"][3] if len(L["pill"]) > 3 else 3))
    if "lockup" in L:
        parts.append(place(lockup(P), *L["lockup"][:3], 1480, 260))
    bg = background(W, H, *L["grid"])
    body = f'<div style="{bg}">' + "\n".join(parts) + '</div>'
    return f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>JobNow</title>
<style>{font_css} body{{margin:0}}</style></head><body>{body}</body></html>'''


LOCAL_FONTS = """
@font-face{font-family:'Bricolage Grotesque';src:url('../fonts/node_modules/@fontsource-variable/bricolage-grotesque/files/bricolage-grotesque-latin-opsz-normal.woff2') format('woff2-variations');font-weight:200 800}
@font-face{font-family:'JetBrains Mono';src:url('../fonts/node_modules/@fontsource-variable/jetbrains-mono/files/jetbrains-mono-latin-wght-normal.woff2') format('woff2-variations');font-weight:100 800}
"""

# replica of the YouTube banner at 1:1 (for calibration)
REPLICA = dict(
    ring=(2400, 170, 1),
    stack=(2060, 500, 1),
    thumbs_left=(150, 1060, 1),
    thumbs_right=(1590, 1060, 1),
    card=(269, 656, 1),
    pill=(301.5, 868, 1),
    lockup=(540, 590, 1),
    grid=(80, 40, 0.058, 2),
)

if __name__ == "__main__":
    which = sys.argv[1]
    out = sys.argv[2]
    if which == "replica":
        html = build(REPLICA, 2560, 1440, LOCAL_FONTS)
    else:
        layout = json.loads(open(which).read())
        html = build(layout["L"], layout["W"], layout["H"], LOCAL_FONTS)
    open(out, "w").write(html)
