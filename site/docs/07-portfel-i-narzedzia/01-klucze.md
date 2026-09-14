---
title: Klucze
description: Co dokładnie leży w portfelu — klucz publiczny jako adres, klucz prywatny jako podpis — pokazane na kluczu wygenerowanym z terminala, i dlaczego nie ma hasła.
sidebar_position: 1
slug: klucze
---

# Klucze

Ten sam portfel podpisze każdą transakcję do końca kursu: airdrop na
devnecie, pierwszy przelew, wdrożenie programu na sesji live. Rozdział
[Portfel jako tożsamość](../02-web3/04-portfel-jako-tozsamosc.md)
wyjaśnił, dlaczego portfel zastępuje login. Ten rozdział pokazuje, co
dokładnie w nim leży — generując klucz z terminala i oglądając go bajt po
bajcie, zanim w następnym rozdziale zrobi to Phantom w tle.

## Para kluczy

Portfel nie przechowuje hasła, tożsamości ani salda. Przechowuje jedną
rzecz: **klucz prywatny** — 32 losowe bajty. Z niego wylicza się
**klucz publiczny** — kolejne 32 bajty, zapisane w base58 jako adres.
Wyliczenie idzie tylko w jedną stronę: z prywatnego da się policzyć
publiczny w mikrosekundę; z publicznego prywatnego nie da się policzyć
wcale, przy żadnej ilości mocy obliczeniowej.

<div className="diagram">

![Portfel trzyma klucz prywatny, z którego wylicza się klucz publiczny będący adresem; strzałka w drugą stronę jest przekreślona](/img/diagrams/7_wallet-01.svg)

</div>

Listing 7-1 generuje parę kluczy narzędziem z Solana CLI.

```bash
$ solana-keygen new --no-bip39-passphrase -o demo2.json
Generating a new keypair
Wrote new keypair to demo2.json
===============================================================================
pubkey: 3XNaX1opSHB821mh5WnTvMz27m4c3KR17DYTEHNhj4Cg
===============================================================================
Save this seed phrase to recover your new keypair:
replace axis chunk noodle borrow receive another real easily flip title assault
===============================================================================
```

<div className="listing"><strong>Listing 7-1.</strong> Nowa para kluczy. Klucz prywatny trafił do pliku, klucz publiczny jest wypisany jako adres, a dwanaście słów pozwala odtworzyć oba. Ten klucz został wygenerowany na potrzeby rozdziału i nigdy nie miał środków.</div>

Trzy rzeczy z tego wyniku wracają wszędzie. `pubkey` to **adres** —
publiczny, można go wkleić do Explorera, podać jako odbiorcę przelewu,
opublikować. Plik `demo2.json` zawiera **klucz prywatny** i nie wolno go
nikomu pokazywać; polecenie nie wypisuje go na ekran celowo. **Seed
phrase** — dwanaście słów — to klucz prywatny zapisany w postaci, którą
człowiek może przepisać na kartkę: z tych słów algorytm odtwarza
dokładnie te same 32 bajty. Rozdział [Phantom](./02-phantom.md) wraca do
frazy, bo to ona jest tym, co użytkownik naprawdę musi chronić.

Listing 7-2 zagląda do pliku i sprawdza, że klucz w nim odpowiada
adresowi.

```bash
$ head -c 60 demo.json
[85,102,53,72,114,192,89,139,37,177,52,26,103,4,243,132,55,4

$ solana-keygen pubkey demo.json
HDT6d92i8AJQet2Z2MuagpVBzFsVswS9YneEQMzcypDK

$ solana-keygen verify HDT6d92i8AJQet2Z2MuagpVBzFsVswS9YneEQMzcypDK demo.json
Verification for public key: HDT6d92i8AJQet2Z2MuagpVBzFsVswS9YneEQMzcypDK: Success

$ solana-keygen verify 3XNaX1opSHB821mh5WnTvMz27m4c3KR17DYTEHNhj4Cg demo.json
Error: Verification for public key: 3XNaX1opSHB821mh5WnTvMz27m4c3KR17DYTEHNhj4Cg: Failed
```

<div className="listing"><strong>Listing 7-2.</strong> Plik z kluczem to tablica 64 bajtów jako JSON (pokazany początek). <code>pubkey</code> wylicza z niego adres; <code>verify</code> składa próbny podpis i sprawdza go podanym adresem.</div>

Plik ma 64 liczby, nie 32: pierwsze 32 to klucz prywatny, kolejne 32 to
dopisany dla wygody klucz publiczny. `solana-keygen pubkey` wylicza adres
z prywatnej połowy — ten sam, który pokazało `new`. `verify` robi coś
więcej: podpisuje kluczem z pliku wiadomość testową i sprawdza podpis
podanym adresem. Dla właściwego adresu — sukces; dla adresu z Listingu
7-1 — porażka, bo to inny klucz. To jest w miniaturze to, co robi każdy
walidator z każdą transakcją.

## Podpis

**Podpis** to 64 bajty wyliczone z treści transakcji i klucza prywatnego.
Każdy węzeł sieci, mając treść, podpis i klucz publiczny nadawcy, może
sprawdzić, że podpis pasuje — bez znajomości klucza prywatnego i bez
pytania kogokolwiek. Zmiana jednego bajtu treści unieważnia podpis; nie
da się więc ani podrobić autora, ani zmienić treści po podpisaniu.
Listing 2-6 w rozdziale [Portfel jako
tożsamości](../02-web3/04-portfel-jako-tozsamosc.md) pokazał to na
wiadomości tekstowej; w transakcji mechanizm jest identyczny, a
podpisywaną treścią jest `message` z Listingu 2-4.

<div className="diagram">

![Klucz prywatny podpisuje transakcję; podpisana transakcja trafia do węzła, który weryfikuje podpis kluczem publicznym](/img/diagrams/7_wallet-02.svg)

</div>

Konsekwencje dla użytkownika są dwie. Podpis jest jednocześnie
identyfikatorem transakcji — ten długi ciąg w base58 z Listingu 2-3, po
którym Explorer ją znajduje. I podpis jest **zgodą**: portfel, który
pokazuje okno „podpisz", pyta w istocie „czy ta treść ma zostać
wykonana w twoim imieniu?". Wszystko, co jest w treści, zostanie
wykonane; nic, czego w niej nie ma, nie może zostać dopisane później.

:::note Dlaczego nie ma hasła
Hasło to sekret, który serwer porównuje z zapisanym wzorem — wymaga
serwera i wzoru. Klucz prywatny to sekret, którego nikt nie porównuje z
niczym: dowodem jego posiadania jest podpis, a sprawdzić go może każdy
bez znajomości sekretu. Nie ma serwera, więc nie ma hasła; nie ma wzoru,
więc nie ma go gdzie ukraść — poza urządzeniem użytkownika.
:::

:::tip Analogia — pieczęć
Pieczęć lakowa dowodzi, kto zamknął list, bo tylko jedna osoba ma
stempel, a odcisk każdy może porównać ze wzorem. Klucz prywatny to
stempel, klucz publiczny to wzór odcisku, a podpis to odcisk na tym
konkretnym liście — na innym liście się nie przyda.
:::

Klucz wygenerowany z terminala jest dobry do testów, ale niewygodny w
przeglądarce. Następny rozdział instaluje portfel, który robi to samo za
użytkownika — i wraca do dwunastu słów.
