---
title: Anatomia konta
description: Pięć pól każdego konta na Solanie, lamporty i SOL, konta danych kontra konta programów, i jak to wszystko odczytać z łańcucha.
sidebar_position: 1
slug: anatomia-konta
---

# Anatomia konta

Każdy rozdział tej strony zaczyna się od jednego pytania. Tutaj brzmi ono:
*gdzie na Solanie leżą dane?* W Web2 odpowiedź to „w bazie danych firmy".
Na Solanie nie ma firmy ani bazy — jest jedna, globalna mapa
„adres → konto", którą przechowuje każdy walidator. Ten rozdział opisuje,
co dokładnie pod takim adresem leży.

## Jeden pomysł

Na Solanie **wszystko jest kontem**. Portfel użytkownika to konto. Saldo
tokena USDC to konto. Program, który obsługuje te tokeny, to też konto.
Konto to najmniejsza jednostka stanu: komórka pamięci, która ma adres,
saldo i ciąg bajtów.

Ten pomysł wygląda niewinnie, ale ma poważną konsekwencję. Skoro portfel,
token i program są tym samym rodzajem obiektu, to trzeba jakoś odróżnić kod
od danych — i ustalić, kto ma prawo dane zmieniać. Odpowiedź na pierwsze
pytanie mieści się w polach konta; odpowiedź na drugie zajmuje osobny
rozdział, [Własność](./02-wlasnosc.md).

:::tip Analogia — plik
Konto to plik na dysku: ma ścieżkę (adres), rozmiar, zawartość i
właściciela, który ma prawo do zapisu. Cała Solana to jeden system
plików, którego kopię trzyma każdy węzeł.
:::

## Pięć pól

Struktura konta w SDK Solany jest krótka. Listing 5-1 pokazuje ją w
postaci, w jakiej definiuje ją crate `solana-account`.

```rust
pub struct Account {
    pub lamports:   u64,      // saldo w lamportach
    pub data:       Vec<u8>,  // surowe bajty
    pub owner:      Pubkey,   // program-właściciel
    pub executable: bool,     // czy konto zawiera kod?
    pub rent_epoch: u64,      // pole historyczne, nieużywane
}
```

<div className="listing"><strong>Listing 5-1.</strong> Struktura konta w SDK Solany. Adres nie jest polem — to klucz, pod którym konto leży w mapie.</div>

Warto zatrzymać się przy każdym polu, bo do wszystkich pięciu wraca reszta
kursu.

**`lamports`** to saldo konta. Jednostką jest **lamport** — jedna miliardowa
SOL, nazwana od Lesliego Lamporta, autora prac o konsensusie. Saldo jest
liczbą całkowitą bez znaku: nie ma ułamków, nie ma wartości ujemnych.
Konto z jednym SOL ma `lamports = 1_000_000_000`.

**`data`** to zawartość konta jako ciąg bajtów. Sieć nie interpretuje tych
bajtów — dla walidatora `data` to tylko tablica o ustalonej długości.
Znaczenie nadaje im program, który jest właścicielem konta. Dla portfela
tablica ma długość zero; dla konta tokena — 165 bajtów; dla konta
zaprojektowanego w Anchorze — tyle, ile zadeklarowano
w [Koszt](./04-koszt.md).

**`owner`** to adres programu, który ma wyłączne prawo zmieniać `data` i
zmniejszać `lamports`. Każde konto ma dokładnie jednego właściciela i jest
nim zawsze program, nigdy użytkownik. To pole jest sednem następnego
rozdziału.

**`executable`** mówi, czy konto zawiera skompilowany kod programu.
Flagę ustawia loader podczas deploymentu i po ustawieniu nie da się jej
cofnąć.

**`rent_epoch`** to pozostałość po dawnym mechanizmie, w którym sieć
cyklicznie pobierała opłatę za przechowywanie danych. Ten mechanizm już nie
działa, ale pole zostało w strukturze. Można je bezpiecznie ignorować.

:::note Adres to klucz, nie pole
Adres konta (`Pubkey`, 32 bajty) nie jest przechowywany w koncie. Solana
trzyma jedną mapę `adres → Account`; adres jest kluczem w tej mapie.
Dlatego w kodzie Anchora adres pobiera się przez `account.key()`, a nie
przez pole struktury.
:::

