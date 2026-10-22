# engine.py — travel-recap-edit renderer (beat grid -> shots -> base -> composite -> mux)
# usage: python3 engine.py plan.py [--preview] [--only-base] [--from-base]
import os, sys, math, json, random, subprocess, importlib.util
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

W = os.path.dirname(os.path.abspath(__file__))
FPS, WD, HT = 30, 1080, 1920
FONT = {k: os.path.expanduser(f'~/.fonts/{v}') for k, v in dict(
    anton='Anton_1.ttf', bebas='BebasNeue_1.ttf', archivo='ArchivoBlack_1.ttf',
    play='PlayfairDisplay_1.ttf', playi='PlayfairDisplay_2.ttf', pacifico='Pacifico_1.ttf',
    unb='Unbounded_1.ttf', caveat='CaveatBrush_1.ttf', marker='PermanentMarker_1.ttf',
    grotesk='SpaceGrotesk_1.ttf').items()}
RED, YELLOW, WHITE = (229, 38, 43), (255, 210, 31), (255, 255, 255)
GRADE = ('colorbalance=rs=-0.05:gs=0.0:bs=0.06:rm=0.02:rh=0.07:gh=0.02:bh=-0.05,'
         'eq=contrast=1.07:saturation=1.06:gamma=0.98')
FIX = {'night': 'hqdn3d=3:3:6:6,eq=brightness=0.04:gamma=1.12',
       'dim': 'eq=brightness=0.03:gamma=1.06', 'flat': 'eq=contrast=1.08:saturation=1.08',
       'purple': 'colorbalance=rs=-0.06:bs=-0.08:rm=-0.04:bm=-0.06', '': ''}


def sh(cmd, **kw):
    r = subprocess.run(cmd, **kw)
    if r.returncode: raise SystemExit(f'failed: {cmd if isinstance(cmd, str) else " ".join(cmd)}')
    return r


# ---------------------------------------------------------------- beat grid
class Grid:
    """Output timeline built from the real beat times of each song excerpt."""
    def __init__(self, sections):
        self.sections, self.t0 = [], 0.0
        import librosa
        for s in sections:
            y, sr = librosa.load(f"{W}/songs/{s['song']}", sr=22050)
            _, bt = librosa.beat.beat_track(y=y, sr=sr, units='time')
            bt = [b for b in bt if s['start'] - 0.05 <= b <= s['end'] + 0.05]
            beats = [self.t0 + b - bt[0] for b in bt]
            self.sections.append(dict(s, beats=beats, offset=self.t0, a0=bt[0], a1=bt[-1]))
            self.t0 += bt[-1] - bt[0]
        self.total = self.t0

    def t(self, sec, b):
        """time of fractional beat b inside section sec"""
        bs = self.sections[sec]['beats']; i = min(int(b), len(bs) - 2); f = b - i
        if b >= len(bs) - 1: i, f = len(bs) - 2, b - (len(bs) - 2)
        return bs[i] + f * (bs[i + 1] - bs[i])

    def f(self, sec, b): return round(self.t(sec, b) * FPS)


# ---------------------------------------------------------------- shot segments
def cover_vf(cx=0.5, cy=0.5, zoom=1.0):
    return (f"scale={int(WD*zoom)}:{int(HT*zoom)}:force_original_aspect_ratio=increase:flags=lanczos,"
            f"crop={WD}:{HT}:(iw-{WD})*{cx}:(ih-{HT})*{cy}")


