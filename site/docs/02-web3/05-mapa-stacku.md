---
title: Mapa stacku Web3
description: Frontend, portfel, RPC, klaster, program, konta — sześć ogniw ułożonych w jeden łańcuch, i dwa z nich, które pisze deweloper.
sidebar_position: 5
slug: mapa-stacku
---

# Mapa stacku Web3

Poprzednie rozdziały wprowadziły elementy nowej architektury po jednym:
klienta, węzeł RPC, transakcję, portfel. Ten rozdział układa je w jeden
łańcuch, który warto zapamiętać jako obraz — każdy kolejny temat kursu
dotyczy jednego z jego ogniw, a pytanie „gdzie na mapie jesteśmy?" ma
zawsze konkretną odpowiedź.

## Sześć ogniw

Droga, jaką przebywa jedna operacja użytkownika — od kliknięcia do
zmienionego stanu — przechodzi przez sześć elementów.

<div className="diagram">

![Frontend → Wallet Adapter → RPC → Klaster → Program → Konta: sześć ogniw stacku Web3 połączonych strzałkami](/img/diagrams/1_paradigm-08.svg)

</div>

1. **Frontend** — aplikacja w przeglądarce. Wyświetla stan, buduje
   transakcje, pokazuje wynik. Pisana w tym, w czym pisze się każdy
   frontend: TypeScript, React, dowolny framework.
2. **Wallet adapter** — warstwa, która łączy frontend z portfelem
   użytkownika. Frontend nie wie, czy użytkownik ma Phantoma, Solflare czy
   portfel sprzętowy; prosi adapter o podpis, a adapter rozmawia z tym
   portfelem, który jest zainstalowany. Standard, który to umożliwia,
   nazywa się **Wallet Standard**.
3. **RPC** — węzeł, do którego frontend wysyła odczyty i podpisane
   transakcje. Wybierany z setek wymiennych dostawców, jak w rozdziale
   [RPC node](./02-rpc-node.md).
4. **Klaster** — walidatorzy, którzy przyjmują transakcję, wykonują ją
   i głosują nad wynikiem. Jedno słowo na całą sieć BFT z pierwszego
   tematu.
5. **Program** — kod on-chain, który klaster uruchamia dla tej
   transakcji. Odpowiednik logiki backendu.
6. **Konta** — miejsce, w którym program zapisuje wynik. Odpowiednik
   bazy danych, z tą różnicą, że publiczny i nienależący do nikogo.

W skrócie: **klient → podpis → RPC → klaster → program → konta**. Odczyt
przechodzi tylko przez trzy pierwsze ogniwa i wraca; zapis idzie do końca.

## Co pisze deweloper

Z sześciu ogniw deweloper pisze **dwa**: frontend i program. Reszta jest
gotowa i wspólna dla całego ekosystemu.

<div className="diagram">

![Ten sam łańcuch sześciu ogniw; Frontend i Program wyróżnione na czerwono jako te, które pisze deweloper](/img/diagrams/1_paradigm-09.svg)

</div>

Portfel pisze zespół Phantoma, adapter to biblioteka, węzły RPC
utrzymują dostawcy, klaster prowadzą walidatorzy, a konta są mechanizmem
sieci. Deweloper, który w Web2 pisał frontend, backend, warstwę
tożsamości i schemat bazy, w Web3 pisze frontend i program — a
tożsamość, infrastruktura i przechowywanie danych są dostarczone.

Listing 2-7 pokazuje, jak wygląda styk frontendu z resztą stacku w
bibliotece **Solana Kit**: jedno wywołanie tworzy klienta z adresem węzła
RPC i automatycznym wykrywaniem portfeli, a odczyt salda jest wywołaniem
metody nazwanej tak samo, jak metoda JSON-RPC z Listingu 2-2.

```ts
import { autoDiscover, createClient } from '@solana/client';

const client = createClient({
  endpoint: 'https://api.devnet.solana.com',   // ogniwo 3: RPC
  walletConnectors: autoDiscover(),            // ogniwo 2: portfel
});

// odczyt — ogniwa 1 → 3 i z powrotem
const { value: lamports } = await client.rpc.getBalance(address).send();
```

<div className="listing"><strong>Listing 2-7.</strong> Styk frontendu ze stackiem. Adres węzła i wykrywanie portfeli to cała konfiguracja; <code>getBalance</code> to ta sama metoda, którą wywołał <code>curl</code> w Listingu 2-2.</div>

Program — drugie ogniwo, które pisze deweloper — jest tematem czterech
kolejnych rozdziałów: [Rust](../04-rust/index.md) jako język, [Model
kont](../05-konta/index.md) jako sposób przechowywania danych,
[Transakcje i Anchor](../06-transakcje-i-anchor/index.md) jako framework.
Zanim to nastąpi, jeden temat pokazuje, co takie programy robią w
praktyce — i dlaczego to działa jako finanse.

:::tip Analogia — sklep internetowy na cudzej platformie
Sprzedawca na dużej platformie handlowej projektuje witrynę i opisuje
produkty; płatności, logowanie, magazyn i dostawa są platformy. Deweloper
Web3 projektuje frontend i pisze program; portfel, RPC, klaster i konta są
sieci. Różnica: platforma należy do jednej firmy, a sieć — do nikogo.
:::
