# plan.py — "Next Station: Baguio" (Day 1 on What Do You Mean?, Day 2 on Dilaw)
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import fit_size, RED, YELLOW, WHITE, WD, HT, FPS

SECTIONS = [
    dict(song='Justin Bieber - What Do You Mean (Lyrics).mp3', start=8.24, end=46.65),   # build -> drop @15.9 -> chorus
    dict(song='Maki - Dilaw (Lyrics).mp3', start=107.32, end=141.62),                   # pre-chorus -> chorus @111.1
]
TAIL_FADE = 0.8


def V(src, **k): return dict(kind='video', src=src, **k)
def Ph(day, n, **k): return dict(kind='photo', src=f'{day}_IMG_{n}', **k)


DAY1 = [  # (beats, shot) — intro is 16 beats of build, drop on b16
    (2, V('D1_IMG_6494', ss=0.0, fix='night')),                 # bus at the Cubao terminal
    (2, V('D1_IMG_6495', ss=4.6, fix='night')),                 # barkada with luggage
    (2, Ph('D1', 6455, fix='night', kb=(1.0, 1.08))),           # Victory Liner front
    (6, V('D1_IMG_6486', ss=0.0, fix='purple')),                # blue bus, city lights pass
    (4, V('D1_IMG_6646', ss=1.0)),                              # dawn arrival walk  (BAGUIO behind them)
    # ---- drop: 1-beat montage, HUD on
    (1, Ph('D1', 6547, kb=(1.12, 1.0))), (1, Ph('D1', 6574)), (1, Ph('D1', 6583, cy=0.3)), (1, Ph('D1', 6578)),
    (2, V('D1_IMG_6697', ss=1.2)),                              # resting under the pines with luggage
    (1, Ph('D1', 6614)), (1, Ph('D1', 6631)),
    (2, V('D1_IMG_6746', ss=0.5)),                              # luggage at SM
    (1, Ph('D1', 6701)), (1, Ph('D1', 6761, cy=0.2)),
    (2, V('D1_IMG_6748', ss=0.4)),                              # SM crossing walk (+ card pop)
    (2, V('D1_IMG_6751', ss=4.3)),                              # sunglasses moment
    (1, Ph('D1', 6774)), (1, Ph('D1', 6782)), (2, V('D1_IMG_6855', ss=0.4)),   # grid overlay here
    (2, V('D1_IMG_6856', ss=0.6)),
    (2, V('D1_IMG_6835', ss=1.5)),                              # skyline pan
    (2, V('D1_IMG_6879', ss=1.0)), (2, V('D1_IMG_6878', ss=8.0)),   # taxi ride (red border)
    (2, V('D1_IMG_6885', ss=0.3)),                              # hotel balcony
    (2, V('D1_IMG_6887', ss=0.3)),                              # mirror selfie
    (4, V('D1_IMG_6904', ss=4.0, push=0.06)),                   # breath: fog rolls over the fields
    (2, V('D1_IMG_6910', ss=2.6)), (1, V('D1_IMG_6909', ss=5.8)), (1, Ph('D1', 6905)),
] + [(0.5, Ph('D1', n)) for n in (6907, 6892, 6898, 6467, 6470, 6400, 6401, 6404,
                                  6422, 6424, 6457, 6600, 6653, 6685, 6694, 6550)] + [   # flashback burst
    (6, V('D1_IMG_6917', ss=0.8)),                              # night in the room
    (None, Ph('D1', 6912, fix='night', kb=(1.0, 1.15))),        # city lights — letterbox closes
]

