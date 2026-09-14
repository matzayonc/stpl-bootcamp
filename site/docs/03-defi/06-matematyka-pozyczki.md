---
title: Matematyka pożyczki
description: LTV, health factor i utilization rate — trzy liczby, które sterują protokołem pożyczkowym — z wzorami, tabelą oprocentowania w modelu kink i policzoną granicą likwidacji.
sidebar_position: 6
slug: matematyka-pozyczki
---

# Matematyka pożyczki

Protokół nie ocenia człowieka — ocenia liczby. Trzy z nich wystarczą, by
opisać każdą pozycję i każdą pulę: dwie mówią, jak daleko pożyczkobiorca
jest od likwidacji, trzecia — ile kosztuje kapitał. Listing 3-5 użył
wszystkich trzech bez definicji; ten rozdział je dostarcza.

## LTV i health factor

**Loan-to-Value (LTV)** to stosunek wartości długu do wartości zastawu:

$$
\text{LTV} = \frac{\text{dług}}{\text{zastaw}}
$$

Pozycja z 70 USDC długu i zastawem wartym 100 USD ma LTV 70%. Protokół
definiuje dla każdego tokena dwa progi: **maksymalne LTV** przy
otwieraniu pozycji (na przykład 75% — nie da się pożyczyć więcej) i
**próg likwidacji** (na przykład 85% — powyżej niego pozycję może zamknąć
likwidator). Odstęp między nimi to zapas, który pożyczkobiorca ma na
spadek ceny, zanim cokolwiek się stanie.

<div className="diagram">

![Pasek LTV od 0% do 110%: strefa bezpieczna do 80%, próg likwidacji przy 90%, zły dług powyżej 100%](/img/diagrams/3_lending-03.svg)

</div>

Pasek pokazuje trzy strefy. Poniżej maksymalnego LTV pozycja jest
zdrowa i można z niej jeszcze pożyczyć. Między maksymalnym LTV a progiem
likwidacji pozycja jest otwarta, ale nie da się jej powiększyć — czeka.
Powyżej progu likwidacji jest do zamknięcia. Powyżej 100% dług przekracza
zastaw i zamknięcie nie pokryje całości — to **bad debt** z poprzedniego
rozdziału, którego próg likwidacji ma nie dopuścić.

LTV mówi, gdzie pozycja jest; **Health Factor (HF)** mówi, ile jej
brakuje do progu, w jednej liczbie:

:::note Health factor
$$
\text{HF} = \frac{\text{zastaw} \cdot \text{próg likwidacji}}{\text{dług}}
$$

HF powyżej 1 — pozycja bezpieczna; HF równe 1 — na progu; HF poniżej 1 —
likwidacja. HF to odwrotność LTV przeskalowana progiem: $\text{HF} =
\text{próg} / \text{LTV}$.
:::

Dla pozycji z Listingu 3-5 przy cenie 100 USD: $\text{HF} = 100 \cdot 0{,}85
/ 70 = 1{,}21$. Interpretacja jest praktyczna — zastaw może stracić
$1 - 1/1{,}21 \approx 17\%$ wartości, zanim HF spadnie do 1. Z tego
wynika cena SOL, przy której nastąpi likwidacja:

$$
p_{\text{likw}} = \frac{\text{dług}}{\text{zastaw}_{\text{SOL}} \cdot \text{próg}}
= \frac{70}{1 \cdot 0{,}85} \approx 82{,}35 \text{ USD}
$$

Listing 3-5 pokazał dokładnie to: przy 83 USD HF wynosiło 1,01, przy 80
USD — 0,97. Interfejsy protokołów wyświetlają tę cenę wprost jako
*liquidation price*, bo to jedyna liczba, na którą pożyczkobiorca musi
patrzeć.

:::tip Przykład — ile dołożyć
Pozycja z HF 0,97 przy cenie 80 USD. Żeby wrócić do HF 1,2,
pożyczkobiorca może spłacić część długu albo dołożyć zastaw. Spłata:
$70 - x$ tak, że $80 \cdot 0{,}85 / (70 - x) = 1{,}2$, czyli $x \approx
13{,}3$ USDC. Dołożenie: $(1 + y) \cdot 80 \cdot 0{,}85 / 70 = 1{,}2$,
czyli $y \approx 0{,}24$ SOL. Obie operacje to zwykłe transakcje, które
można wysłać w tym samym slocie, w którym cena spadła.
:::

