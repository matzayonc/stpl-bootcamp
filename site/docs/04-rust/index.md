---
title: Rust dla Anchora
description: Minimum Rusta potrzebne, żeby czytać lib.rs programu Anchora — składnia, siedem wzorców z prawdziwymi komunikatami kompilatora, pożyczanie i jedna autentyczna instrukcja rozłożona linia po linii.
sidebar_position: 0
---

# Rust dla Anchora

Jedno zdanie organizuje ten temat: **kompilator Rusta odrzuca całe klasy
błędów, zanim kod dotrze na sieć**. Nie ma `null`, więc nie ma dostępu do
pustej wartości bez sprawdzenia; błąd jest wartością zwracaną, więc nie
da się go zignorować; dwa zapisy naraz nie przechodzą kompilacji. Kto
zrozumie, *czego* kompilator odmawia i *dlaczego*, ten czyta program
Anchora bez zatrzymywania się — a o to, nie o pełny język, chodzi.

Rozdział rozwija slajdy *Szybki Rust*
([PDF](https://github.com/matzayonc/stpl-slides/releases/download/latest/4_rust.pdf))
o rzeczy, na które na wykładzie nie ma czasu: pełne komunikaty
kompilatora dla każdego z wzorców, kod, który się kompiluje, obok kodu,
który się nie kompiluje, i instrukcję z prawdziwego programu z logami z
jej wykonania — udanego i nieudanego.

## Zawartość

1. [Po co Rust?](./01-po-co-rust.md) — zakres tematu, dlaczego kod
   obsługujący pieniądze potrzebuje języka, który mówi „nie" przed
   uruchomieniem, SBF i Anchor.
2. [Składnia](./02-skladnia.md) — funkcja z typem po nazwie i strzałką,
   `struct` jako rekord pól, pierwszy program i `rustc`.
3. [Wzorce Rusta](./03-wzorce.md) — niemutowalność, `struct` + `impl`,
   typy z Anchora, `match`, `Option`, `Result` z `?`, makra — każdy z
   komunikatem kompilatora.
4. [Pożyczanie](./04-pozyczanie.md) — `&` i `&mut`, jedna reguła
   (wielu czytających albo jeden piszący), błąd E0502, związek z
   Sealevelem.
5. [Czytamy razem](./05-czytamy-razem.md) — instrukcja `increment`
   linia po linii, log sukcesu i log błędu `Overflow`.

Pytania sprawdzające do rozdziału: [Rust — pytania
kontrolne](../08-pytania-kontrolne/04-rust.md).

## Podsumowanie

Rust nie jest celem, tylko warunkiem: programy on-chain pisze się w nim,
bo błąd w kodzie obsługującym cudze pieniądze jest nieodwracalny, a Rust
zamienia najczęstsze klasy takich błędów w błędy kompilacji. Zakres
tematu to rozpoznawanie, nie pisanie — `mut`, `struct`, `match`,
`Option`, `Result`, `&`, `&mut`, makra.

Składnia jest znajoma po TypeScripcie: `nazwa: Typ` w argumentach i
polach, `-> Typ` dla wyniku, `let` bez typu, gdy kompilator go
wywnioskuje. `struct` to rekord pól bez metod; metody żyją osobno w
`impl`, klas i dziedziczenia nie ma.

Siedem wzorców, siedem odmów kompilatora. Zmienna jest **niemutowalna**,
dopóki nie dostanie `mut` (E0384). **`match`** musi pokryć wszystkie
warianty (E0004). **`Option<T>`** nie jest `T` — `None` trzeba obsłużyć,
zanim wartość da się użyć (E0369). **`Result<T, E>`** niesie błąd jako
wartość widoczną w sygnaturze, a **`?`** przekazuje go wyżej bez
zagnieżdżonych `if`. **Makra** — atrybuty `#[...]` nad elementem i
wywołania z `!` — generują kod, którego autor nie musi pisać.

**Pożyczanie** zastępuje kopiowanie: `&T` to dostęp do odczytu, `&mut T`
do zapisu, a kompilator pilnuje, żeby w danej chwili istniało wiele `&`
albo jedno `&mut`, nigdy oba (E0502). Ta sama reguła, zastosowana do kont
zamiast zmiennych, to Sealevel.

Instrukcja `increment` składa to wszystko w dziesięć linii: `&mut` na
koncie, `checked_add` zwracający `Option`, `ok_or` zamieniający go w
`Result`, `?` zwracający błąd, `msg!` do logu, `Ok(())` na koniec. Log
udanego wywołania ma `Licznik: 42` i `success`; log przekręconego
dodawania ma `Error Number: 6000` i `failed` — i żadnej zmiany w koncie.

:::tip Analogia na koniec
`let` to komórka arkusza z ochroną, `match` to lista kontrolna pilota,
`Option` to paczka albo awizo, `Result` to błąd, którego nie da się
zgubić, makro to formularz z polami, a pożyczanie to biblioteka, w której
wielu może czytać, ale notatki robi jeden.
:::

## Ćwiczenia

Ćwiczenia wymagają zainstalowanego `rustc` (przez `rustup`); nie wymagają
Anchora ani sieci.

1. **Przeczytaj błąd, zanim naprawisz.** Przepisz Listing 4-13 i
   skompiluj go. Następnie usuń linię z `println!` i skompiluj ponownie.
   Wyjaśnij jednym zdaniem, dlaczego druga wersja się kompiluje, choć
   nadal ma `&v` i `&mut v` w sąsiednich liniach. Które słowa z
   komunikatu błędu na to wskazują?

2. **Wyczerpujący `match`.** Do `enum Status` z Listingu 4-7 dodaj
   czwarty wariant `Frozen` i uzupełnij `match` tak, żeby program
   kompilował się bez `_`. Następnie zamień ostatnią gałąź na `_ =>
   "inny"` i ponownie dodaj piąty wariant. Który z dwóch programów
   zauważy, że piąty wariant nie ma etykiety?

3. **Bezpieczne odejmowanie.** Napisz funkcję `withdraw(balance: u64,
   amount: u64) -> Result<u64, String>`, która zwraca nowe saldo albo
   błąd `"insufficient funds"`, używając `checked_sub` i `ok_or`. Wywołaj
   ją dla `(10, 3)` i `(3, 10)` i wypisz oba wyniki przez `{:?}`. Co
   zwróciłoby zwykłe `balance - amount` dla drugiej pary i dlaczego Rust
   tego nie pozwala w trybie release Anchora?

4. **Trzy formy makr.** W Listingu 4-14 wskaż każde użycie makra i
   określ jego formę (atrybut czy wywołanie z `!`). Następnie w
   `lib.rs` z rozdziału [Mini-program](../06-transakcje-i-anchor/05-mini-program.md)
   policz wszystkie makra i zapisz, co każde z nich generuje według
   opisu z rozdziału [Czym jest Anchor](../06-transakcje-i-anchor/02-czym-jest-anchor.md).
