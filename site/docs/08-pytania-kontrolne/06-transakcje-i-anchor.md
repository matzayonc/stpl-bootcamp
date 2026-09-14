---
title: Transakcje i Anchor
description: Pytania sprawdzające do tematu Transakcje i Anchor.
sidebar_position: 6
slug: transakcje-i-anchor
---

# Transakcje i Anchor — pytania kontrolne

Materiał do tych pytań: [Transakcje i Anchor](../06-transakcje-i-anchor/index.md). Jedna poprawna odpowiedź na pytanie.

## Pytania

1. Czym różni się **instrukcja** od **transakcji** na Solanie? Z jakich
   trzech elementów składa się instrukcja, a co poza listą instrukcji niesie
   sama transakcja?

   - **A.** Instrukcja = lista transakcji; transakcja = podpisy walidatorów + nonce
   - **B.** Instrukcja = (program, konta, dane); transakcja = lista instrukcji + podpisy + opłata
   - **C.** Instrukcja i transakcja to synonimy
   - **D.** Instrukcja = podpisy + opłata; transakcja = lista kont i bajtów

2. Co oznacza, że transakcja na Solanie jest **atomowa**? Co stanie się ze
   stanem łańcucha, jeśli druga instrukcja w transakcji zwróci błąd, a
   pierwsza zdążyła już zmienić jakieś konto? Czy opłata sieciowa zostanie
   pobrana?

   - **A.** Każda instrukcja niezależna; zmiana z instrukcji 1 zostaje; opłata nie pobrana
   - **B.** Wszystko albo nic; sieć cofa wszystkie zmiany; opłata pobrana mimo błędu
   - **C.** Wszystko albo nic; sieć cofa wszystkie zmiany; opłata zwrócona nadawcy
   - **D.** Tylko pierwsza instrukcja gwarantowana; kolejne pomijane bez opłaty

3. Wymień trzy makra-atrybuty, które tworzą szkielet każdego programu
   Anchora, i opisz w jednym zdaniu rolę każdego z nich.

   - **A.** `#[program]` = schemat bazy; `#[derive(Accounts)]` = klucze API; `#[account]` = endpointy HTTP
   - **B.** `#[program]` = instrukcje; `#[derive(Accounts)]` = walidacja kont; `#[account]` = układ danych
   - **C.** `#[program]` = moduł testowy; `#[derive(Accounts)]` = serializacja JSON; `#[account]` = zmienne env
   - **D.** `#[program]` = zastępnik `main()`; `#[derive(Accounts)]` = tworzy konta; `#[account]` = saldo SOL

## Pytania zapasowe

4. Czym jest **dyskryminator** w koncie Anchora? Ile bajtów zajmuje, jaką
   pełni funkcję podczas deserializacji i dlaczego trzeba go uwzględnić w
   atrybucie `space`?

   - **A.** Pole `owner` = 32 bajty; identyfikuje program-właściciela
   - **B.** Pierwsze 8 bajtów = odcisk typu; sprawdzany przed deserializacją; musi być w `space`
   - **C.** 4-bajtowy numer wersji; opcjonalny
   - **D.** Hash całego konta; przechowywany poza `data`; nie wlicza się w `space`

5. Co to jest **IDL** i do czego służy klientowi (np. frontendowi)? Z którym
   znanym z Web2 narzędziem porównujemy IDL w analogii i co konkretnie ich
   łączy?

   - **A.** Typ danych Rusta opisujący pola konta; tylko do kompilacji
   - **B.** Zestaw funkcji testowych; analogia: Jest / Mocha
   - **C.** JSON z instrukcjami, kontami, typami; klient czyta IDL i dostaje gotowe wywołania; analogia: Swagger / OpenAPI
   - **D.** Plik TOML z adresami programów; przełączanie devnet/mainnet; analogia: `.env`

<details>
<summary>Klucz odpowiedzi</summary>

1. B
2. B
3. B
4. B
5. C

</details>
