---
title: Czym jest Anchor
description: Ręczna walidacja w surowej Solanie, framework jako odpowiedź, trzy makra, z których składa się każdy program — i szkielet projektu, który generuje anchor init.
sidebar_position: 2
slug: czym-jest-anchor
---

# Czym jest Anchor

Poprzedni rozdział skończył się obserwacją: runtime sprawdza podpisy i
cofa nieudane transakcje, ale to program musi sprawdzić, czy każde konto
z listy jest tym, za które się podaje. Ten rozdział pokazuje, ile tego
sprawdzania jest — i czym jest framework, który robi je z deklaracji.

## Surowa Solana

Program bez frameworku dostaje od runtime'u trzy rzeczy z Listingu 6-1:
adres programu, listę kont jako surowe struktury z polami `lamports`,
`data`, `owner`, `is_signer`, `is_writable`, i dane instrukcji jako
tablicę bajtów. Wszystko, co opisuje [Model kont](../05-konta/index.md),
trzeba sprawdzić samemu, ręcznie, przy każdej instrukcji:

- czy `owner` każdego konta danych to ten program — inaczej ktoś podał
  konto założone przez inny program, o dowolnej zawartości;
- czy konto, które ma podpisać, ma `is_signer` — inaczej każdy może
  wykonać operację w cudzym imieniu;
- czy konto, które ma być zapisane, ma `is_writable` — inaczej zapis
  skończy się błędem runtime'u po wykonaniu całej logiki;
- czy `data` ma właściwą długość i właściwy typ — inaczej odczyt struktury
  z bajtów da śmieci;
- czy adres konta zgadza się z tym, który wynika z seedów — inaczej ktoś
  podstawił własne konto o poprawnym układzie.

Do tego dochodzi zamiana bajtów na strukturę i z powrotem — ręczne
liczenie offsetów, kolejności pól i rozmiarów. W programie z dziesięcioma
instrukcjami i pięcioma typami kont to kilkaset linii sprawdzeń, z
których każda jest nudna, a każda pominięta jest luką. Rozdział
[Własność](../05-konta/02-wlasnosc.md) nazwał to wprost: większość
historycznych exploitów to brakujący owner check albo signer check.

:::warning Ryzyko
Jeden zapomniany `if` to otwarte drzwi do środków. Nie dlatego, że kod
jest skomplikowany, ale dlatego, że sprawdzeń jest dużo, są do siebie
podobne i żadne z nich nie jest potrzebne, żeby program *działał* na
poprawnych danych. Brak sprawdzenia widać dopiero wtedy, gdy ktoś poda
niepoprawne.
:::

## Framework

**Anchor** to framework do pisania programów Solany, który przenosi te
sprawdzenia z ciała instrukcji do **deklaracji**. Programista opisuje
typem, czym konto ma być — `Account<'info, Vault>`, `Signer<'info>` — i
atrybutem, jakie warunki ma spełniać — `mut`, `has_one`, `seeds` — a
framework generuje kod, który sprawdza to wszystko, zanim ciało
instrukcji zobaczy jakiekolwiek dane. Serializację struktur generuje z
ich definicji. Do tego produkuje opis interfejsu, z którego frontend
buduje wywołania, i zamienia numery błędów na czytelne komunikaty — jak
w Listingu 6-2, gdzie `ConstraintSeeds` z `Left`/`Right` to tekst
Anchora, nie runtime'u.

Anchor jest standardem de facto: większość programów w ekosystemie jest
w nim napisana, a narzędzia — Explorer, biblioteki klienckie, testy —
rozumieją jego konwencje. Program w surowej Solanie nadal da się
napisać i bywa to uzasadnione (mniejszy rozmiar, mniej jednostek
obliczeniowych), ale to wybór dla zespołów, które wiedzą, z czego
rezygnują.

