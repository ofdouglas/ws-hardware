---
id: ADR-033
title: Second SN74LV125APWR for onboard open-drain UART
status: accepted
scope: Board 1 UART_MD
created: 2026-09-06
accepted_on: 2026-09-06
accepted_by: Explicit maintainer instruction USR-27
supersedes: none
superseded_by: none
requirements: [B1-R003]
questions: [B1-Q003, B1-Q005]
sources: [USR-27]
---

# ADR-033: Second SN74LV125APWR for open-drain UART

## Decision

Select a second Texas Instruments SN74LV125APWR (TSSOP-14) for the shared onboard UART, separate from the existing VCP buffer B1-B016. Record the new device as B1-B066, quantity one. Total board quantity of this MPN becomes two.

Use one channel per MCU: ground A, drive active-low /OE from UART_MD_TX, and join Y to the shared UART_MD bus observed by all four UART_MD_RX inputs. TX high disables the channel; TX low drives ground. This realizes non-inverting open-drain-equivalent behavior without tying actively driven high outputs together. Supply the new chip from 3V3_SYS. All four channels are occupied; neither this device nor the VCP buffer has spare channels for other interfaces.

The maintainer states the MCUs will be fairly close together. This supports a shared quad package but does not establish bus capacitance or a validated rate. The previously proposed LVC07/LCX07 devices are not selected and receive no footprints.

## Implementation and evidence

[TI SCES124O, Rev.O, May 2022](https://www.ti.com/lit/ds/symlink/sn74lv125a.pdf), pp.3, 5–6, 9: PW pin functions, operating/electrical limits, enable/disable timing and truth table. At VCC=3 V, VOL is specified at 8 mA, with a 0.44 V maximum. Ioff is specified for VCC=0; arbitrary rail ramp/brownout operation still needs qualification. Exact CAD footprint and MCU pad/mux compatibility remain unverified.

Allocate one existing 100 nF auxiliary bypass in B1-B036 to B1-B066. Together with B1-B016, two of the four auxiliary reserves are assigned; the B1-B036 total stays unchanged. Support resistors remain in residual B1-B008: four /OE pull-ups and one shared bus pull-up, with 10 kohm and 470 ohm 1% respectively remaining proposed starting values. Their MPNs and final values are not accepted by this IC-selection instruction.

## Consequences and checks

Keep B1-Q003/005 open for reset defaults, MCU VOH/VIH compatibility, leakage, enable/disable timing, aggregate bus capacitance, rise time, low-state current, firmware arbitration and actual baud. Do not infer 12 Mbaud capability from the VCP target. No new nominal bypass capacitance is added; actual driver/pull-up consumption must be reconciled in the power budget. No CAD, ERC/DRC or bench validation was performed.

The accompanying termination question is evaluated separately in [termination proposal](../../boards/board1/termination_proposal.md); it does not decide resistor MPNs, values, jumpers or the RS-485 PHY.