DAY2 = [
    (3, dict(kind='scatter')),                                  # photo scatter on black
    (2, V('D2_IMG_6918', ss=0.5, fix='night')),                 # first light from the balcony
    (3, V('D2_IMG_7488', ss=3.0, bw=round(1.0 * 0.4876 * FPS))),   # B&W -> colour on the beat
] + [(1 / 3, Ph('D2', n)) for n in (6972, 6974, 7004, 7010, 7011, 7019, 7021, 7023, 7025, 7034, 7036, 7039,
                                     7062, 7064, 7068, 7070, 7081, 7083, 7090, 7110, 7126, 7127, 7132, 7135)] + [
    (2, V('D2_IMG_7122', ss=8.2)),                              # CAMP JOHN HAY sign drive-by
    (2, V('D2_IMG_7130', ss=0.0)),
    (1, V('D2_IMG_7124', ss=2.75)),                             # natural whip pan
    (2, V('D2_IMG_7131', ss=1.6)),
    (1, Ph('D2', 7145)), (1, Ph('D2', 7163)),
    (2, V('D2_IMG_7207', ss=4.6)),                              # selfie in the pines
    (1, Ph('D2', 7196)),
    (2, V('D2_IMG_7334', ss=6.0)),                              # Bell House interior
    (2, V('D2_IMG_7409', ss=1.5)),                              # spin out
    (2, V('D2_IMG_7362', ss=0.0)),
    (2, V('D2_IMG_7363', ss=0.0)), (2, V('D2_IMG_7363', ss=5.0)),
    (1, Ph('D2', 7327)), (1, Ph('D2', 7309)),
    (4, V('D2_IMG_7361', ss=15.6, speed=0.5)),                  # slow-mo hero: arms out on the boardwalk
    (2, V('D2_IMG_7370', ss=2.0)),
    (1, Ph('D2', 7448, kb=(1.0, 1.1))), (1, Ph('D2', 7449, kb=(1.1, 1.0))),
    (2, V('D2_IMG_7411', ss=1.0)),
    (2, V('D2_IMG_7410', ss=4.0)),
    (2, V('D2_IMG_7512', ss=9.0)),
    (4, V('D2_IMG_7644', ss=6.0)),                              # heading home through the lowlands
    (4, Ph('D2', 7039, kb=(1.0, 1.08))),                        # barkada at the flower arch
    (None, Ph('D1', 6572, kb=(1.0, 1.06), cy=0.0)),             # landmark end card, sky on top
]


def build(G):
    shots, events = [], []
    for sec, seq in enumerate((DAY1, DAY2)):
        nb = len(G.sections[sec]['beats']) - 1; b = 0.0; marks = []
        for beats, s in seq:
            if beats is None: beats = nb - b
            f0, f1 = G.f(sec, b), G.f(sec, b + beats)
            shots.append(dict(s, f0=f0, f1=f1)); marks.append(b); b += beats
        assert abs(b - nb) < 1e-6, (sec, b, nb)
        events += (day1 if sec == 0 else day2)(G, sec, nb)
    # make sections contiguous: section 1 starts where section 0 ends
    return shots, events


def F(G, sec, b): return G.f(sec, b)


def day1(G, s, nb):
    f = lambda b: F(G, s, b); beat = G.t(s, 1) - G.t(s, 0); bf = beat * FPS
    big = fit_size('STATION', 'anton', WD - 140, 330)
    words = [dict(txt='NEXT', at=0, until=f(4) - f(2)), dict(txt='STATION', at=f(4) - f(2), until=f(6) - f(2)),
             dict(txt='IS', at=f(6) - f(2), until=f(12) - f(2), blink=(f(7) - f(2), int(bf / 2)))]
    for w in words: w.update(font='anton', size=big, color=RED, y=HT * 0.40)
    bag = fit_size('BAGUIO', 'anton', WD - 80, 360)
    return [
        dict(type='text', f0=f(2), f1=f(12), items=words),                                         # T20
        dict(type='flash', f0=f(12), f1=f(12) + 4, peak=0.9),
        dict(type='behind', f0=f(12), f1=f(16), flash=f(14) - f(12),                               # T6 + T21
             item=dict(txt='BAGUIO', font='anton', size=bag, color=RED, y=HT * 0.36, fade=3)),
        dict(type='text', f0=f(12) + 6, f1=f(16), items=[dict(txt='DAY 01', font='grotesk', size=34, color=WHITE, track=14, y=HT * 0.36 - bag * 0.62)]),
        dict(type='whip', f0=f(16) - 3, f1=f(16) + 3, cut=f(16), dir=1),
        dict(type='hud', f0=f(16), f1=f(64), tags=[('MOMENTS IN', 'BAGUIO2026'), ('SHOT WITH', 'IPHONE')], bottom='DAY 01  ·  FEB 2026'),
        dict(type='whip', f0=f(20) - 3, f1=f(20) + 3, cut=f(20), dir=-1),
        dict(type='zoomthrough', f0=f(24) - 4, f1=f(24) + 4, cut=f(24)),
        dict(type='whip', f0=f(28) - 3, f1=f(28) + 3, cut=f(28), dir=1),
        dict(type='card', f0=f(29), f1=f(30), src='D1_IMG_6770', y=0.16),                          # T18
        dict(type='grid', f0=f(32), f1=f(36)),                                                     # T23
        dict(type='whip', f0=f(38) - 3, f1=f(38) + 3, cut=f(38), dir=-1),
        dict(type='border', f0=f(40), f1=f(44)),                                                   # T23
        dict(type='flash', f0=f(48), f1=f(48) + 5, peak=1.0),                                      # T11 into the fog
        dict(type='whip', f0=f(52) - 3, f1=f(52) + 3, cut=f(52), dir=1, vertical=True),
        dict(type='flash', f0=f(56), f1=f(56) + 3, peak=0.7),
        dict(type='flash', f0=f(64), f1=f(64) + 4, peak=0.8),
        dict(type='letterbox', f0=f(nb - 5), f1=f(nb)),                                            # T4
    ]


