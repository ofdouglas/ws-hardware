---
id: ADR-030
title: Final crystal MPNs, USB-B connector and support resistors
status: accepted
scope: Board 1
created: 2026-09-06
accepted_by: Explicit user selections and declaration that crystal candidates are finalized
supersedes: ADR-017 provisional FTDI MPN status; ADR-024 47 kohm tolerance only
superseded_by: none
---

Accept USB-B1HSB6 (ED2983-ND), RC0805FR-072K2L for EEPROM DO series resistance, and ERJ-6GEYJ473V for the 47 kohm EN pull-down (5% accepted). Finalize ECS-120-18-5PX-CKM-TR for FTDI; retain ECS-120-20-3X-EN-TR for all four MCUs. Crystal loading and electrical qualification remain open.

The user also selected RMCF0805JT12K0 for REF. Record that instruction faithfully, but flag its 5% tolerance against the existing 1% REF requirement: this is an unresolved implementation conflict under B1-Q002, not a verified substitution or waiver. Recommend RMCF0805FT12K0 (1%); no silent replacement approval. EEPROM and REF resistor rows are split from B017 as B056/B057 without adding duplicate quantities.

Crystal capacitors in boards/board1/crystal_networks.md are proposals. The user finalized crystal MPNs, not capacitor values. LED resistor RK73H2ATTD3301F still has no explicit acceptance. Sources remain linked in BOM/research notes; no bench validation claimed.
