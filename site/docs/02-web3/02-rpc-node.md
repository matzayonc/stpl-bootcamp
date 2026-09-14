---
title: RPC node
description: Węzeł, przez który frontend czyta stan łańcucha i wysyła transakcje do klastra.
sidebar_position: 2
slug: rpc-node
---

# RPC node

Frontend nie rozmawia z walidatorami bezpośrednio. Potrzebuje pośrednika,
który wystawia zwykłe API — takich pośredników są setki i wszystkie mówią
tym samym językiem.

- Frontend potrzebuje **okna na łańcuch**
- Setki publicznych węzłów, to samo API
- Analogia — **bankomat dowolnej sieci**
- **Remote Procedure Call (RPC)**

<div className="diagram narrow">

![Frontend → Helius / QuickNode / własny → Klaster](/img/diagrams/1_paradigm-03.svg)

</div>

:::note Definicja
**RPC node** — węzeł sieci, który przyjmuje zapytania klienta i zwraca
aktualny stan lub przekazuje transakcję do klastra.
:::
