# Selected termination resistor and jumper parts

Research 2026-09-06. Topology/counts/120 ohm nominal values are accepted by USR-28 / [ADR-034](../../docs/decisions/034-rs485-termination.md). The exact parts below are accepted by USR-29 / ADR-035, with evidence unverified pending circuit/footprint qualification. Stock and prices are retrieved page snapshots, not reserved inventory; refresh before purchase.

| Allocation | Qty | Selected MPN | DigiKey order code | Specification | Stock shown | USD qty1 |
|---|---:|---|---|---|---:|---:|
| B1-B067/068 | 5 | [TE CRGP0805F120R](https://www.digikey.com/en/products/detail/te-connectivity-passive-product/CRGP0805F120R/8577068) | A130466CT-ND | 120 ohm, 1%, 0805, 1/3 W, pulse-withstanding thick film | 17,131 | 0.24 |
| B1-B069 | 2 | [Sullins PRPC002SAAN-RC](https://www.digikey.com/en/products/detail/sullins-connector-solutions/PRPC002SAAN-RC/2775252) | 35-PRPC002SAAN-RC-ND | 1x2 male header, 2.54 mm, through-hole, gold flash | 9,647 | 0.10 |
| B1-B070 | 2 | [Sullins SPC02SYAN](https://www.digikey.com/en/products/detail/sullins-connector-solutions/SPC02SYAN/76375) | S9001-ND | 1x2 closed-top shunt, 2.54 mm, gold flash | 762,380 | 0.10 |

The five resistors serve two CAN buses (two each) and one local RS-485 endpoint. Each CAN terminal-end resistor has its own header/shunt in series. The remote cable endpoint resistors are outside the onboard BOM. Header pins never directly short CANH/CANL. Follow the jumper modes in [termination arrangement](termination_proposal.md).

TE's [exact product page, internal number 1-2176327-4](https://www.te.com/en/product-1-2176327-4.html) confirms the 0805, 120 ohm, 1%, 0.33 W selection. This gives more dissipation headroom than a common 0.125 W part: using the minimum 118.8 ohm resistance, 3.6 V differential gives 0.109 W. This is a screening example, not a bound on all external drivers: 5 V differential would give 0.210 W. Check derating, remote-driver voltage, pulse/fault exposure and actual board temperature under B1-Q003/004/009 before qualification. Manufacturer series-datasheet revision/derating verification remains open; a distributor power rating is not a completed thermal review.

Sullins [header drawing 11635 RevB, p.1](https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/386/xRxCzzzSxxN-RC_ST_11635-B.pdf) and [shunt drawing 11134 RevD, 2024-06-26, p.1](https://drawings-pdf.s3.amazonaws.com/11134.pdf) are the mechanical references. Header mating length is 5.84 mm; shunt maximum insertion depth is 5.74 +/-0.20 mm, so allow a small seating gap and check engagement/clearance in the layout and sample fit. Both parts are specified for 3 A per contact; termination current is much lower in normal operation. No source-CAD footprint or physical mating test has been verified.

Historical unselected alternative: cut two 2-position sections from the already selected PRPC040SAAN-RC strip and consolidate strip procurement. Reconcile its GPIO cut schedule and total strip count before doing so; do not buy both dedicated headers and extra strips for the same two placements.

The accepted ST3485EBDR has floating-input fail-safe, not guaranteed terminated-idle fail-safe. B1-B023 retains bias/control/protection design and B1-Q009 remains open. Existing power estimates take no reduction credit and termination load must not be counted twice. No ERC/DRC or bench validation was performed.

The dedicated PRPC002SAAN-RC headers are now selected; do not allocate extra PRPC040SAAN-RC strips for these two placements. Bias investigation: [rs485_bias.md](rs485_bias.md).
