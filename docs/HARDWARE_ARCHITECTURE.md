# Hardware family architecture

Status: draft · Authority: family direction, conditional on board scope · Source: SRC-ARCH

The September 1 bench draft describes a larger system than Board 1 MVP. Its “freeze summary” is not a blanket rev-1 requirement after USR-01. [Board 1 requirements](../boards/board1/requirements.md) own the MVP boundary.

## Conventions for the proposed MVP

| Area | Direction | Controlling record |
|---|---|---|
| Roles | One gateway and three leaves; physical labels are not HostIds | B1-R001; ADR-004 |
| CAN | Two independent shared CAN-FD buses, all four nodes on each | B1-R002; ADR-002 |
| UART | Shared open-drain medium plus private directed leaf ring | B1-R003, B1-R004 |
| Bring-up | USB 2.0 Standard-B power and dedicated FT232HL VCP; no dependency on native USB | B1-R005; ADR-001 |
| Power | Accepted independent bridge domain and controlled main-board power; SC189 selected under ADR-010; EN-only main-rail control and SN74LV125APWR selected under ADR-013; enable circuit open | B1-R006; B1-Q002 |
| Debug | Independent SWD access to each MCU; accessible reset and rail measurements | B1-R007, B1-R008 |
| Connectors | Pinouts, polarity, voltage, and termination state documented at each interface | B1-Q004 |

No connector family, pin numbers, transceiver, oscillator, protection network, or supply capability is validated here.

## Future/full bench contract — excluded from MVP unless explicitly promoted

| Area | Inherited direction | MVP treatment |
|---|---|---|
| Signal backbone | 17 twisted pairs; short approximately 10 cm FFTP-style jumpers and polarized headers | Deferred; no connector or pin allocation implied |
| CAN1/2/3 | Passive IN-to-OUT paths; each independently terminable even without a local PHY | Applies to future backbone boards only |
| CAN3 local port | STM32 connection with initial DNP PHY in full draft | Deferred, including footprint and termination |
| RS-485 | RS_485_MULTIDROP (historical SHARED) passes through; RS_485_LEFT/RIGHT terminate separate p2p hop segments and require forwarding | Rev A one p2p port; expanded Board 1 LEFT/RIGHT only; bench multidrop retained |
| 24V_AUX | Optional separate two-conductor passive trunk; nominal 24 V, draft chain maximum 2 A | Deferred; not a Board 1 input rating |
| Local power tap | Protected branch converts to 5 V; downstream trunk never depends on local regulation/firmware | Deferred |
| Source protection | One external 24 V source per chain; reverse polarity/current protection at injection; isolate USB and local 5 V sources | Conditional on future multiple-input implementation |
| Auxiliary output | Protected 5 V, draft 500 mA maximum when supply budget permits | Deferred from Rev A; no USB-only guarantee |
| Test control | External single SPI master; ordinary DUT boards slaves; MCP23S17 family preference | Deferred |
| Triggers/timing | TEST_TRIG0/1, SYNC inputs; selected TIMING0/1 drivers, others high-Z | Deferred |
| Fault injection | External trigger plus local deterministic logic; safe inactive startup; independent of DUT firmware | Deferred |
| Ethernet/T1S | Ordinary Ethernet separately cabled; backbone pair reserved for T1S | Deferred |
| FPGA | Timing capture, traffic generation, segment bridges and controlled frame loss | Future separate instrumentation board |

The draft pair map is functional, not an approved connector pinout: 1–3 CAN1/2/3; 4 RS485_SHARED (RS_485_MULTIDROP, retained for bench); 5 RS485_HOP; 6 T1S_RESERVED; 7–10 TEST_SPI SCLK/MOSI/MISO/CS each with GND; 11 SYNC/GND; 12–13 TEST_TRIG0/1 with GND; 14–15 TIMING0/1 with GND; 16–17 spare. Pin order and electrical details remain unapproved.

Normal WS operation must remain useful without the test-control plane. A future backbone board must explicitly adopt the applicable contract; being a WireSpaces board alone does not impose every connector or PHY.

Board 1 clock/VCP requirements (ADR-005): 168 MHz gateway, 12 Mbaud VCP with RTS/CTS and four-signal power-off isolation; each MCU has its own external crystal. Crystal frequencies and remaining clock trees are implementation work in B1-Q008.

Rev A interface scope: ADR-007 includes both CANs and one RS-485 with ground, plus GPIO breakouts; additional transceivers and external power remain deferred. Canonical CAN names are FD_CAN_A/FD_CAN_B (historical CAN1/CAN2).

ADR-007 is Board 1-specific. Its omission of RS_485_MULTIDROP does not remove that function from the family architecture. Board 1 also requires five LEDs total and spare GPIO breakouts; implementation values remain open.

## Future Board 1 power clarification — USR-12

The intended external-power chain is protected 24 V -> regulated 5 V -> FTDI supply branch and sequenced 3.3 V converter -> MCUs/transceivers. Thus the downstream 3.3 V converter need not accept 24 V. External power remains deferred from Rev A.

Implementation proposal for that later revision: select between USB VBUS and the locally generated 5 V with reverse-current blocking before feeding the system domains; never directly tie the two sources together. Revisit bridge USB-presence sensing, self-powered configuration and main-board enable policy for externally powered operation. Existing Rev A active-PC/suspend behavior stays authoritative until that revision adopts a new power contract. Two-stage efficiency is the product of stage efficiencies; the current 90% target applies to the main converter, not automatically to the entire 24 V path. See [TPSM84203 evaluation](../boards/board1/buck_tps560430.md).
