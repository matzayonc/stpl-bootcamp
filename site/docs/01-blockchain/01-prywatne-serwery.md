---
title: Problem z prywatnymi serwerami
description: Dane, pieniądze i historia na serwerze firmy — co widać, a czego nie da się sprawdzić.
sidebar_position: 1
slug: prywatne-serwery
---

# Problem z prywatnymi serwerami

Każda klasyczna aplikacja finansowa działa na infrastrukturze jednej firmy.
Wygoda jest oczywista; cena tej wygody — mniej.

## Prywatne serwery

- Dane, pieniądze, historia — na serwerze firmy
- Firma może **zmienić zasady** lub zablokować konto
- Kod produkcyjny może różnić się od audytowanego

:::tip Przykłady z życia
- PayPal zamraża konta twórców bez ostrzeżenia
- Giełda FTX wypłacała środki klientów — do czasu
- AWS outage wyłącza dziesiątki popularnych serwisów naraz
:::

## Problem zaufania

Interfejs pokazuje tylko to, co operator zdecyduje się pokazać. Poniżej dwie
listy: to, co użytkownik obserwuje, i to, czego z zewnątrz nie sposób
zweryfikować.

:::note Co widać
- Aplikacja działa
- Saldo się zgadza
- Historia transakcji jest dostępna
:::

:::warning Czego nie wiadomo
- Czy dane nie zostały zmienione
- Czy środki faktycznie tam są
- Co się stanie jutro
:::
