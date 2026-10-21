---
name: travel-recap-edit
description: House editing style for short travel / barkada trip recap videos (TikTok, Reels, Shorts, YouTube intro) — beat-locked flash-cut openers, font-cycling and text-behind-subject titles, letterbox squeezes, whip / hand-cover / white-flash transitions, speed ramps, B&W-to-color pops and a cinematic grade. Use when the user asks to edit a trip vlog, travel recap, "cinematic CapCut-style" edit, or references the Barcelona / Japan / Hong Kong / Disneyland / Travel Recap / Next Station inspo edits. Built from 6 reference TikToks the user picked.
---

# Travel Recap Edit Style

The style the user wants for trip videos, distilled from 6 reference edits
(full shot-by-shot breakdowns: `references/inspo-breakdowns.md`;
ready-to-use ffmpeg recipes: `references/ffmpeg-recipes.md`).

## The style DNA (all 6 references share this)

1. **Short and sound-led.** 18–30 s. One remixed "original sound" carries the
   whole edit; the edit length = the sound length. Never pad past the sound.
2. **Title in the first 0–4 s.** Big place name, always animated (letters
   reveal, fonts cycle, or text sits behind the subject). Never a static title.
3. **Every cut lands on the beat.** Measure BPM first, build a beat grid,
   snap every cut, flash and text change to it. Common shot lengths:
   ⅓ beat (flash montage, ~0.2 s), 1 beat (montage, 0.4–0.7 s),
   2–4 beats (hero / establishing shots, 1–2.5 s).
4. **Energy curve:** hook → title → fast montage → _breath_ (black beat or a
   slow hero shot) → bigger montage → finale (fireworks / sunset / group pose)
   → hard end on the last hit.
5. **Cinematic grade, no clutter.** Teal-orange or moody desaturated teal,
   lifted blacks, light grain, sometimes soft vignette. No subtitles, no
   emoji, no stickers. Text appears only for titles and place names.
6. **Camera language:** walking-POV, low angles, worm's-eye up at buildings,
   hand-in-frame POV (holding ticket / camera / food), group reaction
   close-ups, one slow-mo hero walk, hyperlapse, fireworks or sunset finale.

## Technique catalog

Pick 5–7 per edit; do not stack everything. Timing is in beats (b).

| #   | Technique                                      | Seen in                  | How it plays                                                                                                                                           | Timing          |
| --- | ---------------------------------------------- | ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------- |
| T1  | **Flash-cut opener**                           | Barcelona                | 8–12 different shots, each ⅓ b, before the title                                                                                                       | 2–2.5 s total   |
| T2  | **Font-cycle title**                           | Barcelona, Recap         | Small serif kicker ("Welcome to") + huge place name in yellow; the place name swaps typeface every ⅓ b (bold sans → script → wide → serif), then locks | 3–4 s           |
| T3  | **Title over flash montage**                   | Barcelona                | Title stays locked while the background swaps every ⅓ b                                                                                                | 1.5–2.5 s       |
| T4  | **Letterbox squeeze-out**                      | Barcelona                | Black bars grow from top+bottom until the frame is a slit, then black — ends the intro section                                                         | 1–1.5 s         |
| T5  | **Scattered letter reveal**                    | Japan                    | Heavy red condensed title; letters fade in out of order over ~1.5 s, then hold                                                                         | 2.5 s           |
| T6  | **Text behind subject**                        | Japan, Disneyland        | Title sits _behind_ a person / landmark (subject masked on top of the text)                                                                            | with T5/T7      |
| T7  | **Type-on title**                              | Disneyland               | Small red kicker words first, then the big word types on letter by letter                                                                              | 1.5 s           |
| T8  | **Black beat**                                 | Japan                    | 0.5–0.8 s of pure black right before the drop                                                                                                          | on the pre-drop |
| T9  | **Hand-cover transition**                      | Disneyland               | Hand / palm moves into the lens, fills frame, next shot starts from the hand pulling away                                                              | 0.5–1 s         |
| T10 | **Whip / motion-blur streak**                  | Japan, HK, Recap         | Horizontal or vertical directional blur between two shots moving the same way                                                                          | 4–6 frames      |
| T11 | **White / cream flash**                        | Japan, Disneyland, Recap | 2–4 frame overexposed white frame at a section change                                                                                                  | on a big hit    |
| T12 | **Match-cut series**                           | Hong Kong                | Same framing repeated across places (walking past station signs, doors, signboards) — one per beat                                                     | 1 b each        |
| T13 | **Spin / Dutch-tilt transition**               | Hong Kong                | Shot rotates 15–90° into the next                                                                                                                      | 0.5 s           |
| T14 | **Speed ramp**                                 | Japan, Disneyland        | Real-time → slow-mo (or fast → normal) inside one shot, ramp lands on a hit                                                                            | 1–2 s           |
| T15 | **B&W → color pop**                            | Disneyland, Recap        | Shot starts monochrome, snaps to full color on the beat                                                                                                | 2 b             |
| T16 | **Photo-scatter intro**                        | Recap                    | Small photos flash at random positions on black, one per ⅓ b                                                                                           | 1–1.5 s         |
| T17 | **Stacked recap title**                        | Recap                    | Kicker "RECAP" / huge "TRAVEL VLOG" / tracked tagline "TAKE EVERY MOMENT" in yellow condensed bold                                                     | 3–4 s           |
| T18 | **Card pop (PiP)**                             | Japan                    | A second shot appears as a floating card over the first                                                                                                | 1 b             |
| T19 | **Fireworks / sunset finale + group end pose** | Disneyland               | Biggest visual saved for the last 20 %, then one held group shot to the end                                                                            | last 4–6 s      |
| T20 | **Word-per-beat title with cursor**            | Next Station             | "NEXT" → "STATION" → "IS_" one word per beat in huge red condensed, underscore cursor blinks for 2–3 beats, then the place name lands                  | 3 s             |
| T21 | **Silhouette flash**                           | Next Station             | On the hit, the people in front of the title flash solid white (their mask filled white) for 2 frames                                                  | 2 frames        |
| T22 | **Corner HUD tags**                            | Next Station             | Small red two-line tags pinned in the corners for the whole montage: "MOMENTS IN / BAGUIO2026" left, "SHOT WITH / IPHONE" right                        | whole montage   |
| T23 | **Grid / frame overlays**                      | Next Station             | Thin white rule-of-thirds grid or a thick red border pulses on for 2–3 beats over a shot                                                               | 1–1.5 s         |
| T24 | **Landmark title ending**                      | Next Station             | Last shot is the hero landmark with the big place name back on screen (behind the landmark)                                                            | last 2 s        |

