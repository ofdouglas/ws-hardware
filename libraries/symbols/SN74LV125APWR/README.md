# SN74LV125APWR KiCad symbol

Library ID: `SN74LV125APWR:SN74LV125APWR`. Project-authored symbol for B1-B016; B1-B066 / ADR-001; ADR-013; ADR-033.

[Datasheet](https://www.ti.com/lit/ds/symlink/sn74lv125a.pdf): SCES124O Rev.O, May 2022: p.3 PW pin configuration and pin functions; PDF p.13 exact APWR ordering.

| Pin | Name | KiCad electrical type |
|---|---|---|
| 1 | ~{1OE} | input |
| 2 | 1A | input |
| 3 | 1Y | tri_state |
| 4 | ~{2OE} | input |
| 5 | 2A | input |
| 6 | 2Y | tri_state |
| 7 | GND | power_in |
| 8 | 3Y | tri_state |
| 9 | 3A | input |
| 10 | ~{3OE} | input |
| 11 | 4Y | tri_state |
| 12 | 4A | input |
| 13 | ~{4OE} | input |
| 14 | VCC | power_in |

Units A-D expose each buffer and its active-low OE separately; unit E exposes VCC and GND. Outputs are tri_state. The symbol retains buffer behavior even when Board 1 uses an OE-driven open-drain arrangement under ADR-033. No power pins are hidden.

Assigned standard footprint: `Package_SO:TSSOP-14_4.4x5mm_P0.65mm`. Numbered pad set checked; full land-pattern, assembly, electrical limits, errata and circuit qualification remain open under the existing Board 1 questions. BOM evidence remains unverified. No allocation or part-selection status is changed.

See [validation and BOM coverage](../remaining_ic_symbol_checks.md) and preview/ for KiCad-rendered views. No board ERC/DRC or hardware testing is claimed.
