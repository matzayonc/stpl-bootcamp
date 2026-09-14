---
title: Materiały
description: Mapa tematów Solana Bootcamp Superteam Poland — od blockchaina, przez DeFi, Rust i model kont, po Anchor i pierwszy portfel.
sidebar_position: 0
slug: /
---

# Materiały

Strona towarzyszy nagranym lekcjom bootcampu *Od Zera do Blockchain
Developera* i jest ich **podręcznikiem**: każdy temat to rozdział pisany
jak książka — pełnym tekstem, z numerowanymi listingami, wynikami
prawdziwych narzędzi, podsumowaniem i ćwiczeniami. Slajdy wyznaczają
kolejność i słownik; rozdziały idą głębiej, niż pozwala wykład. Slajdy w
formacie PDF są w
[najnowszym wydaniu](https://github.com/matzayonc/stpl-slides/releases/latest).

## Mapa tematów

| Temat | O czym | Slajdy |
|---|---|---|
| [Blockchain i Solana](./01-blockchain/index.md) | prywatne serwery, BFT, programy on-chain, dlaczego Solana — z liczbami zmierzonymi na sieci | Lekcja 0 |
| [Paradygmat Web3](./02-web3/index.md) | Web2 vs Web3, RPC, read vs write, portfel jako tożsamość, mapa stacku — na prawdziwych zapytaniach | Lekcja 1 |
| [DeFi](./03-defi/index.md) | token, AMM i jego matematyka, lending, likwidacja, composability — z wyceną z agregatora | Lekcje 2–3 |
| [Rust dla Anchora](./04-rust/index.md) | składnia, siedem wzorców z komunikatami kompilatora, pożyczanie, jedna instrukcja linia po linii | Lekcja 4 |
| [Model kont](./05-konta/index.md) | anatomia konta, owner i signer, PDA, rent i rozmiar — na kontach z mainnetu | Lekcja 5 |
| [Transakcje i Anchor](./06-transakcje-i-anchor/index.md) | instrukcja i transakcja, trzy makra Anchora, Borsh, IDL — na skompilowanym liczniku | Lekcja 6 |
| [Portfel i narzędzia](./07-portfel-i-narzedzia/index.md) | klucze, Phantom, devnet, CLI, airdrop, pierwsza transakcja w terminalu i Explorerze | Lekcja 7 |
| [Pytania kontrolne](./08-pytania-kontrolne/00-blockchain-i-solana.md) | pytania sprawdzające do każdego tematu | — |

## Jak czytać te materiały

Kolejność tematów odpowiada kolejności lekcji; DeFi łączy dwie. Każdy
rozdział zaczyna się stroną z zawartością, podsumowaniem i ćwiczeniami —
podsumowanie można przeczytać najpierw, żeby wiedzieć, dokąd rozdział
zmierza. Pojęcia pojawiają się w kolejności: problem, mechanizm,
**nazwa** ze skrótem w nawiasie przy pierwszym użyciu.

Kod i wyniki poleceń są numerowane w obrębie rozdziału (*Listing 5-3*
to trzeci listing w temacie piątym) i pochodzą z prawdziwych narzędzi:
`solana`, `anchor`, `spl-token`, `rustc`, `curl` do publicznego węzła RPC.
Odczyty są z sieci głównej, zapisy — wyłącznie z sieci testowej. Liczby,
które zmieniają się w czasie (stawka depozytu, liczba walidatorów, czas
slotu), były aktualne w chwili pisania; ćwiczenia proszą o ich ponowne
zmierzenie.

Trzy rodzaje bloków pełnią tę samą rolę co na slajdach:

:::note Definicja
Blok neutralny — definicja pojęcia lub kluczowa reguła.
:::

:::warning Ryzyko
Blok ostrzegawczy — problem, pułapka, cena decyzji.
:::

:::tip Przykład
Blok przykładowy — analogia, konkretne liczby, efekt mechanizmu.
Analogie w rozdziale łączą się w łańcuch, który jego podsumowanie
zbiera w jednym bloku.
:::
