Current decision: ESDS452DBZR and its disclosed restricted bench voltage envelope accepted by USR-32 / [ADR-038](../../docs/decisions/038-rs485-tvs.md). The research below is historical; qualification remains open.

# Better-clamping RS-485 TVS candidate

Research 2026-09-06; B1-Q009/B1-B023. No RS-485 TVS, restricted operating envelope or replacement PHY is accepted. ST3485EBDR, 330 ohm bias and 120 ohm termination remain selected.

Recommend evaluating **TI ESDS452DBZR**, quantity one, for the short ground-connected bench link. [DigiKey](https://www.digikey.com/en/products/detail/texas-instruments/ESDS452DBZR/23065579) code **296-ESDS452DBZRCT-ND**; page shows 2,255 in stock, USD 0.63 qty1 / 0.391 qty10. This is retrieved inventory evidence, not reserved stock; refresh before purchase.

[TI SLVSHM5, March 2024, pp.2–4](https://www.ti.com/lit/gpn/esds452) specifies a leaded SOT-23-3 dual bidirectional array, +/-5.5 V standoff, 3 pF typical / 5 pF maximum channel capacitance and 50 nA maximum leakage at standoff at the electrical-table conditions. At +/-1 A, 8/20 us, clamp magnitude is 7.5 V typical / 10 V maximum; at +/-15 A it is 11.5 V typical / 14 V maximum. The 9.6 V TLP figure is typical at 16 A and is not an 8/20 us guaranteed clamp. Pins1/2 are IO and pin3 is GND; exact footprint verification remains open.

Compared with the [previous Bourns SM712](https://www.bourns.com/pdfs/CDSOT23-SM712.pdf), this substantially lowers both capacitance and positive clamping voltage. At the documented 1 A surge condition, 10 V leaves a useful initial margin below the selected PHY's 14 V bus absolute limit. At 15 A, that static margin disappears. Layout overshoot, temperature and the actual required pulse must be evaluated; the array's own survival rating is not an assembled-port immunity rating.

The tradeoff is operating range. Both bus wires must remain within +/-5.5 V relative to **Board 1 local ground**, including remote-driver output, ground shift and normal ringing. This does not preserve the conventional -7 V to +12 V RS-485 envelope. A ground-connected 3.3 V bench setup may support this restriction, but a ground wire alone is not proof. Check the actual kit output limits and ground offsets; the narrower interface contract requires maintainer acceptance before selection. Do not connect a 12 V common-mode industrial segment and expect the TVS to remain inactive.

Other screens: TI ESDS552 supports +/-12 V but its published 23.8 V clamping figure still fails to solve this PHY's 14 V absolute-limit mismatch ([TI product](https://www.ti.com/product/ESDS552)). Nexperia PESD5V0S2BT-Q also narrows working voltage to 5 V and advertises a 14 V clamp at 12 A ([manufacturer](https://www.nexperia.com/product/PESD5V0S2BT-Q)); it does not remove the operating-range tradeoff. Neither is selected. No verified drop-in full-range, guaranteed-under-14-V surge solution was found in this review.

Use ESDS452DBZR as the preferred **conditional** bench candidate. If full common-mode range and strong surge immunity are required, continue coordinated protection research or propose a more tolerant PHY through a new decision; do not silently substitute it. This review changes no accepted interface scope. No source CAD, transient simulation, ERC/DRC or bench validation performed.
