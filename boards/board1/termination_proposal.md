> Historical reference retained for provenance. Current implementation: [termination.md](termination.md). Earlier selections and open-selection statements below may be superseded; use the current note and accepted ADRs.

# Board 1 bus termination

Status: accepted topology and nominal 120 ohm values, 2026-09-06, USR-28 / [ADR-034](../../docs/decisions/034-rs485-termination.md) / B1-R026. Exact resistor/jumper MPNs accepted ADR-035. This file retains the original proposal path for stable links.

## Principle

For a conventional linear high-speed CAN or bidirectional half-duplex RS-485 link, terminate the two physical ends of the entire bus, using resistance matched to the differential line impedance (typically 120 ohm). A remote termination terminates the remote end; it does not automatically replace the local endpoint termination. The eight-position terminal block carries three independent differential buses, each requiring its own termination arrangement.

Primary guidance: [TI RS-485 termination article, SSZTB23A, March 2026](https://www.ti.com/lit/ta/ssztb23a/ssztb23a.pdf) and [TI CAN evaluation guide, SLLU342, May 2022, pp.2 and 9](https://www.ti.com/lit/pdf/sllu342). The latter illustrates one 120 ohm termination at each end and the 60 ohm combined load. It is topology guidance, not validation of this board's exact transceiver/cable combination.

## CAN_A and CAN_B: accepted routing and switching

Route each onboard CAN bus as a short linear trunk through its four transceivers, ending at the terminal block, with an optional single cable extending that end to remote equipment. Keep transceiver branches short. For each CAN bus, use one 120 ohm termination at the opposite onboard end and a second 120 ohm termination connected through a removable jumper at the terminal-block end.

| Configuration | Opposite onboard end | Terminal-block termination | Far end of external cable |
|---|---|---|---|
| Board-only CAN experiments | Connected | Jumper installed | No cable |
| Cable extends bus to a terminated remote endpoint | Connected | Jumper removed | Connected |
| Cable extends bus to an unterminated remote endpoint | Connected | Jumper removed | Add termination at remote end |

Thus the jumper is installed when the bus ends at the terminal block, and removed when that end is extended. Leaving it installed alongside the onboard far-end resistor and remote resistor would create three 120 ohm loads in parallel (40 ohm), rather than two (60 ohm). Adding local resistance cannot cure a physically unterminated remote cable end.

This means four onboard CAN termination resistors total in the accepted arrangement: two per bus, with two connector-end jumpers total. Exact MPNs, ratings, land patterns and routing remain B1-Q003/004. A jumper goes in series with its resistor branch across CANH/CANL; it must never short the differential pair directly.

If Board 1 must tap the middle of a pre-existing cable already terminated at both ends, the assumptions above change: both board terminations must be disconnected and the board connection must be a suitably short stub. A fixed opposite-end resistor would prevent that mode. That intermediate-node mode is outside the accepted Rev A topology; no additional flexibility footprints are authorized.

## RS-485

For the intended bidirectional point-to-point external link, one local termination at the terminal block and one remote termination are appropriate. Use a fixed local 120 ohm resistor: Board 1 is a cable endpoint and no additional local connector/cable terminator is fitted. It is one resistor on this board, not one resistor total for the link. The remote device must provide its own termination or receive an external terminator there.

No second onboard termination is needed simply to run RS-485 without an external device, since this board has only one RS-485 PHY. This differs from the four-transceiver CAN buses that can communicate entirely onboard. A selectable RS-485 termination would only be warranted for an explicit intermediate-node or external-local-terminator use case; that is not automatically added to Rev A.

For <=12 Mbps and fast transceiver edges, design for proper endpoint termination instead of assuming that a short cable makes it unnecessary. A low-speed/electrically-short exception requires timing/geometry evidence. Termination is distinct from receiver fail-safe bias and interface protection.

## Remaining implementation

B1-B067/068/069/070 hold four CAN resistors, one RS-485 resistor, two headers and two shunts. B1-B007 and B1-B023 exclude these split allocations. See [candidate parts](termination_parts.md). Exact resistor power/pulse ratings, jumper/header/shunt parts, cable impedance, fault voltages and local/remote polarity are TBD. Match resistor dissipation to the selected PHY and required faults before using a generic passive. Existing power estimates already include terminated PHY loading; avoid counting it twice, but reconcile actual loading. No schematic or waveform validation performed.

[ADR-035](../../docs/decisions/035-termination-parts.md) / USR-29 accepts the exact termination MPNs in B1-B067–070. [RS-485 bias investigation](rs485_bias.md) records the proposed network, calculations and remote-kit rate check; B1-Q009 remains open.
