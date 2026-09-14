---
title: Ryzyka i composability
description: Co może pójść źle w protokole pożyczkowym i jak protokoły DeFi budują na sobie nawzajem.
sidebar_position: 5
slug: ryzyka-i-composability
---

# Ryzyka i composability

Brak pośrednika oznacza też brak kogoś, kto naprawi błąd. Jednocześnie ten
sam brak pozwala protokołom łączyć się bez pytania kogokolwiek o zgodę.

## Ryzyka w Lending

:::warning Ryzyka, o których warto pamiętać
- **Liquidation risk** — zbyt wysokie LTV przy spadku rynku
- **Bad debt** — protokół traci środki, gdy likwidacja jest za wolna
- **Program risk** — błąd w kodzie = utrata środków
- **Oracle manipulation** — fałszywe ceny prowadzą do likwidacji
- **Rug pull** — złośliwy projekt drainuje płynność
:::

## Composability w DeFi

<div className="diagram">

![AMM i Lending połączone: LP tokeny jako collateral, pożyczone tokeny wracają do AMM, agregator spina oba przez CPI](/img/diagrams/3_lending-02.svg)

</div>

- Protokoły są **composable** — budują na sobie nawzajem jak klocki
- LP tokeny z AMM jako collateral w protokole lending
- Borrowed tokeny ponownie dostarczane do AMM — **leverage loop**
- **Yield aggregatory** automatyzują strategie przez **CPI**
