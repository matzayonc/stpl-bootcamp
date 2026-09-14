---
title: Devnet i airdrop
description: Sieć testowa bez wartości kontra mainnet, instalacja Solana CLI i jego konfiguracja, oraz jak dosypać sobie SOL z faucetu — łącznie z limitem, na który można trafić.
sidebar_position: 3
slug: devnet-i-airdrop
---

# Devnet i airdrop

Cały kurs odbywa się na sieci testowej. Tokeny nie mają tam wartości,
więc można je dostać za darmo — i można się mylić bez kosztów. Ten
rozdział przełącza portfel i terminal na tę sieć, instaluje narzędzia,
których używały wszystkie dotychczasowe listingi, i zdobywa pierwsze SOL.

## Devnet vs mainnet

Solana to nie jedna sieć, ale kilka, prowadzonych tym samym
oprogramowaniem z osobnym stanem. Dwie mają znaczenie dla tego kursu.

:::note Devnet
Piaskownica dla deweloperów. Osobny łańcuch, osobne konta, osobne
programy — ten sam kod walidatora i to samo API, co na sieci głównej.
Tokeny testowe **bez wartości**, rozdawane za darmo na żądanie. Cały
kurs, wszystkie ćwiczenia i sesja live odbywają się tutaj.
:::

:::warning Mainnet
Sieć produkcyjna — `mainnet-beta` w nazewnictwie CLI. Tokeny mają
**realną wartość**, każda transakcja kosztuje prawdziwe SOL, każdy błąd
w programie jest publiczny i nieodwracalny. Listingi w rozdziałach
[Blockchain](../01-blockchain/index.md) i [Model kont](../05-konta/index.md)
*czytały* z mainnetu, bo odczyt jest darmowy; kurs nie zapisuje tam
niczego.
:::

Jest jeszcze **testnet** — sieć, na której zespół Solany testuje nowe
wersje walidatora — i **localnet**, czyli walidator uruchomiony na
własnym komputerze. Na kursie wystarczy devnet; jak nie napisano
inaczej, praca odbywa się tam.

Phantom przełącza się na devnet w ustawieniach: *Settings → Developer
Settings → Testnet Mode*, a potem wybór sieci *Solana Devnet*. Od tej
chwili saldo, historia i wszystkie transakcje w rozszerzeniu dotyczą
devnetu; adres portfela pozostaje ten sam, bo klucz nie zależy od sieci.

## Solana CLI

Wszystkie polecenia `solana …` z dotychczasowych listingów pochodzą z
jednego pakietu narzędzi. Listing 7-3 instaluje go i sprawdza wersję.

```bash
$ sh -c "$(curl -sSfL https://release.anza.xyz/stable/install)"
...
$ solana --version
solana-cli 3.1.14 (src:3134055b; feat:534737035, client:Agave)
```

<div className="listing"><strong>Listing 7-3.</strong> Instalacja Solana CLI ze skryptu Anzy (wynik instalatora pominięty). Wersja 3.x jest wymagana przez Anchor 1.0 z rozdziału <em>Transakcje i Anchor</em>.</div>

Skrypt instaluje binaria w katalogu domowym i dopisuje go do `PATH`;
po instalacji zwykle trzeba otworzyć nowy terminal. Wersja 3.x to
generacja CLI, którą rozumie Anchor 1.0 — starsza 2.x nie zbuduje
programu z rozdziału [Mini-program](../06-transakcje-i-anchor/05-mini-program.md).

CLI ma jeden plik konfiguracji, który mówi, z jaką siecią rozmawia i
jakim kluczem podpisuje. Listing 7-4 ustawia oba i pokazuje wynik.

```bash
$ solana config set --url devnet --keypair ~/.config/solana/id.json
Config File: /home/mateo/.config/solana/cli/config.yml
RPC URL: https://api.devnet.solana.com
WebSocket URL: wss://api.devnet.solana.com/ (computed)
Keypair Path: /home/mateo/.config/solana/id.json
Commitment: confirmed
```

<div className="listing"><strong>Listing 7-4.</strong> Konfiguracja CLI: sieć i domyślny klucz. Od tej chwili każde polecenie bez <code>--url</code> idzie na devnet, a każde bez <code>--keypair</code> podpisuje tym plikiem.</div>

`RPC URL` to węzeł z rozdziału [RPC node](../02-web3/02-rpc-node.md) —
publiczny węzeł devnetu; przy większym ruchu warto podmienić go na
dostawcę komercyjnego. `Keypair Path` to plik w formacie z Listingu 7-2;
jeśli nie istnieje, `solana-keygen new` tworzy go pod tą domyślną
ścieżką. `Commitment: confirmed` mówi, na jaki poziom potwierdzenia CLI
czeka po wysłaniu transakcji — *confirmed* to głosy większości, zwykle w
ciągu sekundy; *finalized* to nieodwołalność, kilkanaście sekund
później.

Klucz w Phantomie i klucz w CLI to dwa różne portfele. Na kursie to
wygodne — Phantom do klikania, CLI do skryptów — a przelew między nimi
jest ćwiczeniem w następnym rozdziale.

## Airdrop

Devnet rozdaje SOL na żądanie z **faucetu** (kranu). Trochę SOL jest
potrzebne na opłaty za transakcje i na depozyty za konta z rozdziału
[Koszt](../05-konta/04-koszt.md). Trzy źródła robią to samo:

- `solana airdrop 1` w CLI — na adres z konfiguracji albo podany jawnie;
- `faucet.solana.com` w przeglądarce — dla adresu skopiowanego z
  Phantoma;
- przycisk *Airdrop* w Solana Playground i podobnych narzędziach.

Wszystkie mają limit — typowo 1–2 SOL na żądanie i kilka żądań dziennie
na adres — bo faucet jest publiczny i bez limitu byłby wyczerpany w
minutę. Listing 7-5 pokazuje, jak wygląda trafienie w ten limit.

```bash
$ solana airdrop 1 HDT6d92i8AJQet2Z2MuagpVBzFsVswS9YneEQMzcypDK --url devnet
Requesting airdrop of 1 SOL
Error: airdrop request failed. This can happen when the rate limit is reached.
```

<div className="listing"><strong>Listing 7-5.</strong> Odmowa z powodu limitu — najczęstszy wynik <code>solana airdrop</code> w godzinach szczytu. To nie jest błąd konfiguracji.</div>

Gdy CLI odmawia, faucet w przeglądarce ma osobny limit i często działa;
gdy oba odmawiają, wystarczy odczekać godzinę albo poprosić o przelew z
portfela, który już ma SOL — devnetowe SOL przelewa się tak samo jak
prawdziwe. Sesja live zaczyna się od upewnienia, że każdy ma saldo.

<div className="diagram screenshot">

![faucet.solana.com — formularz z polem na adres portfela i przyciskiem wyboru sieci Devnet](/img/faucet-devnet-crop.png)

</div>

:::tip Demo — faucet.solana.com
Otwórz faucet, wklej adres skopiowany z Phantoma, wybierz *Devnet* i
kwotę, wyślij. Po kilku sekundach saldo w rozszerzeniu zmienia się z 0
na 1 SOL — to pierwsza zmiana stanu na łańcuchu, którą widać, choć
jeszcze nie własna.
:::

Saldo jest niezerowe, sieć jest testowa, terminal skonfigurowany. Został
ostatni krok kursu: wysłać własną transakcję i zobaczyć ją w sieci.
