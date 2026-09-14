---
title: Portfel jako tożsamość
description: Para kluczy zamiast loginu i hasła — jak podpis dowodzi tożsamości bez serwera, sprawdzony na prawdziwym kluczu, i co to zmienia w UX aplikacji.
sidebar_position: 4
slug: portfel-jako-tozsamosc
---

# Portfel jako tożsamość

W Web2 tożsamość to rekord w bazie operatora: login, hash hasła, adres
e-mail. Serwer sprawdza hasło i od tej chwili „wie", kto wysyła żądania.
W Web3 nie ma serwera ani bazy, a mimo to każdy węzeł musi umieć
stwierdzić, czy transakcję wysłał właściciel konta. Ten rozdział wyjaśnia,
jak to możliwe, i dlaczego odpowiedź zmienia sposób projektowania
aplikacji.

## Para kluczy

Tożsamość w Web3 nie jest przechowywana nigdzie — jest **posiadana**.
Użytkownik ma parę liczb wygenerowanych razem: **klucz prywatny** i
**klucz publiczny**. Klucz publiczny da się wyliczyć z prywatnego; w
drugą stronę się nie da. Klucz publiczny jest **adresem** — to ten ciąg
znaków w base58, który pojawiał się we wszystkich dotychczasowych
listingach. Można go pokazywać każdemu; służy do tego, żeby inni mogli
wysłać coś na to konto i sprawdzić, co z niego wyszło. Klucz prywatny
nigdy nie opuszcza urządzenia użytkownika i służy do jednego: składania
**podpisu**.

Podpis to wynik operacji matematycznej na dwóch wejściach — treści
transakcji i kluczu prywatnym. Ma dwie własności, na których opiera się
cała reszta: każdy, kto zna klucz publiczny, może **sprawdzić**, że podpis
złożono odpowiadającym mu kluczem prywatnym, choć sam nie potrafi takiego
podpisu złożyć; a zmiana choćby jednego bajtu treści unieważnia podpis.
Węzeł, który dostaje transakcję, nie musi pytać nikogo, kim jest nadawca.
Bierze klucz publiczny z transakcji, bierze podpis, sprawdza — i wie.

<div className="diagram">

![Transakcja jest podpisywana kluczem prywatnym; podpisaną transakcję każdy może zweryfikować kluczem publicznym](/img/diagrams/1_paradigm-07.svg)

</div>

Listing 2-6 pokazuje ten mechanizm na kluczu wygenerowanym na potrzeby
tego rozdziału. Polecenie `sign-offchain-message` podpisuje dowolny
tekst; `verify-offchain-signature` sprawdza podpis, mając tylko klucz
publiczny.

```bash
$ solana sign-offchain-message "Logowanie do aplikacji X" --keypair demo.json
4mNAR8bE8L3QHUQ22QBN1Vb9uQdK84pM4c36nsoqA4ZCCsRk5wPMLMVKQpiZsqN3MKdZLPTczNeiTTCVwhZC7rix

$ solana verify-offchain-signature "Logowanie do aplikacji X" \
    4mNAR8bE8L3QHUQ22QBN1Vb9uQdK84pM4c36nsoqA4ZCCsRk5wPMLMVKQpiZsqN3MKdZLPTczNeiTTCVwhZC7rix \
    --signer HDT6d92i8AJQet2Z2MuagpVBzFsVswS9YneEQMzcypDK
Signature is valid

$ solana verify-offchain-signature "Logowanie do aplikacji Y" \
    4mNAR8bE8L3QHUQ22QBN1Vb9uQdK84pM4c36nsoqA4ZCCsRk5wPMLMVKQpiZsqN3MKdZLPTczNeiTTCVwhZC7rix \
    --signer HDT6d92i8AJQet2Z2MuagpVBzFsVswS9YneEQMzcypDK
Error: Invalid signature
```

<div className="listing"><strong>Listing 2-6.</strong> Podpis wiadomości kluczem prywatnym i dwie weryfikacje kluczem publicznym. Zmiana jednej litery w treści (X → Y) unieważnia podpis.</div>

