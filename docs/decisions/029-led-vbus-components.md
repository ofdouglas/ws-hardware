---
id: ADR-029
title: Orange LEDs and raw-VBUS damping components
status: accepted
scope: Board 1 Rev A
created: 2026-09-06
accepted_by: Explicit user instruction "Commit to those candidates."
supersedes: ADR-019 raw damping capacitor dielectric/package and resistor tolerance requirements only
superseded_by: none
---

Accept CSL1901DW1 for four MCU LEDs plus the main-power LED, CL21A475KBQNNNE for B046 (4.7 uF, 50 V, X5R, +/-10%, 0805), and SG73P2BTTD1R0J for B047 (1 ohm, +/-5%, pulse-rated, 1206). X5R replaces X7R for B046 only; 5% replaces 1% for B047. The LED's 0603 body is accepted. Sources and exact allocation are in bom_internal.csv and https://github.com/ofdouglas/ws-hardware/blob/dbcaba10831ade0516dba825d2c97d3f0017e0f5/boards/board1/passive_review.md.

No topology or nominal capacitance changes. At maximum simple capacitor tolerance/temperature screen, B046 is 5.9455 uF; ideal 5.5 V step energy is 89.93 uJ. With Rmin 0.95 ohm, initial power is 31.84 W. Effective capacitance, local temperature, pulse/ringing/repeated-hotplug validation and LED visibility remain open under B1-Q002/010/011. No hardware qualification is claimed.

RK73H2ATTD3301F is a new recommended LED-resistor candidate, not accepted by this instruction. Preserve the approximately 0.5 mA-per-LED budget until actual worst-case current is reconciled.
