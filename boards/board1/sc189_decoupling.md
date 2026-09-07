Current SAM-core update: ADR-026 selects ceramic X7R for B040; the tantalum-only restriction is removed. ADR-027 accepts CL21B105KAFNFNE; effective-C and regulator qualification remain pending.

# SC189 Rev A decoupling proposal

Current authority: ADR-021 selects TPS560430X3FDBVR and total USB current <=500 mA as the efficiency criterion. SC189-specific converter/filter and 30 uF ceiling statements below are historical; MCU/transceiver decoupling remains. Input-switch simplification is under review, not yet qualified.

Status: selected design direction under ADR-010; no schematic or component qualification. Date: 2026-09-06. Basis: USR-13; B1-Q002/B1-Q011.

Efficiency is required at full networking load on USB, not at light load. SC189 is selected; capacitance, startup and full-load qualification remain pending. Future 48 W shared 24 V input does not impose the same efficiency priority.

## Direct 3V3_SYS capacitance allocation

| Group | Proposed allocation | Nominal uF |
|---|---|---:|
| SC189 local output | 10 uF, 1206 or larger X7R, 10% tolerance; 2.2 uH inductor reference | 10.00 |
| STM32 VDD | 4.7 uF plus allowance for four 100 nF pin capacitors | 5.10 |
| STM32 VDDA/VREF+ directly joined, VREFBUF disabled/high-Z | Shared 1 uF bulk; 10 nF at VDDA and 100 nF at VREF+ | 1.11 |
| STM32 VBAT tied to 3V3_SYS | 100 nF | 0.10 |
| Three SAM C21s | Each: 1 uF local bulk plus allowance for four 100 nF supply-pin capacitors | 4.20 |
| Eight TCAN3413 | Each: 100 nF at VCC and 100 nF at VIO | 1.60 |
| One THVD1420 candidate | 100 nF at VCC | 0.10 |
| Main-domain auxiliary logic | Reserve four 100 nF capacitors; reconcile exact isolation/control parts | 0.40 |
| Total | Includes allocation reserves, not finalized pin counts | 22.61 |

Use <=10% initial tolerance. An upper envelope of nominal x 1.10 x 1.15 (X7R positive temperature bound) gives 28.60165 uF, leaving approximately 1.40 uF below 30 uF. This is a capacitor-allocation bound, not a measured rail: unlisted capacitors, manufacturing specifications and effective capacitance must be reconciled. Do not subtract DC-bias loss to make the maximum pass. No extra external 3.3 V bulk capacitor is authorized on breakouts.

The local buck capacitor must be selected using manufacturer bias/temperature data, not just its printed 10 uF value. Verify the Semtech effective-capacitance/filter constraints with the actual 2.2 uH inductor across tolerances; do not count remote capacitors as interchangeable with the local high-frequency output capacitor. The exact DigiKey MPN is pending. If local capacitance must increase, reallocate within the same upper bound before approval.

## SAM regulator capacitors and explicit engineering departure

For each VDDCORE output, use 1 uF X7R ceramic per ADR-026 (effective-C qualification pending; ESR <=0.5 ohm screen) in parallel with 100 nF X7R. These are separate 1.2 V internal-regulator outputs, never tied to 3V3_SYS or each other. They are not direct SC189 output capacitance, but their charging current must be included in startup validation. Exact capacitor MPN/ESR review remains open.

Microchip Table 53-1 lists 10 uF bulk capacitors and explicitly labels these values typical examples. Our 1 uF local bulk plus shared rail capacitance is an engineering proposal departing from that example, not a claim of manufacturer validation. Retain 100 nF at every VDDIN/VDDIO/VDDANA supply pair. Audit exact package counts before CAD. Check local voltage during simultaneous MCU/PHY activity; do not reduce mandatory decoupling to preserve SC189.

## Layout and validation

Use a solid ground plane and low-impedance 3.3 V distribution. Put each pin capacitor at its supply/ground pair; place STM32 bulk nearby. Put the SC189 local capacitor next to inductor return/sense; follow its hot-loop layout guidance. Start with direct analog-rail feeds; ferrite beads do not remove downstream capacitance from the startup budget.

FTDI/EEPROM independent-domain capacitors and SC189 input capacitors are outside this output budget, but remain in USB inrush accounting. Crystal, reset and CAN split-termination capacitors are not direct rail-to-ground output capacitors; account any appreciable startup current separately. Keep main load inactive during ramp; test startup, USB input peak current, ripple and simultaneous bus load steps at low VBUS and temperature corners. This allocation establishes feasibility, not stability, EMC or USB compliance.

## Sources

- ST DS12288 Rev6 Figure16: https://www.st.com/resource/en/datasheet/stm32g474rb.pdf
- Microchip DS60001479J Table45-21, Figure53-1 and Table53-1: https://ww1.microchip.com/downloads/en/DeviceDoc/SAM-C20-C21-Family-Data-Sheet-DS60001479J.pdf
- TI TCAN341x section8.4: https://www.ti.com/lit/ds/symlink/tcan3413.pdf
- TI THVD1420 section9: https://www.ti.com/lit/ds/symlink/thvd1420.pdf
- Semtech source/limitations: [SC189 evaluation](sc189_evaluation.md).

USR-14 accepts this direction: shared analog bulk is an engineering departure from separate ST decoupling networks; place adjacent to both directly joined pins and validate. The local buck remains 10 uF, not two 4.7 uF. Exact MPNs and validation remain open.
