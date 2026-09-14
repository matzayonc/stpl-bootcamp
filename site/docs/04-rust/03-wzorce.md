---
title: Wzorce Rusta
description: Niemutowalność, struct + impl, typy z Anchora, match, Option, Result i makra — siedem wzorców, każdy z analogią, kodem i prawdziwym komunikatem kompilatora, który mówi „nie".
sidebar_position: 3
slug: wzorce
---

# Wzorce Rusta

Siedem konstrukcji odróżnia Rust od JavaScriptu na tyle, żeby zatrzymać
czytającego. Każda z nich zamyka jedną klasę błędów na etapie kompilacji
— i każda ma komunikat, którym kompilator to robi. Ten rozdział pokazuje
wszystkie siedem w tej samej kolejności, w jakiej pojawiają się w
typowym `lib.rs`, z kodem, który się kompiluje, i kodem, który się nie
kompiluje.

:::note To jest trudne
To najdłuższy rozdział tematu i nie trzeba go czytać na raz. Sekcje są
niezależne; do każdej można wrócić, gdy dana konstrukcja pojawi się w
programie na sesji live. Komunikaty błędów są wklejone w całości, bo
czytanie ich jest umiejętnością, którą ten rozdział ćwiczy.
:::

## Niemutowalność

W JavaScripcie każda zmienna zadeklarowana przez `let` jest mutowalna,
a `const` trzeba wybrać świadomie. W Ruście jest **odwrotnie**: `let`
tworzy zmienną, której nie da się zmienić, a mutowalność trzeba
zadeklarować słowem `mut`. Listing 4-4 pokazuje, co się dzieje, gdy się o
tym zapomni.

```rust
fn main() {
    let x = 5;
    x = 6;
    println!("{x}");
}
```

```text
error[E0384]: cannot assign twice to immutable variable `x`
 --> immut.rs:3:5
  |
2 |     let x = 5;
  |         - first assignment to `x`
3 |     x = 6;
  |     ^^^^^ cannot assign twice to immutable variable
  |
help: consider making this binding mutable
  |
2 |     let mut x = 5;
  |         +++
```

<div className="listing"><strong>Listing 4-4.</strong> Przypisanie do niemutowalnej zmiennej. Kompilator wskazuje obie linie — deklarację i próbę zmiany — i proponuje poprawkę.</div>

