# Remaining Board 1 component decisions

Reviewed 2026-09-06 against accepted decisions through ADR-036. The [current BOM](BOM.md) and CSV distinguish exact MPN acceptance from unfinished implementation. Zero-quantity superseded parts are excluded.

| Area / BOM IDs | Remaining selection or implementation |
|---|---|
| LED resistors B1-B026 | RK73H2ATTD3301F remains provisional; no recorded acceptance |
| External RS-485 B1-B021/023 | ST3485EBDR decided ADR-034; bias/control/protection and loaded-current qualification remain open |
| Onboard UART multidrop B1-B008/066 | Second SN74LV125APWR decided ADR-033; support pull-ups, reset/ramp checks and rate remain open |
| CAN/RS-485 termination B1-B067–070; protection B1-B007 | Termination topology, counts and 120 ohm values decided ADR-034; exact [resistor/jumper parts](termination_parts.md) decided ADR-035; ratings/footprints and protection qualification remain open |
| Reset/boot and CBUS B1-B010/053 | Exact support and power-off-safe interface components |
| VCP isolation B1-B016 support | /OE and signal defaults; bypass already allocated in B1-B036 |
| Bridge support B1-B017/061–065 | Decided capacitor and EEPROM pull-up MPNs now have explicit rows; remaining bridge capacitor counts and residual network enumeration open |
| GPIO B1-B027 | Source-strip MPN decided; cut schedule/count, load/protection contract and proposed GPIO series resistors open |
| Text-debug UART B1-B059/060 | Four 1x3 header category decided; exact MPN/cut schedule and off-state adapter protection open |
| Test points B1-B011 | Pads versus fitted parts and locations |
| USB shell | USB-B1HSB6 decided; shield bonding and any support parts open |

USB/FTDI crystal MPNs, oscillator load capacitors, corrected REF resistor, enable pull-down, LEDs, damping components, buck components and general ceramic MPNs are decided. Do not ask to select them again merely because electrical qualification remains unfinished. B1-Q002/005/008/011/012 retain the relevant power, footprint, oscillator and rail checks.

No stock or hardware qualification is implied by decided status. See [audit findings](bom_review.md) for the reconciled scope and checks.

[ADR-035](../../docs/decisions/035-termination-parts.md) / USR-29 accepts the exact termination MPNs in B1-B067–070. [RS-485 bias investigation](rs485_bias.md) records the accepted network, calculations and remote-kit rate check; B1-Q009 remains open.

[ADR-036](../../docs/decisions/036-rs485-bias.md) / USR-30 accepts two 330 ohm 1% bias resistors in B1-B071: 3V3_SYS to A (ST3485EBDR pin6), B (pin7) to GND. Exact MPN and implementation remain unverified. [TVS recommendations](tvs_candidates.md) remain proposed under B1-Q004/009.
