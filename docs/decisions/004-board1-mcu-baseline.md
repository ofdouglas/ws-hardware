---
id: ADR-004
title: Written MCU selection as working baseline
status: accepted
scope: Board 1
created: 2026-09-06
accepted_on: 2026-09-06
accepted_by: Explicit maintainer selection USR-15
supersedes: none
superseded_by: none
requirements: [B1-R001]
questions: [B1-Q005]
sources: [SRC-ARCH sections 3 and 17, SRC-DIAGRAM, USR-15]
---

# ADR-004: Written MCU selection as working baseline

## Context / proposed decision
Carry forward `STM32G474RBT6` ×1 (source package: LQFP64) and `ATSAMC21G17A-AUT` ×3 (source package: TQFP48). These are the written architecture's selections. The topology image instead labels STM32G473CBT6 and SAMC21E15A; use it only for topology orientation.

The source favors gateway peripheral capacity and constrained but practical leaf memory for simultaneous networking and bare-metal/RTOS experiments. It describes the selected leaves as 128 KiB flash / 16 KiB SRAM. These are source claims requiring exact-device verification, not newly validated specifications.

## Alternatives / consequences
The image's smaller variants are not substitution candidates without review. Retaining the written parts avoids restarting selection while the MVP is scoped, but package, pin mux, clocks, memory and simultaneous peripheral feasibility remain B1-Q005.

## Evidence and acceptance criteria
Verify exact orderable devices using primary datasheets and errata; produce a conflict-free pin allocation for all accepted MVP interfaces and debug; review dated sourcing evidence. Resolve any conflicts before schematic freeze. This proposal preserves a source baseline without inventing maintainer approval of a new ADR.

## Revisit trigger
A demonstrated peripheral/pin/resource conflict, unavailable exact part, or changed requirement; not a general desire to compare MCUs again.

## Maintainer acceptance — USR-15 (2026-09-06)

The maintainer explicitly selects one `STM32G474RBT6` and three `ATSAMC21G17A-AUT` and requests that the documents record them as officially selected. This accepts the exact MCU selections and quantities in B1-R001. The proposed-decision text above is retained as history; its statements about pending selection approval are superseded by this acceptance. Exact package/pinmux, electrical, clock, errata, footprint and sourcing verification remain B1-Q005/B1-Q008. Selection acceptance does not mark any allocation verified or accept oscillator/debug implementation proposals.

## Draft implementation evidence

[Board 1 pinmap](../../boards/board1/pinmap.md) links draft sheets for all four selected MCUs. These are implementation proposals, not accepted or verified allocations. B1-Q005 remains open.
