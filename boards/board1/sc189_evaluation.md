# SC189ZSKTRT evaluation

Current authority: ADR-010 selects SC189ZSKTRT and the revised sc189_decoupling.md allocation. This document retains historical evaluation/proposal context; earlier candidate or TPS62902 selection language does not control the current BOM.

Status: evaluation / proposed trial, not selected or qualified · 2026-09-06 · USR-10 · B1-Q002/011

## Assessment

SC189ZSKTRT is a credible Rev A trial candidate: exposed-lead SOT23-5, fixed 3.3 V, and sufficient input/output range. It does not establish the accepted 90% minimum-efficiency objective across the previously proposed 100–600 mA envelope. The package-specific typical curve already falls below 90% at lower loads. Keep the requirement unresolved; do not silently narrow it or book a 92% efficiency floor.

The screenshot supplied by the user is the MLPD-UT6 curve page. The full manufacturer datasheet includes a separate SOT23-5 page (printed p6). At VIN=5 V, 25°C and the reference 2.2 µH network, approximate visual readings are:

| 3.3 V output current | Typical SOT23 efficiency, approximate | Board relevance |
|---|---|---|
| 100 mA | Low/mid-80s percent | Lower end of proposed qualification range; below 90% |
| 185 mA | About 87–89% | Rev A listening estimate including breakout allowance |
| 280 mA | About 90–91% | Rev A nominal loaded estimate |
| 380 mA | About 91–92% | Rev A conservative load allowance |
| 500–600 mA | About 92% | Expanded load region |

These are rough curve readings, not measured results or guaranteed bounds. The 4 V curve is somewhat better than 5 V at light/moderate loads. It does not prove performance at 5.5 V, elevated temperature or process corners. SOT23 switch resistance is higher than the MLPD version; do not transfer the MLPD curve unchanged.

SC189 uses fixed-frequency PWM, without the TPS62902's automatic light-load PFM behavior. Its electrical table gives 7.5 mA typical no-load VIN current; this is consistent with declining light-load efficiency. This current is already represented in efficiency and must not be added again to a curve-based budget. Table shutdown current is 1 µA typical / 10 µA maximum; the headline below-1-µA wording is not a maximum guarantee.

## Proposed trial network

Use the existing controlled main-power switch and independent FTDI domain. SC189 pin mapping from the SOT23 column on printed p14:

| Pin | Function | Trial connection |
|---|---|---|
| 1 | VIN | Switched 5V_SYS; close 10 µF input ceramic plus 100 nF bypass |
| 2 | GND | Common ground, short input-capacitor return |
| 3 | EN | Tie to local switched VIN for initial trial; upstream control must default off |
| 4 | VOUT | Kelvin sense at 3.3 V output capacitor |
| 5 | LX | 2.2 µH inductor to 3V3_SYS |

Prefer 2.2 µH to the smallest 1 µH network: lower ripple and room to use a low-DCR shielded inductor. XGL4020-222MEC is a candidate already researched in buck_converter.md (21.5 mΩ max at 25°C); its core loss at 2.5 MHz and full fault-current suitability still require checking. It is not a Semtech-qualified substitution. Reducing reference DCR from 50 to about 22 mΩ saves only roughly 4 mW at 380 mA, plus a small ripple-current term. That is a few tenths of an efficiency point, not several points.

At 5.5 V input, 3.3 V output, 2 MHz minimum specified frequency and L=1.76 µH (-20%), ripple is approximately 0.375 A peak-to-peak, with 0.79 A peak at 600 mA load before further inductance/current/temperature tolerances. Check saturation against startup, faults and the full current-limit behavior, not just steady load.

For an isolated evaluation circuit, start from Semtech's 2.2 µH / 10 µF output reference, using 0805 or larger X7R/X5R parts and verifying effective capacitance. The datasheet requires at least 10 µF output for 2.2 µH and filter corner frequency below 100 kHz over tolerances/bias. The corner-frequency condition alone is not permission to go below the 10 µF recommendation. Input capacitance must remain at least 4.7 µF effective; 10 µF nominal is the starting point. Exact capacitor MPNs remain open.

## Main integration constraint: total output capacitance

