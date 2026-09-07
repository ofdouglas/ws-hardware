# Board 1 Rev A — current bill of materials

Status: planning BOM · Reviewed: 2026-09-06 · Authority: [bom.csv](bom.csv) and [accepted decisions](../../docs/decisions/README.md).

“Decided” corresponds to `accepted` in the CSV. “Provisional” corresponds to `proposed`. Part selection and evidence are separate: all rows remain unverified. Quantities are per-board allocations; TBD counts and cut-strip consumption need reconciliation against source CAD before procurement.

Current design uses TPS560430, TPS22810 with 47 nF CT, no external FTDI supervisor, accepted ceramic SAM core capacitors, and the finalized crystal/load-capacitor MPNs. Earlier SC189 and supervisor descriptions are retained in their historical ADRs, not as current BOM instructions.

## Decided exact MPNs

| ID | Qty | Function | Manufacturer / MPN | Value / package | Authority |
|---|---:|---|---|---|---|
| B1-B001 | 1 | Gateway MCU | STMicroelectronics / STM32G474RBT6 | NA; LQFP64 (source; verify) | ADR-004 |
| B1-B002 | 3 | Leaf MCU | Microchip / ATSAMC21G17A-AUT | NA; TQFP48 (source; verify) | ADR-004 |
| B1-B003 | 8 | CAN-FD PHYs | Texas Instruments / TCAN3413DR | TBD; SOIC-8; footprint review pending | ADR-002 |
| B1-B004 | 1 | USB-UART bridge | FTDI / FT232HL-REEL | TBD; LQFP48; footprint review pending | ADR-001 |
| B1-B005 | 1 | USB 2.0 Standard-B receptacle | On Shore Technology Inc. / USB-B1HSB6 | TBD; TBD | ADR-001; ADR-030 |
| B1-B006 | 1 | VBUS TVS | Littelfuse / SMF6.0A | TBD; SOD-123F | ADR-019; ADR-022; ADR-024 |
| B1-B009 | 4 | Independent Cortex SWD/reset headers | CNC Tech / 3220-10-0100-00 | 10 positions; Through-hole; 2 x 5; 1.27 mm; shrouded keyed header; footprint TBD | ADR-011; ADR-026 (026-reva-connectors.md) |
| B1-B012 | 1 | 3.3 V buck regulator | Texas Instruments / TPS560430X3FDBVR | 3.3 V fixed; 600 mA; 1.1 MHz FPWM; SOT-23-6 | ADR-021 |
| B1-B013 | 1 | FTDI configuration EEPROM | Microchip Technology / AT93C56B-SSHM-B | 2 Kbit; 128 x 16; 3.3 V; SOIC-8; 3.9 mm body; 1.27 mm pitch; footprint TBD | ADR-001; ADR-018 |
| B1-B014 | 1 | FTDI crystal | ECS Inc. / ECS-120-18-5PX-CKM-TR | 12 MHz; CL 18 pF; HC-49/US leaded SMT; 11.4 x 4.8 x 4.3 mm; footprint TBD | ADR-001; ADR-017; ADR-030 |
| B1-B015 | 1 | Main buck enable control | onsemi / MC74HC1G14DBVT1G | Single Schmitt inverter; SC-74A; 0.95 mm pitch | ADR-013; ADR-024 |
| B1-B016 | 1 | UART power-off isolation | Texas Instruments / SN74LV125APWR | TBD; TSSOP-14; footprint review pending | ADR-001; ADR-013 |
| B1-B018 | 1 | USB data-line ESD protection | Semtech Corporation / RCLAMP0504S.TCT | TBD; SOT-23-6; footprint review pending | ADR-015 |
| B1-B019 | 1 | Gateway main crystal | ECS Inc. / ECS-120-20-3X-EN-TR | 12 MHz; CL 20 pF; Miniature HC-49/US leaded SMT; 7.0 x 4.1 x 2.3 mm; footprint TBD | ADR-005; ADR-014 |
| B1-B020 | 3 | SAM main crystals | ECS Inc. / ECS-120-20-3X-EN-TR | 12 MHz; CL 20 pF; Miniature HC-49/US leaded SMT; 7.0 x 4.1 x 2.3 mm; footprint TBD | ADR-005; ADR-014 |
| B1-B021 | 1 | Rev A external RS-485 PHY | STMicroelectronics / ST3485EBDR | 3.0-3.6 V; half-duplex; guaranteed 12 Mbps; SO8; 3.9 mm body; footprint review pending | ADR-007; ADR-034 |
| B1-B022 | 1 | Signal terminal block | Phoenix Contact / 1989803 | PTSA 0.5/8-2.5-F; Through-hole; 8 positions; 2.5 mm pitch; 45-degree wire entry; footprint TBD | ADR-007; ADR-026 (026-reva-connectors.md) |
| B1-B024 | 4 | MCU status LEDs | ROHM Semiconductor / CSL1901DW1 | Orange LED; 1.8 V typ at 2 mA; 0603; 1.6 x 0.8 x 0.55 mm | ADR-007; ADR-029 |
| B1-B025 | 1 | Board main-power LED | ROHM Semiconductor / CSL1901DW1 | Orange LED; 1.8 V typ at 2 mA; 0603; 1.6 x 0.8 x 0.55 mm | ADR-007; ADR-029 |
| B1-B027 | TBD | GPIO breakout headers | Sullins Connector Solutions / PRPC040SAAN-RC | 40-position source strip; Through-hole; 1 x 40 breakaway male strip; 2.54 mm pitch; cut lengths/footprints TBD | ADR-007; ADR-026 (026-reva-connectors.md) |
| B1-B028 | 1 | Buck inductor | Bourns / SRN6045TA-120M | 12 uH +/-20%; 6 x 6 mm semi-shielded SMT | ADR-021; ADR-025 |
| B1-B029 | 1 | Buck input capacitor | TDK / C3216X7R1V106K160AC | 10 uF 35 V X7R +/-10%; 1206 | ADR-021; ADR-025 |
| B1-B030 | 1 | Buck output capacitor | TDK / C3225X7R1C226M250AC | 22 uF 16 V X7R +/-20%; 1210 | ADR-021; ADR-025 |
| B1-B031 | 1 | Buck input HF bypass | KEMET / C0805C104K5RACTU | 100 nF 50 V X7R +/-10%; 0805 | ADR-021; ADR-025 |
| B1-B036 | 39 | Main 3.3 V pin bypass capacitors | KYOCERA AVX / KGM21NR71E104KT | 100 nF 25 V X7R +/-10%; 0805 | ADR-010; ADR-027 |
| B1-B037 | 4 | Shared STM32 analog bulk and SAM local bulk | Samsung Electro-Mechanics / CL21B105KAFNFNE | 1 uF 25 V X7R +/-10%; 0805 | ADR-010; ADR-027 |
| B1-B038 | 1 | STM32 digital bulk | Murata / GRM21BR71C475KE51L | 4.7 uF 16 V X7R +/-10%; 0805 | ADR-010; ADR-027 |
| B1-B039 | 1 | STM32 VDDA HF bypass | Samsung Electro-Mechanics / CL21B103KBANNNC | 10 nF 50 V X7R +/-10%; 0805 | ADR-010; ADR-027 |
| B1-B040 | 3 | SAM VDDCORE regulator capacitors | Samsung Electro-Mechanics / CL21B105KAFNFNE | 1 uF 25 V X7R +/-10%; 0805 | ADR-010; ADR-026 (026-sam-core-ceramic.md); ADR-027 |
| B1-B041 | 3 | SAM VDDCORE HF bypass | KYOCERA AVX / KGM21NR71E104KT | 100 nF 25 V X7R +/-10%; 0805 | ADR-010; ADR-027 |
| B1-B042 | 2 | Gateway crystal load capacitors | KEMET / C0805C330F5GACTU | 33 pF +/-1%; 50 V C0G; 0805 | ADR-005; ADR-014; ADR-031 |
| B1-B043 | 6 | Three SAM crystal load capacitors (two per MCU) | KEMET / C0805C330F5GACTU | 33 pF +/-1%; 50 V C0G; 0805 | ADR-005; ADR-014; ADR-031 |
| B1-B044 | 1 | Input attachment-ramp switch | Texas Instruments / TPS22810DBVT | NA; SOT-23-6 | ADR-019; ADR-022 |
| B1-B045 | 1 | Raw VBUS direct bypass | Samsung Electro-Mechanics / CL21B105KAFNFNE | 1 uF 25 V X7R +/-10%; 0805 | ADR-019; ADR-027 |
| B1-B046 | 1 | Raw VBUS damping capacitor | Samsung Electro-Mechanics / CL21A475KBQNNNE | 4.7 uF 50 V X5R +/-10%; 0805 | ADR-019; ADR-029 |
| B1-B047 | 1 | Raw VBUS damping resistor | KOA Speer Electronics Inc. / SG73P2BTTD1R0J | 1 ohm +/-5%; anti-surge pulse resistor; 1206 | ADR-019; ADR-029 |
| B1-B048 | 1 | Input switch slew capacitor | Samsung Electro-Mechanics / CL21B473KBCNNNC | 47 nF 50 V X7R +/-10%; 0805 | ADR-022; ADR-027 |
| B1-B051 | 1 | FTDI reset pull-up | Stackpole Electronics Inc. / RMCF0805FT10K0 | 10 kohm +/-1%; 0.125 W; 0805 | ADR-022; ADR-028 |
| B1-B052 | 1 | TPS560430 bootstrap capacitor | KEMET / C0805C104K5RACTU | 100 nF 50 V X7R +/-10%; 0805 | ADR-021; ADR-025 |
| B1-B054 | 1 | PWREN# inverter input pull-up | Stackpole Electronics Inc. / RMCF0805FT10K0 | 10 kohm +/-1%; 0.125 W; 0805 | ADR-024; ADR-028 |
| B1-B055 | 1 | Main buck EN pull-down | Panasonic Industry / ERJ-6GEYJ473V | 47 kohm +/-5%; 0.125 W; 0805 | ADR-024; ADR-030 |
| B1-B056 | 1 | EEPROM DO series resistor | YAGEO / RC0805FR-072K2L | 2.2 kohm +/-1%; 0.125 W; 0805 | ADR-030 |
| B1-B057 | 1 | FTDI REF resistor | Stackpole Electronics Inc. / RMCF0805FT12K0 | 12 kohm +/-1%; 0.125 W; 0805 | ADR-030; ADR-031 |
| B1-B058 | 2 | FTDI crystal load capacitors | KEMET / C0805C270F5GACTU | 27 pF +/-1%; 50 V C0G; 0805 | ADR-031 |
| B1-B061 | TBD | Bridge-domain 100 nF bypass capacitors | KYOCERA AVX / KGM21NR71E104KT | 100 nF 25 V X7R +/-10%; 0805 | ADR-027 |
| B1-B062 | TBD | Bridge-domain 1 uF capacitors | Samsung Electro-Mechanics / CL21B105KAFNFNE | 1 uF 25 V X7R +/-10%; 0805 | ADR-027 |
| B1-B063 | TBD | Bridge-domain 4.7 uF capacitors | Murata / GRM21BR71C475KE51L | 4.7 uF 16 V X7R +/-10%; 0805 | ADR-027 |
| B1-B064 | 1 | FTDI RESET# capacitor | Samsung Electro-Mechanics / CL21B103KBANNNC | 10 nF 50 V X7R +/-10%; 0805 | ADR-022; ADR-027 |
| B1-B065 | 1 | EEPROM DO pull-up resistor | Stackpole Electronics Inc. / RMCF0805FT10K0 | 10 kohm +/-1%; 0.125 W; 0805 | ADR-028 |
| B1-B066 | 1 | Onboard open-drain UART quad driver | Texas Instruments / SN74LV125APWR | 4 channels; A=GND; TX drives /OE; TSSOP-14; footprint review pending | ADR-033 |
| B1-B067 | 4 | CAN termination resistors | TE Connectivity Passive Product / CRGP0805F120R | 120 ohm +/-1%; 1/3 W; 0805 | ADR-034; ADR-035 |
| B1-B068 | 1 | Fixed local RS-485 termination resistor | TE Connectivity Passive Product / CRGP0805F120R | 120 ohm +/-1%; 1/3 W; 0805 | ADR-034; ADR-035 |
| B1-B069 | 2 | CAN termination jumper headers | Sullins Connector Solutions / PRPC002SAAN-RC | 2 positions; gold flash; Through-hole; 1x2; 2.54 mm | ADR-034; ADR-035 |
| B1-B070 | 2 | CAN termination shunts | Sullins Connector Solutions / SPC02SYAN | Gold flash; 1x2; 2.54 mm; closed-top shunt | ADR-034; ADR-035 |
| B1-B072 | 2 | External CAN pair TVS arrays | Texas Instruments / ESD2CAN24DBZRQ1 | Two channels; +/-24 V standoff; SOT-23-3 DBZ | ADR-037 |
| B1-B073 | 1 | External RS-485 pair TVS array | Texas Instruments / ESDS452DBZR | Two channels; +/-5.5 V standoff; SOT-23-3 DBZ | ADR-038 |

