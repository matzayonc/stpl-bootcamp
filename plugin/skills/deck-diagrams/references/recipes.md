# TikZ recipes

All assume the style vocabulary from the `deck-diagrams` skill (`box`, `arr`,
`lbl`) is declared on the picture.

---

## 1. Flow with a composite node

A node that holds internal structure is a raw `\node` with explicit dimensions
rather than the `box` style, because it needs a non-default size:

```latex
\node[box] (client) {Client};

\node[draw=dpaccent, line width=1pt, fill=dpcard,
      rounded corners=2pt,
      minimum width=2.4cm, minimum height=0.85cm,
      right=1.8cm of client] (pool) {};
\node[font=\tiny\itshape, text=dpmuted] at ($(pool.north)+(0,5pt)$) {Pool};
\node[font=\tiny\bfseries, text=dpaccent] at ($(pool.center)+(-0.55cm,0.08cm)$) {A};
\node[lbl]                                at ($(pool.center)+(-0.55cm,-0.18cm)$) {reserve};
% internal divider, inset from both ends
\draw[draw=dpmuted, line width=0.5pt]
      ($(pool.north)+(0,-0.12cm)$) -- ($(pool.south)+(0,0.12cm)$);
```

### Paired arrows for a two-way exchange

Offset the two directions so they read as a round trip, not one line:

```latex
\draw[arr] ([yshift= 3pt]client.east) -- ([yshift= 3pt]pool.west)
      node[midway, above, lbl] {$+$A};
\draw[arr] ([yshift=-3pt]pool.west)   -- ([yshift=-3pt]client.east)
      node[midway, below, lbl] {$+$B};
```

With three nodes (`A ↔ hub ↔ B`), use two such pairs. Vertical ordering of the
arrows encodes prerequisite order: the higher arrow happens first.

---

## 2. Plotted curve with reference coordinates

### Axes and the curve

```latex
\draw[draw=dpmuted, -latex, line width=1pt]
  (-0.3,0) -- (5.8,0) node[right, lbl] {$x$};
\draw[draw=dpmuted, -latex, line width=1pt]
  (0,-0.3) -- (0,5.8) node[above, lbl] {$y$};

\draw[domain=0.75:5.5, smooth, samples=100,
      draw=dpaccent, line width=2pt]
  plot (\x, {4/\x});

\node[font=\small\bfseries, text=dpaccent] at (4.4,1.3) {$x \cdot y = k$};
```

### A marked point with dropped coordinates

```latex
\draw[draw=dpmuted, dashed, line width=0.6pt] (2,0) -- (2,2) -- (0,2);
\node[lbl] at (2,-0.35) {$x_0$};
\node[lbl] at (-0.35,2) {$y_0$};
\filldraw[fill=dpfg, draw=dpaccent, line width=1.5pt] (2,2) circle (4pt);
```

### Δ annotations

`latex-latex` gives bidirectional arrowheads with no extra library:

```latex
\draw[draw=dpaccent, latex-latex, line width=0.8pt] (2,-0.65) -- (3,-0.65)
  node[midway, below, font=\tiny\bfseries, text=dpaccent] {$\Delta x$};
\draw[draw=dpaccent, latex-latex, line width=0.8pt] (-0.72,{4/3}) -- (-0.72,2)
  node[midway, left, font=\tiny\bfseries, text=dpaccent] {$\Delta y$};
```

### Tangent with a slope label

```latex
\draw[draw=dpmuted, line width=0.8pt] (0.6,3.4) -- (3.8,0.2)
  node[midway, above right, font=\tiny\itshape, text=dpmuted] {slope $= -p$};
```

---

## 3. Piecewise linear (a kink chart)

```latex
\draw[draw=dpaccent, line width=2pt] (0,0) -- (4,1) -- (5,5);
\draw[draw=dpmuted, dashed, line width=0.6pt] (4,0) -- (4,1) -- (0,1);

\node[lbl] at (4,-0.35) {$x_{\text{opt}}$};
\node[lbl] at (5,-0.35) {$100\%$};
\node[lbl] at (-0.5,1)  {$r_1$};

\node[font=\tiny\itshape, text=dpmuted]  at (2,-0.7)   {normal zone};
\node[font=\tiny\itshape, text=dpaccent] at (4.6,-0.7) {crisis};

\filldraw[fill=dpfg, draw=dpaccent, line width=1.5pt] (4,1) circle (3pt);
```

Choose the scale so the kink is unmissable. Slopes of 0.25 and 4 — a 16×
contrast — read instantly; 2× does not.

---

## 4. Multi-stop gradient bar

Each segment's `right color` equals the next segment's `left color`, which is
what makes the joins seamless:

```latex
\shade[left color=green!60!black,  right color=orange]              (0,0) rectangle  (8,1);
\shade[left color=orange,          right color=dpaccent]            (8,0) rectangle  (9,1);
\shade[left color=dpaccent,        right color=dpaccent!70!black]   (9,0) rectangle (10,1);
\shade[left color=dpaccent!70!black, right color=dpaccent!40!black](10,0) rectangle (11,1);
```

### Rounded corners

`\shade` ignores `rounded corners`. Clip, then stroke separately. Anything
drawn outside the scope (a threshold line, say) is not clipped:

```latex
\begin{scope}
  \clip[rounded corners=6pt] (0,0) rectangle (11,1);
  \shade[...] ...;   % every segment
\end{scope}
\draw[rounded corners=6pt, draw=dpmuted, line width=0.4pt] (0,0) rectangle (11,1);
```

### Threshold marker and staggered labels

```latex
\draw[draw=dpfg, line width=1.5pt] (9,-0.5) -- (9,1.55);
\node[font=\small\bfseries, text=dpfg, above] at (9,1.55) {threshold};

\node[lbl] at (0,-0.35)  {$0\%$};
\node[lbl] at (8,-0.35)  {$80\%$};
\node[lbl] at (9,-0.6)   {$90\%$};   % dropped lower to clear its neighbours
\node[lbl] at (10,-0.35) {$100\%$};
```

Set `x=0.95cm` on the picture to fit an 11-unit bar into the ~11.1cm Beamer
text width. Fonts are unaffected by coordinate scaling.

---

## 5. Two-state before/after

The most common staged reveal is two stages, not many: the "before" on `<1->`,
the "after" on `<2->`, in the same position so the eye compares them directly
rather than tracking movement.
