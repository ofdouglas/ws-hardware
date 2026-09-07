# RS-485 idle-bus bias

2026-09-06; B1-Q009 / B1-B023. Network/value accepted USR-30 / ADR-036; exact CRGP0805F330R MPN (330 ohm, 1%, 0805, 1/3 W) accepted USR-33 / ADR-039. ST3485EBDR and termination remain accepted ADR-034/035. B1-B071 now holds the accepted bias pair; footprint and electrical qualification remain open.

## Accepted circuit

ST3485EBDR requires A-B >= +200 mV for guaranteed receiver high. Its floating-input guarantee does not cover the two 120 ohm terminations pulling A-B toward zero when both drivers release. UART idle should be high. Accepted network, at Board 1 only: 3V3_SYS -> 330 ohm 1% -> A (pin 6), and B (pin 7) -> 330 ohm 1% -> GND. Keep the accepted local 120 ohm across A/B and the remote endpoint termination. Use the two selected CRGP0805F330R in B1-B071. A pull-up on RO alone cannot fix an enabled receiver driving the wrong state. A/B naming varies between vendors; wire by actual non-inverting/inverting pin function.

Source: [ST DS2947 Rev12, March 2021, pp.2–6](https://www.st.com/resource/en/datasheet/st3485eb.pdf). The 70 mV typical hysteresis is not guaranteed noise margin at zero differential. [TI SLYT324, Passive failsafe for an idle bus](https://www.ti.com/lit/an/slyt324/slyt324.pdf) explains the termination/loading tradeoff; this network retains the already accepted 120 ohm components rather than silently changing them.

## Calculation and limitations

Initial lumped DC model: two 120 ohm endpoint resistors give RT=60 ohm; equal bias resistors R give VAB=VCC*RT/(2R+RT), and idle rail current I=VCC/(2R+RT). This first screen excludes cable resistance, receiver input currents, protection leakage and rail/ground offsets. The tolerance column uses VCC=3.0 V (device operating floor), both terminations -1%, both bias resistors +1%. The remote termination tolerance is not yet verified.

| R per leg | Nominal VAB, 3.3 V | Tolerance-screen VAB | Nominal idle rail current |
|---|---:|---:|---:|
| 680 ohm | 139 mV | 124 mV | 2.32 mA |
| 470 ohm | 198 mV | 177 mV | 3.30 mA |
| 390 ohm | 236 mV | 210 mV | 3.93 mA |
| 330 ohm | 275 mV | 245 mV | 4.58 mA |

470/680 ohm do not meet the +200 mV threshold with both terminators. 390 ohm leaves little tolerance-screen margin. The accepted 330 ohm 1% pair gives about 45 mV remains at the stated corner, before other error sources. This is not a guaranteed all-corners design. A 1 mA adverse differential current through approximately 55 ohm could consume 55 mV; quantify actual receiver/protection leakage rather than dismissing it. Include remote resistor tolerance and voltage drop along the cable when checking the remote end.

Bias adds loading: nominal small-signal differential load becomes 120 || 120 || 660 = 55 ohm before receiver loads. At the biased cable endpoint, 120 || 660 = 101.5 ohm, with approximately -8.3% reflection coefficient against a 120 ohm cable. ST specifies driven output against 54 ohm, but passive equivalent resistance alone is insufficient: bias also opposes the driven-low state. At VAB=-1.5 V and 3.3 V supply the bias branch carries (3.3+1.5)/660 = 7.27 mA opposing the driver, in addition to 25 mA through the terminations. Confirm both transmit polarities, signal amplitude, cable reflections and common mode using exact device models and bench measurements. Do not claim compliance from this screening calculation.

At nominal idle, each 330 ohm resistor dissipates about 6.9 mW; worst driven/fault conditions govern final rating. The 4.58 mA is on the 3.3 V rail, not directly USB current. Explicitly reconcile it and the active-driver bias current with the existing 60/75 mA planning allowances under B1-Q002/009; do not add the entire termination load twice or claim savings. No power-budget maximum has been validated.

## Remote ConnectCore 93 evidence

The published [Digi 3001753x-03_A schematic, sheet 7, variant 55002179-01 Rev3P](https://hub.digi.com/dp/path=/support/asset/connectcore-91-and-93-dvk-schematics-pdf---3001753x-03_a/) text identifies U31 as LTC2862IS8-2#PBF, R236 as 120 ohm and J49 as a two-pin header. The [Digi connector reference](https://docs.digi.com/resources/documentation/digidocs/90002550/reference/devboard/r_connectors.htm) identifies J49 as the RS485 termination jumper. Exact owned-board revision and fitted population are unverified. PDF text was inspected; schematic screenshot retrieval failed, so no visual connectivity/absence-of-bias verification is claimed.

The [Analog Devices LTC2862 selection table](https://www.analog.com/en/products/LTC2862.html) rates the -2 version at 250 kbit/s; the -1 version is 20 Mbit/s. If the kit matches this published population, the link must run at a rate supported by its 250 kbit/s PHY (115200 baud is a sensible initial test), despite Board 1's 12 Mbit/s ceiling. The remote receiver's built-in fail-safe does not itself bias Board 1's receiver. Inspect the actual kit revision, termination setting, connector polarity and any external bias before enabling a Board 1 bias network. Avoid redundant or opposing bias networks.

## Remaining checks

The single Board 1 330 ohm 1% pair is accepted ADR-036; the leakage/loading and endpoint checks above remain qualification work. No extra bias jumper is selected or authorized. Keep DE low during reset and idle; choose /RE shutdown/receive defaults independently. Check the remote-powered/local-unpowered case: a pull-up to switched 3V3_SYS creates a possible backfeed path, which the transceiver's own power-off behavior does not eliminate. Resolve that path within the existing power-state contract before implementing.

B1-Q009 remains open for remote hardware identification, bias ownership, worst-case leakage/temperature, driver loading, cable/common-mode and power-off behavior. Verify idle A-B and RO, both transmit polarities and frame turnaround with both terminations fitted. Exact bias MPNs are accepted ADR-039; no schematic, ERC/DRC or bench validation was performed.

[Current interfaces/protection](interfaces.md) records the selected ESDS452DBZR and restricted operating envelope; [termination](termination.md) records the accepted endpoint parts. Transient compatibility and added bus capacitance remain B1-Q009 checks.

## Selected resistor stress screen

CRGP0805F330R is 1/3 W. At VCC=3.6 V and A=-5.5 V, the ideal pull-up stress is (3.6+5.5)^2/(330*0.99)=0.2535 W. This is below nameplate power but requires thermal derating and does not qualify pulse/fault exposure. [TE exact-part evidence](https://www.te.com/en/product-1-2176327-9.html) is retained; B1-Q009 remains open.
