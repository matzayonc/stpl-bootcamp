---
title: Program i Accounts
description: Moduł #[program] z instrukcjami, struktura #[derive(Accounts)] z walidacją i najważniejsze constraints — na skompilowanym programie licznika, z logiem sprawdzenia, które nie przeszło.
sidebar_position: 3
slug: program-i-accounts
---

# Program i Accounts

Dwa z trzech bloków Anchora: gdzie mieszka logika i jak deklaruje się
konta, na których ta logika działa. Kod w tym rozdziale pochodzi z
programu licznika, który jest w całości w rozdziale
[Mini-program](./05-mini-program.md) — tutaj jest pocięty na fragmenty,
żeby każdy element dostał omówienie.

## `#[program]`

Moduł oznaczony `#[program]` grupuje wszystkie instrukcje programu.
Każda publiczna funkcja w tym module to jedna instrukcja, którą klient
może wywołać. Listing 6-4 pokazuje moduł z dwiema.

```rust
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
```

<div className="listing"><strong>Listing 6-4.</strong> Moduł programu z instrukcjami <code>init</code> i <code>increment</code>. Każda funkcja ma <code>Context&lt;T&gt;</code> jako pierwszy argument i zwraca <code>Result&lt;()&gt;</code>.</div>

Trzy reguły obowiązują każdą funkcję w tym module. Pierwszy argument to
zawsze **`Context<T>`**, gdzie `T` to struktura kont tej instrukcji —
`ctx.accounts` daje do nich dostęp już po walidacji, `ctx.bumps` niesie
bumpy wyliczonych PDA, `ctx.program_id` to adres programu. Kolejne
argumenty (`value: u64` w `init`) to dane instrukcji, które Anchor
odczytał z bajtów `data` z Listingu 6-1. Wynik to `Result<()>` — sukces
albo błąd, który cofnie transakcję, jak w rozdziale
[Transakcja](./01-transakcja.md). `use super::*;` importuje do modułu
wszystko, co jest zdefiniowane w pliku poza nim — struktury kont, typy
stanu, błędy.

`init` zapisuje trzy pola nowego licznika: właściciela z klucza konta,
które podpisało, wartość startową z argumentu i bump wyliczony przez
Anchora. `increment` to instrukcja rozłożona linia po linii w rozdziale
[Czytamy razem](../04-rust/05-czytamy-razem.md). Żadna z nich nie
sprawdza niczego — nie ma `if`, nie ma porównań adresów. Wszystkie
sprawdzenia są w typie `T`.

## `#[derive(Accounts)]`

Każda instrukcja ma osobną strukturę z listą wymaganych kont, oznaczoną
`#[derive(Accounts)]`. Z tej struktury Anchor generuje kod, który przy
wywołaniu instrukcji bierze listę kont z transakcji, przypisuje je do
pól po kolei i sprawdza każde pole według jego typu i atrybutów — **zanim**
wykona się ciało funkcji. Listing 6-5 pokazuje obie struktury programu
licznika.

```rust
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
```

<div className="listing"><strong>Listing 6-5.</strong> Struktury kont dla obu instrukcji. Typ pola mówi, czym konto jest; atrybut <code>#[account(...)]</code> mówi, jakie warunki ma spełniać.</div>

Typy pól są pierwszą warstwą sprawdzeń:

- **`Account<'info, Counter>`** — konto danych tego programu typu
  `Counter`. Anchor sprawdza, że `owner` konta to ten program i że
  pierwsze 8 bajtów `data` to dyskryminator `Counter` (rozdział
  [Serializacja i IDL](./04-serializacja-i-idl.md)), po czym
  deserializuje bajty do struktury. Podstawione konto innego programu
  albo innego typu odpada tutaj.
- **`Signer<'info>`** — konto, którego klucz podpisał transakcję. Anchor
  sprawdza flagę `is_signer`. Nic więcej: `Signer` nie ma danych i nie ma
  typu.
- **`Program<'info, System>`** — konkretny program pod znanym adresem.
  Anchor sprawdza, że podany adres to System Program, a nie coś, co się
  pod niego podszywa.

`'info` w każdym typie to lifetime z rozdziału
[Pożyczanie](../04-rust/04-pozyczanie.md) — przepisuje się go z
szablonu.

:::tip Efekt
Luka jest łapana w deklaracji, nie w ręcznym `if`. Struktura kont działa
jak middleware, który waliduje żądanie, zanim dotrze do logiki: ciało
instrukcji może zakładać, że `counter` jest licznikiem tego programu, a
`authority` podpisało — bo gdyby tak nie było, ciało by się nie
wykonało.
:::

