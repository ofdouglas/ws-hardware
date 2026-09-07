# Board 1 pin/resource allocation

Status: draft · Allocation evidence: unverified · Notes reconciled through ADR-042 on 2026-09-07 · Related: B1-Q005

The table below preserves the original parent resource IDs. Draft per-pad assignments for all MCUs, FTDI and EEPROM appear in the linked spreadsheet below. Accepted MCU MPNs and quantities are in requirements (USR-15 / ADR-004); verify their exact datasheets/errata before allocation. `TBD` means unknown; `NA` means not applicable.

The workbook already contains 264 physical-pad rows B1-P025–288. Parent groups B1-P001–024 are a resource checklist, not additional physical pads or an instruction to allocate the devices again. The workbook owns the draft pad/port/peripheral/mux detail; evidence must include manufacturer document revision/page/table and conflict review before any row becomes verified. See [unfinished decisions](unfinished_decisions.md) for the remaining implementation choices.

| ID | Node | Required signals | Link/requirement |
|---|---|---|---|
| B1-P001 | GW | FD_CAN_A_TX; FD_CAN_A_RX | B1-L01 |
| B1-P002 | GW | FD_CAN_B_TX; FD_CAN_B_RX | B1-L02 |
| B1-P003 | GW | UART_MD drive/sense | B1-L03 |
| B1-P004 | GW | VCP_TX; VCP_RX; VCP_RTS; VCP_CTS | B1-L07 |
| B1-P005 | GW | SWDIO; SWCLK; RESET | B1-R007 |
| B1-P006 | GW | Power; ground; clocks; boot/configuration | B1-R001; B1-Q005 |
| B1-P007 | SAM0 | FD_CAN_A_TX; FD_CAN_A_RX | B1-L01 |
| B1-P008 | SAM0 | FD_CAN_B_TX; FD_CAN_B_RX | B1-L02 |
| B1-P009 | SAM0 | UART_MD drive/sense | B1-L03 |
| B1-P010 | SAM0 | RING_TX; RING_RX | B1-R004 |
| B1-P011 | SAM0 | SWDIO; SWCLK; RESET | B1-R007 |
| B1-P012 | SAM0 | Power; ground; clocks; boot/configuration | B1-R001; B1-Q005 |
| B1-P013 | SAM1 | FD_CAN_A_TX; FD_CAN_A_RX | B1-L01 |
| B1-P014 | SAM1 | FD_CAN_B_TX; FD_CAN_B_RX | B1-L02 |
| B1-P015 | SAM1 | UART_MD drive/sense | B1-L03 |
| B1-P016 | SAM1 | RING_TX; RING_RX | B1-R004 |
| B1-P017 | SAM1 | SWDIO; SWCLK; RESET | B1-R007 |
| B1-P018 | SAM1 | Power; ground; clocks; boot/configuration | B1-R001; B1-Q005 |
| B1-P019 | SAM2 | FD_CAN_A_TX; FD_CAN_A_RX | B1-L01 |
| B1-P020 | SAM2 | FD_CAN_B_TX; FD_CAN_B_RX | B1-L02 |
| B1-P021 | SAM2 | UART_MD drive/sense | B1-L03 |
| B1-P022 | SAM2 | RING_TX; RING_RX | B1-R004 |
| B1-P023 | SAM2 | SWDIO; SWCLK; RESET | B1-R007 |
| B1-P024 | SAM2 | Power; ground; clocks; boot/configuration | B1-R001; B1-Q005 |

Future CAN3, native USB, additional RS-485 and backbone/test signals have no physical reservations. Add rows only when scope warrants them. Review shared pins, voltage domains, debug ownership, oscillator needs, boot straps, reset defaults and PHY control pins across the complete package before marking allocation verified.

## USB/power resources — selected parts, implementation unverified

