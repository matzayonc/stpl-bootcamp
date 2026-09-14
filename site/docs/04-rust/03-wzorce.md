---
title: Wzorce Rusta
description: Niemutowalność, struct + impl, typy Anchora, match, Option, Result i makra — każdy wzorzec z analogią i kodem.
sidebar_position: 3
slug: wzorce
---

# Wzorce Rusta

Siedem wzorców, które odróżniają Rust od JavaScriptu. Każdy z nich zamyka
jedną klasę błędów na etapie kompilacji.

## Niemutowalność

- W JS każda zmienna jest mutowalna — w Ruście **odwrotnie**
- Jak arkusz z ochroną komórek: jawna akcja jest wymagana do edycji
- `mut` to świadoma decyzja widoczna w kodzie; kompilator jej pilnuje

:::note let vs let mut
```rust
let x = 5;      // niemutowalne (domyślnie)
// x = 6;       // BŁĄD kompilacji

let mut y = 5;  // jawna zgoda na zmianę
y = 6;          // OK
```
:::

## Brak klas

- Rust nie ma `class` — są `struct` (pola) i `impl` (metody)
- Bez dziedziczenia — zamiast tego **traity**: interfejsy on steroids
- Każdy typ z Anchora to `struct` z blokiem `impl`

:::note struct + impl
```rust
struct Licznik {
    wartosc: u64,
}

impl Licznik {
    fn inkrementuj(&mut self) {
        self.wartosc += 1;
    }
}
```
:::

## Typy w Anchorze

- `u8`, `u64`, `i64` — liczby; `u` = unsigned (bez znaku)
- `Pubkey` — 32-bajtowy adres konta lub właściciela
- `String`, `bool`, `Vec<T>` — tekst, prawda/fałsz, lista

:::note Typowy stan konta
```rust
#[account]
pub struct Stan {
    pub wlasciciel: Pubkey,       // adres
    pub saldo:      u64,          // liczba dodatnia
    pub aktywny:    bool,         // flaga
    pub glosy:      Vec<Pubkey>,  // lista adresów
}
```
:::

## Match

- `switch` w JS milcząco pomija przypadki — błąd widoczny dopiero w runtime
- Jak lista kontrolna pilota: procedura jest niekompletna, dopóki każdy punkt nie jest omówiony
- `match` wymaga pokrycia **wszystkich** gałęzi — brak = błąd kompilacji

:::warning Match wyczerpujący
```rust
match status {
    0 => msg!("nowy"),
    1 => msg!("aktywny"),
    _ => msg!("inny"),   // _ = pozostałe przypadki
}                        // brak _ przy >1 wariancie = BŁĄD
```
:::

## Option — bez null

- `null` rzuca wyjątek dopiero przy dostępie — za późno
- Jak paczka kurierska: albo `Some(paczka)` na progu, albo `None` z awizo — nie ma ciszy
- Kompilator wymusza obsługę `None` **przed** dostępem do wartości

:::tip Option&lt;T&gt;
```rust
let first = accounts.first();   // Option<&Account>
match first {
    Some(acc) => msg!("konto: {}", acc.key()),
    None      => return Err(MyError::NoAccount.into()),
}
```
:::

## Result — bez wyjątków

- `try/catch` ukrywa, które funkcje mogą zawieść — trzeba czytać dokumentację
- W Ruście błąd jest **wartością** widoczną w sygnaturze — nie da się go przeoczyć
- Operator `?` propaguje błąd w górę bez zagnieżdżonych `if`-ów

:::warning Result&lt;T, E&gt;
```rust
fn load(ctx: &Context<Withdraw>) -> Result<u64> {
    let amt = ctx.accounts.vault.balance()?;
    // ? = jeśli Err, zwróć błąd wywołującemu
    Ok(amt)
}
```
:::

## Makra

- Makro to **kod, który pisze kod** — rozwijane przed kompilacją
- Jak formularz z polami do uzupełnienia: makro wstawia boilerplate, autorowi zostaje logika
- `#[...]` to atrybut; `!` po nazwie oznacza wywołanie makra

:::tip Trzy formy
```rust
#[program]                        // atrybut: ozdabia moduł
pub mod vault { /* ... */ }

msg!("wpłacono: {}", amount);     // makro logujące
let ids = vec![pk_a, pk_b];       // makro tworzące Vec
```
:::
