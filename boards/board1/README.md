# Board 1 — bench MVP

Status: draft · Revision: rev1 planning · Hardware validation: none

Purpose: exercise WS on a gateway and three constrained leaves with simultaneous CAN-FD and UART paths, forwarding and queue-pressure experiments, and bare-metal/RTOS firmware.

[Requirements](requirements.md) own node/link scope, acceptance status and open questions. [Pinmap](pinmap.md) owns allocation/evidence; [readable BOM](BOM.md) and [CSV](bom.csv) are the current planning inventory. Read [ADRs](../../docs/decisions/README.md) before changing architecture.

```text
PC -- USB / dedicated UART VCP -- GW
FD_CAN_A: GW + SAM0 + SAM1 + SAM2
FD_CAN_B: GW + SAM0 + SAM1 + SAM2
UART_MD: GW + SAM0 + SAM1 + SAM2 (open drain)
UART ring: SAM0 -> SAM1 -> SAM2 -> SAM0
RS485_EXT: GW to terminal block
SWD: separate access to GW, SAM0, SAM1, SAM2
```

MCU selections and quantities are accepted in ADR-004 / B1-R001 (USR-15); implementation verification remains open. Rev A networking scope is accepted in ADR-007. Board 1 does not implement the full bench backbone by implication. Draft pin allocations are linked from the pinmap; none are verified and no numeric HostIds are frozen.

See [USB power and VCP proposal](usb_power_vcp.md) for USB-B, the on-hand FT232HL; current main converter is TPS560430 per ADR-021, and accepted Spin A operating scope B1-Q007 (USB-only, active PC required).

## Next design pass

1. Implement the Rev A scope recorded in ADR-007; complete electrical/interface decisions.
2. Resolve power, bus electrical targets and external connectivity (B1-Q002–004).
3. Verify exact MCU resources and allocate pins with debug/clocks preserved (B1-Q005).
4. Select parts, draw schematics, review libraries, then run ERC before layout.

## Bring-up outline — planned, not performed

Inspect assembly and shorts; power with the approved source/current limit; measure rails and startup current; attach SWD to each MCU; confirm VCP; test CAN1 and CAN2 separately; test UART multidrop and each ring hop; then exercise simultaneous links and leaf firmware modes. Record firmware, assembly revision, settings and measurements when hardware exists. Rates and pass thresholds must be defined before testing.

Accepted clock/speed requirements: [clocking.md](clocking.md). Gateway: 168 MHz, 12 Mbaud VCP with TX/RX/RTS/CTS isolation. All four MCUs have external main crystals; onboard UART exact rates remain TBD.

Both CAN buses and one RS-485 port are exposed on signal terminals with ground. [Transceiver shortlist and USB estimate](transceivers_and_power.md) covers Rev A and the future nine-CAN-PHY/two-RS485-PHY scenario.

Board 1 omits the bench multidrop RS-485 port; the overall WS bench retains it. Provide one LED per MCU, one main-power LED, and a few GPIO breakouts per MCU. See ADR-007 and B1-Q010.

## Dual-gateway lab — USR-07

Connect FD_CAN_A, FD_CAN_B and the STM32 RS485_EXT to the user-owned Digi ConnectCore 93 development kit (user reports two CAN-FD and one RS-485 interface). This is the reason to retain Rev A's single external RS-485 while reducing power elsewhere. The kit is external equipment, not an additional Board 1 MCU. Verify exact kit/carrier revision, connector pinouts, signal reference, termination, RS-485 mode and common supported rates before connection. Board 1's 12 Mbps RS-485 ceiling does not imply that the kit supports that rate. Plan individual-link tests followed by simultaneous dual-gateway traffic; no hardware interoperability has yet been tested.

Current main-rail selection: [SC189 decoupling design](sc189_decoupling.md), ADR-010 (accepted design direction). The 90% converter target is accepted; operating envelope and qualification remain B1-Q011.

Proposed next-step choices: [oscillator and SWD/debug/flash options](oscillator_debug_options.md). These do not assign pads or accept implementation choices; see B1-Q004/005/008.

USR-16 / ADR-011 accepts four independent Cortex SWD headers. Use the owned J-Link EDU as planned; PICkit 5 is available if needed. Header pads/MPN and probe/cable qualification remain B1-Q004/005. Common crystal candidate research: [crystal_candidates.md](crystal_candidates.md); no exact MPN selected.

