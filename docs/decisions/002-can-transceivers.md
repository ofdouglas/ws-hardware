---
id: ADR-002
title: CAN-FD transceiver selection
status: accepted
scope: Board 1 FD_CAN_A/FD_CAN_B and future STM32-only third CAN
created: 2026-09-06
accepted_on: 2026-09-06
accepted_by: Explicit user selection USR-06
supersedes: none
superseded_by: none
requirements: [B1-R002, B1-R009]
questions: [B1-Q003, B1-Q004]
sources: [SRC-ARCH sections 4 and 16, USR-06]
---

# ADR-002: CAN-FD transceiver selection

## Context / decision
Support two separate shared CAN-FD buses, each connecting the STM32 and all three SAMs. Plan one PHY channel per MCU per bus (eight channels total); device/package count depends on selection. The user selects TCAN3413DR for these channels and the future STM32-only third CAN. Eight devices are required in Rev A; nine in the expanded estimate. Part selection is accepted; package/pin/footprint and electrical implementation remain unverified.

## Alternatives / consequences
The prior comparison included 3.3 V and 5 V options; the selected part now fixes this design direction. Common parts simplify stocking; control features and supply choices affect pin and power budgets. CAN3 from the full architecture does not enter this BOM by default.

## Acceptance evidence and remaining checks
Resolve B1-Q003/004: target arbitration/data rates, geometry/external access, termination and protection, and required control behavior. Compare exact manufacturer datasheets, errata and dated sourcing evidence. Check I/O compatibility and behavior during reset/unpowered states. USR-06 accepts the MPN. Complete implementation review before schematic approval.

## Revisit trigger
A verified electrical mismatch, changed bus requirements, or material sourcing/lifecycle issue.

Shortlist and power evidence: [https://github.com/ofdouglas/ws-hardware/blob/dbcaba10831ade0516dba825d2c97d3f0017e0f5/boards/board1/transceivers_and_power.md](https://github.com/ofdouglas/ws-hardware/blob/dbcaba10831ade0516dba825d2c97d3f0017e0f5/boards/board1/transceivers_and_power.md). Rev A terminal scope is retained in ADR-007; TCAN3413DR selection is accepted by USR-06; implementation review remains open.