## Utilization rate

Trzecia liczba dotyczy nie pozycji, tylko całej puli. **Utilization rate
(U)** to część wpłaconych środków, która jest aktualnie pożyczona:

:::note Utilization rate
$$
U = \frac{\text{pożyczone}}{\text{wpłacone}}
$$

Pula z 1 000 000 USDC depozytów i 800 000 USDC pożyczek ma $U = 80\%$.
Pozostałe 200 000 leży w puli i czeka — na wypłatę lendera albo na nową
pożyczkę.
:::

$U$ steruje oprocentowaniem, i to w obie strony. Gdy $U$ jest niskie,
większość kapitału leży bezczynnie — protokół obniża oprocentowanie, żeby
zachęcić do pożyczania. Gdy $U$ jest wysokie, w puli zostaje mało
wolnych środków, a lenderzy mogą nie mieć z czego wypłacić — protokół
gwałtownie podnosi oprocentowanie, żeby zniechęcić do pożyczania i
zachęcić do wpłat. Ten drugi efekt jest celowo ostry: powyżej pewnego
progu $U_{\text{opt}}$ krzywa oprocentowania załamuje się w górę. Model
nazywa się **kink** (od „załamania") i Listing 3-6 pokazuje typowe
parametry.

```python
base, slope1, slope2, u_opt = 0.00, 0.10, 3.00, 0.80

def apr(u):
    if u <= u_opt:
        return base + slope1 * u / u_opt
    return base + slope1 + slope2 * (u - u_opt) / (1 - u_opt)

for u in (0.0, 0.2, 0.4, 0.6, 0.8, 0.9, 0.95, 1.0):
    print(f"U = {u:4.0%}  APR pożyczkobiorcy = {apr(u):7.1%}")
```

```text
U =   0%  APR pożyczkobiorcy =    0.0%
U =  20%  APR pożyczkobiorcy =    2.5%
U =  40%  APR pożyczkobiorcy =    5.0%
U =  60%  APR pożyczkobiorcy =    7.5%
U =  80%  APR pożyczkobiorcy =   10.0%
U =  90%  APR pożyczkobiorcy =  160.0%
U =  95%  APR pożyczkobiorcy =  235.0%
U = 100%  APR pożyczkobiorcy =  310.0%
```

<div className="listing"><strong>Listing 3-6.</strong> Model kink z załamaniem przy 80%. Do progu oprocentowanie rośnie o 2,5 punktu na każde 20% wykorzystania; powyżej — o 150 punktów.</div>

Do $U_{\text{opt}}$ oprocentowanie rośnie liniowo i łagodnie: od zera do
10% rocznie. Powyżej — drugie nachylenie jest trzydzieści razy większe, i
w pełni wykorzystana pula kosztuje 310% rocznie. Nikt nie pożycza po
takiej stawce długo: pożyczkobiorcy spłacają, lenderzy wpłacają, $U$
wraca poniżej progu. Załamanie nie jest karą — jest mechanizmem, który
gwarantuje, że lender zawsze może wypłacić.

<div className="diagram narrow">

![Wykres APR w funkcji U: łagodny liniowy wzrost do U_opt, potem stromy odcinek aż do 100%](/img/diagrams/3_lending-04.svg)

</div>

Lenderzy dostają to, co płacą pożyczkobiorcy, pomnożone przez $U$ i
pomniejszone o prowizję protokołu: przy $U = 80\%$ i 10% dla
pożyczkobiorców lender widzi około 8% minus prowizja. Dlatego
oprocentowanie depozytu w DeFi zmienia się z każdym slotem — jest funkcją
stanu puli, nie decyzją komitetu.

To zamyka temat. Wymiana ma swój niezmiennik, pożyczka ma swoje trzy
wskaźniki, a oba mechanizmy są programami, które trzymają tokeny i
przenoszą je według reguł. Następne trzy tematy pokazują, jak takie
programy się pisze — zaczynając od języka.
