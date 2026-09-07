# TPS22810DBVT — DBV SOT-23-6 symbol

Library ID: `TPS22810DBVT:TPS22810DBVT`. Exact MPN: Texas Instruments TPS22810DBVT. Implements the selected B1-B044 part under ADR-019/022; B1-R006/012. New project-authored symbol drawn directly from the manufacturer pin table, not a renamed DRV symbol. No new part selection or design approval is asserted.

## Primary evidence

[TI TPS22810 datasheet SLVSDH0C, Rev. C, January 2018](https://www.ti.com/lit/ds/symlink/tps22810.pdf), page 3: DBV six-pin SOT-23 configuration and functions. The retrieved package addendum dated 15 July 2026 (PDF page 26) lists exact TPS22810DBVT, DBV, six pins, small tape-and-reel. Page 1 identifies the DBV 2 A variant; it must not inherit the DRV 3 A description. Page 4 operating/absolute limits remain part of board electrical qualification, not symbol validation.

| Pin | Name | KiCad electrical type |
|---|---|---|
| 1 | VIN | power_in |
| 2 | GND | power_in |
| 3 | EN/UVLO | input |
| 4 | CT | output |
| 5 | QOD | passive |
| 6 | VOUT | power_out |

CT follows the datasheet output designation for the timing-capacitor node. QOD is modeled as passive because it is the discharge path intended for an optional resistor or direct connection to VOUT; this avoids a misleading output-to-output ERC conflict. This is an ERC modeling choice, not an assertion of reverse-current protection. No hidden pins, stacked pins, or exposed-pad pin 7.

## Footprint and use

Assigned default footprint: `Package_TO_SOT_SMD:SOT-23-6` (installed KiCad footprint library). Confirmed pad set 1–6, no exposed pad, and 0.95 mm lead pitch. Final land-pattern dimensions, assembly clearances and thermal/current qualification remain B1-Q002; the allocation remains unverified. Do not substitute `TPS22810DRV`: its VIN/VOUT, GND, EN, CT and QOD numbering differs.

Accepted board connections remain in boards/board1/usb_input.md and ADR-022; this library creation does not implement a circuit.

## Checks performed

Created and exported using KiCad CLI 7.0.11. Checked the parsed symbol against the six-pin table above and the companion CSV, unique pin positions, standard-footprint pad numbers, and portable project library resolution. SVG export succeeded and the PNG preview was visually inspected for labels and pin numbering. No schematic ERC, PCB DRC, hardware test, full errata review or fabrication approval was performed. See preview/tps22810dbvt.svg and preview/tps22810dbvt.png.
