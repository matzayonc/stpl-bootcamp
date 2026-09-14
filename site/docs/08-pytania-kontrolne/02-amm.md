---
title: AMM
description: Pytania sprawdzające do tematu AMM.
sidebar_position: 2
slug: amm
---

# AMM — pytania kontrolne

Materiał do tych pytań: [AMM](../03-defi/02-amm.md). Jedna poprawna odpowiedź na pytanie.

## Pytania

1. Czym różni się **order book** (np. Binance) od **AMM** (np. Orca) jeśli
   chodzi o sposób ustalania ceny i kto dostarcza płynność?

   - **A.** Order book: cena z formuły; AMM: cena z dopasowania zleceń
   - **B.** Order book: cena z dopasowania zleceń, płynność od animatorów; AMM: cena z formuły, płynność od każdego LP
   - **C.** Oba używają formuły; order book wymaga animatorów, AMM nie dopuszcza prywatnych LP
   - **D.** Order book: swap zawsze możliwy 24/7; AMM: wymaga pasującego zlecenia

2. Co to jest **Impermanent Loss** i kiedy go doświadcza dostawca płynności
   (LP)? Dlaczego w nazwie jest słowo „impermanent" i kiedy ta strata
   znika?

   - **A.** Opłata pobierana przy każdym swapie; wypłacana z opóźnieniem
   - **B.** Strata wartości pozycji LP vs. HODL przy zmianie cen; znika gdy cena wraca do poziomu wejścia
   - **C.** Trwała utrata tokenów przez exploit; protokół może zwrócić po audycie
   - **D.** Różnica bid/ask w jednym bloku; znika po zamknięciu pozycji

3. Co oznacza skrót **CLMM** i czym taki model różni się od klasycznego AMM
   constant product? Wymień jedną zaletę i jedno ryzyko, które wprowadza
   wybór wąskiego przedziału cenowego.

   - **A.** Centralized Liquidity MM; brak IL, ryzyko cenzury
   - **B.** Concentrated Liquidity MM; LP wybiera przedział cenowy; zaleta: wyższe opłaty; ryzyko: wyższy IL poza zakresem
   - **C.** Constant Liquidity MM; taki sam jak constant product, $k$ aktualizowane co epokę
   - **D.** Concentrated Liquidity MM; zaleta: eliminacja IL; ryzyko: niższa efektywność kapitału

<details>
<summary>Klucz odpowiedzi</summary>

1. B
2. B
3. B

</details>
