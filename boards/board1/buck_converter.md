Current update: ADR-024 selects MC74HC1G14DBVT1G. See [current TPS560430 passive proposal](buck_tps560430.md) and bom.csv for proposed passive MPNs; older converter sections are historical.

# Main 3.3 V buck proposal

Current authority: ADR-021 selects TPS560430X3FDBVR and total USB current <=500 mA as the efficiency criterion. SC189-specific converter/filter and 30 uF ceiling statements below are historical; MCU/transceiver decoupling remains. Input-switch simplification is under review, not yet qualified.

Current authority: ADR-010 selects SC189ZSKTRT and the revised sc189_decoupling.md allocation. This document retains historical evaluation/proposal context; earlier candidate or TPS62902 selection language does not control the current BOM.

Status: proposed · Updated: 2026-09-06 · ADR-008 · B1-R023 · B1-Q002/011 · USR-08


Assembly update USR-09 / ADR-009: this QFN proposal is held for package review and is not the default build choice. See [leaded shortlist](buck_leaded_shortlist.md). Its values and estimates remain a reference until a regulator is selected and qualified.

## Recommendation and qualification boundary

Use **TPS62902RPJR**, 2 A synchronous buck, at **1 MHz, automatic PFM/PWM**, with a **2.2 µH Coilcraft XGL4020-222MEC**. Regulate 3V3_SYS to 3.3 V using the internal divider. Keep the independent FTDI domain and upstream controlled main-power switch of ADR-001. One external STM32 RS-485 remains required by ADR-007/USR-07.

The user's 90% minimum converter-efficiency target is accepted as a requirement, not a measured result. Proposed qualification envelope: converter VIN 4.35–5.5 V; output load 100–600 mA; ambient 0–70°C after thermal equilibrium. This covers current planning loads of approximately 185–381 mA Rev A and 192–490 mA expanded, including GPIO reservation. The envelope and temperature range are proposals; no full industrial-temperature guarantee is implied. Startup, suspend, faults and near-zero load have separate requirements; percentage efficiency is not useful at zero output power.

Aim to qualify the converter itself at **at least 92%**, so the whole main-power branch can retain **at least 90%** from USB connector to the output capacitor, including input switch/protection losses. Neither threshold is guaranteed by TI's typical curves. The 2 A chip rating is design headroom, not permission to draw 2 A from USB or export it on headers.

## Evidence and alternatives

