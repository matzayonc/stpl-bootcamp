---
title: Własność
description: Reguła właściciela, rola podpisu, kto tworzy konta i jak Anchor sprawdza owner i signer — z prawdziwymi komunikatami błędów.
sidebar_position: 2
slug: wlasnosc
---

# Własność

Poprzedni rozdział zakończył się pytaniem: program dostaje konta z
zewnątrz, więc co go powstrzymuje przed zapisaniem czegokolwiek do
cudzego konta? Odpowiedź to jedna reguła runtime'u, która obowiązuje
wszystkie programy bez wyjątku — i jeden mechanizm, którym użytkownik
wyraża zgodę na zmianę.

## Reguła właściciela

Każde konto ma dokładnie jednego właściciela — program wskazany w polu
`owner`. Runtime egzekwuje wokół tego pola trzy zasady:

1. Tylko program-właściciel może **zmienić `data`** konta.
2. Tylko program-właściciel może **zmniejszyć `lamports`** konta.
3. **Każdy** program może zwiększyć `lamports` dowolnego konta, o ile
   konto jest oznaczone w transakcji jako zapisywalne.

Trzecia zasada tłumaczy, dlaczego przelew SOL działa: System Program jest
właścicielem portfela nadawcy, więc może odjąć lamporty; odbiorcy nie musi
być właścicielem, bo dodawać wolno każdemu.

Praktyczna mapa właścicieli wygląda tak:

| Konto | Właściciel |
|---|---|
| portfel użytkownika | System Program (`1111…`) |
| konto tokena, mint | Token Program (`Tokenkeg…`) |
| konto stanu własnej aplikacji | własny program |
| konto programu | loader (`BPFLoaderUpgradeab1e…`) |

Reguła jest egzekwowana **po** wykonaniu instrukcji: runtime porównuje
stan kont przed i po, i jeśli program zmienił bajty konta, którego nie
jest właścicielem, cała transakcja jest odrzucana z błędem
`ExternalAccountDataModified`. Program nie może tego ominąć — to nie jest
konwencja, tylko sprawdzenie na poziomie maszyny wirtualnej.

:::note Właściciel to zawsze program
Użytkownik nigdy nie jest właścicielem konta w sensie pola `owner`. Portfel
„należy" do użytkownika tylko dlatego, że System Program wymaga jego
podpisu, zanim odejmie lamporty. Własność i autoryzacja to dwie różne
rzeczy — i to jest temat następnej sekcji.
:::

## Podpis jako zgoda

Skoro tylko Token Program może zmienić saldo na koncie tokena, to jak
użytkownik decyduje, kiedy jego USDC mają zostać przelane? Przez podpis.

Transakcja niesie listę kont i dla każdego z nich dwie flagi: czy konto
jest zapisywalne (`is_writable`) i czy jego klucz podpisał transakcję
(`is_signer`). Podpis składa się kluczem prywatnym — tym, który leży w
portfelu i nigdy go nie opuszcza (rozdział
[Klucze](../07-portfel-i-narzedzia/01-klucze.md)). Walidator weryfikuje
podpis, zanim w ogóle uruchomi program; program dostaje już tylko flagę.

<div className="diagram">

![User (Signer) → podpis → Token Program (Owner) → zapis → Konto](/img/diagrams/5_accounts-02.svg)

</div>

Przelew tokena składa się więc z dwóch niezależnych sprawdzeń:

- **Signer** — Token Program sprawdza, że konto tokena ma w polu danych
  posiadacza, i że ten posiadacz podpisał transakcję. Bez podpisu
  instrukcja kończy się błędem.
- **Owner** — runtime sprawdza, że to Token Program (a nie inny program)
  zmienił bajty konta tokena. Inny program nie mógłby ich zmienić, nawet
  gdyby użytkownik podpisał.

Oba warunki są konieczne. Podpis bez właściwego programu nic nie da;
właściwy program bez podpisu też nie.

:::tip Analogia — sejf w banku
Skrytkę może fizycznie otworzyć tylko pracownik banku (właściciel), ale
robi to wyłącznie na polecenie klienta, który się podpisze (signer). Klient
nie ma klucza do skrytki, pracownik nie ma prawa jej otworzyć sam.
:::

## Kto tworzy konto

