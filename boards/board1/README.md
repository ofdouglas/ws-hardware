# Board 1 Rev A

Status: draft implementation; selected baseline through ADR-039. Part acceptance does not establish electrical or fabrication readiness.

Board 1 is a four-MCU WireSpaces lab: one STM32G474RBT6 gateway and three ATSAMC21G17A-AUT leaves. Each MCU connects to both shared CAN-FD buses and the onboard multidrop UART; the SAMs also form a private UART ring. The gateway provides USB VCP and one external ST3485EBDR RS-485 port. Both CAN pairs and RS-485 have terminal-block access with ground.

USB-B powers an independent FT232HL bridge through the TPS22810 attachment ramp. FTDI PWREN# enables the TPS560430 main 3.3 V converter through MC74HC1G14DBVT1G. SN74LV125APWR isolates VCP TX/RX/RTS/CTS when main power is off. Rev A requires an active PC and must fit the 500 mA configured USB budget; full-load and startup qualification remain open.

The gateway targets 168 MHz and 12 Mbaud VCP. All four MCUs and the FTDI have independent selected 12 MHz crystals and initial load capacitors. Other link rates still need qualification. Each MCU has SWD, a dedicated 115200-baud text UART, four spare GPIOs and an LED; a fifth LED indicates board power. GPIO series resistors remain proposed.

## Current design documents

| Topic | Working document |
|---|---|
| Scope and authoritative question status | [Requirements](requirements.md) |
| Accepted decisions; do not routinely reopen | [ADR register](../../docs/decisions/README.md) |
| Parts, quantities, evidence | [BOM view](BOM.md), [CSV](bom.csv), [remaining selections](remaining_parts.md) |
| USB input, sequencing and current estimates | [USB input](usb_input.md) |
| Bridge, EEPROM, VCP isolation and recovery | [USB VCP](usb_vcp.md) |
| Main converter and distributed capacitors | [Buck](buck_tps560430.md), [decoupling](decoupling.md) |
| PHYs, protection and UART_MD | [Interfaces](interfaces.md) |
| External bus networks | [Termination](termination.md), [RS-485 bias](rs485_bias.md) |
| Oscillators and clock trees | [Crystal networks](crystal_networks.md), [clocking](clocking.md) |
| MCU allocation and breakout details | [Pinmap](pinmap.md), [GPIO breakouts](gpio_breakouts.md) |
| Existing library artifacts and checks | [Symbol catalog](../../libraries/symbols/README.md), [IC coverage](../../libraries/symbols/remaining_ic_symbol_checks.md) |

Use Host/HostId terminology. Requirements own scope and question status; accepted ADRs own decisions; CSV owns parts and quantities. Topic notes explain the current implementation without accepting new circuitry. Reviewed symbols do not imply a completed, validated board schematic or layout.

## Deferred scope

External 24 V power, additional transceivers (including CAN3 and the second Board 1 point-to-point RS-485), the full bench backbone and FPGA/fault instrumentation are later work. RS_485_MULTIDROP is descoped for Board 1, retained in the overall bench architecture. No future footprint or pin reservation is implied.

Before schematic freeze, resolve pinmux, bridge support/defaults, power-off paths, connector numbering, capacitor corners, oscillator startup and current/transient checks in the requirements register. Existing candidate/research files are historical inputs; use the current documents above first.
