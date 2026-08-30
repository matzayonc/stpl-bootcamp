---
description: Start a new deck in an existing dynaprez project
allowed-tools: Bash, Read, Write, Edit, Glob
---

Create a new deck. The topic, if the user gave one, is: $ARGUMENTS

## Step 1 — locate the project

Confirm `preamble.tex` and `presentations/` exist in the working directory. If
not, tell the user to run `/deck-init` first and stop.

List `presentations/` to see the existing decks and pick the next free
`<index>`. Filenames are `<index>_<slug>.tex` — zero-padded index for ordering,
short lowercase slug. Never reuse an index.

## Step 2 — read the rules

Read the `deck-writing` skill before drafting a single frame, and the project's
own `style.md` or `CLAUDE.md` if it has one — project rules win over the
skill's defaults on audience, language, and narrative.

## Step 3 — agree the outline first

Do not draft slides yet. Propose the section structure and the one takeaway per
section, and get the user's sign-off. A deck whose skeleton is wrong is cheaper
to fix as a list than as LaTeX.

Ask about anything that changes the writing and that you cannot infer: what the
audience already knows, and whether this is recorded or live.

## Step 4 — draft

Copy frames from `presentations/99_example.tex` rather than writing them from
memory — it carries the correct form for every pattern.

Hold to the skeleton: `\maketitleframe`, agenda, sections, summary,
`\makeclosingframe`. Never author a section divider by hand. Never leave off the
closing frame.

## Step 5 — build and look

```bash
make <index>
pdftoppm -png -r 60 -f 1 -l 8 dist/<index>_<slug>.pdf /tmp/deckpg
```

Read the rendered pages. Overlay bugs — swallowed bullets on a static frame, a
blank opener on a block-first frame, diagram stages out of sync with bullets —
produce no LaTeX error and are only visible here. If the dedupe line reports
drops on a frame you wrote as an overlay opt-out, fix the source; see the
`deck-writing` skill's `references/overlays.md`.

Report the page count, the dedupe line, and anything you changed after looking.