## Typography

- **Place name:** heavy condensed or wide sans — Anton, Bebas Neue, Archivo Black,
  Inter Display Black (local fallback). Colors: **yellow #FFD21F** or **red #E5262B**.
- **Kicker / tagline:** small serif (Playfair Display, DM Serif) or tracked caps.
- **Cycle fonts (T2):** add a script (Pacifico / Caveat), a wide display and a serif.
- Fetch Google Fonts into `~/.fonts` when not installed; keep Inter as fallback.

## Workflow

1. **Sound first.** Get the track (user file, or extract from an inspo video),
   run BPM + big-hit detection (script in `references/ffmpeg-recipes.md`).
   Note the drop(s): that's where the title lands and where the finale starts.
2. **Map sections to the sound:** intro (to first big hit) → title → montage A
   → breath → montage B → finale → end pose. Write a shot table with beat
   counts before rendering anything.
3. **Pull shots:** contact-sheet every clip, choose by motion direction (pair
   left-moving with left-moving for whips), keep one slow-mo-able hero shot.
4. **Show the plan to the user and wait for an OK** before the first render.
5. **Render** segments → concat → grade + grain → mux the sound. Verify with a
   frame sheet every 1 s and check every cut lands within 1 frame of a beat.
6. **Deliver** the full-quality file plus a light preview copy.

## Adapting to vertical (9:16) footage

The references are 16:9. For Reels / TikTok keep the same timing, center the
title in the upper third, and use vertical whips (T10) for tall shots. For a
16:9 YouTube cut from vertical clips, use 2–3-panel split screens or a blurred
background fill; titles go full width.

## Don'ts

- No captions or subtitles in this style. No emoji. No stickers.
- No cut that is not on a beat. No transition that is not motivated by motion.
- No more than one slow-mo hero shot per 15 s. No idle zooms on every shot.

## Enhancing the user's footage and photos (one consistent mood)

Phone clips and photos from different people and times must look like one
film. Apply in this order, per clip, before the creative grade:

1. **Fix exposure / white balance** per source: night clips `eq=brightness=0.04:gamma=1.1`,
   purple bus light `colorbalance` toward neutral, overcast days lift contrast.
2. **Denoise night shots:** `hqdn3d=3:3:6:6` (video), mild on photos.
3. **Stabilize shaky walking clips:** `vidstabdetect`/`vidstabtransform` if available, else `deshake`.
4. **Sharpen lightly** after scaling: `unsharp=5:5:0.6`.
5. **One shared creative grade** for the whole edit (see recipes §1), then grain.
6. **Photos (HEIC):** convert with `pillow-heif`, apply the same grade, and use
   them as motion: Ken Burns push (2 beats), photo-scatter (T16), polaroid
   stack drops, B&W→color pop (T15), or flash-montage frames (T1). Never show
   a photo static for more than 1 beat.

## Fonts toolkit (download from Google Fonts into ~/.fonts)

GitHub raw font URLs may be blocked; fetch the CSS instead and download the
TTF it links: `curl "https://fonts.googleapis.com/css2?family=Anton" | grep -o 'https://fonts.gstatic.com[^)]*'`,
then `fc-cache -f`.

| Role              | Fonts                                                                        |
| ----------------- | ---------------------------------------------------------------------------- |
| Big place name    | Anton, Bebas Neue, Archivo Black, Big Shoulders Display                      |
| Font-cycle extras | Pacifico, Caveat Brush, Unbounded, Playfair Display Italic, Permanent Marker |
| Kicker / HUD caps | Playfair Display, Space Grotesk, Inter (tracked)                             |
