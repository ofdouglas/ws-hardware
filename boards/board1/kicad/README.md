# Board 1 KiCad project — power and USB

Captured 2026-09-07 with KiCad 7.0.11, native schematic format 20230121, assembly revision A-draft. Open [board1.kicad_pro](board1.kicad_pro) in KiCad. The editable schematics are the authority for implemented connectivity; this is a draft capture, not fabrication approval.

- [Root schematic](board1.kicad_sch): USB-B, shield-to-ground bond, raw-VBUS TVS and damping/bypass, TPS22810 attachment ramp, TPS560430 fixed 3.3 V buck, PWREN# inverter and power LED.
- [USB sheet](usb_bridge.kicad_sch): FT232HL with complete supply filtering/bypass, crystal and reset/reference networks, x16 EEPROM, and all four VCP isolation channels with receiver defaults.
- [Two-page review PDF](review/board1-power-usb.pdf) is exported from those source sheets.

52 fitted physical components. The four GW_VCP_* global nets stop at the MCU interface; directions use the MCU perspective. MCU, CAN, RS-485, SWD and timing/header circuits are outside this capture. No PCB/layout or fabrication files have been created.

## Implementation choices

Existing ADRs through ADR-042 are implemented. Routine draft choices are a direct USB shield-to-ground bond, two 600 ohm-at-100 MHz 0805 ferrites (B1-B078), and six 10 kohm VCP defaults (B1-B079, reuse existing resistor MPN). These are engineering choices within scope, not newly maintainer-accepted MPNs. Optional FTDI post-bead bulk is omitted as shown N.F. in the manufacturer reference circuit; no DNP footprints added.

[CSV](../bom.csv) records exact MPNs, native references and footprint choices. Bridge counts are 11 x 100 nF, 2 x 4.7 uF and no 1 uF; B1-B017 has no residual parts. C24 consumes one existing B1-B036 main-domain bypass allocation, and R4 one existing B1-B026 LED resistor. Uncaptured whole-board quantities remain in the planning BOM.

## Symbol and footprint provenance

All schematic symbols are embedded in the native source. The portable [symbol table](sym-lib-table) includes existing shared project libraries and [board1_symbols.kicad_sym](board1_symbols.kicad_sym). Its FT232HL_BusPowered symbol copies KiCad 7 Interface_USB:FT232H, preserving pin numbers and geometry, with three electrical-type corrections for the selected connection: VCCD pin 39 is power_out; EECLK 44 is output; EECS 45 is bidirectional (I/O, tri-state during reset). FTDI v2.2 supply/pin descriptions and Fig.6.1 support these corrections. PWR_FLAGs identify power sources across passive filters and the USB entry; they are annotations, not components.

Footprints use standard KiCad libraries. Existence and numbered-pad coverage were checked for every part. Exact land-pattern/mechanical approval is still required before layout, particularly J1 and Y1; a generic package match is not a dimensional sign-off. J1 uses the KiCad OST USB-B1HSxx family footprint. Y1 uses the HC49-SD footprint for the selected leaded CSM-7X crystal.

## Checks and remaining stages

Run `python3 scripts/check_board1_power_usb.py` from the repository root. KiCad independently exports the complete hierarchy; the check compares 52 components and all 186 physical pins against [capture_manifest.json](capture_manifest.json), including explicit no-connects, rail separation, polarity, BOM MPN/footprint/count consistency and numbered-pad coverage. The manifest records capture intent; it does not supersede future manual schematic edits. The one-time capture script in scripts/ is provenance and must not be rerun over later CAD edits.

All 56 FTDI/EEPROM workbook pad assignments were also compared with the captured nets using the aliases recorded in pinmap.md; they agree. The two exported PDF pages were rendered and visually reviewed. These checks pass. The separate repository document audit stops at the pre-existing missing ADR-040 research link (`boards/board1/research/enable_startup_reassessment.md`); it does not prevent CAD export or connectivity checking. ERC has **not** been run: this installation's KiCad 7 CLI has no schematic ERC command. Run ERC in Eeschema before schematic approval and review any findings; nothing here claims an ERC pass. No DRC or hardware validation was performed.

B1-Q002/008/011/012 retain schematic approval checks for exact-device limits/errata, oscillator loading and supply/filter corners. Current-document access was incomplete: FTDI's current datasheet index lists a later issue, while v2.2 was available for this capture; TN_130 errata and actual on-hand silicon revision remain to reconcile. This does not hold up the conventional draft. Footprint/mechanical checks belong before layout; input current, EEPROM/readback, startup/suspend/replug, oscillator and 12 Mbaud performance belong to bring-up. [USB VCP](../usb_vcp.md) records the required EEPROM setup.

The FTDI-to-LV125 high-level DC screen is narrow: 2.4 V FTDI VOH minimum versus 0.7 x 3.35 V = 2.345 V LV125 VIH at the buck's specified upper DC output gives 55 mV headroom before ripple/ground error. Retain the accepted buffer, keep paths short, and check signal levels/timing during approval and bring-up; this is not a validated 12 Mbaud margin.

## Evidence

Manufacturer baseline: [FT232H v2.2](https://www.ftdichip.cn/Support/Documents/DataSheets/ICs/DS_FT232H.pdf), especially pin descriptions, Tables 3.4/3.5 and Fig.6.1 p.45; [TPS560430 Rev.B](https://www.ti.com/lit/ds/symlink/tps560430.pdf); [TPS22810](https://www.ti.com/lit/ds/symlink/tps22810.pdf); [SN74LV125A Rev.O](https://www.ti.com/lit/ds/symlink/sn74lv125a.pdf). EEPROM and other exact-part pin evidence remains in the [shared library catalog](../../../libraries/symbols/README.md) and BOM. Source attachments were not edited.
