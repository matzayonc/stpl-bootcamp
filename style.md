# Superteam Poland — Presentation Style Guide

The source of truth for *content* and *narrative* in this repository — the
Beamer decks (§1–§15) and the web chapters under `site/docs/` (§16).
Pairs with `branding.md` (visual chrome) and `README.md` (build & filenames).
See [`style-decisions.md`](style-decisions.md) for the interview that produced
this doc — the *why* behind each rule lives there.

If a rule here conflicts with one of those files, this document wins for narrative
decisions; `branding.md` wins for colors, spacing, and visual treatment.

---

## 1. Why this guide exists

We teach blockchain to a Polish-speaking audience that starts at **zero
blockchain experience**. The recorded part of the course also functions as a
filter — a student who cannot follow the slides will not pass the gating quiz
and will not reach the live workshops. That motivates everything below:
slides exist to make a single takeaway land for a newcomer, not to be a
faithful transcript of what a senior engineer already knows.

The patterns here come from the recorded "Dlaczego blockchain i Solana?"
lecture and from a handful of well-known sources on slide design (see §15).
You do not need to read those sources to follow this guide.

---

## 2. Audience model

Treat the audience as **progressive**:

- The first lesson assumes zero blockchain knowledge. Every primitive
  (blok, węzeł, klucz, podpis, smart kontrakt) is introduced from a real-world
  problem before its technical name is spoken.
- Each subsequent lesson is allowed to assume the technical names introduced
  in earlier lessons. Do not re-derive concepts the curriculum already covered.
- Programming literacy is assumed throughout (the audience can read code,
  understands what a function or a CLI is). Do *not* assume Rust, Anchor,
  Solana RPC, or DeFi vocabulary.

When in doubt about whether a term is known: if the curriculum has not yet
introduced it in a prior lesson, treat it as new and hook it from a problem.

---

## 3. The narrative arc (aspirational)

The recorded reference lecture is built on a three-beat rhythm:

1. **Problem** — a tension the audience can feel without any blockchain
   vocabulary ("your money lives on someone else's server").
