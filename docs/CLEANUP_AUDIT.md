# Documentation cleanup audit

2026-09-07 · Scope: cleanup steps 5–6; no electrical sign-off.

- Preserved all 75 CSV BOM rows byte-for-byte, including MPNs, quantities, acceptance and unverified evidence. Generated view covers every row once and explicitly excludes superseded purchases.
- Added repeatable generation and drift detection. ADR-039 strip cuts total 32/40 positions: one purchased strip, four GPIO and four included debug pieces. PCB pad purchases are zero; actual pad count and fitted scope-ground pin count stay TBD.
- Current Rev A numerical operating points, load assumptions and approximately 70.71% break-even are preserved and checked against the DC path equation. Expanded scenarios retain original no-path-loss arithmetic separately. Obsolete converter targets are removed, recoverable from Git.
- Reproduced all 81 exploratory cable/RC cases and their retained JSON snapshot exactly. That model excludes the protection/switch/load circuit and cannot qualify the FTDI rail.
- Checked repository Markdown local file targets, ADR identifier references and the explicitly retained duplicate ADR-026 filenames. Reviewed the partial-supersession map for ADR-010/013/019/021 and its reciprocal records; completion references remain distinct from supersession.
- Checked local symbol file references and existing selected footprint resources. This is resource availability, not pin/geometry/ERC/DRC verification. B1-B004 FTDI footprint and other TBD allocations remain unresolved.
- Corrected stale TPS62902/SC189 references in the pinmap resource overview and the obsolete 90% target in family architecture. Remaining SC189/30 uF/TLV803 mentions are explicit history, exclusions or supersession boundaries. Family RS_485_MULTIDROP remains retained and Board 1-deferred.
- Requirement and question statuses and ADR IDs/statuses are preserved; current resolution prose reflects existing accepted GPIO/header choices. No fresh parts, rate approval or source-CAD changes.

Run `python3 scripts/board1_documents.py` and `python3 boards/board1/vbus_hotplug_model.py --check` from the repository root. See [model maintenance](../boards/board1/models.md) for inputs and generation commands.

Limits: external links/stock, every Markdown fragment, workbook internals, physical footprints, circuit behavior and hardware immunity were not requalified. Library research history is retained as explicitly labeled implementation evidence. Existing B1-Q002–006 and B1-Q008–014 remain open. The power model still needs real load, bias, startup/suspend and efficiency qualification; reproducing its arithmetic does not close those questions.

## Review follow-up — 2026-09-07

Corrected the GPIO follow-up allocation to B1-B027 and the unallocated resistor proposal (B1-Q010), and restored immutable TPS62902 research links for historical B1-B032–035. The pinmap converter overview was already corrected by PR #5. Quantity overrides now validate CSV purchase/placement meaning and header cut counts under ADR-039. Power results explicitly identify scenarios and validate their load/bridge inputs, including the conservative break-even allowance under ADR-021. Added seven regression tests covering rejected inconsistencies and valid data updates. No selected parts, counts, numerical power results, ADR authority or hardware qualification changed.
