# MCU oscillator and programming/debug options

Status: mixed — debug access accepted by ADR-011; oscillator components proposed · Updated: 2026-09-06
Related: ADR-004/005; B1-R007/B1-R014/B1-R015; B1-Q004/005/008

USR-15 accepts the MCU selections. USR-16 / ADR-011 accepts the independent 10-pin Cortex SWD headers and records the owned J-Link EDU as the planned probe, with owned PICkit 5 available if needed. Other options remain proposals. No physical pads, exact oscillator/header/probe MPNs, footprints or clock trees are verified here. Procurement remains DigiKey-only; order codes and availability are TBD under B1-Q004/008.

## Oscillator recommendation

Evaluate **12 MHz passive main crystals, one per MCU**, first. This offers a possible common frequency with the FT232HL crystal proposal. Each device still has an independent crystal; common frequency does not guarantee one crystal MPN or identical load capacitors suits every oscillator. An **8 MHz crystal per MCU** is a reasonable alternative if electrical margin or sourcing is better. Both frequencies are inside the documented oscillator ranges; that alone does not qualify a component.

For the gateway, candidate arithmetic is 12 MHz / 3 x 84 / 2 = 168 MHz (or 8 MHz / 2 x 84 / 2). These are calculation examples, not validated PLL settings. Complete reference/VCO limits, operating mode, USART kernel routing and CAN clock review under B1-Q008. For the SAMs, derive core, SERCOM and CAN clocks jointly from XOSC through the appropriate clock paths and verify divisors against the chosen link rates; do not equate the FDPLL's name with an allowed CPU clock.

Prefer a crystal package with accessible solder joints and room for rework. Compare a leaded SMT crystal against larger ceramic SMT options; justify a leadless package if selected. Exact frequency, tolerance, temperature stability, aging, load capacitance, ESR and drive level remain TBD. Use C0G/NP0 load capacitors, in 0805 or 0603 where practical. Calculate loading including parasitics and check startup margin and drive; do not select generic 22 pF capacitors without the crystal specification. Keep the loop short and away from switched-power and bus signals.

Retain the accepted crystal architecture. Active oscillator modules or internal-RC-only operation would need a changed decision. No RTC/32.768 kHz crystal is required by the present scope.

## Debug connectors and power behavior

Use the accepted **four independent keyed 10-pin, 1.27 mm Cortex debug headers**, labeled GW/SAM0/SAM1/SAM2. Carry SWDIO, SWCLK, each MCU's reset, target-voltage reference and grounds using the standard connector assignment, to be checked against the chosen probe cable before assigning connector pins. Keep reset independent. Gateway SWO is an optional proposal pending mux review; do not assume SAM trace support. No shared SWD electrical bus or selector is proposed.

A larger 2.54 mm header is easier to handle but requires an explicitly documented adapter. A Tag-Connect-style footprint saves connector area but needs its matching cable and mechanical clearance; for this bench board, fitted headers are the first choice.

Target reference is a voltage-sense connection, not permission for the probe to power the board. Preserve USB-only operation and the switched main rail: check probe behavior with 3V3_SYS off to prevent debug-signal back-powering. Probe USB power alone does not establish target power. Verify connect-under-reset recovery and keep access to the individual reset nets. Select pulls and reset networks from each MCU's guidance. In particular, the SAM checklist calls for a SWCLK pull-up (33 kohm recommended); this must be accounted for during the pin/support-circuit pass.

## Flashing and probe options

Current plan: use the owned J-Link EDU. Verify its revision, software device support and cable/adapter; a standard 20-pin J-Link connector needs the matching Cortex adapter. PICkit 5 is owned fallback equipment, with exact SAM support/cable mapping still to verify. The following purchased-probe alternatives are historical options, not procurement requirements.

Use **SWD to erase/program internal flash, verify the image and debug each MCU** as the primary bring-up path. No external flash is proposed. One movable probe supports sequential work; concurrent debugging needs multiple probes and separate sessions.

