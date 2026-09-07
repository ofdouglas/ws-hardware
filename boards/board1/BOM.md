# Board 1 Rev A bill of materials

Status: planning BOM; current through ADR-039. Tables derived from [bom.csv](bom.csv), which owns quantities, selection/evidence status, library assignments and sourcing evidence. Accepted does not mean electrically verified or procurement-ready. All parts are to be sourced through DigiKey; refresh stock/order codes before purchase.

## Accepted exact MPNs

| ID | Qty | Function | Manufacturer / MPN | Value / package | Evidence | Authority |
|---|---:|---|---|---|---|---|
| B1-B001 | 1 | Gateway MCU | STMicroelectronics / STM32G474RBT6 | NA; LQFP64 (source; verify) | unverified | ADR-004 |
| B1-B002 | 3 | Leaf MCU | Microchip / ATSAMC21G17A-AUT | NA; TQFP48 (source; verify) | unverified | ADR-004 |
| B1-B003 | 8 | CAN-FD PHYs | Texas Instruments / TCAN3413DR | TBD; SOIC-8; footprint review pending | unverified | ADR-002 |
| B1-B004 | 1 | USB-UART bridge | FTDI / FT232HL-REEL | TBD; LQFP48; footprint review pending | unverified | ADR-001 |
| B1-B005 | 1 | USB 2.0 Standard-B receptacle | On Shore Technology Inc. / USB-B1HSB6 | TBD; TBD | unverified | ADR-001; ADR-030 |
| B1-B006 | 1 | VBUS TVS | Littelfuse / SMF6.0A | TBD; SOD-123F | unverified | ADR-019; ADR-022; ADR-024 |
| B1-B008 | 4 | UART_MD driver /OE pull-up resistors | Stackpole Electronics Inc. / RMCF0805FT10K0 | 10 kohm +/-1%; 0.125 W; 0805 | unverified | ADR-033; ADR-039 |
| B1-B009 | 4 | Independent Cortex SWD/reset headers | CNC Tech / 3220-10-0100-00 | 10 positions; Through-hole; 2 x 5; 1.27 mm; shrouded keyed header; footprint TBD | unverified | ADR-011; ADR-026 (026-reva-connectors.md) |
| B1-B012 | 1 | 3.3 V buck regulator | Texas Instruments / TPS560430X3FDBVR | 3.3 V fixed; 600 mA; 1.1 MHz FPWM; SOT-23-6 | unverified | ADR-021 |
| B1-B013 | 1 | FTDI configuration EEPROM | Microchip Technology / AT93C56B-SSHM-B | 2 Kbit; 128 x 16; 3.3 V; SOIC-8; 3.9 mm body; 1.27 mm pitch; footprint TBD | unverified | ADR-001; ADR-018 |
| B1-B014 | 1 | FTDI crystal | ECS Inc. / ECS-120-18-5PX-CKM-TR | 12 MHz; CL 18 pF; HC-49/US leaded SMT; 11.4 x 4.8 x 4.3 mm; footprint TBD | unverified | ADR-001; ADR-017; ADR-030 |
| B1-B015 | 1 | Main buck enable control | onsemi / MC74HC1G14DBVT1G | Single Schmitt inverter; SC-74A; 0.95 mm pitch | unverified | ADR-013; ADR-024 |
| B1-B016 | 1 | UART power-off isolation | Texas Instruments / SN74LV125APWR | TBD; TSSOP-14; footprint review pending | unverified | ADR-001; ADR-013 |
| B1-B018 | 1 | USB data-line ESD protection | Semtech Corporation / RCLAMP0504S.TCT | TBD; SOT-23-6; footprint review pending | unverified | ADR-015 |
| B1-B019 | 1 | Gateway main crystal | ECS Inc. / ECS-120-20-3X-EN-TR | 12 MHz; CL 20 pF; Miniature HC-49/US leaded SMT; 7.0 x 4.1 x 2.3 mm; footprint TBD | unverified | ADR-005; ADR-014 |
| B1-B020 | 3 | SAM main crystals | ECS Inc. / ECS-120-20-3X-EN-TR | 12 MHz; CL 20 pF; Miniature HC-49/US leaded SMT; 7.0 x 4.1 x 2.3 mm; footprint TBD | unverified | ADR-005; ADR-014 |
| B1-B021 | 1 | Rev A external RS-485 PHY | STMicroelectronics / ST3485EBDR | 3.0-3.6 V; half-duplex; guaranteed 12 Mbps; SO8; 3.9 mm body; footprint review pending | unverified | ADR-007; ADR-034 |
| B1-B022 | 1 | Signal terminal block | Phoenix Contact / 1989803 | PTSA 0.5/8-2.5-F; Through-hole; 8 positions; 2.5 mm pitch; 45-degree wire entry; footprint TBD | unverified | ADR-007; ADR-026 (026-reva-connectors.md) |
| B1-B024 | 4 | MCU status LEDs | ROHM Semiconductor / CSL1901DW1 | Orange LED; 1.8 V typ at 2 mA; 0603; 1.6 x 0.8 x 0.55 mm | unverified | ADR-007; ADR-029 |
| B1-B025 | 1 | Board main-power LED | ROHM Semiconductor / CSL1901DW1 | Orange LED; 1.8 V typ at 2 mA; 0603; 1.6 x 0.8 x 0.55 mm | unverified | ADR-007; ADR-029 |
| B1-B026 | 5 | LED resistors | KOA Speer Electronics Inc. / RK73H2ATTD3301F | 3.3 kohm +/-1%; 0.25 W; 0805 | unverified | ADR-007; ADR-039 |
| B1-B027 | 1 | Source strip for GPIO and debug UART headers | Sullins Connector Solutions / PRPC040SAAN-RC | 40-position strip; 32 positions allocated; Through-hole; 1 x 40 breakaway male strip; 2.54 mm pitch; cut lengths/footprints TBD | unverified | ADR-007; ADR-026 (026-reva-connectors.md); ADR-039 |
| B1-B028 | 1 | Buck inductor | Bourns / SRN6045TA-120M | 12 uH +/-20%; 6 x 6 mm semi-shielded SMT | unverified | ADR-021; ADR-025 |
| B1-B029 | 1 | Buck input capacitor | TDK / C3216X7R1V106K160AC | 10 uF 35 V X7R +/-10%; 1206 | unverified | ADR-021; ADR-025 |
| B1-B030 | 1 | Buck output capacitor | TDK / C3225X7R1C226M250AC | 22 uF 16 V X7R +/-20%; 1210 | unverified | ADR-021; ADR-025 |
| B1-B031 | 1 | Buck input HF bypass | KEMET / C0805C104K5RACTU | 100 nF 50 V X7R +/-10%; 0805 | unverified | ADR-021; ADR-025 |
| B1-B036 | 39 | Main 3.3 V pin bypass capacitors | KYOCERA AVX / KGM21NR71E104KT | 100 nF 25 V X7R +/-10%; 0805 | unverified | ADR-010; ADR-027 |
| B1-B037 | 4 | Shared STM32 analog bulk and SAM local bulk | Samsung Electro-Mechanics / CL21B105KAFNFNE | 1 uF 25 V X7R +/-10%; 0805 | unverified | ADR-010; ADR-027 |
| B1-B038 | 1 | STM32 digital bulk | Murata / GRM21BR71C475KE51L | 4.7 uF 16 V X7R +/-10%; 0805 | unverified | ADR-010; ADR-027 |
| B1-B039 | 1 | STM32 VDDA HF bypass | Samsung Electro-Mechanics / CL21B103KBANNNC | 10 nF 50 V X7R +/-10%; 0805 | unverified | ADR-010; ADR-027 |
| B1-B040 | 3 | SAM VDDCORE regulator capacitors | Samsung Electro-Mechanics / CL21B105KAFNFNE | 1 uF 25 V X7R +/-10%; 0805 | unverified | ADR-010; ADR-026 (026-sam-core-ceramic.md); ADR-027 |
| B1-B041 | 3 | SAM VDDCORE HF bypass | KYOCERA AVX / KGM21NR71E104KT | 100 nF 25 V X7R +/-10%; 0805 | unverified | ADR-010; ADR-027 |
| B1-B042 | 2 | Gateway crystal load capacitors | KEMET / C0805C330F5GACTU | 33 pF +/-1%; 50 V C0G; 0805 | unverified | ADR-005; ADR-014; ADR-031 |
| B1-B043 | 6 | Three SAM crystal load capacitors (two per MCU) | KEMET / C0805C330F5GACTU | 33 pF +/-1%; 50 V C0G; 0805 | unverified | ADR-005; ADR-014; ADR-031 |
| B1-B044 | 1 | Input attachment-ramp switch | Texas Instruments / TPS22810DBVT | NA; SOT-23-6 | unverified | ADR-019; ADR-022 |
| B1-B045 | 1 | Raw VBUS direct bypass | Samsung Electro-Mechanics / CL21B105KAFNFNE | 1 uF 25 V X7R +/-10%; 0805 | unverified | ADR-019; ADR-027 |
| B1-B046 | 1 | Raw VBUS damping capacitor | Samsung Electro-Mechanics / CL21A475KBQNNNE | 4.7 uF 50 V X5R +/-10%; 0805 | unverified | ADR-019; ADR-029 |
| B1-B047 | 1 | Raw VBUS damping resistor | KOA Speer Electronics Inc. / SG73P2BTTD1R0J | 1 ohm +/-5%; anti-surge pulse resistor; 1206 | unverified | ADR-019; ADR-029 |
| B1-B048 | 1 | Input switch slew capacitor | Samsung Electro-Mechanics / CL21B473KBCNNNC | 47 nF 50 V X7R +/-10%; 0805 | unverified | ADR-022; ADR-027 |
| B1-B051 | 1 | FTDI reset pull-up | Stackpole Electronics Inc. / RMCF0805FT10K0 | 10 kohm +/-1%; 0.125 W; 0805 | unverified | ADR-022; ADR-028 |
| B1-B052 | 1 | TPS560430 bootstrap capacitor | KEMET / C0805C104K5RACTU | 100 nF 50 V X7R +/-10%; 0805 | unverified | ADR-021; ADR-025 |
| B1-B054 | 1 | PWREN# inverter input pull-up | Stackpole Electronics Inc. / RMCF0805FT10K0 | 10 kohm +/-1%; 0.125 W; 0805 | unverified | ADR-024; ADR-028 |
| B1-B055 | 1 | Main buck EN pull-down | Panasonic Industry / ERJ-6GEYJ473V | 47 kohm +/-5%; 0.125 W; 0805 | unverified | ADR-024; ADR-030 |
| B1-B056 | 1 | EEPROM DO series resistor | YAGEO / RC0805FR-072K2L | 2.2 kohm +/-1%; 0.125 W; 0805 | unverified | ADR-030 |
| B1-B057 | 1 | FTDI REF resistor | Stackpole Electronics Inc. / RMCF0805FT12K0 | 12 kohm +/-1%; 0.125 W; 0805 | unverified | ADR-030; ADR-031 |
| B1-B058 | 2 | FTDI crystal load capacitors | KEMET / C0805C270F5GACTU | 27 pF +/-1%; 50 V C0G; 0805 | unverified | ADR-031 |
| B1-B059 | 4 | Per-MCU text debug UART headers | Sullins Connector Solutions / PRPC040SAAN-RC | Four placement pieces; included in B1-B027 strip; Cut 1x3 sections; 2.54 mm; through-hole | unverified | ADR-032; ADR-039 |
| B1-B061 | TBD | Bridge-domain 100 nF bypass capacitors | KYOCERA AVX / KGM21NR71E104KT | 100 nF 25 V X7R +/-10%; 0805 | unverified | ADR-027 |
| B1-B062 | TBD | Bridge-domain 1 uF capacitors | Samsung Electro-Mechanics / CL21B105KAFNFNE | 1 uF 25 V X7R +/-10%; 0805 | unverified | ADR-027 |
| B1-B063 | TBD | Bridge-domain 4.7 uF capacitors | Murata / GRM21BR71C475KE51L | 4.7 uF 16 V X7R +/-10%; 0805 | unverified | ADR-027 |
| B1-B064 | 1 | FTDI RESET# capacitor | Samsung Electro-Mechanics / CL21B103KBANNNC | 10 nF 50 V X7R +/-10%; 0805 | unverified | ADR-022; ADR-027 |
| B1-B065 | 1 | EEPROM DO pull-up resistor | Stackpole Electronics Inc. / RMCF0805FT10K0 | 10 kohm +/-1%; 0.125 W; 0805 | unverified | ADR-028 |
| B1-B066 | 1 | Onboard open-drain UART quad driver | Texas Instruments / SN74LV125APWR | 4 channels; A=GND; TX drives /OE; TSSOP-14; footprint review pending | unverified | ADR-033 |
| B1-B067 | 4 | CAN termination resistors | TE Connectivity Passive Product / CRGP0805F120R | 120 ohm +/-1%; 1/3 W; 0805 | unverified | ADR-034; ADR-035 |
| B1-B068 | 1 | Fixed local RS-485 termination resistor | TE Connectivity Passive Product / CRGP0805F120R | 120 ohm +/-1%; 1/3 W; 0805 | unverified | ADR-034; ADR-035 |
| B1-B069 | 2 | CAN termination jumper headers | Sullins Connector Solutions / PRPC002SAAN-RC | 2 positions; gold flash; Through-hole; 1x2; 2.54 mm | unverified | ADR-034; ADR-035 |
| B1-B070 | 2 | CAN termination shunts | Sullins Connector Solutions / SPC02SYAN | Gold flash; 1x2; 2.54 mm; closed-top shunt | unverified | ADR-034; ADR-035 |
| B1-B071 | 2 | RS-485 idle-bus bias resistors | TE Connectivity Passive Product / CRGP0805F330R | 330 ohm +/-1%; 1/3 W; 0805 | unverified | ADR-036; ADR-039 |
| B1-B072 | 2 | External CAN pair TVS arrays | Texas Instruments / ESD2CAN24DBZRQ1 | Two channels; +/-24 V standoff; SOT-23-3 DBZ; footprint review pending | unverified | ADR-037 |
| B1-B073 | 1 | External RS-485 pair TVS array | Texas Instruments / ESDS452DBZR | Two channels; +/-5.5 V standoff; SOT-23-3 DBZ; footprint review pending | unverified | ADR-038 |
| B1-B074 | 1 | UART_MD shared bus pull-up resistor | Stackpole Electronics Inc. / RMCF0805FT470R | 470 ohm +/-1%; 0.125 W; 0805 | unverified | ADR-039 |

