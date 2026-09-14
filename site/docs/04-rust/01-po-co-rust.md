---
title: Po co Rust?
description: Zakres tego tematu i powód, dla którego kod on-chain pisze się w języku typowanym.
sidebar_position: 1
slug: po-co-rust
---

# Po co Rust?

Pełny Rust to semestr nauki. Tutaj chodzi o coś mniejszego: rozpoznać
konstrukcje, które pojawiają się w każdym programie Anchora.

## Nie uczymy Rusta

- Pełny Rust to semestralny kurs — nie zmieści się w jednej lekcji
- Cel jest węższy — odblokować czytanie `lib.rs` Anchora
- Lifetime'y, generyki, `async` i borrow checker w głębi — pominięte
- Po tym temacie rozpoznawalne są `mut`, `Option`, `Result`, makra

:::warning To nie kurs Rusta
Pełny kurs Rusta odbywa się oddzielnie — tutaj jest minimum niezbędne do
Anchora.
:::

## Kod on-chain

- Bug w programie Solany to **strata użytkowników** — transakcji nie da się cofnąć
- Większość exploitów to klasy błędów, które typowany język wyklucza w kompilacji
- Rust gwarantuje brak `null`, brak wyścigów danych i jawność błędów — przed uruchomieniem

:::warning Skutek
Cała klasa bugów staje się **niemożliwa**, zanim kod dotrze na sieć.
:::
