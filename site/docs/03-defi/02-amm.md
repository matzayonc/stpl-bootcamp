---
title: AMM
description: Automated Market Maker — cena z formuły zamiast z dopasowania zleceń, płynność od każdego, swap 24/7.
sidebar_position: 2
slug: amm
---

# AMM — Automated Market Maker

Klasyczna giełda dopasowuje zlecenia kupna i sprzedaży. Bez giełdy potrzebny
jest inny sposób ustalania ceny — taki, który da się zapisać w programie.

## Order book vs AMM

| Order Book (CEX) | **Automated Market Maker (AMM)** |
|---|---|
| Kupujący i sprzedający składają zlecenia | Brak zleceń — cena z formuły matematycznej |
| Cena wynika z dopasowania zleceń | Płynność dostarcza każdy (LP) |
| Wymaga animatorów rynku (market makers) | Swap zawsze możliwy, 24/7 |
| Przykład: Binance, Openbook | Przykład: Orca, Raydium |

## Jak działa AMM

<div className="diagram narrow">

![Trader wpłaca SOL do puli AMM (SOL ↑, USDC ↓) i otrzymuje USDC; x · y = k](/img/diagrams/2_amm-01.svg)

</div>

- Pula trzyma dwa tokeny w pewnej proporcji — np. SOL i USDC
- Wymiana SOL na USDC: rezerwa SOL rośnie, USDC maleje

:::tip Analogia — koszyk jabłek i gruszek
Im bardziej koszyk jest nierówny, tym mniej korzystna cena.
:::

## Kto dostarcza płynność

<div className="diagram">

![Oś czasu: wpłata LP → kolejne swapy (opłaty trafiają do puli) → wypłata LP + opłaty](/img/diagrams/2_amm-02.svg)

</div>

- **Liquidity Provider (LP)** wpłaca oba tokeny w proporcji aktualnej ceny
- Zarabia na **opłatach transakcyjnych** (np. 0.25% per swap)
- Może wycofać płynność w dowolnym momencie
- Ryzyko: wartość pozycji zmienia się wraz z cenami tokenów

:::tip Przykład
Pula SOL/USDC, cena 100 USDC/SOL.

Wpłata: 10 SOL + 1 000 USDC ⇒ udział w opłacie z każdej wymiany.
:::

## Ryzyka w AMM

:::warning Ryzyka, o których warto pamiętać
- **Impermanent Loss** — przy zmiennych cenach względem wejścia
- **Price impact** — duże swapy względem puli kosztują więcej
- **Slippage** — cena może się zmienić między wysłaniem a wykonaniem
- **Oracle manipulation** — fałszywe ceny zaburzają wycenę
- **Program risk / Rug pull** — błąd lub zły kod = utrata środków
:::
