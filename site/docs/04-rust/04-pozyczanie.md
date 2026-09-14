---
title: Pożyczanie
description: Referencje & i &mut — Rust nie kopiuje danych, tylko pożycza; jeden piszący albo wielu czytających, nigdy oba naraz — z komunikatem kompilatora, który tego pilnuje.
sidebar_position: 4
slug: pozyczanie
---

# Pożyczanie

Znak `&` pojawił się w Listingach 4-5 i 4-10 bez wyjaśnienia. To
najbardziej rustowy element języka i jedyny, który nie ma odpowiednika
w JavaScripcie ani Pythonie. Ten rozdział wyjaśnia go w zakresie
potrzebnym do czytania programu Anchora — bez wchodzenia w lifetime'y,
które są tematem osobnego semestru.

## Referencja zamiast kopii

W JavaScripcie przekazanie obiektu do funkcji przekazuje referencję,
a przekazanie liczby — kopię, i język nie daje wyboru. Rust daje wybór i
wymaga, żeby był widoczny. Domyślnie przekazanie wartości do funkcji
**przenosi** ją — po wywołaniu oryginalna zmienna przestaje być dostępna.
Żeby funkcja dostała dostęp do danych bez przejęcia ich na własność,
przekazuje się **referencję**: `&wartość`. Funkcja *pożycza* dane;
właściciel się nie zmienia, a po powrocie z funkcji dane są tam, gdzie
były.

Referencje są dwojakie. `&T` to pożyczka **do odczytu** — funkcja może
patrzeć, nie może zmieniać. `&mut T` to pożyczka **do zapisu** — funkcja
może zmieniać, i to jest jedyny sposób, żeby funkcja zmieniła coś, co do
niej nie należy. Listing 4-12 pokazuje obie.

```rust
struct Vault { balance: u64 }

fn read_vault(v: &Vault)            { println!("saldo: {}", v.balance); }
fn add_funds(v: &mut Vault, n: u64) { v.balance += n; }

fn main() {
    let mut v = Vault { balance: 10 };
    read_vault(&v);
    read_vault(&v);
    add_funds(&mut v, 5);
    read_vault(&v);
}
```

```bash
$ rustc borrow_ok.rs && ./borrow_ok
saldo: 10
saldo: 10
saldo: 15
```

<div className="listing"><strong>Listing 4-12.</strong> Dwie funkcje: jedna pożycza do odczytu, druga do zapisu. Wywołujący widzi w miejscu wywołania, która jest która, bo musi napisać <code>&v</code> albo <code>&mut v</code>.</div>

Sygnatura mówi wszystko o tym, co funkcja może zrobić z argumentem.
`read_vault(v: &Vault)` nie jest w stanie zmienić salda — próba
przypisania do `v.balance` w jej ciele to błąd kompilacji.
`add_funds(v: &mut Vault, …)` może, i każdy, kto ją wywołuje, wie o tym
z samego `&mut` w miejscu wywołania. To jest ta sama informacja, którą
`let mut` dawało o zmiennych, przeniesiona na granice funkcji.

## Jedna reguła

Pożyczanie ma jedną regułę, której pilnuje kompilator: w danym momencie
istnieje **albo dowolnie wiele referencji `&`, albo dokładnie jedna
`&mut`** — nigdy obie naraz.

<div className="diagram">

![Trzy funkcje czytają Vault przez & jednocześnie; osobno jedna funkcja pisze przez &mut, mając wyłączny dostęp](/img/diagrams/4_rust-01.svg)

</div>

Listing 4-13 pokazuje, co się dzieje, gdy kod tę regułę łamie.

```rust
struct Vault { balance: u64 }

fn main() {
    let mut v = Vault { balance: 10 };
    let reader = &v;
    let writer = &mut v;
    writer.balance += 1;
    println!("{}", reader.balance);
}
```

```text
error[E0502]: cannot borrow `v` as mutable because it is also borrowed as immutable
 --> borrow.rs:5:18
  |
4 |     let reader = &v;
  |                  -- immutable borrow occurs here
5 |     let writer = &mut v;
  |                  ^^^^^^ mutable borrow occurs here
6 |     writer.balance += 1;
7 |     println!("{}", reader.balance);
  |                    -------------- immutable borrow later used here
```

<div className="listing"><strong>Listing 4-13.</strong> Pożyczka do zapisu, gdy trwa pożyczka do odczytu. Kompilator wskazuje trzy miejsca: początek pierwszej pożyczki, początek drugiej i użycie, które sprawia, że pierwsza wciąż trwa.</div>

Komunikat warto przeczytać jako historię. Linia 4 pożycza `v` do
odczytu. Linia 5 próbuje pożyczyć do zapisu — ale pierwsza pożyczka
jeszcze trwa, bo `reader` jest użyty w linii 7. Gdyby linia 7 nie
istniała, kod by się skompilował: kompilator liczy pożyczkę do
ostatniego użycia, nie do końca bloku. Problem, który ten błąd
uniemożliwia, to odczyt wartości w trakcie jej modyfikacji — źródło
wyścigów danych w językach wielowątkowych i subtelnych błędów w każdym
innym.

W programie Anchora reguła ma bezpośrednie przełożenie. Konto pożyczone
jako `&mut ctx.accounts.vault` ma w ciele instrukcji wyłączny dostęp;
druga próba pożyczenia tego samego konta do zapisu to Listing 4-13.
Runtime Solany egzekwuje tę samą zasadę między transakcjami — dwie
transakcje, które chcą zapisać to samo konto, wykonują się po kolei, a
dwie, które tylko czytają, równolegle. Sealevel z rozdziału [Dlaczego
Solana?](../01-blockchain/04-dlaczego-solana.md) to reguła pożyczania
zastosowana do całej sieci.

:::note Sygnatury
```rust
fn read_vault(v: &Vault)            { msg!("{}", v.balance); }
fn add_funds(v: &mut Vault, n: u64) { v.balance += n; }
```

`&` — czytam, nie zmieniam, może być wielu naraz. `&mut` — zmieniam, jestem
jedyny. Sama sygnatura mówi, czy wywołanie ma skutki uboczne.
:::

:::tip Analogia — biblioteka
Książkę może czytać wielu czytelników naraz — każdy ma swój egzemplarz
albo czyta w czytelni (`&`). Ale robić w niej notatki może tylko jedna
osoba, i tylko wtedy, gdy nikt inny jej nie czyta (`&mut`). Biblioteka
pozostaje właścicielem; czytelnicy pożyczają.
:::

Tyle wystarczy, żeby czytać. Lifetime'y — adnotacje `'a` i `'info`,
które mówią kompilatorowi, jak długo pożyczka jest ważna — pojawiają się
w programie Anchora w jednym miejscu: `Account<'info, T>`. W tym kursie
wystarczy przepisać `'info` tam, gdzie stoi w szablonie; co dokładnie
znaczy, jest poza zakresem.

Wszystkie wzorce są na stole. Ostatni rozdział składa je w jedną,
autentyczną instrukcję programu Anchora — dziesięć linii, w których jest
wszystko.
