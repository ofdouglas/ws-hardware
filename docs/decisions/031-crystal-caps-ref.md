---
id: ADR-031
title: Crystal load capacitors and corrected REF resistor
status: accepted
scope: Board 1
created: 2026-09-06
accepted_by: Explicit user instruction to use RMCF0805FT12K0 and commit to both crystal capacitor MPNs
supersedes: ADR-030 REF resistor MPN only
superseded_by: ADR-044 (33 pF MPN); ADR-045 (27 pF MPN)
---

Use RMCF0805FT12K0 (12 kohm 1%) for B057, resolving the earlier 5% conflict. Accept C0805C330F5GACTU (33 pF) for eight MCU oscillator load capacitors and C0805C270F5GACTU (27 pF) for two FTDI oscillator load capacitors. Both are 0805, C0G, 50 V, 1%. Separate FTDI capacitors from B017; do not double count.

These are accepted initial fitted values. B1-Q008 still covers parasitic loading, drive/startup and frequency qualification; no measured oscillator accuracy is claimed. GPIO series resistors are a new proposal in gpio_breakouts.md, not accepted by this instruction.

## 33 pF sourcing update — 2026-09-07

[ADR-044](044-yageo-crystal-load-capacitors.md) replaces the eight 33 pF KEMET capacitors with YAGEO CC0805FRNPO9BN330. All nominal values, tolerances, 27 pF capacitors and REF resistor decisions remain unchanged.

## 27 pF sourcing update — 2026-09-07

[ADR-045](045-yageo-27pf-crystal-capacitors.md) replaces the two 27 pF KEMET capacitors with YAGEO CC0805FRNPO9BN270. Initial values, tolerances and REF resistor are retained.
