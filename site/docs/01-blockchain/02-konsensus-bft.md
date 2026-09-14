---
title: Sieci z konsensusem BFT
description: Setki niezależnych węzłów, wspólny stan, głosowanie zamiast właściciela — i rejestr, w którym każdy blok jest przypięty do poprzedniego hashem.
sidebar_position: 2
slug: konsensus-bft
---

# Sieci z konsensusem BFT

Poprzedni rozdział zakończył się pytaniem: czy saldo może istnieć bez
serwera, na którym leży? Odpowiedź jest przewrotna — saldo nadal leży na
serwerach, tylko nie na jednym i nie należących do jednej firmy. Ten
rozdział opisuje, jak wiele niezależnych komputerów utrzymuje jeden
wspólny stan i dlaczego żaden z nich nie może go samodzielnie zmienić.

## Wspólna sieć

Skoro problemem jest jeden właściciel, rozwiązaniem jest brak
właściciela. Zamiast jednej bazy danych w jednej firmie, ten sam stan —
wszystkie salda, wszystkie dane, cała historia — przechowuje **wiele
niezależnych węzłów**: komputerów prowadzonych przez różne osoby i
organizacje w różnych krajach, które nie muszą sobie ufać ani nawet się
znać.

Każdy węzeł ma pełną kopię stanu. Gdy ktoś chce ten stan zmienić — na
przykład przelać pieniądze — nie wystarczy przekonać jednego węzła. Zmiana
trafia do wszystkich, a każdy z nich niezależnie sprawdza, czy jest
poprawna: czy nadawca ma środki, czy podpis się zgadza, czy operacja nie
łamie reguł. Zmiana wchodzi w życie dopiero wtedy, gdy zgodzi się na nią
**większość sieci**.

Co z węzłem, który kłamie — twierdzi, że widział przelew, którego nie
było, albo odmawia uznania prawidłowej operacji? Zostaje **przegłosowany**.
Jego wersja stanu różni się od wersji pozostałych, więc reszta sieci ją
ignoruje. Żeby sfałszować stan, trzeba by kontrolować większość węzłów
naraz — a te należą do różnych, niezależnych podmiotów. Sieć, która
działa poprawnie mimo pewnej liczby nieszczerych lub zepsutych
uczestników, ma własność zwaną **Byzantine Fault Tolerance (BFT)**.

:::note Byzantine Fault Tolerance
Nazwa pochodzi od problemu bizantyjskich generałów: kilku dowódców musi
uzgodnić wspólny plan, komunikując się przez posłańców, choć część z nich
może być zdrajcami. Protokół BFT gwarantuje, że uczciwa większość dojdzie
do tej samej decyzji niezależnie od tego, co robią zdrajcy — o ile
zdrajców jest mniej niż jedna trzecia.
:::

Na Solanie węzły, które głosują nad stanem, nazywają się **walidatorami**.
Listing 1-1 pokazuje ich liczbę w chwili pisania, odczytaną jednym
poleceniem z sieci głównej.

```bash
$ solana validators --url mainnet-beta
...
Average Stake-Weighted Skip Rate: 0.08%
Average Unweighted Skip Rate:     0.33%
Active Stake: 438740367.085071862 SOL
Stake By Version:
4.2.2   -  523 current validators (72.16%)   2 delinquent validators ( 0.00%)
4.2.1   -   33 current validators ( 5.11%)   3 delinquent validators ( 0.03%)
...
```

<div className="listing"><strong>Listing 1-1.</strong> Podsumowanie polecenia <code>solana validators</code> (lista skrócona). W chwili pisania głosuje 690 walidatorów; obok nich działają tysiące węzłów, które nie głosują, ale trzymają kopię stanu i odpowiadają na zapytania.</div>

Dwie liczby z tego wyniku warto zapamiętać. Pierwsza to liczba walidatorów
— kilkaset niezależnych organizacji, z których żadna nie ma większości.
Druga to *Active Stake*: 438 milionów SOL, które walidatorzy zablokowali
jako zabezpieczenie. Głos walidatora waży tyle, ile ma zablokowanych
środków — a większość z nich to środki innych osób, które je walidatorowi
powierzyły i mogą w każdej chwili zabrać. Walidator, który głosuje
nieuczciwie, traci nagrody, reputację i delegacje, z których żyje.
Nieuczciwość nie jest więc darmowa — kosztuje więcej, niż da się na niej
zarobić.

:::tip Efekt
Kod uruchomiony w takiej sieci wykona się **dokładnie tak, jak został
napisany**. Nie dlatego, że ktoś tego pilnuje, ale dlatego, że nikt nie
ma władzy, żeby wykonać go inaczej — żaden pojedynczy podmiot nie może
zmienić wyniku, którego nie potwierdzi większość.
:::

## Rejestr BFT

Sama większość nie wystarczy. Gdyby węzły uzgadniały tylko *aktualny*
stan, ktoś mógłby po cichu przepisać historię: zmienić wczorajszy przelew
tak, żeby dzisiejsze saldo wyglądało na uczciwe. Potrzebny jest rejestr,
w którym zmiana przeszłości jest natychmiast widoczna.

