---
title: Składnia
description: Funkcja i struktura na jednym ekranie — typ po nazwie, strzałka do typu zwracanego, struct jako rekord pól — i pierwszy kontakt z kompilatorem.
sidebar_position: 2
slug: skladnia
---

# Składnia

Dla kogoś po TypeScripcie składnia Rusta wygląda znajomo: typ stoi po
nazwie i dwukropku, funkcja ma strzałkę do typu zwracanego, a struktura
to lista pól. Ten rozdział pokazuje dwie konstrukcje, z których składa się
większość programu Anchora, i uruchamia kompilator po raz pierwszy.

## Funkcja

Listing 4-1 to sygnatura instrukcji z programu skarbca — funkcja, która
przyjmuje kwotę i adres, a zwraca wynik.

```rust
fn deposit(amount: u64, owner: Pubkey) -> Result<()> {
    // ciało funkcji
}
```

<div className="listing"><strong>Listing 4-1.</strong> Sygnatura funkcji. Nazwa, argumenty z typami po dwukropku, strzałka i typ zwracany.</div>

Elementy od lewej: `fn` otwiera definicję funkcji; `deposit` to nazwa —
w Ruście zawsze `snake_case`, małe litery i podkreślenia, a kompilator
ostrzega przy odstępstwach. W nawiasie są argumenty, każdy jako
`nazwa: Typ`. `u64` to liczba całkowita bez znaku na 64 bitach — od zera
do około 18 trylionów; `u` znaczy *unsigned*, a liczba to szerokość w
bitach. `Pubkey` to typ z SDK Solany: 32-bajtowy adres konta z rozdziału
[Adres i PDA](../05-konta/03-adres-i-pda.md). Strzałka `->` wskazuje typ
zwracany; `Result<()>` znaczy „sukces bez wartości albo błąd", i dostaje
własną sekcję w [Wzorcach](./03-wzorce.md#result--bez-wyjątków).

Dwie rzeczy, których w tej sygnaturze nie ma, są równie ważne. Nie ma
`return` na końcu — ostatnie wyrażenie w ciele funkcji bez średnika jest
jej wartością. I nie ma sposobu, żeby wywołać `deposit` z argumentem
innego typu niż `u64`: przekazanie liczby ujemnej, ułamka albo tekstu
kończy się błędem kompilacji, nie błędem w runtime.

## Struktura

Listing 4-2 to definicja danych, które ten sam program przechowuje w
koncie.

```rust
struct Vault {
    owner:   Pubkey,
    balance: u64,
}
```

<div className="listing"><strong>Listing 4-2.</strong> Struktura — rekord nazwanych pól z typami. Nie ma metod, konstruktora ani dziedziczenia; to tylko układ danych.</div>

`struct` to odpowiednik interfejsu z TypeScriptu albo klasy bez metod:
lista pól, każde `nazwa: Typ`, oddzielone przecinkami. Nazwy struktur są
w `PascalCase`. Rust nie ma klas — metody dodaje się osobno, w bloku
`impl`, o którym mówi następny rozdział. Ta separacja jest celowa:
struktura opisuje, *jak dane wyglądają w pamięci*, i dokładnie tym samym
opisem Anchor posłuży się, żeby zapisać `Vault` jako bajty w koncie
(rozdział [Serializacja i IDL](../06-transakcje-i-anchor/04-serializacja-i-idl.md)).

Rozmiar struktury da się policzyć z definicji: `Pubkey` ma 32 bajty,
`u64` ma 8, więc `Vault` zajmuje 40 bajtów. To nie jest ciekawostka —
rozdział [Koszt](../05-konta/04-koszt.md) pokazuje, że za każdy z tych
bajtów płaci się depozyt.

## Pierwsze uruchomienie

Kompilator Rusta, `rustc`, jest najczęściej spotykanym narzędziem w tym
temacie — nie dlatego, że trzeba go wywoływać ręcznie (robi to `cargo`, a
w Anchorze `anchor build`), ale dlatego, że jego komunikaty są głównym
źródłem nauki. Listing 4-3 pokazuje najkrótszy program, który da się
skompilować i uruchomić.

```rust
struct Vault {
    owner:   u8,   // uproszczenie: poza Anchorem nie ma typu Pubkey
    balance: u64,
}

fn main() {
    let vault = Vault { owner: 7, balance: 1_000 };
    println!("właściciel {} ma {} lamportów", vault.owner, vault.balance);
}
```

```bash
$ rustc main.rs && ./main
właściciel 7 ma 1000 lamportów
```

<div className="listing"><strong>Listing 4-3.</strong> Struktura, jej utworzenie i odczyt pól. <code>let</code> wiąże wartość z nazwą; podkreślenie w <code>1_000</code> to separator tysięcy, ignorowany przez kompilator.</div>

Trzy drobiazgi z tego listingu wracają wszędzie. `let nazwa = wartość;`
tworzy zmienną — typ nie jest podany, bo kompilator wnioskuje go z
prawej strony. `Vault { owner: 7, balance: 1_000 }` tworzy strukturę,
podając wszystkie pola po nazwie; pominięcie któregoś to błąd kompilacji.
`println!` z wykrzyknikiem to makro, a `{}` w tekście to miejsca, w
które wstawiane są kolejne argumenty — o makrach mówi ostatnia sekcja
[Wzorców](./03-wzorce.md#makra).

:::note Typ po nazwie
`nazwa: Typ` w argumentach i polach, `-> Typ` dla wartości zwracanej,
brak typu przy `let`, gdy kompilator może go wywnioskować. Ta jedna
zasada obejmuje większość tego, co w składni Rusta różni się od
JavaScriptu.
:::

Składnia jest znajoma; to, co niepokoi w Ruście, to nie jak wyglądają
konstrukcje, tylko czego kompilator odmawia. Następny rozdział przechodzi
przez siedem takich odmów — i pokazuje, jaki błąd każda z nich
uniemożliwia.
