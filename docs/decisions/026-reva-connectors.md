---
id: ADR-026
title: Rev A debug, bus and GPIO connector MPNs
status: accepted
scope: Board 1 Rev A connectors
created: 2026-09-06
accepted_on: 2026-09-06
accepted_by: Explicit maintainer instruction USR-25
supersedes: none
superseded_by: none
requirements: [B1-R007, B1-R017, B1-R020]
questions: [B1-Q004, B1-Q005, B1-Q010]
sources: [USR-25]
---

# ADR-026: Rev A connector selections

## Decision

Record the three exact connector MPNs explicitly selected by the maintainer in USR-25 as accepted. The authoritative MPNs, distributor codes and quantities are in [BOM B1-B009/022/027](../../boards/board1/bom.csv): independent Cortex SWD/reset headers, the external bus terminal block and the GPIO breakaway source strip respectively. This implements ADR-007/011 without replacing their architecture or adding deferred interfaces.

## Context and alternatives

The preceding connector review compared a through-hole CNC Tech debug header with an SMT Samtec alternative. The maintainer selected the CNC Tech part together with the proposed Phoenix Contact bus terminal and Sullins GPIO strip. The SMT debug alternative is not selected.

## Consequences and evidence

Retain the four independent debug headers and one eight-position fixed terminal block. GPIO strip quantity stays TBD pending the cut schedule and consumption calculation under B1-Q010; source strips and fitted cut pieces are not interchangeable quantity units. The proposed four 1x5 GPIO headers and terminal signal order are not independently accepted by the MPN instruction.

Manufacturer drawing/product and DigiKey URLs are recorded in the BOM. Selection is accepted, while evidence remains unverified. B1-Q004/005 retain exact footprint and pin-number review, debug position-7 key/cable compatibility, probe adapter/support and USB-only target-power behavior. B1-Q004/010 retain bus/GPIO numbering, mechanical and electrical/load checks. No CAD connectivity, ERC/DRC or hardware tests were performed for this selection.

## Revisit trigger

An exact connector proves mechanically or electrically incompatible, or the maintainer changes requirements. Record evidence and a superseding decision for any replacement; routine review does not reopen these selections.