def day2(G, s, nb):
    f = lambda b: F(G, s, b); beat = G.t(s, 1) - G.t(s, 0); bf = beat * FPS
    scat = ['D2_IMG_7021', 'D2_IMG_7034', 'D2_IMG_7066', 'D2_IMG_7145', 'D2_IMG_7327', 'D2_IMG_7192']
    end = f(nb)
    stack_y = HT * 0.21; bag = fit_size('BAGUIO 2026', 'anton', WD - 100, 300)
    return [
        dict(type='scatter', f0=f(0), f1=f(3), srcs=scat, step=int(bf / 2), seed=5),               # T16
        dict(type='typeon', f0=f(3), f1=f(8), txt='DAY 02', font='anton', size=260, color=YELLOW, y=HT * 0.30, gap=3),  # T7
        dict(type='flash', f0=f(8), f1=f(8) + 4, peak=1.0),
        dict(type='fontcycle', f0=f(8), f1=f(16), txt='BAGUIO', kicker='Welcome to', color=YELLOW, shadow=1, y=HT * 0.44,   # T2 + T3
             step=max(2, int(bf / 3)), fonts=['anton', 'pacifico', 'unb', 'playi', 'marker', 'caveat', 'archivo', 'anton']),
        dict(type='hud', f0=f(16), f1=f(58), color=YELLOW, tags=[('MOMENTS IN', 'CAMP JOHN HAY'), ('SHOT WITH', 'IPHONE')], bottom='DAY 02  ·  FEB 2026'),
        dict(type='whip', f0=f(16) - 3, f1=f(16) + 3, cut=f(16), dir=1),
        dict(type='whip', f0=f(21) - 3, f1=f(21) + 3, cut=f(21), dir=1),
        dict(type='spin', f0=f(32) - 4, f1=f(32) + 4, cut=f(32), deg=40),                          # T13
        dict(type='flash', f0=f(40), f1=f(40) + 4, peak=0.8),
        dict(type='zoomthrough', f0=f(46) - 4, f1=f(46) + 4, cut=f(46)),
        dict(type='whip', f0=f(50) - 3, f1=f(50) + 3, cut=f(50), dir=-1),
        dict(type='flash', f0=f(58), f1=f(58) + 5, peak=1.0),
        dict(type='text', f0=f(62), f1=end, items=[                                                # T17 + T24
            dict(txt='RECAP', font='grotesk', size=40, color=YELLOW, track=22, y=stack_y - bag * 0.62, at=0, fade=4, shadow=1),
            dict(txt='BAGUIO 2026', font='anton', size=bag, color=YELLOW, y=stack_y, at=int(bf), fade=3, shadow=1),
            dict(txt='TAKE EVERY MOMENT', font='grotesk', size=34, color=WHITE, track=12, y=stack_y + bag * 0.62, at=int(2 * bf), fade=4, shadow=1)]),
        dict(type='flash', f0=f(62), f1=f(62) + 4, peak=0.9),
        dict(type='fadeblack', f0=end - 18, f1=end),
    ]
