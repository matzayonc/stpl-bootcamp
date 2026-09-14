---
title: Czytamy razem
description: Prawdziwa instrukcja deposit z programu vault — wszystkie wzorce w dziesięciu liniach.
sidebar_position: 5
slug: czytamy-razem
---

# Czytamy razem

Wszystkie wzorce z tego tematu w jednym fragmencie. To autentyczna
instrukcja z programu Anchora — szczegóły frameworku są w
[Transakcje i Anchor](../06-transakcje-i-anchor/index.md).

## deposit — vault program

- `struct Deposit`, `Context<T>`, `&mut` pożyczka pola (`mut`)
- `checked_add` zwraca `Option`; `ok_or(...)?` zamienia na `Result`
- `msg!` makro, `Ok(())` jawny sukces

:::note deposit — vault program
```rust
pub fn deposit(ctx: Context<Deposit>,    // Context<T>
               amount: u64) -> Result<()> {
    let vault = &mut ctx.accounts.vault; // pożyczka &mut
    vault.balance = vault.balance
        .checked_add(amount)             // zwraca Option
        .ok_or(VaultError::Overflow)?;   // Option->Result, ?
    msg!("Wpłacono: {}", amount);        // makro
    Ok(())                               // Result: sukces
}
```
:::
