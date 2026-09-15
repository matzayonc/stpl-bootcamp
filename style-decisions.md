# style.md — Decision Log

Record of the interview that produced `style.md`. Each round captures the
question asked, the option selected, and the section of `style.md` where the
decision landed. Kept so future authors (and future-Claude) can see *why* a
rule reads the way it does without re-running the interview.

- Interview date: 2026-06-24
- Format: batched `AskUserQuestion` rounds (3–4 questions per batch)
- Resulting doc: `style.md`
- Influences consulted: Reynolds — *Presentation Zen*; Tufte — *Beautiful
  Evidence*; Matuschak & Nielsen — *Quantum Country* / mnemonic medium; MIT
  OCW 6.831 — graphic-design notes; the recorded "Dlaczego blockchain i
  Solana?" lecture (`presentations/0_why.tex`).

---

## Round 1 — Foundational rules

- **Title length** → One thought, ~2–4 words.
  *Not the README's "max 2 words"; matches what the recorded lecture
  actually does.* → `style.md` §4.1
- **Bullet structure** → 3–5 bullets, bold a keyword *where useful* (not
  on every bullet as a quota). → §4.2
- **Narrative arc** (problem → mechanism → benefit) → Aspirational
  pattern, not a per-slide checklist. → §3
- **Helper block** → Mandatory on concept slides; pick the block type by
  semantic role. → §4.3

## Round 2 — Structure & narrative conventions

- **Lesson skeleton** → title → Plan (toc) → sections → summary → `gn`.
  "O mnie" + "Plan kursu" only on the kickoff lecture. → §5
- **Term introduction** → Strict problem-first hook for new domain
  concepts; flexible for synonyms and already-introduced terms. → §6
- **Analogies** → Required for new concepts (canonical toolkit: bank,
  notariusz, giełda, arkusz Google, kontrakt). → §6.1
- **Animation** → Mandatory incremental reveal (`<+->`); override only
  for tables / static quotes / single visuals. → §4.5

## Round 3 — Voice, audience, content patterns

- **Voice** → Impersonal Polish, 3rd person. No `Pan/Pani`, no `ty`. → §11
- **Audience** → Progressive — Lekcja 0 assumes zero blockchain; later
  lessons may assume terms introduced earlier. → §2
- **Helper-block semantic mapping** →
  - `block` = definitions, key numbers, named formulas
  - `alertblock` = problems, risks, watchouts
  - `exampleblock` = effects, illustrations, real-world examples
  → §4.3
- **Two-column comparison** → Only for direct opposition (A vs B); stack
  blocks vertically otherwise. → §4.4

## Round 4 — Content density & technical conventions

- **Anglicisms** → Keep canonical English jargon (smart kontrakt,
  permissionless, slippage, AMM, Health Factor, LP, oracle, rug pull). → §7
- **Mini-quiz / ABCD test** → *Not* on slides. Quizzes live in Kajabi;
  `.tex` files stay clean. → (not in `style.md` by design)
- **Summary slide** → Free-form. Bullets, blocks, or recap are all fine
  as long as a student leaving with only the summary still has the headline. → §5.2
- **Math & code** → Displayed equations inside a `block` titled with the
  formula name; inline `$..$` for variables; worked examples in
  `exampleblock`; code as `\texttt{}` for short, `listings` for longer. → §8

## Round 5 — Scope, lesson types, content limits

- **Recorded vs live** → Same style for both; document the usage
  difference (recorded leans on `\note{}` and reveals; live transitions to
  a `\section{Warsztat}` for the code-along). → §13
- **Scope markers** ([RUST] etc.) → Author notes only, never on slides.
  → (deliberately omitted from `style.md`)
- **Images** → Use liberally to support every key concept. → §9
- **Slide density** → Whatever fits without overflow; author's eye on
  the PDF is the check. → §4

## Round 6 — Images, lesson length, opening framing

- **Image categories** (multi-select):
  - TikZ diagrams for architecture / flow
  - Real screenshots of wallets, explorers, apps
  - Small decorative icons (sparing)
  → §9
- **Lesson length** → Variable, driven by topic; no slide-count target. → §4
- **Opening hook** → Author picks per topic (problem-tension *or*
  "Czym jest X?"). → (left open in §5)
- **"Filtr, nie wykład"** → Mention as motivation in §1; do not codify
  per-slide testability. → §1

## Round 7 — Format, references, what NOT to do

- **Source format** → Always `.tex` (Beamer). `.md` via pandoc is a
  fallback at best. → §15-implicit
- **Citations** → Muted-tiny footnote on specific numbers / quoted
  claims only; never decorate every slide. → §10
- **Speaker notes** (`\note{}`) → Optional; document the convention. → §12

## Round 8 — Anti-patterns & misc

- **Explicit anti-patterns** ("don't do this" list) → None selected.
  Style.md states rules positively rather than via a banlist.
- **Kickoff slides** ("O mnie", "Plan kursu") → Only in Lekcja 0. → §5.1
- **Online sources to incorporate** → All four influences:
  Reynolds, Matuschak/Nielsen, MIT OCW, Tufte. → §15
- **File location** → Top-level `/style.md`, sibling to `branding.md`.

## Round 9 — Pre-draft sign-off

- **Reference exemplar** → Don't name specific files in `style.md` —
  keep it abstract. (The decision log and CLAUDE.md may name `0_why.tex`
  as the working example; `style.md` itself stays file-free.)
- **Online sources** (multi-select) → Pull from all four influences. → §15
- **Glossary slide** → None. Terms are introduced inline with their hook. → §6
- **Ready to draft** → Yes.

---

## Post-draft adjustments

After the initial draft, a self-review surfaced seven items. Four were
auto-actioned per user direction:

1. **`reference/skill/` undocumented** → Added a "Technical reference"
   section to `CLAUDE.md` pointing at the Solana / Anchor reference docs.
2. **`99_example.tex` stale relative to `style.md`** → Rewritten to embody
   the patterns (Polish content, helper blocks by semantic role, two-column
   comparison, math-in-block, `gn` slide). Builds cleanly.
3. **README contradicted `style.md` on title length** → Removed
   "Content style" and "gn slide policy" sections from `README.md`. Replaced
   with a one-line pointer. `style.md` now owns the `gn` template too (§5.4).
4. **Acronym-on-first-use codified** → Added `style.md` §6.3.
   Pattern: `\textbf{Full Name (ACRONYM)}` on debut, acronym alone after.

Three items remain unaddressed (flagged at session close):

- PPTX export caveat (LibreOffice → Google Slides degrades tcolorbox,
  TikZ, auto dividers).
- Polish typography conventions (`---` em-dash, `„..."` quotes) used in
  practice but not codified.
- Existing decks that predate `style.md` (`1_intro`, `2_defi`, `4_pda`,
  `4_accounts`, `5_shared_core`, `6_rust`) need a migration pass —
  particularly missing helper blocks on concept slides.

Also unresolved: `3_amm` exists in both `.tex` and `.md`; `style.md` says
`.tex` is canonical, so the `.md` duplicate is either obsolete or kept
for the `pandoc/` flow.

