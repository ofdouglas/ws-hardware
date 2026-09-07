Current decision: **ST3485EBDR selected**, USR-28 / [ADR-034](../../docs/decisions/034-rs485-termination.md). Termination topology accepted; exact passive/jumper MPNs remain open. The research below is historical; TI fail-safe claims do not apply to ST3485EBDR.

Historical cost-focused shortlist: [ST3485EBDR and MaxLinear SP3485CN-L](rs485_cost_options.md). Both remain proposed; this updates the recommendation, not accepted BOM authority.

# External RS-485 candidates and UART multidrop selection history

Current UART_MD decision: [ADR-033](../../docs/decisions/033-open-drain-uart-buffer.md) selects a second SN74LV125APWR (B1-B066), with grounded A and UART TX driving /OE. Below are the earlier unselected alternatives; their drive-current figures and support counts must not be applied to the selected LV125. Its local bypass uses one B1-B036 reserve, leaving two after the VCP buffer. Support values/rate remain B1-Q003.

Historical candidate review 2026-09-06. Status: proposed; B1-R003/016/021, B1-Q003/009. These are two separate interfaces. No candidate is accepted by the BOM reconciliation, and no new footprint is authorized by this research. Existing source CAD is absent.

## External RS-485

Recommend **TI THVD1450DR**, SOIC-8, for the next selection. It operates from 3.0–5.5 V, provides half-duplex operation with separate DE and /RE, and supports up to 50 Mbps. Operation at the board's <=12 Mbps ceiling does not require a 12-Mbps-only part. Receiver fail-safe covers open, shorted and idle terminated bus conditions. The fast driver edges still require short stubs and correct cable termination; a slower UART setting does not slow those edges. Source: [TI SLLSEY3E, Rev.E, May 2019, pp.4–5, 8–11 and 19](https://www.ti.com/lit/ds/symlink/thvd1450.pdf).

SOIC proposal: 1=R to MCU RX, 2=/RE, 3=DE, 4=D from MCU TX, 5=GND, 6=A, 7=B, 8=3V3_SYS. Preserve the existing separate gateway DE and /RE allocations. Keep the driver disabled during reset; review receiver/shutdown policy, bus polarity and remote equipment before wiring. Use the existing RS-485 bypass allocation in B1-B036, without adding a second copy. This is a candidate pin-function review, not verified MCU mux/footprint allocation.