## Accepted scope / non-purchased categories

| ID | Qty | Function | Manufacturer / MPN | Value / package | Evidence | Authority |
|---|---:|---|---|---|---|---|
| B1-B011 | 0 | PCB test pads; no purchased components | NA / NA | Pad count/locations TBD; PCB copper pads | unverified | ADR-039 |
| B1-B053 | TBD | Gateway CBUS reset and BOOT0 interfaces | TBD / TBD | TBD; TBD | unverified | ADR-023 |
| B1-B075 | TBD | Fitted scope-probe ground clip pins | TBD / TBD | TBD; TBD | unverified | ADR-039 |

## Proposed residual networks

| ID | Qty | Function | Manufacturer / MPN | Value / package | Evidence | Authority |
|---|---:|---|---|---|---|---|
| B1-B007 | TBD | Remaining CAN interface protection | TBD / TBD | TBD; TBD | unverified | ADR-002; ADR-034; ADR-037 |
| B1-B010 | TBD | Remaining MCU boot/reset support | TBD / TBD | TBD; TBD | unverified | ADR-004 |
| B1-B017 | TBD | Remaining unenumerated USB/bridge support network | TBD / TBD | TBD; TBD | unverified | ADR-001; ADR-018; ADR-024 |
| B1-B023 | TBD | Remaining RS-485 protection and control network | TBD / TBD | TBD; TBD | unverified | ADR-007; ADR-034; ADR-036; ADR-038 |
| B1-B060 | TBD | Debug UART support and off-state protection | TBD / TBD | TBD; TBD; 0805 passives preferred | unverified | ADR-032 |

