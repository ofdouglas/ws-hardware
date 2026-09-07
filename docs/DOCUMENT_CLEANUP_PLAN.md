# Proposed documentation cleanup

Status: steps 1 and 2 implemented at maintainer request; review through ADR-039. Steps 3–6 remain proposed. No archive moves, deletions, renumbering or hardware changes performed; existing uncommitted work preserved.

## Findings from the pre-cleanup review

- ST3485EBDR is already accepted in B1-B021/ADR-034; no duplicate selection ADR needed.
- BOM has 75 unique rows: 64 accepted (62 exact MPN rows and two categories), five proposed residual networks and six zero-quantity superseded rows. Readable BOM covers every CSV row once. Counts are rows, not purchasing quantities; cut headers and PCB pads require special treatment.
- Board README still describes SC189 and a 90% efficiency target as current, then appends contradictory newer decisions. It also says crystals are unselected in older paragraphs.
- BOM.md tables are current, but trailing prose still says bias MPNs are open and B008 is residual support, both superseded by ADR-039. Similar overlays occur in research notes.
- sc189_decoupling.md mixes obsolete converter/Cout limits with still-current MCU decoupling rationale. It cannot be archived whole until that live material is extracted.
- ADR-010 and ADR-013 are partially superseded, but a flat accepted status obscures which clauses survive. Both connector and SAM-core decisions use ADR-026.
- Power JSON contains legacy and current models together; research notes contain old stock snapshots. Neither should silently drive new calculations or procurement.
- Libraries now contain real implementation artifacts and symbol checks. Old statements that no CAD/library work exists must be narrowed: no completed board schematic/layout validation is implied by symbol completion.

## Proposed sequence

1. **Completed — repair current entry points.** Rewrite board README as a short current topology/status/navigation page. Keep BOM.md generated from bom.csv, with one allocation-notes section. Remove superseded prose rather than prepend more overrides. requirements.md remains the sole owner of open-question status; remaining_parts.md becomes its concise selection-focused index. Cross-link existing symbol validation instead of duplicating it.

2. **Completed — consolidate current implementation notes.** Retain buck_tps560430.md, crystal_networks.md, clocking.md, pinmap.md and current bus/protection details. Extract current MCU/core decoupling into decoupling.md from sc189_decoupling.md and the BOM. Consolidate USB/VCP and input sequencing into clearly named current notes (usb_vcp.md and usb_input.md). Merge termination_proposal.md + termination_parts.md into termination.md; retain rs485_bias.md. Add one current interface/protection note covering the accepted ST PHY, CAN/RS485 TVS and UART_MD circuit. Preserve assumptions and open electrical checks.

3. **Archive research after extraction.** Move obsolete converter comparisons (buck_converter.md, buck_leaded_shortlist.md, sc189_evaluation.md, tps62046_evaluation.md, tpsm84203_evaluation.md) to boards/board1/archive/research/. Move historical RS485 candidate/cost/SP3485EET reviews, oscillator candidate/debug-options comparisons and TVS alternatives there after moving live decisions to current notes. Archive vbus_input_history_through_adr021.md directly. Treat transceivers_and_power.md and sc189_decoupling.md as mixed documents: extract live content first. Retain bom_review.md as a dated audit under archive/reviews/; consolidate passive_review.md and bom_closeout.md into current implementation/open-work references. Give each archive a date, historical status and successor link; repair all relative links. Do not move immutable parent sources or working symbol libraries.

4. **Clarify decision authority without rewriting history.** Keep ADR files and stable IDs in place. Add a topic-based current-authority map to the ADR index: power, decoupling, clocks, buses, debug, assembly and sourcing. Record clause-level successors for partly superseded ADR-010/013/019; preserve still-active decisions. Add reciprocal supersedes/superseded_by metadata only where existing decisions provide evidence. Use filename-qualified ADR-026 references consistently; avoid silently renumbering previously referenced decisions. Later engineering changes still require new ADRs; editorial consolidation does not invent new acceptance.

5. **Separate live data from historical scenarios.** Audit consumers of power_budget.json and vbus_hotplug_model.py before moving or renaming data keys. Give current Rev A calculations an explicit active entry; retain future expanded-board scenarios separately from obsolete converter assumptions. Keep machine-readable BOM status accepted/proposed and evidence unverified/verified independent. Make readable BOM generation reproducible and distinguish purchase quantity from placement quantity for B027/B059 and zero-purchase PCB pads. Do not infer unknown bridge counts or close qualification questions in this cleanup.

6. **Check the result.** Validate internal links, unique IDs, BOM/view coverage, accepted MPN preservation, supersession references, symbol/footprint links and quantity exclusions. Search current documents for SC189/90%/30 uF/TLV803 and old candidate parts: retain only clearly labeled historical references. Confirm Board 1 RS_485_MULTIDROP stays deferred while remaining in family architecture. Run existing model checks if paths change. Preserve all source files, accepted design choices and open qualification requirements.

## Scope and completion criteria

Start with entry-point corrections and the authority map, then archive research in a separate reviewable change. Finish data/model restructuring last. No new parts, schematic changes or electrical sign-off are included. Done means a new agent can identify the current design from README, requirements, BOM and topic notes without reading historical proposals; history remains accessible and no accepted choice is reopened.

## Implemented scope

Steps 1–2 add current usb_input.md, usb_vcp.md, decoupling.md, termination.md and interfaces.md; rewrite board entry points/BOM view; reconcile retained bias and buck notes. Historical bodies stay in place with successor banners. Root README maturity wording and the live converter-qualification pointer are corrected. BOM CSV, ADR files/index, power data/models and question statuses are unchanged. Basic link and BOM-view checks accompany these edits; the broader step-6 audit remains proposed.
