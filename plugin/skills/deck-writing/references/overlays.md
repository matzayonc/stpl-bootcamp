# Overlays — the reveal system and its two silent failures

`preamble.tex` sets `\beamerdefaultoverlayspecification{<+->}`, so every
`\item` and every helper block consumes the next overlay automatically. That
default is right for most frames. The two opt-outs below are where decks break,
and **neither failure produces a LaTeX error** — the build succeeds and the PDF
is wrong. The only way to catch them is to look at the rendered pages.

---

## Opt-out A — the static frame

For a frame that should land all at once (a diagram, a table, a quote, one
visual the speaker talks over), open it as:

```latex
\begin{frame}<1>{Title}
```

The frame renders overlay 1 only.

### The trap: swallowed bullets

The global `<+->` still hands item 2 overlay 2, item 3 overlay 3, and so on —
overlays this frame never draws. **Every bullet after the first silently
disappears from the PDF.** No warning, and the overlay deduplicator reports
nothing, because no duplicate page is produced.

A static frame can still carry caption bullets — they just must not *advance*.
Pin each one:

```latex
\begin{frame}<1>{Derivation}
  ... tikzpicture ...
  \begin{itemize}
    \item<1-> First caption line
    \item<1-> Second line      % without <1-> this vanishes
  \end{itemize}
\end{frame}
```

---

## Opt-out B — the manually choreographed frame

When a diagram advances in step with the bullets, hand-numbered TikZ scopes
(`visible on=<3->`) and `+`-driven bullets drift apart silently as bullets are
added or removed. Write explicit `\item<N->` on **every** bullet that syncs,
matching the scope numbers exactly. Verbose, but the bullets and the diagram
then share one source of truth.

Reach for this only when the diagram genuinely advances. A static diagram wants
opt-out A.

---

## The block-first blank slide

`block`, `alertblock`, and `exampleblock` self-reveal via a leading `\pause`
(see `preamble.tex`), so a helper block lands on its own click after the
bullets above it. That is intended.

But when a frame **opens** with a block — no always-visible content before it —
those leading pauses push the first content past overlay 1, and the frame opens
on one or more blank slides. `scripts/dedupe_overlays.py` strips interior
duplicate overlays but **keeps the first page of a frame**, so a blank opener
survives into `dist/`.

**Fix.** Immediately after `\begin{frame}`, roll the counter back by the number
of dead leading overlays:

```latex
\begin{frame}{Title}
  \addtocounter{beamerpauses}{-1}   % single block as the whole frame
  \begin{block}{...}
```

Two block-first columns need `-3`. The counter resets per frame, so it does not
leak into the next one.

**Diagnose.** Build without the dedupe pass and look for title-only pages:

```bash
latexmk -pdf -output-directory=/tmp/x presentations/<deck>.tex
pdftotext /tmp/x/<deck>.pdf - | less     # find the first page carrying content
```

N = (raw overlay of the first content) − 1.

**Caution.** If the frame also has a TikZ diagram keyed with absolute
`visible on=<k->`, the decrement shifts the `+`-driven bullets but *not* the
absolute diagram overlays. Re-key the diagram to the bullets' new numbers.

---

## Reading the dedupe report

Every build ends with a line like:

```
deck.pdf: 37 pages, dropped 6 (pre-dedup indices: 7,12,16,17,20,21)
```

Some drops are normal: a helper block's `\pause` produces one dead overlay that
the script cleans up. Drops on a frame you wrote as an *opt-out* are not
normal — they mean the overlay numbers were miscounted. Fix the source rather
than leaning on the script.
