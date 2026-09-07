# ESDS452DBZR KiCad symbol

Library ID: `ESDS452DBZR:ESDS452DBZR`. Project-authored symbol for B1-B073 / ADR-038.

[Datasheet](https://www.ti.com/lit/gpn/esds452): TI SLVSHM5, March 2024: p.2 DBZ diagram and Table 4-1; p.3 working range; orderable addendum lists ESDS452DBZR.

| Pin | Name | KiCad electrical type |
|---|---|---|
| 1 | IO1 | passive |
| 2 | IO2 | passive |
| 3 | GND | passive |

IO1 and IO2 are independent passive TVS nodes referenced to GND pin 3. The accepted RS-485 use is restricted to the +/-5.5 V bus-to-local-ground operating envelope under ADR-038; this symbol does not establish transient coordination or immunity.

Assigned standard footprint: `Package_TO_SOT_SMD:SOT-23`. Numbered pad set checked; full land-pattern, assembly, electrical limits, errata and circuit qualification remain open under the existing Board 1 questions. BOM evidence remains unverified. No allocation or part-selection status is changed.

See [validation and BOM coverage](../remaining_ic_symbol_checks.md) and preview/ for KiCad-rendered views. No board ERC/DRC or hardware testing is claimed.
