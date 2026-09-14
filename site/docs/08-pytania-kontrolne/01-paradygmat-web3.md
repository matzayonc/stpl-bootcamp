---
title: Paradygmat Web3
description: Pytania sprawdzające do tematu Paradygmat Web3.
sidebar_position: 1
slug: paradygmat-web3
---

# Paradygmat Web3 — pytania kontrolne

Materiał do tych pytań: [Paradygmat Web3](../02-web3/index.md). Jedna poprawna odpowiedź na pytanie.

## Pytania

1. Czym jest **RPC node** i jaką rolę pełni w architekturze Web3? Dlaczego
   frontend nie komunikuje się bezpośrednio z klastrem walidatorów, tylko
   przez węzeł RPC?

   - **A.** Serwer twórcy aplikacji z prywatną bazą użytkowników
   - **B.** Węzeł udostępniający publiczne API HTTP/JSON; okno klienta na łańcuch (analogia: bankomat)
   - **C.** Program lokalny z pełną kopią blockchaina
   - **D.** Smart kontrakt filtrujący transakcje przed klastrem

2. Wyjaśnij różnicę między operacją **read** i **write** w Web3. Która z nich
   wymaga podpisu kluczem prywatnym, która kosztuje opłatę sieciową, a która
   wraca natychmiast bez czekania na potwierdzenie?

   - **A.** Read: gratis, bez podpisu, natychmiastowy; write: podpis, opłata, czeka na potwierdzenie
   - **B.** Obie wymagają podpisu; tylko write kosztuje
   - **C.** Read kosztuje mniej; oba czekają na potwierdzenie
   - **D.** Write gratis; read wymaga podpisu

3. W Web2 użytkownik loguje się hasłem i e-mailem na serwer firmy. Co
   zastępuje ten mechanizm w Web3? Jakie są dwie konsekwencje UX takiego
   modelu — jedna pozytywna i jedna negatywna?

   - **A.** OAuth; pozytywne: prostszy login; negatywne: dostawca może zablokować konto
   - **B.** Para kluczy; pozytywne: tożsamość przenośna; negatywne: utrata klucza = utrata dostępu
   - **C.** Biometria; pozytywne: brak haseł; negatywne: zmiana urządzenia = nowa rejestracja
   - **D.** Zdecentralizowany serwer haseł; pozytywne: brak awarii; negatywne: wolniejszy login

<details>
<summary>Klucz odpowiedzi</summary>

1. B
2. A
3. B

</details>