def render_photo(shot, n, out):
    im = ImageOps.exif_transpose(Image.open(f"{W}/photos/{shot['src']}.jpg")).convert('RGB')
    s = max(WD / im.width, HT / im.height) * 1.15
    if s > 1: im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    z0, z1 = shot.get('kb', (1.0, 1.07)); cx, cy = shot.get('cx', 0.5), shot.get('cy', 0.5)
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{WD}x{HT}',
                          '-r', str(FPS), '-i', '-', '-vf', f"{FIX[shot.get('fix', '')] + ',' if shot.get('fix') else ''}{GRADE},format=yuv420p",
                          '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '16', out], stdin=subprocess.PIPE)
    s0 = min(im.width / WD, im.height / HT)  # largest 9:16 box that fits the photo
    for k in range(n):
        e = k / max(1, n - 1); e = e * e * (3 - 2 * e)
        z = z0 + (z1 - z0) * e; bw, bh = WD * s0 / z, HT * s0 / z
        x0 = (im.width - bw) * cx; y0 = (im.height - bh) * cy
        fr = im.crop((int(x0), int(y0), int(x0 + bw), int(y0 + bh))).resize((WD, HT), Image.BILINEAR)
        p.stdin.write(fr.tobytes())
    p.stdin.close(); p.wait()


