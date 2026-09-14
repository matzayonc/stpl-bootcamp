---
title: Matematyka AMM
description: Niezmiennik x·y = k, price impact przy swapie, impermanent loss i concentrated liquidity.
sidebar_position: 3
slug: matematyka-amm
---

# Matematyka AMM

Cała pula sprowadza się do jednego równania. Z niego wynika cena, koszt
dużego swapu i strata dostawcy płynności przy zmianie kursu.

## Constant Product

- Pula trzyma rezerwy dwóch tokenów, $x$ i $y$
- Każdy swap zmienia obie rezerwy, ale ich *iloczyn* musi zostać stały
- Cena chwilowa wynika z proporcji: $p = y / x$
- Im więcej kupuje się jednego tokenu, tym wyższa cena jednostkowa

:::note Niezmiennik
$$
x \cdot y = k
$$

$x$ — rezerwa tokenu A, $y$ — rezerwa tokenu B, $k$ — stała
:::

<div className="diagram narrow">

![Hiperbola x·y = k; punkt (x0, y0) przesuwa się do (x1, y1) po swapie; styczna o nachyleniu −p](/img/diagrams/2_amm-03.svg)

</div>

## Jak działa swap?

- Użytkownik wpłaca $\Delta x$ tokenu A, otrzymuje $\Delta y$ tokenu B
- Nowe rezerwy są policzone tak, aby zachować $k = x \cdot y$
- Im większy swap względem puli, tym gorsza cena — to **price impact**

:::tip Przykład: zakup 100 USDC za SOL
Pula: $x = 10$ SOL, $y = 1\,000$ USDC, $k = 10\,000$.
Po cenie startowej (100 USDC/SOL) oczekiwana zapłata to 1 SOL.

$$
x' = \frac{k}{y - \Delta y} = \frac{10\,000}{900} \approx 11{,}11 \text{ SOL}
$$

Efektywna cena: $\approx 1{,}11$ SOL zamiast 1 SOL — to price impact.
:::

## Impermanent Loss

- IL jest tym większy, im bardziej cena odchyla się od ceny wejścia
- Przy powrocie ceny do poziomu wejścia — IL znika (stąd *impermanent*)
- LP profituje, gdy: **opłaty > IL**
- Strategia: pule stabilnych par (np. USDC/USDT) mają minimalne IL

:::warning Impermanent Loss (IL)
Gdy cena tokenów zmienia się względem chwili wpłaty, wartość pozycji LP jest
*mniejsza* niż gdyby trzymać tokeny (HODL).
:::

## Concentrated Liquidity

- **Concentrated Liquidity Market Maker (CLMM)** — LP wybiera **przedział cenowy** $[p_a,\, p_b]$, w którym działa
- Kapitał jest efektywniejszy — więcej płynności tam, gdzie handel
- Wyższe opłaty przy trafnym wyborze zakresu
- Wyższe ryzyko IL przy wyjściu ceny z zakresu

:::tip Na Solanie
**Orca Whirlpools**, **Raydium CLMM** — wiodące implementacje CLMM
:::
