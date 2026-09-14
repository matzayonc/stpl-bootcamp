---
title: Read vs Write
description: Odczyt jest darmowy i natychmiastowy; zapis wymaga podpisu, opłaty i potwierdzenia klastra. Prawdziwy przelew prześledzony od podpisu do zmienionych sald — i co to znaczy, że nie ma backendu.
sidebar_position: 3
slug: read-vs-write
---

# Read vs Write

Każde żądanie, które frontend wysyła do węzła RPC, należy do jednej z
dwóch kategorii: albo **pyta** o stan, albo chce go **zmienić**. W Web2
ta różnica jest techniczna — `GET` kontra `POST`, oba obsługiwane przez
ten sam serwer w ten sam sposób. W Web3 to dwie różne operacje o różnym
koszcie, różnym czasie i różnych wymaganiach, i ta różnica kształtuje
architekturę każdej aplikacji.

## Read

Odczyt to zapytanie do węzła RPC o fragment stanu: saldo, zawartość
konta, listę transakcji, aktualny slot. Listingi 2-1 i 2-2 z
poprzedniego rozdziału były odczytami. Trzy własności odczytu wynikają z
tego, że węzeł ma stan u siebie i nie musi nikogo pytać:

- jest **darmowy** — węzeł odpowiada z własnej kopii, sieć nic o tym nie
  wie i nikt nie pobiera opłaty;
- **nie wymaga podpisu** — stan jest publiczny, więc nie ma czego
  autoryzować; można odczytać saldo dowolnego konta na świecie;
- odpowiedź przychodzi **natychmiast**, w czasie jednego żądania HTTP.

<div className="diagram small">

![Klient wysyła zapytanie do węzła RPC i dostaje odpowiedź bezpośrednio z jego kopii stanu](/img/diagrams/1_paradigm-04.svg)

</div>

Typowy frontend robi dziesiątki odczytów na minutę — odświeża saldo,
sprawdza ceny, pobiera historię — i wszystkie są tak samo tanie jak
zapytania do własnego API w Web2. Tańsze nawet, bo nie trzeba utrzymywać
serwera, który na nie odpowiada.

## Write

Zapis to zmiana stanu: przelew, wywołanie programu, założenie konta.
Węzeł RPC nie może go wykonać sam — stan zmienia się tylko wtedy, gdy
zgodzi się większość klastra. Węzeł jest więc tylko pośrednikiem:
przyjmuje żądanie i przekazuje je liderowi bieżącego slotu, a klient czeka
na wynik głosowania.

<div className="diagram small">

![Klient wysyła podpisaną transakcję do węzła RPC, węzeł przekazuje ją do klastra, a potwierdzenie wraca tą samą drogą](/img/diagrams/1_paradigm-05.svg)

</div>

Żeby klaster w ogóle rozpatrzył żądanie, musi ono mieć formę
**transakcji** — paczki, którą każdy węzeł może sprawdzić bez ufania
nadawcy. Transakcja niesie trzy rzeczy, których odczyt nie potrzebuje:

- **podpis** kluczem prywatnym nadawcy — dowód, że to właściciel konta
  zgadza się na zmianę (o kluczach mówi [następny
  rozdział](./04-portfel-jako-tozsamosc.md));
- **opłatę** dla walidatora za włączenie do bloku — na Solanie stałe
  5 000 lamportów za podpis;
- **czas** — transakcja czeka, aż trafi do bloku i zbierze głosy; to
  ułamek sekundy do pierwszego potwierdzenia i kilkanaście sekund do
  ostatecznego.

Listing 2-3 pokazuje, jak wygląda zapis wykonany z terminala: przelew
0,1 SOL między dwoma adresami na sieci testowej.

```bash
$ solana transfer HDT6d92i8AJQet2Z2MuagpVBzFsVswS9YneEQMzcypDK 0.1 \
    --allow-unfunded-recipient --url devnet

Signature: 5GGpYdKDUdyEKgkesy4tLTHjy17UcoLHrjSip15fBx51r1xEcPf7Z1ayGBgL9vcP58TUoaheWefLhg3KLFxsFjVS
```

