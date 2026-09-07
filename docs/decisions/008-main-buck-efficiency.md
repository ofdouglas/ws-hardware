---
id: ADR-008
title: Main buck converter for 90 percent minimum efficiency
status: superseded
scope: Board 1 main 3.3 V converter
created: 2026-09-06
accepted_on: TBD
accepted_by: TBD
supersedes: none
superseded_by: ADR-010
requirements: [B1-R023]
questions: [B1-Q002, B1-Q011]
sources: [USR-08, TI SLVSFM1A]
---

# ADR-008: Main buck efficiency proposal

## Context
USR-08 requires a design addressing 90% minimum efficiency and permits a different chip. Rev A retains one RS-485 for the dual-gateway lab. SC189 was a candidate, not an accepted MPN.

## Proposed decision
Use TPS62902RPJR with XGL4020-222MEC, 1 MHz automatic PFM/PWM, internal 3.3 V setting, 10 µF input and 2 x 22 µF output ceramic capacitors, and 10 nF soft start. Preserve ADR-001 power partition. Propose ≥92% converter qualification and ≤100 mΩ input-path resistance to retain ≥90% main-branch efficiency; the user's 90% converter target itself is accepted in B1-R023.

## Alternatives and consequences
TPS6216x offers less efficiency margin; SC189 remains available for comparison. The preferred RPJ package needs reflow and reviewed layout. Neither typical curves nor the 2 A output rating prove USB compliance. Later 24 V input requires its own stage; TPS62902 is rated only to 17 V operating input.

## Evidence and acceptance criteria
See [complete circuit proposal](../../boards/board1/buck_converter.md) for primary sources, pin connections, component values, efficiency envelope and validation matrix. Accepting the chip and qualifying performance are separate actions. Exact passives/footprints, input switch, startup and measurements remain open.

## Revisit trigger
Failure of the specified efficiency or electrical checks, manufacturing constraints, or an explicit changed power requirement.

## Assembly review update — USR-09

ADR-009 now requires package justification. This proposed QFN design remains unaccepted and is held while leaded alternatives are evaluated in [the shortlist](../../boards/board1/buck_leaded_shortlist.md). Do not implement it as a settled choice or transfer its efficiency estimate to another chip.

## USR-13 clarification

The maintainer requires efficiency at full networking load on USB; light-load efficiency is not a selection criterion. Earlier discussion of a 90% floor across 100–600 mA is historical and no longer controls selection. See boards/board1/sc189_decoupling.md (repository-relative) for the new candidate allocation. No converter or capacitor MPN is frozen.
