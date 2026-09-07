# Instructions for hardware design agents

Read `README.md`, `docs/DESIGN_PRINCIPLES.md`, the ADR index and applicable accepted ADRs, then the target board requirements before making changes.

## Proportionate engineering

Design for a manually operated bench prototype. Prefer the simplest conventional circuit meeting accepted requirements and intended operating conditions. Use docs/DESIGN_PRINCIPLES.md for review stages and finding disposition.

- Start from manufacturer-recommended application circuits. Missing documentation of every internal behavior is not itself evidence of incompatibility; concrete conflicting limits still require resolution.
- Before declaring a blocker, identify its triggering condition in intended use, failure mechanism, consequence, supporting evidence and the stage/work it blocks. Otherwise record an implementation detail or bring-up check.
- Do not invent stronger requirements for fault tolerance, sequencing, supervision or uninterrupted operation. Propose extra circuitry only for a concrete unmet requirement or supported failure case.
- Make routine reversible implementation choices within accepted scope with a concise rationale; no separate ADR or approval is needed for every pull resistor or wiring detail. Do not label your own new proposal maintainer-accepted.
- Pending measurements do not block draft schematic capture. Stop research when evidence supports a conventional implementation and more investigation is unlikely to change the choice. Bound any follow-up to a specific decision.
- Keep active summaries current. Remove withdrawn recommendations and dependent BOM calculations rather than leaving competing instructions under correction banners. Preserve accepted ADR history with explicit supersession.
- When delegation is requested, assign bounded checks for material errors, not open-ended searches for possible concerns. Require each finding's evidence, consequence, severity and disposition; “no change needed” is a valid result. The coordinating agent must triage findings before promoting them to blockers or adding circuitry.

## Record discipline

- Use Host/HostId terminology, including SrcHostId and DestHostId.
- Treat source attachments and synced project files as read-only references. Never edit material under the parent project's `sources/` directory.
- Board requirements define scope; future family ideas do not authorize new Board 1 circuitry or DNP footprints.
- Do not reopen accepted ADRs routinely. Implement them. If new evidence makes one infeasible, cite the evidence and propose a new numbered ADR with `supersedes`; retain the original and its history. Only explicit maintainer acceptance changes decision authority.
- Never label your own assumption or generated proposal accepted. Explicit existing maintainer instructions can be recorded as accepted, with provenance.
- Check exact orderable part, package, datasheet revision/page, pin mux, electrical limits, errata, and footprint before marking any allocation verified. Do not infer these from a similar family member or from this scaffold.
- Do not invent MPNs, pins, stock, prices, test results, or design approvals. Use `TBD` and an open-question ID.
- Preserve stable IDs. Update affected requirements, ADR index, pinmap, BOM, and board notes together; link changes by ID. Avoid duplicating authoritative values across prose.
- Keep source CAD as the authority for implemented connectivity; compare it against requirements and verified pinmap. Report conflicts instead of silently picking a winner.
- Do not create fake KiCad files or present placeholder BOM rows as procurement-ready. Keep shared libraries project-local with portable KiCad paths when created.
- For each change, report what changed, supporting evidence, checks performed, and material unresolved items with their review stage. Do not claim ERC/DRC or hardware validation unless actually performed.

- Follow accepted package/assembly constraints in docs/PART_SELECTION_POLICY.md and ADR-009: prefer exposed SMT leads; justify QFN/leadless; exclude BGA unless essential functionality has no viable alternative. Available tools are an iron and hot-air station. Favor 0805 passives (easy for the maintainer); 0603 is acceptable but small. Exclude 0402 and smaller from new selections (USR-17). Smaller crystals are acceptable if they have accessible leads.
