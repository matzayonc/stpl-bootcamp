---
title: Adres i PDA
description: Dwie drogi do adresu konta — klucz publiczny i Program Derived Address. Jak PDA jest wyliczany, czym jest bump i jak deklaruje się go w Anchorze.
sidebar_position: 3
slug: adres-i-pda
---

# Adres i PDA

Program licznika ma jedno konto na użytkownika. Użytkownik wraca po
tygodniu i chce zwiększyć swój licznik. Skąd program — bezstanowy, bez bazy
danych — ma wiedzieć, pod jakim adresem leży konto tego konkretnego
użytkownika? Odpowiedź na to pytanie to najtrudniejszy mechanizm w modelu
kont Solany i zarazem ten, którego używa się najczęściej.

:::note To jest trudne
PDA to temat, do którego warto wrócić po pierwszym własnym programie.
Sesja live rozkłada go na czynniki pierwsze z kodem w edytorze. Ten
rozdział daje pełny obraz, ale nie oczekuje, że wszystko zostanie
zrozumiane za pierwszym razem.
:::

## Adres z klucza

Najprostsza droga do adresu to ta, którą przeszedł portfel z rozdziału
[Klucze](../07-portfel-i-narzedzia/01-klucze.md). Generator losowy daje
klucz prywatny; z niego krzywa Ed25519 wylicza 32-bajtowy klucz publiczny;
te 32 bajty, zapisane w base58, to adres. Każdy adres tego rodzaju ma
klucz prywatny, którym da się podpisać transakcję.

Tak powstaje adres portfela, ale też adres nowego konta danych: klient
generuje jednorazowy keypair, podaje jego klucz publiczny jako adres
nowego konta i podpisuje transakcję tworzącą oboma kluczami — swoim i
tym jednorazowym. Ten wzorzec działa, ale ma wadę, od której zaczął się
rozdział: adres jest losowy, więc ktoś musi go **zapamiętać**. Na Solanie
nie ma gdzie.

<div className="diagram">

![Dwie drogi do adresu konta: keypair → pubkey, albo dane indeksu → wyliczenie (PDA)](/img/diagrams/5_accounts-03.svg)

</div>

## Adres z wyliczenia

Druga droga odwraca problem. Zamiast losować adres i go zapamiętywać,
program **wylicza** go z danych, które i tak zna: własnego adresu i
kilku wybranych bajtów zwanych **seedami** — na przykład napisu `"counter"`
i klucza publicznego użytkownika. Ten sam program, te same seedy, ten sam
adres — zawsze, na każdym komputerze, bez żadnego zapisu. Taki adres to
**Program Derived Address (PDA)**.

Wyliczenie to hash SHA-256 z trzech elementów:

```text
PDA = sha256( seeds… ‖ bump ‖ program_id ‖ "ProgramDerivedAddress" )
```

Napis na końcu to stały separator domeny; `bump` to jeden dodatkowy bajt,
którego rola wymaga chwili uwagi.

### Bump

Adres wyliczony z hasha to 32 losowo wyglądające bajty. Z około
połowy takich ciągów da się odczytać punkt na krzywej Ed25519 — czyli
istnieje dla nich klucz prywatny, choć nikt go nie zna. Dla PDA to
niedopuszczalne: sens PDA polega na tym, że **nie ma** klucza prywatnego,
więc nikt poza programem nie może za ten adres podpisać. Dlatego
wyliczenie dokłada bajt `bump`, zaczyna od wartości 255 i schodzi w dół, aż
trafi na wynik, który **nie leży** na krzywej. Pierwszy taki bump nazywa
się **kanonicznym** i to jego należy używać.

Listing 5-10 pokazuje to wyliczenie wykonane z CLI dla przykładowego
programu i portfela z poprzednich rozdziałów.

```bash
$ solana find-program-derived-address Vau1t11111111111111111111111111111111111111 \
    string:vault pubkey:5tzFkiKscXHK5ZXCGbXZxdw7gTjjD1mBwuoFbhUvuAi9 --output json
{
  "address": "G4AoEnuGj5nmKgMUrtz9WHB8Byck4FbQUXkePWQuEoKY",
  "bumpSeed": 255
}
```

