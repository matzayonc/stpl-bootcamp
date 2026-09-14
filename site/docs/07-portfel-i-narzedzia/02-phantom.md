---
title: Phantom
description: Instalacja rozszerzenia Phantom, co dzieje się przy „Create New Wallet", czym jest seed phrase i jedna zasada obchodzenia się z nim, której nie wolno złamać.
sidebar_position: 2
slug: phantom
---

# Phantom

Klucz z poprzedniego rozdziału leży w pliku i podpisuje z terminala.
W przeglądarce tę samą pracę wykonuje **Phantom** — rozszerzenie, które
trzyma klucze, pokazuje saldo i podpisuje transakcje, gdy poprosi o to
strona. Cztery kroki instalacji i jedna zasada, której złamanie nie ma
odwrotu.

## Instalacja

1. Zainstaluj rozszerzenie **Phantom** ze sklepu przeglądarki (Chrome,
   Brave, Firefox, Edge) — wyłącznie z oficjalnej strony `phantom.com`,
   bo podrobione portfele to najstarszy sposób kradzieży kluczy.
2. Kliknij *Create New Wallet*. Rozszerzenie generuje parę kluczy
   **lokalnie**, w przeglądarce — dokładnie to, co zrobiło `solana-keygen
   new` w Listingu 7-1, tylko bez wypisywania wyniku na ekran. Żaden
   serwer Phantoma nie widzi klucza prywatnego.
3. Zapisz **seed phrase** — dwanaście słów, które rozszerzenie pokaże raz.
   O tym niżej.
4. Ustaw **hasło lokalne**. To hasło szyfruje klucz na dysku tej jednej
   przeglądarki i odblokowuje rozszerzenie po ponownym otwarciu. Nie ma
   nic wspólnego z tożsamością w sieci: nie da się nim odzyskać portfela
   na innym urządzeniu, a jego reset to po prostu ponowny import z seed
   phrase.

<div className="diagram screenshot">

![Phantom po założeniu portfela — widok głównego ekranu z saldem 0 SOL i adresem konta](/img/phantom-balance.png)

</div>

Po czwartym kroku główny ekran pokazuje saldo i skrócony adres — ten sam
rodzaj ciągu, co `pubkey` z Listingu 7-1. Kliknięcie w adres kopiuje go
w całości; to on będzie wklejany do faucetu i do Explorera w kolejnych
rozdziałach.

:::note Co Phantom robi, a czego nie
Phantom trzyma klucz prywatny, wylicza z niego adres, pokazuje saldo
odczytane z węzła RPC i podpisuje transakcje, które przygotowała strona
— po pokazaniu użytkownikowi, co podpisuje. Nie trzyma środków (są w
sieci), nie zna hasła do niczego poza własnym plikiem i nie może
niczego cofnąć. Każdy portfel — Solflare, Backpack, portfel sprzętowy —
robi to samo; różni się interfejsem.
:::

## Seed phrase

Dwanaście słów z drugiego kroku to **seed phrase** — klucz prywatny
zapisany w postaci czytelnej dla człowieka. Słowa pochodzą ze stałej
listy 2 048 słów (standard **BIP-39**), a ich kolejność koduje losowe
bajty, z których deterministycznie powstaje klucz. Ten sam ciąg słów
wpisany w dowolny portfel na dowolnym urządzeniu daje ten sam klucz
prywatny, ten sam adres i dostęp do tych samych środków.

<div className="diagram narrow">

![Seed phrase, z którego deterministycznie powstają kolejne konta: Konto 1, Konto 2, Konto 3](/img/diagrams/7_wallet-03.svg)

</div>

Z jednej frazy wynika nie jeden klucz, ale dowolnie wiele: Phantom
pozwala dodać „Konto 2", „Konto 3" i każde z nich jest wyliczone z tej
samej frazy z innym numerem. Kopia zapasowa jednej frazy to kopia
wszystkich kont. Listing 7-1 pokazał frazę wypisaną przez CLI; Phantom
pokazuje ją w tym samym formacie, tylko w oknie przeglądarki.

Zasady obchodzenia się z frazą wynikają z jednego faktu: **kto ma frazę,
ma środki** — bez hasła, bez urządzenia, bez pytania.

- **Nigdy online.** Nie wklejać do żadnej strony, nie wpisywać w żaden
  formularz, nie wysyłać żadnym komunikatorem. Żadna prawdziwa usługa —
  Phantom, giełda, „wsparcie techniczne" — nigdy o frazę nie prosi.
  Prośba o frazę jest kradzieżą.
- **Bez zdjęć i chmury.** Screenshot trafia do galerii, galeria do
  kopii w chmurze, chmura do każdego, kto zdobędzie hasło do konta.
- **Zapis offline.** Kartka w bezpiecznym miejscu albo menedżer haseł,
  który nie synchronizuje przez cudze serwery. Na kurs wystarczy kartka.
- **Test odzyskiwania.** Zanim na portfelu pojawią się prawdziwe środki,
  warto raz go usunąć i przywrócić z frazy, żeby wiedzieć, że zapis jest
  poprawny.

:::warning Kto ma seed, ma środki
Nie istnieje procedura „zapomniałem frazy" — rozdział [Portfel jako
tożsamość](../02-web3/04-portfel-jako-tozsamosc.md) wyjaśnił, dlaczego nie
może istnieć. I nie istnieje procedura „fraza wyciekła": klucza nie da
się zmienić, można tylko przenieść środki na nowy, jeśli zdąży się przed
złodziejem. Wycieka raz, na zawsze.
:::

Dla portfela deweloperskiego na devnecie te zasady są ćwiczeniem: środki
nie mają wartości. Ale nawyki z devnetu przechodzą na mainnet, i lepiej,
żeby były właściwe od pierwszego dnia.

:::tip Analogia — klucz do mieszkania
Hasło lokalne to zamek w drzwiach: chroni to jedno wejście i da się go
wymienić. Seed phrase to klucz główny, którego kopia otwiera każde drzwi
do tego mieszkania, teraz i za dziesięć lat — a zgubiony klucz główny
oznacza, że ktoś inny ma kopię, i nie wiadomo kto.
:::

Portfel jest. Saldo pokazuje zero — na sieci, na której Phantom stoi
domyślnie, każdy SOL kosztuje prawdziwe pieniądze. Następny rozdział
przełącza portfel na sieć, na której SOL jest za darmo.
