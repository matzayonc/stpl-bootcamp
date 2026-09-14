---
title: Portfel jako tożsamość
description: Para kluczy zamiast hasła — jak działa podpis i co to zmienia w UX.
sidebar_position: 4
slug: portfel-jako-tozsamosc
---

# Portfel jako tożsamość

W Web2 tożsamość to rekord w bazie operatora. W Web3 nie ma operatora, więc
tożsamość musi wynikać z czegoś, co użytkownik posiada sam.

## Portfel jako tożsamość

- Brak hasła — jest **para kluczy**
- **Klucz prywatny** podpisuje transakcję
- **Klucz publiczny** weryfikuje podpis i jest adresem
- Portfel trzyma klucze i podpisuje w imieniu użytkownika

<div className="diagram">

![Transakcja → (klucz prywatny podpisuje) → Podpisana transakcja → (klucz publiczny weryfikuje) → Weryfikacja](/img/diagrams/1_paradigm-07.svg)

</div>

:::tip Analogia
Podpis odręczny nie do podrobienia — ale i bez opcji resetu.
:::

## Konsekwencje UX

- Brak ekranu *„zapomniałem hasła"* — nie ma kto resetować
- Tożsamość **przenośna** — jeden portfel = login do tysięcy aplikacji
- Użytkownik jest **właścicielem** swojej tożsamości, nie operator
- Onboarding krótszy — bez formularzy i maili weryfikacyjnych

:::warning Cena suwerenności
Utrata klucza = utrata dostępu — projektuje się to świadomie
(seed phrase, portfele sprzętowe).
:::
