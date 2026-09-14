---
title: RPC node
description: Węzeł, przez który frontend czyta stan łańcucha i wysyła transakcje — jedno API, setki dostawców, i pierwsze zapytania wykonane z terminala.
sidebar_position: 2
slug: rpc-node
---

# RPC node

Poprzedni rozdział skończył się pytaniem: z czym łączy się klient, skoro
nie ma serwera firmy? Nie z „siecią" w ogóle — sieć to kilkaset
walidatorów i tysiące innych węzłów, a przeglądarka nie może utrzymywać
połączenia z każdym z nich. Klient potrzebuje jednego adresu, pod który
wyśle zapytanie, i który odpowie w imieniu całej sieci.

## Okno na łańcuch

Ten adres to **RPC node**: węzeł sieci, który trzyma aktualną kopię stanu
i wystawia zwykłe API po HTTPS. Frontend pyta go o saldo, o zawartość
konta, o status transakcji — i wysyła mu podpisane transakcje do
przekazania dalej. Nazwa pochodzi od **Remote Procedure Call (RPC)** —
protokołu, w którym klient wywołuje funkcję po nazwie, a serwer zwraca jej
wynik.

Kluczowa różnica wobec API w Web2: takich węzłów są **setki**, prowadzą je
różne firmy i osoby, i wszystkie mówią tym samym językiem. Helius,
QuickNode, Triton, publiczny węzeł Fundacji Solana, własny węzeł
postawiony w piwnicy — każdy odpowie na to samo zapytanie tą samą
odpowiedzią, bo wszystkie czytają ten sam łańcuch. Frontend może zmienić
dostawcę, zmieniając jeden URL w konfiguracji. Nie ma czegoś takiego jak
„API firmy X", które przestaje działać, gdy firma X zamknie usługę.

<div className="diagram narrow">

![Frontend wysyła zapytania do jednego z wielu dostawców RPC — Helius, QuickNode albo własnego węzła — a każdy z nich rozmawia z klastrem](/img/diagrams/1_paradigm-03.svg)

</div>

:::note RPC node
Węzeł sieci, który przyjmuje zapytania klienta i zwraca aktualny stan
łańcucha lub przekazuje transakcję do klastra. Wszystkie węzły RPC
wystawiają to samo API (JSON-RPC po HTTPS), więc są wymienne.
:::

## Pierwsze zapytanie

API jest na tyle proste, że da się z niego korzystać bez żadnej
biblioteki. Listing 2-1 pyta publiczny węzeł sieci głównej o dwie rzeczy:
czy działa, i jaką wersję oprogramowania uruchamia.

```bash
$ curl -s https://api.mainnet-beta.solana.com -X POST \
    -H 'content-type: application/json' \
    -d '{"jsonrpc":"2.0","id":1,"method":"getHealth"}'
{"jsonrpc":"2.0","result":"ok","id":1}

$ curl -s https://api.mainnet-beta.solana.com -X POST \
    -H 'content-type: application/json' \
    -d '{"jsonrpc":"2.0","id":1,"method":"getVersion"}'
{"jsonrpc":"2.0","result":{"feature-set":2409014235,"solana-core":"4.3.0-rc.0"},"id":1}
```

<div className="listing"><strong>Listing 2-1.</strong> Dwa zapytania JSON-RPC do publicznego węzła. Żądanie to obiekt z nazwą metody; odpowiedź to obiekt z polem <code>result</code>.</div>

Format jest zawsze ten sam. Żądanie to JSON z trzema polami: `jsonrpc`
(wersja protokołu), `method` (nazwa funkcji do wywołania) i `id` (numer,
który węzeł odeśle w odpowiedzi, żeby klient mógł sparować odpowiedzi z
pytaniami, gdy wysyła kilka naraz). Odpowiedź niesie ten sam `id` i pole
`result` z wynikiem. `getHealth` zwróciło `"ok"` — węzeł nadąża za siecią.
`getVersion` zwróciło wersję węzła; to informacja o *tym konkretnym*
węźle, nie o sieci, i różne węzły mogą zwrócić różne wartości.