Nowe konto nie pojawia się samo. Tworzy je **System Program** — to jedyny
program, który potrafi zapisać nowy wpis w mapie „adres → konto". Tworzenie
składa się z trzech kroków, które System Program wykonuje w jednej
instrukcji `create_account`:

1. **transfer** — przelewa lamporty z konta płatnika na nowy adres, tyle,
   ile wymaga depozyt za zadeklarowany rozmiar;
2. **allocate** — ustawia długość `data` na zadeklarowaną liczbę bajtów,
   wypełnionych zerami;
3. **assign** — ustawia `owner` na wskazany program.

Po trzecim kroku System Program traci kontrolę nad kontem: właścicielem
jest już program aplikacji i tylko on może zapisać coś w tych bajtach.
Dlatego program, który chce mieć własne konto stanu, musi zawołać System
Program przez **Cross-Program Invocation (CPI)** — wywołanie innego programu
z wnętrza instrukcji. Anchor robi to z deklaracji `init`, co pokazuje
Listing 5-6.

```rust
#[derive(Accounts)]
pub struct Initialize<'info> {
    #[account(init, payer = user, space = 8 + Counter::INIT_SPACE)]
    pub counter: Account<'info, Counter>,
    #[account(mut)]
    pub user: Signer<'info>,
    pub system_program: Program<'info, System>,
}
```

<div className="listing"><strong>Listing 5-6.</strong> Struktura kont dla instrukcji tworzącej konto. Trzy pola odpowiadają trzem rolom: nowe konto, płatnik i program, który je założy.</div>

Każde pole tej struktury odpowiada jednemu elementowi z opisu wyżej:

- `counter` z atrybutem `init` to konto, które ma powstać. Anchor wywoła
  `create_account` i ustawi `owner` na adres bieżącego programu.
- `user` to **płatnik** (`payer`). Musi być `Signer`, bo System Program
  odejmie mu lamporty na depozyt, a odjąć wolno tylko za zgodą. Musi też
  być `mut`, bo jego saldo się zmieni.
- `system_program` to program, który wykona CPI. Anchor sprawdza, że pod tym
  polem faktycznie podano System Program, a nie coś podszywającego się.

Ile lamportów zostanie pobranych i skąd bierze się `8 + Counter::INIT_SPACE`,
wyjaśnia rozdział [Koszt](./04-koszt.md).

## Jak Anchor sprawdza owner i signer

Runtime pilnuje reguły właściciela przy zapisie, ale nie chroni programu
przed **odczytem** fałszywego konta. Gdyby instrukcja `withdraw` czytała
saldo z konta, które podał atakujący, a nie z prawdziwego konta programu,
mogłaby wypłacić środki na podstawie sfabrykowanych danych. Dlatego program
musi sam sprawdzić, czy każde otrzymane konto jest tym, za które się
podaje. W surowej Solanie robi się to ręcznie; Anchor wykonuje to z typu
pola.

Typ `Account<'info, T>` wykonuje dwa sprawdzenia, zanim ciało instrukcji
zobaczy dane:

1. `owner` konta jest równy adresowi bieżącego programu;
2. pierwsze 8 bajtów `data` to **dyskryminator** typu `T` — odcisk nazwy
   struktury, o którym więcej w [Serializacji i
   IDL](../06-transakcje-i-anchor/04-serializacja-i-idl.md).

Typ `Signer<'info>` sprawdza jedno: konto ma ustawioną flagę `is_signer`.
Listing 5-7 pokazuje typową instrukcję, która korzysta z obu typów i
dodatkowo wiąże je ze sobą.

```rust
#[account]
#[derive(InitSpace)]
pub struct Vault {
    pub authority: Pubkey,   // kto może wypłacać
    pub balance:   u64,
}

#[derive(Accounts)]
pub struct Withdraw<'info> {
    #[account(mut, has_one = authority)]
    pub vault: Account<'info, Vault>,
    pub authority: Signer<'info>,
}
```

<div className="listing"><strong>Listing 5-7.</strong> Konto <code>Vault</code> i struktura kont instrukcji <code>withdraw</code>. <code>has_one</code> wiąże pole w danych z podpisem.</div>

Sprawdzenia wykonują się w takiej kolejności:

- `vault: Account<'info, Vault>` — konto należy do tego programu i zaczyna
  się od dyskryminatora `Vault`. Podstawione konto innego programu albo
  innego typu odpada tutaj.
