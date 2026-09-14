---
title: Anatomia konta
description: Pięć pól każdego konta, podział na konta danych i programów oraz różnica wobec kontraktu w Ethereum.
sidebar_position: 1
slug: anatomia-konta
---

# Anatomia konta

Cała Solana to mapa „adres → konto". Zanim pojawi się jakikolwiek program,
warto zobaczyć, co dokładnie pod tym adresem leży.

## Jeden pomysł

- Na Solanie **wszystko jest kontem**
- Portfel? Konto. Token? Konto. Program? Konto.
- Konto = komórka pamięci z adresem, saldem i danymi

:::warning Problem
Skoro wszystko to konta — jak odróżnić kod od danych i kto co zmienia?
:::

## Anatomia konta

```rust
struct Account {
    address:    Pubkey,   // adres konta
    lamports:   u64,      // saldo (SOL)
    data:       Vec<u8>,  // bajty danych
    owner:      Pubkey,   // program-właściciel
    executable: bool,     // czy to kod?
}
```

- Każde konto ma te pola — i tyle
- Cała Solana to mapa „adres → konto"

:::tip Analogia
Konto to plik: ma ścieżkę (adres), rozmiar, zawartość i właściciela.
:::

## Typy kont

| Konto danych | Konto programu |
|---|---|
| `executable = false` | `executable = true` |
| Trzyma stan | Trzyma kod |
| Licznik, saldo, głosy | Skompilowany bytecode |

Jeden program obsługuje miliony kont danych.

## Vs Ethereum

W Ethereum kontrakt trzyma kod i stan razem. Na Solanie kod jest w jednym
koncie, a stan — w dowolnie wielu kontach podawanych z zewnątrz.

<div className="diagram">

![Ethereum: kontrakt = kod + stan. Solana: program → wiele oddzielnych kont danych](/img/diagrams/5_accounts-01.svg)

</div>

:::tip Analogia
Program to funkcja; konta danych to argumenty i pamięć podane z zewnątrz.
:::
