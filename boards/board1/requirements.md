# Board 1 requirements

Status: draft · Authority: per-row status · Updated: 2026-09-06

All `proposed` rows are extracted or suggested starting requirements, not a frozen schematic specification. `accepted` applies only to explicit decisions. `TBD` values block related implementation review. Source IDs resolve in [SOURCE_NOTES](../../docs/SOURCE_NOTES.md).

## Nodes — accepted MCU selection (B1-R001)

| ID | Label | Role | Exact selected MPN | Qty | Source |
|---|---|---|---|---:|---|
| B1-N01 | GW | Gateway | STM32G474RBT6 | 1 | SRC-ARCH §3.1; USR-15 / ADR-004 |
| B1-N02 | SAM0 | Leaf | ATSAMC21G17A-AUT | 1 | SRC-ARCH §3.2; USR-15 / ADR-004 |
| B1-N03 | SAM1 | Leaf | ATSAMC21G17A-AUT | 1 | SRC-ARCH §3.2; USR-15 / ADR-004 |
| B1-N04 | SAM2 | Leaf | ATSAMC21G17A-AUT | 1 | SRC-ARCH §3.2; USR-15 / ADR-004 |

The PC is external test equipment. HostIds are deployment values, not physical node labels.

## Links — Rev A scope per ADR-007; implementation details pending

| ID | Net/group | Endpoints / direction | Medium | Rate | Requirement |
|---|---|---|---|---|---|
| B1-L01 | FD_CAN_A | GW, SAM0, SAM1, SAM2; shared | CAN-FD | TBD | B1-R002 |
| B1-L02 | FD_CAN_B | GW, SAM0, SAM1, SAM2; shared, separate from FD_CAN_A | CAN-FD | TBD | B1-R002 |
| B1-L03 | UART_MD | GW, SAM0, SAM1, SAM2; shared | Open-drain-equivalent UART; ADR-033 driver; support TBD | TBD | B1-R003 |
| B1-L04 | RING_01 | SAM0 TX -> SAM1 RX | Point-to-point UART | TBD | B1-R004 |
| B1-L05 | RING_12 | SAM1 TX -> SAM2 RX | Point-to-point UART | TBD | B1-R004 |
| B1-L06 | RING_20 | SAM2 TX -> SAM0 RX | Point-to-point UART | TBD | B1-R004 |
| B1-L07 | UART_VCP | PC USB <-> bridge UART <-> GW | Dedicated USB-UART VCP | 12 Mbaud capability | B1-R005; B1-R014 |
| B1-L08 | RS485_EXT | GW <-> external endpoint | RS-485; point-to-point half-duplex; ADR-034 | Up to 12 Mbps | B1-R016; B1-R021 |
| B1-L09 | DEBUG_GW | GW MCU TX/RX to external adapter; GND | Dedicated 3.3 V logic UART proposal | 115200 baud | B1-R025 |
| B1-L10 | DEBUG_SAM0 | SAM0 MCU TX/RX to external adapter; GND | Dedicated 3.3 V logic UART proposal | 115200 baud | B1-R025 |
| B1-L11 | DEBUG_SAM1 | SAM1 MCU TX/RX to external adapter; GND | Dedicated 3.3 V logic UART proposal | 115200 baud | B1-R025 |
| B1-L12 | DEBUG_SAM2 | SAM2 MCU TX/RX to external adapter; GND | Dedicated 3.3 V logic UART proposal | 115200 baud | B1-R025 |

USR-04 targets several Mbaud for onboard UARTs, exact rates TBD. This replaces the older exploratory approximately 1 Mbit/s target; the open-drain electrical limit still requires validation. One ring UART per leaf uses TX to the next leaf and RX from the preceding leaf; GW is excluded from the ring.

## Requirement register

