---
title: Koszt
description: Rent-exempt jako zwrotny depozyt, wzór na minimalne saldo, tabela rozmiarów typów, InitSpace, realloc i close — z realnymi liczbami z sieci.
sidebar_position: 4
slug: koszt
---

# Koszt

Każdy bajt każdego konta leży na dysku każdego walidatora — dziś jest ich
kilka tysięcy. Gdyby dane były darmowe, sieć zapełniłaby się śmieciami w
tydzień. Dlatego miejsce na łańcuchu ma cenę, a program deklaruje rozmiar
swoich kont świadomie. Ten rozdział pokazuje, ile dokładnie kosztuje
konto, skąd bierze się ta liczba i co się dzieje, gdy zabraknie SOL albo
bajtów.

## Rent

Pierwotnie Solana pobierała **rent** — cykliczną opłatę za przechowywanie
danych, potrącaną z salda konta co epokę. Konto, które miało na saldzie
równowartość dwóch lat opłat, było z niej zwolnione: **rent-exempt**.
Z czasem sieć wyłączyła pobieranie i zostawiła tylko drugi warunek. Dziś
każde konto **musi** być rent-exempt od chwili utworzenia; transakcja,
która zostawiłaby konto poniżej progu, jest odrzucana.

W praktyce oznacza to, że depozyt jest:

- **jednorazowy** — wpłacany przy tworzeniu konta, nigdy więcej;
- **proporcjonalny do rozmiaru** — im więcej bajtów, tym wyższy;
- **zwrotny** — po zamknięciu konta lamporty wracają na wskazane konto.

:::tip To nie abonament
Rent-exempt to kaucja, nie czynsz. Wpłaca się ją raz, a po zamknięciu
konta wraca w całości — tak jak kaucja za mieszkanie, nie jak rata za
hosting.
:::

## Wzór

Minimalne saldo zależy od rozmiaru danych konta powiększonego o stały
narzut na metadane:

$$
\text{minimum} = (\text{rozmiar} + 128) \cdot \text{stawka}
$$

gdzie 128 to bajty narzutu, a stawka to parametr sieci wyrażony w
lamportach za bajt. Aktualną wartość najłatwiej sprawdzić, pytając sieć.
Listing 5-16 robi to dla trzech rozmiarów, które już się pojawiły.

```bash
$ solana rent 0
Rent-exempt minimum: 0.00065024 SOL

$ solana rent 48
Rent-exempt minimum: 0.00089408 SOL

$ solana rent 165
Rent-exempt minimum: 0.00148844 SOL
```

<div className="listing"><strong>Listing 5-16.</strong> Minimalne saldo dla pustego konta, konta licznika z 48 bajtami i konta tokena. Wartości z devnetu i mainnetu we wrześniu 2026.</div>

Z pierwszej linii da się odczytać stawkę: 650 240 lamportów za 128 bajtów
narzutu to **5 080 lamportów za bajt**. Sprawdzenie dla 48 bajtów:
$(48 + 128) \cdot 5080 = 894\,080$ lamportów, czyli 0.00089408 SOL —
zgadza się z drugą linią.

Stawka nie jest stała w czasie. Przez lata wynosiła 6 960 lamportów za bajt
(3 480 za bajt-rok razy dwa lata) i taką liczbę cytuje większość starszych
materiałów. Konto USDC z Listingu 5-3 zostało założone pod starą stawką —
stąd jego saldo 0.00204 SOL, wyższe niż dzisiejsze minimum dla 165
bajtów. Nadwyżka nie przepada; przy zamknięciu konta wróci w całości.

:::note Gdzie żyje ta liczba
Wzór jest w sysvarze `Rent` — koncie systemowym, które program może
odczytać przez `Rent::get()?.minimum_balance(rozmiar)`. Anchor robi to sam
w constraincie `init`. Klient pyta o to samo metodą RPC
`getMinimumBalanceForRentExemption`.
:::