## Superseded; excluded from assembly and procurement

| ID | Qty | Function | Manufacturer / MPN | Value / package | Evidence | Authority |
|---|---:|---|---|---|---|---|
| B1-B032 | 0 | Buck mode strap | TBD / TBD | 61.9 kohm 1%; 0603 | unverified | ADR-008 |
| B1-B033 | 0 | Buck output strap | TBD / TBD | 249 kohm 1%; 0603 | unverified | ADR-008 |
| B1-B034 | 0 | Buck soft-start capacitor | TBD / TBD | 10 nF 5% C0G; 0603 | unverified | ADR-008 |
| B1-B035 | 0 | Buck PG pullup | TBD / TBD | 100 kohm; 0603 | unverified | ADR-008 |
| B1-B049 | 0 | FTDI USB_5V reset supervisor | Texas Instruments / TLV803EA42RDBZR | 4.2 V falling threshold; 200 ms nominal; SOT-23-3; R pinout | unverified | ADR-020; ADR-022 |
| B1-B050 | 0 | Supervisor supply bypass | TBD / TBD | 100 nF X7R; <=10%; >=10 V; 0805 preferred | unverified | ADR-020; ADR-022 |

## Allocation and sourcing notes

- B1-B027 buys one 40-position PRPC040SAAN-RC strip: four 1x5 GPIO and four 1x3 debug sections use 32 positions. B1-B059 counts included placement pieces, not four additional purchased strips. Dedicated CAN jumper headers B1-B069 are separate.
- B1-B011 represents PCB test pads and has zero purchased components. B1-B075 fitted scope-ground pins are accepted scope with MPN/count/locations TBD; spare strip posts are not yet allocated.
- B1-B061–065 expose existing bridge allocations formerly in B1-B017. The residual row excludes all split parts; capacitor counts B1-B061–063 remain TBD. B1-B053 recovery components/counts also remain TBD.
- B1-B036 contains 39 main-rail 100 nF positions, including four auxiliary reserves: VCP and UART_MD buffers consume two, leaving two. [Decoupling](decoupling.md) owns the allocation explanation and 34.61 uF nominal main-rail calculation. Core, bridge, buck-input and bootstrap capacitance are separate.
- Two SN74LV125APWR ICs serve VCP and UART_MD separately. B1-B008 is exactly four accepted 10 kohm /OE pull-ups; B1-B074 is the accepted shared 470 ohm pull-up.
- [Termination](termination.md), [bias](rs485_bias.md) and [interfaces](interfaces.md) describe accepted bus networks. Residual B1-B007/023 exclude their separately listed resistors, jumpers and TVS arrays.
- Superseded rows preserve stable IDs with zero quantities. Their assembly=tbd field does not authorize fitted or DNP footprints.
- [Symbol catalog](../../libraries/symbols/README.md), [exact-part checks](../../libraries/symbols/symbol_checks.md) and [remaining IC coverage](../../libraries/symbols/remaining_ic_symbol_checks.md) describe real library artifacts. Library checks do not verify board allocation or complete schematic/layout sign-off.
- [Remaining selections](remaining_parts.md) indexes unresolved work; [requirements](requirements.md) owns question status. No quantities, choices or verification statuses were changed by this view.
