---
title: Programy on-chain
description: Logika finansowa jako kod wgrany do sieci BFT — jawne warunki, automatyczna egzekucja, brak pośrednika, i co naprawdę oznacza „niezmienny".
sidebar_position: 3
slug: programy-on-chain
---

# Programy on-chain

Sieć BFT gwarantuje, że stan zmienia się tylko zgodnie z regułami, których
pilnuje większość. Poprzedni rozdział mówił o jednej regule: „przelew
wymaga podpisu nadawcy i wystarczających środków". Pytanie na ten
rozdział brzmi: co, jeśli reguły będą dowolne — jeśli do sieci da się
wgrać **kod**, a sieć będzie go wykonywać tak samo bezstronnie, jak
sprawdza podpisy?

## Kod zamiast instytucji

Prawie każda usługa finansowa to w gruncie rzeczy zestaw reguł plus ktoś,
kto ich pilnuje. Bank udziela pożyczki: reguła to „wypłać, jeśli
zabezpieczenie jest wystarczające; ściągnij, jeśli rata nie wpłynie".
Kantor wymienia waluty: reguła to „wydaj tyle B za tyle A, po dzisiejszym
kursie". Notariusz poświadcza umowę: reguła to „strony podpisały, więc
warunki obowiązują". W każdym przypadku reguła jest prosta, a instytucja
jest droga — bo instytucja to ludzie, budynki, licencje i zaufanie, które
trzeba było zbudować.

Program wgrany do sieci BFT zastępuje instytucję w jednej roli: jako
**wykonawcę reguł**. Reguły są zapisane w kodzie, kod jest publiczny, a
wykonują go wszystkie węzły niezależnie — z tym samym wynikiem, bo wynik
jest częścią stanu, na który sieć głosuje. Taki program nazywa się
**programem on-chain**; w innych ekosystemach mówi się *smart kontrakt*.
Oba słowa znaczą to samo: logika, która działa wewnątrz sieci, a nie na
serwerze firmy.

Trzy własności odróżniają program on-chain od backendu w Web2:

- **Warunki są jawne.** Kod jest publiczny i każdy może go przeczytać
  przed użyciem. Nie ma regulaminu, który różni się od implementacji.
- **Egzekucja jest automatyczna.** Gdy warunek jest spełniony, program
  wykonuje działanie sam. Nie ma działu reklamacji, który może odmówić,
  ani administratora, który może „wstrzymać do wyjaśnienia".
- **Dostęp jest permissionless** — bez dokumentów, bez zgody operatora,
  bez konta u pośrednika. Każdy, kto ma klucz i środki, może wywołać
  program. Program nie wie, kim jest wywołujący, i nie musi wiedzieć.

:::tip Przykłady
**Pożyczka.** Program trzyma pulę tokenów. Kto wpłaci zabezpieczenie o
wartości wyższej niż pożyczka, dostaje wypłatę natychmiast — bez oceny
zdolności kredytowej, bo program jej nie potrzebuje: gdy zabezpieczenie
straci na wartości, program sprzeda je i spłaci dług sam.

**Wymiana walut.** Program trzyma rezerwy dwóch tokenów i wzór, który z
proporcji rezerw wylicza cenę. Kto wpłaci jeden token, dostaje drugi po
tej cenie — bez brokera i bez godzin otwarcia.
:::

Oba przykłady rozwija rozdział [DeFi](../03-defi/index.md). Tutaj ważne
jest jedno: to nie są hipotezy. Programy, które to robią, działają na
sieci głównej od lat i obsługują miliardy dolarów.

## Program to też stan

W sieci BFT wszystko, co węzły uzgadniają, jest częścią stanu — program
też. Kod programu leży w sieci pod adresem, tak samo jak saldo, i podlega
tym samym regułom: jest publiczny, ma historię i nie da się go zmienić bez
zgody większości. Listing 1-3 pokazuje, jak wygląda jeden z najczęściej
używanych programów na Solanie odczytany z sieci.

```bash
$ solana program show JUP6LkbZbjS1jKKwapdHNy74zcZ3tLUZoi5QNyVTaV4 --url mainnet-beta
Program Id: JUP6LkbZbjS1jKKwapdHNy74zcZ3tLUZoi5QNyVTaV4
Owner: BPFLoaderUpgradeab1e11111111111111111111111
ProgramData Address: 4Ec7ZxZS6Sbdg5UGSLHbAnM7GQHp2eFd4KYWRexAipQT
Authority: CvQZZ23qYDWF2RUpxYJ8y9K4skmuvYEEjH7fK58jtipQ
Last Deployed In Slot: 445747349
Data Length: 2892224 (0x2c21c0) bytes
Balance: 18.317550201 SOL
```

<div className="listing"><strong>Listing 1-3.</strong> Agregator wymiany Jupiter: 2,9 MB skompilowanego kodu pod publicznym adresem. <code>Authority</code> to klucz, który może ten kod podmienić.</div>

Kilka pól zasługuje na uwagę. `Data Length` to rozmiar skompilowanego
programu — prawie trzy megabajty kodu, który każdy walidator ma u siebie
i wykonuje na żądanie. `Last Deployed In Slot` mówi, kiedy kod ostatnio
zmieniono; to informacja publiczna, więc użytkownik może sprawdzić, czy
program, z którego korzysta dziś, to ten sam, który audytowano miesiąc
temu. `Balance` to depozyt za miejsce, które kod zajmuje w sieci — o tym
w rozdziale [Koszt](../05-konta/04-koszt.md).

Najważniejsze jest pole `Authority`. To adres, który ma prawo wgrać nową
wersję programu. Dopóki jest ustawiony, autorzy mogą zmienić kod — a więc
i reguły, na które użytkownicy się zgodzili. „Niezmienność" programu
on-chain nie jest więc automatyczna; jest decyzją autorów, którzy mogą
zrzec się tego prawa na stałe. Wtedy w tym polu stoi `none`, jak w
przypadku programu obsługującego tokeny, pokazanego w [Anatomii
konta](../05-konta/01-anatomia-konta.md).

:::warning Kod publiczny to nie kod bezpieczny
Program on-chain wykona się dokładnie tak, jak napisany — również wtedy,
gdy jest napisany źle. Błąd w kodzie, który obsługuje pieniądze, jest
publiczny, powtarzalny i często nieodwracalny. Dlatego pisanie takich
programów wymaga języka i narzędzi, które eliminują całe klasy błędów
przed wdrożeniem; to temat rozdziału [Rust dla Anchora](../04-rust/index.md).
:::

:::tip Analogia — automat z napojami
Automat to reguły zamknięte w maszynie: wrzuć monetę, wybierz numer,
odbierz napój. Nie ma sprzedawcy, który może odmówić, ani menedżera, który
zmieni cenę w trakcie transakcji. Program on-chain to automat, którego
mechanizm każdy może obejrzeć, i którego nie da się przestawić bez
wiedzy wszystkich klientów.
:::

Sieć BFT z programami on-chain to kompletna odpowiedź na problem z
pierwszego rozdziału: saldo bez właściciela, reguły bez instytucji. Ale
odpowiedź teoretyczna. Żeby program mógł zastąpić kantor, musi wykonać
wymianę w sekundę, a nie w minutę, i za grosze, a nie za dolary. Nie
każda sieć to potrafi — i o tym jest ostatni rozdział.
