---
title: Lending
description: Pytania sprawdzające do tematu Lending.
sidebar_position: 3
slug: lending
---

# Lending — pytania kontrolne

Materiał do tych pytań: [Lending](../03-defi/04-lending.md). Jedna poprawna odpowiedź na pytanie.

## Pytania

1. Co oznacza **overcollateralization** (nadzabezpieczenie) i dlaczego
   protokoły lendingowe na Solanie tego wymagają? Czego konkretnie blockchain
   nie wie o pożyczkobiorcy, co zmusza protokół do takiego rozwiązania?

   - **A.** Zastaw < pożyczka; blockchain nie zna ceny tokenów
   - **B.** Zastaw > pożyczka; blockchain nie zna tożsamości ani historii kredytowej; brak windykacji sądowej
   - **C.** Zastaw = pożyczka; blockchain nie widzi innych portfeli
   - **D.** Zastaw > pożyczka wyłącznie z powodu wysokich opłat Solany

2. Wyjaśnij mechanizm **likwidacji**. Co się dzieje, gdy wartość zastawu
   spada zbyt nisko? Kto jest **likwidatorem**, dlaczego opłaca mu się
   działać szybko i czy do likwidacji potrzebna jest zgoda pożyczkobiorcy?

   - **A.** Protokół powiadamia pożyczkobiorcę; 24h na uzupełnienie zastawu; zgoda obu stron wymagana
   - **B.** Protokół zawiesza pożyczkę do powrotu ceny; likwidator to smart kontrakt
   - **C.** Likwidator spłaca dług, przejmuje zastaw z dyskontem; bez zgody pożyczkobiorcy; dyskont = zachęta do szybkości
   - **D.** Protokół emituje nowe tokeny pokrywające stratę; stała prowizja niezależna od czasu

3. Czym jest **Health Factor** (HF) i jaka jest jego graniczna wartość, przy
   której pozycja staje się otwarta na likwidację?

   - **A.** $HF = \text{dług}/(\text{collateral} \cdot \text{threshold})$; likwidacja gdy $HF > 1$
   - **B.** $HF = (\text{collateral} \cdot \text{threshold})/\text{dług}$; likwidacja gdy $HF < 1$
   - **C.** $HF = \text{collateral}/\text{dług}$; likwidacja gdy $HF < 2$
   - **D.** $HF = \text{collateral} - \text{dług}$; likwidacja gdy $HF = 0$

<details>
<summary>Klucz odpowiedzi</summary>

1. B
2. C
3. B

</details>
