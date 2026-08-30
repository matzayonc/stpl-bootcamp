# dynaprez

LaTeX beamer presentation setup.

## Dependencies

- `texlive-meta` (or any TeX Live distribution with `beamer` and `texlive-fontsextra`)
- `latexmk`
- `poppler` — provides `pdftoppm`, used by the overlay deduplicator
- `qpdf` — used by the overlay deduplicator to rewrite PDFs
- `python3` — runs `scripts/dedupe_overlays.py` as part of every build
- `libreoffice` (optional, for PPTX export)

On Manjaro/Arch:

```bash
sudo pacman -S texlive-meta latexmk poppler qpdf python libreoffice-fresh
```

## Overlay deduplication

Beamer's `<+->` auto-overlay can produce visually identical adjacent pages —
dead clicks where an empty container opens but nothing changes on screen.
`scripts/dedupe_overlays.py` runs automatically after every PDF build: it
renders each page at low resolution, hashes it, and drops consecutive
duplicates in place using `qpdf`. No manual step required.

## Usage

```bash
make            # build all presentations → dist/*.pdf
make open       # open default presentation (first alphabetically)
make clean      # remove build artifacts
```

### Filter by name

Any token that is not a named target is treated as a filename filter — all presentations whose filename contains that string are built:

```bash
make 2          # build all files matching *2* → dist/2_defi.pdf, …
make pptx-2     # build + convert to PPTX for files matching *2*
make open-2     # build + open files matching *2*
```

### Single presentation

Override the default with `PRES=`:

```bash
make open PRES=1_intro
make pptx PRES=2_defi
```

Output PDFs go to `dist/`, PPTX files alongside them.

## Google Slides export

Convert a PDF to `.pptx` via LibreOffice, then upload to Google Drive or use **File → Import slides** in Google Slides:

```bash
make pptx           # default presentation
make pptx-2         # all presentations matching *2*
make pptx PRES=name # specific presentation
```

## Adding presentations

Create a new `.tex` file in `presentations/` using `\input{preamble}`. It will be picked up automatically by `make all` and the filter targets.

### Naming convention

Files must follow the pattern `<index>_<slug>.tex`:

- `<index>` — zero-padded number that controls ordering (e.g. `01`, `02`, … `99`)
- `<slug>` — short lowercase name with no spaces (use `_` within the slug if needed)

Examples: `1_intro.tex`, `2_defi.tex`, `99_example.tex`.

Use `99_` for templates or scratch files that should sort last and not appear in a regular run.

### Content & narrative

See [`style.md`](style.md) for the source of truth on titles, bullets, helper blocks, the mandatory closing `gn` slide, and the rest of the narrative conventions. See [`branding.md`](branding.md) for visual treatment.

## Font

Uses [Archivo](https://fonts.google.com/specimen/Archivo) via the `Archivo` LaTeX package (included in `texlive-fontsextra`).

## Publishing as a tool

`plugin/` packages this setup as a Claude Code plugin — the authoring
conventions as skills, plus a brand-neutral copy of the deck template. It is
independent of the decks in `presentations/`, which keep using the
Superteam-specific `preamble.tex` and `style.md` at the repo root.

```
/plugin marketplace add matzayonc/stpl-slides
/plugin install dynaprez@dynaprez
```

See [`plugin/README.md`](plugin/README.md).
