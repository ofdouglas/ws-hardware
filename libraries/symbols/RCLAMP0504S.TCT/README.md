# RCLAMP0504S.TCT KiCad symbol

Library ID: `RCLAMP0504S.TCT:RCLAMP0504S.TCT`. Project-authored symbol for B1-B018 / ADR-015.

[Datasheet](https://www.mouser.com/datasheet/2/761/rclamp0504s-1276604.pdf): Semtech RClamp0504S Revision 01/17/2008, manufacturer document mirrored by Mouser: p.1 diagram; p.5 connection options; p.7 package; p.8 RClamp0504S.TCT ordering.

| Pin | Name | KiCad electrical type |
|---|---|---|
| 1 | IO1 | passive |
| 2 | GND | passive |
| 3 | IO2 | passive |
| 4 | IO3 | passive |
| 5 | VREF | passive |
| 6 | IO4 | passive |

IO1-IO4 label the four independent data-line nodes (pins 1/3/4/6). VREF is the positive reference node at pin 5, NOT a no-connect pin. The manufacturer permits connecting it to a rail or leaving it externally unconnected to use the internal TVS reference. All pins are passive diode-network nodes. The Board 1 pin-5-unconnected proposal does not change the symbol pin type.

Assigned standard footprint: `Package_TO_SOT_SMD:SOT-23-6`. Numbered pad set checked; full land-pattern, assembly, electrical limits, errata and circuit qualification remain open under the existing Board 1 questions. BOM evidence remains unverified. No allocation or part-selection status is changed.

See [validation and BOM coverage](../remaining_ic_symbol_checks.md) and preview/ for KiCad-rendered views. No board ERC/DRC or hardware testing is claimed.
