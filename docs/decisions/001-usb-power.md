---
id: ADR-001
title: USB power and independent VCP bring-up
status: accepted
scope: Board 1 Spin A power-domain and UART-isolation architecture
created: 2026-09-06
accepted_on: 2026-09-06
accepted_by: Explicit user approval USR-04
supersedes: none
superseded_by: ADR-013 (main-switch implementation only)
requirements: [B1-R005, B1-R006, B1-R012, B1-R013]
questions: [B1-Q001, B1-Q002, B1-Q007]
sources: [SRC-ARCH sections 7 and 8, USR-01, USR-03, USR-04]
---

# ADR-001: USB power and independent VCP bring-up

## Context / decision
Use USB 2.0 Standard-B for power and a dedicated FT232HL VCP to STM32, following the user's connector preference and on-hand bridge (USR-03). This updates the earlier USB-C proposal; it does not supersede an accepted decision.

Evaluate the on-hand SC189ZSKTRT for 5V_SYS -> 3V3_SYS. Keep the bridge independently USB-powered. A controlled main-board power switch is accepted for enumeration/suspend behavior, consistent with the user-accepted USB-only, active-PC scope in B1-Q007/B1-R013. Power-off isolation between the bridge and STM32 UART is accepted, including TX/RX and RTS/CTS per ADR-005. Exact switch, isolation parts and regulator support circuitry remain implementation work; this acceptance does not freeze SC189 or its passives.

See [USB power/VCP circuit proposal](https://github.com/ofdouglas/ws-hardware/blob/dbcaba10831ade0516dba825d2c97d3f0017e0f5/boards/board1/usb_power_vcp.md) for domains, support components, budget equation, sources and checks. Native MCU USB and the 24 V backbone remain deferred; auxiliary output scope remains B1-Q001.

## Alternatives / consequences
USB-B suits bench assembly and the requested simpler connector. USB-C remains technically possible but is no longer the preferred connector. Reusing FT232HL requires its external support components and programming. A main LDO would simplify the regulator circuit but dissipate more heat at substantial current. An independently powered main board would support operation through USB suspend but changes the power contract.

## Acceptance evidence and remaining implementation checks
USR-04 explicitly accepts the power architecture and UART power-off isolation. B1-Q007 operating scope is resolved; complete B1-Q002 power budget and circuit review. Review current full FTDI/SC189 datasheets, errata and actual silicon; complete support-part selection, pin mapping, input protection, inrush, power-off signal behavior, startup/suspend and UART checks. Budget all four MCUs and selected PHYs. Existing excerpt review is not a finished electrical design approval.

## Revisit trigger
Power-budget failure, incompatible operating-policy needs, verified part limitations, or changed supply/connector requirements.

## Factual correction — USR-11

The historical phrase “on-hand SC189ZSKTRT” above was an incorrect ownership inference. The user does not own SC189; it was only a candidate. FT232HL remains on hand. This correction does not alter the accepted power architecture or select a regulator.

## Implementation superseded — USR-18

ADR-013 removes the separate main switch and selects SN74LV125APWR. Independent bridge power and configuration/suspend scope remain accepted.
