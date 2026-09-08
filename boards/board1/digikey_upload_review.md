# DigiKey upload review — 2026-09-07

The upload file is `bom_digikey.csv`; `bom_internal.csv` retains stable BOM IDs, designators, selections and evidence. The maintainer renamed the internal file; tooling and local links now follow that name.

## Earlier upload review (historical)

- 45 unique MPN purchase lines and 219 purchased units reconcile to all 83 internal rows using the purchase/placement rules. No count was changed by this review.
- Customer references now identify assembly locations, naturally sorted and losslessly compressed into ranges (for example `U8-U10`). The longest field is 86 characters. Internal stable IDs remain in the internal BOM.
- The earlier export used one 40-position strip for J2/J4/J6/J8 and labeled it `cut 4x8`. This has been superseded in the internal BOM by purchased Adam Tech PH1-08-UA headers; the old export/rules still require reconciliation.
- Two loose shunts are labeled `Shunts for J10-J11`; they have no independent CAD designators. Twelve PCB test pads require no purchased parts. B1-B084 adds seven communications headers; PRPC002SAAN-RC purchase quantity includes these, six ground headers and two termination headers.
- All 28 supplied DigiKey codes agree with the internal sourcing records. The TPS560430, two TDK buck capacitors and Bourns inductor codes were additionally matched against retrieved DigiKey catalog results. This is not a new live catalog/stock verification of every row.
- Seventeen lines have an MPN but no DigiKey code. Match those exact MPNs on upload and review the selected manufacturer/package and cut-tape/tray quantity. Blank DigiKey fields are intentional; no distributor codes were invented.
- No spare/rework allowance is included. Quantities are the minimum modeled one-board purchase quantities.

## Gateway correction and remaining stages

[ADR-043](../../docs/decisions/043-gateway-part-correction.md) records the explicit maintainer correction to STM32G473RBT6. U7, its manifest, internal BOM and purchase CSV agree. The exact G473 native symbol has the same 64 base pin names/types/positions as the previous G474 symbol; connections were preserved. G473-specific electrical/AF/errata review remains under B1-Q005/008 before schematic approval; older G474 evidence and workbook/PDF snapshots are not G473 qualification.

The earlier complete native/document checks passed before the purchased-substitution and ADR-046 updates. Current checks are recorded in the CAD notes; the document and purchase audits currently fail on the pre-existing B027/B059 substitution mismatch described below. These checks do not claim ERC, DRC, completed footprint qualification, live stock, or hardware validation.

## FTDI date marking and purchasing

[FTDI's FT232H datasheet](https://ftdichip.cn/Support/Documents/DataSheets/ICs/DS_FT232H.pdf), package marking notes, defines a two-digit year followed by a two-digit week, followed by revision. `2028` in that date-code position means 2020, week 28. It is not a future year and does not establish authenticity.

The [eBay listing](https://www.ebay.com/itm/178422245530) returned an error, so its photo, exact suffix/revision and seller claims were not independently inspected. No authenticity claim is made. No purchase or supplier-policy change was made. U4 remains on the DigiKey upload file until the maintainer actually elects to source it elsewhere; remove that purchase line when sourcing elsewhere to avoid double buying.

## Repeatable checks

Run from the repository root:

```sh
python3 scripts/board1_digikey.py --write
python3 scripts/board1_digikey.py
python3 scripts/check_board1_complete.py
python3 scripts/board1_documents.py
python3 -m unittest discover -s scripts -p 'test_*.py'
```

The upload checker audits MPN quantities before writing references. It never replaces MPNs, distributor codes or purchase quantities. Run the native checker alongside it: the reference mapping uses the CAD manifest, which must agree with a fresh exported netlist.

ADR-044 update: the eight 33 pF capacitors now use YAGEO CC0805FRNPO9BN330 / DigiKey 311-4175-1-ND. Purchase quantities are unchanged; BOM and native schematic checks pass after substitution.

ADR-045 update: C12/C13 use YAGEO CC0805FRNPO9BN270 / 311-4173-1-ND, quantity two. The 10 uF buck input selection remains unchanged.

## ADR-046 communications-header update

Seven PRPC002SAAN-RC headers J19–J25 are added to B1-B084 and the existing purchase row (now fifteen total: seven measurement, six ground and two termination headers). B1-B011 retains twelve copper pads, with no purchased parts. Customer references include J19–J25.

The document and purchase audits currently expose earlier purchased-substitution records that have not yet been reconciled: B027 is marked superseded but retains quantity one, while B059 selects PH1-08-UA and the cut-strip rules/export still describe PRPC040SAAN-RC. These are release/procurement-record checks; they do not block placing the requested communications headers. This update preserves those unrelated source records instead of silently undoing the purchased selections.