These are auxiliary components, not additional WS Hosts. Details and evidence limits: [USB VCP](usb_vcp.md). FTDI/EEPROM pad rows exist in the workbook; auxiliary IC pin evidence is in the local libraries. Complete board connectivity and current-document review before verification.

| Resource | Domain | Allocation needed | Status |
|---|---|---|---|
| FT232HL | Independent USB bridge power | USB pair; supplies; crystal; reset/reference/test; EEPROM; UART; ACBUS power control | unverified |
| AT93C56B-SSHM-B | Bridge domain | Accepted x16 organization; qualify draft wiring and configuration timing | unverified |
| TPS22810DBVT input ramp | VBUS_RAW -> USB_5V | EN to VIN, CT 47 nF, QOD to OUT; see usb_input.md | unverified |
| TPS560430X3FDBVR | USB_5V -> 3V3_SYS | Accepted converter ADR-021 and passives ADR-025; pin/circuit qualification in buck_tps560430.md | unverified |
| UART isolation | Bridge/main boundary | Direct PWREN# to B016 /OE pins 1/4/10/13 accepted ADR-040; check channel wiring and receiver defaults | unverified |

Clock requirements: [clocking.md](clocking.md), ADR-005. B1-P006/P012/P018/P024 each cover the node's external-main-crystal signals; draft physical pads are recorded in the workbook. B1-P004 needs four compatible USART pins, a 168 MHz kernel source and DMA resources. Do not allocate those oscillator or handshake resources to future expansion.

Rev A RS-485 resource reservation: B1-L08/B1-R016 requires an additional GW UART TX/RX and DE-/RE control (separate control preferred as a proposal). USART3 and separate /RE GPIO have draft pad/mux assignments below; simultaneous allocation and electrical review remain open. The accepted eight-position terminal block serves FD_CAN_A H/L, FD_CAN_B H/L, RS-485 A/B and ground(s); two grounds and the signal order remain proposed. No added MCU CAN pins or CAN transceivers are required merely for terminal access to the existing buses.

One LED control per MCU remains included. ADR-041 / USR-35 replaces the separate GPIO/debug headers with four combined 1x8 timing/debug headers. One selected 40-position strip supplies all 32 positions. General ADC, SPI/I2C and GPIO breakouts are deferred. Resistor selections and PCB test pads plus fitted scope-ground access from ADR-039 remain in force. Exact timing MCU pads remain TBD under B1-Q005/010; scope-ground pin count/MPN remain layout work.

Current [interface implementation](interfaces.md) and [crystal networks](crystal_networks.md) distinguish selected parts from remaining electrical and mechanical checks under B1-Q004/005/008.

USR-16 / ADR-011 accepts four independent Cortex SWD headers. Use the owned J-Link EDU as planned; PICkit 5 is available if needed. The exact header MPN is accepted by ADR-026 (026-reva-connectors.md); numbering/footprint and probe/cable qualification remain B1-Q004/005. Crystal MPNs and initial capacitors are accepted; see [crystal networks](crystal_networks.md).

Current selection — USR-19 / [ADR-014](../../docs/decisions/014-smaller-12mhz-crystal.md): smaller common crystal selected for the four MCU oscillators; ADR-017 separates the FT232HL crystal strategy, with its exact MPN finalized by ADR-030; qualification remains B1-Q008; see BOM B1-B014/019/020. ADR-031 accepts the initial load capacitors. Electrical/pad/footprint and oscillator qualification remain open under B1-Q008/B1-Q005. Assembly: 0805 preferred, 0603 acceptable, no 0402 or smaller; smaller crystals may be considered if leaded.

## Draft SAMC21 allocation — USR-19

[SAMC21 draft pin allocation](../../outputs/samc21-pin-allocation/samc21_pin_allocation.xlsx) contains 48 pad rows per leaf. Stable child IDs B1-P025–B1-P072 belong to SAM0, B1-P073–B1-P120 to SAM1, and B1-P121–B1-P168 to SAM2. Existing B1-P007–B1-P024 remain parent requirement groups, not additional physical assignments. Next unused pin ID: B1-P289 (STM32 uses B1-P169–232; FTDI and EEPROM use B1-P233–288).

