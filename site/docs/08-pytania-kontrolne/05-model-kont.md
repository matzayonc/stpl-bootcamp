---
title: Model kont
description: Pytania sprawdzające do tematu Model kont.
sidebar_position: 5
slug: model-kont
---

# Model kont — pytania kontrolne

Materiał do tych pytań: [Model kont](../05-konta/index.md). Jedna poprawna odpowiedź na pytanie.

## Pytania

1. Co oznacza, że konto na Solanie musi być **rent-exempt**? Czy jest to
   opłata cykliczna, czy jednorazowa? Co dzieje się z tymi lamportami, gdy
   konto zostaje zamknięte?

   - **A.** Zwolnienie z opłat na zawsze; bez depozytu; brak zwrotu
   - **B.** Cykliczna opłata co epokę; lamporty przepadają po zamknięciu
   - **C.** Jednorazowy depozyt proporcjonalny do rozmiaru; lamporty wracają po zamknięciu
   - **D.** Jednorazowa opłata niezależna od rozmiaru; lamporty spalane

2. W modelu kont Solany rozróżniamy role **owner** i **signer**. Kto jest
   ownerem zwykłego konta tokena, a kto jest signerem przy przelewie tego
   tokena? Dlaczego program będący właścicielem nie wystarczy do
   autoryzacji?

   - **A.** Owner = Token Program (prawo zapisu); signer = użytkownik (podpis autoryzuje); własność ≠ autoryzacja
   - **B.** Owner = użytkownik; signer = Token Program, który automatycznie zatwierdza
   - **C.** Owner = System Program; signer = Token Program
   - **D.** Owner = użytkownik; signer = użytkownik; program nie ma dostępu do sieci

3. Tworząc konto w Anchorze deklaruje się parametr **`space`**. Co
   reprezentuje ta liczba i co się stanie, jeśli zostanie podana zbyt
   mała wartość, a co — jeśli zbyt duża?

   - **A.** Liczba instrukcji na koncie; za mały = błąd transakcji; za duży = brak efektu
   - **B.** Rozmiar konta w bajtach; za mały = stan się nie zmieści; za duży = przepłacasz rent
   - **C.** Lamporty na rent; za mały = konto nie rent-exempt; za duży = brak konsekwencji
   - **D.** Liczba pól struktury; Anchor dopasowuje automatycznie; za duży = błąd kompilacji

<details>
<summary>Klucz odpowiedzi</summary>

1. C
2. A
3. B

</details>
