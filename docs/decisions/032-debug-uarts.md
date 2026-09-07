---
id: ADR-032
title: Independent MCU text debug UARTs
status: accepted
scope: Board 1 all four MCUs
created: 2026-09-06
accepted_by: Explicit maintainer instruction USR-26
supersedes: none
superseded_by: none
requirements: [B1-R025]
questions: [B1-Q014]
---

# Decision

Expose a dedicated TX/RX/GND text-debug UART for each of the four MCUs at 115200 baud, on a three-position 0.1-inch (2.54 mm) header. These are additional to SWD, gateway VCP, multidrop, ring and RS-485. Header category and rate are accepted by USR-26; exact header MPN and implemented pin allocation remain unverified.

Propose 3.3 V non-inverted logic, idle high, 8N1 and no flow control. Number each header 1=MCU TX, 2=MCU RX, 3=GND; no power pin. Silkscreen identifies GW/SAM0/SAM1/SAM2 and directions from the MCU perspective. Adapter RX connects to MCU TX and adapter TX to MCU RX. Use a 3.3 V logic USB-UART adapter, not an RS-232-voltage interface. Off-state adapter drive and protection require B1-Q014 review before connection to an unpowered target.

# Draft allocation and evidence

SAM0/1/2 each use SERCOM2: PA12 pad21 TX/PAD0 and PA13 pad22 RX/PAD1, mux C, TXPO=0 and RXPO=1. This leaves SERCOM0 multidrop and SERCOM1 ring intact. [DS60001479J](https://ww1.microchip.com/downloads/en/DeviceDoc/SAM-C20-C21-Family-Data-Sheet-DS60001479J.pdf), p.22, Table 6-2 p.30 and USART CTRLA p.505.

STM32G474RBT6 uses LPUART1: PB11 pad33 TX and PB10 pad30 RX, AF8. The low-power UART can serve as an ordinary asynchronous debug port; this does not replace USART2 VCP. [DS12288 Rev.6](https://www.st.com/resource/en/datasheet/stm32g474vb.pdf), pp.50,63,74. LPUART kernel source/prescaler/baud and SAM SERCOM baud setup still need validation at 115200.

# Consequences and remaining checks

Eight unused MCU pads become debug signals; existing link and breakout allocations remain intact. Keep stable per-pad IDs in the workbook. B1-B059 covers four fitted headers (source strip MPN/cut quantity TBD), B1-B060 covers support/protection as required. Do not count cut headers and source strips twice or reuse occupied UART-buffer channels.

B1-Q014 covers header order/footprint/MPN, input defaults, off-state/back-power behavior, short bench cable assumptions, current limits, clock/baud error, firmware resource use and simultaneous UART/CAN traffic. Confirm exact current datasheets/errata, electrical compatibility and footprint before marking any row verified. No schematic, ERC/DRC or hardware validation is claimed.

Alternatives: multiplexing debug over network/VCP would not provide the requested dedicated per-MCU interface; SWD remains complementary. 8N1 and header ordering are implementation proposals, not separately accepted maintainer requirements.
