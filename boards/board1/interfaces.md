# Board 1 interfaces and protection

Status: current selected implementation through ADR-039; pinmux, rates and electrical qualification remain open in [requirements](requirements.md). [BOM](BOM.md) owns exact counts; [pinmap](pinmap.md) owns allocation evidence.

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

Each MCU has independent SWD and dedicated 115200-baud TX/RX/GND debug UART. Four 1x3 debug and four 1x5 GPIO sections share one PRPC040SAAN-RC strip (32 positions). Debug off-state protection remains B1-Q014; GPIO loading/mux and proposed 220 ohm series resistors remain B1-Q010. See [GPIO note](gpio_breakouts.md). PCB signal/rail test pads have no purchased components; fitted scope-ground pins B1-B075 still need MPN/count/placement.

## Evidence

[TCAN3413](https://www.ti.com/lit/ds/symlink/tcan3413.pdf), [ST3485EB DS2947](https://www.st.com/resource/en/datasheet/st3485eb.pdf), [SN74LV125A SCES124O](https://www.ti.com/lit/ds/symlink/sn74lv125a.pdf), [ESD2CAN24-Q1 SLVSFW5D](https://www.ti.com/lit/ds/symlink/esd2can24-q1.pdf), [ESDS452 SLVSHM5](https://www.ti.com/lit/gpn/esds452), and [local symbol checks](../../libraries/symbols/remaining_ic_symbol_checks.md). These retain the sources used for existing decisions; this consolidation adds no new electrical verification.