Current selection — USR-19 / [ADR-014](../../docs/decisions/014-smaller-12mhz-crystal.md): smaller common crystal selected for the four MCU oscillators; ADR-017 separately proposes an accurate FT232HL crystal; qualification remains B1-Q008; see BOM B1-B014/019/020. Earlier candidate/unselected statements are historical. Load networks and electrical/pad/footprint qualification remain open under B1-Q008/B1-Q005. Assembly: 0805 preferred, 0603 acceptable, no 0402 or smaller; smaller crystals may be considered if leaded.

Draft SAMC21 per-pad spreadsheet and source evidence: [pinmap](pinmap.md#draft-samc21-allocation--usr-19). Assignments remain proposed and unverified.

The allocation workbook also includes the [STM32 gateway draft](pinmap.md#draft-stm32-gateway-allocation), covering all 64 pads.


FTDI configuration EEPROM B1-B013 is selected by USR-23 / [ADR-018](../../docs/decisions/018-ftdi-eeprom.md). The existing pin-allocation workbook now has an FTDI sheet covering bridge and EEPROM pads, linked from [pinmap](pinmap.md#draft-ftdi-and-eeprom-allocation). Selection does not close B1-Q012 startup/timing/programming/footprint qualification. Power-domain support parts remain in B1-B017.

Dedicated PC-controlled gateway reset/BOOT0 are selected by USR-24 / [ADR-023](../../docs/decisions/023-cbus-gateway-recovery.md). The pin workbook is updated; control circuitry and validation remain B1-Q013.

Connector MPNs are accepted by USR-25 / [ADR-026](../../docs/decisions/026-reva-connectors.md), recorded in BOM B1-B009/022/027 and the [readable BOM](BOM.md). Connector footprint/cable qualification and GPIO cut quantities remain open under B1-Q004/005/010; no CAD or hardware validation is implied.

Four dedicated 115200-baud text-debug UART headers are accepted by [ADR-032](../../docs/decisions/032-debug-uarts.md). See pinmap and workbook for draft connections; B1-Q014 retains electrical and header qualification.

The [current BOM](BOM.md) now reflects accepted decisions through ADR-032 without historical component overlays. [Audit findings](bom_review.md) distinguish outstanding selections from qualification; [interface candidates](rs485_uart_candidates.md) cover external RS-485 and onboard open-drain UART.

[ADR-033](../../docs/decisions/033-open-drain-uart-buffer.md) selects a second SN74LV125APWR for UART_MD in B1-B066. The original VCP buffer remains B1-B016. [Termination proposal](termination_proposal.md) evaluates board-only CAN versus external cable operation and one local RS-485 endpoint resistor; those termination choices and ST3485EBDR are now accepted by [ADR-034](../../docs/decisions/034-rs485-termination.md). Exact resistor/jumper parts accepted ADR-035 in [termination parts](termination_parts.md).

[ADR-035](../../docs/decisions/035-termination-parts.md) / USR-29 accepts the exact termination MPNs in B1-B067–070. [RS-485 bias investigation](rs485_bias.md) records the accepted network, calculations and remote-kit rate check; B1-Q009 remains open.

Local KiCad symbol libraries for SAMC21 and TPS22810DBVT are registered in kicad/sym-lib-table; see [catalog](../../libraries/symbols/README.md). Earlier bench files are preserved in the [migration archive](../../libraries/imports/README.md), including a conflicting STM32G473 selection. They are not the current Board 1 implementation. No board validation is implied.

TCAN3413DR, TPS560430X3FDBVR and AT93C56B-SSHM-B are now available in the project symbol table, with [pin evidence and export checks](../../libraries/symbols/symbol_checks.md). BOM assignments are updated; no schematic implementation is claimed.

[ADR-036](../../docs/decisions/036-rs485-bias.md) / USR-30 accepts two 330 ohm 1% bias resistors in B1-B071: 3V3_SYS to A (ST3485EBDR pin6), B (pin7) to GND. Exact MPN and implementation remain unverified. [TVS recommendations](tvs_candidates.md) remain proposed under B1-Q004/009.