## Decided scope; exact parts remain open

| ID | Qty | Function | Manufacturer / MPN | Value / package | Authority |
|---|---:|---|---|---|---|
| B1-B053 | TBD | Gateway CBUS reset and BOOT0 interfaces | TBD / TBD | TBD; TBD | ADR-023 |
| B1-B059 | 4 | Per-MCU text debug UART headers | TBD / TBD | TBD; 1x3; 2.54 mm pitch; through-hole proposed | ADR-032 |
| B1-B071 | 2 | RS-485 idle-bus bias resistors | TBD / TBD | 330 ohm +/-1%; rating TBD; 0805 | ADR-036 |

## Provisional parts and unfinished networks

| ID | Qty | Function | Manufacturer / MPN | Value / package | Authority |
|---|---:|---|---|---|---|
| B1-B007 | TBD | Remaining CAN interface protection | TBD / TBD | TBD; TBD | ADR-002; ADR-034; ADR-037 |
| B1-B008 | TBD | Remaining open-drain UART support network | TBD / TBD | TBD; TBD | ADR-033 |
| B1-B010 | TBD | Remaining MCU boot/reset support | TBD / TBD | TBD; TBD | ADR-004 |
| B1-B011 | TBD | Test points | TBD / TBD | TBD; TBD | NA |
| B1-B017 | TBD | Remaining unenumerated USB/bridge support network | TBD / TBD | TBD; TBD | ADR-001; ADR-018; ADR-024 |
| B1-B023 | TBD | Remaining RS-485 protection and control network | TBD / TBD | TBD; TBD | ADR-007; ADR-034; ADR-036; ADR-038 |
| B1-B026 | 5 | LED resistors | KOA Speer Electronics Inc. / RK73H2ATTD3301F | 3.3 kohm +/-1%; 0.25 W; 0805 | ADR-007 |
| B1-B060 | TBD | Debug UART support and off-state protection | TBD / TBD | TBD; TBD; 0805 passives preferred | ADR-032 |

