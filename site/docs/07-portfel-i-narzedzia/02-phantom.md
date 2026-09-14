---
title: Phantom
description: Instalacja rozszerzenia Phantom i zasady obchodzenia się z seed phrase.
sidebar_position: 2
slug: phantom
---

# Phantom

Phantom to rozszerzenie przeglądarki, które trzyma klucze i podpisuje
transakcje. Cztery kroki instalacji i jedna zasada, której nie wolno złamać.

## Instalacja Phantom

- Zainstaluj rozszerzenie **Phantom** (Chrome, Brave lub Firefox)
- Kliknij *„Create New Wallet"* — portfel generuje parę kluczy lokalnie
- Zapisz **seed phrase** — szczegóły niżej
- Ustaw hasło lokalne — chroni tylko tę przeglądarkę, nie zastępuje seed

<div className="diagram screenshot">

![Phantom po założeniu portfela — widok salda](/img/phantom-balance.png)

</div>

## Seed phrase

- **Seed phrase** — 12 lub 24 słowa generowane przy zakładaniu portfela
- Z tych słów deterministycznie powstają **wszystkie** klucze prywatne
- Nigdy online — bez wklejania, bez screenshotów, bez chmury
- Zapis offline — kartka w sejfie lub lokalny manager haseł

<div className="diagram narrow">

![Seed phrase → deterministycznie → Konto 1, Konto 2, Konto 3](/img/diagrams/7_wallet-03.svg)

</div>

:::warning Kto ma seed, ma środki
Nie istnieje procedura „zapomniałem". Wycieka raz, na zawsze.
:::
