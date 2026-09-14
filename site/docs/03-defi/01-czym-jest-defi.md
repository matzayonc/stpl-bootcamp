---
title: Czym jest DeFi?
description: Obietnica finansów bez pośrednika, jej dwa filary — wymiana i pożyczki — i token jako saldo z regułami w kodzie, odczytany z sieci głównej.
sidebar_position: 1
slug: czym-jest-defi
---

# Czym jest DeFi?

Pierwszy temat złożył obietnicę: usługi finansowe **bez pośrednika**,
wykonywane przez program w sieci BFT. Drugi pokazał, jak taki program
jest wywoływany. Ten temat sprawdza, czy obietnica jest wykonalna — i
zaczyna od pytania, które brzmi naiwnie, ale nie ma oczywistej
odpowiedzi: *co dokładnie miałoby powstać, i z czego?*

## Wracamy do obietnicy

Bank, broker i notariusz znikają, a ich rolę przejmuje kod. Ale bank robi
wiele rzeczy naraz i nie wszystkie da się zastąpić programem. Z całego
katalogu usług finansowych dwie są fundamentem, na którym stoi reszta:
**wymiana** jednego aktywa na drugie i **pożyczka** jednego aktywa pod
zastaw drugiego. Kto umie wymieniać i pożyczać, ma już giełdę i bank;
ubezpieczenia, instrumenty pochodne i fundusze da się zbudować z tych
dwóch klocków.

Zanim jednak pojawi się pierwszy mechanizm, trzeba zauważyć problem,
który w klasycznych finansach jest niewidoczny, bo rozwiązuje go
instytucja. Każdy ruch pieniędzy wymaga zgody kogoś, kto pilnuje
rachunku: bank sprawdza, czy saldo pozwala na przelew; giełda sprawdza,
czy zlecenie ma pokrycie. Skoro nikt nie pilnuje rachunku — co go
pilnuje?

:::warning Jak bez pośrednika?
Każdy ruch wymaga zgody na stan rachunku. Bank jest tą zgodą. Jeśli banku
nie ma, to zgoda musi być *w samym rachunku* — w regułach, które
określają, kto i pod jakim warunkiem może zmienić saldo.
:::

## Definicja

**Decentralized Finance (DeFi)** to usługi finansowe, w których rolę
pośrednika pełni program on-chain. Program trzyma środki, egzekwuje reguły
i rozlicza strony — bez firmy, która by go nadzorowała, i bez konta,
które trzeba by u niej założyć. Dwie cechy odróżniają DeFi od
klasycznego fintechu, który też „automatyzuje finanse":

- **Permissionless.** Z programu może korzystać każdy, kto ma portfel.
  Nie ma weryfikacji tożsamości, nie ma listy dozwolonych krajów, nie ma
  operatora, który może odmówić. Program nie wie, kim jest wywołujący, i
  nie ma jak tego sprawdzić.
- **Composable.** Programy wywołują się nawzajem. Protokół pożyczkowy
  może przyjąć jako zastaw token wyemitowany przez protokół wymiany, a
  trzeci program może połączyć oba w jedną transakcję — bez umowy między
  autorami, bo kod jest publiczny, a wywołanie nie wymaga zgody.

:::tip Dwa przykłady
Wymiana 100 USDC na SOL trwa kilka sekund i nie wymaga konta na giełdzie —
frontend buduje transakcję, portfel ją podpisuje, program wymiany
rozlicza. Wpłata USDC do protokołu pożyczkowego zaczyna naliczać odsetki
w tym samym slocie, w którym transakcja weszła do bloku — bez wniosku,
bez umowy, bez okresu wypowiedzenia.
:::

## Token to saldo z regułami

Żeby program mógł trzymać i przenosić wartość, wartość musi mieć jakąś
postać na łańcuchu. Złoty czy dolar istnieją, bo bank centralny i banki
komercyjne prowadzą rejestry posiadaczy — bez rejestru nie ma waluty.
Solana zna jeden mechanizm zapisu wartości: **konto z saldem**. Saldo
SOL to pole `lamports` w koncie, o którym mówi rozdział [Anatomia
konta](../05-konta/01-anatomia-konta.md). Ale SOL to tylko jedna waluta,
a finanse potrzebują wielu.

Rozwiązanie jest takie samo jak w banku, tylko bez banku. Program —
konkretnie **Token Program**, wbudowany program Solany — prowadzi rejestr
posiadaczy dowolnej liczby walut. Każda waluta to jedno konto zwane
**mintem**, które opisuje jej reguły: ile jednostek istnieje, ile miejsc
po przecinku, kto może dodrukować. Każdy posiadacz ma osobne konto z
saldem tej waluty. Saldo bez banku, z regułami zapisanymi w kodzie
programu — to jest **token**.

Listing 3-1 pokazuje mint najczęściej używanego tokena na Solanie,
odczytany z sieci głównej.

```bash
$ spl-token display EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v --url mainnet-beta

SPL Token Mint
  Address: EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v
  Program: TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA
  Supply: 7822834354886353
  Decimals: 6
  Mint authority: BJE5MMbqXjVwjAF7oxwPYXnTXDyspzZyt4vwenNw5ruG
  Freeze authority: 7dGbd2QZcCKcTndnHcTL8q7SMVXAkp688NTQYwrRCrar
```

<div className="listing"><strong>Listing 3-1.</strong> Mint USDC na sieci głównej. Pięć pól to cały „regulamin" tej waluty; rejestr posiadaczy to miliony osobnych kont.</div>

Każde pole to jedna reguła. `Program` mówi, który kod egzekwuje te
reguły — Token Program, ten sam dla wszystkich tokenów. `Supply` to
łączna liczba jednostek w obiegu, zapisana w najmniejszej jednostce;
przy `Decimals: 6` liczba 7 822 834 354 886 353 oznacza 7,8 miliarda USDC.
`Mint authority` to klucz, który może dodrukować — dla USDC jest to
emitent, firma Circle, bo USDC jest tokenem zabezpieczonym dolarem w
banku. `Freeze authority` to klucz, który może zamrozić konto posiadacza;
USDC go ma, bo emitent podlega regulacjom. Token bez tych dwóch
uprawnień — z `authority` ustawionym na brak — ma stałą podaż i nikt nie
może nikomu zablokować środków. Obie decyzje są publiczne i sprawdzalne
przed pierwszym użyciem.

Token może oznaczać cokolwiek, co ma reguły i posiadaczy: walutę, udział
w puli płynności, głos w zarządzaniu protokołem, bilet wstępu. Dla
programu DeFi wszystko to jest tym samym — kontem z saldem, które można
przenosić za zgodą posiadacza.

:::tip Analogia — żeton w kasynie
Żeton ma wartość tylko w tym kasynie, które go wydało. Reguły — ile
żetonów istnieje, na co można je wymienić, kto może wydać nowe — zna
kasyno, nie bank. Token on-chain działa tak samo, tylko kasynem jest
kod, a reguły każdy może przeczytać przed wejściem.
:::

Jest więc waluta i jest rejestr bez banku. Pierwszy filar obietnicy —
wymiana — wymaga jeszcze jednego: sposobu ustalenia **ceny** bez giełdy,
która dopasowuje kupujących do sprzedających. To temat następnego
rozdziału.
