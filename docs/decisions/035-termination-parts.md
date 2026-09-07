---
id: ADR-035
title: Exact termination resistor and jumper parts
status: accepted
scope: Board 1 Rev A
created: 2026-09-06
accepted_on: 2026-09-06
accepted_by: Explicit maintainer instruction USR-29
supersedes: none
superseded_by: none
requirements: [B1-R026]
questions: [B1-Q003, B1-Q004, B1-Q009]
sources: [USR-29]
---

# ADR-035: Termination parts

Accept all three previously recommended MPNs: five TE CRGP0805F120R resistors across B1-B067/068, two Sullins PRPC002SAAN-RC headers B1-B069, and two Sullins SPC02SYAN shunts B1-B070. Counts and topology remain ADR-034. Use the dedicated two-pin headers, without counting additional GPIO strip consumption for these placements.

[Part specifications, manufacturer drawings and dated DigiKey evidence](../../boards/board1/termination_parts.md) remain the supporting record. Selection does not establish thermal, fault, mating or CAD-footprint qualification; evidence remains unverified. No ERC/DRC or hardware validation performed.

The accompanying instruction to investigate idle-bus bias authorizes research, not acceptance of new bias resistor MPNs or a change to termination. See [bias investigation](../../boards/board1/rs485_bias.md), B1-Q009.
