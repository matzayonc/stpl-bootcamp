---
title: Ryzyka i composability
description: Co może pójść źle w protokole pożyczkowym — od zbyt wolnej likwidacji po zmanipulowany oracle — i jak ten sam brak pośrednika pozwala protokołom budować na sobie nawzajem.
sidebar_position: 5
slug: ryzyka-i-composability
---

# Ryzyka i composability

Brak pośrednika oznacza też brak kogoś, kto naprawi błąd. W banku źle
wyceniony zastaw to problem działu ryzyka; w protokole to strata, którą
ponoszą lenderzy, i nie ma do kogo pisać. Ten rozdział wylicza, co może
pójść źle — a potem pokazuje, że ta sama cecha, która czyni protokół
kruchym, pozwala mu łączyć się z innymi bez pytania kogokolwiek o zgodę.

## Ryzyka w lending

Każdy element mechanizmu z poprzedniego rozdziału ma tryb awarii.

:::warning Ryzyka, o których warto pamiętać
- **Liquidation risk** — z perspektywy pożyczkobiorcy: pozycja z wysokim
  LTV zostanie zlikwidowana przy pierwszym większym spadku, z karą w
  postaci dyskontu likwidatora. Listing 3-5 pokazał, że 20% spadku
  wystarczy.
- **Bad debt** — z perspektywy lendera: gdy cena spadnie szybciej, niż
  likwidatorzy zdążą zareagować, zastaw przestaje pokrywać dług, a
  różnicę tracą wpłacający do puli. Dzieje się to przy gwałtownych
  ruchach rynku i przy mało płynnych tokenach, których nie da się
  szybko sprzedać.
- **Program risk** — błąd w kodzie protokołu. Kod jest publiczny i
  wykonuje się dokładnie tak, jak napisany; jeśli pozwala wypłacić więcej,
  niż wynika z reguł, ktoś to zrobi.
- **Oracle manipulation** — protokół czyta cenę zastawu z oracle'a. Jeśli
  oracle bierze cenę z jednej małej puli AMM, wystarczy ją na chwilę
  przechylić, żeby protokół uznał tani token za drogi i pożyczył pod niego
  prawdziwe USDC. To najczęstszy wektor dużych strat w historii DeFi.
- **Rug pull** — projekt, który od początku był pułapką: kod z ukrytą
  funkcją wypłaty dla autora albo `Authority` programu, które pozwala
  podmienić kod po zebraniu depozytów. Pole `Authority` z Listingu 1-3
  jest pierwszą rzeczą, którą warto sprawdzić.
:::

Żadne z tych ryzyk nie ma odpowiednika w postaci „zadzwoń do banku".
Odpowiednikiem jest **czytanie**: kodu programu, parametrów puli, źródła
cen. To nie jest wygodne i dlatego większość użytkowników tego nie robi —
ale w DeFi to jedyna dostępna forma ochrony.

## Composability w DeFi

Ten sam brak pośrednika ma drugą stronę. Skoro protokół pożyczkowy jest
programem, który przyjmuje tokeny, a protokół wymiany jest programem,
który wydaje tokeny, to nic nie stoi na przeszkodzie, żeby jeden
korzystał z drugiego — i żeby trzeci korzystał z obu.

<div className="diagram">

![AMM i lending połączone: token LP z puli AMM trafia jako zastaw do protokołu pożyczkowego, pożyczone tokeny wracają do AMM, a agregator spina oba wywołaniami CPI](/img/diagrams/3_lending-02.svg)

</div>

Kilka wzorców, które z tego wynikają, jest na tyle powszechnych, że mają
nazwy:

- **Token LP jako zastaw.** Dostawca płynności w AMM ma token
  reprezentujący udział w puli. Protokół pożyczkowy może przyjąć ten token
  jako zastaw — bo umie odczytać z puli, ile jest wart. LP zarabia opłaty
  z puli *i* ma płynność z pożyczki jednocześnie.
- **Leverage loop.** Pożyczkobiorca blokuje SOL, pożycza USDC, wymienia
  USDC na SOL w AMM, blokuje ten SOL jako dodatkowy zastaw, pożycza
  więcej USDC — i tak kilka razy. Efekt to pozycja z kilkukrotnym
  lewarem na cenę SOL, złożona z dwóch protokołów, które nic o sobie nie
  wiedzą.
- **Yield aggregator.** Program, który automatyzuje powyższe: przyjmuje
  depozyt, sam rozkłada go między protokoły według strategii i sam
  reinwestuje odsetki. Użytkownik wywołuje jeden program; ten wywołuje
  kilka innych.

Mechanizm, który to umożliwia, nazywa się **Cross-Program Invocation
(CPI)**: program wywołuje instrukcję innego programu z wnętrza własnej
instrukcji, w tej samej transakcji. Wywołanie nie wymaga zgody autora
wywoływanego programu — kod jest publiczny, interfejs jest publiczny, a
sieć wykonuje każde poprawnie podpisane wywołanie. Rozdział
[Własność](../05-konta/02-wlasnosc.md) pokazuje CPI od strony kodu, a
rozdział [Transakcja](../06-transakcje-i-anchor/01-transakcja.md)
wyjaśnia, dlaczego kilka wywołań w jednej transakcji albo wykona się w
całości, albo wcale.

:::tip Analogia — klocki
Protokoły DeFi są jak klocki z jednego zestawu: każdy ma ten sam rodzaj
wypustek (tokeny, konta, instrukcje), więc każdy pasuje do każdego, choć
zaprojektowały je różne osoby, które nigdy się nie spotkały. Bank i
giełda to klocki z różnych zestawów — żeby je połączyć, trzeba umowy,
integracji i zgody obu stron.
:::

Composability ma też swoją cenę, i jest nią suma ryzyk z pierwszej
części rozdziału. Leverage loop z trzema protokołami ma trzy program
riski, trzy oracle i trzy progi likwidacji; awaria dowolnego z nich
zamyka całą konstrukcję. Kto składa klocki, odpowiada za każdy z nich.

Zostały liczby. Protokół nie ocenia człowieka — ocenia trzy wskaźniki, i
one są tematem ostatniego rozdziału.
