---
name: deck-diagrams
description: TikZ diagrams inside LaTeX Beamer slides — the shared node and arrow style vocabulary, staged reveals synced to bullets, flow diagrams, plotted curves, and the Beamer-specific caveats that make TikZ fail silently. Use when adding or editing any diagram, chart, or graph on a slide.
---

# Diagrams on slides

Prefer TikZ over an imported image for anything structural: it inherits the
brand palette, scales with the slide, and stays editable. Import a raster only
for a real screenshot of a real interface.

Every diagram lives in `\begin{center}...\end{center}` inside a frame.
`calc` and `positioning` are already loaded by `preamble.tex`.

## The style vocabulary

Declare these per `tikzpicture`. Reusing the same four styles across a deck is
most of what makes the diagrams look like one system:

```latex
\begin{tikzpicture}[
  every node/.style={font=\scriptsize\bfseries},
  box/.style={draw=dpaccent, line width=1pt, fill=dpcard, text=dpfg,
              rounded corners=2pt, minimum width=1.4cm,
              minimum height=0.55cm, align=center},
  arr/.style={-latex, draw=dpaccent, line width=1pt},
  lbl/.style={font=\tiny\itshape, text=dpmuted},
]
  \node[box] (a) {Client};
  \node[box, right=1.8cm of a] (b) {Server};
  \draw[arr] (a) -- node[lbl, above] {request} (b);
\end{tikzpicture}
```

Colors come from `brand.tex` — never hardcode a hex in a diagram. Mixing is
fine: `dpaccent!70!black`, `green!60!black`.

## Staged reveals

Wrap each stage in a scope keyed to the overlay of the bullet that introduces
it. Diagram stages do **not** consume their own counter — they overlay the
bullets' existing overlays:

```latex
\begin{scope}[visible on=<2->]
  \node[box, right=1.8cm of pool] (borrower) {Borrower};
  \draw[arr] (pool) -- (borrower);
\end{scope}
```

Two rules behind this:

- **Scope, not per-node style.** `opacity=0` on a `\draw` does not hide a
  `node[midway]` label on that path. A scope propagates both `opacity` and
  `text opacity` to everything inside, labels included.
- **`opacity=0`, not `\only`.** `\only` removes the element, the bounding box
  shrinks, and the diagram jumps between overlays. `opacity=0` keeps the
  geometry and the diagram stays still.

For a stage that is one node plus one labelled arrow, put `visible on` directly
on the node — but keep the scope around the arrow, because its label needs the
scope's text-opacity propagation. Declaring the node early (invisible) locks the
bounding box so nothing reflows when the stage arrives.

Pick stage numbers from each element's narrative role, not from a count. Then
verify: hand-numbered stages and `<+->` bullets drift apart silently when a
bullet is added. See the `deck-writing` skill's `references/overlays.md` — a
choreographed frame needs explicit `\item<N->` on every bullet.

## Caveats that fail silently

- **A diagram-only frame must open `\begin{frame}<1>{Title}`** — otherwise
  Beamer emits an overlay copy per bullet. And on such a frame every bullet
  after the first vanishes unless tagged `\item<1->`.
- **`visible on` cannot be defined inside a frame.** Beamer re-catcodes `<`
  and `>`; it lives in `preamble.tex`. Symptom:
  `! Illegal parameter number in definition of \iterate.`
- **`\shade` ignores `rounded corners`.** Clip first, then stroke the border
  separately.
- **Coordinate scaling does not scale fonts.** `x=0.95cm` on the picture
  changes geometry only; label sizes stay put.

## Recipes

`references/recipes.md` has worked, copy-ready code for: two- and three-node
flow diagrams with paired arrows, plotted curves with dashed reference
coordinates and Δ annotations, piecewise-linear kink charts, and multi-stop
gradient bars with threshold markers.