<div className="listing"><strong>Listing 2-3.</strong> Zapis: przelew na devnecie. Jedyne, co wraca, to podpis transakcji — jej identyfikator w sieci.</div>

Polecenie zrobiło pod spodem cztery rzeczy: zbudowało transakcję z jedną
instrukcją przelewu, podpisało ją kluczem z domyślnego pliku, wysłało do
węzła RPC z konfiguracji i czekało, aż węzeł zgłosi potwierdzenie. Wynik
to **podpis** — 64 bajty w base58, które są jednocześnie dowodem
autoryzacji i unikalnym identyfikatorem transakcji. Mając podpis, każdy
może zapytać sieć, co się z tą transakcją stało. Listing 2-4 robi
dokładnie to — i jest już odczytem.

```bash
$ curl -s https://api.devnet.solana.com -X POST \
    -H 'content-type: application/json' \
    -d '{"jsonrpc":"2.0","id":1,"method":"getTransaction",
         "params":["5GGpYdKDUdyEKgkesy4tLTHjy17UcoLHrjSip15fBx51r1xEcPf7Z1ayGBgL9vcP58TUoaheWefLhg3KLFxsFjVS",
                   {"encoding":"json"}]}'
{
  "result": {
    "blockTime": 1789405326,
    "slot": 498340046,
    "meta": {
      "fee": 5000,
      "preBalances":  [5826829074,         0, 1],
      "postBalances": [5726824074, 100000000, 1],
      "status": { "Ok": null },
      "computeUnitsConsumed": 150,
      "logMessages": [
        "Program 11111111111111111111111111111111 invoke [1]",
        "Program 11111111111111111111111111111111 success"
      ]
    },
    "transaction": {
      "message": {
        "accountKeys": [
          "8xHTGZeWbr2SmN38A6DahxJyY2vUqri1yKMqkN9spzjj",
          "HDT6d92i8AJQet2Z2MuagpVBzFsVswS9YneEQMzcypDK",
          "11111111111111111111111111111111"
        ],
        "header": { "numRequiredSignatures": 1, ... },
        "instructions": [
          { "programIdIndex": 2, "accounts": [0, 1], "data": "3Bxs411Dtc7pkFQj" }
        ],
        "recentBlockhash": "3wZPMuF6WsMJLjc3XH2shoasnFitpQDZpks8JiSAgmqM"
      },
      "signatures": [
        "5GGpYdKDUdyEKgkesy4tLTHjy17UcoLHrjSip15fBx51r1xEcPf7Z1ayGBgL9vcP58TUoaheWefLhg3KLFxsFjVS"
      ]
    }
  }
}
```

<div className="listing"><strong>Listing 2-4.</strong> Ta sama transakcja odczytana z sieci (pola pogrupowane i skrócone). Wszystkie trzy koszty zapisu są tu widoczne: podpis, opłata i slot, w którym transakcja weszła do bloku.</div>

Każda z trzech różnic między odczytem a zapisem ma w tej odpowiedzi
konkretne pole. `signatures` to podpis, który autoryzował zmianę;
`header.numRequiredSignatures: 1` mówi, że wystarczył jeden. `meta.fee`
to 5 000 lamportów pobranych od nadawcy. `slot` i `blockTime` mówią,
*kiedy* transakcja została włączona do łańcucha — zapis nie dzieje się w
chwili wysłania, tylko w chwili zatwierdzenia.

Najciekawsze są `preBalances` i `postBalances`: salda trzech kont z
`accountKeys` przed i po. Nadawca (indeks 0) stracił 100 005 000
lamportów — 0,1 SOL przelewu plus 5 000 opłaty. Odbiorca (indeks 1)
zyskał dokładnie 100 000 000. Trzecie konto to program, który wykonał
przelew — System Program, o którym mówi rozdział [Własność](../05-konta/02-wlasnosc.md).
Pole `data` instrukcji, `3Bxs411Dtc7pkFQj`, to zakodowane polecenie
„przelej 100 000 000 lamportów"; jak takie dane powstają, wyjaśnia rozdział
[Serializacja i IDL](../06-transakcje-i-anchor/04-serializacja-i-idl.md).

