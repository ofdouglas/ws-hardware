# Remaining BOM IC symbol checks

Completed 2026-09-06 with KiCad CLI 7.0.11 after pulling merged PR #1 (main 81559ee), on `codex/remaining-bom-ic-symbols`. Includes the concurrently accepted B1-B072 / ADR-037 CAN and B1-B073 / ADR-038 RS-485 TVS arrays; preserves the independent protection-design edits.

## Coverage

All 13 distinct selected ICs and multi-line ESD/TVS arrays have symbol assignments (14 BOM rows because SN74LV125APWR is used twice). Discrete diodes, passives, connectors, and proposed/unselected parts are outside this IC audit.

| BOM ID | MPN | Symbol | Source |
|---|---|---|---|
| B1-B001 | STM32G474RBT6 | `MCU_ST_STM32G4:STM32G474RBTx` | Default KiCad 7 library |
| B1-B002 | ATSAMC21G17A-AUT | `ATSAMC21G17A-AUT:ATSAMC21G17A-AUT` | [Local pin evidence](ATSAMC21G17A-AUT/README.md) |
| B1-B003 | TCAN3413DR | `TCAN3413DR:TCAN3413DR` | [Local pin evidence](TCAN3413DR/README.md) |
| B1-B004 | FT232HL-REEL | `Interface_USB:FT232H` | Default KiCad 7 library |
| B1-B012 | TPS560430X3FDBVR | `TPS560430X3FDBVR:TPS560430X3FDBVR` | [Local pin evidence](TPS560430X3FDBVR/README.md) |
| B1-B013 | AT93C56B-SSHM-B | `AT93C56B-SSHM-B:AT93C56B-SSHM-B` | [Local pin evidence](AT93C56B-SSHM-B/README.md) |
| B1-B015 | MC74HC1G14DBVT1G | `MC74HC1G14DBVT1G:MC74HC1G14DBVT1G` | [Local pin evidence](MC74HC1G14DBVT1G/README.md) |
| B1-B016 | SN74LV125APWR | `SN74LV125APWR:SN74LV125APWR` | [Local pin evidence](SN74LV125APWR/README.md) |
| B1-B018 | RCLAMP0504S.TCT | `RCLAMP0504S.TCT:RCLAMP0504S.TCT` | [Local pin evidence](RCLAMP0504S.TCT/README.md) |
| B1-B021 | ST3485EBDR | `ST3485EBDR:ST3485EBDR` | [Local pin evidence](ST3485EBDR/README.md) |
| B1-B044 | TPS22810DBVT | `TPS22810DBVT:TPS22810DBVT` | [Local pin evidence](TPS22810DBVT/README.md) |
| B1-B066 | SN74LV125APWR | `SN74LV125APWR:SN74LV125APWR` | [Local pin evidence](SN74LV125APWR/README.md) |
| B1-B072 | ESD2CAN24DBZRQ1 | `ESD2CAN24DBZRQ1:ESD2CAN24DBZRQ1` | [Local pin evidence](ESD2CAN24DBZRQ1/README.md) |
| B1-B073 | ESDS452DBZR | `ESDS452DBZR:ESDS452DBZR` | [Local pin evidence](ESDS452DBZR/README.md) |

## Checks performed

- KiCad parsed and exported all six new libraries without errors, including all five SN74LV125APWR units (ten SVG views total). PNG previews were rendered and visually inspected; the inverter annotation was moved to eliminate a power-label overlap.
- Independently transcribed manufacturer pin tables were compared against symbol pin numbers, names and electrical types. All 39 pins passed. No hidden or stacked pins; each connection sits on the 1.27 mm grid. Active-low enables use overbars and inversion bubbles.
- Every new symbol's numbered pins match the complete pad set of its assigned installed default footprint. This is a numbering check, not complete land-pattern qualification.
- Pinout CSVs match the symbols. Exact MPN/value metadata and all seven affected BOM rows match their library IDs and footprint assignments. Evidence status remains unverified.
- All 12 project-local library-table entries resolve through portable paths, including historical SC189. The two default symbols resolve in installed KiCad libraries; STM32 inheritance resolves to 64 numbered pins, FT232H to 48.

The standard STM32G474RBTx symbol covers the selected STM32G474RBT6 package variant; its default LQFP-64 footprint is copied to the BOM as an unqualified assignment. Default FT232H covers the selected FT232HL-REEL; [FTDI's product page](https://ftdichip.com/products/ft232hl/) identifies the LQFP-48 reel order code. The default symbol has no assigned footprint, so B1-B004 footprint remains TBD pending exact package review. Enable the standard MCU_ST_STM32G4 and Interface_USB global libraries in KiCad; local copies are unnecessary.

Each new library README records the exact manufacturer document revision and pin/package pages used. RCLAMP0504S pin 5 remains a passive VREF node, even if the eventual circuit leaves it externally unconnected. SN74LV125APWR has units A-D for channels and E for visible power pins.

## Remaining qualification

No current Board 1 schematic or PCB is present, so no board ERC/DRC or implemented-connectivity validation was performed. Exact land patterns, electrical limits, pin mux, errata, power sequencing and protection performance remain under existing B1-Q002/003/004/005/009. Symbol availability does not close these questions or qualify a board for fabrication.
