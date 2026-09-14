---
title: Serializacja i IDL
description: Borsh jako format danych konta, dyskryminator jako odcisk typu i IDL jako opis interfejsu dla klientów.
sidebar_position: 4
slug: serializacja-i-idl
---

# Serializacja i IDL

Konto to bajty, program operuje na strukturach, a frontend musi wiedzieć,
co program przyjmuje. Trzy mechanizmy Anchora spinają te trzy światy.

## Serializacja

- Konto trzyma surowe bajty — program operuje na strukturach
- Konwersja tam i z powrotem to **serializacja**
- Anchor używa **Borsh** — kompaktowego formatu binarnego
- Adnotacja `#[account]` dokleja kod serializacji automatycznie

:::tip Efekt
Bez liczenia offsetów i ręcznego wczytywania bajtów — pola struktury
działają jak zwykły rekord.
:::

## Dyskryminator

- Konto trzyma bajty — skąd program wie, jak je odczytać?
- Pierwsze 8 bajtów konta = odcisk typu, czyli **dyskryminator**
- Anchor sprawdza go przed deserializacją — niezgodność = błąd
- Te 8 bajtów musi się zmieścić w zadeklarowanym `space`

:::note Analogia
Nagłówek `Content-Type` dla konta — mówi, jak interpretować zawartość,
zanim zacznie się ją czytać.
:::

## IDL

- Frontend musi wiedzieć, jakie instrukcje program przyjmuje
- Anchor generuje opis: JSON z instrukcjami, kontami i typami
- Ten opis to **Interface Description Language (IDL)**
- Klient (`@coral-xyz/anchor`) bierze IDL i daje gotowe wywołania
- Pełna integracja frontend ↔ program na sesji live

:::tip Analogia
Swagger / OpenAPI dla programu on-chain — jedno źródło prawdy dla
wszystkich klientów.
:::
