---
title: Pierwsza transakcja
description: Transfer SOL na devnecie i jego ślad — w terminalu przez solana confirm, w Explorerze przez podpis — plus transakcja, która nie przeszła, i konto odczytane wprost z łańcucha.
sidebar_position: 4
slug: pierwsza-transakcja
---

# Pierwsza transakcja

Dowolny przelew między dwoma adresami na devnecie to ten sam **write**,
który opisuje rozdział [Read vs Write](../02-web3/03-read-vs-write.md):
podpisany, opłacony, atomowy. Ten rozdział wykonuje taki przelew, a
potem ogląda go z dwóch stron — w terminalu i w Explorerze — żeby każde
pojęcie z kursu miało swoje miejsce na ekranie.

## Przelew

Listing 7-6 przelewa 0,1 SOL z portfela CLI na adres z pliku `demo.json` z
Listingu 7-2, a następnie prosi sieć o pełny opis tego, co się stało.

```bash
$ solana transfer HDT6d92i8AJQet2Z2MuagpVBzFsVswS9YneEQMzcypDK 0.1 \
    --allow-unfunded-recipient --url devnet

Signature: 5GGpYdKDUdyEKgkesy4tLTHjy17UcoLHrjSip15fBx51r1xEcPf7Z1ayGBgL9vcP58TUoaheWefLhg3KLFxsFjVS

$ solana confirm -v 5GGpYdKDUdyEKgkesy4tLTHjy17UcoLHrjSip15fBx51r1xEcPf7Z1ayGBgL9vcP58TUoaheWefLhg3KLFxsFjVS --url devnet
Transaction executed in slot 498340046:
  Block Time: 2026-09-14T19:02:06+02:00
  Version: legacy
  Recent Blockhash: 3wZPMuF6WsMJLjc3XH2shoasnFitpQDZpks8JiSAgmqM
  Signature 0: 5GGpYdKDUdyEKgkesy4tLTHjy17UcoLHrjSip15fBx51r1xEcPf7Z1ayGBgL9vcP58TUoaheWefLhg3KLFxsFjVS
  Account 0: srw- 8xHTGZeWbr2SmN38A6DahxJyY2vUqri1yKMqkN9spzjj (fee payer)
  Account 1: -rw- HDT6d92i8AJQet2Z2MuagpVBzFsVswS9YneEQMzcypDK
  Account 2: -r-x 11111111111111111111111111111111
  Instruction 0
    Program:   11111111111111111111111111111111 (2)
    Account 0: 8xHTGZeWbr2SmN38A6DahxJyY2vUqri1yKMqkN9spzjj (0)
    Account 1: HDT6d92i8AJQet2Z2MuagpVBzFsVswS9YneEQMzcypDK (1)
    Transfer { lamports: 100000000 }
  Status: Ok
    Fee: ◎0.000005
    Account 0 balance: ◎5.826829074 -> ◎5.726824074
    Account 1 balance: ◎0 -> ◎0.1
    Account 2 balance: ◎0.000000001
  Compute Units Consumed: 150
  Log Messages:
    Program 11111111111111111111111111111111 invoke [1]
    Program 11111111111111111111111111111111 success

Finalized
```

<div className="listing"><strong>Listing 7-6.</strong> Przelew i jego pełny opis. Flaga <code>--allow-unfunded-recipient</code> jest potrzebna, bo odbiorca nie istniał jeszcze na łańcuchu — pierwszy przelew go tworzy.</div>

Ten jeden wynik zbiera prawie cały kurs. Od góry:

- **`slot 498340046`** i **`Block Time`** — kiedy transakcja weszła do
  bloku; zapis dzieje się w chwili zatwierdzenia, nie wysłania.
- **`Recent Blockhash`** — hash niedawnego bloku, po którym sieć uznaje
  transakcję za świeżą (rozdział [Transakcja](../06-transakcje-i-anchor/01-transakcja.md)).
- **`Signature 0`** — jeden podpis, ten sam ciąg, który wypisało
  `transfer`; jest jednocześnie identyfikatorem transakcji.
- **Trzy konta z flagami.** `srw-` przy koncie 0 to *signer, readable,
  writable* — nadawca podpisał i zostanie zmieniony. `-rw-` przy koncie 1
  — odbiorca zmieniony, ale nie podpisywał: dodawać lamporty wolno bez
  zgody (rozdział [Własność](../05-konta/02-wlasnosc.md)). `-r-x` przy
  koncie 2 — System Program: tylko odczyt, *executable*.
- **`Instruction 0`** — jedna instrukcja: program System, dwa konta,
  dane rozkodowane jako `Transfer { lamports: 100000000 }`. To trójka z
  Listingu 6-1, tym razem odczytana przez CLI.
- **`Fee: ◎0.000005`** — 5 000 lamportów, opłata bazowa za jeden podpis,
  o której mówił rozdział [Dlaczego Solana?](../01-blockchain/04-dlaczego-solana.md).
- **Salda przed i po.** Nadawca stracił 0,100005 SOL — przelew plus
  opłata. Odbiorca zyskał 0,1. System Program ma 1 lamport i nie zmienił
  się.
- **`Compute Units Consumed: 150`** — koszt obliczeniowy najprostszej
  operacji w sieci; `increment` z Listingu 4-15 kosztował 3 991.
- **`Log Messages`** — `invoke` i `success`, bez `Program log:`, bo System
  Program nie używa `msg!`.
- **`Finalized`** — najwyższy poziom potwierdzenia; transakcja jest
  nieodwołalna.

<div className="diagram narrow">

