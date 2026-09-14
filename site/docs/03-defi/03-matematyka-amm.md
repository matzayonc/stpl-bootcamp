---
title: Matematyka AMM
description: Niezmiennik x·y = k, z którego wynika cena, koszt dużej wymiany i strata dostawcy płynności — policzone na liczbach, z impermanent loss w tabeli i concentrated liquidity na koniec.
sidebar_position: 3
slug: matematyka-amm
---

# Matematyka AMM

Cała pula z poprzedniego rozdziału sprowadza się do jednego równania.
Z niego wynika cena, koszt dużej wymiany i strata dostawcy płynności przy
zmianie kursu — trzy zjawiska, które w Listingu 3-2 były widoczne jako
liczby z agregatora, a tutaj dostają wyprowadzenie.

:::note To jest trudne
Ten rozdział ma najwięcej wzorów w całym kursie. Żaden z nich nie jest
potrzebny do napisania programu w Anchorze, ale bez nich nie da się
zrozumieć, dlaczego pula zachowuje się tak, a nie inaczej. Warto
przeliczyć przykłady samodzielnie — Listingi 3-3 i 3-4 to krótkie skrypty,
które można uruchomić i zmieniać.
:::

## Constant product

Pula trzyma rezerwy dwóch tokenów: $x$ jednostek tokena A i $y$ jednostek
tokena B. Program pozwala na każdą wymianę, która spełnia jeden warunek —
**iloczyn rezerw po wymianie musi być równy iloczynowi przed**.

:::note Niezmiennik
$$
x \cdot y = k
$$

$x$ — rezerwa tokenu A, $y$ — rezerwa tokenu B, $k$ — stała ustalona przy
wpłacie płynności. Wymiany zmieniają $x$ i $y$, ale nie $k$; zmienia je
tylko dodanie lub wycofanie płynności.
:::

Z niezmiennika wynika cena. Dla bardzo małej wymiany cena jednostki A
wyrażona w B to po prostu proporcja rezerw:

$$
p = \frac{y}{x}
$$

Pula z 10 SOL i 1 000 USDC wycenia SOL na 100 USDC. To nie jest cena
ustalona przez nikogo — to stan puli. Gdy cena na innych rynkach jest
inna, ktoś zarobi na wyrównaniu różnicy (kupi tam, gdzie taniej, sprzeda
tam, gdzie drożej), i tym samym przesunie proporcję rezerw do rynkowej.
Arbitraż jest mechanizmem, przez który pula „dowiaduje się" o cenie.

<div className="diagram narrow">

![Hiperbola x·y = k; punkt (x₀, y₀) przesuwa się po krzywej do (x₁, y₁) po wymianie; styczna w punkcie ma nachylenie −p](/img/diagrams/2_amm-03.svg)

</div>

Wykres tłumaczy wszystko, co następuje. Stan puli to punkt na hiperboli
$y = k/x$. Wymiana przesuwa punkt po krzywej — nigdy poza nią. Cena to
nachylenie stycznej w bieżącym punkcie. Krzywa jest wypukła, więc im
dalej od środka, tym bardziej stroma: każda kolejna jednostka kosztuje
więcej niż poprzednia. Rezerwa nigdy nie spada do zera, bo krzywa nie
dotyka osi.

## Jak działa swap

Użytkownik wpłaca $\Delta x$ tokena A i chce wypłacić $\Delta y$ tokena
B. Program wylicza $\Delta y$ tak, żeby nowy stan spełniał niezmiennik:

$$
(x + \Delta x)(y - \Delta y) = k
\quad\Longrightarrow\quad
\Delta y = y - \frac{k}{x + \Delta x}
$$

Ta sama zależność w drugą stronę — ile A trzeba dać, żeby dostać
zadane $\Delta y$ jednostek B — wynika z przekształcenia:

$$
\Delta x = \frac{k}{y - \Delta y} - x
$$

Listing 3-3 liczy to dla trzech wielkości wymiany w puli 10 SOL / 1 000
USDC.

```python
x, y = 10.0, 1_000.0          # rezerwy: SOL, USDC
k = x * y

def buy_usdc(dy):
    """Ile SOL trzeba wpłacić, żeby wypłacić dy USDC."""
    x_new = k / (y - dy)
    return x_new - x

for dy in (10, 100, 500):
    dx = buy_usdc(dy)
    print(f"{dy:>4} USDC kosztuje {dx:6.3f} SOL  →  {dy/dx:7.2f} USDC/SOL")
```

```text
  10 USDC kosztuje  0.101 SOL  →    99.00 USDC/SOL
 100 USDC kosztuje  1.111 SOL  →    90.00 USDC/SOL
 500 USDC kosztuje 10.000 SOL  →    50.00 USDC/SOL
```

<div className="listing"><strong>Listing 3-3.</strong> Trzy wymiany w tej samej puli. Cena startowa to 100 USDC za SOL; efektywna cena spada tym bardziej, im większa wymiana względem rezerw.</div>

