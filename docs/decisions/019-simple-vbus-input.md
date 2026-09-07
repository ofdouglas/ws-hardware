---
id: ADR-019
title: Simple slew-controlled USB input
status: accepted
scope: Board 1 Rev A
created: 2026-09-06
accepted_by: User instruction to simplify and finish the previously accepted TPS22810 design
supersedes: ADR-013 direct USB attachment of SC189 input capacitance only
superseded_by: ADR-020 (interim reset supervision, itself superseded by ADR-022); ADR-021 (SC189 references); ADR-022 (CT and reset); ADR-029 (damping dielectric/package/tolerance)
---

## Current authority (editorial reconciliation)

Retain TPS22810 topology, EN-to-VIN, QOD-to-OUT, SMF6.0A and direct bypass plus shunt RC damping. [ADR-022](022-fast-input-ramp.md) selects 47 nF CT and removes the interim [ADR-020](020-ftdi-supply-reset.md) supervisor. The current planning direct downstream allocation is 14.9 uF, not the interim 15.0 uF. [ADR-021](021-tps560430-main-buck.md) replaces SC189; [ADR-027](027-ceramic-capacitor-mpns.md) selects ceramics; [ADR-029](029-led-vbus-components.md) selects the damping branch and its X5R/5% changes. Use [USB input](../../boards/board1/usb_input.md); historical 100 ms/0.695 mA figures no longer apply.

Historical decision text below is retained as the record at acceptance; superseded clauses are not current implementation instructions.



# Decision

Use SMF6.0A on raw VBUS and TPS22810DBVT upstream of both FTDI and SC189. Tie EN to VIN and QOD to VOUT. Fit CT 1 uF for a nominal roughly 100 ms full ramp. Raw input has one direct 1 uF bypass and one shunt series 1 ohm / 4.7 uF damping branch. Retain the 14.9 uF downstream 5 V allocation.

The user asked to charge more slowly, simplify input capacitance to 1 ohm + 4.7 uF, and finish. Engineering implementation retains one direct 1 uF to follow TI's low-ESR bypass guidance. Remove the separate EN delay/discharge network and parallel precharge idea. This supersedes the previous unaccepted detailed passive proposal.

SC189 PWREN# enable policy and SN74LV125APWR remain ADR-013; data ESD remains ADR-015 and scope ADR-016. This switch controls attachment slew, not USB permission or future source selection.

# Evidence and consequences

[Complete circuit, capacitor accounting and qualification checks](https://github.com/ofdouglas/ws-hardware/blob/dbcaba10831ade0516dba825d2c97d3f0017e0f5/boards/board1/vbus_protection_proposal.md). TI's CT formula gives approximately 0.695 mA for the direct 14.9 uF; actual startup timing/current, internal regulator charging and ESD residual voltage are unverified. Exact passive MPNs are open. Selection is not fabrication or compliance qualification.

# Revisit trigger

Failed startup/inrush/transient measurements, component limits or changed supply scope justify revision. Do not reopen settled package/part preferences without new evidence.
