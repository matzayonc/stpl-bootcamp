---
title: Transakcja
description: Instrukcja jako trójka (program, konta, dane), transakcja jako koperta z podpisami i opłatą, atomowość wykonania.
sidebar_position: 1
slug: transakcja
---

# Transakcja

Klik w przycisk „wymień" wysyła coś do sieci. Węzeł nie ufa frontendowi,
więc to „coś" musi mieć formę, którą da się sprawdzić bajt po bajcie.

## Co wysyła użytkownik

- Frontend pokazuje przycisk „wymień" — klik i coś leci do sieci
- Read jest gratis, write wymaga czegoś więcej
- Węzeł nie ufa frontendowi — musi sam sprawdzić każdy bajt
- Akcję trzeba opakować tak, by węzeł mógł sprawdzić autoryzację

:::warning Pytanie
Kto autoryzuje zmianę stanu — i jak węzeł to weryfikuje?
:::

## Transakcja

- Pojedyncze wywołanie programu to **instrukcja**: trójka (program, konta, dane)
- Koperta z jedną lub kilkoma instrukcjami to **transakcja**
- Koperta niesie też listę **signerów** i **opłatę** dla walidatora
- Read nie wymaga koperty — każdy write owszem

:::note Definicja
Transakcja = lista instrukcji + lista podpisów + opłata.
Jedyna forma zapisu stanu na Solanie.
:::

## Atomowość

- Transakcja wykonuje się w całości albo wcale — to **atomowość**
- Jedna instrukcja zwraca błąd → sieć cofa wszystkie zmiany
- Stan po nieudanej transakcji jest identyczny jak przed
- Opłata leci do walidatora niezależnie od wyniku

:::tip Swap + transfer w jednej tx
Instrukcja 1 wymienia SOL na USDC, instrukcja 2 wysyła USDC do znajomego.
Jeśli transfer padnie, swap też się cofa — nie zostaje połowa operacji.
:::
