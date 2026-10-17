# -*- coding: utf-8 -*-
"""JobNow social templates: HTML slides rendered to PNG with Playwright.

The look comes from the theme's `style` (tools/styles/). Formats:
  pin       1000x1500 (Pinterest)
  vertical  1080x1920 (Reels / TikTok / Shorts)
  wide      1920x1080 (YouTube long video)
  thumb     1280x720  (YouTube thumbnail)
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import styles
from styles.base import ROOT, FORMATS

get_style = styles.get


def v_hook(d, reveal=2):
    return get_style(d).v_hook(d, reveal)


def v_item(d, it, i, n, reveal=3):
    return get_style(d).v_item(d, it, i, n, reveal)


def v_outro(d):
    return get_style(d).v_outro(d)


def w_title(d):
    return get_style(d).w_title(d)


def w_slide(d, *a, **kw):
    return get_style(d).w_slide(d, *a, **kw)


def w_recap(d, items, heading):
    return get_style(d).w_recap(d, items, heading)


def w_outro(d):
    return get_style(d).w_outro(d)


def thumb(d):
    return get_style(d).thumb(d)


def pin(d):
    return get_style(d).pin(d)


# First shrink any .fw block whose words are wider than its column, then shrink each [data-fit]
# box's --f until its content fits the box height.
FIT_JS = """() => {
  for (const el of document.querySelectorAll('[data-fit] .fw')) {
    const fs0 = parseFloat(getComputedStyle(el).fontSize);
    for (let i = 0; i < 40 && el.scrollWidth > el.clientWidth + 2; i++) {
      el.style.fontSize = (parseFloat(getComputedStyle(el).fontSize) * 0.96).toFixed(2) + 'px';
      el.dataset.w = (parseFloat(el.style.fontSize) / fs0).toFixed(3);
    }
  }
  return Array.from(document.querySelectorAll('[data-fit]')).map(box => {
    const inner = box.firstElementChild;
    let f = 1;
    for (let i = 0; inner && i < 60 && inner.offsetHeight > box.clientHeight + 1; i++) { f *= 0.97; box.style.setProperty('--f', f.toFixed(4)); }
    for (const el of box.querySelectorAll('.fw[data-w]')) f = Math.min(f, parseFloat(el.dataset.w));
    return f.toFixed(3);
  });
}"""


class Renderer:
    def __init__(self):
        from playwright.sync_api import sync_playwright
        self._p = sync_playwright().start()
        self.b = self._p.chromium.launch()
        self.pages = {}
        self.last_fit = []

    def render(self, html_str, fmt, out_path):
        W, H = FORMATS[fmt]
        if fmt not in self.pages:
            self.pages[fmt] = self.b.new_page(viewport={'width': W, 'height': H})
        pg = self.pages[fmt]
        tmp = out_path + '.html'
        with open(tmp, 'w') as f:
            f.write(html_str)
        pg.goto('file://' + tmp)
        pg.evaluate('document.fonts.ready')
        self.last_fit = pg.evaluate(FIT_JS)
        pg.wait_for_timeout(60)
        pg.screenshot(path=out_path, clip={'x': 0, 'y': 0, 'width': W, 'height': H})
        os.remove(tmp)
        return self.last_fit

    def close(self):
        self.b.close()
        self._p.stop()