<div className="listing"><strong>Listing 5-10.</strong> PDA dla seedów <code>"vault"</code> + klucz użytkownika. Pierwszy sprawdzony bump (255) już dał adres poza krzywą.</div>

Wynik jest deterministyczny: to polecenie zwróci ten sam adres za rok i
na innym komputerze. Można to potraktować jak ćwiczenie i sprawdzić.

### PDA, który już się pojawił

Konto USDC z Listingu 5-3 nie miało własnego keypaira. Jego adres jest
PDA programu **Associated Token Account** z seedami: portfel, Token
Program, mint. Listing 5-11 odtwarza to wyliczenie.

```bash
$ solana find-program-derived-address ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL \
    pubkey:5tzFkiKscXHK5ZXCGbXZxdw7gTjjD1mBwuoFbhUvuAi9 \
    pubkey:TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA \
    pubkey:EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v --output json
{
  "address": "FzbcyEZ9m8xjtergWgWDq7mfPoHEbboBF791B6cTpzbq",
  "bumpSeed": 254
}
```

<div className="listing"><strong>Listing 5-11.</strong> Adres konta USDC z Listingu 5-3 wyliczony z trzech seedów. Tym razem bump 255 dał punkt na krzywej i został odrzucony; kanoniczny bump to 254.</div>

To dokładnie ten sam adres, który wcześniej został odczytany poleceniem
`solana account`. Portfel (Phantom, Explorer, każda giełda) nie musi
nigdzie zapisywać, gdzie leży konto USDC użytkownika — wylicza je z
adresu portfela i mintu. To jest praktyczna moc PDA: adres jest **indeksem**
obliczonym z danych, a nie rekordem w bazie.

:::tip Analogia — ścieżka do pliku
Skoro konto to plik, to seedy są jego **ścieżką**: program to katalog,
a kolejne seedy to jej segmenty — `licznik/<adres użytkownika>`. Nikt
nie musi pamiętać, gdzie leży plik, bo ścieżka wynika z tego, czyj jest.
I tak jak w systemie plików, ścieżka musi być **unikalna**: dwa konta
pod tymi samymi seedami to jeden i ten sam adres, więc jeśli licznik ma
być osobny dla każdej pary użytkownik–projekt, oba klucze muszą trafić
do seedów.
:::

## Limity

Wyliczenie ma ograniczenia, które warto znać, zanim coś się nie zmieści:

- najwyżej **16 seedów**, każdy o długości do **32 bajtów** — `Pubkey` ma
  dokładnie 32, więc pasuje; dłuższy napis trzeba skrócić lub zhashować;
- bump zajmuje osobny, siedemnasty slot i zawsze jest ostatni;
- wyliczenie na łańcuchu kosztuje jednostki obliczeniowe — 1 500 CU za
  próbę, więc nieudane bumpy mnożą koszt. Dlatego bump zapisuje się w
  koncie i podaje przy kolejnych wywołaniach, zamiast szukać go za każdym
  razem.

## PDA w Anchorze

W Ruście wyliczenie to jedno wywołanie, pokazane w Listingu 5-12.

```rust
let (pda, bump) = Pubkey::find_program_address(
    &[b"vault", user.key().as_ref()],
    &crate::ID,
);
```

<div className="listing"><strong>Listing 5-12.</strong> Ręczne wyliczenie PDA. <code>crate::ID</code> to adres programu z <code>declare_id!</code>.</div>

W praktyce rzadko wywołuje się to samemu. Anchor pozwala zadeklarować PDA
w strukturze kont constraintami `seeds` i `bump`; wtedy framework wylicza
adres i porównuje go z kontem, które faktycznie przyszło w transakcji.
Listing 5-13 pokazuje pełny cykl: utworzenie konta pod PDA i późniejszy
dostęp do niego.

```rust
#[account]
#[derive(InitSpace)]
pub struct Vault {
    pub authority: Pubkey,
    pub balance:   u64,
    pub bump:      u8,        // zapamiętany kanoniczny bump
}

#[derive(Accounts)]
pub struct Initialize<'info> {
    #[account(
        init,
        payer = authority,
        space = 8 + Vault::INIT_SPACE,
        seeds = [b"vault", authority.key().as_ref()],
        bump,
    )]
    pub vault: Account<'info, Vault>,
    #[account(mut)]
    pub authority: Signer<'info>,
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct Withdraw<'info> {
    #[account(
        mut,
        has_one = authority,
        seeds = [b"vault", authority.key().as_ref()],
        bump = vault.bump,
    )]
    pub vault: Account<'info, Vault>,
    pub authority: Signer<'info>,
}
```

