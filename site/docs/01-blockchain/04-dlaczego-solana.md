---
title: Dlaczego Solana?
description: Ograniczenia Bitcoina i Ethereum, liczby zmierzone na sieci głównej — czas slotu, transakcje na blok, opłata — i dwa mechanizmy, które za nimi stoją.
sidebar_position: 4
slug: dlaczego-solana
---

# Dlaczego Solana?

Program on-chain ma sens tylko wtedy, gdy sieć wykonuje go szybko i tanio.
Kantor, w którym wymiana trwa dziesięć minut i kosztuje pięćdziesiąt
dolarów, nie zastąpi kantoru — zastąpi go co najwyżej dla dużych
przelewów między bankami. Ten rozdział odpowiada na pytanie, dlaczego
kurs jest o Solanie, a nie o innej sieci, i robi to liczbami odczytanymi z
sieci głównej.

## Obecne ograniczenia

**Bitcoin** rozwiązał problem z pierwszych dwóch rozdziałów: to sieć BFT z
publicznym rejestrem, działająca bez przerwy od 2009 roku. Ale Bitcoin
celowo nie ma programów on-chain — jego język skryptowy pozwala tylko na
proste warunki wydania środków. Da się na nim przechowywać wartość; nie
da się zbudować pożyczki ani wymiany.

**Ethereum** dodało programy on-chain i jest do dziś największym
ekosystemem smart kontraktów. Cena tej uniwersalności to przepustowość:
sieć bazowa przetwarza kilkanaście transakcji na sekundę, a opłata za
transakcję rośnie wraz z obciążeniem, bo użytkownicy licytują o miejsce w
bloku. W szczytach popularności opłata za prostą wymianę przekraczała 50
dolarów. Przy takim koszcie sens mają tylko duże operacje — mikropłatność,
gra czy program, który wykonuje wiele małych kroków, są ekonomicznie
niemożliwe.

Odpowiedzią Ethereum są sieci drugiej warstwy (**Layer 2**), które
wykonują transakcje poza siecią bazową i zapisują na niej tylko skrót.
Opłaty spadają, ale ekosystem się **fragmentuje**: każda warstwa ma
osobny stan, osobną płynność i osobne mosty między sobą, a program na
jednej warstwie nie może bezpośrednio wywołać programu na innej.

:::warning Problem
Sieć BFT, która wykonuje programy, ale robi to wolno i drogo, jest
zabawką, nie infrastrukturą. Skala nie jest dodatkiem do pomysłu z
poprzedniego rozdziału — jest warunkiem, żeby ten pomysł miał sens.
:::

## Solana

Solana została zaprojektowana z odwrotnym założeniem: jedna warstwa,
która sama jest wystarczająco szybka, żeby nie potrzebować drugiej.
Zamiast powtarzać liczby z materiałów marketingowych, lepiej je zmierzyć.
Listing 1-4 odczytuje czas powstania dwóch bloków oddalonych o dziesięć
tysięcy slotów.

```bash
$ curl -s https://api.mainnet-beta.solana.com -X POST \
    -H 'content-type: application/json' \
    -d '{"jsonrpc":"2.0","id":1,"method":"getBlockTime","params":[447000000]}'
{"jsonrpc":"2.0","result":1789396293,"id":1}

$ curl -s https://api.mainnet-beta.solana.com -X POST \
    -H 'content-type: application/json' \
    -d '{"jsonrpc":"2.0","id":1,"method":"getBlockTime","params":[447010000]}'
{"jsonrpc":"2.0","result":1789399446,"id":1}
```

<div className="listing"><strong>Listing 1-4.</strong> Czas (w sekundach od 1970) dwóch slotów odległych o 10 000. Różnica to 3 153 sekundy — jeden slot trwa około 315 ms.</div>

**Slot** to okno czasu, w którym jeden walidator ma prawo wyprodukować
blok. Dokumentacja Solany podaje 400 ms jako projektowy czas slotu; w
chwili pisania sieć główna jest szybsza i domyka slot w niecałe 320 ms.
Dla porównania Bitcoin produkuje blok co około dziesięć minut, Ethereum
co dwanaście sekund. Transakcja wysłana do Solany trafia do bloku w
ułamku sekundy, a status *confirmed* — potwierdzenie przez większość
głosów — dostaje zwykle w kolejnej.

Listing 1-5 pokazuje, ile pracy mieści się w jednym takim slocie.

