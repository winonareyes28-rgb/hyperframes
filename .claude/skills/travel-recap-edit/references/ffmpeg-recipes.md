# ffmpeg recipes for the travel-recap style

Tested on ffmpeg 6.1. Conventions: segments are rendered one per shot at the
final size and fps (`-r 30`, `yuv420p`, `libx264 -crf 18`, no audio), then
concatenated with the concat demuxer, then graded and muxed with the sound.
Always pass `-nostdin` when ffmpeg runs inside a shell `while read` loop.

## 0. Sound: BPM, beat grid and big hits

```python
# bpm.py <audio> — prints length, BPM, beat length and the 8 strongest hits
import sys, subprocess, numpy as np
sr = 11025
def analyse(path):
    pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-ac', '1', '-ar', str(sr),
                          '-f', 'f32le', '-'], capture_output=True).stdout
    x = np.frombuffer(pcm, np.float32); hop = 256; n = len(x) // hop
    e = np.log1p(100 * np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1)))
    on = np.maximum(0, np.diff(e, prepend=e[0])); on -= on.mean()
    ac = np.correlate(on, on, 'full')[len(on) - 1:]; fps = sr / hop
    lags = np.arange(len(ac)) / fps; m = (lags > 60 / 180) & (lags < 60 / 70)
    bpm = 60 / lags[m][np.argmax(ac[m])]
    hits = []
    for i in np.argsort(on)[::-1]:
        t = i / fps
        if all(abs(t - h) > 0.4 for h in hits): hits.append(t)
        if len(hits) >= 8: break
    return len(x) / sr, bpm, sorted(hits)
for p in sys.argv[1:]:
    d, b, h = analyse(p)
    print(f"{p}: {d:.1f}s ~{b:.0f} BPM beat={60/b:.3f}s hits: {' '.join(f'{t:.2f}' for t in h)}")
```

Beat grid: `beats = [first_hit + k * 60/bpm for k in range(...)]`. Snap every
shot boundary to the nearest grid point; flash-montage shots use ⅓ beat.
Shot durations must be whole frames at 30 fps: `round(d * 30) / 30`.

## 1. Grade + grain (final pass)

```
# teal-orange (Japan / Recap)
colorbalance=rs=-0.06:bs=0.08:rh=0.08:gh=0.02:bh=-0.06,eq=contrast=1.08:saturation=1.05,noise=alls=7:allf=t,vignette=PI/5
# moody teal (Hong Kong)
colorbalance=rs=-0.04:gs=0.02:bs=0.05,eq=contrast=0.95:saturation=0.82:brightness=0.02,noise=alls=9:allf=t
# warm natural (Barcelona / Disneyland)
eq=contrast=1.05:saturation=1.15,colortemperature=temperature=5800,noise=alls=5:allf=t
```

## 2. T1 flash-cut opener / T16 photo scatter

Flash opener: just shots of `round(beat/3 * 30)` frames each, concatenated.
Photo scatter on black (seeded positions, one photo per ⅓ beat):

```
ffmpeg -f lavfi -t 1.2 -i color=black:s=1080x1920:r=30 -i p1.jpg -i p2.jpg -i p3.jpg \
 -filter_complex "[1]scale=360:-2[a];[2]scale=360:-2[b];[3]scale=360:-2[c];\
 [0][a]overlay=120:300:enable='between(t,0,0.4)'[v1];\
 [v1][b]overlay=600:900:enable='between(t,0.4,0.8)'[v2];\
 [v2][c]overlay=240:1400:enable='between(t,0.8,1.2)'" -r 30 out.mp4
```

## 3. T2 font-cycle title (+ T3 title over montage)

One `drawtext` per font, each enabled for ⅓ beat, the last one stays on:

```
F="drawtext=text='BARCELONA':fontsize=170:fontcolor=0xFFD21F:x=(w-tw)/2:y=h*0.42"
-vf "drawtext=fontfile=Playfair.ttf:text='Welcome to':fontsize=48:fontcolor=white:x=(w-tw)/2:y=h*0.42-70,\
$F:fontfile=Anton.ttf:enable='lt(t,0.2)',\
$F:fontfile=Pacifico.ttf:enable='between(t,0.2,0.4)',\
$F:fontfile=Unbounded.ttf:enable='between(t,0.4,0.6)',\
$F:fontfile=Anton.ttf:enable='gte(t,0.6)'"
```

For T3 render the title on a transparent layer once (`-f lavfi color=black@0`

- `format=rgba`, or a PNG made with PIL) and `overlay` it over the flash
  montage after concat, so the text never jumps at a cut.

## 4. T4 letterbox squeeze-out

`drawbox` sizes are evaluated once in ffmpeg 6.x, so slide black bars with
`overlay` (its x/y update per frame). Closes fully over 1.5 s:

```
-i shot.mp4 -f lavfi -i color=black:s=1080x960:r=30 -filter_complex \
"[1]split[t][b];[0][t]overlay=0:'-h+h*min(1,t/1.5)':shortest=1[v];[v][b]overlay=0:'H-h*min(1,t/1.5)':shortest=1"
```

Apply it across the concatenated tail of a montage so the shots keep
flashing while the bars close.