## Konto widziane z CLI

Pola z Listingu 5-1 nie są abstrakcją — da się je odczytać jednym
poleceniem. Listing 5-2 pokazuje wynik `solana account` dla portfela
jednej z dużych giełd na mainnecie (adres jest publiczny, jak każdy adres
na łańcuchu).

```bash
$ solana account 5tzFkiKscXHK5ZXCGbXZxdw7gTjjD1mBwuoFbhUvuAi9 --url mainnet-beta
Public Key: 5tzFkiKscXHK5ZXCGbXZxdw7gTjjD1mBwuoFbhUvuAi9
Balance: 1869541.094783318 SOL
Owner: 11111111111111111111111111111111
Executable: false
Rent Epoch: 18446744073709551615
```

<div className="listing"><strong>Listing 5-2.</strong> Portfel giełdowy na mainnecie: brak danych, właścicielem jest System Program.</div>

Wszystkie pola z Listingu 5-1 są tu widoczne. `Balance` to `lamports`
przeliczone na SOL. `Owner` to adres `11111111111111111111111111111111` —
tak wygląda **System Program**, wbudowany program, który jest właścicielem
każdego portfela. `Executable: false` mówi, że to konto danych. `Rent
Epoch` ma wartość maksymalną dla `u64`, co jest umownym oznaczeniem konta
zwolnionego z opłat. Sekcji `data` nie ma, bo portfel nie przechowuje
żadnych bajtów — cały jego stan to saldo.

Listing 5-3 pokazuje dla porównania konto USDC należące do tego samego
portfela — ten sam typ obiektu, ale z zawartością.

```bash
$ solana account FzbcyEZ9m8xjtergWgWDq7mfPoHEbboBF791B6cTpzbq --url mainnet-beta
Public Key: FzbcyEZ9m8xjtergWgWDq7mfPoHEbboBF791B6cTpzbq
Balance: 0.002040003 SOL
Owner: TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA
Executable: false
Rent Epoch: 18446744073709551615
Length: 165 (0xa5) bytes
0000:   c6 fa 7a f3  be db ad 3a  3d 65 f3 6a  ab c9 74 31   ..z....:=e.j..t1
0010:   b1 bb e4 c2  d2 f6 e0 e4  7c a6 02 03  45 2f 5d 61   ........|...E/]a
...
```

<div className="listing"><strong>Listing 5-3.</strong> Konto tokena USDC: 165 bajtów danych, właścicielem jest Token Program.</div>

Trzy rzeczy różnią to konto od portfela. Właścicielem jest **Token
Program** (`Tokenkeg…`), a nie System Program. Pole `data` ma 165 bajtów —
tyle zajmuje struktura, w której Token Program trzyma adres mintu,
posiadacza i saldo; pierwsze 32 bajty (`c6 fa 7a f3 …`) to adres mintu
USDC zapisany binarnie. Saldo w SOL (0.00204) nie jest przypadkowe: to
minimalny depozyt za 165 bajtów, o którym mówi rozdział
[Koszt](./04-koszt.md). Konto tokena nie ma „swojego" SOL — trzyma tylko
tyle, ile sieć wymaga za miejsce. Saldo USDC, które interesuje
użytkownika, leży w bajtach 64–71 pola `data`, a nie w `lamports`.

## Dwa typy kont

Pole `executable` dzieli wszystkie konta na dwie grupy.

| | Konto danych | Konto programu |
|---|---|---|
| `executable` | `false` | `true` |
| `data` zawiera | stan: licznik, saldo, głosy | skompilowany bytecode |
| `owner` | program, który je obsługuje | loader programów |
| Kto tworzy | System Program lub program-właściciel | `solana program deploy` |
| Przykłady | portfel, konto tokena, konto licznika | Token Program, własny program |

Konta danych trzymają stan; konta programów trzymają kod. Jeden program
obsługuje dowolnie wiele kont danych — Token Program ma jedno konto z
kodem i setki milionów kont z saldami. Ta asymetria to podstawa skalowania:
nowy użytkownik to nowe konto danych, a nie nowa kopia programu.

