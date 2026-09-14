---
title: Składnia
description: Funkcja i struktura — typ po nazwie, strzałka do typu zwracanego, struct jako rekord pól.
sidebar_position: 2
slug: skladnia
---

# Składnia

Dla kogoś po TypeScripcie składnia Rusta wygląda znajomo: typ stoi po
nazwie, a struktura to rekord pól.

## Jak wygląda

- Nazwy w `snake_case`, typ **po** nazwie i dwukropku — jak TypeScript
- Strzałka `->` wskazuje typ zwracany funkcji
- `struct` to rekord pól — jak interfejs bez metod

:::note Funkcja i struktura
```rust
fn deposit(amount: u64, owner: Pubkey) -> Result<()> {
    // argument: typ               typ zwracany
}

struct Vault {
    owner:   Pubkey,
    balance: u64,
}
```
:::
