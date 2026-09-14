# Superteam Poland — Presentation Branding

## Colors

| Role | Name | Hex |
|---|---|---|
| Background | `stpldark` | `#0B0E0F` |
| Card / block surface | `stplcard` | `#161A1B` |
| Progress bar track | `stplborder` | `#1E2526` |
| Brand accent | `stplred` | `#DC143C` |
| Primary text | `stplwhite` | `#FFFFFF` |
| Secondary / muted text | `stplmuted` | `#8A9BA8` |

## Logo

File: `images/stpl-logo.png` (white "St" monogram + red-and-white flag dot,
near-square, transparent background)

- Title slide: `width=3cm`, above the title
- Footline: `height=0.42cm`, left-aligned, lowered into the footline depth so
  it sits on the page number's line (anything under ~0.4cm turns the
  monogram into a blob)

## Layout

- Beamer theme: `default` (no built-in theme chrome)
- Text margins: `0.85cm` left and right
- Navigation symbols: hidden

## Frame Title

- Bold white text, no background box
- Short `2.2cm × 1.5pt` red rule below the title
- Top padding: `0.35cm`

## Progress Bar

- Position: very top of every slide
- Track: `stplborder`, filled portion: `stplred`
- Height: `2.5pt`
- Fills proportionally to `frame / totalframes`

## Title Slide

- Left edge: `5pt` solid red vertical bar (full height)
- Top-right + bottom-right: red radial glows at 7% and 4% opacity
- Content order: logo → title → `3cm` red rule → subtitle → author → `institute · date` (muted)

## Section Divider Slides (auto, `\AtBeginSection`)

- Full dark background with right-side red radial glow (7% opacity)
- Left edge: `5pt` solid red vertical bar
- Content: muted "Section N" label → large bold section name → `3cm` red rule

## Blocks

Implemented via `tcolorbox` (flat, no rounded corners):

| Block type | Left border | Background |
|---|---|---|
| `block` | `stplred` | `stplcard` |
| `alertblock` | `stplred!75!black` | `stplred!10!stplcard` |
| `exampleblock` | `stplmuted` | `stplcard` |

All block titles: bold white. No box rule, no shadow.

### Code reveal card (`codeblock`)

For slides where code should reveal **in step with the bullets** (each fragment
appearing on its bullet's overlay), use `codeblock` instead of `block`:

```latex
\begin{codeblock}{Title}
\begin{lstlisting}[style=reveal]
(*@\onslide<1->@*)first chunk        % shows with bullet 1
(*@\onslide<2->@*)second chunk       % shows with bullet 2
\end{lstlisting}
\end{codeblock}
```

- `codeblock` is the `block` card **without** the auto-`\pause`, so it is
  visible from overlay 1 and its lines can sync to the itemize bullets.
- `[style=reveal]` drops the listing's own background/frame so the card shows
  through solid — otherwise `\onslide` covers the per-line background too and it
  goes ragged.
- `\onslide<k->` (not `\pause`) keeps each line's vertical space, so the card
  height stays constant and lines fade in place. Frame must be `[fragile]`.

## Bullet Points

- Item marker: bold em-dash (`–`), color `stplred`
- Sub-item marker: small em-dash, color `stplmuted`

## Table of Contents

- Entry format: red `–` + section name
- Subsections: `stplmuted`

## Footline

- No background (`footline` color has empty `bg` so the background image
  shows through; using `normal text` would paint a flat `stpldark` band)
- Left: logo
- Right: `n / total` page count in tiny `stplmuted` text

## Web (Docusaurus)

`site/src/css/custom.css` is the CSS implementation of the tokens above
(`--stpl-dark`, `--stpl-card`, `--stpl-border`, `--stpl-red`, `--stpl-white`,
`--stpl-muted`). The mapping to Beamer chrome:

| Beamer | Web |
|---|---|
| Title page (hero bg, 5pt red bar, logo → title → rule → subtitle → institute · date) | `site/src/pages/index.tsx` |
| Frame title red rule (`2.2cm × 1.5pt`) | `h1`/`h2::after`, `56px × 2px` |
| `block` / `alertblock` / `exampleblock` | `:::note` / `:::warning` / `:::tip` admonitions, flat 3px left rule |
| `lstlisting` (card bg, red left rule, red keywords, muted comments) | code blocks + `site/src/theme/prism-stpl.ts` |
| Red `–` bullets, muted sub-bullets | `.markdown ul li::before` |
| Progress bar | 2.5px red line on top of the navbar |
| Footline (logo left, muted page count) | footer (logo, muted copyright) |
| Mermaid colors (`images/src/config.json`) | `themeConfig.mermaid` in `site/docusaurus.config.ts` |
| TikZ diagrams | rendered to SVG by `scripts/tikz2svg.py`, embedded in `<div className="diagram">` (`narrow` / `small` cap the width) |
| Screenshots (`images/*.png`) | `<div className="diagram screenshot">`, thin `stplborder` frame |

Font: Archivo via Google Fonts. Dark mode only; the theme switch is disabled.
Change a color here and in `preamble.tex` first, then mirror it in
`custom.css`.