## 5. T5 scattered letter reveal / T7 type-on

Measure each letter's x with PIL, then one `drawtext` per letter with its own
fade-in start (shuffled order for T5, left-to-right for T7):

```python
from PIL import ImageFont
import random
font = "/path/Anton.ttf"; size = 220; word = "BAGUIO"; W = 1080
f = ImageFont.truetype(font, size)
total = f.getlength(word); x0 = (W - total) / 2
order = list(range(len(word))); random.Random(7).shuffle(order)   # T5; use range() for T7
parts = []
for rank, i in enumerate(order):
    x = x0 + f.getlength(word[:i]); start = 0.15 + rank * 0.18
    parts.append(f"drawtext=fontfile={font}:text='{word[i]}':fontsize={size}:fontcolor=0xE5262B:"
                 f"x={x:.0f}:y=h*0.30:alpha='clip((t-{start})/0.15,0,1)'")
print(",".join(parts))
```

## 6. T6 text behind subject

Needs a per-frame subject mask. With `pip install rembg` (first run downloads
the u2net model):

```
ffmpeg -ss S -t D -i shot.mov -vf fps=30,scale=1080:1920 frames/%04d.png
rembg p -m u2net_human_seg frames/ masks/        # RGBA cut-outs of the person
ffmpeg -framerate 30 -i frames/%04d.png -framerate 30 -i masks/%04d.png \
 -filter_complex "[0]<title drawtext filters>[bg];[bg][1]overlay=0:0" -r 30 out.mp4
```

Keep the title large and placed where the subject overlaps only part of it.
For landmarks (castle, tower) use `-m isnet-general-use` or a hand-drawn
static mask PNG when the camera is locked off.

## 7. Transitions (xfade between two segments)

Each `xfade` shortens the total by its duration — plan offsets on the grid.

```
[a][b]xfade=transition=hblur:duration=0.15:offset=OFF     # T10 whip / motion-blur
[a][b]xfade=transition=fadewhite:duration=0.12:offset=OFF # T11 white flash
[a][b]xfade=transition=squeezev:duration=0.4:offset=OFF   # vertical squeeze
[a][b]xfade=transition=fadegrays:duration=0.3:offset=OFF  # desaturating dissolve
```

Cheaper white flash on a hard cut: `fade=t=in:st=0:d=0.1:color=white` on the
incoming shot. Black beat (T8): a `color=black` segment of 1–2 beats.

T13 spin (rotate into the cut; upscale first so corners never show):

```
scale=iw*1.45:-2,rotate=a='PI/6*max(0,(t-(D-0.25))/0.25)':ow=1080:oh=1920:c=black
```

T9 hand-cover: no filter — cut on the frame where the hand fills the lens in
shot A and start shot B on a matching hand-filled frame (or the hand pulling
away). Use `select` on low-variance frames to find them.

## 8. T14 speed ramp and slow-mo

- 120 fps phone clips: `setpts=4*PTS,fps=30` gives clean 4× slow-mo.
- Ramp inside one shot: split into two segments (`setpts=1*PTS` then
  `setpts=3*PTS`), cut on the beat.
- 30 fps footage slow-mo (approximate):
  `minterpolate=fps=60:mi_mode=mci:mc_mode=aobmc,setpts=2*PTS,fps=30` (slow).

## 9. T15 B&W → color pop

`hue=s=0:enable='lt(t,POP)'` where POP is a beat time inside the shot.

## 10. T18 card pop (picture in picture)

```
[0][1]overlay=(W-w)/2:H*0.18:enable='between(t,0.3,0.9)'   # [1] pre-scaled to 60% + 8px white pad
```

## 11. Concat, grade, mux sound

```
ffmpeg -f concat -safe 0 -i list.txt -i sound.mp3 \
 -vf "<grade from §1>,format=yuv420p" -af "afade=t=out:st=END-0.5:d=0.5" \
 -map 0:v -map 1:a -c:v libx264 -preset slow -crf 19 -c:a aac -b:a 192k -shortest -movflags +faststart out.mp4
```

Verify: frame sheet every 0.5 s, and list cut times
(`select='gt(scene,0.3)',metadata=print`) — each must sit within 1 frame of
a beat-grid point.

## 12. Lessons from the Baguio build

- **T20 cursor:** a lone `_` drawtext is positioned at the glyph's own top, so it
  floats. Draw the word without the cursor, and draw the full word _with_ `_`
  at the same x on blink frames:
  `enable='gte(t,T)*lt(mod(t-T,BEAT),BEAT/2)'`.
- **T6 / T21 text behind people works** with `rembg` (`u2net_human_seg`):
  per frame, composite base → text layer → person cut-out in PIL; for the
  silhouette flash replace the cut-out RGB with white for 2 frames. About
  1 s/frame on CPU at 1080×1920 — keep these shots ≤ 2 s.
- **Check the timeline is continuous** before rendering: every shot's `t0` must
  equal the previous shot's `t1`. One overlapping section pushed every later
  shot late and cut off the ending.
- Use `librosa.beat.beat_track` for the grid; note quiet stretches (no strong
  onsets) — they are the natural "breath" sections.
