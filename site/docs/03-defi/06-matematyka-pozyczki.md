---
title: Matematyka pożyczki
description: LTV, health factor i utilization rate — trzy liczby, które sterują protokołem pożyczkowym.
sidebar_position: 6
slug: matematyka-pozyczki
---

# Matematyka pożyczki

Protokół nie ocenia człowieka — ocenia liczby. Trzy z nich wystarczą, by
opisać bezpieczeństwo pozycji i koszt kapitału.

## LTV i Health Factor

<div className="diagram">

![Pasek LTV od 0% do 110%: strefa bezpieczna do 80%, likwidacja przy 90%, zły dług powyżej 100%](/img/diagrams/3_lending-03.svg)

</div>

- **Loan-to-Value (LTV)** — stosunek wartości pożyczki do wartości collateral
- **Health Factor (HF)** — miara oddalenia pozycji od likwidacji; $HF < 1$ uruchamia likwidację

:::note Health Factor
$$
HF = \frac{\text{collateral} \cdot \text{próg likwidacji}}{\text{dług}}
$$
:::

## Utilization Rate

- Niskie $U$ ⇒ niskie APR (zachęta do pożyczania)
- Wysokie $U$ ⇒ wysokie APR (zachęta do dostarczania płynności)
- **Kink model** — gwałtowny wzrost oprocentowania po przekroczeniu progu optymalnego (np. $U = 80\%$)

:::note Utilization Rate
$$
U = \frac{\text{borrowed}}{\text{supplied}}
$$

Wskaźnik wykorzystania puli — steruje oprocentowaniem.
:::

<div className="diagram narrow">

![Wykres APR od U: łagodny wzrost do U_opt, potem stromy odcinek aż do 100%](/img/diagrams/3_lending-04.svg)

</div>