Komunikat ma stały układ, który warto raz przeczytać uważnie. Pierwsza
linia to kod błędu (`E0384`) i opis jednym zdaniem. Strzałka `-->` mówi,
gdzie: plik, linia, kolumna. Fragment kodu pod spodem ma dwa rodzaje
podkreśleń — `-` oznacza kontekst („tu było pierwsze przypisanie"), `^`
oznacza miejsce błędu. Sekcja `help:` to gotowa poprawka, często z
dokładnym tekstem do wstawienia. Dziewięć na dziesięć błędów Rusta da się
naprawić, czytając tylko `help:`.

Po co ta odwrotność? W programie, który obsługuje pieniądze, większość
wartości **nie powinna** się zmieniać: adres właściciela, wysokość
depozytu, adres programu. `mut` przy zmiennej to widoczna w kodzie
deklaracja „tę wartość zamierzam zmienić", i kompilator pilnuje, żeby
lista takich miejsc była pełna. W Anchorze to samo słowo pojawia się w
constraincie `#[account(mut)]` — konto, które nie jest oznaczone jako
`mut`, nie może zostać zapisane, a próba zapisu jest błędem.

:::tip Analogia — arkusz z ochroną komórek
W arkuszu z włączoną ochroną każda komórka jest tylko do odczytu, dopóki
ktoś jawnie jej nie odblokuje. Edycja przez przypadek jest niemożliwa;
edycja zamierzona jest widoczna, bo wymaga jawnej akcji. `let` to
zablokowana komórka, `let mut` — odblokowana.
:::

## Brak klas

Rust nie ma `class`. Ma `struct` na dane i `impl` na metody, jako dwa
osobne bloki, które mogą być w różnych miejscach pliku. Nie ma
dziedziczenia — zamiast hierarchii klas są **traity**, czyli interfejsy,
które typ implementuje, a o których w tym kursie wystarczy wiedzieć, że
istnieją. Listing 4-5 pokazuje strukturę z jedną metodą.

```rust
struct Licznik {
    wartosc: u64,
}

impl Licznik {
    fn inkrementuj(&mut self) {
        self.wartosc += 1;
    }
}

fn main() {
    let mut l = Licznik { wartosc: 41 };
    l.inkrementuj();
    println!("{}", l.wartosc);
}
```

```bash
$ rustc implx.rs && ./implx
42
```

<div className="listing"><strong>Listing 4-5.</strong> Dane w <code>struct</code>, zachowanie w <code>impl</code>. Metoda, która zmienia strukturę, deklaruje to przez <code>&mut self</code>, a wywołać ją można tylko na zmiennej z <code>mut</code>.</div>

`&mut self` w sygnaturze metody to ten sam mechanizm co `let mut`:
metoda mówi, że będzie zmieniać obiekt, na którym ją wywołano. Metoda,
która tylko czyta, ma `&self`. Gdyby `l` w `main` zostało zadeklarowane
bez `mut`, wywołanie `l.inkrementuj()` skończyłoby się błędem podobnym do
Listingu 4-4. Co znaczy sam znak `&`, wyjaśnia rozdział
[Pożyczanie](./04-pozyczanie.md).

W programie Anchora każdy typ — stan konta, struktura kont instrukcji —
jest `struct`. Metody generuje framework; w kodzie użytkownika bloki
`impl` są rzadkie. Wystarczy je rozpoznawać.

## Typy w Anchorze

Kilka typów wraca w każdym programie i warto je znać z widzenia.

| Typ | Znaczenie | Rozmiar |
|---|---|---|
| `u8`, `u16`, `u32`, `u64` | liczba całkowita bez znaku | 1, 2, 4, 8 bajtów |
| `i64` | liczba całkowita ze znakiem (np. znacznik czasu) | 8 bajtów |
| `bool` | prawda / fałsz | 1 bajt |
| `Pubkey` | adres konta, 32 bajty | 32 bajty |
| `String` | tekst | 4 bajty długości + treść |
| `Vec<T>` | lista elementów typu `T` | 4 bajty długości + elementy |

`u` w nazwie typu liczbowego znaczy *unsigned* — brak znaku, brak liczb
ujemnych. Salda, liczniki i rozmiary są zawsze bez znaku, bo ujemne saldo
nie ma sensu, a próba odjęcia większej liczby od mniejszej powinna być
błędem, nie liczbą ujemną. Listing 4-6 pokazuje typowy stan konta
zbudowany z tych typów.

```rust
#[account]
pub struct Stan {
    pub wlasciciel: Pubkey,       // adres
    pub saldo:      u64,          // liczba dodatnia
    pub aktywny:    bool,         // flaga
    pub glosy:      Vec<Pubkey>,  // lista adresów
}
```

<div className="listing"><strong>Listing 4-6.</strong> Struktura stanu konta w Anchorze. <code>pub</code> czyni pole widocznym poza modułem; <code>#[account]</code> to makro, o którym mówi ostatnia sekcja.</div>

Rozmiar tej struktury to 32 + 8 + 1 + (4 + 32 · liczba głosów) bajtów, i
z tej sumy rozdział [Koszt](../05-konta/04-koszt.md) wylicza depozyt za
konto. `Vec` i `String` mają zmienną długość — dlatego Anchor każe
zadeklarować ich maksimum, zanim konto powstanie.

## Match

`switch` w JavaScripcie milcząco pomija przypadki, których nie
wymieniono; błąd ujawnia się, gdy taki przypadek nadejdzie w runtime.
Rustowy `match` wymaga pokrycia **wszystkich** możliwości — brakująca
gałąź to błąd kompilacji, co pokazuje Listing 4-7.

```rust
enum Status { New, Active, Closed }

fn label(s: Status) -> &'static str {
    match s {
        Status::New    => "nowy",
        Status::Active => "aktywny",
    }
}
```

```text
error[E0004]: non-exhaustive patterns: `Status::Closed` not covered
 --> matchx.rs:3:11
  |
3 |     match s {
  |           ^ pattern `Status::Closed` not covered
  |
note: `Status` defined here
 --> matchx.rs:1:6
  |
1 | enum Status { New, Active, Closed }
  |      ^^^^^^                ------ not covered
  = note: the matched value is of type `Status`
help: ensure that all possible cases are being handled by adding a match arm with a wildcard pattern or an explicit pattern as shown
  |
5 ~         Status::Active => "aktywny",
6 ~         Status::Closed => todo!(),
  |
```

<div className="listing"><strong>Listing 4-7.</strong> Niewyczerpujący <code>match</code>. Kompilator wymienia dokładnie, którego wariantu brakuje, i wskazuje jego definicję.</div>

`enum` to typ o skończonej liczbie wariantów — tutaj trzech. `match`
sprawdza wartość po kolei z każdą gałęzią i wykonuje pierwszą pasującą;
strzałka `=>` oddziela wzorzec od wyniku. Kompilator zna listę wariantów
z definicji `enum`, więc wie, że `Closed` nie jest obsłużony. Gałąź `_`
(podkreślenie) pasuje do wszystkiego, co zostało — jest odpowiednikiem
`default` i wycisza ten błąd, ale użyta bezmyślnie przywraca problem ze
`switch`. W kodzie on-chain lepiej wymienić wszystkie warianty jawnie:
dodanie nowego wariantu do `enum` za pół roku spowoduje wtedy błąd
kompilacji w każdym `match`, który trzeba zaktualizować, zamiast cichego
przejścia przez `_`.

:::tip Analogia — lista kontrolna pilota
Procedura przed startem nie jest ukończona, dopóki każdy punkt nie został
odhaczony — nie ma opcji „reszta pewnie w porządku". `match` to lista
kontrolna, którą kompilator sprawdza za pilota.
:::

## Option — bez null

`null` w JavaScripcie i `None` w Pythonie mają wspólną wadę: można je
przekazać wszędzie tam, gdzie oczekiwana jest wartość, a błąd pojawia
się dopiero przy próbie użycia — często daleko od miejsca, w którym
pustka powstała. Rust nie ma `null`. Wartość, która może nie istnieć, ma
typ **`Option<T>`**: albo `Some(wartość)`, albo `None`. I `Option<T>` nie
jest tym samym typem co `T` — nie da się go użyć jak wartości bez
sprawdzenia, co pokazuje Listing 4-8.

```rust
fn main() {
    let accounts: Vec<u64> = vec![];
    let first: Option<&u64> = accounts.first();
    let doubled = first * 2;
    println!("{doubled}");
}
```

```text
error[E0369]: cannot multiply `Option<&u64>` by `{integer}`
   --> option.rs:4:25
    |
  4 |     let doubled = first * 2;
    |                   ----- ^ - {integer}
    |                   |
    |                   Option<&u64>
    |
note: `Option<&u64>` does not implement `Mul<{integer}>`
```

<div className="listing"><strong>Listing 4-8.</strong> Próba użycia <code>Option</code> jak liczby. Kompilator nie zgaduje, co zrobić z <code>None</code> — każe autorowi zdecydować.</div>

`accounts.first()` zwraca pierwszy element listy — albo `None`, gdy lista
jest pusta. W JavaScripcie `[][0] * 2` daje `NaN` i program idzie dalej.
W Ruście program nie istnieje, dopóki autor nie napisze, co ma się stać w
przypadku `None`. Najczęstsze narzędzie to `match` z poprzedniej sekcji,
jak w Listingu 4-9.

```rust
fn main() {
    let accounts: Vec<u64> = vec![];
    match accounts.first() {
        Some(acc) => println!("pierwsze konto: {acc}"),
        None      => println!("brak kont"),
    }
}
```

```bash
$ rustc optmatch.rs && ./optmatch
brak kont
```

<div className="listing"><strong>Listing 4-9.</strong> Obsłużone obie możliwości. Wewnątrz gałęzi <code>Some(acc)</code> zmienna <code>acc</code> ma już zwykły typ liczbowy.</div>

W programie Anchora `Option` pojawia się przy operacjach, które mogą się
nie udać bez winy nikogo: `checked_add` zwraca `None`, gdy suma nie
mieści się w `u64`; wyszukiwanie w liście zwraca `None`, gdy elementu
nie ma. Rozdział [Czytamy razem](./05-czytamy-razem.md) pokazuje, jak
`Option` zamienia się w błąd instrukcji jednym wywołaniem.

:::tip Analogia — paczka kurierska
Kurier albo zostawia paczkę pod drzwiami (`Some`), albo awizo (`None`).
Nie ma trzeciej opcji — cichego braku paczki, o którym nikt nie wie.
Odbiorca musi sprawdzić, co zastał, zanim otworzy pudełko.
:::

## Result — bez wyjątków

`try/catch` ma tę samą wadę co `null`: patrząc na sygnaturę funkcji, nie
widać, czy może rzucić wyjątek, a `catch` bez treści połyka błąd bez
śladu. W Ruście błąd jest **wartością** zwracaną z funkcji, widoczną w
jej typie: **`Result<T, E>`** to albo `Ok(wartość)`, albo `Err(błąd)`.
Listing 4-10 pokazuje funkcję, która może zawieść, i jak się ją wywołuje.

```rust
use std::num::ParseIntError;

fn parse_amount(s: &str) -> Result<u64, ParseIntError> {
    let n = s.trim().parse::<u64>()?;
    Ok(n)
}

fn main() {
    println!("{:?}", parse_amount("42"));
    println!("{:?}", parse_amount("dużo"));
}
```

```bash
$ rustc result.rs && ./result
Ok(42)
Err(ParseIntError { kind: InvalidDigit })
```

<div className="listing"><strong>Listing 4-10.</strong> Funkcja zwracająca <code>Result</code>. Operator <code>?</code> po <code>parse</code> przekazuje błąd wyżej, jeśli wystąpił; w przeciwnym razie wyłuskuje wartość.</div>

Sygnatura mówi wszystko: `parse_amount` zwraca `u64` albo `ParseIntError`
— nic innego nie może z niej wyjść, a wywołujący musi to obsłużyć, bo
`Result<u64, _>` nie jest `u64`, tak samo jak `Option` w Listingu 4-8.
Operator **`?`** to skrót na najczęstszy przypadek obsługi: „jeśli to
`Err`, zwróć ten błąd z bieżącej funkcji; jeśli `Ok`, wyciągnij wartość
i idź dalej". Zastępuje zagnieżdżone `if`, a jednocześnie nie pozwala
zapomnieć o błędzie — bez `?` albo `match` kompilator ostrzeże, że
`Result` został zignorowany.

W Anchorze każda instrukcja zwraca `Result<()>` — sukces bez wartości
albo błąd programu. `Ok(())` na końcu ciała instrukcji to jawne „udało
się"; każde `?` w ciele to miejsce, w którym instrukcja może się zakończyć
błędem, a cała transakcja — cofnąć. Kod błędu, który trafi do logu,
pochodzi z wartości `Err`.

:::warning Result nie da się przeoczyć
W JavaScripcie funkcja, która może rzucić wyjątek, wygląda tak samo jak
ta, która nie może. W Ruście różnica jest w typie zwracanym, a kompilator
odmawia użycia `Result` jak zwykłej wartości. Ceną jest `?` w wielu
linijkach; zyskiem — brak ścieżki, na której błąd znika bez śladu.
:::

## Makra

Ostatnia konstrukcja nie jest typem ani instrukcją. **Makro** to kod,
który pisze kod: kompilator rozwija je przed właściwą kompilacją,
wstawiając w to miejsce wygenerowany Rust. W programie Anchora makra są
wszędzie i mają trzy formy, pokazane w Listingu 4-11.

```rust
#[program]                        // atrybut: ozdabia moduł
pub mod vault { /* ... */ }

msg!("wpłacono: {}", amount);     // makro logujące
let ids = vec![pk_a, pk_b];       // makro tworzące Vec
```

<div className="listing"><strong>Listing 4-11.</strong> Trzy formy makr. Atrybut <code>#[...]</code> stoi nad elementem i go przekształca; wykrzyknik po nazwie oznacza wywołanie makra w miejscu wyrażenia.</div>

`#[program]`, `#[derive(Accounts)]`, `#[account]` to **atrybuty** — makra,
które biorą element pod sobą (moduł, strukturę) i generują wokół niego
dodatkowy kod: walidację kont, serializację, punkt wejścia programu.
Rozdział [Czym jest Anchor](../06-transakcje-i-anchor/02-czym-jest-anchor.md)
opisuje, co dokładnie każdy z nich dopisuje. `msg!` i `vec!` to makra
**wywoływane** jak funkcje, z wykrzyknikiem: `msg!` zapisuje tekst do
logu programu (to ten log, który pokazuje `solana confirm -v`), `vec!`
buduje listę z elementów. `println!` z Listingu 4-3 jest tego samego
rodzaju. Wykrzyknik jest sygnałem: to nie funkcja, kompilator zrobi tu
coś więcej niż wywołanie.

:::tip Analogia — formularz
Makro to formularz z polami do uzupełnienia: autor wpisuje tylko to, co
jest specyficzne dla jego przypadku, a cała reszta — nagłówki, klauzule,
podpisy — jest dopisywana według wzoru. `#[derive(Accounts)]` nad
strukturą to formularz, który generuje kilkadziesiąt linii sprawdzeń z
kilku linii deklaracji.
:::

Siedem wzorców to prawie cały słownik. Został jeden znak, który pojawia
się w każdej sygnaturze i który Listing 4-5 przemilczał: `&`. Następny
rozdział wyjaśnia, dlaczego Rust nie kopiuje danych i co w zamian
proponuje.
