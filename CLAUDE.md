# Claude Code — Repo Guide

This repository builds LaTeX/Beamer slide decks for the Superteam Poland Solana
Bootcamp. Read the files below before editing slides — they are the source of
truth, this file only points to them.

## Required reading — by task

Before starting any task, read every file listed for that task type. Do not
skip this step.

**Writing or editing slide content** (new slides, bullet text, narrative):
- Read [`style.md`](style.md) — content rules, narrative arc, slide skeleton,
  anglicisms, math/code conventions, voice

**Changing or authoring visual structure** (blocks, colors, layout, bullets):
- Read [`branding.md`](branding.md) — colors, block types, bullets, footline,
  section dividers, title slide
- Read [`preamble.tex`](preamble.tex) — actual implementation; edit only if
  the brand definition itself needs to change

**Adding or editing diagrams / graphs**:
- Read [`graphs.md`](graphs.md) — TikZ libraries, node styles, edge patterns,
  Beamer-specific caveats

**Build, filenames, or repo structure questions**:
- Read [`README.md`](README.md) — `make` targets, filename pattern, `gn` slide

**Editing the website** (`site/`, Docusaurus):
- Read [`branding.md`](branding.md) §Web — how the brand maps to CSS; the
  implementation is `site/src/css/custom.css`
- Content rules from `style.md` apply to doc pages too (Polish, impersonal,
  no emojis, one helper block per concept)
- `site/docs/` mirrors the decks by topic: `NN-<topic>/index.md` = the deck's
  *Podsumowanie*, one page per slide section, `##` per frame, blocks →
  `:::note` / `:::warning` / `:::tip`. When a deck changes, update the
  matching page; when a `tikzpicture` changes, run `make diagrams`
  (`README.md` §Diagrams). Exams in `exam/*.md` feed
  `site/docs/08-pytania-kontrolne/`.

## Existing slides

`presentations/` holds the deck source. Files follow `<index>_<slug>.tex`
(see `README.md`). The recorded reference lecture for narrative rhythm is
`0_why.tex` — when an answer about *style* is unclear, that file is the
working example of what `style.md` describes.

## Technical reference (Solana / Anchor)

`reference/skill/` holds reference docs the AI uses for technical
correctness when writing slide content. Consult it before claiming
anything specific about Anchor, IDL codegen, accounts, payments,
testing, security, or common errors:

- `anchor/`, `programs/`, `kit/`, `surfpool/` — framework-specific notes
- `common-errors.md`, `compatibility-matrix.md` — pitfalls and version
  alignment
- `confidential-transfers.md`, `payments.md`, `security.md`,
  `testing.md`, `idl-codegen.md`, `kit-web3-interop.md`,
  `frontend-framework-kit.md`, `resources.md` — topic deep-dives

Treat these as authoritative for facts; treat `style.md` as authoritative
for how those facts get presented.

## Common tasks

- **New deck**: create `presentations/<index>_<slug>.tex`, start with
  `\input{preamble}`, follow the skeleton in `style.md` §5, end with the
  mandatory `gn` slide from `README.md`.
- **Build**: `make` builds everything to `dist/`. `make N` (where N is a
  filename token) builds only matching decks. `make open-N` builds + opens.
- **Editing visuals**: change `preamble.tex`, then update `branding.md` so
  it stays the source of truth.
- **Editing narrative rules**: change `style.md`. Do not duplicate rules
  here.

## Conventions worth repeating

- Polish, impersonal third person. No emojis on slides.
- Concept slides end in exactly one helper block (`block`, `alertblock`,
  or `exampleblock`) — picked by semantic role per `style.md` §4.3.
- Incremental reveal (`<+->`) is on by default; do not turn it off
  globally.
- Every deck ends with the `gn` slide. No exceptions.
