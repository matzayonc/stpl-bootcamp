---
title: Dlaczego Solana?
description: Ograniczenia Bitcoina i Ethereum oraz liczby, które czynią Solanę infrastrukturą, a nie zabawką.
sidebar_position: 4
slug: dlaczego-solana
---

# Dlaczego Solana?

Programy on-chain mają sens tylko wtedy, gdy sieć wykonuje je szybko i tanio.
Nie każdy blockchain spełnia ten warunek.

## Obecne ograniczenia

- **Bitcoin** — BFT i bezpieczny, ale bez programów on-chain
- **Ethereum** — 15 TPS i gas > $50 przy obciążeniu
- Wysoki koszt = tylko duże operacje mają sens
- Layer 2 obniżają koszty, ale fragmentują ekosystem

:::warning Problem
BFT compute bez skali to zabawka, nie infrastruktura.
:::

## Solana

:::note Kluczowe liczby
- **50 000+ TPS** — przepustowość porównywalna z Visa
- **< $0.001** — niezależnie od obciążenia sieci
- **400 ms** — czas finalizacji bloku
- **Jeden layer** — bez fragmentacji ekosystemu
:::

Dwa mechanizmy stoją za tymi liczbami:

- **PoH** — kryptograficzny zegar dla węzłów
- **Sealevel** — równoległe wykonanie transakcji
