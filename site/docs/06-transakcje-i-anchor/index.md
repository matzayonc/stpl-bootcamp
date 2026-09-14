---
title: Transakcje i Anchor
description: Jak wygląda zapis stanu na Solanie — instrukcja, koperta, atomowość — i jak Anchor zdejmuje z programisty walidację, serializację i IDL, pokazane na skompilowanym i przetestowanym programie licznika.
sidebar_position: 0
---

# Transakcje i Anchor

Jedno zdanie organizuje ten temat: **program sam musi sprawdzić, czy
konta, które dostał, są tym, za co się podają — a Anchor robi to z
deklaracji**. Runtime weryfikuje podpisy i cofa nieudane transakcje, ale
nie wie, czym jest licznik ani kto ma prawo go zwiększyć. Ta wiedza jest w
typach i atrybutach struktury kont, i z niej framework generuje
sprawdzenia, serializację i opis interfejsu. Kto rozumie trzy makra
Anchora, czyta każdy program w ekosystemie.

Rozdział rozwija slajdy *Anatomia Anchora*
([PDF](https://github.com/matzayonc/stpl-slides/releases/download/latest/6_anchor.pdf))
o rzeczy, na które na wykładzie nie ma czasu: rozkodowane bajty
prawdziwej instrukcji, log constraintu, który nie przeszedł, 49 bajtów
konta licznika z podpisanymi polami, dyskryminatory policzone ręcznie,
wygenerowany plik IDL i wynik testów w LiteSVM. Program, z którego to
wszystko pochodzi, jest w całości na ostatniej stronie.

## Zawartość

1. [Transakcja](./01-transakcja.md) — **instrukcja** jako trójka
   (program, konta, dane) z rozkodowanym przelewem, **transakcja** jako
   koperta z podpisami, blockhashem i opłatą, **atomowość** i prawdziwe
   cofnięcie.
2. [Czym jest Anchor](./02-czym-jest-anchor.md) — lista sprawdzeń w
   surowej Solanie, framework jako deklaracja zamiast `if`, trzy bloki,
   szkielet z `anchor init`.
3. [Program i Accounts](./03-program-i-accounts.md) — `#[program]` i
   `Context<T>`, `#[derive(Accounts)]` z typami `Account`, `Signer`,
   `Program`, pięć constraints w tabeli i log `ConstraintSeeds`.
4. [Serializacja i IDL](./04-serializacja-i-idl.md) — **Borsh** na
   bajtach konta, **dyskryminator** jako `sha256` nazwy, **IDL** jako
   JSON dla klienta.
5. [Mini-program](./05-mini-program.md) — cały `lib.rs` licznika w 60
   liniach, omówienie od góry do dołu, trzy testy i ich wynik.

Pytania sprawdzające do rozdziału: [Transakcje i Anchor — pytania
kontrolne](../08-pytania-kontrolne/06-transakcje-i-anchor.md).

## Podsumowanie

**Instrukcja** to trójka: program, lista kont z flagami zapisu i
podpisu, bajty danych. Program nie sięgnie po konto spoza listy.
**Transakcja** to koperta z jedną lub kilkoma instrukcjami, podpisami
każdego signera, ostatnim blockhashem i opłatą 5 000 lamportów za podpis
— jedyna forma zapisu stanu. Wykonuje się **atomowo**: błąd w dowolnej
instrukcji cofa wszystkie, a zostaje tylko opłata i wpis w historii.

Bez frameworku program sprawdza ręcznie właściciela, podpis, flagę
zapisu, długość danych i adres każdego konta, i ręcznie liczy offsety
przy serializacji — kilkaset podobnych linii, z których każda pominięta
jest luką. **Anchor** przenosi to do deklaracji: typ pola mówi, czym
konto jest, atrybut `#[account(...)]` mówi, jakie warunki spełnia, a
framework generuje sprawdzenia, które wykonują się przed ciałem
instrukcji.

Trzy makra to cały program. **`#[program]`** grupuje instrukcje — funkcje
z `Context<T>` jako pierwszym argumentem i `Result<()>` jako wynikiem.
**`#[derive(Accounts)]`** opisuje konta jednej instrukcji:
`Account<'info, T>` sprawdza właściciela i dyskryminator, `Signer`
podpis, `Program` adres; constraints `init`, `mut`, `has_one`, `seeds`,
`bump` dokładają tworzenie, zapis, powiązanie i PDA, i sprawdzają się w
kolejności wypisania. **`#[account]`** opisuje układ danych i generuje
serializację.

Pod spodem konto to **Borsh**: pola po kolei, bez nazw, liczby od
najmniej znaczącego bajtu — `Counter` to 8 + 32 + 8 + 1 = 49 bajtów.
Pierwsze osiem to **dyskryminator**, `sha256("account:Counter")[..8]`,
sprawdzany przed każdą deserializacją; instrukcje mają własne z prefiksem
`global:`. Z tych samych definicji `anchor build` generuje **IDL** — JSON
z instrukcjami, kontami, seedami PDA, typami i błędami — z którego klient
buduje wywołania bez oglądania bajtów.

:::tip Analogia na koniec
Transakcja to koperta, która dojdzie w całości albo wróci nieotwarta;
Anchor to Rails dla Solany — konwencje zamiast powtarzania `if`;
dyskryminator to `Content-Type` konta; a IDL to OpenAPI programu, tyle
że wygenerowane z kodu, więc nie może się od niego rozjechać.
:::

## Ćwiczenia

Ćwiczenia 1–2 wymagają `curl` lub przeglądarki; 3–4 wymagają
zainstalowanego Anchora 1.0 (`anchor --version`) i skopiowania Listingu
6-10 do projektu z `anchor init`.

1. **Rozkoduj instrukcję.** Pobierz przez `getTransaction` dowolny
   przelew SOL z Explorera i rozkoduj pole `data` jego instrukcji z
   base58 na bajty (dowolnym narzędziem online lub trzema liniami
   Pythona). Wskaż cztery bajty numeru operacji i osiem bajtów kwoty;
   przelicz kwotę z little-endian i porównaj z różnicą `preBalances` i
   `postBalances`.

2. **Dyskryminatory z IDL.** W Listingu 6-9 dyskryminatory są zapisane
   jako liczby dziesiętne. Przelicz `[255, 176, 4, 245, 188, 253, 124,
   25]` na hex i porównaj z Listingiem 6-8. Następnie policz
   dyskryminator dla hipotetycznej struktury `account:Vault` i instrukcji
   `global:withdraw`.

3. **Który constraint pierwszy?** Do programu z Listingu 6-10 dopisz
   test, w którym właściciel licznika wywołuje `increment`, ale jako
   `counter` podaje adres PDA wyliczony z seedów *innego* użytkownika.
   Przed uruchomieniem zapisz, który constraint z `Increment` zawiedzie i
   z jakim `Error Number`. Uruchom i sprawdź. Następnie usuń `seeds` i
   `bump` z `Increment`, zbuduj ponownie i powtórz test — co zmienia się
   w logu?

4. **Trzecie pole.** Dodaj do `Counter` pole `created_at: i64` i ustaw
   je w `init` z `Clock::get()?.unix_timestamp`. Zapisz, jak zmieni się
   `INIT_SPACE`, o ile bajtów urośnie konto i ile wyniesie nowy depozyt
   według `solana rent`. Zbuduj, uruchom testy i sprawdź w wypisanych
   bajtach, gdzie leży nowe pole i w jakiej kolejności bajtów.
