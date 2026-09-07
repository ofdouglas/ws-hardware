# AT93C56B-SSHM-B KiCad symbol

Library ID: `AT93C56B-SSHM-B:AT93C56B-SSHM-B`. New project-authored symbol from the manufacturer pin table. Implements B1-B013 / ADR-018; existing part selection is unchanged.

## Evidence and pin model

[Manufacturer datasheet](https://ww1.microchip.com/downloads/aemDocuments/documents/MPD/ProductDocuments/DataSheets/AT93C56B-AT93C66B-Microwire-Serial-EEPROM-Industrial-Grade-DS20006260.pdf): Microchip DS20006260B, Rev. B, February 2024, pp.3-5 SOIC diagram and Table 2-1/pin descriptions; p.31 exact AT93C56B-SSHM-B order code (SOIC SN, tubes).

| Pin | Name | KiCad electrical type |
|---|---|---|
| 1 | CS | input |
| 2 | SK | input |
| 3 | DI | input |
| 4 | DO | tri_state |
| 5 | GND | power_in |
| 6 | ORG | input |
| 7 | NC | no_connect |
| 8 | VCC | power_in |

CS is active high. DO is tri_state when deselected. ORG stays visible as an input; Board 1 straps it to VCC for x16 under ADR-018. Pin 7 is explicitly no_connect and remains visible. No UDFN exposed pad is added to the SOIC package.

## Footprint and qualification

Assigned default footprint: `Package_SO:SOIC-8_3.9x4.9mm_P1.27mm`. All package pins are separate and visible, with no stacked or hidden pins. Standard-footprint pad numbering is checked against the symbol. Exact land-pattern/assembly and circuit electrical qualification, current errata review and board connectivity remain open under B1-Q002/012; BOM evidence remains unverified. No circuitry, mux allocations or acceptance status changed.

## Validation

Validation results are recorded in [the shared check report](../symbol_checks.md). Preview files are in preview/. No board ERC/DRC, hardware measurement or fabrication approval is claimed.
