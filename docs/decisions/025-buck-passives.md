---
id: ADR-025
title: TPS560430 local passive selections
status: accepted
scope: Board 1 Rev A buck
created: 2026-09-06
accepted_by: Explicit user instruction to commit to all proposed buck passives
supersedes: ADR-021 provisional passive choices
superseded_by: none
---

# Decision

Accept Bourns SRN6045TA-120M (12 uH) as B028, TDK C3216X7R1V106K160AC (10 uF 35 V) as B029, TDK C3225X7R1C226M250AC (22 uF 16 V) as B030, and KEMET C0805C104K5RACTU (100 nF 50 V) for B031 and B052. Five installed components, four unique MPNs. Exact connections and evidence are in boards/board1/buck_tps560430.md.

Acceptance freezes part choices, not electrical qualification. Retain effective-capacitance, LC stability, transient, hot-inductor, startup, layout and full-load USB-current checks. The output capacitor is +/-20%; do not apply the historical all-capacitors +/-10% upper-bound calculation to it. No SC189 30 uF ceiling applies. Do not reopen these choices for light-load efficiency or BOM consolidation alone.

No additional general-purpose bypass MPNs, resistor values, crystal load values or SAM core-capacitor substitutions are accepted by this decision. See https://github.com/ofdouglas/ws-hardware/blob/dbcaba10831ade0516dba825d2c97d3f0017e0f5/boards/board1/passive_review.md for remaining selections and consolidation candidates.
