---
title: Pierwsza transakcja
description: Transfer SOL na devnecie i jego ślad w Solana Explorerze — podpis, slot, opłata, zmienione konta.
sidebar_position: 4
slug: pierwsza-transakcja
---

# Pierwsza transakcja

Dowolny transfer między dwoma adresami devnet to ten sam **write**, który
opisuje [Read vs Write](../02-web3/03-read-vs-write.md) — podpisany,
opłacony, atomowy. Explorer pozwala go obejrzeć bez własnego węzła.

## Pierwsza transakcja

- Wykonaj dowolny transfer SOL między dwoma adresami devnet
- Otwórz `explorer.solana.com` i przełącz sieć na **Devnet**
- Znajdź transakcję po podpisie skopiowanym z Phantom
- To dokładnie ten **write** — podpisany, opłacony, atomowy

<div className="diagram narrow">

![Portfel → Walidatory → Explorer](/img/diagrams/7_wallet-04.svg)

</div>

:::tip Co widać w Explorerze
Podpis (identyfikator), status i numer slotu, opłatę sieciową oraz listę
kont, które zmieniły stan.
:::

## Transakcja w Explorerze

<div className="diagram screenshot">

![Szczegóły transakcji w explorer.solana.com na sieci Devnet](/img/explorer-tx-devnet-crop.png)

</div>

explorer.solana.com · sieć: Devnet

## Explorer jako podgląd konta

RPC to okno na łańcuch — Explorer jest jego ładną wersją. Każde pole konta z
[Anatomii konta](../05-konta/01-anatomia-konta.md) widać na żywo.

- Każde pole konta widoczne na żywo, bez własnego węzła
- `adres` — gdzie konto żyje
- `owner` — który program nim rządzi
- `lamports` oraz `data` / `executable` — saldo, treść, kod vs dane

:::tip Demo — Solana Explorer
Otwórz realne konto i odczytaj jego pola wprost z łańcucha.
:::
