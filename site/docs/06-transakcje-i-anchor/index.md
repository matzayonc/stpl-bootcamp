---
title: Transakcje i Anchor
description: Jak wygląda zapis stanu na Solanie i jak Anchor zdejmuje z programisty walidację, serializację i IDL.
sidebar_position: 0
---

# Transakcje i Anchor

Read jest darmowy; każdy write to transakcja, którą węzeł musi zweryfikować
bajt po bajcie. Anchor to framework, który tę weryfikację — i resztę
boilerplate'u — generuje z deklaracji. Odpowiada slajdom *Anatomia Anchora*
([PDF](https://github.com/matzayonc/stpl-slides/releases/download/latest/6_anchor.pdf)).

## W skrócie

:::note Co Anchor robi za programistę
- Walidacja kont przed ciałem instrukcji
- Serializacja Borsh i dyskryminatory
- IDL i czytelne błędy zamiast surowych kodów
:::

:::note Trzy bloki do zapamiętania
`#[program]` — instrukcje · `#[derive(Accounts)]` — konta + walidacja ·
`#[account]` — układ danych.
:::

## Strony

1. [Transakcja](./01-transakcja.md) — instrukcja, koperta z podpisami, atomowość
2. [Czym jest Anchor](./02-czym-jest-anchor.md) — surowa Solana, framework, trzy bloki
3. [Program i Accounts](./03-program-i-accounts.md) — `#[program]`, `#[derive(Accounts)]`, constraints
4. [Serializacja i IDL](./04-serializacja-i-idl.md) — Borsh, dyskryminator, opis interfejsu
5. [Mini-program](./05-mini-program.md) — cały licznik na jednym ekranie
