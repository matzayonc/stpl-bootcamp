---
title: Mini-program
description: Kompletny program licznika w Anchorze — declare_id, instrukcja, struktura kont i układ danych na jednym ekranie.
sidebar_position: 5
slug: mini-program
---

# Mini-program

Wszystkie trzy bloki razem. To kompletny, kompilujący się program — bez
skrótów.

```rust title="lib.rs"
use anchor_lang::prelude::*;

declare_id!("Lic1111111111111111111111111111111111111111");

#[program]
pub mod licznik {
    use super::*;
    pub fn init(ctx: Context<Init>, value: u64) -> Result<()> {
        ctx.accounts.counter.value = value;
        Ok(())
    }
}

#[derive(Accounts)]
pub struct Init<'info> {
    #[account(init, payer = user, space = 8 + 8)]
    pub counter: Account<'info, Counter>,
    #[account(mut)] pub user: Signer<'info>,
    pub system_program: Program<'info, System>,
}

#[account]
pub struct Counter { pub value: u64 }
```

- `declare_id!` — adres programu; musi zgadzać się z kluczem deploymentu
- `#[program]` — jedna instrukcja `init`, która zapisuje wartość startową
- `#[derive(Accounts)]` — `init` tworzy konto, `user` płaci rent i podpisuje, `system_program` je zakłada
- `#[account]` — 8 bajtów dyskryminatora + 8 bajtów `u64`, stąd `space = 8 + 8`
