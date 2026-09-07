# Decision register

Status: draft index · Authority: individual accepted ADRs

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

Use [template.md](template.md); next ID: ADR-037. Numbering is permanent.

Historical collision: both [connector selection](026-reva-connectors.md) and [ceramic SAM core selection](026-sam-core-ceramic.md) carry ADR-026. Preserve both IDs and histories; use the filename-qualified reference to distinguish them. BOM references now do this explicitly.

ADR-027 accepts the exact SAM core capacitor. ADR-030 finalizes the FTDI crystal. ADR-031 resolves the REF tolerance conflict and accepts oscillator load capacitors. These subsequent decisions do not erase earlier history.

Before changing an accepted choice, read the ADR and its evidence. A superseding decision requires explicit maintainer acceptance; part-selection acceptance alone does not establish implementation verification.

Implementation evidence: [library migration and TPS22810 DBV symbol](../../libraries/symbols/README.md) implements ADR-004/019/022. Archived SC189 remains superseded by ADR-021. No ADR status or numbering changed; board qualification questions remain open.

Additional implementation evidence for ADR-002/018/021: [exact-part symbols and checks](../../libraries/symbols/symbol_checks.md). Existing accepted decisions and open board qualifications are unchanged.
