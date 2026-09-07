---
id: ADR-041
title: Combined per-MCU timing and debug headers
status: accepted
scope: Board 1 Rev A
created: 2026-09-07
accepted_by: Explicit maintainer instruction USR-35
supersedes: ADR-007 general breakout scope; ADR-032 three-pin connector format; ADR-039 header cut plan only
requirements: [B1-R020, B1-R025, B1-R027]
sources: [USR-35]
---

# Current authority

ADR-042 records the maintainer-specified pin order and series resistors. Header scope and cut plan below remain accepted; the historical description of pin order as an engineering choice is superseded.

# Decision

Provide one 1x8, 0.1-inch male header per MCU: debug UART RX/TX, two grounds, global SYNC and TRIG inputs to interrupt-capable GPIO on every MCU, and two private EVENT0/EVENT1 outputs per MCU. General ADC, SPI/I2C and GPIO breakouts are deferred to a later revision; no associated support parts or DNP footprints are implied.

Retain the selected Sullins PRPC040SAAN-RC. Four eight-position pieces use 32 positions from one 40-position strip. B1-B027 owns the source-strip purchase; B1-B059 owns all four placed headers. Eight spare positions remain unallocated. Keep independent SWD headers, 115200-baud text UARTs, LEDs, selected resistors and scope-ground access.

[Timing header implementation](../../boards/board1/timing_headers.md) defines the routine pin order and implementation checks. Exact timing pads are not yet verified. The requested interface is accepted; the engineering pin order is a reversible implementation choice. No schematic connectivity or hardware validation is claimed.
