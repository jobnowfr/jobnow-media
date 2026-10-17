"""Turn a day's content + manifest into the exact Metricool payloads to schedule.

usage: python3 tools/plan_posts.py content/YYYY-MM-DD.json  > /tmp/plan.json
       python3 tools/plan_posts.py --medias YYYY-MM-DD            (which visual goes with which text post)

Prints a JSON list of {"slot", "network", "date", "info"} where `info` is the string to pass
as the `info` argument of createScheduledPost (blogId 7430673), and `date` the `date` argument.
Theme A fills the morning / midday slots, theme B the afternoon / evening slots.

The text networks (X, Threads, Bluesky, LinkedIn, the Facebook post) usually carry a visual too:
the Reel (720p copy), the YouTube thumbnail or the Pinterest infographic, rotating with the date,
with about one post in five left as plain text.
"""
import datetime, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TZ = 'Europe/Paris'
OFFSET = {'summer': '+02:00', 'winter': '+01:00'}

# (time, network, format) per theme. Instagram: Reels only (no feed posts), 11 posts per theme, 22 per day.
SLOTS = {
    'A': [('10:00', 'facebook', 'post'), ('10:00', 'youtube', 'long'),
          ('11:00', 'linkedin', 'post'), ('12:00', 'bluesky', 'post'), ('12:00', 'tiktok', 'video'),
          ('12:30', 'twitter', 'post'), ('12:30', 'instagram', 'reel'), ('12:30', 'facebook', 'reel'),
          ('13:00', 'threads', 'post'), ('13:00', 'pinterest', 'pin'), ('14:00', 'youtube', 'short')],
    'B': [('16:00', 'youtube', 'long'), ('17:00', 'linkedin', 'post'),
          ('18:00', 'facebook', 'post'), ('18:00', 'tiktok', 'video'), ('18:30', 'youtube', 'short'),
          ('19:00', 'twitter', 'post'), ('19:00', 'instagram', 'reel'), ('19:00', 'facebook', 'reel'),
          ('19:30', 'bluesky', 'post'), ('20:00', 'threads', 'post'), ('20:30', 'pinterest', 'pin')],
}
PINTEREST_BOARD = 'Modèles de CV'

# Visual attached to each text post, by network. Index = (day ordinal + 0 for A / 2 for B) % 5.
# 'reel' = vertical video, 'thumb' = 16:9 image with the hook, 'pin' = tall infographic, None = text only.
# Each position has exactly one None across networks, so every day has one text-only post per theme.
MEDIA_CYCLE = {
    'twitter': ['thumb', 'reel', None, 'pin', 'reel'],
    'threads': [None, 'pin', 'reel', 'reel', 'thumb'],
    'bluesky': ['reel', 'thumb', 'pin', 'pin', None],
    'linkedin': ['thumb', 'reel', 'pin', None, 'pin'],
    'facebook': ['thumb', None, 'pin', 'thumb', 'pin'],   # the Facebook text post; the Reel is a separate post
}
MEDIA_LABEL = {'reel': 'vidéo (le Reel)', 'thumb': 'image (la miniature)', 'pin': "image (l'infographie de l'épingle)", None: 'texte seul'}


def media_kind(day, key, net, m=None):
    cyc = MEDIA_CYCLE.get(net)
    if not cyc:
        return None
    o = datetime.date.fromisoformat(day).toordinal()
    kind = cyc[(o + (0 if key == 'A' else 2)) % len(cyc)]
    if kind == 'reel' and net == 'bluesky' and m and m.get('reel_seconds', 0) > 59:
        kind = 'pin'   # Bluesky (via Metricool) takes videos up to 60 s
    return kind


def plain(s):
    return re.sub(r'\s+', ' ', re.sub(r'\*\*|\[\[|\]\]', '', s)).strip()


def attach(info, kind, url, m, T):
    """Add the chosen visual (and its alt text) to a text post."""
    if kind == 'reel':
        info['media'] = [f'{url}/{m.get("reel_small", m["reel"])}']
        info['mediaAltText'] = [None]
    elif kind == 'thumb':
        info['media'] = [f'{url}/{m["thumb"]}']
        info['mediaAltText'] = [f'Visuel JobNow : {plain(T["thumb_text"])}'[:400]]
    elif kind == 'pin':
        steps = ' ; '.join(f'{int(it["n"])}. {plain(it["short"])}' for it in T['items'])
        info['media'] = [f'{url}/{m["pin"]}']
        info['mediaAltText'] = [f'Infographie JobNow : {plain(T["pin_headline"])}. {steps}'[:900]]
    return info


def offset_for(day):
    """Europe/Paris offset: CEST between the last Sunday of March and the last Sunday of October."""
    import datetime as dt
    y, m, d = map(int, day.split('-'))
    date = dt.date(y, m, d)

    def last_sunday(month):
        x = dt.date(y, month, 31)
        return x - dt.timedelta(days=(x.weekday() + 1) % 7)
    return OFFSET['summer'] if last_sunday(3) <= date < last_sunday(10) else OFFSET['winter']


