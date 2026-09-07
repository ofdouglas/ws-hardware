# Board 1 KiCad project — complete Rev A schematic

Completed 2026-09-07 with KiCad 7.0.11, native schematic format20230121, revision A-draft. Open [board1.kicad_pro](board1.kicad_pro). The editable source is the authority for implemented connectivity. This is complete draft capture, not fabrication approval; no PCB layout or fabrication outputs have been created.

| Page | Source | Contents |
|---|---|---|
| 1 | [Overview](board1.kicad_sch) | Hierarchy and scope |
| 2 | [Power](power.kicad_sch) | Preserved USB input/ramp, buck, enable and power LED |
| 3 | [USB](usb_bridge.kicad_sch) | Preserved FTDI/EEPROM and four-channel VCP isolation |
| 4 | [Gateway](gateway.kicad_sch) | STM32G474, supplies, crystal, reset/BOOT0, SWD and timing/debug |
| 5–7 | [SAM0](sam0.kicad_sch), [SAM1](sam1.kicad_sch), [SAM2](sam2.kicad_sch) | Three independent SAMC21 circuits and headers |
| 8–9 | [CAN A](can_a.kicad_sch), [CAN B](can_b.kicad_sch) | Eight PHYs, per-PHY standby defaults and endpoint termination |
| 10 | [Interfaces](interfaces.kicad_sch) | UART_MD quad driver, RS-485/defaults/bias/termination, shared timing pulls |
| 11 | [Access](access.kicad_sch) | External terminal block, three TVS arrays, six ground headers and test pads |

[Complete 11-page review PDF](review/board1-complete.pdf). The earlier two-page power/USB PDF and capture_manifest.json are retained as historical capture evidence; use the complete PDF and [complete_manifest.json](complete_manifest.json) for current review.

## Capture and component reconciliation

239 schematic component objects comprise 220 fitted components/connectors and 19 PCB copper test pads; two removable CAN shunts are assembly accessories without additional PCB footprints. The strip-stock purchase and testpad/shunt exceptions are explicit in [schematic_bom_allocations.json](schematic_bom_allocations.json). All populated components have MPNs, references and footprint assignments in [bom.csv](../bom.csv); no count remains TBD. Evidence status stays unverified until the relevant approval checks finish.

The original 52 power/USB components retain their pin mappings, MPNs and values. Only hierarchy and the VBUS_RAW global name scope changed. The four GW_VCP nets now reach the gateway.

Routine completion choices: four reset pull-ups, three SAM SWCLK pull-ups and gateway BOOT0 pull-down use10k B080; NRST uses100n B081 and each SAM RESET uses10n B082. Eight10k CAN STB pull-ups B083 establish explicit standby. Four RS-485 defaults B023 establish shutdown/idle, and four debug RX10k pull-ups B060 establish idle. These reuse selected MPNs; they are engineering choices within authorized scope, not newly maintainer-accepted decisions. No automatic CBUS recovery or future circuitry was added.

Each timing/debug header has six independent330ohm branches near its MCU. Shared SYNC/TRIG each have one10k pull-down before fanout. Six separately purchased two-pin ground headers reuse PRPC002SAAN-RC and do not consume the eight spare positions in the timing-header strip.

B036 reconciles to37 actual main-rail100n bypasses; two unused planning reserves were removed. Main nominal capacitance becomes34.41uF. B007/B010 residual aggregates now have zero parts; B023 andB060 are fully enumerated. [Decoupling](../decoupling.md) and the generated BOM use the captured counts.

## Evidence and corrections

The MCU review found and fixed an actual workbook error in STM32 pads19–29: LED PA5 is pad19, VSSA pad27, VREF+ pad28 and VDDA pad29. Stable physical-pad IDs were retained. [Pinmap](../pinmap.md) links the corrected workbook and [MCU capture plan](../mcu_capture_plan.json). All208 MCU pads were independently compared to that plan/workbook and a fresh KiCad netlist. Timing interrupts are GWPC0/PC1 EXTI0/1 and SAMPA02/PA03 EXTINT2/3; events use GWPC2/PC3 and SAMPB08/PB09.

The RS-485 RO-to-PC11 high-level screen passes: ST3485 VOH>=2.0V at4mA; PC11 FT_f supports alternate guaranteed VIH=0.49VDD+0.26, at most1.9015V with3.35V main DC rail (ST DS12288Rev6 Table54pp128–129). This is a static limit comparison, not a measured waveform margin. FTDI-to-LV125 still has the previously recorded55mV high-level DC headroom before ripple/ground error; use short paths and validate12Mbaud at bring-up.

[Footprint checks](footprint_checks.md) record manufacturer-drawing checks and the two new portable connector footprints. All source symbols are embedded. The standard STM32 exact variant is flattened from its KiCad library inheritance without changing its pins. The existing Board1 FT232HL symbol retains corrected VCCD/EECLK/EECS electrical types. PWR_FLAGs are annotations, not physical circuitry.

## Checks and remaining stages

Run `python3 scripts/check_board1_complete.py` from the repository root. It exports native KiCad XML and checks239 objects/872 pins, explicit NCs, fields, exact numbered-pad coverage, all BOM quantities and independent topology rules for MCU ownership, SWD, header branches, ring, UART_MD, CAN polarity/termination/protection, RS-485, separate SAM core rails and preserved power/USB circuitry. These checks pass. All11 PDF pages were rendered and visually reviewed. Capture scripts are one-time provenance, not the editing authority; do not rerun over subsequent manual CAD edits.

ERC has not run: KiCad7 CLI exposes schematic export but no ERC command. Run Eeschema ERC before schematic approval; no ERC/DRC or hardware validation is claimed. Exact assembly/mating and layout placement remain layout checks. The stale ADR-040 research link now points to its verified historical Git revision; the accepted decision text is unchanged. The repository document audit and its seven regression tests pass.

Manual bench operating limits: external timing/debug sources must be3.3V, and drive only while3V3_SYS is on; connect after configuration and disconnect before power-off/suspend. Series resistors do not provide power-off isolation. Disable/disconnect the RS-485 peer before local power-off/suspend because the accepted330ohm bias can feed main power. SWD VTref is sense only. First programming uses connect-under-reset with external bus peers disconnected, then firmware establishes PHY defaults. These limits avoid adding automatic isolation to this prototype.

Bring-up: program/read back FTDI EEPROM per [USB VCP](../usb_vcp.md); check current/startup/suspend, MCU reset/boot, crystal start/frequency,12Mbaud VCP and chosen CAN/UART rates. SAM EIC uses synchronous active-run mode; clear flags after enable and heed DS80000740T errata for the fitted revision. Measurements are not draft-capture blockers.

Primary references: [STM32 DS12288](https://www.st.com/resource/en/datasheet/stm32g474rb.pdf), [SAM DS60001479J](https://ww1.microchip.com/downloads/aemDocuments/documents/MCU32/ProductDocuments/DataSheets/SAM-C20-C21-Family-Data-Sheet-DS60001479J.pdf), [TCAN3413](https://www.ti.com/lit/ds/symlink/tcan3413.pdf), [ST3485](https://www.st.com/resource/en/datasheet/st3485eb.pdf), [LV125](https://www.ti.com/lit/ds/symlink/sn74lv125a.pdf), [FT232H v2.2](https://www.ftdichip.cn/Support/Documents/DataSheets/ICs/DS_FT232H.pdf). FTDI current errata/on-hand silicon reconciliation remains an approval check; no retrieved source attachments were edited.
