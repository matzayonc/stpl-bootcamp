---
title: Model kont
description: Na Solanie wszystko jest kontem — pięć pól, reguła właściciela, PDA, rent i rozmiar, oraz jak to wszystko sprawdzić w Explorerze i z CLI.
sidebar_position: 0
---

# Model kont

Jeden pomysł organizuje całą Solanę: **wszystko jest kontem**. Portfel,
token, program — każde z nich to komórka pamięci z adresem, saldem i
danymi. Kto zrozumie, jak wygląda konto, kto może je zmieniać, skąd bierze
się jego adres i ile kosztuje, ten rozumie już połowę tego, co robi
program Anchora. Druga połowa — transakcje i sam framework — jest w
następnym temacie.

Rozdział rozwija slajdy *Model Kont*
([PDF](https://github.com/matzayonc/stpl-slides/releases/download/latest/5_accounts.pdf))
o rzeczy, na które na wykładzie nie ma czasu: prawdziwe konta odczytane z
mainnetu, mechanikę PDA, wzór na depozyt i komunikaty błędów, które Anchor
wypisuje, gdy któreś sprawdzenie nie przejdzie.

## Zawartość

1. [Anatomia konta](./01-anatomia-konta.md) — pięć pól, lamporty, konta
   danych i programów, różnica wobec Ethereum. Trzy prawdziwe konta
   odczytane z CLI.
2. [Własność](./02-wlasnosc.md) — reguła właściciela, podpis jako zgoda,
   jak System Program tworzy konto, co sprawdzają `Account` i `Signer` i
   jak wyglądają błędy `AccountOwnedByWrongProgram` oraz `ConstraintHasOne`.
3. [Adres i PDA](./03-adres-i-pda.md) — adres z klucza, adres z
   wyliczenia, bump kanoniczny, `seeds` i `bump` w Anchorze, PDA jako
   signer.
4. [Koszt](./04-koszt.md) — rent-exempt jako kaucja, wzór z aktualną
   stawką, tabela rozmiarów, `InitSpace`, `realloc`, `close`.
5. [Konta w praktyce](./05-w-praktyce.md) — te same konta w Explorerze,
   CLI i przez RPC; dwa znaczenia słowa `owner`.

Pytania sprawdzające do rozdziału: [Model kont — pytania
kontrolne](../08-pytania-kontrolne/05-model-kont.md).

## Podsumowanie

Konto to struktura `{lamports, data, owner, executable}` pod 32-bajtowym
adresem; adres jest kluczem w globalnej mapie, nie polem. Konta programów
mają `executable = true` i trzymają kod; wszystkie inne trzymają stan.
Jeden program obsługuje dowolnie wiele kont danych, które dostaje z
zewnątrz przy każdym wywołaniu — to główna różnica wobec Ethereum i powód,
dla którego transakcje na Solanie mogą wykonywać się równolegle.

Zmieniać `data` i zmniejszać `lamports` może wyłącznie program-właściciel;
dodawać lamporty może każdy. Użytkownik nie jest nigdy właścicielem —
wyraża zgodę podpisem, a program-właściciel sprawdza ten podpis, zanim coś
zmieni. W Anchorze `Account<'info, T>` sprawdza właściciela i
dyskryminator, `Signer<'info>` sprawdza podpis, a `has_one` wiąże oba ze
sobą. Nowe konta tworzy System Program: przelew depozytu, alokacja,
przypisanie właściciela.

Adres bierze się z klucza publicznego albo z wyliczenia. **Program Derived
Address (PDA)** to hash seedów i adresu programu z dodatkowym bajtem
`bump`, dobranym tak, by adres nie miał klucza prywatnego. Dzięki temu
program znajduje konto użytkownika bez bazy danych, a w CPI może za takie
konto „podpisać". Bump zapisuje się w koncie, żeby nie szukać go ponownie.

Miejsce kosztuje: konto musi być **rent-exempt**, czyli mieć depozyt
$(\text{rozmiar} + 128) \cdot \text{stawka}$ lamportów — jednorazowy i
zwrotny po `close`. Rozmiar deklaruje się z góry: 8 bajtów dyskryminatora
plus suma pól, najlepiej przez `#[derive(InitSpace)]`. Za mało bajtów
kończy się błędem `AccountDidNotSerialize`; za dużo — cicho przepłaconym
depozytem.

:::tip Analogia na koniec
Konto to plik; program to aplikacja z prawem zapisu do tego pliku; PDA to
ścieżka do pliku wyliczona z nazwy użytkownika, a rent-exempt to kaucja
za miejsce na dysku.
:::

## Ćwiczenia

Ćwiczenia wymagają zainstalowanego Solana CLI (rozdział [Portfel i
narzędzia](../07-portfel-i-narzedzia/index.md)) i dostępu do sieci; nie
wymagają własnego programu.

1. **Trzy konta, trzy typy.** Odczytaj poleceniem `solana account` na
   mainnecie: mint USDC (`EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v`),
   System Program (`11111111111111111111111111111111`) i dowolny portfel
   z Explorera. Dla każdego zapisz `owner`, `executable` i długość `data`,
   a potem wyjaśnij jednym zdaniem, dlaczego mint ma 82 bajty, a portfel
   zero. Co jest właścicielem System Programu?

2. **Rachunek depozytu.** Struktura ma pola `authority: Pubkey`,
   `created_at: i64`, `tags: Vec<u8>` z `#[max_len(16)]` i `nick: String`
   z `#[max_len(24)]`. Policz `INIT_SPACE`, dodaj dyskryminator i sprawdź
   wynik poleceniem `solana rent`. Następnie policz, o ile lamportów
   przepłaci milion takich kont, jeśli `nick` dostanie `#[max_len(64)]`
   zamiast 24.

3. **Odtworzenie PDA.** Skopiuj adres własnego portfela z Phantoma i
   wylicz poleceniem `solana find-program-derived-address` adres swojego
   konta USDC na devnecie (mint devnetowy:
   `4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU`; seedy jak w Listingu
   5-11). Jeśli konto istnieje, odczytaj je; jeśli nie — wyjaśnij, jaki
   `owner` i jakie `data` miałoby po utworzeniu i kto musiałby zapłacić
   depozyt.

4. **Który check by to zatrzymał?** Dla każdej sytuacji wskaż, które
   sprawdzenie z Listingu 5-7 (`Account`, `Signer`, `has_one`) odrzuci
   transakcję i jaki `Error Number` pojawi się w logu:
   (a) atakujący podaje jako `vault` własne konto założone innym
   programem o identycznym układzie pól;
   (b) atakujący podaje prawdziwy `vault` ofiary i podpisuje własnym
   kluczem;
   (c) atakujący podaje prawdziwy `vault` i klucz ofiary jako
   `authority`, ale bez jej podpisu.
