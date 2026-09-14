---
title: Portfel i narzędzia
description: Klucze wygenerowane z terminala, Phantom i seed phrase, devnet, Solana CLI, airdrop i pierwsza transakcja prześledzona w terminalu i w Explorerze — część praktyczna, po której wszystko z kursu da się zobaczyć na żywo.
sidebar_position: 0
---

# Portfel i narzędzia

Jedno zdanie organizuje ten temat: **wszystko, co kurs opisywał, da się
zobaczyć na własnym koncie w ciągu godziny**. Para kluczy z rozdziału o
tożsamości, transakcja z rozdziału o zapisie, pola konta z modelu kont,
opłata i slot z rozdziału o Solanie — każde z nich ma swoje miejsce w
wyniku jednego polecenia albo na jednej stronie Explorera. To rozdział,
po którym teoria przestaje być teorią.

Rozdział rozwija slajdy *Pierwszy wallet*
([PDF](https://github.com/matzayonc/stpl-slides/releases/download/latest/7_wallet.pdf))
o rzeczy, na które na wykładzie nie ma czasu: klucz wygenerowany i
zweryfikowany z CLI, zawartość pliku z kluczem, instalację i
konfigurację narzędzi, odmowę faucetu, pełny opis prawdziwego przelewu
z `solana confirm -v`, transakcję odrzuconą przed wysłaniem i konto
odczytane po wszystkim.

## Zawartość

1. [Klucze](./01-klucze.md) — klucz prywatny i publiczny,
   `solana-keygen new`, plik z kluczem i `verify`, **podpis** jako zgoda
   i identyfikator, dlaczego nie ma hasła.
2. [Phantom](./02-phantom.md) — instalacja w cztery kroki, co
   rozszerzenie robi, a czego nie, **seed phrase** i BIP-39, cztery zasady
   i jedna, której nie wolno złamać.
3. [Devnet i airdrop](./03-devnet-i-airdrop.md) — devnet kontra
   mainnet, przełączenie Phantoma, instalacja Solana CLI i `solana
   config`, trzy źródła **airdropu** i limit.
4. [Pierwsza transakcja](./04-pierwsza-transakcja.md) — przelew z
   `solana transfer`, pełny rozbiór przez `solana confirm -v`, odmowa z
   powodu salda, Explorer jako podgląd transakcji i konta.

Pytania sprawdzające do rozdziału: [Portfel i narzędzia — pytania
kontrolne](../08-pytania-kontrolne/07-portfel-i-narzedzia.md).

## Checklist

- [ ] Phantom zainstalowany z oficjalnej strony
- [ ] Seed phrase zapisany offline i przetestowany przez odzyskanie
- [ ] Sieć w Phantomie przełączona na **Devnet**
- [ ] Solana CLI zainstalowane, `solana config get` pokazuje devnet
- [ ] Airdrop wykonany, saldo w Phantomie i w CLI większe od zera
- [ ] Przelew między portfelem CLI a Phantomem widoczny w Explorerze

Po odhaczeniu wszystkich punktów jest wszystko, czego sesja live wymaga
na wejściu.

## Podsumowanie

Portfel przechowuje jedną rzecz — **klucz prywatny**, 32 bajty — i
wylicza z niego **klucz publiczny**, który jest **adresem**. Wyliczenie
idzie tylko w jedną stronę. `solana-keygen new` tworzy parę, zapisuje
prywatną połowę do pliku z 64 liczbami i wypisuje adres oraz **seed
phrase**; `verify` składa próbny podpis i sprawdza go adresem — w
miniaturze to, co każdy walidator robi z każdą transakcją. **Podpis** to
64 bajty z treści i klucza prywatnego, weryfikowalne kluczem publicznym,
nieważne po zmianie jednego bajtu; jest zgodą na treść i identyfikatorem
transakcji. Hasła nie ma, bo nie ma serwera, który by je porównywał.

**Phantom** robi to samo w przeglądarce: generuje klucz lokalnie, pokazuje
saldo z RPC, podpisuje po pokazaniu treści. Hasło lokalne szyfruje plik
na tym urządzeniu; **seed phrase** — dwanaście słów BIP-39 — odtwarza
klucz i wszystkie konta z niego wyliczone na dowolnym urządzeniu. Kto ma
frazę, ma środki: nigdy online, bez zdjęć, zapis offline, test
odzyskiwania.

**Devnet** to osobny łańcuch z tym samym kodem i API co **mainnet**, ale
z tokenami bez wartości; cały kurs dzieje się tam, mainnet jest tylko
czytany. **Solana CLI** 3.x instaluje się skryptem Anzy; `solana config
set --url devnet` ustawia sieć i domyślny klucz dla wszystkich poleceń.
**Airdrop** z CLI, faucetu lub Playground daje 1–2 SOL na żądanie z
limitem, w który łatwo trafić.

Przelew `solana transfer` zwraca podpis; `solana confirm -v` rozkłada go
na slot, blockhash, konta z flagami `srw-`, instrukcję `Transfer`,
opłatę 5 000 lamportów, salda przed i po, jednostki obliczeniowe i logi.
Transfer ponad saldo jest odrzucany przed wysłaniem, bez podpisu i bez
opłaty. **Explorer** pokazuje to samo z `getTransaction` w przeglądarce,
a strona konta — pola `lamports`, `owner`, `executable`, `data` z modelu
kont na żywo.

:::tip Analogia na koniec
Klucz prywatny to stempel, klucz publiczny to wzór odcisku, podpis to
odcisk na tym jednym liście; seed phrase to klucz główny do mieszkania,
którego zgubienie oznacza, że ktoś inny ma kopię; devnet to plac
manewrowy, na którym każdy błąd jest darmowy; a Explorer to okno na
łańcuch — ta sama szyba, przez którą patrzy `curl`, tylko z ramą.
:::

## Ćwiczenia

Ćwiczenia wymagają Phantoma, Solana CLI i przeglądarki; wszystko na
devnecie.

1. **Dwa portfele, jeden przelew.** Wygeneruj klucz CLI (`solana-keygen
   new`), zdobądź na niego SOL z airdropu i przelej 0,05 SOL na adres
   swojego Phantoma. Odczytaj transakcję przez `solana confirm -v` i w
   Explorerze; zapisz slot, opłatę i flagi obu kont. Następnie zrób
   przelew w drugą stronę z Phantoma i porównaj: który portfel był
   `fee payer` w każdej transakcji?

2. **Ile kosztuje nic.** Wyślij przelew na 0 SOL (`solana transfer
   <adres> 0`). Czy transakcja przeszła? Ile pobrano opłaty? Co pokazuje
   `Account 1 balance` w `confirm -v`? Wyjaśnij jednym zdaniem, za co
   dokładnie sieć pobiera opłatę.

3. **Odzyskaj klucz.** Usuń portfel z Phantoma (*Settings → Manage
   Accounts → Remove*) i przywróć go z seed phrase. Sprawdź, że adres i
   saldo są te same. Następnie w Phantomie dodaj „Account 2" i odczytaj
   jego adres — czy ten adres da się odtworzyć z tej samej frazy na innym
   urządzeniu? Skąd to wiadomo?

4. **Trzy odczyty, trzy narzędzia.** Dla adresu swojego Phantoma odczytaj
   saldo trzema drogami: w rozszerzeniu, przez `solana balance` i przez
   `curl` z `getBalance` na `api.devnet.solana.com`. Zapisz wszystkie
   trzy wartości i `context.slot` z odpowiedzi RPC. Które z tych trzech
   narzędzi ma własną kopię stanu, a które tylko pytają?
