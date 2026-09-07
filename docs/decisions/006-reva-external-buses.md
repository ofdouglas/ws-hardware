---
id: ADR-006
title: Rev A links and terminal access
status: superseded
scope: Board 1 Rev A feature boundary
created: 2026-09-06
accepted_on: 2026-09-06
accepted_by: Explicit current user scope instruction USR-05
supersedes: none
superseded_by: ADR-007
requirements: [B1-R016, B1-R017, B1-R018]
questions: [B1-Q001, B1-Q009]
sources: [USR-05]
---

# ADR-006: Rev A links and terminal access

## Decision
Rev A implements FD_CAN_A and FD_CAN_B (historically CAN1/CAN2), all onboard UARTs, the VCP and one STM32 external RS-485 interface. Both CAN buses and RS-485 must be accessible through terminal-block connections including one or two ground terminals. The implementation proposal uses two grounds; terminal order/MPN is not frozen.

Additional RS-485 transceivers, STM32-only CAN3 and further external connectivity belong to later revisions. Estimate the expanded configuration as three total STM32 RS-485 PHYs plus one CAN3 PHY; the terminal connection to an existing CAN bus adds no PHY.

## Context / consequences
This resolves the Rev A networking scope. It narrows the earlier broad statement that external connectors were deferred: these three signal interfaces are now explicitly included. B1-R013 is superseded by B1-R018 to preserve its history. USB-only active-PC power and UART isolation (ADR-001), clock requirements (ADR-005), and the exclusion of the full backbone/test architecture (ADR-003) remain in force.

Exact PHYs are still candidates. Half-duplex non-isolated RS-485, 8-position terminal order and two grounds are implementation proposals. See https://github.com/ofdouglas/ws-hardware/blob/dbcaba10831ade0516dba825d2c97d3f0017e0f5/boards/board1/transceivers_and_power.md for the shortlist, sources and estimates.

## Acceptance and review
USR-05 supplies feature scope, not approval of specific transceivers, connector pin order, electrical limits or unrestricted future USB power. Verify the complete bus termination and off-board signal/protection geometry before schematic approval.

## Revisit trigger
Explicit scope change or demonstrated interface feasibility issue.