Printed p19 says total output capacitance should not exceed 30 µF to avoid startup problems; 10–22 µF is the recommended typical range. Count all capacitance directly charged on 3V3_SYS: local buck capacitor, four MCU supply networks, eight CAN PHYs, RS-485, isolation and other logic. Examine both nominal/tolerance maximum and voltage-dependent capacitance during startup; DC-bias-reduced operating capacitance alone does not establish startup compatibility.

Do not carry over the TPS62902 proposal's 44 µF local output network: it exceeds this recommendation before distributed decoupling. The repository has no finalized decoupling BOM, so compatibility is currently unknown. Do not reduce required MCU/PHY decoupling to force a fit. If the required rail capacitance exceeds the limit, prefer another regulator or obtain manufacturer-supported validation rather than silently exceeding the recommendation.

Internal soft start is nominally 100 µs, using stepped current limits; no external soft-start timing pin exists. It is not equivalent to the previously proposed 3.25 ms TPS62902 ramp. The main input switch's controlled rise does not automatically guarantee the output inrush profile. For scale only, charging 30 µF through 3.3 V in 100 µs corresponds to 0.99 A average capacitor current; actual ramp follows the chip's current-limit sequence. Measure USB input inrush and keep MCUs/traffic inactive during startup.

No PG output is available. Main-rail-valid detection/reset/isolation needs a separate reviewed implementation. During shutdown, ensure externally driven lines cannot back-power the main rail, and review VIN/VOUT sequencing against VOUT absolute maximum VIN+0.3 V. No external main-rail power source is included.

## Power implications and decision

At representative operating points, calculated total converter loss is only about 80–120 mW (185 mA at assumed 88%, 280 mA at 90%, 380 mA at 91.5%). These use approximate typical efficiencies; they are not maximum thermal dissipation. Package thermal resistance is 90°C/W on Semtech's specified board, so heating is unlikely to be the principal problem at these loads, but verify on our layout.

The previous 4.5 V USB / 50 mV path-drop calculation gives about 414 mA total Rev A input if the converter achieves 90% at the conservative load. At 88%, it is about 421 mA. These are sensitivity calculations, not SC189 guarantees, and keep all other load allowances unchanged. Falling below 90% at light load does not inherently break the 500 mA USB budget, but it fails a literal 90% floor across that range. Efficiency qualification and total-board USB compliance are separate checks.

Recommendation: consider SC189 for a small evaluation build, conditional on the 30 µF rail-capacitance audit. Test 100, 185, 280, 380, 500 and 600 mA at 4.35, 4.45, 5.0 and 5.5 V, then temperature corners. Record efficiency, output regulation/ripple, load steps, startup current and shutdown behavior. The earlier 0–70°C test envelope remains proposed. Do not freeze SC189 or revise the 90% requirement based solely on these curves.

## Sources and evidence limits

- [Semtech product page](https://www.semtech.com/products/power-management/buck-converters/sc189): package, input range and family overview; currently lists a 2018-12-04 datasheet entry.
- [Semtech datasheet, manufacturer document mirrored by KST](https://www.kstmicro.com/wp-content/uploads/2025/03/SC189ZSKTRT.pdf): August 27, 2010 cover; printed pp2–4 limits, p6 SOT23 plots, p14 pin functions, pp17–20 soft start and passive constraints. A readable [second mirror](https://www.zenkaeurope.com/assets/datasheet/SC189ZSKTRT.pdf) was used to inspect p6 visually. Direct manufacturer download did not yield a PDF; reconcile current revision/errata before CAD sign-off.
- User screenshot: MLPD typical curves; reference evidence, not an instruction or selection approval.

No schematic, bench measurement, procurement check or hardware qualification was performed in this evaluation. The TPS62902 reference remains on package hold; no BOM substitution is made by this assessment.

## USR-13 clarification

The maintainer requires efficiency at full networking load on USB; light-load efficiency is not a selection criterion. Earlier discussion of a 90% floor across 100–600 mA is historical and no longer controls selection. See boards/board1/sc189_decoupling.md (repository-relative) for the new candidate allocation. No converter or capacitor MPN is frozen.
