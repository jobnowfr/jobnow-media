"""Suggest the two visual styles of a day: the least recently used ones, never yesterday's.

usage: python3 tools/pick_styles.py YYYY-MM-DD
prints e.g. {"A": "cahier", "B": "bureau"} plus when each style was last used.
"""
import datetime, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from styles import NAMES, DESCRIPTIONS

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def pick(day, hist):
    d = datetime.date.fromisoformat(day)
    prev = (d - datetime.timedelta(days=1)).isoformat()
    last = {n: '0000-00-00' for n in NAMES}
    for h in hist:
        st = h.get('style')
        if st in last and h.get('date', '') < day:
            last[st] = max(last[st], h['date'])
    banned = {h.get('style') for h in hist if h.get('date') == prev}
    order = NAMES[d.toordinal() % len(NAMES):] + NAMES[:d.toordinal() % len(NAMES)]   # tie-break rotates with the date
    ranked = sorted((n for n in order if n not in banned), key=lambda n: last[n])
    return ranked[:2], last


if __name__ == '__main__':
    day = sys.argv[1]
    hist = json.load(open(os.path.join(REPO, 'content', 'history.json')))
    (a, b), last = pick(day, hist)
    print(json.dumps({'A': a, 'B': b}, ensure_ascii=False))
    for n in NAMES:
        print(f'  {n:8s} dernier usage {last[n] if last[n] != "0000-00-00" else "jamais":10s}  {DESCRIPTIONS[n]}')