:::tip Analogia — Rails dla Solany
Framework webowy nie zmienia tego, co robi HTTP; zmienia to, ile
razy programista pisze parsowanie nagłówków. Anchor nie zmienia tego, co
robi runtime; zmienia to, ile razy programista pisze `if account.owner
!= program_id`. Konwencje zamiast powtarzania.
:::

## Trzy bloki

Każdy program Anchora składa się z trzech makr-atrybutów, i cała reszta
tego tematu to ich omówienie.

| Makro | Nad czym stoi | Co opisuje | Rozdział |
|---|---|---|---|
| `#[program]` | moduł z funkcjami | **co program robi** — instrukcje | [Program i Accounts](./03-program-i-accounts.md) |
| `#[derive(Accounts)]` | struktura pól-kont | **na czym** — konta instrukcji i ich walidacja | [Program i Accounts](./03-program-i-accounts.md) |
| `#[account]` | struktura pól danych | **jak wygląda stan** — układ danych w koncie | [Serializacja i IDL](./04-serializacja-i-idl.md) |

:::note Trzy role
**Co robi** (instrukcje) · **na czym** (konta + walidacja) · **jak wygląda
stan** (pola konta). Każdy program Anchora, niezależnie od rozmiaru, jest
zbudowany z tych trzech elementów; duże programy mają ich po prostu
więcej.
:::

## Szkielet projektu

Anchor to też narzędzie wiersza poleceń. Listing 6-3 pokazuje, co
generuje `anchor init` w wersji 1.0 — wersji używanej w tym kursie.

```bash
$ anchor init licznik
...
licznik initialized

$ find licznik -type f -not -path '*/node_modules/*' | sort
licznik/Anchor.toml
licznik/Cargo.toml
licznik/migrations/deploy.ts
licznik/package.json
licznik/programs/licznik/Cargo.toml
licznik/programs/licznik/src/constants.rs
licznik/programs/licznik/src/error.rs
licznik/programs/licznik/src/instructions.rs
licznik/programs/licznik/src/instructions/initialize.rs
licznik/programs/licznik/src/lib.rs
licznik/programs/licznik/src/state.rs
licznik/programs/licznik/tests/test_initialize.rs
licznik/rust-toolchain.toml
licznik/target/deploy/licznik-keypair.json
licznik/tsconfig.json
```

<div className="listing"><strong>Listing 6-3.</strong> Projekt wygenerowany przez <code>anchor init</code> (lista skrócona o pliki konfiguracyjne edytora). Program leży w <code>programs/licznik/src/</code>, testy obok w <code>tests/</code>.</div>

Kilka plików warto znać z nazwy. `Anchor.toml` to konfiguracja projektu:
adres programu, sieć docelowa, ścieżka do portfela. `programs/licznik/`
to jeden program — projekt może mieć ich kilka. `src/lib.rs` to punkt
wejścia; szablon dzieli program na `state.rs` (struktury `#[account]`),
`instructions/` (po jednej strukturze `#[derive(Accounts)]` i jednej
funkcji na plik) i `error.rs` (`#[error_code]`). Ten podział jest
konwencją, nie wymogiem — rozdział [Mini-program](./05-mini-program.md)
pokazuje ten sam program w jednym pliku, bo tak czyta się go łatwiej.
`target/deploy/licznik-keypair.json` to klucz, z którego wynika adres
programu; `tests/` zawiera test w Ruście, który uruchamia program w
lokalnej maszynie wirtualnej bez sieci.

Trzy polecenia obsługują cały cykl: `anchor build` kompiluje program do
pliku `.so` i generuje opis interfejsu, `anchor test` uruchamia testy,
`anchor deploy` wgrywa program do sieci z `Anchor.toml`. Sesja live
przechodzi przez wszystkie trzy; tutaj wystarczy wiedzieć, że istnieją.

Następny rozdział otwiera dwa pierwsze bloki — moduł z instrukcjami i
strukturę kont — na kodzie, który został skompilowany i przetestowany.
