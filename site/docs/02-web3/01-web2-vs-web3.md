---
title: Web2 vs Web3
description: Centralny serwer z prywatną bazą kontra klaster węzłów wykonujący publiczny program.
sidebar_position: 1
slug: web2-vs-web3
---

# Web2 vs Web3

Oba modele da się streścić w jednym zdaniu. Różnica sprowadza się do tego,
kto trzyma prawdę o stanie.

## Web2 w jednym zdaniu

- Klient pyta **centralny serwer**, który ufa sam sobie
- Baza danych **pod kontrolą dostawcy** — prywatna
- Aplikacja działa, dopóki działa operator

<div className="diagram narrow">

![Klient → (HTTPS) → Serwer firmy → (zaufanie) → Prywatna DB](/img/diagrams/1_paradigm-01.svg)

</div>

:::warning Jeden właściciel prawdy
Firma decyduje, co jest w bazie. Trzeba jej zaufać, że nie kłamie.
:::

## Web3 w jednym zdaniu

- Klient wysyła **podpisaną transakcję** do sieci
- Logika żyje on-chain jako **program**
- Dane w koncie blockchain — **bezzaufaniowe wykonanie**

<div className="diagram narrow">

![Klient → (podpis) → Klaster → (stan) → Konta](/img/diagrams/1_paradigm-02.svg)

</div>

:::tip Backend staje się programem
Nie ma serwera firmy — jest klaster węzłów, który każdy może odpytać.
:::
