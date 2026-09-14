---
title: Pożyczanie
description: Referencje & i &mut — Rust nie kopiuje danych, tylko pożycza; jeden piszący albo wielu czytających.
sidebar_position: 4
slug: pozyczanie
---

# Pożyczanie

Rust nie kopiuje danych domyślnie i nie pozwala na dwa jednoczesne zapisy.
Zamiast tego funkcja dostaje pożyczkę — do odczytu albo do zapisu.

## Pożyczanie

- Rust nie kopiuje danych domyślnie — przekazuje **pożyczkę** referencji (`&`)
- Jak biblioteka: `&` = czytanie książki, `&mut` = pisanie notatek; właściciel się nie zmienia
- Kompilator gwarantuje: jeden `&mut` **lub** wiele `&` — nigdy oba naraz

<div className="diagram">

![Trzy funkcje czytają Vault przez & jednocześnie; jedna funkcja pisze przez &mut wyłącznie](/img/diagrams/4_rust-01.svg)

</div>

:::note Sygnatury
```rust
fn read_vault(v: &Vault)            { msg!("{}", v.balance); }
fn add_funds(v: &mut Vault, n: u64) { v.balance += n; }
```
:::
