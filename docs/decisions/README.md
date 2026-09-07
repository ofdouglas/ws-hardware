# Decision register

Status: draft index · Authority: individual accepted ADRs

## Current authority map

Read this map before the chronological register. An accepted ADR may retain only some clauses; its historical decision text does not override later accepted decisions. Part selection never closes qualification questions. Retain both ADR-026 IDs and cite their filenames; no renumbering is authorized.

| Topic | Current authority and surviving scope | Implementation |
|---|---|---|
| Family terminology / Rev A boundary | ADR-003/004/007; RS_485_MULTIDROP deferred for Board 1, retained for family | [Requirements](../../boards/board1/requirements.md) |
| USB power / input | ADR-001 domain policy; ADR-013 isolation; ADR-040 direct PWREN# enable/startup; ADR-019 ramp topology; ADR-022 47 nF/no supervisor; ADR-024 inverter; ADR-015/016 ESD scope; ADR-027/028/029/030 passives | [Input](../../boards/board1/usb_input.md), [VCP](../../boards/board1/usb_vcp.md) |
| Main buck | ADR-021 TPS560430 and total 500 mA criterion; ADR-025 exact LC/passives; no 90% floor or SC189 Cout ceiling | [Buck](../../boards/board1/buck_tps560430.md) |
| Decoupling | ADR-010 MCU/bypass allocation only; [ADR-026 core](026-sam-core-ceramic.md) ceramic; ADR-027 MPNs; ADR-025 local output | [Decoupling](../../boards/board1/decoupling.md) |
| Crystals / clocks | ADR-005 timing targets; ADR-014 MCU crystals; ADR-017 separate FTDI strategy; ADR-030 exact FTDI crystal; ADR-031 initial load caps and REF correction | [Clocks](../../boards/board1/clocking.md), [crystals](../../boards/board1/crystal_networks.md) |
| CAN / RS-485 | ADR-002 TCAN3413; ADR-034 ST3485/termination; ADR-035 termination MPNs; ADR-036 bias; ADR-037 CAN TVS; ADR-038 restricted RS-485 TVS envelope; ADR-039 bias MPNs | [Interfaces](../../boards/board1/interfaces.md), [termination](../../boards/board1/termination.md), [bias](../../boards/board1/rs485_bias.md) |
| Onboard UART | ADR-033 second LV125 driver; ADR-039 support resistors; actual rate unqualified | [Interfaces](../../boards/board1/interfaces.md) |
| Debug / recovery / connectors | ADR-011 SWD; ADR-018 EEPROM; ADR-023 CBUS; [ADR-026 connectors](026-reva-connectors.md); ADR-032 text UART; ADR-039 header cuts/test access | [Pinmap](../../boards/board1/pinmap.md), [remaining work](../../boards/board1/remaining_parts.md) |
| LEDs / GPIO | ADR-007 scope; ADR-029 LEDs; ADR-039 LED resistors and four GPIOs/MCU; GPIO series resistors still proposed | [BOM](../../boards/board1/BOM.md) |
| Assembly / sourcing | ADR-009 plus current maintainer package rules; DigiKey-only sourcing policy | [Part policy](../PART_SELECTION_POLICY.md) |

Completion of an earlier proposal (for example ADR-024 pulls by ADR-028/030) is not wholesale supersession. Metadata lists replacements only; implementation links and this map also show completions. New engineering changes still require explicit acceptance and a new ADR where applicable.

Allocation-note reconciliation (2026-09-07): [pinmap](../../boards/board1/pinmap.md) and its workbook now distinguish current selections from unfinished implementation. [Unfinished decisions](../../boards/board1/unfinished_decisions.md) references the existing board questions; this editorial cleanup adds no accepted decisions or verified allocations.

## Chronological register