```bash
$ solana epoch-info --url mainnet-beta
Block height: 425071651
Slot: 447029244
Epoch: 1034
Transaction Count: 548422147382
Epoch Slot Range: [446688000..447120000)
Epoch Completed Percent: 78.992%
Epoch Completed Slots: 341244/432000 (90756 remaining)
Epoch Completed Time: 1day 5h 55m 44s/1day 13h 53m 42s (7h 57m 58s remaining)
```

<div className="listing"><strong>Listing 1-5.</strong> Stan sieci głównej w chwili pisania: 548 miliardów transakcji od startu, 432 000 slotów na epokę, epoka trwa niecałe półtora dnia.</div>

`Transaction Count` to łączna liczba transakcji wykonanych przez sieć od
jej uruchomienia — ponad pół biliona. Blok 447028671 z Listingu 1-2
zawierał 1 453 transakcje (odczyt tego samego `getBlock` z
`"transactionDetails": "signatures"`); przy trzech blokach na sekundę daje to kilka tysięcy transakcji
na sekundę w zwykłym ruchu, z zapasem sięgającym dziesiątek tysięcy. Część
tych transakcji to głosy walidatorów, które też przechodzą przez łańcuch —
ale to właśnie pokazuje skalę: sieć, która obsługuje własny konsensus jako
zwykłe transakcje, ma przepustowość porównywalną z siecią kart
płatniczych.

`Epoch Completed Time` daje drugą drogę do czasu slotu: 341 244 sloty w
107 744 sekund to ten sam wynik, co w Listingu 1-4. Dwa niezależne
pomiary, jedna liczba — tak wygląda weryfikacja, o której mówił rozdział o
[konsensusie](./02-konsensus-bft.md).

Ostatnia liczba to opłata. Każda transakcja na Solanie kosztuje stałą
opłatę bazową 5 000 lamportów za podpis — 0,000005 SOL, ułamek centa
niezależnie od obciążenia sieci. Listing 7-6 w rozdziale [Pierwsza
transakcja](../07-portfel-i-narzedzia/04-pierwsza-transakcja.md) pokazuje
tę opłatę pobraną z prawdziwego przelewu.

:::note Kluczowe liczby
- **~315 ms** — czas slotu zmierzony w chwili pisania (400 ms projektowo)
- **tysiące transakcji na sekundę** w zwykłym ruchu, dziesiątki tysięcy w szczycie
- **0,000005 SOL** — opłata bazowa za podpis, stała
- **jedna warstwa** — jeden stan, jedna płynność, programy wywołują się nawzajem bezpośrednio
:::

## Skąd te liczby

Dwa mechanizmy odpowiadają za skalę i oba warto znać z nazwy, bo wracają
w dalszych rozdziałach.

**Proof of History (PoH)** to kryptograficzny zegar. W klasycznej sieci
BFT węzły muszą najpierw uzgodnić *kolejność* zdarzeń, a dopiero potem
ich treść — i to uzgadnianie jest wolne, bo wymaga wymiany wiadomości
między wszystkimi. Solana każe liderowi slotu wpleść transakcje w ciąg
hashy liczonych jeden po drugim; skoro hash N+1 zależy od hasha N, to
transakcja wpisana między nie na pewno wydarzyła się po jednej i przed
drugą. Kolejność jest udowodniona w samych danych, więc węzły nie muszą
jej negocjować.

**Sealevel** to środowisko wykonania, które uruchamia transakcje
**równolegle**. Jest to możliwe, bo każda transakcja na Solanie deklaruje
z góry, których kont dotknie — jak wyjaśnia rozdział [Model
kont](../05-konta/index.md). Dwie transakcje, które dotykają różnych kont,
nie mogą sobie przeszkodzić, więc walidator wykonuje je jednocześnie na
różnych rdzeniach procesora. Ethereum wykonuje transakcje jedna po
drugiej, bo nie wie z góry, co która zmieni.

:::tip Analogia — kasy w supermarkecie
Sieć z jedną kolejką obsługuje klientów po kolei, choćby miała dziesięć
kasjerów. Solana każe każdemu klientowi napisać na wejściu, co kupuje —
i klienci z różnymi listami idą do różnych kas jednocześnie. Zegar PoH to
numerek z automatu, który rozstrzyga kolejność bez pytania kasjerów.
:::

To zamyka pierwszy temat. Sieć BFT z publicznym rejestrem rozwiązuje
problem zaufania; programy on-chain zastępują instytucje; Solana robi to w
skali, w której zastąpienie ma sens. Następny temat schodzi o poziom
niżej: co dokładnie zmienia się w architekturze aplikacji, gdy backend
staje się programem w sieci.