| Exact MPN | DigiKey cut-tape code | Availability observed | Qty-one USD | Disposition |
|---|---|---:|---:|---|
| [THVD1450DR](https://www.digikey.com/en/products/detail/texas-instruments/THVD1450DR/9356550) | 296-50395-1-ND | 17,382 | 2.17 | Preferred stocked candidate |
| [THVD1420DR](https://www.digikey.com/en/products/detail/texas-instruments/THVD1420DR/14124063) | 296-THVD1420DRCT-ND | Out of stock | Not used | Existing unaccepted 12 Mbps candidate; replaced in B1-B021 by accepted ST3485EBDR |

Stock is page evidence retrieved for this review, not reserved inventory. Recheck at purchase. Do not accept a distributor-suggested substitute solely on its parametric match: direction-control behavior and exact pinout matter.

B1-Q009 still needs cable/endpoint common-mode and fault review, termination topology, DE timing, external protection and loaded current. Retain the existing conservative 60/75 mA RS-485 planning allowances until recalculated; no savings are assumed. Built-in IC ESD ratings are not a board-level protection qualification. These limits and currents need complete exact-device review before evidence becomes verified.

## Historical UART multidrop candidates — not selected

Recommend **four TI SN74LVC1G07DBVR**, one SOT-23-5 non-inverting open-drain buffer per MCU TX. At 3.0–3.6 V the input thresholds are VIH >=2.0 V and VIL <=0.8 V; the specified sink capability at 3 V is up to 24 mA. The higher advertised 32 mA rating applies at 4.5 V. Partial-power-down Ioff is specified. DBV pins: 1=NC, 2=A, 3=GND, 4=Y, 5=VCC. Source: [TI SCES296AG, Rev.AG, October 2025, pp.3–6 and 9](https://www.ti.com/lit/ds/symlink/sn74lvc1g07.pdf).

Proposal:

```text
Each MCU TX --> non-inverting open-drain buffer --> shared UART_MD
Each MCU RX <------------------------------------ shared UART_MD
3V3_SYS ---- one shared pull-up ----------------> shared UART_MD
```

TX high releases the bus; TX low pulls it low. The bus is high only when every transmitter releases it. RX remains able to observe traffic, including the local transmitter's echo. Firmware must coordinate transmitters; electrically safe wired contention does not decode overlapping frames correctly. A plain inverting transistor stage would reverse normal UART polarity and is not this proposal.

Power buffers and the bus pull-up from 3V3_SYS. Bias each buffer input high while its MCU TX is undriven; the already selected 10 kohm resistor MPN is a candidate for these additional positions, not an accepted new quantity. Qualify high-impedance reset/ramp behavior: Ioff at VCC=0 does not prove arbitrary brownout behavior or isolate all attached MCU RX pins. Never tie push-pull MCU TX outputs directly together.

| Exact MPN | Role / proposed quantity | DigiKey cut-tape code | Page stock / qty-one USD |
|---|---|---|---|
| [SN74LVC1G07DBVR](https://www.digikey.com/en/products/detail/texas-instruments/SN74LVC1G07DBVR/377455) | Preferred; 4 single gates near MCUs | 296-8485-1-ND | 148,394 / $0.14 |
| [MC74LCX07DTR2G](https://www.digikey.com/en/products/detail/onsemi/MC74LCX07DTR2G/920963) | Alternative; 1 hex buffer, use 4 channels | MC74LCX07DTR2GOSCT-ND | 17,240 / $0.39 |

The onsemi alternative offers non-inverting open-drain outputs and 24 mA sink capability at 3.0 V in TSSOP-14. It consolidates packages but routes all TX signals to one location. Tie unused inputs to a defined level and leave their outputs unconnected. Exact ordering and mechanical details: [MC74LCX07/D, Rev.16, July 2024, pp.1–5 and TSSOP drawing](https://www.onsemi.com/pdf/datasheet/mc74lcx07-d.pdf). The similar TI SN74LVC07APWR was also considered, but its [exact DigiKey page](https://www.digikey.com/en/products/detail/texas-instruments/SN74LVC07APWR/377393) showed zero stock. Do not populate both driver alternatives.

## Pull-up and timing screen

A single **470 ohm, 0805 pull-up** is a starting value for evaluation, not a selected MPN or validated operating value. For a nominal 3.3 V lumped RC bus, t10–90 ≈ 2.2RC:

| Assumed total bus C | 10–90% rise | Time to 0.7 VCC from 0 V |
|---:|---:|---:|
| 50 pF | 51.7 ns | 28.3 ns |
| 100 pF | 103.4 ns | 56.6 ns |
| 200 pF | 206.8 ns | 113.2 ns |

The 0.7 VCC threshold is an illustrative screen, not a verified SAM/STM32 threshold. At 3 Mbaud, one bit is 333 ns; at 6 Mbaud it is 167 ns. Receiver sample timing, threshold variation, falling-edge delay, parasitics and ringing reduce the apparent RC margin. These numbers do not establish either baud rate. Pull-up current while low is at most about 3.3/470 = 7.0 mA in this nominal ideal model; resistor dissipation is 23.2 mW. Use rail/resistor extremes and actual VOL for final sizing. A 1 kohm alternative halves current approximately but increases rise time by 2.13x. No resistor footprint alternatives are added by this comparison.

Measure/estimate all four receivers, all connected driver outputs, PCB traces, protection and probing capacitance. Verify the exact MCU RX input characteristics and allowed edge rates; add a Schmitt receiver only if required by that review. Provide local 100 nF bypass per populated buffer package, reconciling against B1-B036's auxiliary reserves (one already used by B1-B016). Four single gates may exceed the remaining reserve; no silent capacitance increase or power-budget saving is booked. Keep all circuit counts in B1-B008 until a topology is selected and the aggregate can be split accurately.

## Verification boundary

Datasheet characteristics and DigiKey listings were reviewed for candidate selection; RC values above are calculations. No exact CAD footprint validation, MCU errata sign-off, ERC/DRC, waveform capture or hardware test was performed. Keep B1-Q003/005/009 open. Accepted CAN PHYs, VCP isolation and debug UART ports are unchanged.

Additional requested candidate: [UMW SP3485EET review](sp3485eet_review.md). Not selected; exact-device documentation and receiver/power checks remain open.