All three leaves use the same proposed mapping: CAN0 PA24/PA25, CAN1 PB10/PB11; multidrop SERCOM0 PA08/PA09; ring SERCOM1 PA16/PA17; main crystal PA14/PA15; SWCLK/SWDIO PA30/PA31; RESET pad 40. PA20/PA21 provisionally control the two PHY STB inputs, PA27 drives an LED, and PA02/PA03/PB08/PB09 are four proposed breakouts. The workbook records power/ground/core pins and unused pads, source URLs/pages, direction and ring adjacency.

Evidence: Microchip DS60001479J section 4.2.1 p.22, Table 6-2 pp.29–30, Tables 6-5/6-6 p.34 and USART CTRLA p.505. This is a proposed allocation, with all evidence statuses unverified. B1-Q003/004/005/008/010 remain open for multidrop circuitry, rates, probe/header, errata/current documents, footprint, electrical and clock qualification, and GPIO/LED implementation. No CAD connectivity or hardware validation exists. Proposed PHY controls and breakouts do not select extra parts or future circuitry.

## Draft STM32 gateway allocation

The [allocation workbook](../../outputs/samc21-pin-allocation/samc21_pin_allocation.xlsx) includes an **STM32** sheet for STM32G474RBT6, with 64 physical pad rows, IDs B1-P169–B1-P232. Original groups B1-P001–006 remain parent references. RS-485, LED and breakout rows reference their requirement IDs directly.

| Function | Proposed peripheral / pads | Requirements |
|---|---|---|
| FTDI VCP | USART2 AF7: PA2 TX pad14, PA3 RX pad17, PA1 RTS pad13, PA0 CTS pad12 | B1-R005/014; B1-P004 |
| Multidrop UART | USART1 AF7: PA9 TX pad43, PA10 RX pad44 | B1-R003; B1-P003 |
| External RS-485 | USART3 AF7: PC10 TX pad52, PC11 RX pad53, PB14 DE pad36; GPIO PC12 /RE pad54 | B1-R016/021 |
| FD_CAN_A | FDCAN1 AF9: PA11 RX pad45, PA12 TX pad46; GPIO PC6 STB pad38 | B1-R002; B1-P001 |
| FD_CAN_B | FDCAN2 AF9: PB12 RX pad34, PB13 TX pad35; GPIO PC7 STB pad39 | B1-R002; B1-P002 |
| Debug / reset | PA13 SWDIO pad49, PA14 SWCLK pad50, PG10-NRST pad7 | B1-R007; B1-P005 |
| Crystal / boot | PF0 HSE_IN pad5, PF1 HSE_OUT pad6; reserve PB8-BOOT0 pad61 | B1-R001/015; B1-P006 |
| LED / timing | PA5 LED pad22; PC0–PC3 pads8–11 are timing candidates only, assignments TBD | B1-R019/027 |