| ID | Title | Status | Scope |
|---|---|---|---|
| [ADR-001](001-usb-power.md) | USB power and independent VCP bring-up (power/isolation architecture) | accepted | Board 1 MVP |
| [ADR-002](002-can-transceivers.md) | CAN-FD transceiver selection (TCAN3413DR) | accepted | Board 1 CAN1/CAN2 |
| [ADR-003](003-terminology-and-mvp-boundary.md) | Host terminology and reduced first PCBA | accepted | Repository / Board 1 |
| [ADR-004](004-board1-mcu-baseline.md) | MCU selection (STM32G474RBT6 / ATSAMC21G17A-AUT) | accepted | Board 1 |
| [ADR-005](005-clock-and-vcp-speed.md) | Crystal clocks and 12 Mbaud gateway VCP | accepted | Board 1 Spin A |
| [ADR-006](006-reva-external-buses.md) | Rev A links and terminal access | superseded | Board 1 Rev A |
| [ADR-007](007-board1-rs485-power-scope.md) | Board 1 RS-485 scope, LEDs and GPIO | accepted | Board 1; bench multidrop retained |
| [ADR-008](008-main-buck-efficiency.md) | Main buck efficiency proposal | superseded | Board 1 main 3.3 V rail |
| [ADR-009](009-assembly-package-policy.md) | Assembly and package policy | accepted | Project-wide |
| [ADR-010](010-sc189-and-decoupling.md) | SC189 and Rev A decoupling | accepted | Board 1 main rail |
| [ADR-011](011-swd-debug-access.md) | Independent Cortex SWD headers and owned probes | accepted | Board 1 debug |
| [ADR-012](012-common-12mhz-crystal.md) | Common leaded 12 MHz crystal | superseded | Board 1, five oscillators |
| [ADR-013](013-enable-control-uart-isolation.md) | SC189 enable control and SN74LV125APWR | accepted | Board 1 Rev A; replaces ADR-001 main-switch implementation |
| [ADR-014](014-smaller-12mhz-crystal.md) | Smaller leaded 12 MHz crystal | accepted | Four MCU crystals; FTDI scope superseded by ADR-017 |
| [ADR-015](015-usb-data-esd.md) | RCLAMP0504S.TCT USB data ESD | accepted | Board 1 Rev A |
| [ADR-016](016-usb-protection-scope.md) | USB ESD and hot-plug protection scope | accepted | Board 1 Rev A |
| [ADR-017](017-separate-ftdi-crystal.md) | Separate accurate FT232HL crystal | accepted | Strategy; exact MPN subsequently accepted ADR-030 |
| [ADR-018](018-ftdi-eeprom.md) | AT93C56B-SSHM-B configuration EEPROM | accepted | Board 1 FT232HL bridge |
| [ADR-019](019-simple-vbus-input.md) | Simple slew-controlled USB input | accepted | Board 1 Rev A; replaces direct input attachment in ADR-013 |
| [ADR-020](020-ftdi-supply-reset.md) | FTDI supply-qualified reset with TLV803E | superseded | Board 1 Rev A; adds supervision to ADR-019 |
| [ADR-021](021-tps560430-main-buck.md) | TPS560430 main buck and USB-current criterion | accepted | Replaces ADR-010 converter/filter and efficiency floor |
| [ADR-022](022-fast-input-ramp.md) | Fast TPS22810 ramp without external FTDI supervisor | accepted | Board 1 Rev A |
| [ADR-023](023-cbus-gateway-recovery.md) | Dedicated CBUS gateway reset and BOOT0 | accepted | Board 1 gateway recovery |
| [ADR-024](024-pwren-inverter.md) | MC74HC1G14DBVT1G PWREN# inverter | accepted | Implements ADR-013; SMF6.0A alone retained |
| [ADR-025](025-buck-passives.md) | TPS560430 local passive MPNs | accepted | Five components; four unique parts |
| [ADR-026](026-reva-connectors.md) | Rev A debug, bus and GPIO connector MPNs | accepted | Implements ADR-007/011; B1-B009/022/027 |
| [ADR-026](026-sam-core-ceramic.md) | Ceramic SAM VDDCORE capacitors | accepted | Supersedes ADR-010 dielectric restriction |
| [ADR-027](027-ceramic-capacitor-mpns.md) | General ceramic capacitor MPNs | accepted | Decoupling and input timing; completes SAM core selection |
| [ADR-028](028-10k-pullup-resistor.md) | Common 10 kohm pull-up resistor | accepted | B051/B054 and bridge support |
| [ADR-029](029-led-vbus-components.md) | Orange LEDs and VBUS damping parts | accepted | B024/025/046/047 |
| [ADR-030](030-usb-crystals-support.md) | USB connector, crystal finalization and support resistors | accepted | REF tolerance conflict resolved by ADR-031 |
| [ADR-031](031-crystal-caps-ref.md) | Crystal capacitors and corrected REF resistor | accepted | Resolves ADR-030 REF tolerance conflict |
| [ADR-032](032-debug-uarts.md) | Independent MCU text debug UARTs | accepted | Four 115200-baud TX/RX/GND headers |
| [ADR-033](033-open-drain-uart-buffer.md) | Second SN74LV125APWR for onboard open-drain UART | accepted | B1-B066; implements B1-R003 |
| [ADR-034](034-rs485-termination.md) | ST3485EBDR and Rev A bus termination | accepted | B1-B021/067–070; B1-R026 |
| [ADR-035](035-termination-parts.md) | Exact termination resistor and jumper MPNs | accepted | B1-B067–070; B1-R026 |
| [ADR-036](036-rs485-bias.md) | RS-485 330 ohm bias network | accepted | B1-B071; B1-R016/021 |
| [ADR-037](037-can-tvs.md) | ESD2CAN24DBZRQ1 CAN TVS arrays | accepted | B1-B072; B1-R009/017 |
| [ADR-038](038-rs485-tvs.md) | ESDS452DBZR and restricted bench voltage envelope | accepted | B1-B073; B1-R016/017 |
| [ADR-039](039-bom-closeout-selections.md) | Resistors, UART support, header cuts and test access | accepted | B1-B008/011/026/027/059/071/074/075 |
| [ADR-040](040-startup-and-vcp-enable.md) | Conventional FTDI startup and direct PWREN# VCP enable | accepted | Supersedes ADR-013 rail-valid /OE prerequisite only |

Use [template.md](template.md); next ID: ADR-041. Numbering is permanent.

Historical collision: both [connector selection](026-reva-connectors.md) and [ceramic SAM core selection](026-sam-core-ceramic.md) carry ADR-026. Preserve both IDs and histories; use the filename-qualified reference to distinguish them. BOM references now do this explicitly.

ADR-027 accepts the exact SAM core capacitor. ADR-030 finalizes the FTDI crystal. ADR-031 resolves the REF tolerance conflict and accepts oscillator load capacitors. These subsequent decisions do not erase earlier history.

Before changing an accepted choice, read the ADR and its evidence. A superseding decision requires explicit maintainer acceptance; part-selection acceptance alone does not establish implementation verification.

Implementation evidence: [library migration and TPS22810 DBV symbol](../../libraries/symbols/README.md) implements ADR-004/019/022. Archived SC189 remains superseded by ADR-021. No ADR status or numbering changed; board qualification questions remain open.

Additional implementation evidence for ADR-002/018/021: [exact-part symbols and checks](../../libraries/symbols/symbol_checks.md). Existing accepted decisions and open board qualifications are unchanged.

Implementation evidence: [remaining IC symbols and BOM coverage](../../libraries/symbols/remaining_ic_symbol_checks.md) implements the existing selected parts, including ADR-037/038. No decision acceptance or electrical qualification is changed.
