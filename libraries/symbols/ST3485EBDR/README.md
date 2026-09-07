# ST3485EBDR KiCad symbol

Library ID: `ST3485EBDR:ST3485EBDR`. Project-authored symbol for B1-B021 / ADR-007; ADR-034.

[Datasheet](https://www.st.com/resource/en/datasheet/st3485eb.pdf): DS2947 Rev.12, March 2021: p.2 pin configuration/functions; p.16 SO8 dimensions; p.18 exact EBDR order code.

| Pin | Name | KiCad electrical type |
|---|---|---|
| 1 | RO | tri_state |
| 2 | ~{RE} | input |
| 3 | DE | input |
| 4 | DI | input |
| 5 | GND | power_in |
| 6 | A | bidirectional |
| 7 | B | bidirectional |
| 8 | VCC | power_in |

RE is active low; DE is active high. A is noninverting and B is inverting. RO is tri_state when disabled. This symbol does not establish terminated-idle fail-safe behavior or validate the accepted external bias network.

Assigned standard footprint: `Package_SO:SOIC-8_3.9x4.9mm_P1.27mm`. Numbered pad set checked; full land-pattern, assembly, electrical limits, errata and circuit qualification remain open under the existing Board 1 questions. BOM evidence remains unverified. No allocation or part-selection status is changed.

See [validation and BOM coverage](../remaining_ic_symbol_checks.md) and preview/ for KiCad-rendered views. No board ERC/DRC or hardware testing is claimed.
