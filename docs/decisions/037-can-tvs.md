---
id: ADR-037
title: CAN TVS array selection
status: accepted
scope: Board 1 Rev A external CAN pairs
created: 2026-09-06
accepted_on: 2026-09-06
accepted_by: Explicit maintainer instruction USR-31
supersedes: none
superseded_by: none
requirements: [B1-R009, B1-R017]
questions: [B1-Q004]
sources: [USR-31]
---

# ADR-037: CAN TVS selection

Accept Texas Instruments ESD2CAN24DBZRQ1, quantity two, as B1-B072: one array for each external CAN pair near the terminal block. Connect DBZ pins1/2 to the bus pair and pin3 to ground. Keep protection independent of termination jumpers. B1-B007 excludes these arrays and remains only a residual protection allocation, without authorizing additional footprints.

[TVS evidence](https://github.com/ofdouglas/ws-hardware/blob/dbcaba10831ade0516dba825d2c97d3f0017e0f5/boards/board1/tvs_candidates.md) links TI SLVSFW5D and the exact DigiKey listing. Selection does not establish transient, differential-stress, footprint or layout qualification. Evidence remains unverified; no ERC/DRC or hardware immunity testing was performed.

The instruction to find a better RS-485 part is interpreted in the current TVS-selection context. [Alternative TVS research](https://github.com/ofdouglas/ws-hardware/blob/dbcaba10831ade0516dba825d2c97d3f0017e0f5/boards/board1/rs485_tvs_alternatives.md) remains proposed; ST3485EBDR and the accepted bias/termination remain selected. A restricted ground-offset envelope is not accepted merely by requesting research.
