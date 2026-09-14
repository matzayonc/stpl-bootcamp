---
title: DeFi
description: Dwa filary finansów bez pośrednika — wymiana tokenów przez AMM i pożyczki pod zastaw — z tokenem odczytanym z sieci, prawdziwą wyceną z agregatora i matematyką policzoną na liczbach.
sidebar_position: 0
---

# DeFi

Jedno pytanie organizuje ten temat: **co może zrobić program, który umie
tylko trzymać tokeny i przenosić je według reguł?** Okazuje się, że
giełdę i bank — jeśli zastąpi się dopasowywanie zleceń jednym równaniem,
a ocenę zdolności kredytowej zastawem, który program już trzyma w ręku.
Kto zrozumie te dwa mechanizmy, rozumie, z czego zbudowana jest reszta
DeFi.

Rozdział łączy slajdy *AMM na Solanie*
([PDF](https://github.com/matzayonc/stpl-slides/releases/download/latest/2_amm.pdf))
i *Lending na Solanie*
([PDF](https://github.com/matzayonc/stpl-slides/releases/download/latest/3_lending.pdf))
i rozwija je o rzeczy, na które na wykładzie nie ma czasu: mint USDC
odczytany z sieci głównej, wycenę 1 SOL i 10 000 SOL z prawdziwego
agregatora, skrypty, które liczą price impact, impermanent loss, health
factor i model kink, oraz wyprowadzenie ceny likwidacji.

## Zawartość

1. [Czym jest DeFi?](./01-czym-jest-defi.md) — obietnica i jej dwa
   filary, **DeFi** jako permissionless i composable, **token** jako
   saldo z regułami, mint USDC z CLI.
2. [AMM](./02-amm.md) — order book kontra **AMM**, pula i proporcja
   rezerw, prawdziwa wycena z price impactem, **LP** i opłaty, lista
   ryzyk.
3. [Matematyka AMM](./03-matematyka-amm.md) — niezmiennik $x \cdot y =
   k$, wzór na swap policzony dla trzech wielkości, **impermanent loss**
   w tabeli, **CLMM**.
4. [Lending](./04-lending.md) — pula, lender i borrower, **zastaw**,
   **nadzabezpieczenie**, oracle, **likwidacja** z dyskontem i symulacja
   spadku ceny.
5. [Ryzyka i composability](./05-ryzyka-i-composability.md) — bad debt,
   oracle manipulation, rug pull; token LP jako zastaw, leverage loop,
   agregatory i **CPI**.
6. [Matematyka pożyczki](./06-matematyka-pozyczki.md) — **LTV**,
   **health factor** i cena likwidacji, **utilization rate** i model
   kink z tabelą oprocentowania.

Pytania sprawdzające do rozdziału: [AMM — pytania
kontrolne](../08-pytania-kontrolne/02-amm.md) i [Lending — pytania
kontrolne](../08-pytania-kontrolne/03-lending.md).

## Podsumowanie

**DeFi** to usługi finansowe, w których pośrednikiem jest program
on-chain: permissionless, bo program nie wie, kim jest wywołujący, i
composable, bo programy wywołują się nawzajem bez umów. Wartość na
łańcuchu ma jedną postać — konto z saldem — a **token** to takie saldo
prowadzone przez Token Program według reguł zapisanych w mincie: podaż,
miejsca po przecinku, kto może dodrukować, kto może zamrozić. Wszystkie
te reguły są publiczne przed pierwszym użyciem.

**AMM** zastępuje giełdę pulą dwóch tokenów i jednym niezmiennikiem:
$x \cdot y = k$. Cena to proporcja rezerw, wymiana przesuwa punkt po
hiperboli, a każda kolejna jednostka kosztuje więcej — to **price
impact**, który agregator zmniejsza, dzieląc zlecenie między pule.
Płynność wpłaca **LP** w zamian za udział w opłatach, ponosząc
**impermanent loss**: przy czterokrotnej zmianie ceny 20% względem
trzymania tokenów, przy powrocie ceny — zero. **CLMM** koncentruje
płynność w przedziale cenowym kosztem większego IL poza nim.

**Lending** zastępuje bank pulą, do której lenderzy wpłacają, a
borrowerzy pożyczają pod **zastaw** wart więcej niż dług —
**nadzabezpieczenie** jest jedyną gwarancją, bo program nie ocenia
zdolności i niczego nie egzekwuje. Cenę zastawu dostarcza **oracle**; gdy
spadnie poniżej progu, **likwidator** spłaca dług i zabiera zastaw z
dyskontem. Ryzyka — bad debt, oracle manipulation, program risk, rug
pull — nie mają infolinii; mają kod do przeczytania. Ta sama otwartość
daje **composability** przez **CPI**: token LP jako zastaw, leverage
loop, agregatory.

Trzy liczby opisują wszystko: **LTV** to dług przez zastaw, **health
factor** to zastaw razy próg likwidacji przez dług — poniżej 1 następuje
likwidacja, a cena likwidacji wynika z odwrócenia wzoru — i
**utilization rate**, czyli pożyczone przez wpłacone, który w modelu
kink steruje oprocentowaniem: łagodnie do progu, gwałtownie powyżej, tak
by lender zawsze mógł wypłacić.

:::tip Analogia na koniec
Token to żeton w kasynie, którego reguły każdy może przeczytać przed
wejściem; AMM to koszyk jabłek i gruszek, w którym cena wynika z
nierównowagi; protokół pożyczkowy to lombard, który nie pyta o dochody,
bo trzyma zastaw w ręku; a composability to klocki z jednego zestawu,
które pasują do siebie, choć projektowały je różne osoby.
:::

## Ćwiczenia

Ćwiczenia wymagają `curl`, Pythona (lub dowolnego języka z arytmetyką) i
przeglądarki; Solana CLI jest potrzebne tylko w pierwszym.

1. **Regulamin tokena.** Odczytaj `spl-token display` (lub stronę w
   Explorerze) dla trzech mintów: USDC
   (`EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v`), USDT
   (`Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB`) i dowolnego tokena z
   pierwszej strony wyników na Jupiterze. Dla każdego zapisz `Decimals`,
   podaż w jednostkach czytelnych dla człowieka, i czy `Mint authority` oraz
   `Freeze authority` są ustawione. Który z tokenów może zamrozić konto
   posiadacza, a który nie może zmienić podaży?

2. **Własny price impact.** Uruchom skrypt z Listingu 3-3 dla puli
   1 000 SOL / 100 000 USDC (ta sama cena, sto razy większa płynność) i
   tych samych trzech wielkości wymiany. Porównaj ceny efektywne z
   tabelą w rozdziale. Następnie pobierz z agregatora Jupiter wycenę 100
   SOL i 1 000 SOL i sprawdź, czy `priceImpactPct` rośnie w podobnym
   tempie.

3. **Cena likwidacji.** Pozycja: 5 SOL zastawu, 300 USDC długu, próg
   likwidacji 80%. Policz LTV, health factor i cenę SOL, przy której
   nastąpi likwidacja. Następnie policz, ile USDC trzeba spłacić albo ile
   SOL dołożyć, żeby cena likwidacji spadła o połowę. Zapisz oba wyniki z
   wyprowadzeniem.

4. **Kink w drugą stronę.** Zmodyfikuj skrypt z Listingu 3-6 tak, by
   liczył też oprocentowanie lendera (APR pożyczkobiorcy razy $U$ razy
   $1 - \text{prowizja}$, z prowizją 10%). Przy jakim $U$ lender dostaje
   najwięcej? Dlaczego protokół mimo to wolałby, żeby $U$ nie było wyższe
   niż $U_{\text{opt}}$?
