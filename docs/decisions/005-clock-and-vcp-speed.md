---
id: ADR-005
title: Crystal-referenced clocks and 12 Mbaud gateway VCP
status: accepted
scope: Board 1 Spin A clocking and VCP capability
created: 2026-09-06
accepted_on: 2026-09-06
accepted_by: Explicit user instruction USR-04 in current design conversation
supersedes: none
superseded_by: none
requirements: [B1-R014, B1-R015]
questions: [B1-Q003, B1-Q005, B1-Q008]
sources: [USR-04]
---

# ADR-005: Crystal-referenced clocks and 12 Mbaud gateway VCP

## Decision
Design the STM32 gateway to operate at 168 MHz and its FT232H VCP UART to support 12 Mbaud. Provide TX, RX, RTS and CTS, short interconnects, and power-off isolation on all four signals. All four MCUs use individual external crystals as the references for their high-speed link clocks. The FTDI retains its own external crystal.

Onboard UARTs target several Mbaud, with exact rates subject to peripheral timing and electrical review. Only the gateway VCP requires 12 Mbaud; do not impose that target on the SAM leaves or the open-drain multidrop medium.

## Context / alternatives / consequences
168 MHz is the user's preferred gateway operating point. The derived 12 Mbaud configuration uses a 168 MHz USART kernel clock and 8x oversampling, not merely a 168 MHz CPU. Internal RC-only link timing and omitting RTS/CTS would violate this decision. Crystal frequencies, MPNs, load networks, exact MCU pins and final bus clock trees remain implementation choices, not accepted values.

The accepted power-off isolation architecture is recorded in ADR-001. See [clock and UART implementation note](../../boards/board1/clocking.md) for calculation, signal directions and remaining verification.

## Acceptance and validation
USR-04 explicitly accepts power architecture/isolation and requests the clock, speed, flow-control and crystal requirements. This accepts design requirements, not measured 12 Mbaud performance. Verify clock routing, mux conflicts, oscillator margins, isolation timing and sustained full-duplex operation before hardware sign-off.

## Revisit trigger
An evidenced silicon/pin/timing/power limitation or explicit changed requirement; do not routinely reopen the selected speed or external-crystal policy.
