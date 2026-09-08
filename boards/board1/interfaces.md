# Board 1 interfaces and protection

Gateway correction (2026-09-07): STM32G473RBT6 is selected and captured per [ADR-043](../../docs/decisions/043-gateway-part-correction.md). DS12288 references and older workbook/PDF snapshots below are prior G474 evidence, not G473 qualification. Recheck exact G473 AF/electrical limits under B1-Q005/008 before schematic approval.

Status: current selected implementation through ADR-039; complete draft capture; rates and electrical qualification remain open in [requirements](requirements.md). [BOM](BOM.md) owns exact counts; [pinmap](pinmap.md) owns allocation evidence.

## External buses

| Interface | Selected PHY | Selected protection | Network |
|---|---|---|---|
| FD_CAN_A and FD_CAN_B | Eight TCAN3413DR total, one per MCU per bus | Two ESD2CAN24DBZRQ1 total, one per terminal pair | Fixed plus jumper-removable termination per bus |
| Gateway RS485_EXT | One ST3485EBDR, 3–3.6 V supply, 12 Mbps ceiling | One ESDS452DBZR | Fixed local termination and one accepted 330 ohm bias pair |

Authority: ADR-002/034/037/038; [termination](termination.md), [bias](rs485_bias.md). Both TVS types use DBZ pins 1/2 for their bus wires and pin 3 for ground. Place near terminal entry with short ground returns; CAN TVS is connected regardless of termination jumper state. Verify exact symbol/footprint and routed connectivity. Remaining protection/control B1-B007/023 must exclude these split allocations.

**RS-485 operating contract:** each wire must stay within +/-5.5 V of Board 1 ground during normal operation, including ground offset and ringing. ESDS452DBZR selection accepts this restricted bench envelope, not the full RS-485 common-mode range. Its cited 15 A test clamp reaches the PHY absolute limit without overshoot margin; this is not a validated surge rating. No 24 V fault protection is implied. Establish actual remote hardware, cable/polarity, leakage, offsets, DE and /RE defaults and local-off backfeed behavior under B1-Q009.

The published ConnectCore 93 carrier population may use a 250 kbit/s PHY. Verify the owned kit before setting link speed; the detailed evidence and initial 115200-baud suggestion are in [rs485_bias.md](rs485_bias.md). Board 1's PHY ceiling does not set the remote endpoint's capability.

## Onboard UART_MD

B1-B066 is a second SN74LV125APWR, separate from the fully allocated VCP buffer. Power it from 3V3_SYS and use one existing auxiliary 100 nF bypass from B1-B036. For each of four channels: A -> GND, MCU UART_MD_TX -> /OE, Y -> shared UART_MD. All MCU UART_MD_RX inputs observe the shared bus. High/idle TX releases the output; low TX drives the shared line low.

Four RMCF0805FT10K0 /OE pull-ups (B1-B008) default drivers released. One RMCF0805FT470R 470 ohm pull-up (B1-B074) pulls the shared bus to 3V3_SYS. These values/parts are accepted ADR-039; do not leave them as selection questions. Confirm reset/ramp pin states, VOL, receiver thresholds, bus capacitance and simultaneous mux use under B1-Q003/005.

At 3.3 V the pull-up draws approximately 7 mA when low. Ideal 470 ohm RC 10–90% rise times for 50/100/200 pF are 51.7/103.4/206.8 ns; this is a screen, not a qualified baud rate. SN74LV125A is not a 24 mA LVC driver. Include real drive limits and reset/power behavior before accepting several-Mbaud operation. Reconcile duty-dependent pull-up current with the power model.

## Other links and access

The SAM UART ring is direct point-to-point signaling, separate from UART_MD; rates and pinmux remain under review. Gateway VCP TX/RX/RTS/CTS and power-off isolation are in [usb_vcp.md](usb_vcp.md).

