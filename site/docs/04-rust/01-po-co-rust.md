---
title: Po co Rust?
description: Zakres tego tematu — rozpoznać konstrukcje z każdego lib.rs, nie nauczyć się języka — i powód, dla którego kod obsługujący cudze pieniądze pisze się w języku, który odrzuca błędy przed uruchomieniem.
sidebar_position: 1
slug: po-co-rust
---

# Po co Rust?

Programy on-chain na Solanie pisze się w Ruście. Dla kogoś po
JavaScripcie albo Pythonie to pierwsza realna bariera kursu — Rust ma
opinię języka trudnego, i opinia ta jest zasłużona. Ten temat nie jest
próbą jej obalenia. Jest odpowiedzią na węższe pytanie: *ile Rusta trzeba
znać, żeby przeczytać program Anchora ze zrozumieniem?*

## Nie uczymy Rusta

Pełny kurs Rusta to semestr: lifetime'y, generyki, traity, `async`,
borrow checker w głębi. Nic z tego nie mieści się w jednym temacie i nic
z tego nie jest potrzebne, żeby zrozumieć program licznika. Cel jest
inny — po tym temacie plik `lib.rs` programu Anchora ma się czytać bez
zatrzymywania się na każdej linijce. Konkretnie: rozpoznawalne mają być
`mut`, `struct`, `match`, `Option`, `Result`, `&`, `&mut` i makra z
`#[...]` i `!`. To wystarcza, żeby czytać; pisanie przychodzi na sesji
live, z kompilatorem, który podpowiada.

:::warning To nie jest kurs Rusta
Rozdział pomija świadomie wszystko, co nie pojawia się w typowym
programie Anchora. Kto po kursie chce pisać w Ruście poza Solaną,
powinien sięgnąć po *The Rust Programming Language* — ta strona jest
wzorowana na jego układzie i będzie znajoma.
:::

## Kod on-chain

Dlaczego w ogóle Rust, a nie język, który ekosystem już zna? Odpowiedź
wynika z tego, co program on-chain robi i czego nie może.

Program on-chain obsługuje cudze pieniądze. Błąd w nim nie jest
zgłoszeniem w systemie ticketów — jest stratą użytkowników, którą widać
w Explorerze, i której nie da się cofnąć, bo transakcja zatwierdzona
przez klaster jest ostateczna. Rozdział [Programy
on-chain](../01-blockchain/03-programy-on-chain.md) nazwał to drugą
stroną niezmienności: kod wykona się dokładnie tak, jak napisany,
również wtedy, gdy jest napisany źle.

Większość historycznych exploitów w DeFi to nie wyrafinowane ataki, tylko
klasy błędów, które każdy programista zna z własnej praktyki: wartość,
która mogła być pusta i nikt tego nie sprawdził; liczba, która
przekroczyła zakres i zawinęła się do zera; błąd, który został połknięty
przez pusty `catch`; dwie części kodu, które modyfikowały ten sam stan
naraz. W językach dynamicznych te błędy ujawniają się w runtime — czyli
na łańcuchu, z prawdziwymi środkami.

Rust został zaprojektowany tak, żeby te klasy błędów **nie przeszły
kompilacji**. Nie ma `null`, więc nie ma dostępu do pustej wartości bez
sprawdzenia. Błąd jest zwykłą wartością zwracaną z funkcji, więc nie da
się go nie zauważyć. Dwa jednoczesne zapisy do tej samej zmiennej są
odrzucane przez kompilator. Każdy z tych mechanizmów dostaje własną
sekcję w rozdziale [Wzorce Rusta](./03-wzorce.md), a Listing 4-2 i
następne pokazują, jak wygląda kompilator, który mówi „nie".

:::tip Skutek
Cała klasa błędów staje się **niemożliwa**, zanim kod dotrze na sieć.
Nie „mniej prawdopodobna" — niemożliwa, bo program z takim błędem nie
istnieje jako plik wykonywalny. To jest usługa, którą Rust świadczy w
zamian za swoją trudność, i w przypadku kodu obsługującego pieniądze ta
wymiana jest opłacalna.
:::

Jest jeszcze powód techniczny: walidator wykonuje programy w maszynie
wirtualnej **SBF** (odmianie eBPF), a Rust jest językiem, dla którego
istnieje najdojrzalszy kompilator na tę platformę. Anchor — framework z
rozdziału [Transakcje i Anchor](../06-transakcje-i-anchor/index.md) —
jest napisany w Ruście i generuje kod w Ruście. Wybór języka jest więc
w praktyce dokonany; ten temat ma sprawić, żeby nie był barierą.

Następny rozdział zaczyna od tego, co widać na pierwszy rzut oka —
jak wygląda funkcja i struktura.
