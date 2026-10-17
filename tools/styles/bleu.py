# -*- coding: utf-8 -*-
"""bleu: the original JobNow look (brand blue grid, lime highlights, Bricolage + JetBrains Mono)."""
from .base import Style, BLUE, LIME, INK, LAV, SANS, MONO


class Bleu(Style):
    key = 'bleu'
    trans_item = 'slideleft'

    def css(self, W, H, fmt, k):
        cell = round(60 * k)
        return f"""
html,body{{background:{BLUE}}}
body{{font-family:{SANS};color:#fff}}
.bg{{position:absolute;inset:0;background-color:{BLUE};
  background-image:radial-gradient(ellipse farthest-corner at 50% 45%, rgba(13,22,120,0) 40%, rgba(13,22,120,.32) 72%, rgba(13,22,120,.5) 100%),
  linear-gradient(90deg, rgba(255,255,255,.06) 1px, transparent 1px), linear-gradient(0deg, rgba(255,255,255,.06) 1px, transparent 1px);
  background-size:100% 100%, {cell}px {cell}px, {cell}px {cell}px; background-position:0 0, {cell // 2}px 0, 0 {cell // 2}px}}
.hl{{background:{LIME};color:{INK};padding:0 .16em;border-radius:.14em;box-decoration-break:clone;-webkit-box-decoration-break:clone}}
b{{color:#fff;font-weight:700}}
.eyebrow,.kicker{{font-family:{MONO};letter-spacing:.14em;color:{LAV};text-transform:uppercase}}
.kicker{{color:{LIME}}}
.h1{{font-weight:800;letter-spacing:-.035em;line-height:1.04}}
.num{{font-family:{MONO};font-weight:700;color:{LIME};line-height:1}}
.title{{font-weight:800;letter-spacing:-.03em;line-height:1.06}}
.body{{font-weight:500;color:#e3e8ff;line-height:1.38;letter-spacing:-.005em}}
.fix{{background:{LIME};color:{INK};border-radius:{round(26 * k)}px}}
.fix .lab{{font-family:{MONO};font-weight:700;letter-spacing:.14em;opacity:.85}}
.fix .txt{{font-weight:700;letter-spacing:-.015em;line-height:1.28}}
.ex{{border-radius:{round(20 * k)}px;display:flex;align-items:center}}
.ex.bad{{background:rgba(10,16,80,.45);color:#c9cff5;border:2px solid rgba(255,255,255,.14)}}
.ex.good{{background:#fff;color:{INK}}}
.ex .tag{{font-family:{MONO};font-weight:700;letter-spacing:.1em;border-radius:999px;flex:none}}
.ex.bad .tag{{background:rgba(255,255,255,.12);color:#fff}}
.ex.good .tag{{background:{BLUE};color:#fff}}
.ex .v{{font-weight:600;line-height:1.25}}
.ex.bad .v{{text-decoration:line-through;text-decoration-thickness:3px;text-decoration-color:rgba(255,255,255,.55)}}
.chip{{border:2px solid rgba(255,255,255,.35);border-radius:999px;font-family:{MONO};color:#fff}}
.li .n{{font-family:{MONO};font-weight:700;color:{INK};background:{LIME};border-radius:999px;display:flex;align-items:center;justify-content:center;flex:none}}
.li .t{{font-weight:700;letter-spacing:-.02em;line-height:1.18}}
.li .s{{font-weight:500;color:#dfe4ff;line-height:1.3}}
.progress i{{display:block;height:{round(8 * k)}px;border-radius:9px;background:rgba(255,255,255,.25)}}
.progress i.on{{background:{LIME}}}
.url{{font-family:{MONO};font-weight:700;color:#fff}}
.foot{{font-family:{MONO};font-weight:700;color:#fff}}
.pinfoot{{font-family:{MONO};color:{LAV}}}
"""
