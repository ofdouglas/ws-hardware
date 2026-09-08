---
id: ADR-046
title: Communications measurement headers
status: accepted
scope: Board 1 Rev A measurement access
created: 2026-09-07
accepted_on: 2026-09-07
accepted_by: Explicit maintainer instruction USR-38 in this conversation
supersedes: ADR-039 (communications copper-testpad scope only)
superseded_by: none
requirements: [B1-R008, B1-R004]
questions: [B1-Q004]
sources: [USR-38]
---

# ADR-046: Communications measurement headers

The maintainer requests: “communications test points should use 2-pin 0.1\" headers” and “we need test points for the UART ring”, then supplies the seven interface arrangements below. This explicitly authorizes replacing communications copper pads and adding three UART-ring observation headers. It supersedes only the communications copper-pad portion of ADR-039; ordinary rail/reset/boot/core pads, fitted ground headers and its other surviving decisions remain.

| Header | Interface | Pin 1 | Pin 2 |
|---|---|---|---|
| J19 | CAN A | FD_CAN_A_H | FD_CAN_A_L |
| J20 | CAN B | FD_CAN_B_H | FD_CAN_B_L |
| J21 | RS-485 | RS485_A | RS485_B |
| J22 | SAM0 → SAM1 UART ring | RING_01 | GND |
| J23 | SAM1 → SAM2 UART ring | RING_12 | GND |
| J24 | SAM2 → SAM0 UART ring | RING_20 | GND |
| J25 | Shared UART_MD | UART_MD | GND |

Retire TP13–TP19 without reusing their designators. Retain TP1–TP12 and the six dedicated two-post ground headers J13–J18. B1-B011 therefore has twelve PCB pads and no purchased components. New stable BOM item B1-B084 contains seven fitted headers. Reuse the already selected Sullins PRPC002SAAN-RC and its 1×2 2.54 mm vertical through-hole footprint as a routine implementation choice, not a separately maintainer-specified MPN. Existing manufacturer references are in [termination notes](../../boards/board1/termination.md).

Place headers near the measured link with short observation branches, reasonable clip clearance, concise function/polarity silkscreen and nearby ground access for differential headers. UART headers carry their own ground. These are observation connectors, not termination jumpers; fit no shunts. No resistor, PHY, protection or termination circuit changes follow from this decision. Layout approval checks physical access, polarity and routing; link waveform qualification remains bring-up work. Header selection does not assert ERC/DRC, mechanical qualification or hardware validation.

The alternatives were retaining the copper pads or using larger connectors. The requested 1×2 headers provide removable probe/lead access with a small conventional footprint and add seven purchased pieces. No additional architecture review is needed for this bounded bench-access change.
