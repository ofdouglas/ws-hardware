Current update: ADR-029 accepts the three LED/VBUS candidates reviewed below. Prior candidate discussions are historical. B046 is now 4.7 uF 50 V X5R; B047 is 1 ohm +/-5%. See [remaining parts](remaining_parts.md) for current decision status.

Current SAM-core update: ADR-026 selects ceramic X7R for B040; the tantalum-only restriction is removed. ADR-027 accepts CL21B105KAFNFNE; effective-C and regulator qualification remain pending.

# Board 1 passive selection review

Updated: 2026-09-06. Authority: bom.csv and accepted ADRs, especially ADR-025. Selection and qualification are separate. Counts below are allocation counts, not a completed schematic placement audit. No stock refresh or new component substitutions were performed in this review.

## Exact MPNs accepted

| IDs | Qty | Part | Function |
|---|---:|---|---|
| B028 | 1 | SRN6045TA-120M | 12 uH buck inductor |
| B029 | 1 | C3216X7R1V106K160AC | 10 uF 35 V X7R 1206 buck input |
| B030 | 1 | C3225X7R1C226M250AC | 22 uF 16 V X7R 1210 buck output |
| B031, B052 | 2 | C0805C104K5RACTU | 100 nF 50 V X7R 0805 input HF and bootstrap |
| B019, B020 | 4 | ECS-120-20-3X-EN-TR | Four separate 12 MHz MCU crystals; load caps decided ADR-031 |

The FTDI crystal B014 ECS-120-18-5PX-CKM-TR is decided by ADR-030. SMF6.0A and RCLAMP0504S.TCT are selected protection semiconductors, not additional R/L/C selections.

## Ceramic MPNs accepted by ADR-027

| IDs | MPN | Value/rating |
|---|---|---|
| B036, B041; bridge bypass | KGM21NR71E104KT | 100 nF 25 V |
| B037, B040, B045; bridge 1 uF | CL21B105KAFNFNE | 1 uF 25 V |
| B038; FTDI bulk | GRM21BR71C475KE51L | 4.7 uF 16 V |
| B039; FTDI reset | CL21B103KBANNNC | 10 nF 50 V |
| B048 | CL21B473KBCNNNC | 47 nF 50 V |

All are 0805 X7R +/-10%. Retain ADR-025 buck parts. ADR-029 decides CL21A475KBQNNNE (4.7 uF / 50 V X5R) for B046 and SG73P2BTTD1R0J for B047. ADR-028 decides RMCF0805FT10K0 for B051/B054 and EEPROM pull-up B065. The 16 V Murata part is not a raw-VBUS substitute. B036 includes the SN74LV125 bypass reserve. Core-rail capacitors are separate from main-rail output C. No quantity changes; bridge enumeration and effective-C qualification remain open.

## Values proposed or networks not finished

| IDs | Existing direction | Work remaining |
|---|---|---|
| B054, B055 | Decided RMCF0805FT10K0 / ERJ-6GEYJ473V | Startup/leakage verification remains; ADR-028/030 |
| B017 / B061–065 | Bridge residual support / decided MPN allocations | B061–064 own accepted capacitor MPNs; B065 owns EEPROM pull-up. B056–058 own DO series/REF/crystal capacitors. Enumerate remaining capacitor rails/counts and residual networks without duplicates. |
| B042/B043/B058 | Decided 33 pF MCU and 27 pF FTDI C0G capacitors | ADR-031; oscillator loading, drive and startup qualification remain; additional drive-limit resistors only if required |
| B007 | CAN termination/protection | Termination arrangement, resistor values/ratings, any split capacitors and population options |
| B023 | RS-485 termination/protection/control | Termination, bias if needed, control pulls and protection components |
| B008 | Onboard multidrop UART network | Drive topology, pull-ups/series resistors, rise-time/loading checks |
| B010, B053 | MCU reset/boot/SWD and CBUS recovery | Pulls, reset capacitors and power-off-safe interface passives |
| B026 | Five provisional RK73H2ATTD3301F LED resistors | Exact LED is decided; resistor MPN still needs selection and current/visibility qualification |
| B016 support | UART isolation defaults | /OE and signal default/series networks; supply bypass already reserved in B036 |
| Connector/shield | USB shell grounding | Direct/RC connection and any associated passives still unresolved |

## Review findings and next work

1. All five local buck passives now have accepted exact MPNs. Bootstrap is 50 V, satisfying the previously corrected >=16 V requirement. No additional buck feedback-divider, mode, PG or soft-start passives are needed.
2. Historical TPS62902 B032–B035 and removed supervisor B049/B050 remain zero-quantity/superseded. They are not pending purchases. SC189 network references in historical documents do not control the current design.
3. Local output C has +/-20% tolerance, unlike the earlier +/-10% allocation. Main-rail C remains 34.61 uF nominal. A simple positive tolerance/temperature screen is 22*1.20*1.15 + 12.61*1.10*1.15 = 46.31165 uF, not the old uniform-10% bound. This is a screen, not a full capacitance/startup guarantee; effective minimum capacitance still requires bias/temperature/aging data. No 30 uF limit applies.
4. The main procurement/design priorities are selected SAM core capacitor qualification, B047 damping pulse capability, then complete the bridge/control enumeration. B046 and oscillator capacitors are decided; termination passives still require circuit decisions.
5. The 1 uF SAM bulk and shared STM32 analog bulk are already accepted engineering departures documented in ADR-010, with local transient/placement verification still required. No silent return to larger example values is made by this review.

