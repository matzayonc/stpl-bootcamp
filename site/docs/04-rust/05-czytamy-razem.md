---
title: Czytamy razem
description: Prawdziwa instrukcja increment z programu licznika — wszystkie wzorce w dziesięciu liniach — plus log z jej wykonania i log z błędu, który Result przekazał do sieci.
sidebar_position: 5
slug: czytamy-razem
---

# Czytamy razem

Wszystkie wzorce z tego tematu w jednym fragmencie. Listing 4-14 to
instrukcja `increment` z programu licznika, który jest tematem rozdziału
[Transakcje i Anchor](../06-transakcje-i-anchor/index.md) — skompilowana,
przetestowana i wykonana, z logami pokazanymi niżej. Szczegóły frameworku
(skąd bierze się `Context`, co robi `#[account]`) są tam; tutaj chodzi
wyłącznie o to, żeby każdą linię dało się przeczytać.

## Instrukcja `increment`

```rust
pub fn increment(ctx: Context<Increment>) -> Result<()> {   // 1
    let counter = &mut ctx.accounts.counter;                // 2
    counter.value = counter                                 // 3
        .value                                              // 4
        .checked_add(1)                                     // 5
        .ok_or(LicznikError::Overflow)?;                    // 6
    msg!("Licznik: {}", counter.value);                     // 7
    Ok(())                                                  // 8
}

#[error_code]
pub enum LicznikError {
    #[msg("Licznik przekroczył zakres u64")]
    Overflow,
}
```

<div className="listing"><strong>Listing 4-14.</strong> Instrukcja, która zwiększa licznik o jeden, i typ błędu, który może zwrócić. Numery linii w komentarzach służą omówieniu poniżej.</div>

**Linia 1** to sygnatura z rozdziału [Składnia](./02-skladnia.md): funkcja
`increment`, jeden argument `ctx` typu `Context<Increment>`, wynik
`Result<()>`. `Context<T>` to typ generyczny — struktura, która trzyma
konta opisane przez typ `Increment` i kilka metadanych. `pub` czyni
funkcję widoczną poza modułem; Anchor wymaga tego, żeby wystawić ją jako
instrukcję.

**Linia 2** to pożyczka do zapisu z rozdziału [Pożyczanie](./04-pozyczanie.md).
`ctx.accounts.counter` to konto licznika; `&mut` mówi, że ta instrukcja
je zmieni. Od tej chwili do końca funkcji nikt inny nie może go
pożyczyć. `let` bez `mut` — sama zmienna `counter` nie będzie
przypisywana ponownie, choć to, na co wskazuje, tak.

**Linie 3–6** to jedno wyrażenie rozbite na cztery linie, czytane od
góry. `counter.value` to obecna wartość, typu `u64`. `.checked_add(1)`
dodaje jeden i zwraca `Option<u64>` — `Some(suma)`, jeśli wynik mieści się
w `u64`, `None`, jeśli by się przekręcił. `.ok_or(LicznikError::Overflow)`
zamienia `Option` w `Result`: `Some(x)` staje się `Ok(x)`, a `None` —
`Err(Overflow)`. Znak `?` na końcu robi to, co w Listingu 4-10: jeśli
`Err`, natychmiast zwraca ten błąd z całej instrukcji; jeśli `Ok`,
wyłuskuje sumę, która trafia do `counter.value` po lewej stronie `=`.
Cztery linie, dwa typy z rozdziału [Wzorce](./03-wzorce.md), zero
możliwości, żeby przekręcony licznik przeszedł niezauważony.

**Linia 7** to makro `msg!` — zapis do logu programu, z `{}` zastąpionym
wartością. To ten log, który widać w Explorerze i w `solana confirm -v`.

**Linia 8** to jawny sukces: `Ok(())`. Brak średnika sprawia, że jest to
wartość zwracana z funkcji.