Listing 2-2 zadaje pytanie, które ma już parametry: o saldo konkretnego
konta.

```bash
$ curl -s https://api.mainnet-beta.solana.com -X POST \
    -H 'content-type: application/json' \
    -d '{"jsonrpc":"2.0","id":1,"method":"getBalance",
         "params":["5tzFkiKscXHK5ZXCGbXZxdw7gTjjD1mBwuoFbhUvuAi9"]}'
{"jsonrpc":"2.0","result":{"context":{"apiVersion":"4.3.0-rc.0","slot":447030351},"value":1865318783298127},"id":1}

$ curl -s https://solana-rpc.publicnode.com -X POST \
    -H 'content-type: application/json' \
    -d '{"jsonrpc":"2.0","id":1,"method":"getBalance",
         "params":["5tzFkiKscXHK5ZXCGbXZxdw7gTjjD1mBwuoFbhUvuAi9"]}'
{"jsonrpc":"2.0","result":{"context":{"apiVersion":"4.2.2","slot":447030350},"value":1865318783298127},"id":1}
```

<div className="listing"><strong>Listing 2-2.</strong> To samo pytanie do dwóch niezależnych dostawców. Różne wersje węzła, sąsiednie sloty, identyczne saldo.</div>

Tablica `params` niesie argumenty — tutaj jeden: adres konta. Odpowiedź
ma dwie części. `value` to saldo w lamportach (jedna miliardowa SOL; konto
ma 1,86 miliona SOL, bo to portfel dużej giełdy). `context.slot` mówi, z
którego momentu łańcucha pochodzi odpowiedź — saldo może się zmienić
sekundę później, a klient, który porównuje dwie odpowiedzi, powinien
porównać też sloty.

Drugie wywołanie idzie do innego dostawcy, prowadzonego przez inną firmę,
na innym oprogramowaniu (`4.2.2` zamiast `4.3.0-rc.0`). Saldo jest
identyczne co do lamporta. To jest praktyczny sens słowa *wymienne*: dwa
obce sobie serwery odpowiadają tak samo, bo żaden z nich nie jest źródłem
prawdy — oba tylko ją czytają.

:::tip Analogia — bankomat dowolnej sieci
Karta działa w każdym bankomacie, nie tylko w bankomacie własnego banku,
bo wszystkie bankomaty mówią tym samym protokołem i pytają o to samo
konto. RPC node to bankomat: można wybrać ten najbliżej, ten
najszybszy albo postawić własny — saldo będzie to samo.
:::

## Kto płaci za węzeł

Publiczny węzeł `api.mainnet-beta.solana.com` jest darmowy, ale ma limity
zapytań i nie nadaje się na produkcję. Aplikacje korzystają z dostawców
komercyjnych, którzy sprzedają przepustowość — tak jak firmy Web2 kupują
hosting. Różnica jest w tym, co się kupuje: nie miejsce na własną logikę i
dane, tylko **dostęp do cudzych**, które są takie same u każdego
dostawcy. Dostawcę RPC zmienia się w minutę; dostawcę hostingu bazy
danych — w miesiąc.

:::warning Węzeł RPC nie jest źródłem prawdy
Węzeł może być opóźniony, przeciążony albo — w skrajnym przypadku —
złośliwy i zwracać nieprawdziwe dane. Klient, który chce mieć pewność,
pyta dwa węzły albo sprawdza dowód kryptograficzny. W praktyce wybiera się
renomowanego dostawcę i porównuje `context.slot` z bieżącym; do tego
wraca rozdział o [Explorerze](../07-portfel-i-narzedzia/04-pierwsza-transakcja.md).
:::

Węzeł RPC obsługuje dwa rodzaje żądań: takie, które pytają o stan, i
takie, które go zmieniają. Listingi 2-1 i 2-2 pokazały tylko pierwszy
rodzaj — i celowo, bo drugi wygląda zupełnie inaczej. To temat następnego
rozdziału.
