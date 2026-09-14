---
title: Rust dla Anchora
description: Minimum Rusta potrzebne, żeby czytać lib.rs programu Anchora — bez lifetime'ów, generyków i async.
sidebar_position: 0
---

# Rust dla Anchora

Nie jest to kurs Rusta. Cel jest węższy: po tym temacie `lib.rs` programu
Anchora czyta się bez paniki — `mut`, `Option`, `Result`, `&`, makra.
Odpowiada slajdom *Szybki Rust*
([PDF](https://github.com/matzayonc/stpl-slides/releases/download/latest/4_rust.pdf)).

## W skrócie

1. **Niemutowalność** domyślna — `mut` = jawna decyzja
2. **struct + impl** zamiast klas; traity zamiast dziedziczenia
3. **Option** zamiast null; **Result** zamiast wyjątków, `?` propaguje
4. **Pożyczanie** (`&`, `&mut`) — bez kopiowania, bez wyścigów
5. **Makra** (`#[...]`, `msg!`) generują boilerplate

:::tip Efekt
To jeszcze nie cały Rust — ale `lib.rs` z Anchora czyta się bez paniki.
:::

## Strony

1. [Po co Rust?](./01-po-co-rust.md) — zakres tematu i dlaczego kod on-chain potrzebuje typów
2. [Składnia](./02-skladnia.md) — funkcja i struktura na jednym ekranie
3. [Wzorce Rusta](./03-wzorce.md) — niemutowalność, struct + impl, typy, match, Option, Result, makra
4. [Pożyczanie](./04-pozyczanie.md) — `&` i `&mut` bez kopiowania
5. [Czytamy razem](./05-czytamy-razem.md) — prawdziwy `deposit` z programu vault