Evidence: [ST DS12288 Rev.6](https://www.st.com/resource/en/datasheet/stm32g474rb.pdf), Figure 7 p.50, package column in Table 12 pp.57–72, AF Table 13 pp.73–75. [ES0430 Rev.9](https://www.st.com/resource/en/errata_sheet/es0430-stm32g471xx473xx474xx483xx484xx-device-errata-stmicroelectronics.pdf) identifies applicable USART/FDCAN review areas (§2.16/2.19); actual silicon revision and workaround review remain open.

All assignments are proposed/unverified. Pad uniqueness and chosen peripheral/mux combinations were checked against the retrieved data sheet. Workbook values and formulas on existing sheets were preserved and the added sheet rendered for readability. This is not a completed electrical, errata, footprint, ERC/DRC or bench review. B1-Q003/004/005/008/009/010 remain open. USART2 requires a 168 MHz kernel for the intended 12 Mbaud configuration; default APB clocks must not be assumed sufficient. Review PA9/PA10 control of UCPD dead-battery pulls on unused PB6/PB4, NRST option bytes and BOOT0 recovery policy. No extra ring UART, native USB, third CAN or future circuitry is reserved.


## Draft FTDI and EEPROM allocation

The workbook includes an **FTDI** sheet. FT232HL LQFP48 uses B1-P233–280; selected AT93C56B-SSHM-B SOIC-8 uses B1-P281–288. All 56 rows are unverified draft connections. B1-B004 and B1-B013 remain the component records, with EEPROM selection accepted by USR-23 / ADR-018.

| FT232HL pad / function | Proposed destination |
|---|---|
| 13 / ADBUS0 TXD | STM32 PA3, pad 17, USART2_RX through isolation |
| 14 / ADBUS1 RXD | STM32 PA2, pad 14, USART2_TX through isolation |
| 15 / ADBUS2 RTS# | STM32 PA0, pad 12, USART2_CTS through isolation |
| 16 / ADBUS3 CTS# | STM32 PA1, pad 13, USART2_RTS through isolation |
| 21 / ACBUS0 | EEPROM-configured PWREN# to MC74HC1G14DBVT1G default-off TPS560430 EN polarity interface |
| 43 / EEDATA; 44 / EECLK; 45 / EECS | EEPROM data network; SK pad 2; CS pad 1 |

Source: [FT_000288 v2.2](https://www.ftdichip.cn/Support/Documents/DataSheets/ICs/DS_FT232H.pdf), Tables 3.1–3.5, pp.11–13, and §7 p.49. The FTDI current index lists v2.3; reconcile it and TN_130 with actual silicon before verification. The new sheet also accounts for every supply/ground, crystal, REF, TEST, RESET# and unused pin. VCCA/VCORE each receive only their own bypass; EEPROM and VCCIO use independent VCCD power. No native USB, extra GPIO connector or debug header is added.

EEPROM evidence: DS20006260B pp.3–9 and 31, linked in ADR-018 and the sheet. B1-Q012 retains timing/startup/programming/footprint checks; B1-Q002 retains power-off isolation, support parts, USB current and default-off logic; B1-Q008 retains crystal qualification. UART cross-directions were checked against the STM32 sheet. All 48 FTDI pads and eight EEPROM pads have unique IDs and pad numbers within each device. No CAD exists to compare, and no ERC/DRC or hardware test was performed.


## Gateway reset and deferred recovery

[ADR-042](../../docs/decisions/042-header-resistors-recovery-scope.md) defers automated CBUS recovery to Rev B. ACBUS5/pad29 (B1-P261) and ACBUS6/pad30 (B1-P262) are unconnected in Rev A. Keep STM32 NRST/pad7 (B1-P175) on independent SWD reset and PB8/BOOT0/pad61 (B1-P229) default low. B1-B053 has zero parts/footprints; ordinary reset/boot support remains B1-B010, B1-Q005. Stable physical-pad IDs remain unchanged.

## Accepted connector selections

ADR-026 retains connector MPN selections. ADR-041 / USR-35 replaces the separate GPIO/debug headers with four combined 1x8 timing/debug headers. One selected 40-position strip supplies all 32 positions. General ADC, SPI/I2C and GPIO breakouts are deferred. Resistor selections and PCB test pads plus fitted scope-ground access from ADR-039 remain in force. Exact timing MCU pads remain TBD under B1-Q005/010; scope-ground pin count/MPN remain layout work. B1-Q004/005 retain terminal numbering, footprints, SWD cable/key and adapter checks. See [timing headers](timing_headers.md).


## Per-MCU debug UARTs — ADR-032

Dedicated 115200-baud debug UARTs implement B1-R025 using pins 1=MCU RX, 2=MCU TX and grounds 3/6 of the [combined timing/debug header](timing_headers.md); 3.3 V logic, 8N1/no flow control. Each RX/TX has its own 330 ohm near the MCU (B1-B076 / ADR-042); each timing signal likewise has its own resistor. Shared SYNC/TRIG fan out on the header side of the four input resistors, not on the MCU side.

| MCU | TX / stable ID | RX / stable ID | Peripheral |
|---|---|---|---|
| GW | PB11 pad33 / B1-P201 | PB10 pad30 / B1-P198 | LPUART1 AF8 |
| SAM0 | PA12 pad21 / B1-P045 | PA13 pad22 / B1-P046 | SERCOM2 mux C, PAD0 TX/PAD1 RX |
| SAM1 | PA12 pad21 / B1-P093 | PA13 pad22 / B1-P094 | SERCOM2 mux C, PAD0 TX/PAD1 RX |
| SAM2 | PA12 pad21 / B1-P141 | PA13 pad22 / B1-P142 | SERCOM2 mux C, PAD0 TX/PAD1 RX |

All eight pads were previously unused. Existing network, SWD, boot assignments are preserved; previous general-breakout pads are now unassigned timing candidates. Workbook rows include source locators; [ADR-032](../../docs/decisions/032-debug-uarts.md) records setup and evidence. B1-Q014 retains baud, electrical, adapter/off-state and footprint checks. No row is marked verified.

## BOM reconciliation and selected interfaces

The [BOM audit](remaining_parts.md) splits already accepted bridge passives from B1-B017 into B1-B061–065 without changing pad allocations. [RS-485 and UART multidrop parts](interfaces.md) are accepted under ADR-034/033/039; electrical qualification remains B1-Q003/009. No new verified MCU mux, driver pin allocation or source-CAD connectivity is asserted.

## Accepted UART_MD driver — ADR-033

B1-B066 is the second SN74LV125APWR, separate from B1-B016. Existing MCU UART_MD TX/RX reservations are retained. The following channel-to-node ordering is a proposed implementation allocation; all evidence remains unverified.

| Node | TX to /OE pin | A pin to GND | Y pin to shared UART_MD |
|---|---:|---:|---:|
| GW | 1 | 2 | 3 |
| SAM0 | 4 | 5 | 6 |
| SAM1 | 10 | 9 | 8 |
| SAM2 | 13 | 12 | 11 |

PW package pin 14 to 3V3_SYS, pin 7 to GND; one local 100 nF from existing B1-B036 auxiliary reserve. All four UART_MD_RX inputs observe the shared bus. [TI SCES124O Rev.O p.3](https://www.ti.com/lit/ds/symlink/sn74lv125a.pdf) supplies pin functions; [ADR-033](../../docs/decisions/033-open-drain-uart-buffer.md) records selection. B1-Q003/005 retain exact MCU mux/footprint, supply-ramp and rate checks. The four accepted /OE pull-ups are B1-B008; the accepted shared bus pull-up is B1-B074 (ADR-039). No workbook MCU pad changes or source-CAD connections are claimed.

## RS-485 and termination — ADR-034

Selected B1-B021 ST3485EBDR SO8: 1 RO to gateway RX; 2 /RE; 3 DE; 4 DI from gateway TX; 5 GND; 6 A; 7 B; 8 3V3_SYS. Preserve separate gateway DE and /RE reservations. Source: [ST DS2947 Rev12 p.2](https://www.st.com/resource/en/datasheet/st3485eb.pdf). These are device pin functions, not verified MCU mux or source-CAD connectivity. Existing B1-B036 RS-485 bypass remains allocated once. Bias and MCU thresholds remain B1-Q009.

[ADR-034](../../docs/decisions/034-rs485-termination.md) / B1-R026 sets the [termination arrangement](termination.md). Terminal-block position assignment, resistor/jumper footprints and routing remain unverified B1-Q004. No MCU pad reservations or source attachments were changed.

[ADR-035](../../docs/decisions/035-termination-parts.md) / USR-29 accepts the exact termination MPNs in B1-B067–070. [RS-485 bias investigation](rs485_bias.md) records the accepted network, calculations and remote-kit rate check; B1-Q009 remains open.

## Library pin evidence

B1-B002 uses the [imported SAMC21 symbol](../../libraries/symbols/ATSAMC21G17A-AUT/README.md). B1-B044 uses the [DBV-specific TPS22810 symbol and pin table](../../libraries/symbols/TPS22810DBVT/README.md), implementing ADR-019/022. These assignments do not close B1-Q002/005 or verify mux/board connectivity. The [archived earlier bench project](../../libraries/imports/README.md) uses STM32G473RBTx, conflicting with ADR-004; it requires reconciliation before reuse.

B1-B003/012/013 pin evidence is available in the [TCAN3413DR](../../libraries/symbols/TCAN3413DR/README.md), [TPS560430X3FDBVR](../../libraries/symbols/TPS560430X3FDBVR/README.md) and [AT93C56B-SSHM-B](../../libraries/symbols/AT93C56B-SSHM-B/README.md) libraries. No board net or MCU mux allocation changed; B1-Q002/003/004/011/012 remain open.

[ADR-036](../../docs/decisions/036-rs485-bias.md) / USR-30 accepts two 330 ohm 1% bias resistors in B1-B071: 3V3_SYS to A (ST3485EBDR pin6), B (pin7) to GND. Exact MPN and implementation remain unverified. [TVS selections](interfaces.md) are accepted under ADR-037/038; qualification remains B1-Q004/009.

[ADR-037](../../docs/decisions/037-can-tvs.md) / USR-31 accepts B1-B072: two ESD2CAN24DBZRQ1 arrays near the CAN terminal pairs, DBZ pins1/2 to CANH/CANL and pin3 to GND, independent of termination jumpers. Exact CAD connectivity/footprint and transient qualification remain B1-Q004. [RS-485 TVS selection](interfaces.md) is accepted under ADR-038; qualification remains B1-Q009.

[ADR-038](../../docs/decisions/038-rs485-tvs.md) / USR-32 accepts ESDS452DBZR B1-B073: DBZ pins1/2 to A/B, pin3 GND. Normal operation requires both RS-485 wires within +/-5.5 V of local Board 1 ground. Actual endpoint/offset and transient qualification remain B1-Q009. See [remaining selections and qualification](remaining_parts.md).

The remaining selected IC/array symbols are available for B1-B015/016/018/021/066/072/073; [pin-table checks and coverage](../../libraries/symbols/remaining_ic_symbol_checks.md) are symbol evidence only. MCU mux, board allocations and implemented connectivity remain unverified. RCLAMP0504S pin 5 is VREF, not a no-connect type; an externally unconnected circuit choice is separate.

ADR-041 / USR-35 replaces the separate GPIO/debug headers with four combined 1x8 timing/debug headers. One selected 40-position strip supplies all 32 positions. General ADC, SPI/I2C and GPIO breakouts are deferred. Resistor selections and PCB test pads plus fitted scope-ground access from ADR-039 remain in force. Exact timing MCU pads remain TBD under B1-Q005/010; scope-ground pin count/MPN remain layout work.

Recovery disposition: ADR-042 confirms PB14 ROM startup can assert the draft RS-485 DE, then defers automated recovery. Do not apply the old speculative recovery remaps for Rev A. Network mux and reset defaults still require normal schematic review. First programming uses SWD with external bus peers disconnected.

USR-37: global SYNC and TRIG each have one header-side 10 kohm pull-down to GND (B1-B077). The four per-MCU 330 ohm input branches remain separate; no MCU pad allocation changes. See [timing headers](timing_headers.md) for wiring.