2. **Mechanism** — how the technology resolves the tension ("thousands of
   independent nodes hold the same state; a dishonest one is outvoted").
3. **Benefit** — what becomes possible because of the mechanism ("code that
   runs exactly as written, without a single party able to intervene").

This is the *recommended* shape for a section, not a per-slide checklist.
Apply it at the granularity where it fits — a section, a sub-topic, or a
single slide if the slide is dense enough.

---

## 4. The slide

### 4.1 Title

- One thought. Roughly **2–4 words**.
- Noun phrase or short question. Both are fine
  ("Prywatne serwery", "Czym jest Solana?").
- The title should be a label, not a summary. The body of the slide carries
  the content.

### 4.2 Bullets

- **3–5 bullets** per slide.
- Bold a key term per bullet **where it helps** — not as a quota. Use `\textbf{}`
  on the word a student should remember from that line.
- One line per bullet whenever possible. Multi-line bullets are a smell that
  the slide is trying to do too much.

### 4.3 Helper block (mandatory on concept slides)

A *concept slide* — one that introduces or unpacks a technical idea — must
end with **one** helper block. Pick the type by semantic role:

| Block          | Use for                                        |
|----------------|------------------------------------------------|
| `block`        | Definitions, key numbers, named formulas       |
| `alertblock`   | Problems, risks, things to watch out for       |
| `exampleblock` | Effects, illustrations, real-world examples    |

Helper-block bodies stay short: 2–3 lines, or a 3-item sub-list. If the helper
needs more than that, it is the slide.

Slides that do *not* need a helper block:

- Transition / section-bridge slides.
- Pure A-vs-B comparison slides (the comparison is the content).
- Summary / recap slides.
- The closing `gn` slide.

### 4.4 Two-column comparison

Reach for `\begin{columns}` **only** for direct opposition between two
parallel concepts ("Co widzisz / Czego nie wiesz", "Lender / Borrower",
"Prywatny serwer / Blockchain"). If the two halves are not contrasting,
stack blocks vertically instead.

### 4.5 Animation

The preamble sets `\beamerdefaultoverlayspecification{<+->}`. **Keep it as
the default.** Bullets reveal one at a time so the speaker controls pace
and the student's eye does not race ahead. Two opt-outs exist for cases
where the default does the wrong thing:

**(a) Static frame — diagram or table that lands all at once.** Open with
`\begin{frame}<1>{Tytuł}`. The whole frame is rendered on a single overlay
and no `<+->` ticks fire. Use this for: a pure TikZ diagram with no
synchronized bullets, a table, a static quote, a single visual the speaker
wants to talk over without clicking. Existing examples: `2_amm.tex:215`,
`3_lending.tex:240` (the Utilization Rate chart), `1_paradigm.tex:403,450`
(the Web3 stack map).

**(b) Manually-choreographed frame — TikZ stages synchronized with
bullets.** When a diagram reveals in step with the surrounding itemize,
the default `<+->` and the hand-numbered `\begin{scope}[visible on=<N->]`
counts drift apart silently when bullets are added or removed. Convention:
write explicit `\item<N->` overlays on **every** bullet that needs to
sync, matching the TikZ scope numbers exactly. The cost is verbosity;
the benefit is that the bullets and the diagram share one source of
truth — adding a bullet no longer silently breaks the diagram. The
worked example is `1_paradigm.tex:198-277` ("Read vs Write"), which
choreographs eight overlays across two columns. Reach for this only
when the diagram actually needs to advance with the bullets — if the
diagram is static, prefer (a).

When the post-build `scripts/dedupe_overlays.py` reports dropped pages on
an opt-out frame, the author miscounted overlays. Fix the source rather
than relying on the script.

---

## 5. Lesson skeleton

```
\maketitleframe                         % title slide
\begin{frame}{Plan} \tableofcontents    % toc
... \section{...} \begin{frame}{...}    % content sections
\begin{frame}{Podsumowanie} ...         % free-form recap (see §5.2)
\begin{frame}[plain] ... gn ...         % closing slide (mandatory)
```

### 5.1 Kickoff-only slides

The very first lesson of the course adds an "O mnie" and a "Plan kursu"
slide before `\tableofcontents`. Subsequent lessons skip these and go
straight to the toc.

### 5.2 Summary

A summary slide is recommended at the end of any lesson with more than one
section. The shape is free — bullets, one or two blocks, or a side-by-side
recap of two themes are all acceptable. The goal is that a student who only
remembers the summary slide still leaves with the lesson's headline.

### 5.3 Section dividers

Generated automatically by `\AtBeginSection`. Do not author them by hand.
Pick section names that read as standalone phrases — they appear large on
the divider slide.

### 5.4 Closing slide (`gn`)

Every deck ends with the `gn` sign-off slide, immediately before
`\end{document}`. Do not add section headings or any content after it.

```latex
% ================================================================
\begin{frame}[plain]
  \begin{center}
    \vfill
    {\Huge\bfseries\color{stplwhite} gn}
    \vfill
  \end{center}
\end{frame}
```

---

## 6. Introducing terms

For a **new domain concept** (one the curriculum has not yet introduced),
follow the recorded-lecture pattern:

1. Set up the problem in plain Polish, without the technical word.
2. Describe the mechanism in plain Polish, still without the word.
3. *Then* name it, bolded, as a label: `\textbf{Byzantine Fault Tolerance (BFT)}`.

For synonyms, restatements, or terms already introduced earlier in the
course, this dance is optional — you can use the technical name directly.

### 6.1 Analogies are required for new concepts

Every new technical concept gets at least one analogy from Web2 or daily
life *before* it is formalized. The recurring toolkit:

- **bank** for custodial intermediaries and trust
- **notariusz** for verification and irrevocability
- **giełda** for matching and price discovery
- **arkusz Google** for shared state and concurrent edits
- **kontrakt** for enforceable, pre-agreed terms

Reach for a fresh analogy when one of these does not land — but never skip
the step. Formalism without analogy is the fastest way to lose the room.

### 6.2 Acknowledge difficulty

When a concept is genuinely hard (consensus, cryptographic signatures, AMM
math), say so on the slide. A muted line such as `\textcolor{stplmuted}{To
jest trudne — zatrzymaj film i wróć do tego slajdu}` reframes struggle as
expected, not as failure, and is more honest than glossing.

### 6.3 Acronyms on first use

When a term is commonly referenced by an acronym, the debut form pairs the
full name with the acronym in parentheses, both inside the same `\textbf{}`:

```latex
\textbf{Byzantine Fault Tolerance (BFT)}
\textbf{Automated Market Maker (AMM)}
\textbf{Loan-to-Value (LTV)}
```

After the debut, use the acronym alone (`BFT`, `AMM`, `LTV`). Do not repeat
the expansion. If a later lesson references the term and you are unsure
whether the audience has seen it, treat it as new and re-expand.

---

## 7. Anglicisms and naming

Keep canonical industry terms in English. Polish learners need to recognize
them when they read docs, GitHub, or Discord:

- `smart kontrakt`, `permissionless`, `composable`, `slippage`, `AMM`,
  `Health Factor`, `Utilization Rate`, `LP`, `oracle`, `rug pull`.

Do not invent Polish translations for these. A short Polish gloss in
parentheses is fine the *first* time a term debuts in a lesson, but do not
repeat it.

Polish words are still preferred for everything else (sieć, węzeł, podpis,
klucz, opłata, blok, rejestr). The test: would a senior Solana engineer
writing on Discord use the English term? If yes, keep it English.

---

## 8. Math and code on slides

### 8.1 Math

- **Displayed equations** (`\[ ... \]`) live inside a `\begin{block}` whose
  title names the formula (e.g., "Loan-to-Value", "Niezmiennik").
- **Inline math** (`$ ... $`) is for variable references in prose.
- Worked examples (plug numbers into the formula) belong in an
  `exampleblock`, not in the definition block.

### 8.2 Code

- Short identifiers, commands, filenames: `\texttt{cargo build}`,
  `\texttt{solana-cli}`.
- Multi-line snippets: use the `listings` package inside a `\begin{block}`
  titled with the file or context. Keep snippets under ~10 lines — anything
  longer needs to be split or shown live, not on a slide.
- **Revealing code in step with bullets**: when a snippet's fragments map to
  the bullets above it, reveal each fragment on its bullet's overlay. Use the
  `codeblock` card + `\begin{lstlisting}[style=reveal]` and tag lines with
  `(*@\onslide<k->@*)` (see `branding.md` → Code reveal card). Do **not** use
  `\pause` inside a normal titled `block` listing — its auto-`\pause` desyncs
  the code from the bullets and the per-line background goes ragged.
  - No 1:1 mapping? A fragment appears only on the bullet that names it;
    bullets without a matching line reveal nothing new. Structural scaffolding
    (struct headers, braces) rides on overlay 1 for context.
  - No bullets on the frame (code-only): plain `\begin{lstlisting}` with
    `\pause` between chunks is fine — the card just grows.
- Theory lessons should not need code. If a theory slide reaches for code,
  consider whether the explanation needs an analogy instead.

---

## 9. Images, diagrams, screenshots

Use images **liberally** when they support a key concept. The categories that
earn their place:

- **TikZ diagrams** for architecture and flow (network topology, account
  model, swap flow, transaction lifecycle). TikZ keeps brand colors
  consistent with the rest of the deck — prefer it for anything that needs
  to look native to the slide.
- **Real screenshots** of wallets, explorers, and live apps (Phantom, Solana
  Explorer, Orca, Kamino, Anchor IDL viewer) when explaining a real
  interface the student will use.
- **Decorative icons** — small, used sparingly to mark recurring slide
  types or callouts. Color must align with `branding.md` (white, muted, red).

Store assets under `images/`. Reference them with `\includegraphics`. Never
include stock photos, unrelated illustrations, or anything that does not
serve the concept on screen.

### 9.1 The squint test

Before shipping a slide, look at it at half size or from across the room.
The most important element on the slide should still be the one your eye
lands on. If it is not, increase contrast, drop a bullet, or move the
helper block.

---

## 10. Citations and sources

When a slide claims a specific number, quote, or fact a student might want
to verify, attach a muted citation:

```latex
\textcolor{stplmuted}{\tiny solana.com/docs · 2026}
```

Place it on the bottom-right of the relevant block or under the bullet.
Cite where it earns its keep — a single number on a key-numbers block, a
quoted claim, a chart's data source. Do not cite analogies, definitions,
or anything that is common knowledge in the ecosystem.

---

## 11. Voice and tone

- **Impersonal Polish, third person.** "Tysiące węzłów przechowuje stan."
  "Kod wykonuje się dokładnie tak jak napisany." No `Pan/Pani`, no `ty`.
- Short, declarative sentences. The slide is the speaker's prompt, not
  their script.
- Active voice over passive. Verbs over nominalizations.
- No exclamation marks. No emojis on slides.

---

## 12. Speaker notes

Beamer's `\note{...}` is available. Use it when:

- You are recording a lesson and want the spoken line preserved.
- A slide's brevity hides a point the speaker must mention out loud.

Live sessions usually skip notes. They are optional, not required.

---

## 13. Recorded vs live lessons

Slide *style* is identical for both. The differences are usage:

- **Recorded lessons** are self-paced. The incremental-reveal default
  paces the eye; favor `\note{}` for the spoken script; aim for a slide
  to be comprehensible without the audio.
- **Live lessons** start with a short theory block (5–10 slides) in this
  same style, then transition to a code-along. Use a `\section{Warsztat}`
  divider to mark the handoff from slides to terminal.

---

## 14. Quick checklist before shipping a slide

- [ ] Title is 2–4 words and names one thought.
- [ ] 3–5 bullets, bolded keyword where useful, one line each.
- [ ] Concept slide ends in one helper block, picked by semantic role.
- [ ] New term is hooked by a problem before being named.
- [ ] At least one analogy for genuinely new concepts.
- [ ] Columns only used for direct A-vs-B opposition.
- [ ] Incremental reveal still on, or override is intentional.
- [ ] Squint test passes — the eye lands on the right element.
- [ ] Specific numbers and quotes carry a muted citation.
- [ ] No emojis, no prose paragraphs, no Polish translation of canonical
      English jargon.

---

## 16. Web chapters (`site/docs/`)

The website is not a transcript of the decks. It is a **textbook** built on
the model of *The Rust Programming Language*: full prose chapters that a
reader works through alone, with numbered listings, real tool output and
exercises. The decks are the spine — every chapter follows its deck's
section order and vocabulary — but the chapter may go deeper than the
slides and may add material the lecture skips. Chapter `05-konta` is the
worked template; when a rule below is unclear, that chapter is the answer.

Everything in §2 (progressive audience), §6 (problem → mechanism → name),
§6.1 (analogies), §7 (anglicisms) and §11 (voice) applies verbatim. What
follows is only what differs from slides.

### 16.1 Files

```
site/docs/NN-<topic>/
  _category_.json     # label, position, link → index
  index.md            # opening, Zawartość, Podsumowanie, Ćwiczenia
  01-<slug>.md        # one page per major section of the deck
  02-<slug>.md
  …
```

- `NN` is the topic number (`01`–`07`; `08` holds the quizzes from
  `exam/*.md`, `09` is reserved for the first-program walkthrough).
- Every page has frontmatter `title`, `description` (one sentence, used by
  the sidebar tooltip and search), `sidebar_position`, and `slug`.
- Pages are 150–300 lines. A section of the deck that needs more than that
  is two pages; one that needs less is folded into a neighbour.

### 16.2 Page shape

1. **Opening paragraph** — the question this page answers, in plain Polish,
   tied to the previous page's closing sentence. No "in this chapter we
   will"; the question *is* the intro.
2. **`##` sections** in the deck's order. Each section is prose: the problem,
   the mechanism, then the bolded term (§6). Bullet lists only for real
   enumerations — steps of an algorithm, rows of a checklist, the three
   rules of a mechanism. Never a bullet that is a full sentence in disguise.
3. **Hand-off sentence** — the last paragraph names the question the next
   page answers.

The hardest page of a chapter opens with `:::note To jest trudne` (the web
form of §6.2). Do not use it anywhere else in the chapter.

### 16.3 Listings

Every code, CLI, JSON or log block is a numbered listing:

```md
```bash
$ solana account <ADRES>
…
```

<div className="listing"><strong>Listing 5-3.</strong> Konto tokena USDC: 165 bajtów danych, właścicielem jest Token Program.</div>
```

- Number is `N-k`: `N` = topic number without the leading zero, `k`
  counts up through the chapter's pages in reading order (`index.md`
  has no listings). Renumber the chapter when inserting one.
- The caption states what the reader should notice, not what the code is.
- Prose refers to listings by number ("Listing 5-3 pokazuje…") and then
  **walks through it** — field by field for output, line by line for
  code. A listing that gets no walkthrough is a listing the page does
  not need.
- CLI listings start with `$ ` and show the real command including
  `--url`/`-u` when it matters. Use `<ADRES>`-style placeholders only
  in "how to" snippets, never in captured output.
- Rust listings are complete enough to compile in context: keep
  `use`, `declare_id!`, struct headers — no `// ...` inside a struct
  the reader is meant to type.

### 16.4 Real output

Output is **captured, not reconstructed**. `solana`, `anchor`, `spl-token`,
`cargo`, `rustc` and `curl` against a public RPC are the sources; the
Explorer and Phantom are captured as screenshots.

- Read from **mainnet** for public accounts (USDC mint, Token Program, a
  large exchange wallet). Write only on **devnet** with a throwaway
  keypair.
- Trim long output with a line containing `...` and say so in the
  caption. Never add, reorder or "fix" a line.
- Numbers that drift (rent rate, validator count, block height, fees)
  are measured at writing time; the prose says "w chwili pisania" and the
  chapter's exercises ask the reader to re-measure.
- No API keys, no private RPC URLs, no personal addresses. Placeholder
  program IDs must be valid base58 (`Vau1t111…`, `Lic1111…`).
- Compiler errors are shown in full — the `help:` block is part of the
  lesson.

### 16.5 Blocks and diagrams

Admonitions keep the semantic roles of §4.3, one role per block:

| Slide | Web | Role |
|---|---|---|
| `block` | `:::note Tytuł` | definition, rule, invariant |
| `alertblock` | `:::warning Tytuł` | risk, pitfall, cost |
| `exampleblock` | `:::tip Tytuł` | analogy, worked example, effect |

- Analogy blocks are titled `Analogia — <obraz>` and **chain within a
  chapter**: the file in *Anatomia konta* becomes the path in *Adres i
  PDA* and the deposit in *Koszt*; the chapter's `Podsumowanie` ends
  with the full chain in one `:::tip Analogia na koniec`.
- A page has as many blocks as it has sections that need one; the
  one-block-per-slide rule does not apply. Two blocks in a row is a
  smell.
- Diagrams are the deck's TikZ pictures rendered by `make diagrams`,
  embedded as `<div className="diagram">` (`narrow`/`small` cap the width)
  with alt text that reads as a sentence. Screenshots use
  `<div className="diagram screenshot">`. Do not draw new diagrams for the
  web that the deck does not have; add them to the deck first.

### 16.6 Cross-references

- Link on the **first mention** of a concept that another chapter owns:
  `[Klucze](../07-portfel-i-narzedzia/01-klucze.md)`. Relative `.md`
  paths, to the page, not the folder.
- Within a chapter, link forward once ("wyjaśnia rozdział [Koszt]") and
  never re-explain what a previous page established — refer to the
  listing number instead.
- Every `index.md` links its quiz page in `08-pytania-kontrolne/`.

### 16.7 `index.md`

In this order:

1. **Opening** — the chapter's one organising idea and what the chapter
   adds beyond the deck; link to the deck PDF
   (`releases/download/latest/<deck>.pdf`).
2. `## Zawartość` — numbered list, one line per page: link, dash, the
   three or four things the page covers. Then the quiz link.
3. `## Podsumowanie` — three to five paragraphs restating the chapter's
   mechanisms in the order taught, with the bolded terms; no new facts.
   Ends with the chained analogy block.
4. `## Ćwiczenia` — three or four numbered tasks with a bold title, doable
   with the CLI, Explorer or a text editor; each has a concrete deliverable
   ("zapisz…", "policz…", "wskaż, które sprawdzenie…"). Imperative mood is
   allowed here and only here. No solutions on the page. State the
   prerequisites (CLI installed, devnet SOL) in one sentence up front.

### 16.8 Keeping the site in sync

- When a deck changes, update the matching chapter in the same commit.
- When a `tikzpicture` changes, run `make diagrams` and commit the SVGs.
- When `exam/*.md` changes, mirror it in `08-pytania-kontrolne/`.
- Live numbers in the text are stale by definition; re-measure them when
  touching the page.

---

## 15. Influences

This guide draws on:

- **The recorded "Dlaczego blockchain i Solana?" lecture** — the in-house
  reference for narrative rhythm (problem → mechanism → benefit), helper-
  block usage, and analogy-first term introduction.
- **Garr Reynolds, *Presentation Zen*** — one idea per slide, signal over
  noise, restraint as a virtue.
- **Edward Tufte, *Beautiful Evidence*** — slides hide evidence; when you
  do show data on a slide, make it dense and honest. Avoid bullet-as-thought
  fragmentation by anchoring every bullet to a takeaway.
- **Andy Matuschak & Michael Nielsen, *Quantum Country* / mnemonic
  medium** — analogies before formalism, multiple representations of the
  same idea, naming difficulty explicitly so struggle reads as expected.
- **MIT OCW 6.831 graphic-design notes** — the squint test, simplicity,
  visual variables, Gestalt grouping.

None of these are required reading to follow this guide. They are listed
so future authors can dig deeper when a rule feels arbitrary — the
reasoning is usually in one of these.
