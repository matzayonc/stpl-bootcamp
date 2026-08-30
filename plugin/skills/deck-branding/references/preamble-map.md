# What `preamble.tex` defines

A map for editing layout. Sections appear in this order in the file; each is
marked by a `%% ---- ... ----` banner.

| Section | Defines | Notes |
|---|---|---|
| Document class | `aspectratio=169`, `etoolbox`, `inputenc`, `fontenc` | Decks need no `\usepackage` of their own |
| `\input{brand}` | All tokens | Must precede every use; loaded before the font |
| Font | `\dpfontpackage` loaded via `\expandafter` | Empty macro ⇒ Computer Modern |
| TikZ | `calc`, `positioning`, `visible on` tikzset | `visible on` **must** be defined here, not in a frame — see caveat below |
| Base colors | `background canvas`, `normal text`, `structure` | |
| Asset helpers | `\dpiflogo`, `\dplogoat`, `\dpbgimage`, `\dpprogress` | All guard with `\IfFileExists` |
| Backgrounds | `\dpdefaultbg`, `\dpherobg` | Hero is used by title + dividers, then reset |
| Title metadata | Title/subtitle/author/institute/date colors, `\date{\the\year}` | |
| Frame title | Centered bold + 2.2cm accent rule | |
| Reveals | `\beamerdefaultoverlayspecification{<+->}` | Do not disable globally |
| Bullets | itemize/enumerate markers and colors | |
| Blocks | `dpbase` tcolorbox style, three block environments | Each opens with `\pause` |
| Listings | `\lstset` defaults | Add `\lstdefinelanguage` here |
| `codeblock` | Card without `\pause` + `reveal` listing style | |
| Table of contents | Accent em-dash entries | |
| Footline | Logo left, `n / total` right | |
| Title page | `\maketitleframe` + template | Logo block is skipped when no logo is set |
| Section dividers | `\AtBeginSection` | Do not author dividers by hand |
| Closing frame | `\makeclosingframe`, word from `\dpclosingword` | Mandatory last slide |

## The catcode caveat

`visible on` is built on `alt/.code args={<#1>#2#3}`, which uses `<` and `>`.
Inside a `\begin{frame}`, Beamer re-catcodes those characters for overlay
parsing. Defining that tikzset inside a frame fails with:

```
! Illegal parameter number in definition of \iterate.
```

It must stay in the preamble, before `\begin{document}`.

## Editing checklist

When you change layout in `preamble.tex`:

1. Update the table above if a section moved or a macro changed name.
2. Update the `deck-branding` skill if the change alters how a deck *author*
   writes slides (a new environment, a changed block semantic).
3. Rebuild the reference deck (`make 99`) and look at the pages — layout
   regressions do not surface as LaTeX errors.
