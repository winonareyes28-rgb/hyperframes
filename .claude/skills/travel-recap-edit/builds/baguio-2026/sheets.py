# sheets.py photos|videos — labelled contact sheets for shot picking
import sys, glob, os, subprocess, json
from PIL import Image, ImageDraw, ImageFont
W = os.path.dirname(os.path.abspath(__file__))
F = ImageFont.truetype(os.path.expanduser('~/.fonts/SpaceGrotesk_1.ttf'), 22)
def sheet(items, name, cols=8, tw=240, th=320):
    rows = (len(items) + cols - 1) // cols
    S = Image.new('RGB', (cols * tw, rows * (th + 28)), 'black'); d = ImageDraw.Draw(S)
    for k, (label, im) in enumerate(items):
        im = im.copy(); im.thumbnail((tw, th)); x, y = (k % cols) * tw, (k // cols) * (th + 28)
        S.paste(im, (x + (tw - im.width) // 2, y)); d.text((x + 4, y + th + 2), label, fill='yellow', font=F)
    S.save(f'{W}/sheets/{name}.jpg', quality=80)
mode = sys.argv[1]
if mode == 'photos':
    ps = sorted(glob.glob(f'{W}/photos/*.jpg'))
    for i in range(0, len(ps), 48):
        sheet([(os.path.basename(p)[:-4].replace('IMG_', ''), Image.open(p)) for p in ps[i:i + 48]], f'photos_{i // 48:02d}')
else:
    for p in sorted(glob.glob(f'{W}/proxy/*.mp4')):
        n = os.path.basename(p)[:-4]; out = f'{W}/sheets/v_{n}.jpg'
        if os.path.exists(out) or 'tmp' in n or not n.split('_')[1].startswith('IMG'): continue
        d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p], capture_output=True, text=True).stdout or 0)
        k = 8 if d < 60 else 16; items = []
        for j in range(k):
            t = d * (j + 0.5) / k; f = f'/tmp/_f.jpg'
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(t), '-i', p, '-frames:v', '1', '-vf', 'scale=480:-2', f])
            if os.path.exists(f): items.append((f'{n[3:]} {t:.1f}s', Image.open(f).copy()))
        if items: sheet(items, f'v_{n}', cols=8)
