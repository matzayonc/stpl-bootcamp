# dynaprez

Beamer slide decks that look designed, authored by an agent that knows the rules.

A Claude Code plugin: four skills carrying the craft, two commands, and a
themeable deck template with an overlay-deduplicating build.

## Install

```
/plugin marketplace add matzayonc/stpl-slides
/plugin install dynaprez@dynaprez
```

Then, in an empty directory:

```
/deck-init      # scaffold the project, set the brand
/deck-new       # start a deck
```

## What is in it

**Skills** load on their own when the work calls for them:

| Skill | Covers |
|---|---|
| `deck-writing` | Slide titles, bullets, helper blocks, columns, deck skeleton, reveals, the pre-ship checklist. References: narrative arc and term introduction; the overlay system and its two silent failure modes. |
| `deck-branding` | The six-token palette in `brand.tex`, block and card styles, the `codeblock` reveal card, listings languages, chrome. Reference: a map of `preamble.tex`. |
| `deck-diagrams` | TikZ style vocabulary, staged reveals synced to bullets, Beamer caveats. Reference: worked recipes for flows, curves, kink charts, gradient bars. |
| `deck-build` | Make targets and filename filters, the dedupe pass, visual verification, PPTX export, Docker, reading LaTeX errors. |

**Commands**: `/deck-init` scaffolds a project and sets its brand;
`/deck-new` takes a deck from outline to built PDF.

**Template** (`template/`): `preamble.tex` (layout, ~275 lines),
`brand.tex` (every decision that is yours), `Makefile`, `.latexmkrc`,
`Dockerfile`, `scripts/dedupe_overlays.py`, and `presentations/99_example.tex`
— a reference deck showing each supported pattern exactly once.

## Design

**One file to rebrand.** `brand.tex` holds six colour roles, a font, three
optional asset paths, and the closing word. `preamble.tex` is written entirely
against those tokens. Unset or missing assets are skipped, never fatal — a deck
with no logo and no background images still renders correctly.

**Overlays are the hard part.** Beamer's incremental reveal has failure modes
that produce a clean build and a wrong PDF: a static frame swallows every bullet
after the first, a block-first frame opens on a blank slide, hand-numbered
diagram stages drift out of sync with `<+->` bullets. The skills document all
three with their fixes, and every command ends by rendering pages to PNG and
looking at them — because nothing else catches these.

**The dedupe pass.** Helper blocks self-reveal via `\pause`, which costs one
dead overlay each. `scripts/dedupe_overlays.py` hashes rendered pages and drops
consecutive duplicates after every build. Its report is a diagnostic, not just
cleanup: drops on a frame written as a deliberate opt-out mean the overlay
numbers are wrong.

## Requirements

`texlive` (beamer, tcolorbox, listings, pgf, fontsextra), `latexmk`, `poppler`,
`qpdf`, `python3`. Optional: `libreoffice` for PPTX export. Or use the bundled
`Dockerfile`.
