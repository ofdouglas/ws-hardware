---
id: ADR-039
title: Bias and LED resistors, UART support, headers and test access
status: accepted
scope: Board 1 Rev A
created: 2026-09-06
accepted_on: 2026-09-06
accepted_by: Explicit maintainer instruction USR-33
supersedes: none
superseded_by: ADR-041 (header/general-breakout clauses only); ADR-046 (communications copper-testpad scope only)
requirements: [B1-R003, B1-R008, B1-R019, B1-R020, B1-R025]
questions: [B1-Q003, B1-Q004, B1-Q009, B1-Q010, B1-Q014]
sources: [USR-33]
---

# ADR-039: BOM closeout selections

Accept two TE CRGP0805F330R for RS-485 bias B1-B071 and five KOA RK73H2ATTD3301F LED resistors B1-B026.

Accept the multidrop support plan: four Stackpole RMCF0805FT10K0 pull-ups from driver /OE to 3V3_SYS in B1-B008, and one RMCF0805FT470R shared UART_MD bus pull-up in B1-B074. The second SN74LV125APWR and allocated bypass remain separately counted. Acceptance does not qualify a baud rate or rail-ramp behavior.

Accept the header plan: four 1x5 GPIO headers (four GPIOs plus ground per MCU) and four 1x3 debug UART headers from one PRPC040SAAN-RC 40-position strip. B1-B027 is the one-strip purchasing allocation; B1-B059 is four cut placement pieces included in that strip, not four extra purchases. 32 positions are allocated; actual cuts and final GPIO mux remain to verify. No GPIO series-resistor MPN is accepted by agreeing to the header plan.

Accept ordinary PCB signal/rail test pads B1-B011, with no purchased component for those pads. The maintainer additionally requires fitted pins for scope-probe ground clips, recorded separately as B1-B075. Exact pin MPN, count and positions remain TBD until layout/clip access is resolved. Spare strip posts are a proposal only; do not assume their consumption or silently add a new connector purchase.

[Closeout review](https://github.com/ofdouglas/ws-hardware/blob/dbcaba10831ade0516dba825d2c97d3f0017e0f5/boards/board1/bom_closeout.md) supplies part and sourcing references. Retain thermal, bias, reset, timing, GPIO load and debug power-off qualification questions. No ERC/DRC or hardware validation was performed; evidence remains unverified.

Header/general-breakout clauses are partially superseded by [ADR-041](041-timing-debug-headers.md). Other decisions remain in force.

The communications copper-testpad scope is superseded by [ADR-046](046-communications-measurement-headers.md). Rail/reset/boot/core copper pads and fitted scope-ground access remain in force.
