---
id: ADR-022
title: Fast TPS22810 input ramp without external FTDI supervisor
status: accepted
scope: Board 1 Rev A input
created: 2026-09-06
accepted_by: User accepted TPS22810 with CT 47 nF and requested current design
supersedes: ADR-019 CT value; ADR-020 external FTDI supervisor
superseded_by: none
---

# Decision

Use TPS22810DBVT, CT=47 nF, EN tied to VIN, QOD tied to VOUT. Retain SMF6.0A raw TVS, direct 1 uF bypass and shunt series 1 ohm/4.7 uF damping. Remove TLV803EA42RDBZR and its dedicated supply bypass. Retain FTDI RESET# 10 kohm to independent FTDI 3.3 V and existing 10 nF to ground. TPS560430X3FDBVR remains selected by ADR-021. PWREN# through a default-off inversion interface enables the buck after configuration and disables it during suspend/reset/unpowered states.

Nominal CT sizing gives 4.03 ms 10–90% at 5 V and about 5 ms full ramp, not guaranteed timing. This removes the intentionally slow 100 ms ramp; ordinary initial USB enumeration is expected to follow rail settling. Qualification must cover power-on, interrupted supply/replug, suspend/resume, reset defaults and USB current. No overvoltage supervisor, polarity blocking or external power is added. TPS22919 is not selected.

# Authority and checks

[Current circuit and operating points](../../boards/board1/usb_input.md) owns implementation details and remaining questions. Part selection is not hardware qualification. CT timing is typical; input-transient attenuation does not guarantee an FTDI-safe clamp during already-on events. Revisit on measured failures, inadequate margin or changed supply scope, not preference alone.
