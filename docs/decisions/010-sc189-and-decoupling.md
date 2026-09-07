---
id: ADR-010
title: SC189 and Rev A decoupling selection
status: accepted
scope: Board 1 Rev A main converter and decoupling design direction
created: 2026-09-06
accepted_on: 2026-09-06
accepted_by: Explicit user instruction USR-14
supersedes: ADR-008
superseded_by: ADR-021 (converter, filter, output-C ceiling); ADR-026 (026-sam-core-ceramic.md, dielectric restriction only)
requirements: [B1-R012, B1-R023]
questions: [B1-Q002, B1-Q011]
sources: [USR-13, USR-14]
---

## Current authority (editorial reconciliation)

MCU/transceiver bypass allocation, shared STM32 analog bulk and 1 uF SAM bulk remain accepted. [ADR-021](021-tps560430-main-buck.md) replaces SC189, its LC and 30 uF limit; [ADR-025](025-buck-passives.md) fixes the new LC MPNs. [ADR-026 (SAM core)](026-sam-core-ceramic.md) replaces the dielectric restriction, completed by [ADR-027](027-ceramic-capacitor-mpns.md). Use [current decoupling](../../boards/board1/decoupling.md), not the historical 22.61 uF total.

Historical decision text below is retained as the record at acceptance; superseded clauses are not current implementation instructions.


# SC189 and decoupling


Select SC189ZSKTRT with a 2.2 uH inductor and 10 uF local output capacitor. Adopt the revised [decoupling allocation](https://github.com/ofdouglas/ws-hardware/blob/dbcaba10831ade0516dba825d2c97d3f0017e0f5/boards/board1/sc189_decoupling.md): one shared STM32 VDDA/VREF+ 1 uF bulk capacitor and 1 uF local bulk per SAM. Retain small pin bypass capacitors and separate core-rail networks. Preferred decoupling values are 100 nF, 1 uF and 4.7 uF, with electrical exceptions including the buck's 10 uF and VDDA 10 nF. Two 4.7 uF output capacitors were discussed but not adopted.

Preserve independent bridge power, controlled main power and UART isolation. Efficiency matters at full networking load from USB, not light load. Nominal direct output allocation is 22.61 uF, with a 28.602 uF initial-tolerance/temperature upper estimate. Exact component choices must preserve the <=30 uF ceiling and minimum effective capacitance.

This selects design direction and stated categories, not fabrication readiness. DigiKey sourcing, exact capacitor/inductor MPNs, supply pin counts, shared analog capacitor placement, SAM bulk departure, startup/inrush, stability, full-load efficiency and transient performance remain to validate. Do not routinely reopen SC189; revisit only on verified infeasibility or changed requirements. Historical TPS62902-specific parts are excluded from the current BOM population.