| ID | Scope | Status | Requirement | Verification / acceptance evidence | Basis / decision |
|---|---|---|---|---|---|
| B1-R001 | MVP | accepted | Populate exactly the four nodes above | Exact datasheets/errata, pin/resource review, schematic and BOM | USR-15; SRC-ARCH §3; ADR-004; B1-Q005 |
| B1-R002 | MVP | accepted | Attach all four nodes independently to CAN1 and CAN2; support simultaneous traffic | Eight PHY channels accounted for; electrical review; bench traffic at accepted rates | SRC-ARCH §4.1; ADR-002 |
| B1-R003 | MVP | accepted | Provide shared onboard open-drain UART among all four nodes | Review drive/pull-up/reset behavior; measure rise time and traffic at accepted rate | SRC-ARCH §5.1; USR-27; ADR-033; B1-Q003 |
| B1-R004 | MVP | accepted | Provide directed SAM0 -> SAM1 -> SAM2 -> SAM0 UART ring | Connectivity/pin review and traffic on each hop | SRC-ARCH §5.2 |
| B1-R005 | MVP | accepted | Provide USB 2.0 Standard-B power and dedicated FT232HL VCP to GW; native USB not required for bring-up | USB/interface review; PC enumeration and serial exchange | SRC-ARCH §7; USR-03; ADR-001 |
| B1-R006 | MVP | proposed | Operate normal networking from USB alone within a defined current budget | Approved startup/worst-case power analysis and measured rail/current limits | SRC-ARCH §8.4; ADR-001; B1-Q002 |
| B1-R007 | MVP | accepted | Give all four MCUs independent 10-pin Cortex SWD programming/debug headers and reset access | Independent connection, programming and reset of each MCU | USR-16; ADR-011; SRC-ARCH §7.3; B1-Q004 |
| B1-R008 | MVP | proposed | Expose ground, rails and useful link observation points | Schematic/layout accessibility review; probe access at bring-up | Scaffold recommendation; B1-Q004 |
| B1-R009 | MVP | proposed | Define termination and protection for both CAN buses and any external interfaces | Electrical/topology review; observed bus waveforms at accepted limits | SRC-ARCH §4.3; B1-Q003/004 |
| B1-R010 | MVP boundary | accepted | Keep full inter-board signal/power backbone and deterministic fault injection out of first-PCBA requirements | Scope/BOM/CAD review shows no implicit inclusion | USR-01/02; ADR-003 |
| B1-R011 | MVP experiment | proposed | Support leaf bare-metal and RTOS experiments with simultaneous CAN/UART activity | Firmware demonstrations and recorded memory/queue use; quantitative thresholds TBD | SRC-ARCH §15; B1-Q006 |
| B1-R012 | MVP power | accepted | Use independent USB bridge power and controlled main-board power; provide power-off isolation on VCP TX/RX/RTS/CTS | Startup/suspend/resume and current/leakage measurements; circuit review | ADR-001; B1-Q002; B1-Q007 |
| B1-R013 | Spin A power scope | superseded | Exclusively USB-powered from an active PC; external connectors and advanced power architecture belong to later respins | Scope review; startup/suspend/resume validation of resulting circuit | User follow-up to USR-03; replaced by B1-R018 / ADR-006 |
| B1-R014 | Gateway VCP | accepted | Support 12 Mbaud with STM32 at 168 MHz, a 168 MHz USART kernel clock, short traces and available hardware RTS/CTS | Clock/mux review; full-duplex traffic, flow-control and isolation timing under load | USR-04; ADR-005; B1-Q008 |
| B1-R015 | MCU clocks | accepted | Give GW and each SAM its own external main crystal as the reference for high-speed link clocks | Oscillator/clock-tree review and startup/tolerance validation for all four MCUs | USR-04; ADR-005; B1-Q008 |
| B1-R016 | Rev A RS-485 | accepted | Provide one STM32 external RS-485 port alongside both CANs, all onboard UARTs and VCP | Peripheral/mux and schematic review; external link traffic | USR-05; ADR-006; B1-Q009 |
| B1-R017 | Rev A terminals | accepted | Expose FD_CAN_A, FD_CAN_B and RS-485 differential pairs plus one or two ground terminals | Connector continuity, labeling, termination and protection review | USR-05; ADR-006; B1-Q004 |
| B1-R018 | Rev A power/scope | superseded | USB-only active-PC operation; include B1-R017 signal terminals; defer external power, extra transceivers and further connectors to later revisions | Scope and power-state review | USR-03/05; ADR-001; ADR-006; replaced by B1-R022 |
| B1-R019 | Rev A LEDs | accepted | One controllable LED per MCU and one board power LED | Pin/resource and all-on current review | USR-06; ADR-007 |
| B1-R020 | Rev A GPIO | accepted | Provide a few spare I/O pins per MCU on breakouts | Four GPIOs per MCU accepted ADR-039; full pinmux audit and electrical/load contract pending | USR-06; ADR-007; B1-Q010 |
| B1-R021 | Board 1 RS-485 | accepted | External rate ceiling 12 Mbps; expanded Board 1 has LEFT/RIGHT p2p ports only; bench MULTIDROP remains in family architecture | Topology, rate and power review | USR-06; ADR-007; B1-Q009 |
| B1-R022 | Rev A power/scope | accepted | USB-only active-PC operation with bus terminals and GPIO breakouts; external power and additional PHYs remain for later revisions | Scope and power-state review | ADR-001; ADR-007; replaces B1-R018 |
| B1-R023 | Main buck efficiency | accepted | Support conservative full networking load within 500 mA total USB current; no fixed 90% or light-load efficiency target | Full-load USB current and startup measurements; approx 70.7% steady-state break-even under current assumptions | ADR-021 |
| B1-R024 | Gateway recovery | accepted | Provide dedicated FTDI CBUS GPIO control of STM32 reset and BOOT0 for ROM UART programming; preserve SWD and RTS/CTS | Review defaults and power-off behavior; demonstrate Linux GPIO control and ROM programming without application firmware | USR-24; ADR-023; B1-Q013 |
| B1-R025 | MCU text debug | accepted | Give each MCU a dedicated 115200-baud TX/RX/GND UART on a three-pin 0.1-inch header | Pin/peripheral and clock review; simultaneous bidirectional debug/network traffic; header/adapter/off-state checks | USR-26; ADR-032; B1-Q014 |
| B1-R026 | Rev A termination | accepted | Implement the CAN fixed-plus-jumper endpoint arrangement and fixed local RS-485 120 ohm termination in ADR-034 | Review endpoint routing, jumper modes, resistor ratings and measured waveforms | USR-28; ADR-034; B1-Q003/004/009 |

