---
title: Sieci z konsensusem BFT
description: Tysiące niezależnych węzłów, wspólny stan i zaufanie do matematyki zamiast do właściciela.
sidebar_position: 2
slug: konsensus-bft
---

# Sieci z konsensusem BFT

Skoro problemem jest jeden właściciel, rozwiązaniem jest brak właściciela:
stan przechowuje wiele niezależnych węzłów, a zmiana wymaga zgody większości.

## Wspólna sieć

- Tysiące niezależnych węzłów przechowuje ten sam stan
- Żeby zmienić dane, trzeba przekonać **większość sieci**
- Nieszczery węzeł zostaje przegłosowany
- To jest **Byzantine Fault Tolerance (BFT)**

:::tip Efekt
Kod uruchomiony w takiej sieci wykona się **dokładnie tak, jak napisany** —
bez możliwości ingerencji żadnego pojedynczego podmiotu.
:::

## Rejestr BFT

Sama większość nie wystarczy; potrzebny jest jeszcze rejestr, którego nie da
się po cichu przepisać.

- Zmiana bloku kryptograficznie unieważnia kolejne
- Stan sieci jest **publiczny** — każdy może go zweryfikować
- Każda operacja **podpisana kluczem** właściciela

| Prywatny serwer | Blockchain |
|---|---|
| Zaufanie do właściciela | Zaufanie do matematyki |
