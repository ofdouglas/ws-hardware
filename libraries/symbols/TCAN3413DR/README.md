# TCAN3413DR KiCad symbol

Library ID: `TCAN3413DR:TCAN3413DR`. New project-authored symbol from the manufacturer pin table. Implements B1-B003 / ADR-002; existing part selection is unchanged.

## Evidence and pin model

[Manufacturer datasheet](https://www.ti.com/lit/ds/symlink/tcan3413.pdf): TI SLLSFS8A, Rev. A, November 2023, p.3 Table 4-1 and D-package diagram; exact TCAN3413DR ordering in PDF p.31.

| Pin | Name | KiCad electrical type |
|---|---|---|
| 1 | TXD | input |
| 2 | GND | power_in |
| 3 | VCC | power_in |
| 4 | RXD | tri_state |
| 5 | VIO | power_in |
| 6 | CANL | bidirectional |
| 7 | CANH | bidirectional |
| 8 | STB | input |

Pin 5 is VIO for TCAN3413, not the TCAN3414 SHDN input. RXD is tri_state to reflect its powered-off high-impedance state; CANH/CANL are bidirectional bus pins. VCC and VIO remain distinct power inputs. No thermal pad belongs to the D package.

## Footprint and qualification

Assigned default footprint: `Package_SO:SOIC-8_3.9x4.9mm_P1.27mm`. All package pins are separate and visible, with no stacked or hidden pins. Standard-footprint pad numbering is checked against the symbol. Exact land-pattern/assembly and circuit electrical qualification, current errata review and board connectivity remain open under B1-Q003/004; BOM evidence remains unverified. No circuitry, mux allocations or acceptance status changed.

## Validation

Validation results are recorded in [the shared check report](../symbol_checks.md). Preview files are in preview/. No board ERC/DRC, hardware measurement or fabrication approval is claimed.
