---
title: Program i Accounts
description: Moduł #[program] z instrukcjami, struktura #[derive(Accounts)] z walidacją i najważniejsze constraints.
sidebar_position: 3
slug: program-i-accounts
---

# Program i Accounts

Dwa z trzech bloków Anchora: gdzie mieszka logika i jak deklaruje się
konta, na których ta logika działa.

## `#[program]`

- Moduł `#[program]` grupuje wszystkie instrukcje programu
- Każda `pub fn` w tym module to jedna instrukcja on-chain
- Pierwszy argument zawsze **`Context<T>`** — konta + meta
- Zwracany typ to `Result<()>` — sukces lub błąd Anchora

:::note Szkielet instrukcji
```rust
#[program]
pub mod licznik {
    use super::*;
    pub fn increment(ctx: Context<Increment>) -> Result<()> {
        ctx.accounts.counter.value += 1;
        Ok(())
    }
}
```
:::

## `#[derive(Accounts)]`

- Każda instrukcja ma osobną `struct` z listą wymaganych kont
- `#[derive(Accounts)]` generuje walidację z deklaracji pól
- Constraints sprawdzane **przed** ciałem instrukcji
- Owner pilnuje danych, signer autoryzuje zmianę

:::tip Efekt
Luka łapana w deklaracji, nie w ręcznym `if` — middleware walidujący
request, zanim dotrze do logiki.
:::

## Constraints

- **init** — tworzy nowe konto i opłaca rent
- **mut** — konto będzie zmieniane (zapis bajtów)
- **signer** — klucz musi podpisać transakcję
- **seeds** — adres wyliczony deterministycznie (PDA)
- **has_one** — pole konta musi pasować do innego konta

:::note Struktura kont dla `deposit`
```rust
#[account]
pub struct Vault { pub owner: Pubkey, pub balance: u64 }

#[derive(Accounts)]
pub struct Deposit<'info> {
    #[account(mut, has_one = owner)] // vault.owner == owner.key
    pub vault: Account<'info, Vault>,
    #[account(mut)]
    pub owner: Signer<'info>,
}
```
:::
