# ESD2CAN24DBZRQ1 KiCad symbol

Library ID: `ESD2CAN24DBZRQ1:ESD2CAN24DBZRQ1`. Project-authored symbol for B1-B072 / ADR-037.

[Datasheet](https://www.ti.com/lit/ds/symlink/esd2can24-q1.pdf): SLVSFW5D Rev.D, March 2026: p.3 DBZ diagram and Table 4-1; p.10 functional block; orderable addendum lists ESD2CAN24DBZRQ1 in DBZ.

| Pin | Name | KiCad electrical type |
|---|---|---|
| 1 | IO1 | passive |
| 2 | IO2 | passive |
| 3 | GND | passive |

IO1 and IO2 are separate bidirectional protection nodes, both referenced to ground pin 3. All pins are passive. The DBZ SOT-23 pinout is used, not a pin-swapped generic dual-diode symbol. CANH/CANL net assignments remain schematic decisions under ADR-037.

Assigned standard footprint: `Package_TO_SOT_SMD:SOT-23`. Numbered pad set checked; full land-pattern, assembly, electrical limits, errata and circuit qualification remain open under the existing Board 1 questions. BOM evidence remains unverified. No allocation or part-selection status is changed.

See [validation and BOM coverage](../remaining_ic_symbol_checks.md) and preview/ for KiCad-rendered views. No board ERC/DRC or hardware testing is claimed.
