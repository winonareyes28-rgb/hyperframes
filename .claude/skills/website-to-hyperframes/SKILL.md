---
name: website-to-hyperframes
description: Turn a live website URL into a finished HyperFrames promo or site-tour video built from THIS checkout — the repo-local CLI and the tracked `skills/product-launch-video` pipeline, with the house motion doctrine (motion-doctrine, cut-the-curve, seam-craft, oversized-cursor, captions-overlay) layered on top. Use when working inside the hyperframes repo and the user says "turn this website into a video", "site-to-video", "website to hyperframes", or hands over a product URL for a showcase-grade launch film. Outside this repo, use the published /product-launch-video instead.
metadata:
  internal: true
---

# Website → HyperFrames (repo-native)

Input: one website URL (plus an optional brief / script).
Output: a lint-clean, check-clean, seam-gate-green project in
`videos/<project>/` (gitignored). Render only after the review pause.

This skill is a **thin overlay**, not a second pipeline. The capture → design →
storyboard → frames → finalize steps are `skills/product-launch-video/SKILL.md`,
run step by step with its gates. This page only changes three things:

1. **Source of truth = this checkout.** Every command, script, and reference
   resolves to tracked repo files, never to an installed or `@latest` copy.
2. **Seams follow the house doctrine.** Ordinary cuts are planned as a vector
   ledger, stamped, and verified — not picked from the transition registry.
3. **Website-specific guards** on capture and on how captured screens are used.

Not a website? Route elsewhere: arbitrary text → `/faceless-explainer`, a PR →
`/pr-to-video`, a bare "make a video" → `/hyperframes` (intent layer).

## Load first, non-negotiable

`motion-doctrine` (gateway) → `cut-the-curve` → `seam-craft`. Add
`oversized-cursor` when any scene is pointer-led (most site tours are), and
`captions-overlay` whenever the film carries narration captions. These
supersede the motion guidance inside `skills/hyperframes-animation/` wherever
they disagree.

## Path map (resolve once, use everywhere)

| Token                           | Resolves to                                         |
| ------------------------------- | --------------------------------------------------- |
| `<REPO>`                        | repo root (`git rev-parse --show-toplevel`)         |
| `<HF>`                          | `node <REPO>/packages/cli/bin/hyperframes.mjs`      |
| `<PLV>`                         | `<REPO>/skills/product-launch-video`                |
| `<SKILL_DIR>`                   | `<PLV>` — wherever the PLV skill says `<SKILL_DIR>` |
| `<MEDIA_DIR>`                   | `<REPO>/skills/media-use`                           |
| `<HYPERFRAMES_AUDIO_SKILL_DIR>` | `<REPO>/skills/hyperframes-audio`                   |
| `<DOCTRINE>`                    | `<REPO>/.claude/skills/motion-doctrine`             |
| `<PROJECT>`                     | `<REPO>/videos/<kebab-brand>` (e.g. `acme-promo`)   |

Read every `npx hyperframes …` line in the PLV skill as `<HF> …`. Do NOT run
`npx hyperframes@latest`, `npx hyperframes skills update`, or
`npx skills add …` from this checkout — the first two test a different build
than the one you are changing, and `skills add --all` here deletes `skills/`
(see the repo CLAUDE.md warning).

**Prereq:** `<HF>` loads `packages/cli/dist/`. If `dist/` is missing or older
than your branch, run `bun install && bun run build` at `<REPO>` first, then
`<HF> doctor`.

## Pipeline — PLV steps with repo-native deltas

Run PLV Step 0 → Step 6 in order and pass each PLV gate. Deltas only:

### Step 0 · Setup

- Skip PLV's "keep this skill fresh" command (see above).
- No `BRIEF.md` → run the repo's `skills/hyperframes/SKILL.md` intent layer
  with route `skills/hyperframes/references/routes/product-launch-video.md`.
  Settle **sell or show** first; a show answer goes into `BRIEF.md` as intent.