## Superseded; excluded from assembly and procurement

| ID | Qty | Function | Manufacturer / MPN | Value / package | Authority |
|---|---:|---|---|---|---|
| B1-B032 | 0 | Buck mode strap | TBD / TBD | 61.9 kohm 1%; 0603 | ADR-008 |
| B1-B033 | 0 | Buck output strap | TBD / TBD | 249 kohm 1%; 0603 | ADR-008 |
| B1-B034 | 0 | Buck soft-start capacitor | TBD / TBD | 10 nF 5% C0G; 0603 | ADR-008 |
| B1-B035 | 0 | Buck PG pullup | TBD / TBD | 100 kohm; 0603 | ADR-008 |
| B1-B049 | 0 | FTDI USB_5V reset supervisor | Texas Instruments / TLV803EA42RDBZR | 4.2 V falling threshold; 200 ms nominal; SOT-23-3; R pinout | ADR-020; ADR-022 |
| B1-B050 | 0 | Supervisor supply bypass | TBD / TBD | 100 nF X7R; <=10%; >=10 V; 0805 preferred | ADR-020; ADR-022 |

## Allocation and sourcing notes

- Exact DigiKey order codes, manufacturer evidence and remaining checks are in the CSV. [BOM audit](bom_review.md) records corrections; [interface candidates](rs485_uart_candidates.md) records new proposals and dated availability.
- B1-B061–065 expose previously accepted bridge capacitor/resistor choices formerly hidden in B1-B017. B1-B017 now excludes all split rows. Unknown bridge capacitor counts remain TBD; this is not an increase in designed capacitance.
- B1-B027 is a 40-position GPIO source strip with cut consumption TBD. B1-B059 is four fitted text-debug headers, with exact source part still undecided. Do not order four full strips merely because four cut headers are needed.
- B1-B036 includes four auxiliary bypass reserves: one for B1-B016 and one for B1-B066, leaving two. Total bypass quantity and nominal main-rail capacitance are unchanged.
- Main 3.3 V nominal allocation is 39×0.1 + 4×1 + 4.7 + 0.01 + 22 = **34.61 uF**. Positive tolerance/temperature screen is 22×1.20×1.15 + 12.61×1.10×1.15 = **46.31165 uF**. These are allocation estimates, not qualified effective-C bounds; no SC189 30 uF limit applies.
- Separate SAM core networks, buck input/bootstrap and FTDI-domain capacitors are not direct main-rail output capacitance. Their startup loads still require review.
- Superseded rows retain stable IDs and zero quantities. Their `assembly=tbd` schema value does not authorize fitted or DNP footprints.
- Remaining blockers include CAD footprint/connectivity, interface termination/protection, bridge support counts, GPIO/debug cut schedules and loads, power/startup and oscillator qualification. No ERC/DRC or hardware test was performed.

