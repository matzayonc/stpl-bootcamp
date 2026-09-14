---
title: Czym jest Anchor
description: Ręczna walidacja w surowej Solanie, framework jako odpowiedź i trzy makra, z których składa się każdy program.
sidebar_position: 2
slug: czym-jest-anchor
---

# Czym jest Anchor

Bez frameworku program dostaje listę kont jako surowe bajty i sam musi
sprawdzić wszystko, co opisuje [Model kont](../05-konta/index.md). Anchor
robi to z deklaracji.

## Surowa Solana

- Bez frameworku program dostaje listę kont jako surowe bajty
- Programista sam sprawdza ownera, signera, rozmiar, dyskryminator
- Sam też serializuje strukturę do bajtów i z powrotem
- Jeden zapomniany `if` = otwarte drzwi do funduszy

:::warning Ryzyko
Ręczna walidacja, ręczna serializacja, ręczne sprawdzanie podpisów —
łatwo o lukę bezpieczeństwa.
:::

## Czym jest Anchor

- **Anchor** — framework do pisania programów Solany
- Walidacja kont, serializacja i IDL — z automatu
- Programista pisze logikę, framework dostarcza boilerplate
- Standard de facto: większość programów w ekosystemie jest w Anchorze

:::tip Analogia
Rails / NestJS dla Solany — konwencje zamiast pisania wszystkiego od zera.
:::

## Trzy bloki

- Program Anchor składa się z trzech makr-atrybutów
- `#[program]` — moduł z instrukcjami
- `#[derive(Accounts)]` — struktury kont z walidacją
- `#[account]` — układ danych w koncie danych

:::note Trzy role
**co robi** (instrukcje) · **na czym** (konta + walidacja) ·
**jak wygląda stan** (pola konta).
:::
