---
description: Scaffold a new Beamer deck project in the current directory and set its brand
allowed-tools: Bash, Read, Write, Edit, Glob
---

Set up a dynaprez deck project in the current working directory.

## Step 1 — check the ground

List the current directory. If `preamble.tex` or `presentations/` already
exists, stop and report what is there: this command scaffolds, it does not
overwrite. Suggest `/deck-new` instead if the project is already set up.

## Step 2 — copy the template

```bash
cp -rn "${CLAUDE_PLUGIN_ROOT}/template/." .
```

`-n` so nothing existing is clobbered. This brings in `preamble.tex`,
`brand.tex`, `Makefile`, `.latexmkrc`, `Dockerfile`, `.gitignore`,
`scripts/dedupe_overlays.py`, `images/`, and the reference deck
`presentations/99_example.tex`.

## Step 3 — set the brand

Read the `deck-branding` skill, then ask the user for whatever you cannot
infer from the repo (a `README`, an existing site, or brand assets already in
the directory are fair game to check first):

- accent colour, and whether the deck is dark or light background
- a logo file, if they have one
- organisation name for the title slide

Apply the answers to `brand.tex` only. Leave asset macros empty rather than
pointing at files that do not exist — unset assets are skipped cleanly.

## Step 4 — verify

```bash
make 99
```

Confirm `dist/99_example.pdf` exists and report the dedupe line. Then render a
couple of pages and actually look at them, so a broken palette is caught now:

```bash
pdftoppm -png -r 60 -f 1 -l 2 dist/99_example.pdf /tmp/deckcheck
```

## Step 5 — hand off

Tell the user: `99_example.tex` is the pattern reference — copy frames from it
rather than writing them from memory — and `/deck-new` starts a real deck.
Mention that the build depends on `latexmk`, `poppler`, and `qpdf` if any step
failed for a missing binary.