## Rozmiar

Rozmiar konta deklaruje się przy tworzeniu i jest to decyzja, którą warto
podjąć świadomie. Za mało — stan się nie zmieści i instrukcja się wywali;
za dużo — depozyt jest wyższy, niż trzeba. Konto z 1 000 bajtów zapasu
kosztuje 5 milionów lamportów więcej, a przy milionie użytkowników to
5 000 SOL zamrożone bez potrzeby.

### Ile zajmuje pole

Anchor serializuje pola w formacie Borsh (rozdział [Serializacja i
IDL](../06-transakcje-i-anchor/04-serializacja-i-idl.md)), więc rozmiar
każdego typu jest z góry znany:

| Typ | Bajty |
|---|---|
| `bool`, `u8`, `i8` | 1 |
| `u16`, `i16` | 2 |
| `u32`, `i32`, `f32` | 4 |
| `u64`, `i64`, `f64` | 8 |
| `u128`, `i128` | 16 |
| `Pubkey` | 32 |
| `[T; N]` | N · rozmiar(T) |
| `Option<T>` | 1 + rozmiar(T) |
| `enum` | 1 + największy wariant |
| `String` | 4 + długość w bajtach |
| `Vec<T>` | 4 + N · rozmiar(T) |

Dwa ostatnie wiersze wymagają decyzji: `String` i `Vec` mają zmienną
długość, więc trzeba z góry ustalić maksimum. Cztery bajty na początku to
zapisana długość.

### Dyskryminator

Do sumy pól Anchor dokłada **8 bajtów dyskryminatora** na początku konta —
odcisk typu, który sprawdza przy każdym odczycie (rozdział
[Własność](./02-wlasnosc.md)). Stąd wzorzec `space = 8 + …`, który pojawia
się w każdym programie Anchora. Konto `Counter` z polami `authority:
Pubkey` i `count: u64` zajmuje więc $8 + 32 + 8 = 48$ bajtów — dokładnie
tyle, ile sprawdzało polecenie `solana rent 48`.

<div className="diagram small">

![Układ 48 bajtów: 8 B dyskryminator, 32 B authority, 8 B licznik](/img/diagrams/5_accounts-04.svg)

</div>

### `InitSpace` zamiast ręcznego liczenia

Ręczne sumowanie działa, ale rozjeżdża się z kodem przy pierwszej zmianie
struktury. Anchor ma na to makro `#[derive(InitSpace)]`, które wylicza
stałą `INIT_SPACE` z definicji pól. Listing 5-17 pokazuje oba sposoby obok
siebie.

```rust
// Ręcznie: łatwo zapomnieć zaktualizować po dodaniu pola
#[account]
pub struct Counter {
    pub authority: Pubkey,   // 32
    pub count:     u64,      //  8
}
// #[account(init, payer = user, space = 8 + 32 + 8)]

// Z InitSpace: stała liczy się z pól
#[account]
#[derive(InitSpace)]
pub struct Profile {
    pub authority: Pubkey,          // 32
    pub count:     u64,             //  8
    #[max_len(32)]
    pub name:      String,          //  4 + 32
    #[max_len(10)]
    pub friends:   Vec<Pubkey>,     //  4 + 10 * 32
}
// #[account(init, payer = user, space = 8 + Profile::INIT_SPACE)]
// Profile::INIT_SPACE == 32 + 8 + 36 + 324 == 400
```

<div className="listing"><strong>Listing 5-17.</strong> <code>#[max_len]</code> ustala maksimum dla pól o zmiennej długości; bez niego <code>InitSpace</code> nie skompiluje się dla <code>String</code> ani <code>Vec</code>.</div>

`INIT_SPACE` nie zawiera dyskryminatora — `8 +` zostaje w deklaracji.
To celowe: dyskryminator jest cechą konta Anchora, a nie struktury danych.

## Kiedy coś nie pasuje

