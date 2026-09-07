# TPS560430 Rev A passive design

Status: passive MPNs accepted by ADR-025; electrical qualification pending. Updated 2026-09-06. Authority: ADR-021 buck, ADR-022 input ramp, ADR-024 inverter. This is the current buck implementation note; Git retains older converter history.

## Circuit

USB_5V -> VIN5; VIN5 -> 10 uF || 100 nF -> GND2.
SW6 -> 12 uH -> 3V3_SYS; 3V3_SYS -> local 22 uF -> ground.
CB1 -> 100 nF -> SW6. FB3 -> quiet sense at local output-capacitor positive terminal.
EN4 <- MC74HC1G14DBVT1G, with accepted ERJ-6GEYJ473V 47 kohm to ground (ADR-030).
No external feedback divider for fixed X3F. No catch diode or external soft-start/compensation network.

## Accepted parts

| BOM item | Qty | MPN | Value / construction | DigiKey cut tape |
|---|---:|---|---|---|
| B028 | 1 | Bourns SRN6045TA-120M | 12 uH +/-20%; semi-shielded; 6 x 6 mm | 118-SRN6045TA-120MCT-ND |
| B029 | 1 | TDK C3216X7R1V106K160AC | 10 uF +/-10%, 35 V X7R, 1206 | 445-14799-1-ND |
| B030 | 1 | TDK C3225X7R1C226M250AC | 22 uF +/-20%, 16 V X7R, 1210 | 445-3955-1-ND |
| B031/B052 | 2 | KEMET C0805C104K5RACTU | 100 nF +/-10%, 50 V X7R, 0805 | 399-C0805C104K5RACTUCT-ND |

DigiKey listings accessed 2026-09-06; web-index inventory is not a live purchase guarantee. B029 35 V is a stock/derating choice for the 5 V rail, not approval to connect this branch directly to 24 V. B052 rating corrects the old >=10 V placeholder: TI recommends >=16 V. Inverter bypass uses the accepted bridge-domain KGM21NR71E104KT allocation B1-B061; do not add it to these buck rows.

## Sizing calculations

Design VIN 4.44–5.5 V; 3.3 V output. Current planning load 380.55 mA, device output ceiling 600 mA. USB permission remains 500 mA total input.

Ripple approximation: deltaI = 3.3*(1-3.3/VIN)/(L*f). At 5 V, 12 uH, 1.1 MHz: 85 mA p-p. At 5.5 V: 100 mA p-p. With L=-20% and f=0.935 MHz: 147 mA p-p, before further bias/temperature effects. Estimated peak at 600 mA load: 674 mA, below the 800 mA minimum high-side limit. This is a sizing screen, not a fault-current guarantee.

Bourns lists DCR 65 milliohm +/-20% (78 milliohm upper at 25 C), Irms 3 A typical and Isat 4 A typical at 30% inductance drop. Copper loss at 380.55 mA is about 11.4 mW using 78 milliohm including nominal ripple; at 600 mA about 28 mW. Hot DCR and core loss are additional. Generous current headroom also covers the regulator's 1.4 A maximum peak-current-limit specification; verify hot L and transient overshoot. Keep the semi-shielded inductor away from crystals and analog inputs.

The 10 uF input retains the 14.9 uF direct USB_5V capacitance budget and existing attachment-ramp estimate. Approximate input capacitor ripple current at 600 mA output and 5.5 V input is 294 mA RMS. Require >=2.2 uF effective local input C; retain the 100 nF at VIN/GND.

22 uF local + 12.41 uF distributed = 34.41 uF nominal main-rail C. The SC189 30 uF ceiling is obsolete. Require at least 10 uF effective local output C after bias, tolerance, temperature and aging. Exact DC-bias curve readout and combined corner bounds remain pending; do not treat the nominal 22 uF as guaranteed effective C. With 10 uF effective C and the 147 mA ripple screen, capacitive ripple is about 2 mV p-p before ESR/layout effects.

For a 0.2 A load step, TI's eight-cycle triangular-charge estimate gives about 86 mV deviation at 0.935 MHz and 10 uF effective C. This is a first-order estimate, not the total rail-error guarantee. Validate actual simultaneous MCU/PHY load steps and release. Nominal capacitor charging during a linear 10–90% rise in 1.8 ms is about 50.5 mA output (34.41 uF * 2.64 V / 1.8 ms), plus active loads and internal-core startup. Soft-start minimum is unspecified; do not call this a maximum.

## Layout / completion

Place input bypass at VIN/GND, bootstrap directly at CB/SW, and output capacitor beside inductor return. Keep SW copper compact; route FB away from SW/inductor. Review actual cap bias/ripple-heating curves and footprints, combined LC stability, startup and representative load steps. Measure full-load efficiency; the conservative USB budget breaks even near 70.7%, not 90%. No simulation or bench test has been performed.

## Sources

- [TI datasheet, Table 1 and sections 9.2.2.4–7](https://www.ti.com/lit/ds/symlink/tps560430.pdf).
- [TI confirms fixed-output FB connection](https://e2e.ti.com/support/power-management-group/power-management/f/power-management-forum/948634/tps560430-tps560430x3f-fb-pin-connection).
- [Bourns inductor datasheet](https://www.bourns.com/docs/product-datasheets/srn6045ta.pdf); [DigiKey](https://www.digikey.com/en/products/detail/bourns-inc/SRN6045TA-120M/7315033).
- [TDK input characterization](https://product.tdk.com/system/files/dam/doc/product/capacitor/ceramic/mlcc/charasheet/c3216x7r1v106k160ac.pdf); [DigiKey](https://www.digikey.com/en/products/detail/tdk-corporation/C3216X7R1V106K160AC/3952035).
- [TDK output characterization](https://product.tdk.com/system/files/dam/doc/product/capacitor/ceramic/mlcc/charasheet/c3225x7r1c226m250ac.pdf); [DigiKey](https://www.digikey.com/en/products/detail/tdk-corporation/C3225X7R1C226M250AC/1587497).
- [KEMET DigiKey listing](https://www.digikey.com/en/products/detail/kemet/C0805C104K5RACTU/411169).

Related current notes: [USB input](usb_input.md) and [distributed decoupling](decoupling.md).
