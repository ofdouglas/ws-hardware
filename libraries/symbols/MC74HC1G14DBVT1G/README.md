# MC74HC1G14DBVT1G KiCad symbol

Library ID: `MC74HC1G14DBVT1G:MC74HC1G14DBVT1G`. Project-authored symbol for B1-B015 / ADR-013; ADR-024.

[Datasheet](https://www.onsemi.com/pdf/datasheet/mc74hc1g14-d.pdf): MC74HC1G14/D Rev.20, January 2026: p.1 pin assignment; p.5 exact DBVT1G ordering and SC-74A package.

| Pin | Name | KiCad electrical type |
|---|---|---|
| 1 | NC | no_connect |
| 2 | A | input |
| 3 | GND | power_in |
| 4 | Y | output |
| 5 | VCC | power_in |

Y has an inversion bubble; the body is labeled Schmitt. NC pin 1 is visible and explicitly no_connect.

Assigned standard footprint: `Package_TO_SOT_SMD:SOT-23-5`. Numbered pad set checked; full land-pattern, assembly, electrical limits, errata and circuit qualification remain open under the existing Board 1 questions. BOM evidence remains unverified. No allocation or part-selection status is changed.

See [validation and BOM coverage](../remaining_ic_symbol_checks.md) and preview/ for KiCad-rendered views. No board ERC/DRC or hardware testing is claimed.
