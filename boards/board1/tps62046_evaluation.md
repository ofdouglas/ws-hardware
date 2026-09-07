# TPS62046DGQR evaluation

Status: candidate assessment, not selected or qualified · USR-11 · B1-Q002/011 · ADR-009 applies

## Assessment

Promising compromise between efficiency and manual assembly. TPS62046 is fixed 3.3 V, accepts 2.5–6 V input, supports up to 1.2 A and uses 1.25 MHz switching with selectable automatic power-save operation. Tie MODE low for the initial efficiency evaluation. Figure 1 shows roughly mid-90s typical efficiency around 100–600 mA at VIN=5 V, VOUT=3.3 V with power save enabled; visual readings are approximate. This gives more apparent margin than SC189, especially at low load, but does not prove a 90% worst-case floor.

Source: [TI SLVS463B, October 2005](https://www.ti.com/lit/ds/symlink/tps62046.pdf), pp2–4 electrical/package details, p6 Figure1, pp13–16 application/layout. [Exact part status](https://www.ti.com/quality-reliability-packaging-download/de-de/report?opn=TPS62046DGQR) lists active. Stock/price, errata and exact library validation are not complete.

## Underside pad is required

DGQ is a 10-pin MSOP PowerPAD package with visible leads, 0.5 mm lead pitch and approximately 3 x 3 mm body. It is not an ordinary pad-free MSOP. TI's pinout note says PowerPAD must connect to GND; the layout guidance on p16 explicitly requires it to be soldered to the PCB. Do not omit that joint just because estimated power dissipation is modest. The quoted thermal performance assumes the soldered pad and thermal vias.

The older application text gives a 1.52 x 1.79 mm pad; current appended package drawings may differ. Verify the exact current DGQ mechanical drawing and recommended land pattern for the ordered device before creating the footprint; do not use an old application-text dimension as the sole authority.

## Assembly with available tools

Engineering judgment: feasible with solder paste and the user's hot-air station, followed by iron touch-up of the visible leads. It remains harder than an ordinary SOT23 or MSOP without a bottom pad, but offers more inspection and repair access than the small TPS62902 leadless package.

Use a reviewed PowerPAD footprint, controlled paste amount (a small stencil is helpful), and ground/thermal-via design following TI's package guidance. Avoid excessive underside solder that can lift the leads; avoid open vias wicking away the required solder. Provide access around the IC for hot air and an iron. A large connected ground plane may make uniform reflow harder without preheat; confirm the process on a small evaluation PCB before committing the full board. Do not assume an oven or preheater is already available. A hidden joint cannot be fully inspected visually; basic electrical success alone does not certify solder coverage.

[TI PowerPAD assembly guidance](https://www.ti.com/lit/an/slma002g/slma002g.pdf). The pad should not be treated as an iron-only assembly feature or replaced with an improvised unsoldered thermal contact.

## Next electrical checks

The fixed-output application uses a 6.2 µH inductor and 22 µF input/output capacitors (Figure17). These are starting references, not a frozen Board 1 network; check current inductor availability/DCR, effective capacitance, full distributed output capacitance, startup and load steps. Do not transplant the TPS62902 2.2 µH network. There is no PG pin or external soft-start timing pin, so retain separate review of reset/isolation and USB inrush sequencing. MODE high forces PWM and changes light-load efficiency.

Prefer this over SC189 for the next detailed comparison if the required PowerPAD soldering process is acceptable. It follows the exposed-lead preference, but its mandatory hidden joint still needs the assembly justification above. No user selection or 90% efficiency qualification is implied, and the existing BOM has not been changed to this part.
