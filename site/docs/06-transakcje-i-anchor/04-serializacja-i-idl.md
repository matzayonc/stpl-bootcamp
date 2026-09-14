---
title: Serializacja i IDL
description: Borsh jako format danych konta, dyskryminator jako odcisk typu i IDL jako opis interfejsu dla klientów — pokazane na 49 bajtach prawdziwego konta licznika i wygenerowanym pliku JSON.
sidebar_position: 4
slug: serializacja-i-idl
---

# Serializacja i IDL

Konto to bajty, program operuje na strukturach, a frontend musi wiedzieć,
co program przyjmuje. Trzy mechanizmy Anchora spinają te trzy światy, i
wszystkie trzy da się zobaczyć w jednym koncie: liczniku z poprzedniego
rozdziału, zaraz po `init` z wartością 41 i jednym `increment`.

## Serializacja

Pole `data` konta to tablica bajtów bez struktury — dla runtime'u
`Counter` z trzema polami i losowy szum wyglądają tak samo. Program
musi te bajty **odczytać** do struktury na początku instrukcji i
**zapisać** z powrotem na końcu. Ta konwersja w obie strony to
**serializacja**, a format, którego używa Anchor, nazywa się **Borsh** —
*Binary Object Representation Serializer for Hashing*: pola po kolei, bez
nazw, bez wyrównania, liczby od najmniej znaczącego bajtu, listy i teksty
poprzedzone czterobajtową długością.

Listing 6-7 pokazuje strukturę stanu licznika i bajty, które z niej
powstały, odczytane z konta w teście.

```rust
#[account]
#[derive(InitSpace)]
pub struct Counter {
    pub authority: Pubkey,   // 32 bajty
    pub value:     u64,      //  8 bajtów
    pub bump:      u8,       //  1 bajt
}
```

```text
data (49 bytes):
ff b0 04 f5 bc fd 7c 19                             ← dyskryminator (8)
0f 16 87 06 c6 87 a0 42 dc 0d 1a 99 8e cd e5 bc     ← authority (32)
49 c6 e5 b8 13 4a a4 18 b2 af ee 0a 19 d9 4d b6
2a 00 00 00 00 00 00 00                             ← value = 42 (8, little-endian)
ff                                                  ← bump = 255 (1)
```

<div className="listing"><strong>Listing 6-7.</strong> Struktura i jej obraz w koncie. 8 + 32 + 8 + 1 = 49 bajtów; kolejność bajtów odpowiada kolejności pól, a <code>0x2a</code> to 42.</div>

Warto przejść po bajtach. Pierwsze osiem to dyskryminator, o którym za
chwilę. Kolejne 32 to `authority` — klucz publiczny zapisany binarnie,
bez base58. Potem `value`: `2a 00 00 00 00 00 00 00` to `u64` równe 42,
z najmniej znaczącym bajtem na początku, dokładnie tak jak kwota w
Listingu 6-1. Ostatni bajt to `bump` — 255, bo pierwszy sprawdzony bump
dał adres poza krzywą. Nie ma nazw pól, separatorów ani nagłówka: kto
zna definicję struktury, umie te bajty odczytać, kto nie zna — widzi 49
bajtów.

Adnotacja `#[account]` — trzeci blok Anchora — generuje ten kod
serializacji z definicji. Programista pisze `counter.value = …`, a
Anchor przed instrukcją deserializuje bajty do `Counter`, po instrukcji
serializuje `Counter` do bajtów i zapisuje w koncie (jeśli jest `mut`).
`#[derive(InitSpace)]` dopisuje stałą `Counter::INIT_SPACE` równą sumie
rozmiarów pól — 41 — której `init` używa w `space = 8 + Counter::INIT_SPACE`.

:::tip Efekt
Bez liczenia offsetów i ręcznego wczytywania bajtów — pola struktury
działają jak zwykły rekord. Zmiana kolejności pól w kodzie zmienia
układ bajtów w koncie, więc struktura `#[account]` po wdrożeniu jest jak
schemat bazy danych: rozszerzać można, przestawiać nie.
:::

## Dyskryminator

Skoro bajty nie mają nagłówka, to skąd program wie, że konto podane jako
`Account<'info, Counter>` faktycznie zawiera `Counter`, a nie inną
strukturę tego samego programu o przypadkiem podobnym rozmiarze? Z
pierwszych ośmiu bajtów. **Dyskryminator** to odcisk nazwy typu:
pierwsze 8 bajtów `sha256("account:Counter")`. Anchor zapisuje go przy
`init` i sprawdza przy każdym odczycie, zanim zdeserializuje resztę.
Niezgodność to błąd `AccountDiscriminatorMismatch`, a te 8 bajtów jest
powodem, dla którego każde `space` zaczyna się od `8 +`.

Listing 6-8 odtwarza wartość z Listingu 6-7 w trzech linijkach Pythona.

```python
import hashlib
for name in ("account:Counter", "global:init", "global:increment"):
    print(f"{name:18} {hashlib.sha256(name.encode()).digest()[:8].hex()}")
```

