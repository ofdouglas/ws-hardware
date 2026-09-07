# Board 1 decoupling allocation

Status: accepted parts/allocation; capacitor corners and implementation unverified. Authority: surviving MCU allocation in ADR-010; converter/filter ADR-021/025; ceramic SAM core ADR-026 (`026-sam-core-ceramic.md`); MPNs ADR-027. [CSV](bom.csv) owns quantities. [Buck note](buck_tps560430.md) owns the local converter network.

## Main 3.3 V rail

| BOM | Qty | Allocation | Selected capacitor |
|---|---:|---|---|
| B1-B036 | 37 | 100 nF bypass: STM32 6, SAMs 12, CAN VCC/VIO 16, RS-485 1, VCP/UART_MD 2 | KGM21NR71E104KT, 25 V X7R, 0805 |
| B1-B037 | 4 | 1 uF: shared STM32 VDDA/VREF+ bulk and one per SAM | CL21B105KAFNFNE, 25 V X7R, 0805 |
| B1-B038 | 1 | STM32 digital bulk, 4.7 uF | GRM21BR71C475KE51L, 16 V X7R, 0805 |
| B1-B039 | 1 | STM32 VDDA 10 nF | CL21B103KBANNNC, 50 V X7R, 0805 |
| B1-B030 | 1 | Buck-local output, 22 uF | C3225X7R1C226M250AC, 16 V X7R, 1210 |

STM32 six bypass positions cover four VDD, VREF+ and VBAT. VDDA/VREF+ share the selected 1 uF with direct rail connection; disable VREFBUF/high impedance. This is an accepted allocation departure from separate analog bulk examples and requires placement/analog-supply validation. Each SAM's 1 uF local bulk also departs from the manufacturer's typical 10 uF example (Figure 53-1/Table 53-1); qualify load steps rather than claiming the example mandates this allocation.

Capture assigns one bypass to each VCP/UART_MD buffer. The two unused auxiliary planning reserves were removed, yielding37 actual placements, with no unneeded footprints. Reset filter capacitors B081/B082 are separate from main supply bypass.

Nominal direct main-rail C = 37*0.1 + 4*1 + 4.7 + 0.01 + 22 = **34.41 uF**. Positive tolerance/temperature screen = 22*1.20*1.15 + 12.41*1.10*1.15 = **46.05865 uF**. These are not measured effective-capacitance bounds. The superseded SC189 30 uF limit does not apply to TPS560430; qualify its combined local/distributed network instead.

## Separate SAM core rails

Each SAM VDDCORE has one CL21B105KAFNFNE 1 uF (B1-B040, three total) and one KGM21NR71E104KT 100 nF (B1-B041, three total). These are separate internal regulator outputs near 1.23 V: never connect them to 3V3_SYS or to each other. They are excluded from direct main-rail capacitance but included in startup-load review.

The ceramic selection is explicit maintainer acceptance, not proof of datasheet equivalence. SAMC21 DS60001479J Table 45-21 (p.1038) lists 0.8/1/1.2 uF with tantalum/electrolytic wording and separate 100 nF X7R. Retain the effective-C check at 1.23 V across tolerance, temperature and aging, the <=0.5 ohm ESR screen, and regulator startup/stability qualification. The primary references below retain the source evidence; Git retains the earlier analysis.

## Other domains and layout

USB input capacitors are in [usb_input.md](usb_input.md), bridge allocations in [usb_vcp.md](usb_vcp.md). Buck input and bootstrap capacitors are separate from output C; bootstrap connects CB to SW, not ground. Bridge B1-B061/062/063 counts are11/0/2 and do not duplicate main or core capacitors.

Place bypass at each supply pin with short return to the ground plane and bulk near its load. No added ferrite or external bulk is implied. Validate actual pin count/rail allocation, effective capacitance, regulator stability, load steps, startup charging and rail noise under B1-Q002/005/011. No hardware validation is claimed.

## Retained primary references

[ST DS12288 Rev6 Figure 16](https://www.st.com/resource/en/datasheet/stm32g474rb.pdf), [Microchip DS60001479J Table 45-21 and Figure/Table 53-1](https://ww1.microchip.com/downloads/en/DeviceDoc/SAM-C20-C21-Family-Data-Sheet-DS60001479J.pdf), and [TCAN341x supply guidance section 8.4](https://www.ti.com/lit/ds/symlink/tcan3413.pdf) support the allocation review. Retain a bypass at every applicable SAM VDDIN/VDDIO/VDDANA supply pair; reconcile exact package counts before capture. Main-rail ramp/load-step checks include internal-core charging. No extra external breakout bulk is authorized.
