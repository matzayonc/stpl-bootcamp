---
title: Koszt
description: Rent-exempt jako jednorazowy zwrotny depozyt oraz świadome deklarowanie rozmiaru konta w Anchorze.
sidebar_position: 3
slug: koszt
---

# Koszt

Każdy bajt konta jest przechowywany przez każdy węzeł sieci. Dlatego dane
on-chain mają cenę — i dlatego rozmiar konta deklaruje się świadomie.

## Rent

- Dane zajmują miejsce u **każdego** węzła — więc kosztują
- Konta muszą być **rent-exempt**: depozyt z góry
- Depozyt proporcjonalny do rozmiaru konta
- Zamknięcie konta → lamporty wracają do właściciela

:::tip To nie abonament
Rent-exempt to jednorazowy, zwrotny depozyt — nie miesięczna opłata.
:::

## Rozmiar

- Tworząc konto, deklaruje się rozmiar (bajty na dane)
- Za mało — stan się nie zmieści; za dużo — przepłacony rent

```rust
#[account(init, payer = signer, space = 8 + 32 + 8)]
```

<div className="diagram small">

![Układ 48 bajtów: 8 B dyskryminator, 32 B owner, 8 B licznik](/img/diagrams/5_accounts-04.svg)

</div>

- W Anchorze liczy się to świadomie atrybutem `space`
- Projektowanie danych = projektowanie kont