- Init: `<HF> init "videos/<project>" --non-interactive --example=blank --skill=product-launch-video`
  from `<REPO>`, then `cd <PROJECT>` for every later step.

### Step 1 · Capture (the website is the input — no silent fallback)

- `<HF> capture "<URL>" -o ./capture --json`.
- `ok: false` or `capture/BLOCKED.md` → **stop and report** the blocker
  (bot wall, auth, DNS). Never drop into no-capture mode on your own; that
  produces a generic film the user did not ask for. Offer: a different URL,
  user-supplied screenshots, or an explicit switch to no-capture.
- Show-it-as-is briefs: the captured screens are the hero assets. Re-frame,
  crop, and pan them; do not redraw them as mock UI.

### Step 2–3 · Design system, storyboard, script

As PLV. Add one artifact before leaving Step 3: a draft **vector ledger** —
one line per cut: `from → to · technique · axis/dir · why`, following
motion-doctrine's Vector Law and the Z scale-sign rule. Show it with the
storyboard at the Step 3 approval gate.

### Step 4–5 · Visual design, frames

- Every frame-worker sub-agent prompt adds: "Load `motion-doctrine` and
  `cut-the-curve` from `<REPO>/.claude/skills/` before animating; scenes
  perform, never idle-wobble; the entry must be mid-flight at the cut."
- Pointer-led UI scenes: the worker also loads `oversized-cursor` (off-screen
  entry, tip-targeting, click ignites the next beat).
- Clip gating: a frame's first entry tween starts at its `data-start` with
  initial `autoAlpha: 0` — the usual cause of a zero-overlap seam failure.

### Step 6 · Finalize — stamp seams instead of injecting transitions

Replace PLV's `transitions.mjs inject` / `verify` pair with the doctrine pair.
Running both double-tweens the same frame wrappers (`#el-<NN-name>`, named
after each `compositions/frames/NN-*.html` file).

```bash
# ledger.json at <PROJECT> — schema: <DOCTRINE>/references/seam-gate.md
node <DOCTRINE>/scripts/seam-gate.mjs probe --t <cut> --project .   # find carrier selectors
node <DOCTRINE>/scripts/seam-stamp.mjs --ledger ledger.json --write index.html
node <DOCTRINE>/scripts/seam-gate.mjs verify --ledger ledger.json --project .
```

- Match-cuts / morphs get visibility sets only from the stamp; hand-author the
  carrier handoff, then re-verify.
- `#root` must paint an opaque stage ground (seam-craft white-flash guard).
  `<PLV>/scripts/assemble-index.mjs` paints it from `frame.md`'s canvas role
  (body falls back to `#000`); re-check after any hand edit.
- Then continue PLV Step 6 as written: voiceover carve (when a bed plays
  under voice), `<HF> lint`, `<HF> check`, `<HF> snapshot --at …` with
  cut −0.1s / +0.2s pairs, review pause, render.
- **Any edit to a frame's first/last ~1s, or a VO regen, re-opens that seam** —
  re-stamp and re-verify before presenting.

## Gates (all green before the review pause)

1. Every PLV gate, Steps 0–6.
2. `seam-gate.mjs verify` exits 0 (no FAIL; resolve WARNs or justify each).
3. `<HF> lint` and `<HF> check` — 0 errors.
4. Contact sheet inspected: no pop at any cut, captions present across the
   spoken window when the film is narrated.
5. Final reply: MP4 path, duration, the URL captured, and the frame ids so
   revisions can target a single frame.

## Project layout

```
videos/<project>/
├── BRIEF.md · hyperframes.json · frame.md
├── capture/                 # <HF> capture output (never hand-edited)
├── STORYBOARD.md · SCRIPT.md · audio_meta.json
├── ledger.json              # vector ledger → seam-stamp / seam-gate input
├── compositions/frames/NN-*.html
├── index.html               # assembled master; seams between <seams:auto> markers
└── renders/video.mp4
```