ADR-033 / USR-27 decides the second SN74LV125APWR: total two ICs across B1-B016/066. B1-B008 holds only residual support. [Termination arrangement](termination_proposal.md) and ST3485EBDR are accepted by ADR-034 / USR-28. B1-B067–070 separate the five resistors and two header/shunt sets from residual protection rows. [Exact termination parts](termination_parts.md) accepted ADR-035. Bias network/value accepted ADR-036 in B1-B071; exact bias MPN open; see [investigation](rs485_bias.md).

## Local library assignments

B1-B002 and B1-B044 now have project-local symbol IDs and default-footprint assignments in bom.csv; see [symbol catalog](../../libraries/symbols/README.md). Both remain unverified at the board-allocation level. The imported SC189 symbol is historical and does not add a BOM row.

B1-B003/012/013 now have exact-part local symbols and standard-footprint assignments in bom.csv. See the [symbol checks](../../libraries/symbols/symbol_checks.md); allocation evidence remains unverified.

CAN TVS arrays decided ADR-037; B1-B007 excludes B1-B072. [RS-485 alternatives](rs485_tvs_alternatives.md) remain proposed under B1-B023.

ESDS452DBZR is decided ADR-038 in B1-B073. Current remaining choices and implementation work: [BOM closeout](bom_closeout.md).

[Selected IC symbol coverage](../../libraries/symbols/remaining_ic_symbol_checks.md) now includes all 13 distinct selected ICs/arrays: six new local libraries plus the existing local and default KiCad symbols. B1-B015/016/018/021/066/072/073 receive exact local IDs; B1-B001/004 use default STM32/FTDI IDs. B1-B004 footprint remains TBD. Evidence remains unverified.