Pierwsze polecenie potrzebowało pliku z kluczem prywatnym. Dwa następne
potrzebowały tylko adresu (`--signer`) — to jest dokładnie sytuacja
węzła, który weryfikuje transakcję: ma treść, ma podpis, ma klucz
publiczny nadawcy, i to wystarcza. Trzecie polecenie pokazuje, dlaczego
podpisu nie da się „przenieść" na inną transakcję: ten sam podpis dla
innej treści jest nieważny.

To samo dzieje się w Listingu 2-4: pole `signatures` to podpis złożony
pod `message`, a `accountKeys[0]` to klucz publiczny, którym każdy
walidator go sprawdził, zanim w ogóle zaczął wykonywać przelew.

## Portfel

Klucz prywatny to 32 bajty, których nie da się zapamiętać ani bezpiecznie
przepisywać. Przechowuje go i używa **portfel** — program, który trzyma
klucze i podpisuje transakcje w imieniu użytkownika. W przeglądarce to
rozszerzenie takie jak Phantom; w terminalu to plik z kluczem, jak
`demo.json` w Listingu 2-6; w wersji najbezpieczniejszej — osobne
urządzenie, które nigdy nie pokazuje klucza komputerowi.

Gdy aplikacja Web3 chce coś zapisać, nie prosi użytkownika o hasło.
Buduje transakcję i przekazuje ją portfelowi; portfel pokazuje
użytkownikowi, co ma podpisać, i po zatwierdzeniu zwraca podpisaną
transakcję. Aplikacja nigdy nie widzi klucza prywatnego — widzi tylko
podpisy. Portfel jest więc **loginem** do każdej aplikacji naraz: jedna
para kluczy, tysiące serwisów, zero formularzy rejestracji.

:::tip Analogia — podpis odręczny
Podpis odręczny dowodzi tożsamości, bo tylko jedna osoba umie go złożyć,
a każdy może go porównać ze wzorem. Podpis kryptograficzny jest lepszy w
jednym i gorszy w jednym: nie da się go podrobić — ale nie ma też
urzędu, który wyda nowy, gdy ręka przestanie działać.
:::

## Konsekwencje UX

Przeniesienie tożsamości z bazy operatora do portfela użytkownika zmienia
kilka rzeczy, które w Web2 uchodzą za oczywiste.

**Nie ma ekranu „zapomniałem hasła".** Nie dlatego, że nikt go nie
zaprojektował, tylko dlatego, że nie ma kto go obsłużyć. Serwer, który
mógłby zresetować dostęp, musiałby mieć klucz — a wtedy tożsamość
należałaby do niego, nie do użytkownika.

**Tożsamość jest przenośna.** Ten sam portfel loguje do giełdy, do gry,
do aplikacji pożyczkowej i do narzędzia, które powstanie za rok. Historia
użytkownika — jego konta, tokeny, transakcje — jest publiczna i
przypisana do adresu, więc nowa aplikacja może ją odczytać od pierwszej
sekundy, bez importu danych i bez zgody poprzedniej aplikacji.

**Użytkownik jest właścicielem tożsamości, nie operator.** Aplikacja nie
może zablokować konta, bo konto nie jest jej. Może odmówić obsługi w
swoim interfejsie — ale program on-chain, który stoi za interfejsem,
odpowie każdemu, kto wyśle poprawnie podpisaną transakcję.

**Onboarding jest krótszy.** Zamiast formularza, maila weryfikacyjnego i
hasła jest jedno kliknięcie „połącz portfel". Wszystko, co aplikacja
musi wiedzieć o użytkowniku, to adres.

:::warning Cena suwerenności
Utrata klucza prywatnego to utrata dostępu — bez odwołania, bez
infolinii. Kradzież klucza to kradzież wszystkiego, co pod nim leży.
Ekosystem projektuje wokół tego całą warstwę zabezpieczeń: frazę
odzyskiwania, portfele sprzętowe, multisig. Rozdział
[Phantom](../07-portfel-i-narzedzia/02-phantom.md) pokazuje, jak wygląda
to w praktyce i czego nie wolno zrobić z frazą.
:::

Wszystkie elementy nowej architektury są już na stole: klient, portfel,
węzeł RPC, klaster, program, konta. Ostatni rozdział układa je w jeden
łańcuch i odpowiada na pytanie, które dla dewelopera jest
najważniejsze — które z tych ogniw pisze on sam.
