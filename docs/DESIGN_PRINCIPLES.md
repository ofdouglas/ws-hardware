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

## Review gates

- Scope: explicit acceptance of the MVP requirements and resolution of scope blockers.
- Schematic: exact package pin/mux review; power/startup/current budget; clocks/reset/debug; PHY behavior and termination; connector pin numbering; reviewed symbols/footprints; ERC findings resolved or documented.
- Layout: placement/routing review for selected bus rates and geometry; clear test/debug access and silkscreen; DRC findings resolved or documented; schematic/pinmap/BOM agreement.
- Release: approved assembly variant, complete BOM, fabrication/assembly outputs tied to a revision, and a bring-up checklist. Record actual measurements after assembly separately from design expectations.

These are future gates, not checks already passed by this scaffold.