```text
account:Counter    ffb004f5bcfd7c19
global:init        dc3bcfec6cfa2f64
global:increment   0b12680968ae3b21
```

<div className="listing"><strong>Listing 6-8.</strong> Dyskryminatory policzone ręcznie. Pierwszy zgadza się z ośmioma bajtami z Listingu 6-7; dwa kolejne to dyskryminatory instrukcji.</div>

Instrukcje mają dyskryminatory tak samo, z prefiksem `global:`. To one
są pierwszymi ośmioma bajtami pola `data` instrukcji — odpowiednikiem
`02 00 00 00` z System Programu w Listingu 6-1. Wywołanie `init(41)`
wysyła 16 bajtów danych: `dc 3b cf ec 6c fa 2f 64` (dyskryminator) i
`29 00 00 00 00 00 00 00` (41 jako `u64`). Anchor czyta pierwsze osiem,
wybiera funkcję z modułu `#[program]`, a resztę deserializuje do jej
argumentów.

:::note Analogia — Content-Type
Nagłówek `Content-Type` mówi przeglądarce, jak interpretować bajty
odpowiedzi, zanim zacznie je czytać. Dyskryminator mówi programowi, jaka
struktura leży w koncie — i pozwala odrzucić konto, które twierdzi, że
jest czymś innym.
:::

## IDL

Frontend musi wiedzieć, jakie instrukcje program przyjmuje, jakie konta
każda z nich wymaga, jakie argumenty i w jakiej kolejności — inaczej nie
zbuduje poprawnego pola `data` ani listy kont. Anchor generuje ten opis
przy `anchor build` jako plik JSON: **Interface Description Language
(IDL)**. Listing 6-9 pokazuje fragment IDL programu licznika.

```json
{
  "address": "6hqBGkDSZTaF5cFshxX1pZPJkM3QAtEHFuWc2VxKdBmY",
  "metadata": { "name": "licznik", "version": "0.1.0", "spec": "0.1.0" },
  "instructions": [
    {
      "name": "increment",
      "discriminator": [11, 18, 104, 9, 104, 174, 59, 33],
      "accounts": [
        { "name": "counter", "writable": true,
          "pda": { "seeds": [ { "kind": "const", "value": [99, 111, 117, 110, 116, 101, 114] },
                              { "kind": "account", "path": "authority" } ] } },
        { "name": "authority", "signer": true, "relations": ["counter"] }
      ],
      "args": []
    },
    { "name": "init", "discriminator": [220, 59, 207, 236, 108, 250, 47, 100],
      "accounts": [ ... ], "args": [ { "name": "value", "type": "u64" } ] }
  ],
  "accounts": [ { "name": "Counter", "discriminator": [255, 176, 4, 245, 188, 253, 124, 25] } ],
  "errors": [ { "code": 6000, "name": "Overflow", "msg": "Licznik przekroczył zakres u64" } ],
  "types": [
    { "name": "Counter", "type": { "kind": "struct", "fields": [
        { "name": "authority", "type": "pubkey" },
        { "name": "value", "type": "u64" },
        { "name": "bump", "type": "u8" } ] } }
  ]
}
```

<div className="listing"><strong>Listing 6-9.</strong> <code>target/idl/licznik.json</code> (skrócony). Wszystko, co klient musi wiedzieć: instrukcje z kontami i argumentami, układ typów, kody błędów — i dyskryminatory z Listingu 6-8 zapisane dziesiętnie.</div>

Każda sekcja odpowiada jednemu z trzech bloków. `instructions` pochodzi
z `#[program]` i `#[derive(Accounts)]`: nazwy kont, ich flagi
(`writable`, `signer`), a nawet seedy PDA — `[99, 111, 117, 110, 116, 101,
114]` to `"counter"` w ASCII — dzięki czemu klient sam wylicza adres
licznika i nie musi go od nikogo dostać. `relations: ["counter"]` to
`has_one`. `types` pochodzi z `#[account]` i pozwala klientowi
zdeserializować konto po odczycie — Explorer używa dokładnie tego, żeby
pokazać pola z nazwami zamiast hex dumpu. `errors` to `#[error_code]`, z
którego klient tłumaczy `0x1770` na `Overflow`.

Biblioteka kliencka (`@anchor-lang/core` w wersji 1.0) bierze ten plik i
udostępnia gotowe wywołania: `program.methods.init(41).accounts({...})`
buduje instrukcję z właściwym dyskryminatorem, zserializowanym
argumentem i listą kont w kolejności z IDL. Frontend nie widzi bajtów.
Pełna integracja frontend ↔ program jest na sesji live.

:::tip Analogia — OpenAPI
IDL jest dla programu on-chain tym, czym Swagger dla API: jednym
źródłem prawdy, z którego generuje się klientów, dokumentację i
walidację. Różnica: IDL generuje się z kodu, więc nie może się od niego
rozjechać.
:::

Trzy bloki, trzy mechanizmy pod spodem. Ostatni rozdział składa wszystko
w jeden plik — program, który został skompilowany, przetestowany i
którego bajty zostały pokazane wyżej.