**`LicznikError`** to `enum` z jednym wariantem, ozdobiony makrem
`#[error_code]`, które nadaje mu numer (od 6000 w górę) i tekst z
`#[msg]`. To wszystko, co potrzeba, żeby `?` w linii 6 miało co zwrócić.

## Wykonanie

Listing 4-15 to log z wykonania tej instrukcji w teście, po
wcześniejszym ustawieniu licznika na 41.

```text
Program 6hqBGkDSZTaF5cFshxX1pZPJkM3QAtEHFuWc2VxKdBmY invoke [1]
Program log: Instruction: Increment
Program log: Licznik: 42
Program 6hqBGkDSZTaF5cFshxX1pZPJkM3QAtEHFuWc2VxKdBmY consumed 3991 of 200000 compute units
Program 6hqBGkDSZTaF5cFshxX1pZPJkM3QAtEHFuWc2VxKdBmY success
```

<div className="listing"><strong>Listing 4-15.</strong> Log udanego wywołania. Linia <code>Licznik: 42</code> pochodzi z <code>msg!</code>; <code>success</code> to <code>Ok(())</code> widziane przez runtime.</div>

Pierwsza i ostatnia linia to runtime: wywołanie programu i jego wynik.
`Instruction: Increment` dopisuje Anchor. `consumed 3991 of 200000
compute units` to koszt obliczeniowy — jednostki, o których mówi rozdział
[Adres i PDA](../05-konta/03-adres-i-pda.md) przy okazji wyliczania
bumpa.

Listing 4-16 to ten sam kod, gdy licznik ustawiono wcześniej na
maksymalną wartość `u64`.

```text
Program 6hqBGkDSZTaF5cFshxX1pZPJkM3QAtEHFuWc2VxKdBmY invoke [1]
Program log: Instruction: Increment
Program log: AnchorError occurred. Error Code: Overflow. Error Number: 6000. Error Message: Licznik przekroczył zakres u64.
Program 6hqBGkDSZTaF5cFshxX1pZPJkM3QAtEHFuWc2VxKdBmY consumed 4404 of 200000 compute units
Program 6hqBGkDSZTaF5cFshxX1pZPJkM3QAtEHFuWc2VxKdBmY failed: custom program error: 0x1770
```

<div className="listing"><strong>Listing 4-16.</strong> Ta sama instrukcja z przekręconym dodawaniem. <code>checked_add</code> zwróciło <code>None</code>, <code>ok_or</code> zamieniło je w <code>Err(Overflow)</code>, <code>?</code> zwróciło błąd, runtime cofnął transakcję.</div>

Cała ścieżka błędu z linii 5–6 jest widoczna w logu: nazwa wariantu
(`Overflow`), numer (`6000`, czyli `0x1770`) i tekst z `#[msg]`. Nie ma
`msg!("Licznik: …")`, bo funkcja zakończyła się w linii 6 — linia 7 się
nie wykonała. Nie ma też zmienionej wartości w koncie: transakcja, która
zwraca `Err`, nie zapisuje niczego, jak wyjaśnia rozdział
[Transakcja](../06-transakcje-i-anchor/01-transakcja.md). W JavaScripcie
`value + 1` przy maksimum dałoby po prostu błędną liczbę i program
poszedłby dalej. Tutaj nie ma takiej ścieżki.

:::note Wszystkie wzorce w jednym miejscu
Sygnatura z typem po nazwie i strzałką (Składnia). `&mut` jako pożyczka
do zapisu (Pożyczanie). `Option` z `checked_add` i `Result` z `ok_or`
oraz `?` (Wzorce). `msg!` i `#[error_code]` jako makra (Wzorce). `Ok(())`
jako jawny sukces. Dziesięć linii, cały słownik tego tematu.
:::

Kto przeczytał Listing 4-14 bez zatrzymywania się, ma z Rusta tyle, ile
ten kurs wymaga. Następny temat odkłada język na bok i pyta o to, na czym
`increment` pracuje — czym jest `ctx.accounts.counter`, skąd ma adres i
ile kosztuje.
