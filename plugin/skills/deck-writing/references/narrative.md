# Narrative — sequencing a deck

## The three-beat rhythm

Build a section on:

1. **Problem** — a tension the audience feels without any jargon
   ("your money lives on someone else's server").
2. **Mechanism** — how the technology resolves it ("thousands of independent
   nodes hold the same state; a dishonest one is outvoted").
3. **Benefit** — what becomes possible ("code that runs exactly as written,
   with no single party able to intervene").

This is the shape of a *section*, not a per-slide checklist. Apply it wherever
it fits — a section, a sub-topic, or one dense slide.

## Audience model

Treat the audience as progressive. Establish what the first session assumes,
then let each later session build on the names introduced earlier without
re-deriving them. Write down that assumed baseline somewhere in the project
(`style.md` or `CLAUDE.md`) — it is the single most useful thing to pin down
before drafting, and it is the decision this skill cannot make for you.

When unsure whether a term is known: if nothing earlier in the material
introduced it, treat it as new.

## Introducing a new term

1. Set up the problem in plain language, without the technical word.
2. Describe the mechanism, still without the word.
3. *Then* name it, bolded, as a label: `\textbf{Byzantine Fault Tolerance (BFT)}`.

Optional for synonyms, restatements, or terms already introduced.

**Acronyms.** The debut pairs the full name and the acronym inside one
`\textbf{}`: `\textbf{Automated Market Maker (AMM)}`. After that, the acronym
alone. Do not repeat the expansion — unless a later session references it and
you are unsure the audience has seen it, in which case re-expand.

## Analogies are required

Every genuinely new concept gets at least one analogy from everyday life
*before* it is formalized. Build a small recurring toolkit for the domain and
reuse it, so the analogies compound rather than each one costing fresh setup.
A generic starting set: the bank (custodial trust), the notary (verification
and irrevocability), the shared spreadsheet (concurrent state), the contract
(enforceable pre-agreed terms).

Reach for a fresh analogy when one does not land — but never skip the step.
Formalism without analogy is the fastest way to lose the room.

## Acknowledge difficulty

When a concept is genuinely hard, say so on the slide. A muted line —
`\textcolor{dpmuted}{This one is hard — pause and come back to this slide}` —
reframes struggle as expected rather than as failure, and is more honest than
glossing over it.

## Citations

When a slide claims a specific number, quote, or verifiable fact, attach a
muted source under the block or bullet:

```latex
\textcolor{dpmuted}{\tiny source.example/docs \textperiodcentered\ 2026}
```

Cite where it earns its keep — a key number, a quoted claim, a chart's data
source. Do not cite analogies, definitions, or common knowledge.

## Voice

- Short declarative sentences. The slide is the speaker's prompt, not a script.
- Active voice over passive; verbs over nominalizations.
- Consistent grammatical person throughout the deck — pick one and hold it.
- No exclamation marks. No emojis.

## Recorded vs live

Style is identical; usage differs.

- **Recorded** is self-paced: incremental reveal does the pacing, `\note{}`
  preserves the spoken line, and a slide should be comprehensible without the
  audio.
- **Live** typically opens with 5–10 theory slides, then hands off to a demo or
  code-along. Mark the handoff with its own `\section` divider.

## Speaker notes

Beamer's `\note{...}` is available and optional. Use it when recording, or when
a slide's brevity hides something the speaker must say out loud.

## Influences

Reynolds, *Presentation Zen* (one idea per slide, restraint); Tufte,
*Beautiful Evidence* (when you do show data, make it dense and honest);
Matuschak & Nielsen, *Quantum Country* (analogies before formalism, naming
difficulty explicitly); MIT 6.831 graphic-design notes (the squint test,
Gestalt grouping). None are required reading — they are where the reasoning
lives when a rule above feels arbitrary.
