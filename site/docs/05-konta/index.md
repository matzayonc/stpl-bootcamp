---
title: Model kont
description: Na Solanie wszystko jest kontem — anatomia, typy, własność, adresy i koszt danych on-chain.
sidebar_position: 0
---

# Model kont

Jeden pomysł organizuje całą Solanę: **wszystko jest kontem**. Portfel,
token, program — każde z nich to komórka pamięci z adresem, saldem i
danymi. Odpowiada slajdom *Model Kont*
([PDF](https://github.com/matzayonc/stpl-slides/releases/download/latest/5_accounts.pdf)).

## W skrócie

1. Adres prowadzi do `{lamports, data, owner, executable}`
2. Kod i stan rozdzielone — program skaluje się na miliony kont
3. Tylko owner-program zmienia dane; użytkownik autoryzuje podpisem
4. Dane on-chain kosztują — konta muszą być rent-exempt

:::tip Analogia na koniec
Konto to plik; program to aplikacja z prawem zapisu do tego pliku.
:::

## Strony

1. [Anatomia konta](./01-anatomia-konta.md) — pięć pól, dwa typy, różnica wobec Ethereum
2. [Własność](./02-wlasnosc.md) — owner, signer i skąd bierze się adres
3. [Koszt](./03-koszt.md) — rent-exempt i rozmiar konta

Podgląd konta w Solana Explorerze jest w
[Portfel i narzędzia](../07-portfel-i-narzedzia/04-pierwsza-transakcja.md).
