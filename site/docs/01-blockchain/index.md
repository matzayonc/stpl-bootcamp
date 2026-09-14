---
title: Blockchain i Solana
description: Dlaczego finanse potrzebują sieci BFT, co daje program on-chain i dlaczego platformą bootcampu jest Solana — z liczbami zmierzonymi na sieci głównej.
sidebar_position: 0
---

# Blockchain i Solana

Jedno pytanie organizuje ten temat: **komu trzeba ufać, żeby saldo było
prawdziwe?** W Web2 odpowiedź brzmi „firmie, która trzyma bazę". Cały
blockchain to próba zmiany tej odpowiedzi na „nikomu konkretnemu" — i
cała Solana to próba zrobienia tego w skali, w której zmiana ma
praktyczne znaczenie. Kto zrozumie, po co istnieje sieć BFT i co w niej
robi program, ten wie, po co jest reszta kursu.

Rozdział rozwija slajdy *Dlaczego blockchain i Solana?*
([PDF](https://github.com/matzayonc/stpl-slides/releases/download/latest/0_why.pdf))
o rzeczy, na które na wykładzie nie ma miejsca: liczbę walidatorów i
stawkę zabezpieczenia odczytane z sieci, dwa sąsiednie bloki z widocznym
ogniwem hasha, metadane prawdziwego programu on-chain i czas slotu
zmierzony zamiast zacytowany.

## Zawartość

1. [Problem z prywatnymi serwerami](./01-prywatne-serwery.md) — dane,
   pieniądze i historia na serwerze firmy; co widać, czego nie da się
   sprawdzić; problem zaufania.
2. [Sieci z konsensusem BFT](./02-konsensus-bft.md) — wspólny stan w
   setkach węzłów, przegłosowany kłamca, **BFT**, łańcuch bloków
   powiązanych hashem, rejestr publiczny i podpisany.
3. [Programy on-chain](./03-programy-on-chain.md) — kod zamiast
   instytucji, jawne warunki, permissionless, program jako część stanu i
   co naprawdę znaczy `Authority`.
4. [Dlaczego Solana?](./04-dlaczego-solana.md) — czego brakuje Bitcoinowi
   i Ethereum, czas slotu i przepustowość zmierzone z RPC, opłata bazowa,
   **PoH** i **Sealevel**.

Pytania sprawdzające do rozdziału: [Blockchain i Solana — pytania
kontrolne](../08-pytania-kontrolne/00-blockchain-i-solana.md).

## Podsumowanie

Klasyczna aplikacja finansowa trzyma dane, pieniądze i historię na
serwerze jednej firmy. Użytkownik widzi działający interfejs i
zgadzające się saldo, ale nie ma sposobu sprawdzić, czy dane nie zostały
zmienione, czy środki istnieją i co będzie jutro. To **problem zaufania**:
nie w tym, że firma kłamie, ale w tym, że nie da się tego zweryfikować.

Sieć BFT usuwa właściciela zamiast go kontrolować. Ten sam stan trzymają
setki niezależnych walidatorów — 690 w chwili pisania — a zmiana wchodzi w
życie, gdy zgodzi się większość; nieszczery węzeł zostaje przegłosowany i
traci nagrody oraz powierzone mu środki. Historia jest ułożona w **łańcuch
bloków**, z których każdy niesie hash poprzedniego, więc zmiana przeszłości
unieważnia wszystko, co przyszło po niej. Stan jest publiczny, a każda
operacja podpisana kluczem właściciela. Zaufanie do osoby zamienia się w
zaufanie do matematyki.

Do takiej sieci da się wgrać nie tylko salda, ale i **program on-chain**:
kod, który wszystkie węzły wykonują niezależnie i z tym samym wynikiem.
Program zastępuje instytucję jako wykonawcę reguł — warunki są jawne,
egzekucja automatyczna, dostęp permissionless. Program sam jest częścią
stanu: ma adres, rozmiar, historię wdrożeń i klucz `Authority`, który może
go zmienić, dopóki autorzy się go nie zrzekną.

Program on-chain ma sens tylko w sieci, która wykonuje go szybko i tanio.
Bitcoin nie ma programów; Ethereum ma, ale kilkanaście transakcji na
sekundę i opłaty rosnące z obciążeniem zepchnęły ruch na warstwy drugie,
które fragmentują stan. Solana jest jedną warstwą: slot trwa około 315 ms
(400 ms projektowo), blok mieści ponad tysiąc transakcji, opłata bazowa to
stałe 5 000 lamportów. Stoją za tym **Proof of History** — zegar wpisany w
ciąg hashy, który udowadnia kolejność bez negocjacji — i **Sealevel**,
który wykonuje równolegle transakcje dotykające różnych kont.

:::tip Analogia na koniec
Saldo w banku to komórka w cudzym arkuszu; rejestr BFT to księga, której
każda strona zaczyna się od odcisku poprzedniej, trzymana przez kilkuset
notariuszy naraz; program on-chain to automat z napojami, którego
mechanizm każdy może obejrzeć; a Solana to supermarket, w którym klienci
z różnymi listami zakupów idą do różnych kas jednocześnie.
:::

## Ćwiczenia

Ćwiczenia wymagają tylko przeglądarki i `curl`; zainstalowane Solana CLI
(rozdział [Portfel i narzędzia](../07-portfel-i-narzedzia/index.md))
ułatwia pierwsze dwa, ale nie jest konieczne.

1. **Zmierz slot.** Odczytaj `getSlot` z publicznego RPC, odczekaj
   dokładnie 60 sekund i odczytaj ponownie. Policz czas slotu i porównaj z
   Listingiem 1-4. Następnie odczytaj `getBlockTime` dla obu slotów i
   sprawdź, czy różnica czasów zgadza się z odmierzonymi 60 sekundami.

2. **Znajdź ogniwo.** Wybierz dowolny slot z ostatniej godziny i pobierz
   `getBlock` dla niego oraz dla `parentSlot` z odpowiedzi
   (`transactionDetails: "none"`). Zapisz, które pole w bloku późniejszym
   równa się któremu polu w bloku wcześniejszym. Co się stanie z tą
   równością, gdyby ktoś zmienił jedną transakcję w bloku wcześniejszym?

3. **Kto może zmienić program?** Dla trzech programów — Jupiter
   (`JUP6LkbZbjS1jKKwapdHNy74zcZ3tLUZoi5QNyVTaV4`), Token Program
   (`TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA`) i System Program
   (`11111111111111111111111111111111`) — odczytaj `solana program show`
   albo stronę w Explorerze i zapisz wartość `Authority`. Wyjaśnij jednym
   zdaniem dla każdego, kto i pod jakim warunkiem może zmienić jego kod.
   Dlaczego dla System Programu polecenie zwraca błąd?

4. **Trzy listy.** Wybierz aplikację finansową, z której korzystasz na co
   dzień, i wypisz dla niej trzy listy z rozdziału o [prywatnych
   serwerach](./01-prywatne-serwery.md): co widać, czego nie wiadomo i
   która instytucja pilnuje każdego z punktów z drugiej listy. Następnie
   wskaż, które punkty z drugiej listy program on-chain rozwiązuje, a
   których nie rozwiązuje wcale.
