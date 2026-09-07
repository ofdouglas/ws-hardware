# Board 1 research dispositions

Status: startup/enable settled by ADR-040; support and CBUS recovery details remain proposals. Updated 2026-09-07.

| Item | Current disposition | Next work |
|---|---|---|
| FTDI startup | Accepted conventional startup, existing RC/ramp, no added supervisor or sequencer | Complete supply/filter/bypass counts and normal programming procedure from the [support proposal](ftdi_support_proposal.md); check startup/replug at bring-up |
| VCP enable | Accepted PWREN# directly to all four LV125 /OE inputs, existing bridge pull-up and buck inverter | Complete receiver defaults and pin wiring; [implementation](vcp_enable_proposal.md) |
| CBUS recovery | [Reset/BOOT0 circuit](cbus_recovery_proposal.md) remains proposed | Resolve specific ROM pin interactions and component/default choices |

[ADR-040](../../../docs/decisions/040-startup-and-vcp-enable.md) supersedes the rail-valid enable prerequisite. The two-monitor/NAND proposal and its combined BOM deltas are withdrawn. [Reassessment](enable_startup_reassessment.md) records the rationale. Acceptance does not imply measurements have occurred or accept the other research parts.

## Allocation changes needed for ROM recovery

ST's ROM bootloader can actively drive **PB14**, currently proposed for RS-485 DE. A passive pull-down cannot override that output. Its I2C use of PC6/PC7 also conflicts with the draft gateway CAN standby controls. The recovery note proposes these changes to currently unused pads:

| Function | Current draft | Proposed replacement | Consequence |
|---|---|---|---|
| RS-485 DE | PB14, pad 36 | PD2, pad 55 / B1-P223 | Software DE with low default; qualify assertion and USART TC-based release at the chosen rate |
| Gateway CAN A standby | PC6 | PB7, pad 60 / B1-P228 | High default until application enables the PHY |
| Gateway CAN B standby | PC7 | PB9, pad 62 / B1-P230 | High default until application enables the PHY |

These are proposed reallocations only. PC8 is not a ROM-unused substitute: the ROM uses it for I2C3. Reconcile the three changes with B1-Q003/005/009/013, the complete simultaneous mux allocation, requirements, interface notes and stable workbook rows together when adopted.

Moving standby controls does **not** settle PA11/PA12's CAN1 versus ROM USB-DFU overlap. A local CAN RX driver can still drive the MCU pad even with its external cable removed; standby does not imply a high-impedance RX output. Resolve whether ROM operation causes contention before approving the recovery wiring; settled sheets can be captured meanwhile. Keep SAM transmitters quiet during USART2 ROM selection, and explicitly disable RS-485 transmission/reception as described in the recovery note. Do not promise that the proposed three pad moves alone solve every ROM interaction.

## Parts and validation

Reconcile only components actually used by the final implementation. The current B036 allocation has two unused auxiliary bypass positions; the proposed CBUS logic would consume one. No monitor/gate bypasses are required. Bridge support counts and receiver pulls remain to be finalized; update the BOM and power model once when those details are adopted.

Check exact pins, defaults, interface levels and ROM compatibility before schematic approval. Normal enumeration, EEPROM programming/readback, suspend/resume and replug checks belong to bring-up. Investigate abnormal timing or faults further only when concrete evidence warrants it. No schematic or hardware validation has been performed.