def base(text, network, day, hhmm, media=None):
    return {'autoPublish': True, 'descendants': [], 'draft': False, 'firstCommentText': '', 'hasNotReadNotes': False,
            'media': media or [], 'mediaAltText': [], 'providers': [{'network': network}],
            'publicationDate': {'dateTime': f'{day}T{hhmm}:00', 'timezone': TZ},
            'shortener': False, 'smartLinkData': {'ids': []}, 'text': text}


def print_medias(day):
    for key in ('A', 'B'):
        print(f'Thème {key} : ' + ', '.join(f'{net} = {MEDIA_LABEL[media_kind(day, key, net)]}' for net in MEDIA_CYCLE))


def main(path):
    C = json.load(open(path))
    day = C['date']
    M = json.load(open(os.path.join(REPO, 'media', day, 'manifest.json')))
    url = M['base_url']
    off = offset_for(day)
    out = []
    for T in C['themes']:
        k, cap, m = T['key'], T['captions'], M['themes'][T['key']]
        for hhmm, net, fmt in SLOTS[k]:
            if net == 'facebook' and fmt == 'post':
                info = attach(base(cap['facebook_post'], net, day, hhmm), media_kind(day, k, 'facebook', m), url, m, T)
                info['facebookData'] = {'type': 'POST'}
            elif net == 'facebook' and fmt == 'reel':
                info = base(cap['facebook_reel'], net, day, hhmm, [f'{url}/{m["reel"]}'])
                info['facebookData'] = {'type': 'REEL', 'title': cap['facebook_reel_title']}
            elif net == 'instagram' and fmt == 'reel':
                info = base(cap['instagram_reel'], net, day, hhmm, [f'{url}/{m["reel"]}'])
                info['instagramData'] = {'type': 'REEL', 'showReelOnFeed': True, 'isAiGenerated': False}
            elif net == 'youtube' and fmt == 'long':
                chapters = '\n'.join(f'{t} {lab}' for t, lab in m['chapters'])
                desc = f'{cap["youtube_long_intro"]}\n\n{chapters}\n\n{cap["youtube_long_outro"]}'
                info = base(desc, net, day, hhmm, [f'{url}/{m["yt"]}'])
                info['videoThumbnailUrl'] = f'{url}/{m["thumb"]}'
                info['youtubeData'] = {'title': cap['youtube_long_title'], 'type': 'video', 'privacy': 'public',
                                       'tags': cap['youtube_tags'], 'category': 'EDUCATION', 'madeForKids': False,
                                       'isAiGeneratedContent': False}
            elif net == 'youtube' and fmt == 'short':
                info = base(cap['youtube_short_text'], net, day, hhmm, [f'{url}/{m["reel"]}'])
                info['youtubeData'] = {'title': cap['youtube_short_title'], 'type': 'short', 'privacy': 'public',
                                       'tags': cap['youtube_tags'], 'category': 'EDUCATION', 'madeForKids': False,
                                       'isAiGeneratedContent': False}
            elif net == 'tiktok':
                info = base(cap['tiktok'], net, day, hhmm, [f'{url}/{m["reel"]}'])
                info['tiktokData'] = {'title': cap['tiktok_title'], 'disableComment': False, 'disableDuet': False,
                                      'disableStitch': False, 'privacyOption': 'PUBLIC_TO_EVERYONE',
                                      'commercialContentThirdParty': False, 'commercialContentOwnBrand': True,
                                      'autoAddMusic': False, 'isAigc': False}
            elif net == 'pinterest':
                info = base(cap['pinterest_text'], net, day, hhmm, [f'{url}/{m["pin"]}'])
                info['pinterestData'] = {'boardId': PINTEREST_BOARD, 'pinTitle': cap['pinterest_title'],
                                         'pinLink': 'https://jobnow.fr', 'pinNewFormat': True}
            elif net == 'linkedin':
                info = attach(base(cap['linkedin'], net, day, hhmm), media_kind(day, k, net, m), url, m, T)
                info['firstCommentText'] = cap.get('linkedin_comment', '')
                info['linkedinData'] = {'type': 'post', 'previewIncluded': True, 'publishImagesAsPDF': False}
            elif net == 'twitter':
                info = attach(base(cap['x'], net, day, hhmm), media_kind(day, k, net, m), url, m, T)
                info['twitterData'] = {'tags': []}
            elif net == 'bluesky':
                info = attach(base(cap['bluesky'], net, day, hhmm), media_kind(day, k, net, m), url, m, T)
                info['blueskyData'] = {'postLanguages': ['fr']}
            elif net == 'threads':
                info = attach(base(cap['threads'], net, day, hhmm), media_kind(day, k, net, m), url, m, T)
                info['threadsData'] = {}
            else:
                raise ValueError((net, fmt))
            kind = media_kind(day, k, net, m) if (net, fmt) != ('facebook', 'reel') else 'reel'
            out.append({'slot': f'{k} {hhmm} {net} {fmt}' + (f' + {kind}' if net in MEDIA_CYCLE and fmt != 'reel' and kind else ''),
                        'network': net, 'date': f'{day}T{hhmm}:00{off}',
                        'info': json.dumps(info, ensure_ascii=False)})
    out.sort(key=lambda x: x['date'])
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    if sys.argv[1] == '--medias':
        print_medias(sys.argv[2])
    else:
        main(sys.argv[1])
