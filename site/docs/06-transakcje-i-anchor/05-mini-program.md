---
title: Mini-program
description: Kompletny program licznika w Anchorze 1.0 — declare_id, dwie instrukcje, dwie struktury kont, układ danych, błąd — w jednym pliku, skompilowany i przetestowany, z wynikiem testów.
sidebar_position: 5
slug: mini-program
---

# Mini-program

Wszystkie trzy bloki razem, w jednym pliku. To kompletny program — bez
skrótów i bez `// ...` — który został skompilowany poleceniem `anchor
build`, przetestowany w lokalnej maszynie wirtualnej i z którego pochodzą
wszystkie logi i bajty w tym temacie. Listing 6-10 to cały `lib.rs`.

```rust title="programs/licznik/src/lib.rs"
use anchor_lang::prelude::*;

declare_id!("6hqBGkDSZTaF5cFshxX1pZPJkM3QAtEHFuWc2VxKdBmY");

#[program]
pub mod licznik {
    use super::*;

    pub fn init(ctx: Context<Init>, value: u64) -> Result<()> {
        let counter = &mut ctx.accounts.counter;
        counter.authority = ctx.accounts.user.key();
        counter.value = value;
        counter.bump = ctx.bumps.counter;
        Ok(())
    }

    pub fn increment(ctx: Context<Increment>) -> Result<()> {
        let counter = &mut ctx.accounts.counter;
        counter.value = counter
            .value
            .checked_add(1)
            .ok_or(LicznikError::Overflow)?;
        msg!("Licznik: {}", counter.value);
        Ok(())
    }
}

#[derive(Accounts)]
pub struct Init<'info> {
    #[account(
        init,
        payer = user,
        space = 8 + Counter::INIT_SPACE,
        seeds = [b"counter", user.key().as_ref()],
        bump,
    )]
    pub counter: Account<'info, Counter>,
    #[account(mut)]
    pub user: Signer<'info>,
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct Increment<'info> {
    #[account(
        mut,
        has_one = authority,
        seeds = [b"counter", authority.key().as_ref()],
        bump = counter.bump,
    )]
    pub counter: Account<'info, Counter>,
    pub authority: Signer<'info>,
}

#[account]
#[derive(InitSpace)]
pub struct Counter {
    pub authority: Pubkey,
    pub value: u64,
    pub bump: u8,
}

#[error_code]
pub enum LicznikError {
    #[msg("Licznik przekroczył zakres u64")]
    Overflow,
}
```

<div className="listing"><strong>Listing 6-10.</strong> Program licznika w całości: 60 linii, z których żadna nie sprawdza ręcznie właściciela, podpisu ani adresu.</div>

## Od góry do dołu

**`use anchor_lang::prelude::*;`** importuje wszystko, czego program
potrzebuje z frameworku: `Context`, `Account`, `Signer`, `Program`,
`Pubkey`, `Result`, makra. Jedna linia zamiast kilkunastu importów.

**`declare_id!`** ustala adres programu. Musi zgadzać się z kluczem z
`target/deploy/licznik-keypair.json`, bo z tego klucza wynika adres, pod
którym `anchor deploy` wgra kod; Anchor sprawdza tę zgodność przy każdym
wywołaniu i odrzuca transakcję, gdy program został wgrany pod innym
adresem, niż deklaruje. Ta wartość jest też wpisana w `Anchor.toml` i w
IDL z Listingu 6-9.

**`#[program]`** — moduł z dwiema instrukcjami, omówiony przy Listingu
6-4. `init` zapisuje trzy pola nowego licznika; `increment` dodaje jeden
z kontrolą przepełnienia.

**`#[derive(Accounts)]` × 2** — jedna struktura na instrukcję, omówione
przy Listingu 6-5. `Init` tworzy konto pod PDA z seedów `"counter"` +
klucz użytkownika, każe użytkownikowi zapłacić depozyt i wymaga System
Programu do CPI. `Increment` wymaga istniejącego licznika pod tym samym
PDA, związanego przez `has_one` z podpisującym.

**`#[account]` + `#[derive(InitSpace)]`** — układ danych z Listingu 6-7:
41 bajtów pól plus 8 dyskryminatora.

**`#[error_code]`** — jeden błąd własny, numer 6000, z tekstem, który
pojawił się w Listingu 4-16.

## Testy

Anchor 1.0 generuje testy w Ruście, które uruchamiają skompilowany
program w **LiteSVM** — lokalnej maszynie wirtualnej Solany bez sieci,
bez walidatora i bez czekania na sloty. Listing 6-11 to wynik trzech
testów napisanych dla tego programu: `init` z wartością 41 i jeden
`increment`; `increment` obcym kluczem; `increment` przy maksymalnej
wartości.

```bash
$ cargo test
   Compiling licznik v0.1.0
    Finished `test` profile [unoptimized + debuginfo] target(s) in 18.52s
     Running tests/test_initialize.rs

running 3 tests
test init_then_increment ... ok
test increment_by_stranger_fails ... ok
test increment_overflows ... ok

test result: ok. 3 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.19s
```

<div className="listing"><strong>Listing 6-11.</strong> Trzy testy, trzy ścieżki: sukces, odrzucenie przez constraint, odrzucenie przez błąd własny. Cały przebieg trwa 0,19 s.</div>

Dwa z trzech testów sprawdzają, że program **odmawia** — i to one są
ważniejsze. `increment_by_stranger_fails` oczekuje w logu
`ConstraintSeeds` (Listing 6-6); `increment_overflows` oczekuje
`Overflow` (Listing 4-16). Program, który przechodzi tylko test sukcesu,
nie jest przetestowany: luki z rozdziału [Czym jest
Anchor](./02-czym-jest-anchor.md) ujawniają się wyłącznie na
niepoprawnych danych, więc testy muszą takie dane podawać.

Skompilowany program to plik `target/deploy/licznik.so` o rozmiarze
147 472 bajtów. `solana rent` dla tego rozmiaru zwraca 0,75 SOL — tyle
kosztuje wgranie go do sieci, i tyle wraca przy zamknięciu programu.
Wdrożenie na devnet, wywołanie z klienta TypeScript przez IDL i
obejrzenie licznika w Explorerze to program sesji live.

:::note Trzy bloki, raz jeszcze
`#[program]` — co robi: `init`, `increment`. `#[derive(Accounts)]` — na
czym: `Init`, `Increment`. `#[account]` — jak wygląda stan: `Counter`.
Sześćdziesiąt linii; każda z nich ma swoje miejsce w jednym z trzech
bloków albo jest jego parametrem.
:::

To zamyka temat i teoretyczną część kursu. Zostało jedno: mieć własny
portfel, trochę SOL na sieci testowej i umieć zobaczyć własną
transakcję. To temat ostatniego rozdziału.