- TPS62902: TI SLVSFM1A, November 2023, Figure 8-11 (printed p25) shows approximately 95–96% typical at VIN=5 V, VOUT=3.3 V, 1 MHz, 2.2 µH and our 0.1–0.6 A range. Curve readout is approximate, not measured Board 1 data. The small 1.5 x 2 mm, 9-pin RPJ package needs reflow and a reviewed land pattern. [Datasheet](https://www.ti.com/lit/ds/symlink/tps62902.pdf), [exact orderable device](https://www.ti.com/product/TPS62902/part-details/TPS62902RPJR).
- TPS62160/TPS62162: Figure 12 of SLVSAM2E gives only about 92–93% typical near the present active load, less margin. TPS62160 offers easier VSSOP assembly but is not preferred for this efficiency objective. [Datasheet](https://www.ti.com/lit/ds/symlink/tps62160.pdf).
- SC189ZSKTRT (not owned; USR-11 correction): retain as an alternative for measurement. Earlier excerpt review did not establish a 90% floor; this proposal does not claim SC189 cannot meet it. No accepted SC189 MPN decision is being superseded.

## Proposed circuit

```text
USB-B VBUS -> input protection -> USB_5V -> controlled main switch -> 5V_SYS
                                   |                                  |
                                   +-> independent FTDI domain        +-> VIN, EN
                                                                          TPS62902
                                                              SW -> 2.2 uH -> 3V3_SYS
                                                              VOS <----------+ (Kelvin sense)
                                                              GND ----------- GND
```

Local component labels below are proposal identifiers, not assigned CAD references.

| Item | Proposed value / MPN | Connection and reason |
|---|---|---|
| U_BUCK | TPS62902RPJR | RPJ 9-pin VQFN-HR; pin table below |
| L_BUCK | XGL4020-222MEC, 2.2 µH ±20% | SW to 3V3_SYS; shielded, low DCR; 4 x 4 x 2.1 mm |
| C_IN | 10 µF 25 V X7R, C3216X7R1E106K160AB | VIN to GND at chip; **1206** per TDK, despite inconsistent size entry in TI Table 8-5 |
| C_HF | 100 nF, ≥10 V X7R, 0603, MPN TBD | Additional close VIN bypass |
| C_OUT | 2 x 22 µF 10 V X7S, C2012X7S1A226M125AC | Parallel at inductor output; 0805; final DC-bias/temperature/aging check pending |
| R_MODE | 61.9 kΩ 1%, 0603, ≤100 ppm/°C | MODE/S-CONF to GND: Table 7-1 option 13, VSET + 1 MHz + auto PFM/PWM + output discharge |
| R_VSET | 249 kΩ 1%, 0603, ≤100 ppm/°C | VSET to GND: Table 7-2 option 16, 3.3 V; open is also documented but populated resistor makes intent explicit |
| C_SS | 10 nF 5% C0G, 0603, MPN TBD | SS/TR to GND; roughly 3.25 ms typical soft start using Eq14, 0.8 V reference and 2.5 µA |
| R_PG | 100 kΩ, 0603, MPN TBD | PG pull-up to 3V3_SYS; about 33 µA while pulled low |

The XGL4020-222 has 19.5 mΩ typical / 21.5 mΩ maximum DCR at 25°C, and 4.4 A saturation rating at 20% inductance reduction. High current rating is chosen for low loss and fault margin, not output allocation. [Coilcraft](https://www.coilcraft.com/en-us/products/power/shielded-inductors/molded-inductor/xgl/xgl4020/xgl4020-222/). Capacitor sources: [input characteristic sheet](https://product.tdk.com/en/system/files/dam/doc/product/capacitor/ceramic/mlcc/charasheet/c3216x7r1e106k160ab_200122.pdf), [output part](https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C2012X7S1A226M125AC). Manufacturer part identities checked; no distributor stock or price commitment.

### Pin connections from TI Table 5-1

| Pin | Name | Proposed connection |
|---|---|---|
| 1 | PG | R_PG to 3V3_SYS; rail-valid observation / sequencing input |
| 2 | SW | L_BUCK only; keep copper small |
| 3 | VOS | Sense positive terminal of C_OUT, away from SW |
| 4 | GND | Solid common ground plane and local capacitor returns |
| 5 | EN | Direct to local switched VIN at C_IN; upstream default-off switch owns USB power control |
| 6 | VIN | 5V_SYS and C_IN/C_HF |
| 7 | MODE/S-CONF | R_MODE to GND; no extra capacitor or externally driven control |
| 8 | SS/TR | C_SS to GND |
| 9 | FB/VSET | R_VSET to GND; no feedback divider in this mode |

TI allows at most 30 pF on configuration pins; avoid test-pad/probe loading during strap readout. PG is not guaranteed low when VIN is absent. UART isolation must also be gated by the independent USB power permission and valid supplies, not PG alone. EN-to-VIN does not replace the upstream switch or guarantee USB inrush compliance. Active discharge is not reverse-current isolation; no external source may energize 3V3_SYS in this revision.

## Capacitors, ramp and layout

TI Table 8-3 recommends 2.2 µH / 22 µF at 1 MHz and supports 47 µF. Start with 44 µF nominal local output capacitance to allow for ceramic derating. Confirm effective local capacitance remains at least about 22 µF at 3.3 V across the proposed envelope; replace/increase package size if it does not. Include all distributed MCU/PHY capacitors when checking loop stability and startup. At 2.2 µH, approaching 100 µF enters a table entry requiring at least 10 mΩ ESR; do not blindly add low-ESR bulk capacitance.

At a 3.25 ms ramp, 100 µF total charges at about 102 mA on the output, in addition to live loads. Actual startup capacitance and minimum ramp time must be calculated with component tolerances and TI Equations 15–16. Hold reset/traffic inactive until the rail is valid. Keep C_IN and other main-domain capacitance behind the controlled switch; separately budget capacitance visible directly at USB attachment. C_SS controls output ramp, while the upstream switch controls its input capacitor charging.

Follow TI Figure 8-86 and EVM layout: tiny VIN/C_IN/GND switching loop, short SW-to-inductor route, ground plane, short quiet VOS and configuration routes, thermal vias as appropriate on VIN/GND copper. Place the buck away from MCU/FTDI crystals and USB routing. Check PFM ripple and EMI with the networking workload; forcing PWM would require a new efficiency qualification, not a free firmware change.

## Loss and USB budget

At 600 mA output, 5.5 V input, L=2.2 µH and 1 MHz, nominal ripple is about 0.60 A peak-to-peak. With L at -20%, it is about 0.75 A and the estimated peak is about 0.975 A. Switching frequency is typical, so this is sizing arithmetic, not a worst-case current bound; check actual frequency, inductance under bias/temperature, and current-limit fault operation.

A partial loss check uses TI maximum MOSFET resistances (111/40 mΩ for VIN>4 V) and approximately 27.5 mΩ hot inductor DCR at 95°C: conduction loss near 600 mA is around 50 mW. At 1.98 W output, the 92% total-loss allowance is 172 mW. Remaining switching/core/control losses must fit the balance. This supports feasibility but cannot prove the floor, particularly in PFM at lower loads; datasheet switching/core-loss maxima are not complete.

Propose a **100 mΩ maximum combined onboard input-path resistance**, including protection, switch and traces at temperature. At 500 mA total USB draw, conservatively reserve 50 mV before the buck: 4.5 V at USB-B becomes at least 4.45 V at VIN. With 92% buck efficiency the branch efficiency is at least 0.92 x 4.45/4.5 = 90.98%, before separately unbudgeted control current. The existing miscellaneous/bridge allowances must explicitly absorb such controls; avoid a high-resistance PTC or series Schottky consuming this allocation. Exact input protection/switch selection stays B1-Q002.

Using the existing conservative loads (including LEDs and 20 mA breakout reserve, 100 mA bridge allowance):

| Assumption | Rev A USB current | Expanded USB current |
|---|---:|---:|
| Historical sensitivity: 4.4 V / 85%, no explicit path loss | 436 mA | 532 mA |
| 4.5 V connector, 50 mV path drop, 90% buck | 414 mA | 504 mA |
| 4.5 V connector, 50 mV path drop, 92% buck qualification goal | 407 mA | 495 mA |

The 50 mV bound assumes current stays within 500 mA; the 504 mA row therefore indicates failure, not a self-consistent passing corner. Expanded Board 1 still has minimal margin and remains a later power-architecture problem. Rev A retains its RS-485 and approximately 93 mA estimated headroom at the proposed qualified corner. MCU/PHY workload assumptions remain estimates, not validated maxima.

Use 4.5 V at the USB-B connector for the full-load USB 2.0 boundary, with separate low-voltage enumeration and transient checks. The earlier 5.25 V upper figure came from the base specification; current USB-IF drop/droop testing specifies **5.5 V** maximum. Qualify the buck and review the entire USB input chain accordingly. [USB-IF drop/droop v1.4.1 Table 1](https://www.usb.org/sites/default/files/USB20_32_BC12_Drop_Droop_1_4_1.pdf), [base USB 2.0 §§7.2.1–7.2.2](https://edg.uchicago.edu/~tang/USB/usb_20.pdf).

## Acceptance work

1. Verify exact footprints, resistor strap tolerances, capacitor effective values and actual distributed capacitance; reconcile all package drawings and any errata before CAD approval.
2. Sweep VIN 4.35, 4.45, 4.5, 5.0 and 5.5 V and IOUT 100, 150, 200, 300, 400, 500 and 600 mA at proposed ambient 0, 25 and 70°C; include mode-transition regions. Use an independent bench supply for loads exceeding USB allowance.
3. Measure averaged input/output power with Kelvin voltage sensing and calibrated current measurements; include all converter support losses. Use measurement uncertainty in the lower efficiency bound. Test multiple boards/components; combine measurement with tolerance/temperature analysis. A room-temperature EVM result alone is not a production worst-case guarantee.
4. Require ≥92% converter efficiency for the proposed margin strategy, and ≥90% main-branch efficiency including input path. If only 90% converter passes, use the 414 mA Rev A estimate and resolve branch margin explicitly.
5. Check rail ripple/overshoot, representative load steps, startup/suspend/resume, discharge and isolation behavior. Validate complete USB current separately, including inrush, pre-enumeration and suspend.

No schematic, simulation, efficiency measurement or hardware qualification has been performed. B1-Q011 remains open; CAD/sourcing evidence remains unverified.

## USR-13 clarification

The maintainer requires efficiency at full networking load on USB; light-load efficiency is not a selection criterion. Earlier discussion of a 90% floor across 100–600 mA is historical and no longer controls selection. See boards/board1/sc189_decoupling.md (repository-relative) for the new candidate allocation. No converter or capacitor MPN is frozen.