Rejestr składa się z **bloków**. Blok to paczka operacji zatwierdzonych w
jednym kroku, a każdy blok zawiera **hash** poprzedniego — skrót
kryptograficzny jego zawartości. Hash ma dwie własności, na których opiera
się cały mechanizm: zmiana choćby jednego bajtu na wejściu daje zupełnie
inny wynik, a z wyniku nie da się odtworzyć wejścia. Skoro blok N zawiera
hash bloku N−1, a blok N+1 zawiera hash bloku N, to zmiana czegokolwiek w
bloku N−1 unieważnia hashe we wszystkich blokach po nim. Podrobić
historię znaczy przepisać cały łańcuch od zmienionego miejsca do dziś — i
przekonać do tej wersji większość sieci. Stąd nazwa: **blockchain**,
łańcuch bloków.

Listing 1-2 pokazuje dwa kolejne bloki z sieci głównej, odczytane przez
API węzła.

```bash
$ curl -s https://api.mainnet-beta.solana.com -X POST \
    -H 'content-type: application/json' \
    -d '{"jsonrpc":"2.0","id":1,"method":"getBlock",
         "params":[447028670,{"transactionDetails":"none","rewards":false}]}'
{
  "result": {
    "blockHeight": 425071081,
    "blockTime": 1789405354,
    "blockhash": "CmrZr53VSsdHShCmC8YDyeVGvGdd8ZkGEPVe68Dgso6W",
    "parentSlot": 447028669,
    "previousBlockhash": "FDMVAL3z3Dhy4VJLrcyXwo3QnMSBLiayD6MNcXFJaN8n"
  }
}

$ curl -s https://api.mainnet-beta.solana.com -X POST \
    -H 'content-type: application/json' \
    -d '{"jsonrpc":"2.0","id":1,"method":"getBlock",
         "params":[447028671,{"transactionDetails":"none","rewards":false}]}'
{
  "result": {
    "blockHeight": 425071082,
    "blockTime": 1789405354,
    "blockhash": "ArJC7KfrF9EXcNAcqbMVLTPDF1VN561WYXL5oSGvjx6S",
    "parentSlot": 447028670,
    "previousBlockhash": "CmrZr53VSsdHShCmC8YDyeVGvGdd8ZkGEPVe68Dgso6W"
  }
}
```

<div className="listing"><strong>Listing 1-2.</strong> Dwa sąsiednie bloki (lista transakcji pominięta). <code>previousBlockhash</code> drugiego bloku to <code>blockhash</code> pierwszego — to jest ogniwo łańcucha.</div>

Warto prześledzić pola. `blockhash` pierwszego bloku to
`CmrZr53V…`; drugi blok ma dokładnie tę wartość w polu
`previousBlockhash`. Gdyby ktoś zmienił choć jedną transakcję w bloku
447028670, jego hash przestałby się zgadzać z tym, co zapisano w bloku
447028671 — i w każdym z milionów bloków, które przyszły później.
`blockTime` obu bloków jest ten sam, bo Solana produkuje bloki szybciej niż
raz na sekundę; o tym mówi rozdział [Dlaczego Solana?](./04-dlaczego-solana.md).
`parentSlot` i `blockHeight` to dwa sposoby numerowania: slot to numer
„miejsca w czasie", wysokość to liczba bloków, które faktycznie powstały.

Do łańcucha bloków dochodzą dwie reguły, które domykają rejestr:

- Stan sieci jest **publiczny**. Każdy może uruchomić węzeł, pobrać całą
  historię i samodzielnie sprawdzić, że dzisiejsze salda wynikają z
  wczorajszych operacji. Listing 1-2 wykonano bez żadnego konta ani
  uprawnień.
- Każda operacja jest **podpisana kluczem** właściciela. Nie da się
  wykonać przelewu z cudzego konta, bo nie da się złożyć cudzego podpisu
  — nawet będąc walidatorem. Jak działa ten podpis, wyjaśnia rozdział
  [Klucze](../07-portfel-i-narzedzia/01-klucze.md).

| | Prywatny serwer | Blockchain |
|---|---|---|
| Kto trzyma stan | jedna firma | setki niezależnych węzłów |
| Kto może go zmienić | operator, w dowolnej chwili | większość sieci, tylko zgodnie z regułami |
| Czy da się sprawdzić historię | nie — baza jest prywatna | tak — rejestr jest publiczny, a bloki powiązane hashem |
| Do czego jest zaufanie | do właściciela | do matematyki |

Ostatni wiersz tej tabeli to sedno. Blockchain nie usuwa zaufania — zamienia
zaufanie do *osoby* na zaufanie do *mechanizmu*, który każdy może
zweryfikować. Osoba może zmienić zdanie; hash nie.

:::tip Analogia — księga u notariusza
Klasyczny rejestr to zeszyt w szufladzie urzędnika: wpisy da się dopisać,
wyrwać kartkę, poprawić długopisem. Rejestr BFT to księga, której każda
strona zaczyna się od odcisku poprzedniej, a kopię trzyma kilkuset
notariuszy naraz. Żeby zmienić stronę sprzed roku, trzeba przepisać
wszystkie następne — w kilkuset egzemplarzach jednocześnie.
:::

Sieć umie więc uzgodnić stan i pilnować historii. Ale jak dotąd mowa
tylko o *saldach*. Następny rozdział pokazuje, co się dzieje, gdy do
takiej sieci wgra się nie liczbę, tylko **program**.
