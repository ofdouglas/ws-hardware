---
id: ADR-042
title: Header series resistors and Rev A recovery scope
status: accepted
scope: Board 1 Rev A
created: 2026-09-07
accepted_by: Explicit maintainer instruction USR-36; recovery deferral uses its conditional authorization
supersedes: ADR-041 engineering pin-order status only; ADR-023 Rev A CBUS recovery requirement
requirements: [B1-R024, B1-R025, B1-R027]
sources: [USR-36]
---

# Decision

The maintainer specifies the exact header order: 1 debug RX, 2 debug TX, 3 GND, 4 SYNC, 5 TRIG, 6 GND, 7 EVENT0, 8 EVENT1. Directions are from the MCU perspective. SYNC/TRIG are global inputs; EVENT0/1 and debug signals are private to each MCU. Fit a separate 330 ohm series resistor close to each of the six MCU signal pins: 24 total. Ground connections have no resistor. Retain four 1x8 sections from the selected strip and independent SWD.

[Timing headers](../../boards/board1/timing_headers.md) defines the branch topology. B1-B076 owns the 24 resistors. Reusing the already selected CRGP0805F330R in 0805 is a routine engineering implementation choice, not a claim of new explicit maintainer MPN acceptance. The two RS-485 bias resistors remain separately counted in B1-B071.

The maintainer permits reset/BOOT0 recovery to wait for Rev B if it is not easily resolved. Apply that permission to the automated FTDI CBUS recovery feature after the bounded check below. B1-R024 is deferred, B1-Q013 is resolved for Rev A by deferral, and B1-B053 has zero Rev A components/footprints. Leave ACBUS5/6 unconnected. Retain ordinary MCU reset, SWD programming/reset and gateway BOOT0-low defaults under B1-B010/B1-Q005. No future recovery circuitry or DNP footprints are reserved.

# Bounded recovery check and disposition

A conventional open-drain reset sink and main-domain BOOT0 driver are straightforward. However, ROM entry also initializes unrelated interfaces. [ST AN2606 Rev.70, Table 117, pp.279–281](https://www.st.com/resource/en/application_note/an2606-stm32microcontroller-system-memory-boot-mode-stmicroelectronics.pdf) says SPI2 MISO PB14 goes high at startup. The draft pinmap uses PB14 for RS-485 DE, so entering ROM would enable that transmitter without application control, potentially contending with an active remote driver. PC6/PC7 also become I2C4 pins instead of application-controlled CAN standby signals. These are concrete allocation dependencies, not a missing startup guarantee.

Fixing recovery therefore extends into networking allocation and ROM-mode behavior review. Given existing independent SWD and the requested schedule, defer that integration. This affects automated ROM recovery only and does not block schematic capture. No assertion is made that recovery is fundamentally infeasible or that USB/CAN output contention has been demonstrated.

Rev A first programming: use SWD connect-under-reset with external bus peers disconnected, install an application that establishes safe PHY defaults, then connect peers. Review reset defaults/normal boot option bytes before schematic approval. A blank device's boot behavior still matters to bring-up despite the recovery deferral. Rev B can reconsider the pin allocation and control circuit together if the feature is promoted again. No ERC, hardware or programming test was performed.