## Constraints

Atrybut `#[account(...)]` to druga warstwa: warunki, które Anchor
sprawdza lub akcje, które wykonuje, ponad to, co wynika z typu. Pięć z
Listingu 6-5 pokrywa większość programów.

| Constraint | Co robi | Gdzie w Listingu 6-5 |
|---|---|---|
| `init` | tworzy konto przez CPI do System Programu: przelew depozytu od `payer`, alokacja `space` bajtów, przypisanie `owner`; zapisuje dyskryminator | `Init.counter` |
| `mut` | konto będzie zapisane; Anchor sprawdza `is_writable` i po instrukcji serializuje strukturę z powrotem do bajtów | `Init.user` (traci lamporty), `Increment.counter` |
| `has_one = authority` | pole `counter.authority` musi być równe `authority.key()` — wiąże konto danych z podpisem | `Increment.counter` |
| `seeds = [...]` | adres konta musi być PDA wyliczonym z tych seedów i adresu programu | oba |
| `bump` / `bump = counter.bump` | bez wartości: znajdź kanoniczny bump i udostępnij w `ctx.bumps`; z wartością: użyj podanej i sprawdź | `Init` szuka, `Increment` używa |

`payer = user` i `space = 8 + Counter::INIT_SPACE` to parametry `init`:
kto płaci depozyt i ile bajtów zaalokować. Skąd `8 +` i co liczy
`INIT_SPACE`, wyjaśnia rozdział [Koszt](../05-konta/04-koszt.md); skąd
`seeds` i `bump` — rozdział [Adres i PDA](../05-konta/03-adres-i-pda.md).

Constraints wykonują się w kolejności pól, a w polu — w kolejności
wypisanej. Listing 6-6 pokazuje, co się stało, gdy do `increment` konto
licznika podał ktoś inny niż jego właściciel: obcy klucz jako
`authority`, podpisany obcym kluczem.

```text
Program 6hqBGkDSZTaF5cFshxX1pZPJkM3QAtEHFuWc2VxKdBmY invoke [1]
Program log: Instruction: Increment
Program log: AnchorError caused by account: counter. Error Code: ConstraintSeeds. Error Number: 2006. Error Message: A seeds constraint was violated.
Program log: Left:
Program log: GmCfULKZrQZV94FFAYAqgaUayBrbwiD7v2mY5ckbfHVu
Program log: Right:
Program log: HqPkdQCVfA1CWYWYfJWtCy9iLzd2Ni5S4PAeR6hihGKY
Program 6hqBGkDSZTaF5cFshxX1pZPJkM3QAtEHFuWc2VxKdBmY consumed 5068 of 200000 compute units
Program 6hqBGkDSZTaF5cFshxX1pZPJkM3QAtEHFuWc2VxKdBmY failed: custom program error: 0x7d6
```

<div className="listing"><strong>Listing 6-6.</strong> Obcy klucz podał prawdziwy licznik ofiary jako <code>counter</code>. Pierwsze sprawdzenie, które nie przeszło, to <code>seeds</code> — nie <code>has_one</code>, choć ono też by nie przeszło.</div>

Ten log uczy czegoś, czego nie widać w kodzie. Intuicyjnie to `has_one`
powinno zatrzymać obcego — pole `counter.authority` nie zgadza się z jego
kluczem. Ale `seeds` sprawdza się wcześniej i już ono zawodzi: seedy to
`"counter"` plus klucz *podanego* `authority`, a z obcego klucza wychodzi
inny adres PDA (`Right`) niż adres podanego konta (`Left`). Dla obcego
klucza prawdziwy licznik ofiary po prostu nie jest „jego" adresem.
`has_one` byłby drugą linią obrony, gdyby program nie używał PDA — i
warto go mieć, bo constraints są tanie, a luki nie.

:::warning Kolejność ma znaczenie
Constraints sprawdzają się od góry do dołu, pole po polu. Gdy kilka może
zawieść, w logu pojawi się pierwsze — a to nie zawsze to, którego
programista szuka. Przy diagnozie warto przeczytać całą strukturę kont, nie
tylko wiersz z błędem.
:::

Dwa bloki są omówione: co program robi i na czym. Został trzeci — jak
wygląda stan, czyli co dokładnie leży w tych 49 bajtach, które `init`
zapisało w koncie. To temat następnego rozdziału.