def render_shot(shot, n, out):
    kind = shot.get('kind', 'video')
    if kind == 'black' or kind == 'scatter':
        sh(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', f'color=black:s={WD}x{HT}:r={FPS}', '-frames:v', str(n),
            '-c:v', 'libx264', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', out]); return
    if kind == 'photo': return render_photo(shot, n, out)
    src = f"{W}/proxy/{shot['src']}.mp4"; sp = shot.get('speed', 1.0)
    vf = [f"setpts=PTS/{sp}" if sp != 1 else None, f"fps={FPS}",
          cover_vf(shot.get('cx', 0.5), shot.get('cy', 0.5), shot.get('zoom', 1.0)),
          FIX[shot.get('fix', '')] or None, 'unsharp=5:5:0.5', GRADE]
    if shot.get('push'):  # slow push-in across the shot (motivated, not idle)
        z = shot['push']; vf.append(f"scale=w='{WD}*(1+{z}*n/{n})':h=-2:eval=frame,crop={WD}:{HT}")
    if 'bw' in shot: vf.append(f"hue=s=0:enable='lt(t,{shot['bw'] / FPS:.3f})'")
    if shot.get('hflip'): vf.append('hflip')
    vf.append('format=yuv420p')
    sh(['ffmpeg', '-v', 'error', '-y', '-ss', str(shot.get('ss', 0)), '-i', src, '-vf', ','.join(v for v in vf if v),
        '-frames:v', str(n), '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '16', out])
    got = int(subprocess.run(['ffprobe', '-v', 'error', '-count_frames', '-select_streams', 'v', '-show_entries',
                              'stream=nb_read_frames', '-of', 'csv=p=0', out], capture_output=True, text=True).stdout.strip() or 0)
    if got < n:  # source ran out: freeze-pad the tail
        sh(['ffmpeg', '-v', 'error', '-y', '-i', out, '-vf', f'tpad=stop_mode=clone:stop={n - got}', '-frames:v', str(n),
            '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '16', out + '.pad.mp4'])
        os.replace(out + '.pad.mp4', out)


# ---------------------------------------------------------------- text helpers
_fc = {}
def font(name, size):
    k = (name, size)
    if k not in _fc: _fc[k] = ImageFont.truetype(FONT[name], size)
    return _fc[k]


def text_img(txt, name, size, color, track=0, stroke=0):
    f = font(name, size)
    widths = [f.getlength(c) for c in txt]; tw = int(sum(widths) + track * (len(txt) - 1)) + 4 * size // 10
    asc, desc = f.getmetrics(); im = Image.new('RGBA', (max(1, tw), asc + desc + size // 5), (0, 0, 0, 0))
    d = ImageDraw.Draw(im); x = size // 5
    for c, w in zip(txt, widths):
        d.text((x, size // 10), c, font=f, fill=color + (255,), stroke_width=stroke, stroke_fill=(0, 0, 0, 255)); x += w + track
    return im.crop(im.getbbox() or (0, 0, 1, 1))


def fit_size(txt, name, maxw, start):
    s = start
    while s > 20 and font(name, s).getlength(txt) > maxw: s -= 4
    return s


def paste_c(canvas, im, cx, cy, alpha=1.0):
    if alpha < 1: im = im.copy(); im.putalpha(im.getchannel('A').point(lambda a: int(a * alpha)))
    canvas.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))


# ---------------------------------------------------------------- compositor effects
_rembg = None
def person_mask(rgb):
    global _rembg
    from rembg import remove, new_session
    if _rembg is None: _rembg = new_session('u2net_human_seg')
    small = Image.fromarray(rgb).resize((540, 960))
    m = remove(small, session=_rembg, only_mask=True).resize((WD, HT), Image.BILINEAR)
    return m.filter(ImageFilter.GaussianBlur(1.5))


def motion_blur(a, px, vertical=False):
    if px < 2: return a
    acc = np.zeros(a.shape, np.float32); k = 8
    for i in range(k):
        acc += np.roll(a, int((i / (k - 1) - 0.5) * px), axis=0 if vertical else 1)
    return (acc / k).astype(np.uint8)


def rotate_cover(a, deg, zoom=1.0):
    im = Image.fromarray(a); s = 1.0 + abs(math.sin(math.radians(deg))) * 0.9 + (zoom - 1)
    im = im.resize((int(WD * s), int(HT * s)), Image.BILINEAR).rotate(deg, Image.BILINEAR)
    x, y = (im.width - WD) // 2, (im.height - HT) // 2
    return np.asarray(im.crop((x, y, x + WD, y + HT)))


def apply_event(ev, k, fr, canvas_rgba, ctx):
    """ev: dict with f0, f1, type. k = frame index. fr = np rgb frame (may be replaced). returns fr."""
    t, n = k - ev['f0'], ev['f1'] - ev['f0']; u = t / max(1, n - 1)
    typ = ev['type']
    if typ == 'whip':  # straddles a cut: blur ramps up to the cut then down
        c = ev['cut']; dist = abs(k - c + 0.5); px = ev.get('px', 260) * max(0, 1 - dist / 3.5)
        sh_ = int(ev.get('dir', 1) * (60 if k < c else -60) * max(0, 1 - dist / 3.5))
        fr = np.roll(motion_blur(fr, px, ev.get('vertical', False)), sh_, axis=0 if ev.get('vertical') else 1)
    elif typ == 'spin':
        c = ev['cut']; x = (k - c + 0.5) / 4.0; deg = ev.get('deg', 35) * (1 - min(1, abs(x))) ** 2 * (1 if x < 0 else -1)
        fr = motion_blur(rotate_cover(fr, deg), abs(deg) * 3)
    elif typ == 'zoomthrough':
        c = ev['cut']; x = (k - c + 0.5) / 4.0; z = 1 + 0.35 * (1 - min(1, abs(x))) ** 2
        fr = np.asarray(Image.fromarray(fr).resize((int(WD * z), int(HT * z)), Image.BILINEAR).crop(
            (int((WD * z - WD) / 2), int((HT * z - HT) / 2), int((WD * z - WD) / 2) + WD, int((HT * z - HT) / 2) + HT)))
    elif typ == 'flash':
        a = ev.get('peak', 1.0) * (1 - u) ** 1.6
        fr = (fr * (1 - a) + 255 * a).astype(np.uint8)
    elif typ == 'letterbox':
        e = min(1, u * 1.05); e = e * e; h = int(HT / 2 * e)
        fr = fr.copy(); fr[:h] = 0; fr[HT - h:] = 0
    elif typ == 'fadeblack':
        fr = (fr * (1 - u)).astype(np.uint8)
    elif typ == 'fadein':
        fr = (fr * min(1, u)).astype(np.uint8)
    elif typ == 'card':  # T18 picture-in-picture card pop
        im = ctx['photo'](ev['src'], 640); pop = min(1, t / 4); s = 0.85 + 0.15 * (1 - (1 - pop) ** 3)
        im = im.resize((int(im.width * s), int(im.height * s)))
        canvas_rgba.alpha_composite(im, ((WD - im.width) // 2, int(HT * ev.get('y', 0.2))))
    elif typ == 'scatter':  # T16 photos at seeded positions, one per step
        rnd = random.Random(ev.get('seed', 3)); step = ev['step']
        for i, src in enumerate(ev['srcs']):
            x, y, r = rnd.randint(60, WD - 460), rnd.randint(160, HT - 700), rnd.uniform(-9, 9)
            if t >= i * step:
                im = ctx['photo'](src, 400).rotate(r, expand=True)
                canvas_rgba.alpha_composite(im, (x, y))
    elif typ == 'text':  # generic text: words appear at their own frame offsets
        for it in ev['items']:
            if it.get('at', 0) <= t < it.get('until', 10 ** 6):
                im = ctx['text'](it); a = min(1, (t - it.get('at', 0) + 1) / it.get('fade', 1))
                if it.get('blink') and t >= it['blink'][0] and ((t - it['blink'][0]) // it['blink'][1]) % 2:
                    im = ctx['text'](dict(it, txt=it['txt'] + '_'))
                    paste_c(canvas_rgba, im, it.get('x', WD / 2) + (im.width - ctx['text'](it).width) / 2, it.get('y', HT * 0.4), a)
                    continue
                paste_c(canvas_rgba, im, it.get('x', WD / 2), it.get('y', HT * 0.4), a)
    elif typ == 'fontcycle':  # T2: place name swaps typeface every `step` frames, then locks
        fonts = ev['fonts']; i = min(len(fonts) - 1, t // ev['step']); nm = fonts[i]
        sz = fit_size(ev['txt'], nm, WD - 120, ev.get('size', 260))
        paste_c(canvas_rgba, ctx['text'](dict(txt=ev['txt'], font=nm, size=sz, color=ev['color'], shadow=ev.get('shadow', 0))), WD / 2, ev.get('y', HT * 0.42))
        if ev.get('kicker'):
            paste_c(canvas_rgba, ctx['text'](dict(txt=ev['kicker'], font='playi', size=64, color=WHITE, shadow=ev.get('shadow', 0))), WD / 2,
                    ev.get('y', HT * 0.42) - sz * 0.62 - 20)
    elif typ == 'typeon':  # T7 / T5 letter reveal (order shuffled for scatter)
        word, nm, sz = ev['txt'], ev.get('font', 'anton'), ev.get('size', 300)
        f = font(nm, sz); total = f.getlength(word); x0 = (WD - total) / 2; order = list(range(len(word)))
        if ev.get('scatter'): random.Random(7).shuffle(order)
        layer = Image.new('RGBA', (WD, HT), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
        for rank, i in enumerate(order):
            a = max(0, min(1, (t - rank * ev.get('gap', 3)) / 3))
            if a > 0: d.text((x0 + f.getlength(word[:i]), ev.get('y', HT * 0.3)), word[i], font=f, fill=ev['color'] + (int(255 * a),))
        if ev.get('behind'): ctx['behind'].append(layer)
        else: canvas_rgba.alpha_composite(layer)
    elif typ == 'behind':  # T6 text behind subject (+ T21 silhouette flash)
        it = ev['item']; im = ctx['text'](it); layer = Image.new('RGBA', (WD, HT), (0, 0, 0, 0))
        a = min(1, (t + 1) / it.get('fade', 1)); paste_c(layer, im, it.get('x', WD / 2), it.get('y', HT * 0.42), a)
        ctx['behind'].append(layer); ctx['silhouette'] = ctx['silhouette'] or (ev.get('flash') is not None and ev['flash'] <= t < ev['flash'] + 2)
    elif typ == 'hud':  # T22 corner tags
        for (txt1, txt2), (x, y, anchor) in zip(ev['tags'], [(54, 120, 'l'), (WD - 54, 120, 'r')]):
            for j, tx in enumerate((txt1, txt2)):
                im = ctx['text'](dict(txt=tx, font='grotesk' if j == 0 else 'anton', size=30 if j == 0 else 44,
                                      color=ev.get('color', RED), track=4 if j == 0 else 2))
                xx = x if anchor == 'l' else x - im.width
                canvas_rgba.alpha_composite(im, (int(xx), y + j * 42))
        if ev.get('bottom'):
            im = ctx['text'](dict(txt=ev['bottom'], font='grotesk', size=28, color=WHITE, track=10))
            paste_c(canvas_rgba, im, WD / 2, HT - 140, 0.85)
    elif typ == 'grid':  # T23 rule-of-thirds grid
        d = ImageDraw.Draw(canvas_rgba); a = int(200 * (1 if (t // 4) % 2 == 0 or t < 8 else 0.6))
        for i in (1, 2):
            d.line([(WD * i // 3, 0), (WD * i // 3, HT)], fill=(255, 255, 255, a), width=3)
            d.line([(0, HT * i // 3), (WD, HT * i // 3)], fill=(255, 255, 255, a), width=3)
    elif typ == 'border':  # T23 thick red border pulse
        d = ImageDraw.Draw(canvas_rgba); w = 26 if (t // 3) % 2 == 0 else 16
        d.rectangle([w // 2, w // 2, WD - w // 2, HT - w // 2], outline=RED + (255,), width=w)
    elif typ == 'counter':  # small running clock / date stamp
        im = ctx['text'](dict(txt=ev['fmt'](k), font='grotesk', size=30, color=WHITE, track=6))
        paste_c(canvas_rgba, im, WD / 2, ev.get('y', HT - 140), 0.9)
    return fr


# ---------------------------------------------------------------- main pipeline
def main():
    plan_path = sys.argv[1]; preview = '--preview' in sys.argv
    spec = importlib.util.spec_from_file_location('plan', plan_path); P = importlib.util.module_from_spec(spec); spec.loader.exec_module(P)
    G = Grid(P.SECTIONS)
    shots, events = P.build(G)
    # continuity check: every shot must start where the previous ended
    for a, b in zip(shots, shots[1:]):
        assert a['f1'] == b['f0'], f"gap/overlap at {a} -> {b}"
    total = shots[-1]['f1']; print(f'{len(shots)} shots, {total} frames = {total / FPS:.2f}s (audio {G.total:.2f}s)')
    seg = f'{W}/segments'; os.makedirs(seg, exist_ok=True)
    if '--from-base' not in sys.argv:
        from concurrent.futures import ThreadPoolExecutor
        def job(i):
            s = shots[i]; out = f'{seg}/{i:03d}.mp4'
            key = json.dumps({k: v for k, v in s.items()}, sort_keys=True, default=str)
            if os.path.exists(out) and os.path.exists(out + '.key') and open(out + '.key').read() == key: return
            render_shot(s, s['f1'] - s['f0'], out); open(out + '.key', 'w').write(key)
        list(ThreadPoolExecutor(4).map(job, range(len(shots))))
        with open(f'{seg}/list.txt', 'w') as fh:
            for i in range(len(shots)): fh.write(f"file '{seg}/{i:03d}.mp4'\n")
        sh(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{seg}/list.txt', '-c', 'copy', f'{W}/base.mp4'])
    if '--only-base' in sys.argv: return
    # audio: song excerpts back to back, 12 ms crossfade at the switch, fade out at end
    parts = []
    for i, s in enumerate(G.sections):
        parts += ['-ss', f"{s['a0']:.3f}", '-t', f"{s['a1'] - s['a0'] + (0.012 if i < len(G.sections) - 1 else 0):.3f}", '-i', f"{W}/songs/{s['song']}"]
    fc = ''.join(f'[{i}:a]' for i in range(len(G.sections)))
    xf = '[0:a][1:a]acrossfade=d=0.012:c1=tri:c2=tri[a]' if len(G.sections) == 2 else f'{fc}concat=n={len(G.sections)}:v=0:a=1[a]'
    end = total / FPS; tail = P.TAIL_FADE
    sh(['ffmpeg', '-v', 'error', '-y', *parts, '-filter_complex', f'{xf};[a]atrim=0:{end:.3f},afade=t=out:st={end - tail:.3f}:d={tail},loudnorm=I=-14:TP=-1.0[o]',
        '-map', '[o]', '-ar', '48000', '-c:a', 'aac', '-b:a', '256k', f'{W}/audio.m4a'])
    # composite
    photo_cache, text_cache = {}, {}
    def photo(src, w):
        k = (src, w)
        if k not in photo_cache:
            im = ImageOps.exif_transpose(Image.open(f'{W}/photos/{src}.jpg')).convert('RGB'); im.thumbnail((w, w * 2))
            pad = Image.new('RGBA', (im.width + 24, im.height + 24), (255, 255, 255, 255)); pad.paste(im, (12, 12))
            photo_cache[k] = pad
        return photo_cache[k]
    def text(it):
        k = json.dumps(it, sort_keys=True, default=str)
        if k not in text_cache:
            im = text_img(it['txt'], it.get('font', 'anton'), it.get('size', 200), tuple(it.get('color', WHITE)), it.get('track', 0))
            if it.get('shadow'):  # soft drop shadow so titles read over busy frames
                pad = max(12, im.height // 6); sh_ = Image.new('RGBA', (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
                blk = Image.new('RGBA', im.size, (0, 0, 0, 0)); blk.putalpha(im.getchannel('A').point(lambda a: int(a * 0.75)))
                sh_.alpha_composite(blk, (pad, pad + pad // 4)); sh_ = sh_.filter(ImageFilter.GaussianBlur(pad / 2.5))
                sh_.alpha_composite(im, (pad, pad)); im = sh_
            text_cache[k] = im
        return text_cache[k]
    out = f'{W}/final_preview.mp4' if preview else f'{W}/final.mp4'
    dec = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', f'{W}/base.mp4', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    vf = 'noise=alls=4:allf=t,vignette=PI/5.5,format=yuv420p'
    if preview: vf = 'scale=540:960,' + vf
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{WD}x{HT}', '-r', str(FPS), '-i', '-',
                            '-i', f'{W}/audio.m4a', '-vf', vf, '-map', '0:v', '-map', '1:a', '-c:v', 'libx264',
                            '-preset', 'veryfast' if preview else 'slow', '-crf', '26' if preview else '20', '-maxrate', '24M', '-bufsize', '48M', '-profile:v', 'high',
                            '-c:a', 'copy', '-shortest', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    by_frame = {}
    for ev in events:
        for k in range(ev['f0'], ev['f1']): by_frame.setdefault(k, []).append(ev)
    fb = WD * HT * 3
    for k in range(total):
        buf = dec.stdout.read(fb)
        if len(buf) < fb: print('base ended early at', k); break
        fr = np.frombuffer(buf, np.uint8).reshape(HT, WD, 3); orig = fr
        canvas = Image.new('RGBA', (WD, HT), (0, 0, 0, 0))
        ctx = dict(photo=photo, text=text, behind=[], silhouette=False)
        evs = sorted(by_frame.get(k, []), key=lambda e: e.get('z', 0))
        for ev in evs:
            if ev['type'] in ('whip', 'spin', 'zoomthrough'): fr = apply_event(ev, k, fr, canvas, ctx)
        base = Image.fromarray(fr).convert('RGBA')
        for ev in evs:
            if ev['type'] not in ('whip', 'spin', 'zoomthrough', 'flash', 'letterbox', 'fadeblack', 'fadein'): apply_event(ev, k, fr, canvas, ctx)
        if ctx['behind']:
            m = person_mask(np.asarray(base.convert('RGB')))
            for layer in ctx['behind']: base.alpha_composite(layer)
            person = Image.fromarray(fr).convert('RGBA')
            if ctx['silhouette']: person = Image.new('RGBA', (WD, HT), (255, 255, 255, 255))
            person.putalpha(m); base.alpha_composite(person)
        base.alpha_composite(canvas); fr = np.asarray(base.convert('RGB'))
        for ev in evs:
            if ev['type'] in ('flash', 'letterbox', 'fadeblack', 'fadein'): fr = apply_event(ev, k, fr, canvas, ctx)
        enc.stdin.write(np.ascontiguousarray(fr).tobytes())
        if k % 300 == 0: print(f'  frame {k}/{total}', flush=True)
    enc.stdin.close(); enc.wait(); dec.kill()
    print('wrote', out)


if __name__ == '__main__':
    main()
