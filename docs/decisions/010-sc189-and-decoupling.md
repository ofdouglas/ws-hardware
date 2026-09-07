---
id: ADR-010
title: SC189 and Rev A decoupling selection
status: accepted
scope: Board 1 Rev A main converter and decoupling design direction
created: 2026-09-06
accepted_on: 2026-09-06
accepted_by: Explicit user instruction USR-14
supersedes: ADR-008
superseded_by: ADR-021 (converter, local filter and 30 uF ceiling only)
requirements: [B1-R012, B1-R023]
questions: [B1-Q002, B1-Q011]
sources: [USR-13, USR-14]
---

# SC189 and decoupling

Current scope: ADR-021 selects TPS560430X3FDBVR. MCU/transceiver decoupling allocations remain; the SC189-specific circuit and capacitor ceiling below are historical.

Select SC189ZSKTRT with a 2.2 uH inductor and 10 uF local output capacitor. Adopt the revised [decoupling allocation](../../boards/board1/sc189_decoupling.md): one shared STM32 VDDA/VREF+ 1 uF bulk capacitor and 1 uF local bulk per SAM. Retain small pin bypass capacitors and separate core-rail networks. Preferred decoupling values are 100 nF, 1 uF and 4.7 uF, with electrical exceptions including the buck's 10 uF and VDDA 10 nF. Two 4.7 uF output capacitors were discussed but not adopted.

Preserve independent bridge power, controlled main power and UART isolation. Efficiency matters at full networking load from USB, not light load. Nominal direct output allocation is 22.61 uF, with a 28.602 uF initial-tolerance/temperature upper estimate. Exact component choices must preserve the <=30 uF ceiling and minimum effective capacitance.

This selects design direction and stated categories, not fabrication readiness. DigiKey sourcing, exact capacitor/inductor MPNs, supply pin counts, shared analog capacitor placement, SAM bulk departure, startup/inrush, stability, full-load efficiency and transient performance remain to validate. Do not routinely reopen SC189; revisit only on verified infeasibility or changed requirements. Historical TPS62902-specific parts are excluded from the current BOM population.
