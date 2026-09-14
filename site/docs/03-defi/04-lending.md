---
title: Lending
description: Pożyczki bez banku — pula, zastaw, nadzabezpieczenie i automatyczna likwidacja — czyli jak pożyczyć komuś, kogo się nie zna i od kogo nie da się nic wyegzekwować.
sidebar_position: 4
slug: lending
---

# Lending

Wymiana tokenów działa bez giełdy i bez animatora rynku — wystarczyła
pula i jeden wzór. Drugi filar obietnicy jest trudniejszy. Bank, który
udziela pożyczki, robi trzy rzeczy: ocenia, czy klient odda; prowadzi
rejestr, kto ile jest winien; i ściąga dług, gdy klient nie płaci.
Program on-chain nie zna tożsamości pożyczkobiorcy, więc nie może ocenić
zdolności, i nie ma sądu ani komornika, więc nie może niczego ściągnąć.
Pytanie na ten rozdział: co w takim razie broni protokół przed
niespłaconym długiem?

## Drugi filar

Rejestr jest najprostszy — to konta, jak w każdym programie. Ocena
zdolności i egzekucja muszą zostać zastąpione czymś, co program *może*
zrobić. A program może tylko jedno: trzymać tokeny i przenosić je według
reguł. Z tego jednego narzędzia trzeba zbudować całą mechanikę pożyczki.

:::warning Bez oceny kredytowej
Łańcuch nie wie, kim jest pożyczkobiorca. Adres nie ma historii
kredytowej, dochodów ani dokumentów. Skoro nie ma scoringu i nie ma
egzekucji, to jedyną gwarancją spłaty może być coś, co program już
trzyma w ręku, zanim wypłaci pożyczkę.
:::

## Jak to działa

Protokół pożyczkowy to pula, do której jedni wpłacają, a drudzy z niej
pożyczają — z tą różnicą wobec AMM, że pożyczający musi najpierw coś
zostawić.

<div className="diagram">

![Lender wpłaca USDC do puli i otrzymuje odsetki; borrower blokuje SOL jako zastaw w puli i pożycza z niej USDC](/img/diagrams/3_lending-01.svg)

</div>

**Lender** wpłaca tokeny do puli — na przykład USDC — i od tej chwili
nalicza mu się oprocentowanie. Nie pożycza nikomu konkretnemu; pożycza
puli, a pula rozkłada odsetki od wszystkich pożyczkobiorców na
wszystkich wpłacających.

**Borrower** blokuje w puli inny token — na przykład SOL — jako
**zastaw** (*collateral*) i pożycza USDC. SOL nie zostaje sprzedany:
nadal należy do pożyczkobiorcy, nadal rośnie lub spada, tylko leży w
koncie programu, dopóki dług nie zostanie spłacony. To jest praktyczny
powód, dla którego ktokolwiek pożycza w DeFi — potrzebuje płynności bez
pozbywania się aktywa.

**Protokół** — program on-chain — trzyma pulę, nalicza odsetki i
egzekwuje reguły. Nie ma pracowników, godzin otwarcia ani decyzji
uznaniowych. Na Solanie tak działają **Kamino**, **MarginFi** i
**Solend**; pierwszy z nich obsługuje ponad miliard dolarów depozytów.

:::tip Przykład
Posiadacz 10 SOL potrzebuje 500 USDC na miesiąc. Zamiast sprzedać 5 SOL,
blokuje 10 SOL jako zastaw i pożycza 500 USDC. Po miesiącu oddaje 500
USDC plus odsetki i odblokowuje 10 SOL — które przez ten czas mogły
zdrożeć. Gdyby sprzedał, miałby 5 SOL i musiałby odkupić po nowej cenie.
:::

## Dlaczego więcej, niż się pożycza

Zastaw jest jedyną gwarancją. Gdy pożyczkobiorca nie odda — a program nie
ma jak go zmusić — protokół zatrzyma zastaw i sprzeda go, żeby pokryć
dług. To działa tylko wtedy, gdy zastaw jest wart **więcej** niż dług,
i to z zapasem, bo cena zastawu może spaść, zanim protokół zdąży go
sprzedać. Stąd reguła, która wygląda absurdalnie z perspektywy banku:
żeby pożyczyć 70 USDC, trzeba zablokować SOL warte 100.

:::note Nadzabezpieczenie
**Overcollateralization** — zastaw jest celowo wyższy niż pożyczka.
Nadwyżka to bufor, który pokrywa spadek ceny zastawu między chwilą, gdy
pozycja staje się niebezpieczna, a chwilą, gdy protokół ją zamknie. Im
bardziej zmienny token, tym większy wymagany bufor: dla USDC jako zastawu
wystarczy kilka procent, dla mało płynnego tokena — kilkadziesiąt.
:::

