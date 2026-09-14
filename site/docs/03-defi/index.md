---
title: DeFi
description: Dwa filary finansów bez pośrednika — wymiana tokenów (AMM) i pożyczki (lending) — wraz z matematyką, która je trzyma.
sidebar_position: 0
---

# DeFi

Obietnica z pierwszego tematu brzmiała: usługi finansowe **bez pośrednika**.
Ten temat pokazuje dwa filary, na których ta obietnica stoi — wymianę tokenów
i pożyczki — oraz matematykę, która zastępuje giełdę i bank. Łączy slajdy
*AMM na Solanie*
([PDF](https://github.com/matzayonc/stpl-slides/releases/download/latest/2_amm.pdf))
i *Lending na Solanie*
([PDF](https://github.com/matzayonc/stpl-slides/releases/download/latest/3_lending.pdf)).

## W skrócie

:::note Wymiana
- **DeFi** — usługi finansowe bez pośrednika; token to saldo z regułami w kodzie
- **AMM** zastępuje order book proporcją rezerw — duży swap kosztuje więcej
- **LP** dostarcza płynność i zarabia opłaty, ale wartość pozycji zależy od cen
:::

:::note Pożyczki
- **Overcollateralized borrowing** — zastaw broni protokół zamiast scoringu kredytowego
- Gdy wartość zastawu spada za nisko — **likwidacja** automatycznie zamyka dług
- **Composability**: AMM i lending łączą się jak klocki — leverage loop, yield aggregatory
:::

## Strony

1. [Czym jest DeFi?](./01-czym-jest-defi.md) — obietnica, definicja, token jako saldo z regułami
2. [AMM](./02-amm.md) — order book vs AMM, pula, dostawcy płynności, ryzyka
3. [Matematyka AMM](./03-matematyka-amm.md) — constant product, swap, impermanent loss, CLMM
4. [Lending](./04-lending.md) — pula, zastaw, nadzabezpieczenie, likwidacja
5. [Ryzyka i composability](./05-ryzyka-i-composability.md) — co może pójść źle i jak protokoły się łączą
6. [Matematyka pożyczki](./06-matematyka-pozyczki.md) — LTV, health factor, utilization rate