- Vendor tools: STLINK-V3SET for STM32; Atmel-ICE for SAM. ST documents SWD/SWV and Cortex cable support; Microchip documents SAM programming/debugging through SWD. Confirm selected software/OS/device support and cable contents before purchase. Do not assume ST-LINK provides vendor-supported SAM programming.
- Common probe: evaluate a genuine SEGGER J-Link supported by both toolchains. SEGGER's published list includes device families; confirm the exact STM32G474RB and ATSAMC21G17A flash algorithms and selected probe/software combination before treating this as qualified.
- Gateway serial recovery: consider the STM32 system-memory bootloader only after checking AN2606 for the exact part, allowed UART pins and boot/option-byte entry configuration. The accepted FT232HL VCP connection is not automatically a working ROM-loader path.
- Later application firmware may support WS/UART/CAN updates. SAM bootloader installation, recovery behavior and flash-space allocation would be firmware work; do not assume an unprogrammed SAM can be flashed over its ring UART.

## Manufacturer evidence and limits

Reviewed 2026-09-06:

- [ST DS12288 Rev 6](https://www.st.com/resource/en/datasheet/stm32g474rb.pdf), pp. 1–2: HSE crystal range 4–48 MHz and debug capabilities. Full exact-package/errata review remains open.
- [Microchip DS60001479J](https://ww1.microchip.com/downloads/en/DeviceDoc/SAM-C20-C21-Family-Data-Sheet-DS60001479J.pdf), section 20.6.2, p. 191: 0.4–32 MHz crystal mode; schematic checklist p. 1182: SWCLK pull-up guidance. No package allocation verified.
- [ST AN2867](https://www.st.com/resource/en/application_note/an2867-guidelines-for-oscillator-design-on-stm8afals-and-stm32-mcusmpus-stmicroelectronics.pdf): crystal/loading/oscillator-design guidance; component-specific calculation pending.
- [STLINK-V3SET](https://www.st.com/en/development-tools/stlink-v3set.html): SWD/SWV, 3–3.6 V application voltage and cable interfaces.
- [Microchip Atmel-ICE overview](https://developerhelp.microchip.com/xwiki/bin/view/software-tools/programmers-and-debuggers/atmel-ice/): manufacturer-indexed excerpt supports SAM SWD programming/debugging; full-page retrieval timed out.
- [SEGGER supported devices](https://www.segger.com/supported-devices/jlink/): exact-device support qualification remains pending.
- [ST AN2606](https://www.st.com/resource/en/application_note/an2606-stm32microcontroller-system-memory-boot-mode-stmicroelectronics.pdf): follow-up reference only; PDF retrieval failed, so no exact bootloader interface/pin claim is made.

No bench or ERC/DRC checks were performed. Subsequent dated crystal stock/price checks are recorded in crystal_candidates.md. B1-Q004/005/008 remain open; final rates/electrical behavior also depend on B1-Q003.

Common 12 MHz component preference (USR-16): see [live DigiKey candidate research](crystal_candidates.md). No exact crystal has been selected.

J-Link cable reference: [SEGGER adapters](https://www.segger.com/products/debug-probes/j-link/accessories/adapters/overview/) documents conversion from standard 20-pin 0.1-inch to Cortex 10-pin 0.05-inch. Confirm the owned cable inventory before ordering.

Hand-assembly follow-up: prefer the leaded HC-49 SMT / through-hole candidates now documented in crystal_candidates.md over the earlier small ceramic candidates. Exact component selection and oscillator qualification remain open.

Current selection — USR-19 / [ADR-014](../../docs/decisions/014-smaller-12mhz-crystal.md): smaller common crystal selected for the four MCU oscillators; ADR-017 separately proposes an accurate FT232HL crystal; qualification remains B1-Q008; see BOM B1-B014/019/020. Earlier candidate/unselected statements are historical. Load networks and electrical/pad/footprint qualification remain open under B1-Q008/B1-Q005. Assembly: 0805 preferred, 0603 acceptable, no 0402 or smaller; smaller crystals may be considered if leaded.
