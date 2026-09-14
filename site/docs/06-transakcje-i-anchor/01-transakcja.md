---
title: Transakcja
description: Instrukcja jako trójka (program, konta, dane), transakcja jako koperta z podpisami i opłatą, atomowość wykonania — rozebrane na prawdziwym przelewie i prawdziwym cofnięciu.
sidebar_position: 1
slug: transakcja
---

# Transakcja

Klik w przycisk „wymień" wysyła coś do sieci. Rozdział [Read vs
Write](../02-web3/03-read-vs-write.md) nazwał to „coś" transakcją i
pokazał jej koszty: podpis, opłatę, czas. Ten rozdział otwiera kopertę.
Węzeł nie ufa frontendowi, więc wszystko, co w niej jest, musi mieć
formę, którą da się sprawdzić bajt po bajcie — i ta forma jest
zaskakująco prosta.

## Instrukcja

Najmniejsza jednostka pracy na Solanie to **instrukcja**: pojedyncze
wywołanie jednego programu. Instrukcja składa się z dokładnie trzech
rzeczy:

1. **program** — adres kodu, który ma zostać wykonany;
2. **konta** — lista adresów, na których program będzie pracował, z
   flagami: czy konto jest zapisywalne i czy jego klucz podpisał;
3. **dane** — ciąg bajtów z argumentami, który program interpretuje po
   swojemu.

Nic więcej. Program nie może sięgnąć po konto, którego nie ma na liście
— to reguła z rozdziału [Anatomia konta](../05-konta/01-anatomia-konta.md),
dzięki której runtime wie z góry, co instrukcja dotknie. Listing 6-1
pokazuje instrukcję przelewu z Listingu 2-4, tym razem z rozkodowanymi
danymi.

```json
"accountKeys": [
  "8xHTGZeWbr2SmN38A6DahxJyY2vUqri1yKMqkN9spzjj",
  "HDT6d92i8AJQet2Z2MuagpVBzFsVswS9YneEQMzcypDK",
  "11111111111111111111111111111111"
],
"instructions": [
  { "programIdIndex": 2, "accounts": [0, 1], "data": "3Bxs411Dtc7pkFQj" }
]
```

```text
data (base58 → hex):  02 00 00 00   00 e1 f5 05 00 00 00 00
                      └─ u32: 2 ─┘   └─── u64: 100 000 000 ───┘
                      (Transfer)      (lamportów)
```

<div className="listing"><strong>Listing 6-1.</strong> Instrukcja przelewu: program pod indeksem 2 (System Program), konta 0 i 1 (nadawca, odbiorca), 12 bajtów danych — numer operacji i kwota.</div>

Trzy elementy są widoczne. `programIdIndex: 2` wskazuje na trzeci wpis w
`accountKeys` — System Program. `accounts: [0, 1]` to nadawca i odbiorca,
też jako indeksy do tej samej listy; transakcja trzyma każdy adres raz, a
instrukcje odwołują się do niego numerem. `data` to 12 bajtów: pierwsze
cztery to numer operacji w System Programie (2 oznacza *Transfer*),
kolejne osiem to kwota jako `u64` zapisany od najmniej znaczącego bajtu —
`00 e1 f5 05` czytane od tyłu to `0x05f5e100`, czyli 100 000 000. Jak z
bajtów robi się argumenty w Anchorze, wyjaśnia rozdział
[Serializacja i IDL](./04-serializacja-i-idl.md).

## Transakcja

**Transakcja** to koperta z jedną lub kilkoma instrukcjami. Oprócz nich
niesie trzy rzeczy, których instrukcja sama nie ma:

- **listę podpisów** — po jednym dla każdego konta, które w którejkolwiek
  instrukcji jest oznaczone jako signer; pierwszy podpisujący jest
  zawsze **płatnikiem opłaty**;
- **ostatni blockhash** — hash niedawnego bloku, po którym sieć poznaje,
  że transakcja jest świeża; transakcja z blockhashem starszym niż około
  minutę jest odrzucana, co uniemożliwia wysłanie tej samej koperty
  ponownie;
- **opłatę** — pobieraną od płatnika niezależnie od wyniku, 5 000
  lamportów za każdy podpis.

