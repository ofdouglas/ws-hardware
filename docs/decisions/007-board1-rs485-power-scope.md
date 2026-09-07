---
id: ADR-007
title: Board 1 RS-485 scope, LEDs and GPIO access
status: accepted
scope: Board 1 only; WS bench multidrop retained
created: 2026-09-06
accepted_on: 2026-09-06
accepted_by: User instructions and scope clarification USR-06
supersedes: ADR-006
superseded_by: ADR-041 (header/general-breakout clauses only)
requirements: [B1-R016, B1-R017, B1-R019, B1-R020, B1-R021, B1-R022]
questions: [B1-Q002, B1-Q009, B1-Q010]
sources: [USR-05, USR-06]
---

# ADR-007: Board 1 RS-485 scope, LEDs and GPIO access

## Decision
Retain Rev A's two shared CAN-FD buses, all onboard UARTs, VCP and one external RS-485, with both CANs and RS-485 on terminals including ground(s). TCAN3413DR selection is accepted separately in ADR-002.

The expanded Board 1 has only RS_485_LEFT and RS_485_RIGHT point-to-point ports, plus the STM32-only third CAN. RS_485_MULTIDROP is descoped for Board 1 currently. It remains in the overall WS bench architecture, including the historical RS485_SHARED backbone function; do not remove the family capability or its reserved connectivity.

Use 12 Mbps as the external RS-485 design maximum. Provide one LED per MCU, one board power LED, and a few spare GPIOs per MCU on breakouts. Exact LED current, GPIO count/pins, breakout load contract and RS-485 MPN remain implementation proposals. THVD1420DR is preferred for review, not yet accepted.

## Consequences / supersession
This supersedes ADR-006 to update its three-RS485 expanded assumption and extend Rev A with LEDs/GPIO breakouts. Rev A still has one RS-485, not both point-to-point ports. B1-R022 replaces B1-R018's broad connector deferral. USB-only active-PC power, independent bridge and isolation remain unchanged. Future external power details stay deferred. Reducing the port count does not establish a worst-case 500 mA guarantee.

## Validation / revisit trigger
Validate power with all LEDs on, external I/O loads and the required traffic. A change to Board 1 scope or demonstrated power/electrical limitations can justify a superseding decision; it does not automatically change the bench family.

## Rationale addendum — USR-07

The user explicitly reaffirms the single Rev A STM32 RS-485 port to connect an existing Digi ConnectCore 93 development kit alongside FD_CAN_A and FD_CAN_B, forming a dual-gateway lab. Retain all three external interfaces during power optimization. Removing the Rev A RS-485 port was considered but not accepted. This adds rationale without changing the accepted decision. Kit interface details and common operating rates require verification under B1-Q004/009 before wiring.

Header/general-breakout clauses are partially superseded by [ADR-041](041-timing-debug-headers.md). Other decisions remain in force.