<div className="listing"><strong>Listing 5-13.</strong> Konto <code>Vault</code> pod PDA. Przy <code>init</code> Anchor szuka bumpa; przy <code>withdraw</code> dostaje go z konta.</div>

Różnica między dwiema deklaracjami jest istotna:

- W `Initialize` constraint `bump` bez wartości każe Anchorowi **znaleźć**
  kanoniczny bump (pętla od 255 w dół). Wynik jest dostępny w ciele
  instrukcji jako `ctx.bumps.vault` — to go zapisuje się w polu
  `vault.bump`.
- W `Withdraw` constraint `bump = vault.bump` każe **użyć** zapisanej
  wartości. Anchor wylicza adres jednym hashem i sprawdza, że jest równy
  adresowi konta `vault`. To oszczędza CU i, co ważniejsze, wymusza
  kanoniczny bump — nikt nie podstawi konta pod innym, „legalnym", ale
  niekanonicznym bumpem.

Ciało instrukcji `initialize` zapisuje więc trzy pola:

```rust
pub fn initialize(ctx: Context<Initialize>) -> Result<()> {
    let vault = &mut ctx.accounts.vault;
    vault.authority = ctx.accounts.authority.key();
    vault.balance   = 0;
    vault.bump      = ctx.bumps.vault;
    Ok(())
}
```

<div className="listing"><strong>Listing 5-14.</strong> Instrukcja zapisuje bump wyliczony przez Anchora, żeby kolejne instrukcje nie musiały go szukać.</div>

Gdy ktoś poda do `withdraw` konto pod innym adresem niż wynik wyliczenia,
Anchor odrzuci transakcję, zanim ciało instrukcji się wykona:

```text
Program log: AnchorError caused by account: vault. Error Code: ConstraintSeeds. Error Number: 2006. Error Message: A seeds constraint was violated.
Program log: Left:
Program log: 9rcmWummeg95uB1pGF3wBPTTUNBfKZRWENCocPwHjCGc
Program log: Right:
Program log: G4AoEnuGj5nmKgMUrtz9WHB8Byck4FbQUXkePWQuEoKY
```

<div className="listing"><strong>Listing 5-15.</strong> Podane konto (<code>Left</code>) nie jest adresem wyliczonym z seedów (<code>Right</code>).</div>

## PDA może „podpisać"

Skoro PDA nie ma klucza prywatnego, kto podpisuje w jego imieniu — na
przykład gdy skarbiec ma wypłacić SOL, którego jest właścicielem System
Program? Runtime ma na to regułę: program, z którego adresu wyliczono PDA,
może w wywołaniu CPI oznaczyć to konto jako signer, podając seedy i bump.
Runtime sam sprawdza, że seedy prowadzą do tego adresu. Żaden inny program
ani użytkownik nie jest w stanie tego zrobić.

Ten mechanizm — `invoke_signed` w surowej Solanie,
`CpiContext::new_with_signer` w Anchorze — pozwala programowi być
**depozytariuszem**: trzymać tokeny na koncie, do którego nikt nie ma
klucza, i wypłacać je tylko wtedy, gdy logika programu na to pozwoli.
Praktyczne użycie jest w rozdziale
[Transakcje i Anchor](../06-transakcje-i-anchor/index.md).

:::warning Seedy to interfejs publiczny
Adres PDA wynika z seedów, więc każdy, kto zna seedy, zna adres. To nie
jest luka — konto i tak jest publiczne — ale oznacza, że zmiana seedów po
wdrożeniu programu „gubi" wszystkie istniejące konta. Seedy projektuje
się raz, jak schemat bazy danych.
:::

Wiadomo już, jak konto wygląda, kto może je zmieniać i skąd bierze się
jego adres. Ostatnie pytanie brzmi: ile to kosztuje.
