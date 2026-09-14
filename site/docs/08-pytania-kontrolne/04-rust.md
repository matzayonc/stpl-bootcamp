---
title: Rust dla Anchora
description: Pytania sprawdzające do tematu Rust dla Anchora.
sidebar_position: 4
slug: rust
---

# Rust dla Anchora — pytania kontrolne

Materiał do tych pytań: [Rust dla Anchora](../04-rust/index.md). Jedna poprawna odpowiedź na pytanie.

## Pytania

1. Jaka jest różnica między pożyczką **`&Vault`** a pożyczką **`&mut Vault`**?
   Ile pożyczek każdego typu może istnieć jednocześnie według reguł
   kompilatora?

   - **A.** `&` = zapis i odczyt; `&mut` = tylko odczyt; dowolna liczba obu
   - **B.** `&` = odczyt; `&mut` = zapis; albo jeden `&mut` albo wiele `&` — nigdy oba naraz
   - **C.** Równoważne; różnią się tylko czasem życia
   - **D.** `&` = kopia danych; `&mut` = wskaźnik; max dwie pożyczki każdego typu

2. Czym różni się typ **`Option<T>`** od **`Result<T, E>`**? Który z nich
   reprezentuje brak wartości, a który operację, która może zawieść? Do
   czego służy operator **`?`** stosowany przy `Result`?

   - **A.** `Option` = brak wartości (`Some`/`None`); `Result` = operacja może zawieść (`Ok`/`Err`); `?` propaguje błąd w górę
   - **B.** `Option` = może zawieść; `Result` = wartość opcjonalna; `?` konwertuje `Result` na `Option`
   - **C.** Oba równoważne; `?` rozpakowuje lub wywołuje `panic!`
   - **D.** `Option` = operacje I/O; `Result` = wartość opcjonalna; `?` to skrót `match Ok`

3. W Ruście nie istnieje słowo kluczowe `class`. Jakie dwa konstrukty
   zastępują klasy znane z innych języków — jeden trzymający pola, drugi
   metody? Co zastępuje **dziedziczenie**?

   - **A.** `enum` (pola) + `fn` (metody); zagnieżdżanie enumów
   - **B.** `struct` (pola) + `impl` (metody); traity zamiast dziedziczenia
   - **C.** `struct` (pola) + `trait` (metody); brak zastępnika dziedziczenia
   - **D.** `mod` (pola) + `impl` (metody); `#[derive]` kopiuje pola

<details>
<summary>Klucz odpowiedzi</summary>

1. B
2. A
3. B

</details>