Each MCU has independent SWD and a combined 1x8 timing/debug header under ADR-041. Four sections share one PRPC040SAAN-RC strip (32 positions). See [timing headers](timing_headers.md) for pin order, shared inputs and private outputs. B1-Q005/010 retain timing pad/interrupt and load checks; B1-Q014 retains debug qualification. PCB test pads and fitted scope-ground access remain required; six dedicated two-post ground headers are captured; exact placement/clip clearance remains layout work.

## Evidence

[TCAN3413](https://www.ti.com/lit/ds/symlink/tcan3413.pdf), [ST3485EB DS2947](https://www.st.com/resource/en/datasheet/st3485eb.pdf), [SN74LV125A SCES124O](https://www.ti.com/lit/ds/symlink/sn74lv125a.pdf), [ESD2CAN24-Q1 SLVSFW5D](https://www.ti.com/lit/ds/symlink/esd2can24-q1.pdf), [ESDS452 SLVSHM5](https://www.ti.com/lit/gpn/esds452), and [local symbol checks](../../libraries/symbols/remaining_ic_symbol_checks.md). These retain the sources used for existing decisions; this consolidation adds no new electrical verification.

## Retained protection and debug checks

ESD2CAN24DBZRQ1 has 3 pF typical channel C and a typical 37 V clamp at 5.7 A, 8/20 us (SLVSFW5D). These typical values do not guarantee clamp margin. Check both TCAN3413 per-pin +/-58 V absolute limits and its 58 V differential limit: opposite-polarity clamps can violate differential stress even if each pin passes. The protected port cannot inherit the bare PHY sustained-fault rating.

ESDS452DBZR has 3 pF typical/5 pF maximum channel C and 50 nA maximum leakage at the stated standoff/table conditions. Its 8/20 us clamp is 7.5 V typical/10 V maximum at 1 A, 11.5 V typical/14 V maximum at 15 A; the 9.6 V TLP figure is a different typical test. Retain actual-temperature leakage, bias margin, waveform and layout coordination checks. Route discharge returns without MCU ground necks or long TVS stubs.

UART_MD's 470 ohm resistor at 3.6 V/-1% R draws 7.74 mA before VOL drop, about 27.9 mW. This approaches the cited LV125 8 mA operating test point: qualify VOL and timing, not just resistor dissipation.

SWD target reference is voltage sense, not authorization for probe power. Check all debug signals with 3V3_SYS off, cable orientation and connect-under-reset. Owned J-Link EDU is planned, PICkit 5 available (ADR-011); verify exact-device support and the owned 20-pin-to-Cortex-10-pin adapter ([SEGGER adapters](https://www.segger.com/products/debug-probes/j-link/accessories/adapters/overview/)). The SAM checklist Table53-7 p.1182 permits10–50kohm SWCLK pull-up (33kohm recommended). Capture uses the already selected10kohm MPN in B080; no new resistor value is needed.

The accepted Phoenix 1989803 terminal has eight positions at 2.5 mm pitch. Captured order is CAN_A_H, CAN_A_L, GND, CAN_B_H, CAN_B_L, RS485_A, RS485_B, GND; confirm numbering and actual peer polarity under B1-Q004. Ground terminals remain required.

ADR-042 specifies 330 ohm in series near every MCU header signal pin (24 total, B1-B076). SYNC/TRIG share header-side nets with one resistor per MCU input; debug and EVENT nets remain private. Grounds connect directly. Automated CBUS recovery is deferred; independent SWD remains.

USR-37 adds one 10 kohm pull-down to each shared SYNC/TRIG net (B1-B077), before its four MCU-side series branches. See [timing headers](timing_headers.md). No additional MCU pins or repeated per-MCU pull-downs are needed.

Complete capture: each TCAN3413 STB has10k to3V3_SYS (B083), following TI§7.3.8 guidance against relying solely on internal failsafe bias. RS-485 DE has10k toGND; /RE, DI and RO each have10k toSYS (B023). Firmware sets TX idle before enabling PHYs. PC11 FT_f input supports the ST3485 RO guaranteed high level per DS12288Rev6 Table54; see CAD notes for the static margin. Disable/disconnect powered RS-485 peers before local power-off/suspend because the accepted bias resistor otherwise feeds SYS.
