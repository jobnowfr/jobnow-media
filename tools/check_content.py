"""Validate a day's content file before rendering and scheduling.

usage: python3 tools/check_content.py content/YYYY-MM-DD.json
Exit code 1 with a list of problems if anything is off.
"""
import datetime, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from styles import NAMES as STYLE_NAMES, STYLES

THEME_KEYS = ['key', 'category', 'topic', 'kick', 'style', 'eyebrow', 'sub', 'v_hook', 'v_hook_sub', 'w_title',
              'thumb_text', 'pin_headline', 'pin_foot', 'cta_headline', 'chips', 'items', 'captions']
ITEM_KEYS = ['n', 'title', 'short', 'body', 'body_short', 'fix', 'fix_short', 'why']
CAPTIONS = {  # key: max length (None = no limit worth checking)
    'x': 270, 'bluesky': 300, 'threads': 500, 'linkedin': 2800, 'linkedin_comment': 600,
    'facebook_post': 3000, 'facebook_reel': 1500, 'facebook_reel_title': 90,
    'instagram_reel': 2000, 'tiktok': 2000, 'tiktok_title': 90,
    'youtube_long_title': 100, 'youtube_long_intro': 1500, 'youtube_long_outro': 1500,
    'youtube_short_title': 100, 'youtube_short_text': 1500, 'pinterest_title': 100, 'pinterest_text': 480,
}
DASHES = ['—', '–', ' - ']


def x_len(s):
    n = 0
    for ch in s:
        o = ord(ch)
        n += 1 if (o <= 4351 or 8192 <= o <= 8205 or 8208 <= o <= 8223 or 8242 <= o <= 8247) else 2
    return n


def walk_strings(obj, path=''):
    if isinstance(obj, str):
        yield path, obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield from walk_strings(v, f'{path}.{k}')
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk_strings(v, f'{path}[{i}]')


def style_problems(C):
    """Each theme needs a known style; A and B differ; no style of the previous day again."""
    out = []
    themes = C.get('themes', [])
    names = [t.get('style') for t in themes]
    for t in themes:
        st = t.get('style')
        if st not in STYLE_NAMES:
            out.append(f'{t.get("key", "?")}.style : « {st} » inconnu (choix : {", ".join(STYLE_NAMES)})')
        elif 'palette' in t and not (isinstance(t['palette'], int) and 0 <= t['palette'] < len(STYLES[st].palettes)):
            out.append(f'{t.get("key", "?")}.palette : entier entre 0 et {len(STYLES[st].palettes) - 1}, ou ne pas mettre le champ')
    if len(names) == 2 and names[0] == names[1]:
        out.append('les thèmes A et B doivent avoir deux styles différents')
    hist_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'content', 'history.json')
    try:
        day = datetime.date.fromisoformat(C.get('date', ''))
        hist = json.load(open(hist_path))
    except (ValueError, OSError):
        return out
    prev = (day - datetime.timedelta(days=1)).isoformat()
    used = {h.get('style') for h in hist if h.get('date') == prev}
    for t in themes:
        if t.get('style') in used:
            out.append(f'{t.get("key", "?")}.style : « {t["style"]} » a déjà servi la veille ({prev}), prends-en un autre (python3 tools/pick_styles.py {C["date"]})')
    return out


def main(path):
    C = json.load(open(path))
    errs = []
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', C.get('date', '')):
        errs.append('date manquante ou mal formée')
    themes = C.get('themes', [])
    if [t.get('key') for t in themes] != ['A', 'B']:
        errs.append('il faut exactement deux thèmes, clés A puis B')
    errs += style_problems(C)
    for T in themes:
        k = T.get('key', '?')
        for key in THEME_KEYS:
            if key not in T:
                errs.append(f'{k}: champ manquant {key}')
        items = T.get('items', [])
        if not 3 <= len(items) <= 7:
            errs.append(f'{k}: {len(items)} items (il en faut entre 3 et 7)')
        for i, it in enumerate(items):
            for key in ITEM_KEYS:
                if key not in it:
                    errs.append(f'{k}.items[{i}]: champ manquant {key}')
            if it.get('n') != f'{i + 1:02d}':
                errs.append(f'{k}.items[{i}]: n doit valoir {i + 1:02d}')
            if len(it.get('title', '')) > 44:
                errs.append(f'{k}.items[{i}]: titre trop long ({len(it["title"])} > 44)')
            for key, lim in (('body', 120), ('body_short', 80), ('fix', 95), ('fix_short', 55), ('short', 42), ('why', 190)):
                if len(it.get(key, '')) > lim:
                    errs.append(f'{k}.items[{i}].{key}: {len(it[key])} caractères (max {lim})')
            if 'example' in it and 'card' in it:
                errs.append(f'{k}.items[{i}]: example et card ne vont pas ensemble')
        cap = T.get('captions', {})
        for key, lim in CAPTIONS.items():
            if key not in cap:
                errs.append(f'{k}.captions: manque {key}')
            elif lim:
                n = x_len(cap[key]) if key == 'x' else len(cap[key])
                if n > lim:
                    errs.append(f'{k}.captions.{key}: {n} caractères (max {lim})')
        if 'youtube_tags' not in cap or not isinstance(cap['youtube_tags'], list):
            errs.append(f'{k}.captions: youtube_tags doit être une liste')
        if '#shorts' not in cap.get('youtube_short_title', ''):
            errs.append(f'{k}.captions.youtube_short_title: ajoute #shorts')
        for p, s in walk_strings(T):
            if s.count('[[') != s.count(']]'):
                errs.append(f'{k}{p}: surlignage [[ ]] mal fermé')
            for d in DASHES:
                if d in s:
                    errs.append(f'{k}{p}: tiret interdit {d!r}')
            if re.search(r'\bgratuit', s, re.I):
                errs.append(f'{k}{p}: « gratuit » interdit (JobNow est payant)')
    if errs:
        print('\n'.join(errs))
        sys.exit(1)
    print('OK')


if __name__ == '__main__':
    main(sys.argv[1])
