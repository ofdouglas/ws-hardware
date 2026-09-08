# Proposed documentation cleanup

Status: steps 1–6 implemented through ADR-039. Maintainer instructed deletion instead of archiving for step 3; Git retains history. Data separation, reproducible BOM generation and cleanup audit complete; electrical qualification remains open. No ADR renumbering, hardware changes or qualification sign-off.

## Findings from the pre-cleanup review

- ST3485EBDR is already accepted in B1-B021/ADR-034; no duplicate selection ADR needed.
- BOM has 75 unique rows: 64 accepted (61 exact MPN rows and three category/non-purchased rows), five proposed residual networks and six zero-quantity superseded rows. Readable BOM covers every CSV row once. Counts are rows, not purchasing quantities; cut headers and PCB pads require special treatment.
- Board README still describes SC189 and a 90% efficiency target as current, then appends contradictory newer decisions. It also says crystals are unselected in older paragraphs.
- BOM.md tables are current, but trailing prose still says bias MPNs are open and B008 is residual support, both superseded by ADR-039. Similar overlays occur in research notes.
- decoupling.md mixes obsolete converter/Cout limits with still-current MCU decoupling rationale. It cannot be archived whole until that live material is extracted.
- ADR-010 and ADR-013 are partially superseded, but a flat accepted status obscures which clauses survive. Both connector and SAM-core decisions use ADR-026.
- Power JSON contains legacy and current models together; research notes contain old stock snapshots. Neither should silently drive new calculations or procurement.
- Libraries now contain real implementation artifacts and symbol checks. Old statements that no CAD/library work exists must be narrowed: no completed board schematic/layout validation is implied by symbol completion.

## Proposed sequence

1. **Completed — repair current entry points.** Rewrite board README as a short current topology/status/navigation page. Keep BOM.md generated from bom_internal.csv, with one allocation-notes section. Remove superseded prose rather than prepend more overrides. requirements.md remains the sole owner of open-question status; remaining_parts.md becomes its concise selection-focused index. Cross-link existing symbol validation instead of duplicating it.

2. **Completed — consolidate current implementation notes.** Retain buck_tps560430.md, crystal_networks.md, clocking.md, pinmap.md and current bus/protection details. Extract current MCU/core decoupling into decoupling.md from decoupling.md and the BOM. Consolidate USB/VCP and input sequencing into clearly named current notes (usb_vcp.md and usb_input.md). Merge termination.md + termination.md into termination.md; retain rs485_bias.md. Add one current interface/protection note covering the accepted ST PHY, CAN/RS485 TVS and UART_MD circuit. Preserve assumptions and open electrical checks.

3. **Completed — delete obsolete research after extraction.** At maintainer direction, removed 22 redundant research/review/legacy circuit notes. Current checks and primary evidence are consolidated into the live topic notes. ADR/source citations use immutable Git links to the original research. No archive directory created; source attachments and working symbol libraries retained.

4. **Completed — clarify decision authority without rewriting history.** Keep ADR files and stable IDs in place. Add a topic-based current-authority map to the ADR index: power, decoupling, clocks, buses, debug, assembly and sourcing. Record clause-level successors for partly superseded ADR-010/013/019; preserve still-active decisions. Add reciprocal supersedes/superseded_by metadata only where existing decisions provide evidence. Use filename-qualified ADR-026 references consistently; avoid silently renumbering previously referenced decisions. Later engineering changes still require new ADRs; editorial consolidation does not invent new acceptance.

5. **Completed — separate live data from historical scenarios.** Audit consumers of power_budget.json and vbus_hotplug_model.py before moving or renaming data keys. Give current Rev A calculations an explicit active entry; retain future expanded-board scenarios separately from obsolete converter assumptions. Keep machine-readable BOM status accepted/proposed and evidence unverified/verified independent. Make readable BOM generation reproducible and distinguish purchase quantity from placement quantity for B027/B059 and zero-purchase PCB pads. Do not infer unknown bridge counts or close qualification questions in this cleanup.

6. **Completed — check the result.** Validate internal links, unique IDs, BOM/view coverage, accepted MPN preservation, supersession references, symbol/footprint links and quantity exclusions. Search current documents for SC189/90%/30 uF/TLV803 and old candidate parts: retain only clearly labeled historical references. Confirm Board 1 RS_485_MULTIDROP stays deferred while remaining in family architecture. Run existing model checks if paths change. Preserve all source files, accepted design choices and open qualification requirements.

## Scope and completion criteria

Start with entry-point corrections and the authority map, then delete superseded research after extraction in a separate reviewable change. Finish data/model restructuring last. No new parts, schematic changes or electrical sign-off are included. Done means a new agent can identify the current design from README, requirements, BOM and topic notes without reading historical proposals; history remains accessible and no accepted choice is reopened.

## Implemented scope

Steps 1–2 add current usb_input.md, usb_vcp.md, decoupling.md, termination.md and interfaces.md; rewrite board entry points/BOM view; reconcile retained bias and buck notes. At step 2, historical bodies stayed in place with successor banners; step 3 subsequently removed these redundant notes. Root README maturity wording and the live converter-qualification pointer are corrected. Steps 1–2 did not change BOM CSV, ADR files/index, power data/models or question statuses. Basic link and BOM-view checks accompany these edits; the broader step-6 audit remains proposed.

## Steps 3–4 record

Deleted research is recoverable at Git revision `dbcaba10831ade0516dba825d2c97d3f0017e0f5`. Added a topic authority map and partial-supersession metadata/current-scope notes, preserving historical ADR decision bodies and both filename-qualified ADR-026 identities. Retained current electrical checks and repaired document citations. BOM selections, quantities, evidence status, question status and power model data are unchanged.

## Steps 5–6 record

Current Rev A power data is explicit schema v2; deferred expanded scenarios are separate and obsolete converter goals removed. Numerical assumptions/operating points remain unchanged. BOM CSV is unchanged; the generated view makes purchase/placement exceptions explicit. Standard-library generator/audit and model commands are documented in boards/board1/models.md. The exploratory hotplug snapshot is reproduced independently of current-board qualification. See [audit report](CLEANUP_AUDIT.md) for coverage and remaining limitations.
