---
title: AMM
description: Automated Market Maker — cena z proporcji rezerw zamiast z dopasowania zleceń, płynność od każdego, wymiana 24/7 — z prawdziwą wyceną z agregatora i listą ryzyk.
sidebar_position: 2
slug: amm
---

# AMM — Automated Market Maker

Klasyczna giełda ustala cenę, dopasowując zlecenia: ktoś chce sprzedać
po 100, ktoś chce kupić po 100, giełda ich łączy. Do tego potrzebny jest
ktoś, kto zlecenia zbiera, i ktoś, kto zawsze stoi po drugiej stronie —
animator rynku. Program on-chain nie ma jak zatrudnić animatora. Ten
rozdział pokazuje mechanizm, który ustala cenę **bez zleceń** i który
da się zapisać w kilku linijkach kodu.

## Order book vs AMM

| Order book (giełda klasyczna) | **Automated Market Maker (AMM)** |
|---|---|
| Kupujący i sprzedający składają zlecenia z ceną | Nikt nie składa zleceń — cena wynika z formuły |
| Cena to punkt, w którym zlecenia się spotykają | Cena to proporcja dwóch rezerw w puli |
| Płynność dostarczają animatorzy rynku | Płynność dostarcza każdy, kto wpłaci do puli |
| Bez animatora — brak drugiej strony, brak transakcji | Wymiana zawsze możliwa, 24/7, dopóki pula ma rezerwy |
| Binance, Openbook | Orca, Raydium |

Order book jest lepszy dla dużych, płynnych rynków — daje ciaśniejsze
ceny. AMM jest prostszy, nie wymaga nikogo po drugiej stronie i działa
dla tokena, który powstał godzinę temu. W DeFi na Solanie istnieją oba,
ale AMM jest punktem wyjścia, bo jest mechanizmem, który da się
zrozumieć w całości.

## Jak działa AMM

**Pula** to konto programu, które trzyma dwa tokeny w pewnej proporcji —
na przykład SOL i USDC. Kto chce wymienić SOL na USDC, wpłaca SOL do
puli i wypłaca z niej USDC. Rezerwa SOL rośnie, rezerwa USDC maleje.
Cena nie jest ustalana przez nikogo — wynika z tego, ile jest jednego
tokena w stosunku do drugiego, a formuła pilnuje, żeby pula nigdy nie
została wyczerpana: im mniej USDC zostaje, tym więcej SOL trzeba dać za
każdy kolejny dolar.

<div className="diagram narrow">

![Trader wpłaca SOL do puli AMM, rezerwa SOL rośnie, rezerwa USDC maleje, trader otrzymuje USDC; nad pulą wzór x · y = k](/img/diagrams/2_amm-01.svg)

</div>

:::tip Analogia — koszyk jabłek i gruszek
Koszyk ma 10 jabłek i 10 gruszek; wymiana idzie po jednym za jedno. Kto
wyjmie 5 gruszek, zostawia koszyk z 15 jabłkami i 5 gruszkami — i teraz
za każdą kolejną gruszkę musi dać 3 jabłka. Im bardziej koszyk jest
nierówny, tym mniej korzystna cena dla tego, kto pogłębia nierówność.
:::

Efekt widać na prawdziwej wycenie. Listing 3-2 pyta agregator Jupiter —
program, który szuka najlepszej trasy przez wszystkie pule na Solanie —
o cenę dwóch wymian: jednego SOL i dziesięciu tysięcy SOL.

```bash
$ curl -s "https://lite-api.jup.ag/swap/v1/quote?inputMint=So11111111111111111111111111111111111111112&outputMint=EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v&amount=1000000000&slippageBps=50"
{ "inAmount": "1000000000", "outAmount": "103035488", "priceImpactPct": "0", ... }

$ curl -s "https://lite-api.jup.ag/swap/v1/quote?inputMint=So1111...&outputMint=EPjF...&amount=10000000000000&slippageBps=50"
{ "inAmount": "10000000000000", "outAmount": "1029677813381", "priceImpactPct": "0.0006", ...
  "routePlan": [ {"label": "TesseraV", "percent": 47}, {"label": "Scorch", "percent": 21}, ... ] }
```