## Deferred / undecided features

| Feature | Status | MVP handling | Basis |
|---|---|---|---|
| Full 17-pair backbone, 24 V trunk/tap, test SPI, trigger/fault hardware | deferred | No circuitry, connectors or reserved pins implied | ADR-003 |
| CAN3 and its initial-DNP local PHY/termination | deferred | Excluded from proposed baseline; no footprint implied | SRC-ARCH §4.2; B1-Q001 |
| Second Board 1 RS-485 p2p port | deferred | Rev A has one; expanded Board 1 has LEFT/RIGHT, two total | ADR-007 |
| RS_485_MULTIDROP (historical RS485_SHARED) | deferred | Descoped for Board 1 currently; retained in overall bench architecture | USR-06 clarification; ADR-007 |
| Protected 5V_AUX_OUT | deferred | No external power output in Rev A estimate | SRC-ARCH §8.5; ADR-006 |
| Native STM32 USB option | deferred | No connector or pin reservation assumed | SRC-ARCH §7.2; B1-Q001 |
| T1S, FPGA instrumentation, wireless, Ethernet | deferred | Future experiments, no MVP implementation | SRC-ARCH §§9,14 |

## Open questions — authoritative register

| ID | Status | Owner | Question / required result | Blocks | Resolution |
|---|---|---|---|---|---|
| B1-Q001 | resolved | Maintainer | Rev A networking scope | Scope freeze | USR-05/06 / ADR-007: both CANs, onboard UARTs, VCP, one external RS-485, signal terminals and GPIO breakouts; added PHYs deferred |
| B1-Q002 | open | Power designer | Complete USB-B/FT232HL/TPS560430 power proposal: budget, current datasheets/errata, support parts, protection, EN control/isolation and any auxiliary allowance | Power schematic | TPS560430 selected ADR-021; input circuit and LC implementation under review |
| B1-Q003 | open | Interface designer | Choose CAN arbitration/data and UART rates; multidrop circuit/pull-up; PHY behavior and termination | PHY selection and electrical review | TBD |
| B1-Q004 | open | Board designer | Define external bus access, connector pinouts, grounding/protection, debug/reset headers, test points and mechanical constraints | Connector allocation and layout | TBD |
| B1-Q005 | open | Board designer | Verify exact MCU/package peripherals, simultaneous mux use, clocks/boot/reset/debug, electrical compatibility and availability | Pinmap and schematic freeze | TBD |
| B1-Q006 | open | Firmware/test owner | Define representative workloads, rates, queue/memory reporting and pass thresholds for simultaneous links and bare-metal/RTOS | Experiment acceptance | TBD |
| B1-Q007 | resolved | Maintainer | Spin A power operating scope | Power-state architecture | User: exclusively USB powered, requires PC on; advanced power deferred; bus terminals and GPIO breakouts included. See current B1-R022 |
| B1-Q008 | open | Clock/firmware designer | Implement 168 MHz gateway and 12 Mbaud VCP; choose four MCU crystals and validated PLL/peripheral clocks including CAN and onboard UART divisors | Clock and pinmap freeze | ADR-014/030 finalize MCU and FTDI crystal MPNs; ADR-031 accepts load capacitors; load/startup/drive and clock-tree/bench review pending |
| B1-Q009 | open | Interface designer | Select RS-485 part, rate, half/full-duplex, DE-/RE control, termination/bias, protection and cable assumptions | RS-485 schematic | ST3485EBDR and termination topology decided ADR-034; 12 Mbps ceiling retained. Bias investigation rs485_bias.md records accepted 330 ohm legs ADR-036; loading/leakage/power-off checks and owned Digi kit revision/rate remain open, alongside MCU thresholds/control/protection |
| B1-Q010 | open | Board designer | Select five LEDs/current targets; allocate spare GPIOs per MCU with load and protection contract | Pinmap and final power budget | Proposed 0.5 mA per LED; four GPIOs/MCU; 20 mA aggregate external-load reserve; not ratings |
| B1-Q011 | open | Power designer | Qualify converter efficiency envelope, passives, layout and losses | Main power design approval | USR-13 limits efficiency qualification to full networking load; see buck_tps560430.md and decoupling.md; temperature/full-load corners and measurements pending |
| B1-Q012 | open | Interface designer | Qualify selected FTDI EEPROM: clock and word-program timing, supply ramp, reset/read delay, rapid power cycling, current datasheets/errata and SOIC footprint | USB bridge schematic freeze | AT93C56B-SSHM-B selected USR-23 / ADR-018; FTDI sheet has draft wiring. FT_Prog program/readback and startup measurements pending |
| B1-Q013 | open | Interface designer | Design CBUS reset/BOOT0 interfaces, polarity, defaults, off-state protection and SWD sharing; verify option bytes, ROM-probed pin behavior and Linux control | Gateway recovery schematic and programming sign-off | ADR-023 allocates CBUS5/6; B1-B053 components TBD; workbook endpoints updated but unverified |
| B1-Q014 | open | Interface/firmware designer | Qualify debug UART pinmux, baud clocks, header order/MPN/footprint, 3.3 V adapter interface and unpowered-input behavior | Debug UART schematic and bring-up | ADR-032 accepts four ports at 115200 baud; SERCOM2 and LPUART1 draft mappings in workbook; B1-B059 header cuts accepted ADR-039; B1-B060 support parts TBD |