- `authority: Signer<'info>` — klucz `authority` podpisał transakcję.
- `has_one = authority` — pole `vault.authority` jest równe
  `authority.key()`. Bez tego warunku dowolna osoba mogłaby podpisać
  transakcję **własnym** kluczem i wypłacić z cudzego skarbca: dwa
  pierwsze sprawdzenia przeszłyby bez zarzutu.

:::warning Dwa różne „ownery"
Pole `owner` w metadanych konta (program) i pole `authority` w danych
konta (użytkownik) to dwie różne rzeczy. Wiele programów nazywa to drugie
pole `owner`, co prowadzi do pomyłek. W tym kursie pole w danych nazywa
się `authority`, a słowo *owner* oznacza wyłącznie program-właściciela.
:::

## Kiedy sprawdzenie zawodzi

Z komunikatów błędów uczy się najwięcej, a na Solanie są nimi logi
programu. Listing 5-8 pokazuje, co wypisze walidator, gdy ktoś poda do
`withdraw` konto, którego właścicielem nie jest ten program.

```text
Program log: Instruction: Withdraw
Program log: AnchorError caused by account: vault. Error Code: AccountOwnedByWrongProgram. Error Number: 3007. Error Message: The given account is owned by a different program than expected.
Program log: Left:
Program log: 11111111111111111111111111111111
Program log: Right:
Program log: Vau1t11111111111111111111111111111111111111
Program Vau1t11111111111111111111111111111111111111 failed: custom program error: 0xbbf
```

<div className="listing"><strong>Listing 5-8.</strong> Podano portfel (właściciel: System Program) tam, gdzie oczekiwano konta <code>Vault</code>. Anchor wypisuje, co dostał (<code>Left</code>) i czego oczekiwał (<code>Right</code>).</div>

Kilka elementów tego komunikatu warto umieć czytać:

- `caused by account: vault` — nazwa pola ze struktury `Withdraw`, przy
  którym sprawdzenie nie przeszło.
- `Error Number: 3007` i `0xbbf` to ta sama liczba w zapisie dziesiętnym i
  szesnastkowym. Kody 3000–3999 to błędy kont; 2000–2999 to naruszone
  constraints (`has_one`, `seeds`, …); 6000 i wyżej to błędy własne
  programu z `#[error_code]`.
- `Left` / `Right` to porównywane wartości — tutaj rzeczywisty i
  oczekiwany właściciel.

Listing 5-9 pokazuje drugą typową sytuację: konto jest prawidłowe, ale
podpisał ktoś inny niż `vault.authority`.

```text
Program log: Instruction: Withdraw
Program log: AnchorError caused by account: vault. Error Code: ConstraintHasOne. Error Number: 2001. Error Message: A has one constraint was violated.
Program log: Left:
Program log: 5tzFkiKscXHK5ZXCGbXZxdw7gTjjD1mBwuoFbhUvuAi9
Program log: Right:
Program log: 8pY6jCJ6hqZ7fYT5mUeR9K4mDbqBhvyBCwQ4xw3AoDkq
Program Vau1t11111111111111111111111111111111111111 failed: custom program error: 0x7d1
```

<div className="listing"><strong>Listing 5-9.</strong> Naruszony <code>has_one</code>: podpisujący nie jest tym, kogo skarbiec ma zapisanego jako <code>authority</code>.</div>

Transakcja, w której padł taki błąd, nie zmienia niczego — cofa się w
całości, jak opisuje rozdział
[Transakcja](../06-transakcje-i-anchor/01-transakcja.md). Opłatę sieciową
płaci się mimo to.

:::warning Brak sprawdzenia to najczęstsza luka
Większość historycznych exploitów na Solanie to brakujący owner check albo
signer check: program ufał kontu, którego nie zweryfikował. W Anchorze
typy `Account` i `Signer` załatwiają to z deklaracji — ale tylko wtedy,
gdy nie zastąpi się ich typem `UncheckedAccount`, który świadomie pomija
wszystkie sprawdzenia.
:::

Wiadomo już, kto może zmieniać konto i kto musi się na to zgodzić.
Pozostaje pytanie, skąd program ma wiedzieć, **pod jakim adresem** szukać
konta danego użytkownika — bez bazy danych, w której mógłby to
zapisać. To temat następnego rozdziału.
