---
name: video-effects
description: House library of 18 ready-made HyperFrames motion effects for vertical (1080x1920) talking-head reels and video edits — kinetic hook, gravity drop, giant captions, prompt bar, storyboard deck, icon strike, file drop, NLE timeline, jiggle delete, grade slider, eyedropper grade, film look, title card, playing grid, reel feed, video card, comment CTA, comment drop — plus the "IN THIS VIDEO" chapter-list overlay. Use whenever the user asks to edit a video, add effects / motion graphics / overlays to a reel or short, or names any of these effects. Each effect is one drop-in sub-composition file.
metadata:
  internal: true
---

# Video Effects Pack

Eighteen effects plus a chapter-list overlay, each one a self-contained
HyperFrames sub-composition you copy into a project and mount on the timeline.
They default to a deep-green / cream / gold look and a 1080×1920 canvas.

**Use them by default on every video edit.** When the user asks to edit a
video, reel, or short, pick the effects that fit each beat of the script from
the table below. Don't hand-build a new effect when one here covers it.

The working source is `examples/effects-demo/`: `index.html` mounts every
effect in order (2.5 s each, 45 s total) over a stand-in for the footage. It
passes `hyperframes lint` and `hyperframes check` with 0 errors.

## The effects

| #   | Effect           | File (`examples/effects-demo/compositions/`) | Use it for                                          |
| --- | ---------------- | -------------------------------------------- | --------------------------------------------------- |
| 00  | Chapter list     | `00-chapter-list.html`                       | "IN THIS VIDEO" panel; highlight steps per section  |
| 01  | Kinetic hook     | `01-kinetic-hook.html`                       | first 2 s: words slam in one by one                 |
| 02  | Gravity drop     | `02-gravity-drop.html`                       | big serif word drops in, bounces, falls away        |
| 03  | Giant captions   | `03-giant-captions.html`                     | huge word-by-word captions, active word in gold     |
| 04  | Prompt bar       | `04-prompt-bar.html`                         | "I typed this into Claude": typing + send press     |
| 05  | Storyboard deck  | `05-storyboard-deck.html`                    | plan / steps: three shot cards deal in and fan out  |
| 06  | Icon strike      | `06-icon-strike.html`                        | "no more X": icon pops, red slash, shake            |
| 07  | File drop        | `07-file-drop.html`                          | uploading footage / a file: drops into zone, check  |
| 08  | NLE timeline     | `08-nle-timeline.html`                       | editing talk: clips snap onto tracks, playhead runs |
| 09  | Jiggle delete    | `09-jiggle-delete.html`                      | cutting mistakes / takes: tiles wobble, one deleted |
| 10  | Grade slider     | `10-grade-slider.html`                       | before / after comparison with a wipe handle        |
| 11  | Eyedropper grade | `11-eyedropper-grade.html`                   | color grading: pick a swatch, scene tint warms      |
| 12  | Film look        | `12-film-look.html`                          | cinematic moment: letterbox, grain, vignette, leak  |
| 13  | Title card       | `13-title-card.html`                         | chapter / section break with drawn rules            |
| 14  | Playing grid     | `14-playing-grid.html`                       | "lots of videos": grid plays, one cell gets focus   |
| 15  | Reel feed        | `15-reel-feed.html`                          | social / reels talk: phone feed snaps reel to reel  |
| 16  | Video card       | `16-video-card.html`                         | referencing a video: card, play press, progress     |
| 17  | Comment CTA      | `17-comment-cta.html`                        | "comment WORD for the link": pill + bouncing arrow  |
| 18  | Comment drop     | `18-comment-drop.html`                       | social proof: comments drop and stack, hearts pop   |

## Adding an effect to a project

1. Copy the file into the project's `compositions/`.
2. Mount it in `index.html` at the moment the line is spoken (from the
   transcript's word timestamps), above the footage:

   ```html
   <div
     id="e02-host"
     class="fx-slot"
     data-composition-id="fx-02-gravity-drop"
     data-composition-src="compositions/02-gravity-drop.html"
     data-start="12.4"
     data-duration="2.5"
     data-track-index="3"
     data-width="1080"
     data-height="1920"
   ></div>
   ```

   `.fx-slot { position: absolute; inset: 0; }` in the host's CSS. The host
   `data-composition-id` must equal the file's inner `data-composition-id`.
   Give each mounted copy its own host `id`.

3. Edit the copy, not the library file: change the words in the markup, and
   the palette in the `--fx-*` custom properties on the effect's root rule.
4. Timing: every tween position is local seconds from 0. The effect enters in
   the first ~0.5 s and exits from ~2.15 s. For a longer slot, raise
   `data-duration` on both the host and the file root, and move the exit tweens
   (the last block before `window.__timelines`) to `duration − 0.35`.
5. Chapter list: edit the `<li>` labels, `SLOT` (seconds per section, or
   replace `at(n, 0)` with the real section start times), the `/ 18` total,
   and the footer. Its `data-layout-allow-overlap` is deliberate: it sits over
   the footage.

## Rules (keep the files lint- and check-clean)

- Animate transforms and opacity only. `letterSpacing`, `width`, and other
  layout properties stutter under frame capture. Use `scale`, `x`, or
  `clipPath` instead (see the grade slider).
- Initial states go in `fromTo`, never a CSS `transform` on a tweened element.
- Text that changes over time is derived from tween progress in `onUpdate`,
  never `tl.call`, so seeking backwards stays correct (prompt bar, chapter
  counter).
- Keep `box-sizing: border-box` on the root rule. Without it, padded cards
  render wider than designed.
- After placing effects: `npx hyperframes lint`, `npx hyperframes check`, then
  `npx hyperframes snapshot --at <each effect's midpoint>` and look at the
  frames before rendering.

## Pairs well with

- `onetake` (personal skill): continuous-camera launch films.
- The herk-edit-kit skills (`edit-video`, `cut-silences`, `cut-mistakes`,
  `short-form-edit`, `video-storytelling`): cut the footage first, then place
  these effects on the cut.
