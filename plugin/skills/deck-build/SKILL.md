---
name: deck-build
description: Build, preview, and troubleshoot LaTeX Beamer decks — make targets and filename filters, the overlay deduplication pass, PPTX and Google Slides export, Docker builds, and reading LaTeX errors. Use when building or previewing a deck, exporting it, or diagnosing a failed or wrong-looking build.
---

# Building decks

## Layout

```
presentations/<index>_<slug>.tex   decks — index sorts, slug names
preamble.tex  brand.tex            shared layout + tokens
images/                            assets
scripts/dedupe_overlays.py         post-build overlay cleanup
build/  dist/                      intermediates / output PDFs
```

`<index>` is zero-padded and controls ordering; `<slug>` is short and
lowercase. Use `99_` for templates and scratch decks so they sort last.

## Commands

```bash
make              # build every deck to dist/
make 3            # any non-target token is a filename filter: builds *3*
make open-3       # build + open matching decks
make pptx-3       # build + convert matching decks to PPTX
make open PRES=1_intro   # explicit single deck
make clean
```

`PRES=` overrides the default deck for `open` and `pptx`; the default is the
first deck alphabetically.

## The dedupe pass

Every build ends by running `scripts/dedupe_overlays.py` over the PDF. It
rasterizes each page at 50 dpi, hashes it, and drops consecutive identical
pages — the dead clicks Beamer produces when a container opens on an overlay
that renders nothing new.

```
deck.pdf: 37 pages, dropped 6 (pre-dedup indices: 7,12,16,17,20,21)
```

**Read this line.** A few drops are normal — each helper block's `\pause`
costs one. Drops on a frame you wrote as a deliberate overlay opt-out mean you
miscounted; fix the source. The script cannot help with a *blank first page* of
a frame, which it always keeps by design — that is the block-first bug, and its
fix is in the `deck-writing` skill's `references/overlays.md`.

To inspect the raw overlays before deduplication:

```bash
latexmk -pdf -output-directory=/tmp/raw presentations/<deck>.tex
```

## Verify visually

A deck can build cleanly and still be wrong: swallowed bullets, a blank
opener, a diagram whose stages drifted out of sync. None of these raise a
LaTeX error. After a non-trivial change, render and look:

```bash
pdftoppm -png -r 60 -f 4 -l 9 dist/<deck>.pdf /tmp/pg   # pages 4–9
```

Then read the PNGs. This is the only reliable check for overlay bugs.

## Export

```bash
make pptx-<filter>
```

Converts via LibreOffice's PDF import filter — each slide becomes an image, so
text is not editable, but layout and fonts survive intact. Upload the `.pptx`
to Drive, or use **File → Import slides** in Google Slides.

## Docker

The bundled `Dockerfile` builds on `texlive/texlive:latest` plus LibreOffice.
`make` is the entrypoint, so it takes the same arguments:

```bash
docker build -t deck .
docker run --rm -v "$PWD/dist:/work/dist" deck          # make
docker run --rm -v "$PWD/dist:/work/dist" deck open-2   # make open-2
```

Mount a volume on `/work/dist` to get the PDFs back.

## Dependencies

`texlive` with `beamer`, `tcolorbox`, `listings`, `pgf/tikz`, and
`texlive-fontsextra` (for the bundled Archivo default); `latexmk`; `poppler`
(`pdftoppm`); `qpdf`; `python3`; optionally `libreoffice` for PPTX.

```bash
sudo pacman -S texlive-meta latexmk poppler qpdf python libreoffice-fresh   # Arch
sudo apt install texlive-full latexmk poppler-utils qpdf python3            # Debian
```

## Reading failures

- **`Illegal parameter number in definition of \iterate`** — a tikzset using
  `<`/`>` was defined inside a frame. Move it to `preamble.tex`.
- **`Missing \endcsname inserted` / verbatim errors around a listing** — the
  frame needs `[fragile]`.
- **`File not found` for an image** — paths resolve from the project root, not
  from `presentations/`. Brand assets in `brand.tex` are guarded and skip
  silently; `\includegraphics` in a deck is not.
- **`Undefined control sequence` on `\dp...`** — `brand.tex` is missing a
  macro the preamble expects. Compare against the template's `brand.tex`.
- **Build hangs or a stale error persists** — `make clean`, then rebuild.
  `latexmk` caches aggressively in `build/`.
