---
title: Własność
description: Program-właściciel jako jedyny uprawniony do zapisu, podpis użytkownika jako autoryzacja, adres z klucza lub z PDA.
sidebar_position: 2
slug: wlasnosc
---

# Własność

Skoro dane leżą w kontach, ktoś musi mieć prawo je zmieniać. Na Solanie
to prawo ma dokładnie jeden program — a użytkownik jedynie wyraża zgodę.

## Właściciel

- Każde konto danych ma program-**właściciela**
- Tylko właściciel może zmienić bajty konta
- Portfel → System Program; token → Token Program
- Konto aplikacji → jej program

:::warning Problem
Skoro tylko program zmienia dane — jak użytkownik autoryzuje zmianę? Podpisem.
:::

## Owner, Signer

<div className="diagram">

![User (Signer) → podpis → Token Program (Owner) → zapis → Konto](/img/diagrams/5_accounts-02.svg)

</div>

:::tip Przelew tokena
Właścicielem konta jest Token Program — ale to **użytkownik** podpisuje zgodę.
:::

## Adres

- Część adresów = klucz publiczny (portfele, nowe konta)
- Część wyliczana deterministycznie przez program — to **PDA**
- PDA = Program Derived Address

<div className="diagram">

![Dwie drogi do adresu konta: keypair → pubkey, albo dane indeksu → wyliczenie (PDA)](/img/diagrams/5_accounts-03.svg)

</div>

:::warning Sesja live
PDA rozkłada się na czynniki pierwsze na sesji live — najtrudniejszy temat
kursu.
:::
