"""Render every visual for one day of JobNow posts.

usage: python3 tools/build_day.py content/YYYY-MM-DD.json

Writes to media/YYYY-MM-DD/ :
  pin_<K>.jpg      Pinterest pin (1000x1500)
  thumb_<K>.jpg    YouTube thumbnail (1280x720)
  reel_<K>.mp4     vertical video (Reels / TikTok / Shorts)
  reel_<K>_720.mp4 same video in 720x1280, attached to X, Threads, Bluesky and LinkedIn posts
  yt_<K>.mp4       long horizontal video (YouTube)
  manifest.json    file list, durations and YouTube chapters
and contact sheets for visual checking in .preview/YYYY-MM-DD/ (not committed).
Each theme is drawn in its own `style` (tools/styles/). Texts that had to be shrunk a lot to fit
are listed under "shrunk" in the output: shorten them in the content file and rebuild.
"""
import json, os, subprocess, sys, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import social as S
import music
from PIL import Image

REPO = S.ROOT
RAW = 'https://raw.githubusercontent.com/jobnowfr/jobnow-media/main'
FPS = 30
SHRINK_WARN = 0.8   # a text block drawn below 80 % of its normal size is reported


def mmss(t):
    t = int(round(t))
    return f'{t // 60}:{t % 60:02d}'


def video(T, fmt, out, seed, work, shrunk):
    n = len(T['items'])
    tr = S.get_style(T).trans_item   # transition between items, chosen by the style
    seq = []  # (html, seconds, transition into this slide, label)
    chapters = []
    if fmt == 'vertical':
        seq.append((S.v_hook(T, 1), 1.3, None, 'accroche'))
        seq.append((S.v_hook(T, 2), 2.4, ('fade', 0.25), 'accroche'))
        for i, it in enumerate(T['items']):
            seq.append((S.v_item(T, it, i, n, 1), 1.1, (tr, 0.35), f'item {i + 1}'))
            seq.append((S.v_item(T, it, i, n, 2), 2.3, ('fade', 0.22), f'item {i + 1}'))
            seq.append((S.v_item(T, it, i, n, 3), 3.0, ('fade', 0.22), f'item {i + 1}'))
        seq.append((S.v_outro(T), 3.8, (tr, 0.35), 'fin'))
    else:
        kick = T.get('kick', 'POINT')
        seq.append((S.w_title(T), 6.0, None, 'titre'))
        chapters.append((0, 'Intro'))
        seq.append((S.w_recap(T, T['items'], 'Au programme'), 8.0, ('fade', 0.5), 'au programme'))
        for i, it in enumerate(T['items']):
            start = sum(x[1] for x in seq)
            chapters.append((start, f'{kick.capitalize()} {i + 1} : {it["title"][0].lower() + it["title"][1:]}'))
            lab = f'{kick} {i + 1} / {n}'
            side = None if (it.get('example') or it.get('card')) else 'stack'
            seq.append((S.w_slide(T, lab, it['title'], body=it['why'], side='stack', idx=i, n=n), 8.5, (tr, 0.5), f'item {i + 1} (why)'))
            seq.append((S.w_slide(T, lab, it['title'], body=it['body'], fix=it['fix'], example=it.get('example'),
                                  card=it.get('card'), side=side, idx=i, n=n, fixlab=it.get('fixlab', 'À FAIRE')), 9.5, ('fade', 0.4), f'item {i + 1}'))
        chapters.append((sum(x[1] for x in seq), 'Récap'))
        seq.append((S.w_recap(T, T['items'], 'Ce qu\'il faut retenir'), 10.0, (tr, 0.5), 'récap'))
        seq.append((S.w_outro(T), 7.5, ('fade', 0.5), 'fin'))

    os.makedirs(work, exist_ok=True)
    r = S.Renderer()
    files = []
    for i, (h, d, _, label) in enumerate(seq):
        p = os.path.join(work, f'f{i:03d}.png')
        fit = r.render(h, fmt, p)
        if fit and min(float(f) for f in fit) < SHRINK_WARN:
            shrunk.append(f'{T["key"]} {fmt} {label} ({min(float(f) for f in fit):.2f})')
        files.append(p)
    r.close()

    args = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y']
    for k, p in enumerate(files):
        pad = seq[k + 1][2][1] if k + 1 < len(seq) else 0
        args += ['-loop', '1', '-framerate', str(FPS), '-t', f'{seq[k][1] + pad:.3f}', '-i', p]
    filters, prev, t_acc = [], '[0:v]', seq[0][1]
    for k in range(1, len(seq)):
        kind, td = seq[k][2]
        filters.append(f'{prev}[{k}:v]xfade=transition={kind}:duration={td}:offset={t_acc:.3f}[x{k}]')
        prev = f'[x{k}]'
        t_acc += seq[k][1]
    filters.append(f'{prev}format=yuv420p[v]')
    wav = os.path.join(work, 'music.wav')
    music.make(wav, t_acc, seed)
    args += ['-i', wav, '-filter_complex', ';'.join(filters), '-map', '[v]', '-map', f'{len(seq)}:a',
             '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-profile:v', 'high', '-r', str(FPS),
             '-c:a', 'aac', '-b:a', '160k', '-ar', '44100', '-shortest', '-movflags', '+faststart', out]
    subprocess.run(args, check=True)
    return round(t_acc, 2), chapters