Owners are roles, not assigned people. Close questions with evidence/ADR links; retain their IDs. No open question has been silently answered by a generated part or pin choice.

Naming: FD_CAN_A = historical CAN1; FD_CAN_B = historical CAN2. These are two physical buses, not additional buses.

USR-19 / ADR-014 selects the common MCU crystal for B1-R015; USR-22 / ADR-017 requires a separate accurate FTDI crystal for B1-R005, finalized by ADR-030; exact MPN and quantities are in BOM B1-B014/019/020. B1-Q008 remains open for oscillator qualification and load networks; crystal selection alone does not resolve it.

Draft implementation evidence for B1-R001/002/003/005/007/014/015/016/019/020/021: the STM32 sheet linked in [pinmap](pinmap.md#draft-stm32-gateway-allocation). All pin evidence remains unverified and no question is closed by this allocation.

USR-23 / ADR-018 selects B1-B013 for B1-R005/012. The new FTDI sheet covers bridge and EEPROM pads; B1-Q002/008/012 remain open for the linked implementation checks.

USR-25 / [ADR-026](../../docs/decisions/026-reva-connectors.md) accepts exact connector MPNs in BOM B1-B009/022/027 for B1-R007/017/020. B1-Q004 remains open for terminal numbering, polarity, footprints and debug cable/adapter checks; B1-Q005 retains MCU debug qualification. B1-Q010 retains GPIO count/order, cut schedule, source-strip quantity and load/protection limits. Terminal order remains open; ADR-039 subsequently accepts four 1x5 GPIO headers and the cut schedule.

[ADR-027](../../docs/decisions/027-ceramic-capacitor-mpns.md) accepts ceramic capacitor MPNs in B036–041/045/048 and bridge support mapping for B1-R001/012/023. B1-Q002/011 remain open for effective capacitance, core regulation, damping pulse and implementation qualification.

ADR-029 accepts exact LED and raw-VBUS damping MPNs for B1-R019/012; B1-Q002/010/011 retain qualification. [Remaining component decisions](remaining_parts.md) tracks unresolved procurement choices.

ADR-030 finalizes USB-B connector and crystal MPNs. The interim REF tolerance conflict was resolved by ADR-031 below; B1-Q008 retains loading/gain/drive/startup qualification. See crystal_networks.md for the accepted initial load capacitors.

ADR-031 resolves the B1-Q002 REF tolerance subissue with RMCF0805FT12K0 and accepts crystal capacitor MPNs; B1-Q002/008 remain open for other qualification. GPIO series-resistor proposal is in gpio_breakouts.md under B1-Q010.

BOM reconciliation exposes accepted ADR-027/028 bridge allocations as B1-B061–065, split from B1-B017 with no added scope. B1-Q002/012 retain count/rail qualification. [Interface candidate review](interfaces.md) informs B1-Q003/009; no proposed transceiver or multidrop driver is accepted by this audit.

USR-27 / [ADR-033](../../docs/decisions/033-open-drain-uart-buffer.md) accepts B1-B066 for B1-R003. B1-B008 support values are accepted by ADR-039; B1-Q003/005 remain open for timing, reset/power, thresholds and implementation. [Termination proposal](termination.md) records the CAN jumper and fixed local RS-485 evaluation under B1-Q003/004/009; topology and nominal 120 ohm values subsequently accepted by USR-28 / ADR-034 / B1-R026; exact resistor/jumper MPNs subsequently accepted ADR-035.

[ADR-035](../../docs/decisions/035-termination-parts.md) / USR-29 accepts the exact termination MPNs in B1-B067–070. [RS-485 bias investigation](rs485_bias.md) records the accepted network, calculations and remote-kit rate check; B1-Q009 remains open.

Library implementation evidence for B1-R001/006/012: [local symbols](../../libraries/symbols/README.md) and [migration/conflict record](../../libraries/imports/README.md). B1-Q002/005 remain open; the archived STM32G473 bench schematic does not supersede the accepted STM32G474 selection.

Symbol implementation evidence for B1-R002/005/006/012/023: [three exact-part library checks](../../libraries/symbols/symbol_checks.md), implementing ADR-002/018/021. This does not close B1-Q002/003/004/011/012 or change requirement status.

[ADR-036](../../docs/decisions/036-rs485-bias.md) / USR-30 accepts two 330 ohm 1% bias resistors in B1-B071: 3V3_SYS to A (ST3485EBDR pin6), B (pin7) to GND. Exact MPN and implementation remain unverified. [TVS selections](interfaces.md) are accepted ADR-037/038; qualification remains open under B1-Q004/009.

[ADR-037](../../docs/decisions/037-can-tvs.md) / USR-31 accepts B1-B072: two ESD2CAN24DBZRQ1 arrays near the CAN terminal pairs, DBZ pins1/2 to CANH/CANL and pin3 to GND, independent of termination jumpers. Exact CAD connectivity/footprint and transient qualification remain B1-Q004. [RS-485 TVS selection](interfaces.md) is accepted ADR-038; qualification remains open under B1-Q009.

[ADR-038](../../docs/decisions/038-rs485-tvs.md) / USR-32 accepts ESDS452DBZR B1-B073: DBZ pins1/2 to A/B, pin3 GND. Normal operation requires both RS-485 wires within +/-5.5 V of local Board 1 ground. Actual endpoint/offset and transient qualification remain B1-Q009. See [BOM closeout recommendations](remaining_parts.md).

[Complete selected IC/array symbol coverage](../../libraries/symbols/remaining_ic_symbol_checks.md) supports schematic capture for the existing requirements. These library checks do not close B1-Q002/003/004/005/009 or change requirement acceptance/verification.

[ADR-039](../../docs/decisions/039-bom-closeout-selections.md) / USR-33 accepts bias and LED MPNs, four 10 kohm /OE pull-ups B1-B008, one 470 ohm UART_MD pull-up B1-B074, four 1x5 GPIO and four 1x3 debug headers cut from one strip, and PCB pads plus fitted scope-ground pins B1-B075. Final GPIO mux, pad/pin positions, ground-pin MPN/count and electrical qualification remain open. Header acceptance does not accept the proposed GPIO series resistors.
