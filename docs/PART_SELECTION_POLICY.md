# Part selection policy

Status: draft policy · Authority: selection/review workflow

Prefer readily sourced parts, inspectable/reworkable packages, documented electrical behavior, and a small set of reusable library components. Existing MCU choices are accepted selections (USR-15 / ADR-004), not an invitation to re-optimize the architecture every session. Check ADR-004 before revisiting them.

Collect the following evidence at the relevant review stage in DESIGN_PRINCIPLES.md. Do not make procurement, layout or bench evidence a prerequisite for proposing or capturing a conventional circuit. Reuse existing checked evidence; investigate only limits relevant to the intended use.

For each selected part, record in the BOM or linked evidence:

- Exact manufacturer and orderable MPN, package, quantity, assembly variant, symbol and footprint.
- Primary manufacturer datasheet URL, revision/date and relevant pages; applicable errata.
- Required versus supported electrical limits: supply, I/O levels, timing, temperature, load, startup/reset, and unpowered behavior as relevant.
- Distributor, dated stock/price evidence, currency and quantity break when procurement is evaluated. Stock and prices expire; never infer them from a past architecture draft.
- Reason for selection, requirement/ADR references, evidence status, and any separately reviewed alternatives.

Compare PHYs against the actual bus rates, rails, common-mode/fault needs, control pins, package, termination, and power budget. Compare USB bridge options against target PC support and dependable bring-up. Do not fill missing specifications from memory or a neighboring part.

An alternate requires pin, footprint, electrical and firmware compatibility review; a similar name is insufficient. CAD library review must check pad numbering, exposed pads, orientation, package dimensions and land pattern against the exact part. Use project-local libraries and `${KIPRJMOD}`-relative paths; record upstream source/license for imported assets.

## BOM schema

`bom_internal.csv` is an initial functional planning BOM. `item_id` is stable. `quantity` is total per board for that row; `TBD` is permitted until resolved. `references=TBD` means schematic designators do not exist yet. Split grouped rows when actual parts/designators are assigned.

`assembly`: `fit` (planned populated), `dnp` (designed footprint, omitted), `tbd` (undecided). `selection_status`: `proposed`, `accepted`, `rejected`, `superseded`. `evidence_status`: `unverified`, `verified`. `TBD` marks unknown fields. A planned `fit` row is not evidence of an accepted design. Deferred architecture is omitted from the BOM rather than represented as DNP.

Do not order from this scaffold. Procurement readiness requires accepted selections, exact MPNs/quantities/references, verified packages and footprints, current availability evidence, and reconciliation against the released schematic/assembly variant.

## Assembly and package constraints — accepted USR-09 / ADR-009

- Available assembly/rework tools: soldering iron and hot-air station. Choose parts and layouts that can be assembled, inspected and reworked with these tools.
- Prefer SMT IC packages with exposed leads, such as SOIC, TSSOP/MSOP/VSSOP and appropriately sized SOT packages. An exposed thermal pad is not an exposed lead; evaluate any mandatory underside solder joint separately.
- QFN and other leadless packages can be considered only with a documented justification explaining why the benefit outweighs assembly/rework difficulty and why suitable leaded alternatives are inadequate.
- Exclude BGA unless it is existential to the intended function: no viable alternative can realize an essential requirement. Document that necessity and the required assembly/rework approach; convenience, density or incremental performance is insufficient.
- Accepted USR-17 size guidance: default to 0805 imperial (2012 metric), which the maintainer finds easy; 0603 (1608 metric) is acceptable but small. Use 1206 or larger where electrical requirements or handling warrant it. Exclude 0402 and smaller from new selections. Smaller crystal packages are acceptable if they retain accessible leads; package dimensions alone do not establish solderability.
- Judge the actual footprint, lead pitch and access for rework, not just the package-family name. Keep room around components for iron/hot-air access. Do not silently assume a reflow oven or outsourced BGA assembly is available.

## Sourcing constraint — accepted USR-12

Source all project parts from DigiKey for procurement simplicity. Record exact DigiKey order codes alongside manufacturer MPNs in the BOM or linked procurement evidence. Confirm current availability before purchase; a catalog listing alone does not establish stock. Do not select an alternative supplier without an explicit maintainer change to this constraint. Historical candidate notes are research history, not procurement approval; recheck any candidate against this constraint before selection.

## Decoupling value preference — USR-14

Prefer 100 nF, 1 uF and 4.7 uF for BOM consolidation when electrically appropriate. This is secondary to electrical requirements; retain justified exceptions such as buck input 10 uF and output 22 uF, analog 10 nF and crystal-load capacitors. Equal nominal values do not imply interchangeable dielectrics, ESR, packages or voltage ratings.
