---
title: Klucze
description: Portfel jako tożsamość, klucz publiczny jako adres, klucz prywatny jako podpis — i dlaczego nie ma hasła.
sidebar_position: 1
slug: klucze
---

# Klucze

Ten sam portfel podpisze każdą transakcję do końca kursu. Zanim powstanie,
warto wiedzieć, co dokładnie w nim leży.

## Portfel — login

- Portfel to **tożsamość** użytkownika w sieci
- Ten sam portfel podpisze każdą transakcję do końca kursu
- Czemu nie ma hasła?

## Para kluczy

- **Klucz publiczny** pełni rolę adresu — można go swobodnie udostępniać
- **Klucz prywatny** autoryzuje transakcje — nigdy nie opuszcza portfela

<div className="diagram">

![Portfel z kluczem prywatnym → klucz publiczny (adres); z publicznego nie da się policzyć prywatnego](/img/diagrams/7_wallet-01.svg)

</div>

## Podpis

- Klucz prywatny podpisuje transakcję — każdy węzeł weryfikuje podpis kluczem publicznym
- Zmiana jednego bajtu unieważnia podpis — treści i autora nie można sfałszować

<div className="diagram">

![Klucz prywatny → podpisuje → Podpis → transakcja → Węzeł sieci; klucz publiczny → weryfikacja](/img/diagrams/7_wallet-02.svg)

</div>
