# Egzamin --- Lekcja 8: Prywatność

## Pytania

1. Podpis kryptograficzny gwarantuje autentyczność, integralność i
   niezaprzeczalność. Których dwóch własności **nie** zapewnia, i co z tego
   wynika dla obserwatora przeglądającego transakcję w explorerze?

   A. Nie zapewnia integralności ani autentyczności; obserwator widzi tylko podpis
   B. Nie zapewnia poufności ani anonimowości; obserwator widzi kwotę, strony i całą historię
   C. Nie zapewnia niezaprzeczalności ani trwałości; obserwator nie widzi nadawcy
   D. Nie zapewnia szybkości ani kompresji; obserwator widzi wyłącznie saldo

2. Czym jest **zobowiązanie (commitment)** i jakie dwie własności musi
   spełniać? Po co do skrótu dokładana jest losowa zaślepka?

   A. Podpis wieloosobowy; jawność i trwałość; zaślepka skraca dane
   B. Zaszyfrowana kopia transakcji; szybkość i tanie przechowywanie; zaślepka to numer bloku
   C. Zalakowana wartość; wiążące i ukrywające; zaślepka uniemożliwia przeliczenie krótkiego zbioru wartości
   D. Adres jednorazowy; anonimowość i przenośność; zaślepka to klucz publiczny odbiorcy

3. Co dokładnie ukrywają **poufne transfery (confidential transfers)** w
   Token-2022, a co pozostaje jawne dla każdego obserwatora łańcucha?

   A. Ukrywają adresy stron; kwoty i salda pozostają jawne
   B. Ukrywają kwoty i salda; adresy nadawcy i odbiorcy pozostają jawne
   C. Ukrywają całą transakcję; jawny jest wyłącznie znacznik czasu
   D. Ukrywają wyłącznie saldo odbiorcy; reszta jest jawna

## Pytania zapasowe

4. Wymień trzy własności **dowodu z wiedzą zerową (ZKP)**, które sprawiają, że
   weryfikator może zaufać odpowiedzi, nie poznając danych, na których się ona
   opiera.

   A. Zupełność, poprawność, wiedza zerowa
   B. Poufność, integralność, dostępność
   C. Determinizm, odwracalność, kompresja
   D. Autentyczność, niezaprzeczalność, trwałość

5. Na czym polega **homomorfizm addytywny** szyfrowania i dlaczego jest
   niezbędny, aby sieć mogła obsłużyć zaszyfrowane saldo konta?

   A. Ten sam tekst daje zawsze ten sam szyfrogram; sieć porównuje szyfrogramy
   B. Szyfrogram da się odszyfrować dwoma różnymi kluczami; sieć wybiera tańszy
   C. Dwa szyfrogramy można dodać bez odszyfrowania; sieć aktualizuje saldo, nie znając kwot
   D. Szyfrowanie zmniejsza rozmiar danych; sieć mieści więcej transakcji w bloku

## Klucz odpowiedzi

1. B
2. C
3. B
4. A
5. C
