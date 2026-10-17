"""Grab frames at given times from a video into a contact sheet. usage: frames.py video.mp4 sheet.png w h t1 t2 ..."""
import sys, subprocess, os, tempfile
from PIL import Image
src, sheet, w, h = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
ts = [float(x) for x in sys.argv[5:]]
d = tempfile.mkdtemp(dir='/tmp/claude-0/-home-claude/6dd4a10d-f91b-59ea-ab2a-f458f2b135e1/scratchpad')
ims = []
for i, t in enumerate(ts):
    p = os.path.join(d, f'{i:02d}.png')
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-ss', str(t), '-i', src, '-frames:v', '1', '-vf', f'scale={w}:{h}', p], check=True)
    ims.append(Image.open(p))
cols = min(len(ims), 6 if w > h else 11)
rows = (len(ims) + cols - 1) // cols
S = Image.new('RGB', (cols * (w + 10), rows * (h + 10)), 'white')
for i, im in enumerate(ims):
    S.paste(im, ((i % cols) * (w + 10), (i // cols) * (h + 10)))
S.save(sheet)
print(sheet)