Węzeł nie przyjmie zapisu, który nie ma tej formy. Listing 2-5 pokazuje
odpowiedź na próbę wysłania czegoś, co nie jest poprawnie zbudowaną
transakcją.

```bash
$ curl -s https://api.devnet.solana.com -X POST \
    -H 'content-type: application/json' \
    -d '{"jsonrpc":"2.0","id":1,"method":"sendTransaction",
         "params":["AQAAAAAAAAAAAAAAAAAAAAAAAAAA...",{"encoding":"base64"}]}'
{"jsonrpc":"2.0","error":{"code":-32602,"message":"failed to deserialize solana_transaction::versioned::VersionedTransaction: Attempting to read 32 bytes"},"id":1}
```

<div className="listing"><strong>Listing 2-5.</strong> Węzeł odrzuca bajty, które nie są transakcją, zanim cokolwiek trafi do klastra. Zapis bez podpisu nie ma jak przejść.</div>

| | Read | Write |
|---|---|---|
| Kto odpowiada | jeden węzeł RPC, z własnej kopii | klaster, po głosowaniu |
| Podpis | nie | tak, kluczem prywatnym |
| Koszt | 0 | opłata bazowa 5 000 lamportów za podpis |
| Czas | jedno żądanie HTTP | do bloku w ułamku sekundy, ostatecznie po kilkunastu |
| Przykład | saldo, zawartość konta, status transakcji | przelew, wywołanie programu |

:::note Read vs Write
Odczyt to pytanie do jednego węzła o publiczny stan — darmowe, bez
podpisu, natychmiastowe. Zapis to transakcja: podpisana, opłacona,
zatwierdzona przez klaster. Wszystko, co frontend robi, jest jednym albo
drugim, i warto o każdej operacji wiedzieć, którym.
:::

## Bezserwerowa architektura

Skoro logika jest programem, a stan leży w sieci, to co zostaje z
backendu? Nic. Program on-chain nie działa na serwerze dewelopera — ten
sam kod uruchamia każdy walidator, a wynik uznaje się za prawdziwy, gdy
się zgodzą. Deweloper nie utrzymuje uptime'u, nie robi deploymentu na
VPS, nie skaluje instancji przed kampanią marketingową. Wgrywa program
raz, a sieć wykonuje go dla każdego, kto wyśle transakcję.

<div className="diagram narrow">

![Sześć walidatorów, każdy z identyczną kopią programu i stanu; frontend może pytać dowolnego z nich](/img/diagrams/1_paradigm-06.svg)

</div>

Stan też jest publiczny i leży w sieci, nie w bazie dewelopera. Konto
użytkownika w programie — jego saldo, jego pozycja, jego głos — to konto
na łańcuchu, które użytkownik może obejrzeć w Explorerze bez pytania
autora aplikacji o zgodę. Deweloper pisze logikę i interfejs;
infrastrukturę dostarcza sieć.

:::warning Druga strona medalu
Kod jest publiczny, więc błąd też jest publiczny — każdy może go
przeczytać i wykorzystać. Kod jest wykonywany bezstronnie, więc błędu
nie da się „naprawić po cichu" — poprawka to nowa wersja programu, którą
widać w historii wdrożeń. Brak backendu to nie tylko brak kosztów; to
także brak miejsca, w którym można coś ukryć albo cofnąć.
:::

Zostało jedno pojęcie z pierwszego rozdziału, które nie dostało jeszcze
wyjaśnienia: *podpisana*. Skoro nie ma serwera z tabelą użytkowników, to
skąd sieć wie, kto wysyła transakcję? Odpowiedź jest w następnym
rozdziale.