def save_jpg(png, out, limit=900_000):
    """JPEG under ~900 KB (Bluesky refuses images over 1 MB): lower the quality step by step if needed."""
    im = Image.open(png).convert('RGB')
    for q in (92, 88, 84, 80, 76, 72):
        im.save(out, 'JPEG', quality=q, optimize=True)
        if os.path.getsize(out) <= limit:
            break


def small_copy(src, out):
    """720x1280 copy of a vertical video: lighter, inside every network's limits (X caps portrait video at 1900 px)."""
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', src, '-vf', 'scale=720:1280:flags=lanczos',
                    '-c:v', 'libx264', '-preset', 'medium', '-crf', '22', '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-r', str(FPS),
                    '-c:a', 'aac', '-b:a', '128k', '-ar', '44100', '-movflags', '+faststart', out], check=True)


def sheet(paths, out, w, h, cols):
    ims = [Image.open(p).convert('RGB').resize((w, h)) for p in paths]
    rows = (len(ims) + cols - 1) // cols
    s = Image.new('RGB', (cols * (w + 10), rows * (h + 10)), 'white')
    for i, im in enumerate(ims):
        s.paste(im, ((i % cols) * (w + 10), (i // cols) * (h + 10)))
    s.save(out)


def frames(src, times, w, h, work):
    out = []
    for i, t in enumerate(times):
        p = os.path.join(work, f'grab_{i:02d}.png')
        subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-ss', f'{t:.2f}', '-i', src,
                        '-frames:v', '1', '-vf', f'scale={w}:{h}', p], check=True)
        out.append(p)
    return out


def main(content_path):
    C = json.load(open(content_path))
    day = C['date']
    out_dir = os.path.join(REPO, 'media', day)
    prev_dir = os.path.join(REPO, '.preview', day)
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(prev_dir, exist_ok=True)
    seed_base = int(day.replace('-', '')) % 9973
    manifest = {'date': day, 'base_url': f'{RAW}/media/{day}', 'themes': {}}
    shrunk = []
    r = S.Renderer()
    for T in C['themes']:
        T['_date'] = day
        k = T['key']
        st = S.get_style(T)
        pin_p = os.path.join(prev_dir, f'pin_{k}.png')
        th_p = os.path.join(prev_dir, f'thumb_{k}.png')
        for html, fmt, p, label in ((S.pin(T), 'pin', pin_p, 'épingle'), (S.thumb(T), 'thumb', th_p, 'miniature')):
            fit = r.render(html, fmt, p)
            if fit and min(float(f) for f in fit) < SHRINK_WARN:
                shrunk.append(f'{k} {label} ({min(float(f) for f in fit):.2f})')
        save_jpg(pin_p, os.path.join(out_dir, f'pin_{k}.jpg'))
        save_jpg(th_p, os.path.join(out_dir, f'thumb_{k}.jpg'))
        sheet([pin_p, th_p], os.path.join(prev_dir, f'_sheet_pin_thumb_{k}.png'), 640, 720, 2)
        manifest['themes'][k] = {'style': st.key, 'palette': st.pi, 'pin': f'pin_{k}.jpg', 'thumb': f'thumb_{k}.jpg'}
    r.close()

    for i, T in enumerate(C['themes']):
        k = T['key']
        work = os.path.join(prev_dir, f'work_{k}')
        reel_s, _ = video(T, 'vertical', os.path.join(out_dir, f'reel_{k}.mp4'), seed_base + 2 * i, work + '_v', shrunk)
        small_copy(os.path.join(out_dir, f'reel_{k}.mp4'), os.path.join(out_dir, f'reel_{k}_720.mp4'))
        yt_s, chapters = video(T, 'wide', os.path.join(out_dir, f'yt_{k}.mp4'), seed_base + 2 * i + 1, work + '_w', shrunk)
        m = manifest['themes'][k]
        m.update({'reel': f'reel_{k}.mp4', 'reel_small': f'reel_{k}_720.mp4', 'reel_seconds': reel_s, 'yt': f'yt_{k}.mp4', 'yt_seconds': yt_s,
                  'chapters': [[mmss(t), lab] for t, lab in chapters]})
        n = len(T['items'])
        vt = [0.6, 3.0] + [3.7 + 6.4 * j + 5.5 for j in range(n)] + [reel_s - 1.0]
        sheet(frames(os.path.join(out_dir, f'reel_{k}.mp4'), vt, 216, 384, work + '_v'),
              os.path.join(prev_dir, f'_sheet_reel_{k}.png'), 216, 384, 8)
        wt = [3.0, 10.0] + [14 + 18 * j + 13 for j in range(n)] + [yt_s - 12, yt_s - 3]
        sheet(frames(os.path.join(out_dir, f'yt_{k}.mp4'), wt, 480, 270, work + '_w'),
              os.path.join(prev_dir, f'_sheet_yt_{k}.png'), 480, 270, 4)
        for wdir in (work + '_v', work + '_w'):
            shutil.rmtree(wdir, ignore_errors=True)

    json.dump(manifest, open(os.path.join(out_dir, 'manifest.json'), 'w'), ensure_ascii=False, indent=1)
    print(json.dumps({'out': out_dir, 'preview': prev_dir, 'shrunk': shrunk,
                      'themes': {k: {'style': v['style'], 'palette': v['palette'], 'reel_s': v['reel_seconds'], 'yt_s': v['yt_seconds']}
                                 for k, v in manifest['themes'].items()}}, ensure_ascii=False))


if __name__ == '__main__':
    main(sys.argv[1])