Dwie rzeczy mogą pójść źle przy tworzeniu konta i obie mają
charakterystyczne komunikaty.

**Płatnik nie ma dość SOL.** System Program odmawia przelewu depozytu i
wypisuje, ile brakuje:

```text
Program 11111111111111111111111111111111 invoke [2]
Transfer: insufficient lamports 412000, need 894080
Program 11111111111111111111111111111111 failed: custom program error: 0x1
```

<div className="listing"><strong>Listing 5-18.</strong> Konto płatnika ma 412 000 lamportów, a depozyt za 48 bajtów wymaga 894 080. Na devnecie ratunkiem jest airdrop.</div>

**Zadeklarowano za mało bajtów.** Anchor tworzy konto o podanym rozmiarze,
ale przy zapisie struktury na końcu instrukcji nie ma gdzie jej zmieścić:

```text
Program log: Instruction: Initialize
Program log: AnchorError occurred. Error Code: AccountDidNotSerialize. Error Number: 3004. Error Message: Failed to serialize the account.
Program Lic1111111111111111111111111111111111111111 failed: custom program error: 0xbbc
```

<div className="listing"><strong>Listing 5-19.</strong> Zapis 48-bajtowej struktury do konta, dla którego zadeklarowano <code>space = 8 + 8</code>. Zwykle winna jest ręczna arytmetyka.</div>

Zbyt duże `space` nie daje żadnego błędu — tylko wyższy depozyt. To
najgorszy rodzaj pomyłki, bo nic jej nie sygnalizuje.

## Zmiana rozmiaru i zamknięcie

Konto nie jest skazane na rozmiar z chwili utworzenia. Dwa constrainty
Anchora pozwalają nim zarządzać; Listing 5-20 pokazuje oba.

```rust
#[derive(Accounts)]
pub struct Grow<'info> {
    #[account(
        mut,
        realloc = 8 + Profile::INIT_SPACE + 320,  // miejsce na 10 kolejnych Pubkey
        realloc::payer = authority,
        realloc::zero = false,
    )]
    pub profile: Account<'info, Profile>,
    #[account(mut)]
    pub authority: Signer<'info>,
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct CloseProfile<'info> {
    #[account(mut, close = authority, has_one = authority)]
    pub profile: Account<'info, Profile>,
    #[account(mut)]
    pub authority: Signer<'info>,
}
```

<div className="listing"><strong>Listing 5-20.</strong> <code>realloc</code> zmienia rozmiar i dopłaca (lub zwraca) różnicę depozytu; <code>close</code> zwraca cały depozyt na wskazane konto.</div>

`realloc` ma dwa limity: konto może urosnąć o najwyżej **10 KiB w jednej
instrukcji** i nigdy nie może przekroczyć **10 MiB**. `realloc::zero`
decyduje, czy nowe bajty mają zostać wyzerowane — to ma znaczenie, gdy
konto wcześniej było większe i zmniejszone, bo stare bajty mogą tam
jeszcze leżeć.

`close` robi trzy rzeczy: przelewa wszystkie lamporty na konto
`authority`, zeruje `data` i przepisuje `owner` na System Program. Po
zamknięciu adres jest wolny — można pod nim założyć nowe konto, także pod
tym samym PDA.

:::warning Zamknięcie bez has_one
`close = authority` sam w sobie nie sprawdza, kto zamyka. Bez `has_one =
authority` (albo innego warunku) każdy podpisany mógłby zamknąć cudze konto
i zgarnąć depozyt. Constraint `close` mówi, *dokąd* idą lamporty, nie
*kto* ma prawo je odebrać.
:::

Projektowanie danych na Solanie to projektowanie kont: jakie pola, jaki
maksymalny rozmiar, pod jakim adresem, kto płaci i kto może zamknąć.
Następny rozdział pokazuje, jak wszystkie te decyzje wyglądają na żywo w
Explorerze.
