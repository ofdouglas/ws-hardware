# Design principles and document conventions

Status: draft policy · Authority: repository workflow · Updated: 2026-09-06

Prefer a small board that brings up reliably, exposes the intended networking experiments, and can be inspected and reworked. Add complexity when a concrete experiment needs it. Provide debug, reset, rail measurements, and observable links before sophisticated instrumentation. Keep power-up and unpowered-interface behavior explicit.

## Authority

1. Explicit current maintainer instructions, with provenance recorded.
2. Accepted ADRs within their stated scope.
3. Accepted board requirement rows for implementation scope; family conventions apply only where that scope includes them.
4. Proposed requirements, architecture drafts, source notes, and diagrams are planning inputs.

If instructions and recorded decisions conflict, record the conflict and reconcile the affected records before implementation. An accepted ADR does not silently accept every row linked to it. Schematics encode implemented connectivity; verified pinmaps document reviewed allocation; the BOM records intended assembly. Disagreement among these is a defect to resolve, not a new decision.

## Status vocabulary

| Object | Allowed status | Meaning |
|---|---|---|
| Document | draft, reviewed | Editorial maturity; never bulk acceptance of its contents |
| Requirement / ADR | proposed, accepted, deferred, rejected, superseded | Candidate; explicit decision; outside current scope; declined; replaced with link |
| Pin/BOM evidence | unverified, verified | Primary-source checks absent or completed with evidence |
| Open question | open, resolved | Unanswered, or answered with decision/evidence link |

`TBD` means unknown; `NA` means inapplicable. Avoid blank cells except where a file schema explicitly permits them. Future means scope, not a promise to populate or reserve pins. DNP means a real designed footprint omitted from an assembly variant; it is not interchangeable with deferred.

Keep stable IDs: `B1-Nxx` nodes, `B1-Lxx` links, `B1-Rxxx` requirements, `B1-Qxxx` questions, `B1-Pxxx` pin rows, `B1-Bxxx` BOM rows, `ADR-NNN` decisions. IDs are never reused. Board requirements own question status; other documents reference question IDs rather than duplicate answers.

## Decision discipline

Check `docs/decisions/README.md` before proposing a choice. Accepted decisions stay settled until new evidence or an explicit changed requirement justifies a replacement ADR. New ADRs include alternatives, consequences, evidence, and precise acceptance criteria. Record accepted date and who/what instruction accepted it. Do not rewrite accepted history to resemble a fresh decision.

Proposals may guide reversible planning but do not authorize fabrication. Routine edits within accepted scope need no fresh decision. Keep one change focused; include requirement/ADR IDs and update derived files in the same change.

## Proportionate design and stopping rules

Rev A is a manually operated bench prototype. Use conventional manufacturer application circuits and the accepted operating scope. Distinguish behavior needed during normal operation from later bring-up observations and hypothetical faults. Do not silently strengthen requirements into guaranteed operation across arbitrary brownouts, corrupt configuration, abnormal external drive or every supply-collapse order. Actual absolute-maximum violations, incompatible logic levels and output contention in intended use remain material concerns.

A missing guarantee is uncertainty, not automatically a failure. Identify a plausible mechanism and material consequence before expanding research or proposing mitigation. Use existing engineering allowances for negligible contributions; refine a calculation when it can change a component, connection or budget decision. Do not repeatedly recheck settled evidence without a relevant change.

Routine reversible implementation choices can be made within accepted scope and documented in the circuit/BOM notes. Reserve ADRs for meaningful scope, architecture or durable policy decisions, and for changes to accepted ADRs. Maintainer acceptance and engineering evidence are separate; passing a pin check need not wait for bench tests, and an accepted circuit need not be called electrically verified.

Classify remaining work in the existing question's resolution text or working checklist without creating another authority register:

| Disposition | Treatment |
|---|---|
| Implementation detail | Resolve while capturing; record chosen wiring/value and rationale |
| Schematic check | Verify relevant pins, mux, limits and connectivity before schematic approval |
| Bring-up check | Measure on assembled hardware; does not block draft capture |
| Deferred / no change | Outside scope or insufficient reason to alter the conventional circuit |

For a blocker, state trigger, mechanism, consequence, evidence and affected gate. Block only the dependent work. A broad open question may contain a settled decision and pending measurements: record the settled subitem explicitly rather than repeatedly reopening it. No need to close the whole question prematurely.

Stop when the evidence supports an implementation and further research is unlikely to change it. If uncertainty is material, define one bounded next check. Reviews should prioritize concrete errors and can conclude “no change needed.” Extra complexity needs a demonstrated benefit against an accepted requirement.

## Review stages

- Draft capture: draw settled circuitry and resolve routine details; label unresolved connections/proposals. Do not require future measurements or complete layout qualification to start.
- Schematic approval: check exact package pins/mux, supply and logic compatibility, clocks/reset/debug, PHY behavior, connector numbering and symbol mappings; reconcile BOM and resolve or document actual ERC findings. Review relevant current/startup calculations. Mechanical footprint qualification must finish before layout commitment.
- Layout approval: review land patterns, placement/routing for intended rates, test access and silkscreen; reconcile CAD/pinmap/BOM and actual DRC findings.
- Prototype release: review assembly BOM and fabrication outputs tied to a revision, plus a finite bring-up checklist. Unperformed bring-up measurements are expected at this stage and must not be represented as passed.
- Bring-up: measure startup, power, clocks, programming and link performance under intended conditions. Investigate faults revealed by results. Broader production/compliance qualification is a separate scope decision.

These stages define when work is needed, not claims that checks have passed. Active summaries must show current decisions; remove withdrawn recommendations and their derived parts/calculations. Historical accepted ADR text remains with an explicit supersession notice.