Wynik warto przeczytać wiersz po wierszu. Za 10 USDC — jeden procent
rezerwy — płaci się 0,101 SOL, czyli prawie dokładnie po cenie
startowej. Za 100 USDC — dziesięć procent rezerwy — płaci się 1,111 SOL
zamiast 1: cena efektywna to 90 USDC za SOL. Za 500 USDC — połowę
rezerwy — trzeba oddać 10 SOL, tyle, ile pula miała na początku; cena
efektywna spadła do 50. Różnica między ceną startową a efektywną to
**price impact** i rośnie nieliniowo z wielkością wymiany. Agregator w
Listingu 3-2 dzielił 10 000 SOL między kilka pul właśnie po to, żeby w
każdej z nich pozostać w okolicach pierwszego wiersza tej tabeli.

:::tip Przykład — 100 USDC za SOL
Pula: $x = 10$ SOL, $y = 1\,000$ USDC, $k = 10\,000$. Wypłata 100 USDC
zostawia $y' = 900$, więc $x' = 10\,000 / 900 \approx 11{,}11$ SOL.
Wpłata to $11{,}11 - 10 = 1{,}11$ SOL zamiast 1 SOL, którego oczekiwałby
ktoś liczący po cenie startowej. Nadwyżka 0,11 SOL to price impact.
:::

## Impermanent loss

LP wpłacił oba tokeny. Gdy ich wzajemna cena się zmienia, arbitraż
przesuwa punkt po krzywej — pula oddaje token, który zdrożał, i przyjmuje
ten, który staniał. Przy wypłacie LP dostaje inną proporcję niż wpłacił,
a wartość tego, co dostaje, jest **niższa** niż gdyby oba tokeny po
prostu trzymał. Różnica to **impermanent loss (IL)**.

Dla puli constant product IL zależy tylko od tego, ile razy zmieniła się
cena. Jeśli $r$ to stosunek ceny przy wypłacie do ceny przy wpłacie, to
wartość pozycji LP względem trzymania wynosi:

$$
\text{IL}(r) = \frac{2\sqrt{r}}{1 + r} - 1
$$

Listing 3-4 tabelaryzuje ten wzór.

```python
from math import sqrt
for r in (1.0, 1.25, 1.5, 2.0, 3.0, 4.0, 5.0):
    il = 2 * sqrt(r) / (1 + r) - 1
    print(f"cena ×{r:<4}  IL = {il*100:6.2f}%")
```

```text
cena ×1.0   IL =   0.00%
cena ×1.25  IL =  -0.62%
cena ×1.5   IL =  -2.02%
cena ×2.0   IL =  -5.72%
cena ×3.0   IL = -13.40%
cena ×4.0   IL = -20.00%
cena ×5.0   IL = -25.46%
```

<div className="listing"><strong>Listing 3-4.</strong> Impermanent loss w funkcji zmiany ceny. Wzór jest symetryczny: spadek ceny czterokrotny daje tę samą stratę co wzrost czterokrotny.</div>

Trzy obserwacje z tej tabeli tłumaczą, jak LP podejmują decyzje. Po
pierwsze, przy $r = 1$ strata wynosi zero — stąd słowo *impermanent*:
jeśli cena wróci do poziomu z chwili wpłaty, strata znika. Po drugie,
strata rośnie wolno na początku (0,6% przy zmianie o ćwierć) i szybko
później (20% przy czterokrotnej) — pary tokenów, które chodzą razem, jak
USDC/USDT, mają IL bliski zera. Po trzecie, LP zarabia netto tylko wtedy,
gdy zebrane opłaty przekraczają IL; dla zmiennej pary to wymaga dużego
obrotu.

:::warning Impermanent loss
Gdy cena tokenów zmienia się względem chwili wpłaty, wartość pozycji LP
jest niższa niż wartość tych samych tokenów trzymanych poza pulą. Strata
jest „tymczasowa" tylko w tym sensie, że znika, gdy cena wróci — a cena
nie musi wrócić.
:::

## Concentrated liquidity

Pula constant product rozkłada płynność po całej krzywej — od ceny
bliskiej zeru do bliskiej nieskończoności. Większość tej płynności nigdy
nie jest używana: SOL nie kosztuje ani 1 USDC, ani 10 000. Ulepszenie
nazywa się **Concentrated Liquidity Market Maker (CLMM)**: LP wybiera
**przedział cenowy** $[p_a, p_b]$, w którym jego płynność ma działać.
Wewnątrz przedziału pula zachowuje się jak constant product, ale z
kapitałem skoncentrowanym tam, gdzie faktycznie odbywa się handel — więc
ten sam depozyt daje mniejszy price impact i zbiera więcej opłat.

Cena tego ulepszenia jest dwojaka. Gdy cena rynkowa wyjdzie poza
przedział, pozycja LP przestaje zarabiać i składa się w całości z tańszego
tokena — IL jest większy niż w zwykłej puli. A wybór przedziału to
decyzja, którą trzeba podejmować i aktualizować; pasywny LP w CLMM
zwykle traci.

:::tip Na Solanie
**Orca Whirlpools** i **Raydium CLMM** to dwie największe implementacje
CLMM; pule z Listingu 3-2 (`TesseraV`, `HumidiFi`) to nowsze
konstrukcje, które łączą koncentrację z własną wyceną. Kod każdej z nich
jest publiczny.
:::

Wymiana ma już swój wzór. Drugi filar obietnicy — pożyczka — wymaga
odpowiedzi na trudniejsze pytanie: jak pożyczyć komuś, kogo się nie zna
i od kogo nie da się nic wyegzekwować. To temat następnego rozdziału.