No schematic, procurement, bench testing or full electrical qualification is claimed. Counts and unique IDs were checked against the BOM.

## Resistor review — accepted pull-up and historical damping alternative

- **RMCF0805FT10K0**: accepted ADR-028. Stackpole 10 kohm +/-1%, 0805, 0.125 W. Recommended for the FTDI RESET# and PWREN# pull-ups, and EEPROM 10 kohm pull-up. At 3.3 V held low, dissipation is only 1.089 mW and current 330 uA. Does not replace the 47 kohm EN pull-down or 12 kohm REF resistor. [Manufacturer series datasheet](https://www.seielect.com/Catalog/SEI-RMCF_RMCP.pdf); [DigiKey exact part](https://www.digikey.com/en/products/detail/stackpole-electronics-inc/RMCF0805FT10K0/1942435).
- **RL1632R-1R00-F**: Susumu 1 ohm +/-1%, 1206, 0.5 W. Historical unselected B047 alternative; ADR-029 selects SG73P2BTTD1R0J instead. The damping branch is not in the board DC path. An ideal 5.5 V step into 1 ohm + 4.7 uF gives initial 30.25 W, RC time constant 4.7 us, and total resistor energy 71.09 uJ; 4.7 uF * 1.10 * 1.15 gives 89.93 uJ. These are calculated RC screens, not measured cable-ringing/ESD bounds. Continuous 0.5 W alone does not qualify that pulse. The published graph is labeled RL1632-R050 (50 milliohm), with durations starting at 1 ms; it does not directly qualify this 1 ohm part at microsecond durations. Obtain applicable manufacturer pulse data or validate repeated hot-plug resistance drift and waveform before marking verified. [Manufacturer RL datasheet, p.2](https://www.susumu.co.jp/common/pdf/n_catalog_partition08_en.pdf); [DigiKey exact part](https://www.digikey.com/en/products/detail/susumu/RL1632R-1R00-F/714366).

No live stock guarantee or hardware test is claimed. Remaining work belongs to B1-Q002/011.

## LED and VBUS selections reviewed 2026-09-06

ADR-029 accepts the three exact MPNs below. The analysis records their selection rationale and remaining electrical checks; earlier candidate alternatives remain research history.

| Candidate | Assessment |
|---|---|
| CSL1901DW1 | Recommended low-current orange indicator. ROHM specifies 1.8 V typical and 9.4 mcd typical at 2 mA. Body 1.6 x 0.8 x 0.55 mm (0603), allowed but smaller than preferred 0805. Start with about 3.0–3.3 kohm series resistance for approximately 0.5 mA from 3.3 V, then check visibility. The 2 mA Vf/brightness limits do not guarantee 0.5 mA behavior; GPIO drop and actual low-current Vf affect current. Five at nominal 0.5 mA preserve the 2.5 mA LED budget; driving all at 2 mA would add 7.5 mA to main-rail load. |
| CL21A475KBQNNNE | Recommended for B046: 4.7 uF +/-10%, 50 V, X5R, 0805. Exceeds the prior 25 V rating requirement. ADR-029 accepts X5R in place of X7R: +/-15% temperature characteristic over -55 to +85 C, appropriate for a room-temperature bench board subject to local temperature validation. Not an unconditional X7R substitute. Check effective capacitance at 5–5.5 V from bias/aging data; 50 V rating alone does not establish it. Existing positive C bound 4.7 * 1.10 * 1.15 = 5.9455 uF remains the same within X5R temperature range. |
| SG73P2BTTD1R0J | Preferred damping candidate over the current-sense Susumu part: purpose-designed anti-surge pulse thick film, 1 ohm +/-5%, 1206. Current KOA sheet (04/16/26) rates 2B at 1 W; use applicable terminal-temperature derating. ADR-029 accepts relaxation from 1% to 5%, which is reasonable for RC damping; no precision function depends on it. At 5.5 V and Rmin=0.95 ohm, initial ideal-step power 31.84 W; upper capacitance 5.9455 uF gives 89.93 uJ, independent of R. RC range from resistor tolerance alone is 4.465–4.935 us at nominal C. KOA publishes a 2B one-pulse curve extending to 0.001 ms (1 us), more relevant than the previously reviewed Susumu curve. Numerical curve margin and repeated hot-plug/ringing qualification remain open; continuous power rating alone is not pulse sign-off. |

Primary sources: [ROHM LED](https://www.rohm.com/products/led/chip-leds-mono-color-type/standard/csl1901dw-product), [Samsung capacitor](https://product.samsungsem.com/mlcc/CL21A475KBQNNN.do), [KOA SG73P, pp.1–2](https://www.koaspeer.com/pdfs/SG73P.pdf).
DigiKey listings: [LED](https://www.digikey.com/en/products/detail/rohm-semiconductor/CSL1901DW1/16685592), [capacitor](https://www.digikey.com/en/products/detail/samsung-electro-mechanics/CL21A475KBQNNNE/3886906), [resistor](https://www.digikey.com/en/products/detail/koa-speer-electronics-inc/SG73P2BTTD1R0J/10192656). Stock must be refreshed at purchase. No hardware tests performed.

RK73H2ATTD3301F is recommended for B026: 3.3 kohm +/-1%, 0805, 0.25 W. At assumed Vf=1.8 V: (3.3-1.8)/3300 = 0.455 mA, resistor power 0.682 mW. Low-current Vf and GPIO drop affect actual current; verify brightness. Exact part remains proposed. Manufacturer: https://www.koaspeer.com/catimages/Products/RK73H/RK73H.pdf .
