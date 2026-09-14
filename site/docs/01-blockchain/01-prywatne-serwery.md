---
title: Problem z prywatnymi serwerami
description: Dane, pieniądze i historia na serwerze jednej firmy — co użytkownik widzi, czego nie może sprawdzić, i dlaczego działająca aplikacja nie jest dowodem uczciwości.
sidebar_position: 1
slug: prywatne-serwery
---

# Problem z prywatnymi serwerami

Każda aplikacja finansowa, z której korzysta się na co dzień — bank,
giełda, PayPal, aplikacja do przelewów — działa na infrastrukturze jednej
firmy. Ten rozdział zaczyna się od pytania, które w Web2 rzadko pada, bo
odpowiedź wydaje się oczywista: *skąd wiadomo, że to, co pokazuje
aplikacja, jest prawdą?*

## Prywatne serwery

Model jest wszędzie ten sam. Firma utrzymuje serwery i bazę danych; klient
łączy się z nimi przez aplikację lub stronę. W bazie leżą trzy rzeczy, na
których użytkownikowi zależy najbardziej:

- **dane** — kim jest, co posiada, jakie ma uprawnienia;
- **pieniądze** — liczba w kolumnie „saldo";
- **historia** — lista operacji, które doprowadziły do tego salda.

Wygoda tego modelu jest oczywista: firma dba o dostępność, obsługuje
reklamacje, resetuje hasła. Cena jest mniej oczywista, bo płaci się ją
rzadko — ale w całości. Firma, która trzyma bazę, może **zmienić zasady**:
podnieść opłaty, zablokować konto, ograniczyć wypłaty. Nie musi przy tym
nic tłumaczyć, bo baza jest jej. Kod, który obsługuje pieniądze, może
różnić się od tego, który pokazano audytorowi — nikt z zewnątrz nie ma jak
tego sprawdzić. A gdy infrastruktura padnie, padają wszystkie usługi, które
na niej stoją.

:::tip Przykłady z życia
PayPal zamraża konta twórców bez ostrzeżenia i bez podania powodu. Giełda
FTX przez lata wypłacała środki klientów na żądanie — dopóki nie okazało
się, że tych środków nie ma. Awaria jednego regionu AWS wyłącza dziesiątki
popularnych serwisów naraz, choć każdy z nich ma „własny" backend.
:::

Żaden z tych przypadków nie jest błędem modelu. To model działa dokładnie
tak, jak został zaprojektowany: jedna strona ma pełną kontrolę, druga ma
zaufanie.

## Problem zaufania

Interfejs aplikacji pokazuje tylko to, co operator zdecyduje się pokazać.
Użytkownik obserwuje trzy rzeczy: aplikacja działa, saldo się zgadza,
historia transakcji jest dostępna. Na tej podstawie wnioskuje, że
wszystko jest w porządku. Ale to wnioskowanie ma lukę — żadna z
obserwacji nie dotyczy tego, co naprawdę ma znaczenie.

:::note Co widać
Aplikacja odpowiada. Saldo wyświetla liczbę, której użytkownik się
spodziewał. Lista operacji ma właściwe pozycje.
:::

:::warning Czego nie wiadomo
Czy dane w bazie nie zostały zmienione po fakcie. Czy środki, które
pokazuje saldo, fizycznie istnieją. Co się stanie jutro, gdy firma zmieni
regulamin, zbankrutuje albo dostanie nakaz zamrożenia konta.
:::

Różnica między tymi dwiema listami to **problem zaufania**. Nie chodzi o
to, że firmy kłamią — większość nie kłamie. Chodzi o to, że użytkownik
**nie ma sposobu, żeby to sprawdzić**. Musi ufać, a zaufanie nie jest
własnością systemu, tylko relacją między ludźmi — i jak każda relacja może
się zmienić.

W klasycznych finansach ten problem rozwiązuje się warstwami instytucji:
bank kontroluje regulator, regulatora kontroluje sąd, sąd — wyborcy. Każda
warstwa dodaje koszt, opóźnienie i kolejny podmiot, któremu trzeba ufać.
Dla przelewu w kraju to działa; dla przelewu między krajami działa
wolniej i drożej; dla kogoś w kraju bez działających instytucji nie działa
wcale.

:::tip Analogia — arkusz kalkulacyjny na cudzym koncie
Saldo w banku to komórka w arkuszu Google, do którego użytkownik ma
dostęp „tylko do odczytu", a właściciel arkusza — pełny. Właściciel może w
każdej chwili zmienić liczbę, cofnąć historię edycji albo odebrać dostęp.
Użytkownik widzi arkusz, ale nie ma nad nim kontroli.
:::

Pytanie, które z tego wynika, brzmi: czy da się zbudować system, w którym
saldo nie leży na serwerze żadnej firmy — a mimo to jest jedno, spójne i
nie da się go po cichu zmienić? Odpowiedź zajmuje następny rozdział.