<div className="listing"><strong>Listing 3-2.</strong> Wycena 1 SOL i 10 000 SOL w tym samym momencie (odpowiedzi skrócone). Duża wymiana dostaje gorszą cenę za jednostkę i jest dzielona między kilka pul.</div>

Kwoty są w najmniejszych jednostkach: `1000000000` lamportów to 1 SOL,
`103035488` to 103,035 USDC przy sześciu miejscach po przecinku. Za jeden
SOL agregator daje 103,04 USDC. Za dziesięć tysięcy SOL daje 1 029 678
USDC — czyli 102,97 za sztukę. Różnica to **price impact**: własny wpływ
wymiany na cenę, wynikający z tego, że duża wymiana przesuwa proporcję
rezerw. `priceImpactPct` podaje ją wprost. Pole `routePlan` pokazuje, jak
agregator ją zmniejsza — dzieli zlecenie między kilka pul, żeby żadnej nie
przechylić za mocno. To jest composability z poprzedniego rozdziału w
praktyce: jeden program wywołuje cztery inne w jednej transakcji.

Dokładny wzór, z którego wynika ta różnica, jest w rozdziale [Matematyka
AMM](./03-matematyka-amm.md).

## Kto dostarcza płynność

Pula musi skądś mieć rezerwy. Wpłaca je **Liquidity Provider (LP)** —
każdy, kto zdeponuje oba tokeny w proporcji odpowiadającej aktualnej
cenie. W zamian dostaje udział w puli, zwykle w postaci osobnego tokena
LP, i prawo do części opłat: każda wymiana zostawia w puli niewielki
procent (na przykład 0,25%), który rozkłada się na wszystkich dostawców
proporcjonalnie do udziału. LP może wycofać płynność w dowolnym momencie
— dostaje wtedy oba tokeny w proporcji, jaka jest w puli *teraz*, plus
zebrane opłaty.

<div className="diagram">

![Oś czasu: LP wpłaca 10 SOL i 1 000 USDC; kolejne wymiany zostawiają opłaty w puli; LP wypłaca udział powiększony o opłaty](/img/diagrams/2_amm-02.svg)

</div>

:::tip Przykład
Pula SOL/USDC przy cenie 100 USDC za SOL. LP wpłaca 10 SOL i 1 000 USDC —
oba składniki warte po 1 000 USD. Od tej chwili każda wymiana w puli
zostawia w niej 0,25% obrotu, a LP ma prawo do części tej kwoty
proporcjonalnej do swojego udziału.
:::

W tym mechanizmie jest ukryte ryzyko, które nie ma odpowiednika na
klasycznej giełdzie: LP wpłacił *dwa* tokeny, a ich wzajemna cena się
zmienia. Gdy cena SOL wzrośnie, traderzy będą wyjmować SOL z puli i
wkładać USDC — LP przy wypłacie dostanie mniej SOL i więcej USDC niż
wpłacił, i zwykle mniej wartości, niż gdyby oba tokeny po prostu
trzymał. Zjawisko nazywa się **impermanent loss** i ma własny wzór w
następnym rozdziale.

## Ryzyka w AMM

:::warning Ryzyka, o których warto pamiętać
- **Impermanent loss** — LP traci względem trzymania tokenów, gdy ich
  wzajemna cena odchyla się od ceny wpłaty.
- **Price impact** — duża wymiana względem rozmiaru puli dostaje gorszą
  cenę; Listing 3-2 pokazał to na 10 000 SOL.
- **Slippage** — cena może się zmienić między wysłaniem transakcji a jej
  wykonaniem, bo ktoś inny zdąży wymienić wcześniej. Parametr
  `slippageBps=50` w Listingu 3-2 to zgoda na najwyżej 0,5% różnicy;
  większa różnica cofa transakcję.
- **Oracle manipulation** — inne protokoły czytają cenę z puli; kto na
  chwilę przechyli małą pulę, oszuka program, który jej ufa.
- **Program risk i rug pull** — błąd w kodzie puli albo celowo złośliwy
  kod oznacza utratę rezerw. Program jest publiczny, więc można go
  przeczytać, ale nie każdy to robi.
:::

Mechanizm jest opisany; został wzór. Następny rozdział pokazuje jedno
równanie, z którego wynika cena, koszt dużej wymiany i strata dostawcy
płynności przy zmianie kursu.