Listing 5-4 pokazuje, jak wygląda konto programu odczytane tym samym
poleceniem.

```bash
$ solana account TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA --url mainnet-beta
Public Key: TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA
Balance: 0.200653906 SOL
Owner: BPFLoaderUpgradeab1e11111111111111111111111
Executable: true
Rent Epoch: 18446744073709551615
Length: 36 (0x24) bytes
0000:   02 00 00 00  27 f1 90 b1  d3 af 98 b8  ce 71 4c 44   ....'........qLD
0010:   e8 ca df f9  f8 fc 45 cb  8e 5f ac 42  02 ef f8 11   ......E.._.B....
```

<div className="listing"><strong>Listing 5-4.</strong> Token Program: <code>executable = true</code>, właścicielem jest loader, a dane to 36 bajtów wskaźnika.</div>

Właścicielem jest **loader** — wbudowany program, który umie uruchomić
kod. Zaskakujące może być pole `Length: 36`: cały Token Program na pewno
nie mieści się w 36 bajtach. Loader używany dzisiaj
(`BPFLoaderUpgradeab1e…`) trzyma program w dwóch kontach: konto programu
zawiera tylko 4-bajtowy znacznik i 32-bajtowy adres drugiego konta —
**ProgramData** — w którym leży właściwy bytecode. Dzięki temu program da
się zaktualizować, podmieniając zawartość ProgramData bez zmiany adresu,
pod którym wszyscy go wywołują. Listing 5-5 pokazuje to samo z perspektywy
polecenia `solana program show`.

```bash
$ solana program show TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA --url mainnet-beta
Program Id: TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA
Owner: BPFLoaderUpgradeab1e11111111111111111111111
ProgramData Address: 3gvYRKWyXRR9xKWe1ZjPhLY5ZJRN7KDB4rFZFGoJfFk2
Authority: none
Last Deployed In Slot: 419472000
Data Length: 108600 (0x1a838) bytes
Balance: 0.75968282 SOL
```

<div className="listing"><strong>Listing 5-5.</strong> Konto ProgramData ma 108 600 bajtów bytecode'u. <code>Authority: none</code> oznacza, że nikt nie może już tego programu zmienić.</div>

`Authority: none` to ważny szczegół dla każdego, kto trzyma środki w
tokenach: Token Program jest **niezmienny** — jego autorzy zrzekli się
prawa do aktualizacji. Program napisany w tym kursie będzie miał w tym
polu adres dewelopera, dopóki ten prawa nie odda.

## Vs Ethereum

Dla kogoś, kto zna Ethereum, powyższy podział jest najważniejszą różnicą
między platformami. W Ethereum kontrakt to jeden obiekt, który trzyma kod
**i** własny stan (`storage`). Na Solanie kod jest w koncie programu, a
stan — w dowolnie wielu oddzielnych kontach danych, które program dostaje
z zewnątrz przy każdym wywołaniu.

<div className="diagram">

![Ethereum: kontrakt = kod + stan. Solana: program → wiele oddzielnych kont danych](/img/diagrams/5_accounts-01.svg)

</div>

Różnica ma konsekwencje praktyczne, do których wraca rozdział
[Transakcje i Anchor](../06-transakcje-i-anchor/index.md):

- Program jest **bezstanowy**. Każde wywołanie musi jawnie wskazać, na
  których kontach ma pracować — to lista kont w instrukcji.
- Dwie transakcje, które dotykają różnych kont, mogą wykonać się
  **równolegle**. Runtime widzi listy kont z góry i wie, że nie kolidują.
- Program nie może „sięgnąć" po konto, którego nie dostał. To ogranicza,
  ale i zabezpiecza: zakres działania każdej instrukcji jest jawny.

:::tip Analogia — funkcja i argumenty
Program to funkcja; konta danych to argumenty i pamięć podane z zewnątrz.
Funkcja nie ma zmiennych globalnych — wszystko, na czym pracuje, przychodzi
w wywołaniu.
:::

Następny rozdział odpowiada na pytanie, które pozostało otwarte: skoro
program dostaje konta z zewnątrz, co powstrzymuje go przed zapisaniem
czegokolwiek do cudzego konta?