W Listingu 2-4 wszystkie trzy są widoczne: `signatures` z jednym
podpisem, `recentBlockhash` i `meta.fee: 5000`. Odczyt nie potrzebuje
koperty — węzeł odpowiada z własnej kopii. Każdy zapis, bez wyjątku,
potrzebuje.

:::note Transakcja
Lista instrukcji + lista podpisów + ostatni blockhash. Jedyna forma, w
jakiej stan Solany może się zmienić. Instrukcja to trójka (program,
konta, dane); transakcja to koperta, która niesie jedną lub więcej takich
trójek do klastra.
:::

Kilka instrukcji w jednej kopercie to nie wyjątek, tylko norma.
Frontend, który chce założyć konto tokena i od razu na nie przelać,
wysyła jedną transakcję z dwiema instrukcjami. Agregator z Listingu 3-2
wysyła jedną transakcję z wywołaniami czterech pul. Instrukcje wykonują
się po kolei, w kolejności z listy — i tu pojawia się własność, która
odróżnia transakcję od zwykłej listy żądań HTTP.

## Atomowość

Transakcja wykonuje się **w całości albo wcale**. Jeśli którakolwiek
instrukcja zwróci błąd, runtime cofa wszystkie zmiany wykonane przez
wcześniejsze instrukcje tej samej transakcji, a stan sieci po niej jest
identyczny jak przed. Nie ma „połowy operacji". To jest **atomowość**.

Listing 6-2 pokazuje cofnięcie w praktyce. Instrukcja `increment` z
programu licznika została wysłana przez kogoś, kto nie jest właścicielem
licznika; jedno ze sprawdzeń Anchora nie przeszło.

```text
Program 6hqBGkDSZTaF5cFshxX1pZPJkM3QAtEHFuWc2VxKdBmY invoke [1]
Program log: Instruction: Increment
Program log: AnchorError caused by account: counter. Error Code: ConstraintSeeds. Error Number: 2006. Error Message: A seeds constraint was violated.
Program log: Left:
Program log: GmCfULKZrQZV94FFAYAqgaUayBrbwiD7v2mY5ckbfHVu
Program log: Right:
Program log: HqPkdQCVfA1CWYWYfJWtCy9iLzd2Ni5S4PAeR6hihGKY
Program 6hqBGkDSZTaF5cFshxX1pZPJkM3QAtEHFuWc2VxKdBmY consumed 5068 of 200000 compute units
Program 6hqBGkDSZTaF5cFshxX1pZPJkM3QAtEHFuWc2VxKdBmY failed: custom program error: 0x7d6
```

<div className="listing"><strong>Listing 6-2.</strong> Instrukcja odrzucona przez constraint. Ostatnia linia — <code>failed</code> — oznacza, że runtime cofnął całą transakcję; licznik ma tę samą wartość co przed nią.</div>

Wszystko, co program zdążył zrobić do momentu błędu, znika: zapisane
bajty, przelane lamporty, założone konta. Co *nie* znika, to opłata —
walidator wykonał pracę i została ona opłacona, a informacja o
nieudanej transakcji trafia do łańcucha jako historia. Dlatego frontend
symuluje transakcję na węźle RPC przed wysłaniem: symulacja jest
odczytem, więc jest darmowa, a pokazuje ten sam log, co Listing 6-2.

:::tip Swap i przelew w jednej transakcji
Instrukcja 1 wymienia SOL na USDC w puli; instrukcja 2 przelewa USDC do
znajomego. Jeśli przelew się nie uda — bo znajomy nie ma konta USDC —
wymiana też się cofa. Użytkownik nie zostaje z USDC, których nie chciał
mieć. W Web2 taki scenariusz wymaga transakcji bazodanowej *i*
mechanizmu kompensacji, jeśli druga usługa jest zewnętrzna; tutaj jest
wbudowany w koperty.
:::

Runtime sprawdza podpisy i egzekwuje atomowość. Ale to, czy konto na
liście jest tym, za które się podaje — czy `counter` to naprawdę licznik
tego użytkownika, a nie podstawione konto o podobnym układzie — musi
sprawdzić sam program. W Listingu 6-2 zrobił to Anchor, z deklaracji.
Następny rozdział wyjaśnia, ile pracy oszczędza.
