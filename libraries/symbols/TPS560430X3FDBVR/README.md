# TPS560430X3FDBVR KiCad symbol

Library ID: `TPS560430X3FDBVR:TPS560430X3FDBVR`. New project-authored symbol from the manufacturer pin table. Implements B1-B012 / ADR-021; existing part selection is unchanged.

## Evidence and pin model

[Manufacturer datasheet](https://www.ti.com/lit/ds/symlink/tps560430.pdf): TI SLVSE22B, Rev. B, June 2018, p.3 device comparison and pin functions; exact TPS560430X3FDBVR ordering in PDF p.26.

| Pin | Name | KiCad electrical type |
|---|---|---|
| 1 | CB | passive |
| 2 | GND | power_in |
| 3 | FB | input |
| 4 | EN | input |
| 5 | VIN | power_in |
| 6 | SW | power_out |

The X3F metadata identifies fixed 3.3 V and 1.1 MHz FPWM. FB remains a visible sense input, not a power output. CB is modeled passive as a floating bootstrap-capacitor node referenced to SW, avoiding an artificial requirement for a separate rail power flag. SW is power_out. No exposed pad.

## Footprint and qualification

Assigned default footprint: `Package_TO_SOT_SMD:SOT-23-6`. All package pins are separate and visible, with no stacked or hidden pins. Standard-footprint pad numbering is checked against the symbol. Exact land-pattern/assembly and circuit electrical qualification, current errata review and board connectivity remain open under B1-Q002/011; BOM evidence remains unverified. No circuitry, mux allocations or acceptance status changed.

## Validation

Validation results are recorded in [the shared check report](../symbol_checks.md). Preview files are in preview/. No board ERC/DRC, hardware measurement or fabrication approval is claimed.
