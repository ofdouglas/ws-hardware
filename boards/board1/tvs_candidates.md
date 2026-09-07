# CAN and RS-485 TVS recommendations

2026-09-06. Proposed only; B1-B007/023, B1-Q004/009. Scope assumption: connector ESD/transient suppression for the existing lab board. No industrial surge level, sustained external-voltage fault rating, new power input or transceiver substitution is accepted. All evidence remains unverified pending circuit/layout qualification.

| Interface | Qty | Recommendation / candidate | DigiKey cut-tape code | Stock shown |
|---|---:|---|---|---:|
| Two external CAN pairs | 2 | [TI ESD2CAN24DBZRQ1](https://www.digikey.com/en/products/detail/texas-instruments/ESD2CAN24DBZRQ1/16982061) — recommended | 296-ESD2CAN24DBZRQ1CT-ND | 255,314 |
| External RS-485 pair | 1 | [Bourns CDSOT23-SM712](https://www.digikey.com/en/products/detail/bourns-inc/CDSOT23-SM712/1630592) — conditional candidate, not a qualified standalone surge solution for ST3485EBDR | CDSOT23-SM712CT-ND | 458,323 |

Both are active, leaded SOT-23-3 arrays covering two bus lines per package. Stock is retrieved page evidence, not reserved inventory. CAN part qty-one price shown USD 0.87; refresh all pricing and availability before purchase. Keep the research in residual protection allocations; do not count these arrays twice or mark them accepted.

## CAN

ESD2CAN24DBZRQ1 is a good candidate for one array per connector CAN pair. Its 3 pF typical channel capacitance suits CAN-FD with little added loading. Standoff is +/-24 V; the datasheet gives typical 37 V clamping at 5.7 A, 8/20 us. The TCAN3413 bus absolute limits are +/-58 V. This supports selection screening, not a guaranteed transient margin: check maximum clamping, pulse shape, layout overshoot and differential stress. Opposite-polarity simultaneous clamps could exceed the transceiver's 58 V differential limit even when each pin is below its individual absolute limit.

[TI SLVSFW5D, March 2026, pp.3,6,10–12](https://www.ti.com/lit/ds/symlink/esd2can24-q1.pdf) gives pins, characteristics and use guidance. DBZ pins1/2 are protected IOs and pin3 is ground. [TCAN3413 datasheet, RevA, p.4](https://www.ti.com/lit/ds/symlink/tcan3413.pdf) supplies bus absolute limits. A 24 V TVS rating is compatible with this USB-powered board; it does not imply adding 24 V power. It does mean the protected port must not inherit the bare PHY's +/-58 V sustained-fault claim.

## RS-485: compatibility boundary

Bourns CDSOT23-SM712 preserves the conventional -7 V to +12 V operating range. Pins1/2 connect to A/B and pin3 to ground. It adds 75 pF typical per line. At 1 A its specified clamps are +19/-11 V; at 17 A, +26/-14 V. These are pulse-specific limits, not operating voltage ratings. Source: [Bourns datasheet pp.1–2](https://www.bourns.com/pdfs/CDSOT23-SM712.pdf); retrieved version has no revision identifier captured, so revision qualification remains open.

ST3485EBDR A/B absolute limits are +/-14 V: [ST DS2947 Rev12 p.4](https://www.st.com/resource/en/datasheet/st3485eb.pdf). Consequently, the positive clamp cannot establish protection of this PHY against the rated surge. ST's built-in IEC ESD capability may allow useful protection coordination, but it does not prove tolerance of a longer surge above absolute maximum. Do not select the CAN 24 V TVS for this port either.

Recommendation: shortlist CDSOT23-SM712 as the connector-side TVS if developing and testing a coordinated protection network; do not freeze it as the sole surge protector. A lower-voltage clamp would restrict allowable RS-485 common mode, while a stronger PHY would change an accepted choice. Neither is silently introduced here. Additional series/current-limiting protection requires calculation of clamp coordination, signal loss, bias and fault energy before proposing exact parts. A resistor alone cannot guarantee that an otherwise high-impedance protected input stays below 14 V.

The 75 pF typical line capacitance requires edge/settling review at the Board 1 12 Mbit/s ceiling; a slower actual Digi link does not qualify the faster case. Leakage must be included in accepted 330 ohm bias margins. Datasheet leakage maxima at the standoff voltages are not a complete hot-temperature bound at the actual idle common mode.

## Placement and remaining qualification

Place each array beside its terminal-block pair, with short direct routing from connector through the protection node toward the bus, and a short low-inductance return to the connector ground region. Avoid long TVS stubs and routing discharge current through MCU ground necks. Protection stays connected regardless of the CAN termination jumper position. One array per external pair is proposed, not one per onboard PHY. Verify the exact footprint and pin1 orientation; a matching SOT-23 name alone is insufficient.

B1-Q004/009 retain the required ESD/EFT/surge environment, exact clamp coordination, layout, cable grounding and bench testing. No schematic implementation, ERC/DRC, transient simulation or hardware immunity test was performed. The RS-485 protection recommendation is deliberately conditional on those checks; ST3485EBDR remains the accepted PHY.
