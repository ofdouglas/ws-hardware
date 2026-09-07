# Board 1 bus termination

Status: topology and exact parts accepted ADR-034/035; circuit, thermal and mechanical qualification open. Scope: B1-R026. Terminate the two physical ends of each complete bus; remote parts are outside the onboard BOM.

## CAN_A and CAN_B

Route each bus as a short linear trunk through its four PHYs, with short branches. One end is opposite the terminal block, the other at the terminal block, optionally extended by one external cable. Fit a fixed 120 ohm at the opposite onboard end and a jumper-removable 120 ohm at the terminal end.

| Use | Fixed onboard resistor | Terminal-end jumper | Remote end |
|---|---|---|---|
| Board-only | Connected | Installed | No cable |
| External cable extension | Connected | Removed | Must have its own termination |

The jumper is in series with the resistor branch across CANH/CANL, never directly across the pair. Leaving it installed when a remote termination is present gives three terminators (40 ohm combined), not the intended two (60 ohm). A remote unterminated end must be corrected there. Mid-bus tapping is outside this Rev A topology because the opposite onboard resistor is fixed; no extra flexibility footprints are implied. TVS remains connected independently of jumper state.

## RS-485

Board 1 is a point-to-point cable endpoint. Fit one fixed local 120 ohm across A/B at the terminal; the remote endpoint needs its own termination. There is no second onboard resistor or termination jumper for RS-485. [Idle bias](rs485_bias.md) and [protection](interfaces.md) are separate networks. The selected 12 Mbps ceiling does not waive endpoint termination or cable qualification.

## Accepted parts and allocation

| BOM | Qty | MPN | Function |
|---|---:|---|---|
| B1-B067 | 4 | CRGP0805F120R | Two 120 ohm, 1%, 0805, 1/3 W resistors per CAN |
| B1-B068 | 1 | CRGP0805F120R | Local RS-485 termination |
| B1-B069 | 2 | PRPC002SAAN-RC | Dedicated 1x2, 2.54 mm CAN jumper headers |
| B1-B070 | 2 | SPC02SYAN | CAN shunts |

Do not allocate these dedicated headers from the GPIO/debug strip. B1-B007/023 exclude these split termination rows. Existing PHY power allowances include terminated loading; reconcile actual bias/driver loading without counting the full termination load twice.

## Qualification and evidence

Using 118.8 ohm minimum resistance, 3.6 V differential dissipates 0.109 W; 5 V dissipates 0.210 W. These are screens, not bounds on external drivers or faults. Verify derating, pulse exposure, remote levels and board temperature under B1-Q003/004/009. [TE exact resistor page](https://www.te.com/en/product-1-2176327-4.html) supports the selection; series thermal verification remains open.

[Header drawing 11635 RevB](https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/386/xRxCzzzSxxN-RC_ST_11635-B.pdf) gives 5.84 mm mating length; [shunt drawing 11134 RevD](https://drawings-pdf.s3.amazonaws.com/11134.pdf) gives 5.74 +/-0.20 mm maximum insertion depth. Check seating gap, engagement and clearance in sample mating/layout. Footprint and physical fit are unverified.

Topology sources: [TI RS-485 termination guidance SSZTB23A](https://www.ti.com/lit/ta/ssztb23a/ssztb23a.pdf), [TI CAN guide SLLU342](https://www.ti.com/lit/pdf/sllu342). Git history retains the original research and dated price/stock snapshots. Refresh DigiKey availability at procurement. No ERC/DRC or waveform validation is asserted.
