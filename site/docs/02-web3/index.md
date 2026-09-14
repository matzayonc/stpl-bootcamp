---
title: Paradygmat Web3
description: Co znika z Web2 stacku i co wchodzi na jego miejsce — RPC, transakcja, portfel — prześledzone na prawdziwych zapytaniach i prawdziwym przelewie.
sidebar_position: 0
---

# Paradygmat Web3

Jedno zdanie organizuje ten temat: **backend staje się programem, a baza
danych — publicznymi kontami**. Wszystko inne wynika z tego zdania: skoro
nie ma serwera, klient musi dotrzeć do sieci przez węzeł RPC; skoro nie ma
bazy użytkowników, tożsamość musi być parą kluczy; skoro stan jest
wspólny, odczyt i zapis są dwiema różnymi operacjami. Kto zrozumie tę
mapę, wie, gdzie w niej leży każdy następny temat.

Rozdział rozwija slajdy *Paradygmat Web3*
([PDF](https://github.com/matzayonc/stpl-slides/releases/download/latest/1_paradigm.pdf))
o rzeczy, których na wykładzie nie ma: zapytania JSON-RPC wykonane z
terminala do dwóch niezależnych dostawców, prawdziwy przelew rozłożony
na podpis, opłatę i zmienione salda, i podpis kryptograficzny sprawdzony
na własnym kluczu.

## Zawartość

1. [Web2 vs Web3](./01-web2-vs-web3.md) — klient, serwer i prywatna
   baza kontra klient, klaster i publiczny program; tabela tego, co się
   zmienia.
2. [RPC node](./02-rpc-node.md) — okno na łańcuch, **RPC**, format
   JSON-RPC, to samo saldo z dwóch niezależnych dostawców, węzeł jako
   pośrednik, nie źródło prawdy.
3. [Read vs Write](./03-read-vs-write.md) — odczyt darmowy i bez
   podpisu; zapis jako **transakcja** z podpisem, opłatą i slotem;
   prawdziwy przelew w `getTransaction`; architektura bez backendu.
4. [Portfel jako tożsamość](./04-portfel-jako-tozsamosc.md) — para
   kluczy, podpis i jego weryfikacja z CLI, portfel jako login do
   wszystkiego, konsekwencje UX i cena suwerenności.
5. [Mapa stacku Web3](./05-mapa-stacku.md) — sześć ogniw od frontendu
   do kont, dwa z nich pisze deweloper, styk z biblioteką Kit.

Pytania sprawdzające do rozdziału: [Paradygmat Web3 — pytania
kontrolne](../08-pytania-kontrolne/01-paradygmat-web3.md).

## Podsumowanie

Web2 to klient, serwer i prywatna baza: serwer jest jedynym źródłem
prawdy, a klient musi mu ufać. Web3 wymienia środek tej architektury —
klient wysyła **podpisaną transakcję** do klastra, który wykonuje
**publiczny program** i zapisuje wynik w **kontach** na łańcuchu. Logika
staje się programem, dane stają się publiczne, a infrastruktura przestaje
być problemem dewelopera.

Klient nie łączy się z klastrem bezpośrednio, tylko z **węzłem RPC** —
jednym z setek wymiennych węzłów, które trzymają kopię stanu i wystawiają
to samo API JSON-RPC. Dwa obce sobie węzły zwracają to samo saldo co do
lamporta, bo żaden nie jest źródłem prawdy; oba ją czytają. Węzeł może
być opóźniony lub przeciążony, więc odpowiedź niesie `context.slot`, który
mówi, z jakiego momentu pochodzi.

Każde żądanie jest **odczytem** albo **zapisem**. Odczyt to pytanie do
jednego węzła o publiczny stan: darmowe, bez podpisu, natychmiastowe.
Zapis to **transakcja**: podpisana kluczem prywatnym, opłacona stałą
opłatą bazową 5 000 lamportów za podpis, wykonana dopiero w slocie, w
którym klaster ją zatwierdził. `getTransaction` pokazuje wszystkie trzy
koszty w polach `signatures`, `meta.fee` i `slot`, a `preBalances` i
`postBalances` — dokładny efekt.

Tożsamość nie jest przechowywana, tylko posiadana: **klucz publiczny**
jest adresem, **klucz prywatny** składa **podpis**, który każdy węzeł
weryfikuje bez pytania kogokolwiek, i który staje się nieważny po zmianie
jednego bajtu treści. **Portfel** trzyma klucz i podpisuje w imieniu
użytkownika, będąc loginem do każdej aplikacji naraz. Ceną jest brak
ekranu „zapomniałem hasła" — utrata klucza to utrata dostępu.

Cały stack to sześć ogniw: **frontend → wallet adapter → RPC → klaster →
program → konta**. Deweloper pisze pierwsze i piąte; reszta jest gotowa i
wspólna dla ekosystemu.

:::tip Analogia na koniec
Serwer Web2 to jeden właściciel prawdy; węzeł RPC to bankomat dowolnej
sieci, który tę prawdę tylko odczytuje; podpis to podpis odręczny, którego
nie da się podrobić, ale i nie da się wyrobić na nowo; a deweloper Web3 to
sprzedawca na platformie, która nie należy do nikogo — projektuje witrynę
i towar, a płatności, logowanie i magazyn dostaje od sieci.
:::

## Ćwiczenia

Ćwiczenia wymagają `curl` i przeglądarki; ćwiczenie 3 wymaga Solana CLI
(rozdział [Portfel i narzędzia](../07-portfel-i-narzedzia/index.md)).

1. **Dwa węzły, jeden stan.** Odczytaj `getBalance` dla adresu z Listingu
   2-2 z trzech różnych publicznych węzłów RPC (dwa z rozdziału plus
   dowolny znaleziony w dokumentacji dostawcy). Zapisz `value`,
   `context.slot` i `apiVersion` z każdej odpowiedzi. Które pola się
   różnią i dlaczego to nie jest problem?

2. **Rozbiór transakcji.** Wybierz dowolną transakcję z Explorera na
   sieci głównej i pobierz ją przez `getTransaction`. Wskaż w odpowiedzi:
   ile podpisów była wymagana (`numRequiredSignatures`), ile wyniosła
   opłata, które konto ją zapłaciło (porównaj `preBalances` i
   `postBalances`) i ile instrukcji zawierała. Czy różnica sald zgadza się
   z opłatą co do lamporta?

3. **Podpis nie wędruje.** Wygeneruj klucz `solana-keygen new -o
   test.json`, podpisz nim trzy różne wiadomości i zweryfikuj każdy podpis
   z każdą wiadomością (dziewięć kombinacji). Zapisz tabelę wyników.
   Następnie zweryfikuj jeden z podpisów z `--signer` ustawionym na klucz
   publiczny innej osoby (dowolny adres z Explorera). Co mówi wynik o
   tym, kto może „przejąć" cudzy podpis?

4. **Read czy write?** Dla każdej operacji w typowej aplikacji giełdowej
   — wyświetlenie kursu, wyświetlenie salda, złożenie zlecenia, anulowanie
   zlecenia, pobranie historii, połączenie portfela — określ, czy to
   odczyt, czy zapis, i przez które ogniwa mapy stacku przechodzi. Które
   z tych operacji wymagają zgody użytkownika w portfelu?
