---
name: deck-branding
description: Visual identity for LaTeX Beamer decks — the six-color token system in brand.tex, block and card styles, code listing setup, title slide, section dividers, and footline. Use when rebranding a deck, changing colors, fonts, or logos, adding a syntax-highlighted language, or altering slide chrome.
---

# Branding a deck

Two files, one job each:

- **`brand.tex`** — every decision that is yours: palette, font, logo,
  backgrounds, the closing word. Rebranding means editing this file and
  nothing else.
- **`preamble.tex`** — layout and chrome, written entirely against the tokens
  `brand.tex` defines. Touch it only to change the *layout*, and update
  `references/preamble-map.md` when you do.

## The six color roles

Roles, not names. Change the hexes freely; keep the roles, because the preamble
and every diagram recipe refers to them by role.

| Token      | Role                                              |
|------------|---------------------------------------------------|
| `dpbg`     | Slide background                                  |
| `dpcard`   | Block / card surface                              |
| `dpborder` | Hairlines, progress-bar track                     |
| `dpaccent` | Brand accent — rules, bullet markers, keywords    |
| `dpfg`     | Primary text                                      |
| `dpmuted`  | Secondary text, axis lines, citations             |

Only `dpaccent` should read as "the brand colour". Using two accents on one
slide is the fastest way to make a deck look unresolved — reach for
`dpaccent!70!black` or `dpmuted` for a second emphasis level instead.

**Going light-background**: four tokens move, not two. Swap `dpbg` and `dpfg`,
darken `dpmuted` (one that reads correctly on near-black is illegible on white),
and lighten `dpcard` and `dpborder` — both were picked for a dark ground, and a
near-black progress-bar track across the top of a white slide is the tell.
`dpaccent` is the only token that carries over unchanged.

## Assets are optional

`\dplogofile`, `\dpbgdefaultfile`, and `\dpbgherofile` may be left empty, and a
path that does not resolve is skipped rather than failing the build. A deck with
no assets at all still renders correctly — accent bar, progress bar, and radial
glows are drawn in TikZ from the palette. Add assets when you have them; do not
block a deck on them.

## Blocks

Flat `tcolorbox` cards with a 3pt left accent rule, no shadow, no rounded
corners.

| Environment    | Left rule            | Surface                  |
|----------------|----------------------|--------------------------|
| `block`        | `dpaccent`           | `dpcard`                 |
| `alertblock`   | `dpaccent!75!black`  | `dpaccent!10!dpcard`     |
| `exampleblock` | `dpmuted`            | `dpcard`                 |

Each carries a leading `\pause` so the block lands on its own click after the
bullets. That is deliberate, and it is why a frame that *opens* with a block
needs a counter fix — see the `deck-writing` skill's `references/overlays.md`.

### `codeblock` — code synced to bullets

The same card **without** the auto-`\pause`, so it is visible from the current
overlay and its lines can reveal in step with the itemize above:

```latex
\begin{frame}[fragile]{Title}     % [fragile] is mandatory
  \begin{itemize}
    \item<1-> What the signature takes
    \item<2-> The line that does the work
  \end{itemize}
  \begin{codeblock}{example.py}
\begin{lstlisting}[style=reveal, language=Python]
(*@\onslide<1->@*)def transfer(src, dst, amount):
(*@\onslide<2->@*)    src.balance -= amount
\end{lstlisting}
  \end{codeblock}
\end{frame}
```

- `[style=reveal]` drops the listing's own background so the solid card shows
  through — without it, `\onslide` covers the per-line background too and the
  card goes ragged.
- `\onslide<k->` rather than `\pause` keeps each line's vertical space, so the
  card height stays constant and lines fade in place.
- Scaffolding (headers, closing braces) rides on `<1->` for context. Bullets
  with no matching line simply reveal nothing new.

## Adding a language to listings

`listings` ships definitions for most mainstream languages — pass
`language=Python` and it works. For a language it does not know, define it once
in `preamble.tex` near the `\lstset` block:

```latex
\lstdefinelanguage{Rust}{
  keywords={fn,pub,struct,impl,trait,let,mut,self,Self,match,return,enum,use},
  morecomment=[l]{//},
  morestring=[b]",
  sensitive=true,
}
```

Then either `\lstset{language=Rust}` for a deck-wide default, or
`language=Rust` per listing. Keyword lists are worth extending with the
domain's own type names — highlighting the API surface is most of the value.

## Chrome

Bullet markers are an em-dash (`dpaccent`), sub-items a smaller em-dash
(`dpmuted`). The footline is logo left, `n / total` right, no background. Frame
titles are centered bold text over a 2.2cm accent rule, no box. A progress bar
fills across the top of every content slide — set `\dpprogressbar` to anything
but `true` to drop it.

Title slide and section dividers are generated (`\maketitleframe`,
`\AtBeginSection`). Never author a divider by hand.

For the full map of what `preamble.tex` defines and where, see
`references/preamble-map.md`.
