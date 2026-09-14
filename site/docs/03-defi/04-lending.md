---
title: Lending
description: Pożyczki bez banku — pula, zastaw, nadzabezpieczenie i automatyczna likwidacja.
sidebar_position: 4
slug: lending
---

# Lending

Bank ocenia zdolność, prowadzi rejestr i ściąga dług. Program on-chain nie
zna tożsamości pożyczkobiorcy, więc całą mechanikę musi zamknąć w puli tokenów
i regułach.

## Drugi filar

- Wymiana tokenów działa bez giełdy i bez animatora rynku
- Drugi filar obietnicy — **pożyczki bez banku**
- Bank ocenia zdolność, prowadzi rejestr, ściąga dług — co go zastąpi w kodzie?
- Cała mechanika musi się zamknąć w smart kontrakcie i puli tokenów

:::warning Bez oceny kredytowej
Łańcuch nie wie, kim jest pożyczkobiorca. Skoro nie ma scoringu — co broni
protokół przed niespłaconym długiem?
:::

## Jak to działa

<div className="diagram">

![Lender wpłaca USDC do puli i dostaje odsetki; Borrower blokuje SOL jako zastaw i pożycza USDC](/img/diagrams/3_lending-01.svg)

</div>

- **Lender** wpłaca tokeny do puli i zarabia odsetki
- **Borrower** blokuje SOL jako zastaw i pożycza USDC — bez sprzedaży SOL
- Protokół zarządza pulą i egzekwuje reguły przez program on-chain
- Na Solanie: **Kamino Finance**, **Solend**, **MarginFi**

:::tip Przykład
Posiadacz SOL potrzebuje USDC na bieżące wydatki. Zastawia SOL, pożycza
USDC — SOL zostaje jego i dalej rośnie (lub spada).
:::

## Dlaczego więcej, niż się pożycza?

- Blockchain nie zna tożsamości pożyczkobiorcy — brak scoringu kredytowego
- Protokół nie może ściągnąć długu sądownie — jedyną gwarancją jest zastaw
- Wartość zastawu musi *przekraczać* wartość pożyczki
- Im niestabilniejszy token, tym wyższe wymagane nadzabezpieczenie

:::note Nadzabezpieczenie (overcollateralization)
Zastaw jest celowo wyższy niż pożyczka — nadwyżka to bufor bezpieczeństwa
protokołu na wypadek spadku cen.
:::

## Likwidacja

- Gdy wartość zastawu spada zbyt nisko — protokół uruchamia **likwidację**
- **Likwidator** spłaca dług i przejmuje zastaw z dyskontem
- Mechanizm zamyka dług automatycznie, bez zgody pożyczkobiorcy
- Dyskont zachęca likwidatorów do działania szybko

:::tip Przykład
Zastaw: SOL warte 100 USD, pożyczka: 70 USDC.

SOL spada o 25% ⇒ zastaw = 75 USD, dług = 70 USDC.

Protokół uruchamia likwidację — likwidator spłaca dług i przejmuje SOL.
:::