![Portfel wysyła transakcję do walidatorów; Explorer odczytuje jej ślad z łańcucha](/img/diagrams/7_wallet-04.svg)

</div>

## Transakcja, która nie przeszła

Listing 7-7 pokazuje, co się dzieje, gdy nowy portfel — z 0,1 SOL —
próbuje wysłać 5 SOL.

```bash
$ solana transfer 8xHTGZeWbr2SmN38A6DahxJyY2vUqri1yKMqkN9spzjj 5 \
    --keypair demo.json --url devnet
Error: Account HDT6d92i8AJQet2Z2MuagpVBzFsVswS9YneEQMzcypDK has insufficient funds for spend (5 SOL) + fee (0.000005 SOL)
```

<div className="listing"><strong>Listing 7-7.</strong> Odmowa przed wysłaniem. CLI sprawdziło saldo odczytem i nie wysłało transakcji, więc nie ma ani podpisu, ani opłaty.</div>

Warto zauważyć, *gdzie* ta odmowa nastąpiła. CLI zrobiło odczyt salda —
darmowy, bez podpisu — i porównało z kwotą plus opłatą, zanim cokolwiek
podpisało. Nie ma podpisu, więc nie ma identyfikatora; nie ma wpisu w
łańcuchu, bo nic do niego nie trafiło. Gdyby CLI tego nie sprawdziło,
transakcja zostałaby odrzucona przez sieć z tym samym powodem — ale
wtedy jako nieudana transakcja w historii, z pobraną opłatą. Frontendy
robią to samo sprawdzenie symulacją.

## Explorer

`solana confirm -v` pokazuje w terminalu to, co **Solana Explorer**
pokazuje w przeglądarce. Po otwarciu `explorer.solana.com`, przełączeniu
sieci na *Devnet* w prawym górnym rogu i wklejeniu podpisu z Listingu 7-6
w pole wyszukiwania, strona wyświetla tę samą transakcję.

<div className="diagram screenshot">

![Szczegóły transakcji w explorer.solana.com na sieci Devnet: podpis, status, slot, opłata, lista kont i instrukcja Transfer](/img/explorer-tx-devnet-crop.png)

</div>

Układ jest ten sam, co w listingu: sekcja *Overview* z podpisem, statusem,
slotem, czasem i opłatą; *Account Input(s)* z listą kont i zmianami sald;
*Instruction(s)* z programem i rozkodowanymi danymi; *Program Logs* na
dole. Explorer robi jedną rzecz więcej — każdy adres jest linkiem, więc
kliknięcie w konto 1 prowadzi do jego strony.

:::tip Co widać w Explorerze
Podpis jako identyfikator, status i numer slotu, opłatę sieciową, listę
kont ze zmianami sald i rozkodowaną instrukcję. Wszystko to jest odczytem
z węzła RPC — Explorer nie ma własnej bazy, tylko ładniejszy interfejs
do tego samego `getTransaction`, które Listing 2-4 wywołał przez `curl`.
:::

## Explorer jako podgląd konta

Strona konta w Explorerze pokazuje pola z rozdziału [Anatomia
konta](../05-konta/01-anatomia-konta.md) na żywo, bez własnego węzła.
Listing 7-8 odczytuje to samo konto — odbiorcę z Listingu 7-6, po tym,
jak odesłał 0,01 SOL z powrotem — z terminala.

```bash
$ solana account HDT6d92i8AJQet2Z2MuagpVBzFsVswS9YneEQMzcypDK --url devnet

Public Key: HDT6d92i8AJQet2Z2MuagpVBzFsVswS9YneEQMzcypDK
Balance: 0.089995 SOL
Owner: 11111111111111111111111111111111
Executable: false
Rent Epoch: 18446744073709551615
```

<div className="listing"><strong>Listing 7-8.</strong> Konto, które godzinę wcześniej nie istniało. Saldo 0,1 − 0,01 − 0,000005; właścicielem jest System Program; danych brak — to portfel.</div>

Każde pole ma swoje miejsce w kursie. `Balance` to `lamports` po dwóch
transakcjach — przychodzącej i wychodzącej z opłatą. `Owner` to System
Program: tylko on może odjąć lamporty z tego konta, i zrobi to
wyłącznie za podpisem klucza z `demo.json`. `Executable: false` — konto
danych, nie program. Brak sekcji z bajtami — portfel nie ma `data`. W
Explorerze te same pola nazywają się *Balance*, *Assigned Program Id*,
*Executable* i *Allocated Data Size*, a rozdział [Konta w
praktyce](../05-konta/05-w-praktyce.md) pokazuje pełną mapę nazw i to samo
konto odczytane przez RPC.

:::tip Demo — Solana Explorer
Otwórz stronę własnego portfela z Phantoma w Explorerze (sieć: Devnet).
Odczytaj *Balance* i porównaj z rozszerzeniem; odczytaj *Assigned
Program Id* i sprawdź, że to `1111…`; przewiń do *Transaction History* i
znajdź airdrop z poprzedniego rozdziału. To trzy odczyty z jednego węzła
RPC — i cały stan konta, jaki istnieje.
:::

To zamyka kurs w wersji nagrywanej. Portfel istnieje, ma środki na sieci
testowej, wysłał transakcję i da się ją zobaczyć w sieci — z tym samym
podpisem, opłatą, instrukcją i kontami, które sześć wcześniejszych
tematów opisywało z osobna. Na sesji live ten sam portfel wdroży program
z rozdziału [Mini-program](../06-transakcje-i-anchor/05-mini-program.md).
