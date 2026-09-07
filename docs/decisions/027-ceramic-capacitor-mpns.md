---
id: ADR-027
title: General ceramic capacitor MPNs
status: accepted
scope: Board 1 decoupling and input timing
created: 2026-09-06
accepted_by: User instruction "Use CL21B105KAFNFNE for SAM VDDCORE. Commit to all of the capacitor choices."
supersedes: none; completes category choices and ADR-026 (026-sam-core-ceramic.md) ceramic SAM-core selection
superseded_by: none
---

# Decision

Accept these 0805 X7R ceramic parts, all +/-10%:

| MPN | Value/rating | Allocation |
|---|---|---|
| KGM21NR71E104KT | 100 nF / 25 V | B036/B041 and bridge-domain bypass positions |
| CL21B105KAFNFNE | 1 uF / 25 V | B037/B040/B045 and bridge-domain 1 uF positions |
| GRM21BR71C475KE51L | 4.7 uF / 16 V | B038 and FTDI bulk positions |
| CL21B103KBANNNC | 10 nF / 50 V | B039 and FTDI RESET# capacitor |
| CL21B473KBCNNNC | 47 nF / 50 V | B048 TPS22810 CT |

Retain the accepted ADR-025 buck capacitors and inductor. Do not substitute the 16 V Murata part into B046, which retains its 25 V raw-VBUS requirement and an unresolved exact MPN. T491A105K020AT is excluded by the user's ceramic instruction. Crystal load capacitors and unfinished interface networks are not selected by this decision.

# Qualification and evidence

Exact manufacturer links are recorded in bom.csv. Acceptance freezes MPN selection, not effective capacitance, regulator stability, footprints or hardware performance. SAM VDDCORE remains one separate 1 uF plus 100 nF network per MCU; preserve the datasheet interpretation and qualification boundary in 026-sam-core-ceramic.md. No nominal capacitance or USB-current calculation changes. Bridge support quantities still need enumeration; do not duplicate reserved capacitors.

Resistor candidates RMCF0805FT10K0 and RL1632R-1R00-F are evaluated in https://github.com/ofdouglas/ws-hardware/blob/dbcaba10831ade0516dba825d2c97d3f0017e0f5/boards/board1/passive_review.md, not accepted by this capacitor decision.