Bufor nie jest stały. Protokół nie patrzy na to, ile pożyczkobiorca
wpłacił, tylko na to, ile jego zastaw jest wart **teraz** — cenę czyta z
**oracle'a**, czyli programu, który dostarcza kursy z rynku. Gdy SOL
tanieje, bufor się kurczy. Gdy skurczy się do zera, uruchamia się ostatni
element mechanizmu.

## Likwidacja

**Likwidacja** to sprzedaż zastawu, zanim przestanie pokrywać dług.
Protokół nie robi tego sam — nie ma jak wyjść na rynek. Zamiast tego
otwiera możliwość dla każdego: kto spłaci dług pożyczkobiorcy, ten może
zabrać jego zastaw **z dyskontem**, na przykład 5% poniżej ceny rynkowej.
Ten ktoś nazywa się **likwidatorem** i jest zwykle botem, który
obserwuje wszystkie pozycje w protokole i reaguje w tym samym slocie, w
którym cena przekroczy próg. Dyskont jest jego wynagrodzeniem; dla
pożyczkobiorcy to kara za doprowadzenie pozycji do progu.

Listing 3-5 symuluje, co dzieje się z pozycją z poprzedniego przykładu,
gdy cena SOL spada. Trzy liczby, które tu padają — LTV, próg likwidacji
i health factor — dostają definicje w rozdziale [Matematyka
pożyczki](./06-matematyka-pozyczki.md); tutaj wystarczy śledzić ostatnią
kolumnę.

```python
collateral_sol = 1.0        # zastaw
debt_usdc     = 70.0        # dług
threshold     = 0.85        # próg likwidacji

for price in (100, 90, 83, 80, 75):
    value = collateral_sol * price
    ltv = debt_usdc / value
    hf  = value * threshold / debt_usdc
    flag = "LIKWIDACJA" if hf < 1 else ""
    print(f"SOL = {price:>3} USD  zastaw = {value:5.1f}  LTV = {ltv:5.1%}  HF = {hf:4.2f}  {flag}")
```

```text
SOL = 100 USD  zastaw = 100.0  LTV = 70.0%  HF = 1.21
SOL =  90 USD  zastaw =  90.0  LTV = 77.8%  HF = 1.09
SOL =  83 USD  zastaw =  83.0  LTV = 84.3%  HF = 1.01
SOL =  80 USD  zastaw =  80.0  LTV = 87.5%  HF = 0.97  LIKWIDACJA
SOL =  75 USD  zastaw =  75.0  LTV = 93.3%  HF = 0.91  LIKWIDACJA
```

<div className="listing"><strong>Listing 3-5.</strong> Pozycja: 1 SOL zastawu, 70 USDC długu, próg likwidacji 85%. Spadek ceny o 20% wystarcza, żeby zastaw przestał pokrywać dług z wymaganym buforem.</div>

Przy cenie 100 USD pozycja ma zapas: dług to 70% zastawu, a protokół
pozwala na 85%. Przy 90 USD zapas maleje, ale pozycja jest bezpieczna.
Przy 83 USD dług to już 84,3% zastawu — o włos od progu. Przy 80 USD
próg jest przekroczony: protokół pozwala likwidatorowi spłacić 70 USDC i
zabrać SOL warte 80 USD z dyskontem. Pożyczkobiorca zostaje z 70 USDC,
które pożyczył, i bez SOL. Gdyby protokół czekał do 75 USD, zastaw
nadal pokrywałby dług — ale przy 70 USD już nie, i strata spadłaby na
lenderów. Próg 85% to właśnie bufor na czas między sygnałem a reakcją.

:::tip Przykład
Zastaw: SOL warte 100 USD, pożyczka: 70 USDC. SOL spada o 20% do 80 USD.
Likwidator spłaca 70 USDC i odbiera SOL warte 80 USD — zarabia różnicę
pomniejszoną o to, co protokół zatrzymuje jako opłatę. Dług jest
zamknięty automatycznie, bez zgody i bez udziału pożyczkobiorcy.
:::

Cały mechanizm — zastaw, nadzabezpieczenie, oracle, likwidator z
dyskontem — zastępuje ocenę zdolności i egzekucję komorniczą jednym
narzędziem, które program ma: trzymaniem tokenów. Nie jest to model bez
wad. Następny rozdział wylicza, co może pójść źle, i pokazuje drugą stronę
tego samego mechanizmu — jak protokoły budują na sobie nawzajem.
