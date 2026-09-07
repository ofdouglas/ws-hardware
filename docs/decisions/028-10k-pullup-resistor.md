---
id: ADR-028
title: Common 10 kohm pull-up resistor
status: accepted
scope: Board 1 FTDI and control support
created: 2026-09-06
accepted_by: Explicit user instruction "Commit to RMCF0805FT10K0."
supersedes: none
superseded_by: none
---

Use Stackpole RMCF0805FT10K0 (10 kohm +/-1%, 0805, 0.125 W) for B051 RESET# and B054 PWREN# pull-ups and the 10 kohm EEPROM pull-up within B017. Do not duplicate B017 quantities or substitute for 12 kohm REF or 47 kohm EN pull-down. At 3.3 V, a held-low pull-up draws 330 uA and dissipates 1.089 mW. Exact MPN is accepted; implementation/footprint/startup qualification remains open under B1-Q002/012. Manufacturer source: https://www.seielect.com/Catalog/SEI-RMCF_RMCP.pdf .

CSL1901DW1, CL21A475KBQNNNE and SG73P2BTTD1R0J are contemporaneous evaluation requests, not accepted selections. See boards/board1/passive_review.md.
