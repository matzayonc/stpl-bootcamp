---
title: Read vs Write
description: Odczyt jest darmowy i natychmiastowy; zapis wymaga podpisu, opłaty i potwierdzenia klastra.
sidebar_position: 3
slug: read-vs-write
---

# Read vs Write

Każda operacja klienta należy do jednej z dwóch kategorii. Rozróżnienie jest
proste, ale wpływa na całą architekturę aplikacji.

## Read vs Write

:::note Read
<div className="diagram small">

![Klient ↔ RPC](/img/diagrams/1_paradigm-04.svg)

</div>

- Gratis, bez podpisu
- Dowolny węzeł RPC
- Odpowiedź natychmiast
- Np. podgląd salda konta
:::

:::warning Write
<div className="diagram small">

![Klient → RPC → Klaster → ack](/img/diagrams/1_paradigm-05.svg)

</div>

- **Transakcja** podpisana kluczem
- Opłata sieciowa za włączenie
- Czeka na potwierdzenie klastra
- Np. wysłanie tokena
:::

## Bezserwerowa architektura

Skoro logika jest programem w klastrze, deweloper nie utrzymuje żadnego
backendu — ten sam kod uruchamia każdy walidator.

- Kod nie żyje na **własnym** serwerze
- Brak uptime'u, deploymentu, VPS
- Stan **publiczny on-chain**
- Dev pisze logikę, nie infrastrukturę

<div className="diagram narrow">

![Sześć walidatorów, każdy z tą samą kopią programu](/img/diagrams/1_paradigm-06.svg)

</div>

:::warning Druga strona medalu
Kod publiczny i niezmienny — błąd też publiczny i trudny do cofnięcia.
:::
