---
title: Konta w praktyce
description: Trzy sposoby odczytu konta — Explorer, CLI i RPC — na tych samych trzech adresach, oraz dwa znaczenia słowa owner w odpowiedzi JSON.
sidebar_position: 5
slug: w-praktyce
---

# Konta w praktyce

Wszystko z tego rozdziału da się zobaczyć na żywo, bez własnego węzła i
bez pisania kodu. RPC to okno na łańcuch (rozdział
[RPC node](../02-web3/02-rpc-node.md)); Explorer jest jego czytelną wersją,
a CLI — wersją dla terminala. Ta strona przechodzi przez te same trzy konta
trzema narzędziami, żeby pola z Listingu 5-1 przestały być abstrakcją.

## Trzy adresy do sprawdzenia

| Rola | Adres |
|---|---|
| portfel (System Program) | `5tzFkiKscXHK5ZXCGbXZxdw7gTjjD1mBwuoFbhUvuAi9` |
| konto tokena USDC (Token Program, PDA) | `FzbcyEZ9m8xjtergWgWDq7mfPoHEbboBF791B6cTpzbq` |
| program (loader) | `TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA` |

Wszystkie trzy są na mainnecie. Na devnecie te same role pełnią własny
portfel z Phantoma, konto tokena założone przez faucet i program wdrożony
na sesji live — warto powtórzyć poniższe kroki na własnych adresach po
rozdziale [Portfel i narzędzia](../07-portfel-i-narzedzia/index.md).

## Explorer

Po wklejeniu adresu w `explorer.solana.com` strona konta pokazuje na
górze sekcję *Overview*. Mapa na pola konta:

| Explorer | Pole |
|---|---|
| *Address* | klucz w mapie (nie pole struktury) |
| *Balance (SOL)* | `lamports` ÷ 10⁹ |
| *Allocated Data Size* | długość `data` w bajtach |
| *Assigned Program Id* | `owner` |
| *Executable* | `executable` |

Explorer robi jedną rzecz więcej niż surowe pola: gdy zna program-właściciela,
**dekoduje** `data`. Dla konta tokena pokaże mint, posiadacza i saldo w
USDC; dla programu Anchora z opublikowanym IDL — pola struktury z nazwami
z kodu (rozdział [Serializacja i
IDL](../06-transakcje-i-anchor/04-serializacja-i-idl.md)). Dla konta bez
znanego układu wyświetli hex, tak jak `solana account`.

## CLI

Polecenie `solana account` pojawiło się już w Listingach 5-2 do 5-4.
Dwa dodatki, które oszczędzają czas:

```bash
$ solana config set --url devnet          # domyślna sieć dla wszystkich poleceń
$ solana account <ADRES> --output json    # to samo co RPC, bez hex dumpu
$ solana balance <ADRES>                  # tylko lamports, w SOL
```

<div className="listing"><strong>Listing 5-21.</strong> Bez <code>--url</code> CLI używa sieci z konfiguracji; <code>solana config get</code> pokazuje, która to.</div>

## RPC

Pod spodem zarówno Explorer, jak i CLI wysyłają to samo zapytanie
`getAccountInfo`. Listing 5-22 pokazuje odpowiedź dla portfela — to
struktura z Listingu 5-1 przetłumaczona na JSON.

```bash
$ curl -s https://api.mainnet-beta.solana.com -X POST \
    -H 'content-type: application/json' \
    -d '{"jsonrpc":"2.0","id":1,"method":"getAccountInfo",
         "params":["5tzFkiKscXHK5ZXCGbXZxdw7gTjjD1mBwuoFbhUvuAi9",{"encoding":"base64"}]}'
{
  "result": {
    "context": { "slot": 447026248 },
    "value": {
      "data": ["", "base64"],
      "executable": false,
      "lamports": 1869363538369958,
      "owner": "11111111111111111111111111111111",
      "rentEpoch": 18446744073709551615,
      "space": 0
    }
  }
}
```

<div className="listing"><strong>Listing 5-22.</strong> Odpowiedź RPC skrócona do istotnych pól. <code>data</code> to pusty ciąg w base64, <code>space</code> to jego długość.</div>

`lamports` przyszło jako liczba całkowita, bez przecinka — SDK i portfele
dzielą przez 10⁹ dopiero przy wyświetlaniu. `slot` w `context` mówi, z
którego momentu łańcucha pochodzi odpowiedź; dwa zapytania sekundę po
sobie mogą zwrócić inne saldo i inny slot.

Dla konta tokena RPC umie zrobić to, co Explorer: zdekodować dane, jeśli
poprosić o `"encoding": "jsonParsed"`. Listing 5-23 pokazuje wynik.

```json
"value": {
  "data": {
    "parsed": {
      "info": {
        "mint":  "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
        "owner": "5tzFkiKscXHK5ZXCGbXZxdw7gTjjD1mBwuoFbhUvuAi9",
        "state": "initialized",
        "tokenAmount": { "amount": "1942770513897", "decimals": 6,
                         "uiAmountString": "1942770.513897" }
      },
      "type": "account"
    },
    "program": "spl-token",
    "space": 165
  },
  "executable": false,
  "lamports": 2040003,
  "owner": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA",
  "rentEpoch": 18446744073709551615,
  "space": 165
}
```

<div className="listing"><strong>Listing 5-23.</strong> To samo konto z <code>jsonParsed</code>: RPC rozpoznał Token Program i zdekodował 165 bajtów do pól.</div>

Ten listing jest najlepszą ilustracją pułapki z rozdziału
[Własność](./02-wlasnosc.md): słowo `owner` występuje **dwa razy** i znaczy
dwie różne rzeczy. Zewnętrzny `owner` (`Tokenkeg…`) to pole konta —
program, który ma prawo zapisu. Wewnętrzny `owner` w `parsed.info`
(`5tzF…`) to pole *w danych* — użytkownik, którego podpis Token Program
wymaga przy przelewie. Saldo USDC (`amount`) leży w danych, a `lamports`
to tylko depozyt za miejsce.

:::note Dwa salda, dwa ownery
Konto tokena ma saldo w SOL (`lamports`, depozyt) i saldo w tokenie
(`amount`, w danych). Ma właściciela-program (`owner` konta) i
posiadacza-użytkownika (`owner` w danych). Przy czytaniu odpowiedzi RPC
warto zawsze sprawdzić, na którym poziomie zagnieżdżenia jest pole.
:::

## Podgląd własnych kont

Po wdrożeniu programu z rozdziału
[Transakcje i Anchor](../06-transakcje-i-anchor/index.md) te same
narzędzia pokażą jego konta. Kilka rzeczy, których warto szukać:

- `Assigned Program Id` konta licznika równy adresowi programu — to reguła
  właściciela w praktyce;
- pierwsze 8 bajtów `data` identyczne dla wszystkich kont tego samego typu
  — dyskryminator;
- `Balance` konta równy dokładnie wynikowi `solana rent <rozmiar>` — depozyt
  bez nadwyżki;
- adres konta zgodny z `solana find-program-derived-address` dla seedów
  z kodu — PDA.

Gdy któraś z tych obserwacji się nie zgadza, program robi coś innego, niż
autor sądzi — i to zwykle najszybszy sposób, żeby to zauważyć.
