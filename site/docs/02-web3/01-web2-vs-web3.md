---
title: Web2 vs Web3
description: Centralny serwer z prywatną bazą kontra klaster węzłów wykonujący publiczny program — oba modele w jednym zdaniu i to, co między nimi znika.
sidebar_position: 1
slug: web2-vs-web3
---

# Web2 vs Web3

Pierwszy temat odpowiedział na pytanie *po co* istnieje blockchain. Ten
temat schodzi o poziom niżej i pyta, *co to zmienia dla kogoś, kto pisze
aplikacje*. Punkt wyjścia to porównanie dwóch architektur — tej, którą
każdy deweloper zna, i tej, która zastępuje jej środek.

## Web2 w jednym zdaniu

Klasyczna aplikacja to trzy warstwy: klient, serwer i baza danych. Klient
— przeglądarka albo aplikacja mobilna — wysyła żądanie przez HTTPS do
serwera firmy. Serwer sprawdza, kim jest użytkownik, wykonuje logikę i
zapisuje wynik w bazie, do której nikt poza firmą nie ma dostępu. W jednym
zdaniu: **klient pyta centralny serwer, który ufa sam sobie**.

<div className="diagram narrow">

![Klient łączy się przez HTTPS z serwerem firmy, który jako jedyny ma dostęp do prywatnej bazy danych](/img/diagrams/1_paradigm-01.svg)

</div>

Ta architektura ma jedną cechę, która w Web2 jest tak oczywista, że nikt
jej nie nazywa: **serwer jest jedynym źródłem prawdy**. Gdy klient pyta o
saldo, serwer odpowiada liczbą z własnej bazy, a klient nie ma jak
sprawdzić, czy liczba jest prawdziwa. Gdy klient prosi o przelew, serwer
decyduje, czy go wykonać — i decyzja nie podlega weryfikacji z zewnątrz.
Aplikacja działa dokładnie tak długo, jak długo działa i chce działać jej
operator.

:::warning Jeden właściciel prawdy
Firma decyduje, co jest w bazie. Wszystko, co klient widzi, jest tym, co
serwer zdecydował się pokazać. To nie jest wada implementacji, którą da się
naprawić lepszym kodem — to definicja modelu.
:::

Dla dewelopera ta architektura oznacza konkretną listę obowiązków: serwer
trzeba postawić, utrzymać, skalować, zabezpieczyć i monitorować; bazę
trzeba zaprojektować, backupować i migrować; tożsamość użytkowników trzeba
przechowywać i chronić. Większość pracy nad typową aplikacją Web2 to nie
logika biznesowa, tylko infrastruktura wokół niej.

## Web3 w jednym zdaniu

W Web3 środek tej architektury zostaje wymieniony. Klient nadal istnieje —
to ta sama przeglądarka. Ale zamiast wysyłać żądanie do serwera firmy,
wysyła **podpisaną transakcję** do sieci węzłów, które nie należą do
nikogo konkretnego. Logika, którą w Web2 wykonywał serwer, żyje w sieci
jako **program on-chain**. Dane, które leżały w prywatnej bazie, leżą w
**kontach** na łańcuchu — publicznie, w kopii na każdym węźle. W jednym
zdaniu: **klient wysyła podpisaną transakcję do klastra, który wykonuje
publiczny program**.

<div className="diagram narrow">

![Klient podpisuje transakcję i wysyła ją do klastra węzłów, które zapisują wynik w kontach na łańcuchu](/img/diagrams/1_paradigm-02.svg)

</div>

Trzy słowa w tym zdaniu wymagają rozwinięcia i każde dostaje własny
rozdział. **Podpisana** — bo nie ma serwera, który sprawdzi hasło; o tym
w [Portfelu jako tożsamości](./04-portfel-jako-tozsamosc.md). **Klaster** —
bo klient musi jakoś dotrzeć do sieci, a nie może połączyć się z każdym
węzłem naraz; o tym w [RPC node](./02-rpc-node.md). **Wykonuje** — bo
odczyt i zapis to w tym modelu dwie zupełnie różne operacje; o tym w
[Read vs Write](./03-read-vs-write.md).

To, co zostało, nazywa się często **bezzaufaniowym wykonaniem**
(*trustless execution*): wynik operacji nie zależy od dobrej woli żadnego
podmiotu, bo ten sam kod na tych samych danych wykonują niezależnie setki
węzłów, a wynik uznaje się za prawdziwy dopiero wtedy, gdy się zgodzą.
Klient nie ufa serwerowi, bo serwera nie ma.

:::tip Backend staje się programem
Nie ma serwera firmy — jest klaster węzłów, który każdy może odpytać, i
program, który każdy może przeczytać. To, co deweloper Web2 nazywał
„backendem", dzieli się na dwie części: logikę, która staje się programem
on-chain, i infrastrukturę, która przestaje być jego problemem.
:::

| | Web2 | Web3 |
|---|---|---|
| Logika | serwer firmy | program on-chain |
| Dane | prywatna baza | konta na łańcuchu, publiczne |
| Tożsamość | login i hasło w bazie | para kluczy w portfelu |
| Kto sprawdza żądanie | serwer, ufając sobie | każdy węzeł, weryfikując podpis |
| Kto utrzymuje infrastrukturę | deweloper | sieć |

Tabela mówi, *co* się zmienia. Reszta tematu mówi, *jak* — zaczynając od
pytania, z czym właściwie łączy się klient, skoro serwera nie ma.
