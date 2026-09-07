# Leaded buck shortlist

Status: preliminary search, 2026-09-06 · USR-09 · ADR-009 · B1-Q011

Screening target: 3.3 V output, roughly 0.1–0.6 A, low-input operation after USB path losses, and a credible route to at least 90% converter efficiency. None below has a proven 90% worst-case floor. No replacement MPN or passive network is frozen.

| Candidate | Package | Evidence and disposition |
|---|---|---|
| Diodes AP63200 | TSOT26, six exposed leads | 3.8–32 V input; 2 A; adjustable; 500 kHz; PFM at light load. Worth evaluating first for a leaded design. Published efficiency plots reviewed are at 12/24 V, so do not infer a numeric 5 V-to-3.3 V floor. |
| Diodes AP63203 | TSOT26, six exposed leads | Same input range; fixed 3.3 V; 1.1 MHz. Simpler voltage setting; compare actual efficiency with AP63200 rather than assuming the lower-frequency option wins. |
| TI TPS62160DGKR | VSSOP-8, exposed leads | 3–17 V input, 1 A; adjustable. Figure 12 shows about 92–93% typical near the Board 1 active load at 5 V input. Potentially adequate for 90%, but little margin for temperature/tolerances and the proposed 92% internal qualification goal. TPS62162 fixed-output version is WSON, not this leaded alternative. |
| Microchip MCP16311, MSOP variant | MSOP-8, exposed leads | 4.4–30 V input, 1 A; PWM/PFM. Typical 3.3 V curves indicate low/mid-90s efficiency near relevant loads and low input voltages. Only 50 mV input margin at the 4.45 V planning corner; cannot cover proposed 4.35 V robustness sweep. Secondary candidate, not preferred. Exact ordering suffix not frozen. |

Primary sources: [Diodes DS41326 Rev3-2, Nov2024](https://www.diodes.com/datasheet/download/AP63200-AP63201-AP63203-AP63205.pdf), [TI SLVSAM2E, Figure12](https://www.ti.com/lit/ds/symlink/tps62160.pdf), [Microchip DS20005255D, Figures2-1/2-4](https://ww1.microchip.com/downloads/aemDocuments/documents/APID/ProductDocuments/DataSheets/MCP16311-2-30V-Input-1A-Output-High-Efficiency-Integrated-Synchronous-Switch-Step-Down-Regulator-DS20005255D.pdf). Curve values are approximate typical readings, not guarantees. No sourcing/footprint/errata sign-off or measurements were performed.

Screened out: TPS562201 needs 4.5 V at the IC, leaving no input-path margin; MP2315 also needs 4.5 V and its reviewed datasheet marks it not recommended for new designs. TPS62932 has exposed leads but a very small 0.5 mm-pitch SOT583 package, so it is not the first choice for easier assembly. [TPS562201](https://www.ti.com/lit/gpn/tps562201), [MP2315](https://www.monolithicpower.com/pub/media/document/MP2315_r1.01.pdf), [TPS62932](https://www.ti.com/product/TPS62932).

Recommendation: evaluate AP63200/AP63203 with suitable low-DCR inductors, and compare SC189 as another unpurchased candidate. SC189 remains a solderable SOT23-5 candidate with unqualified efficiency. Retain TPS62902 only as an efficiency reference/justified fallback, not an accepted build choice. The old TPS62902 passives and 407 mA estimate do not automatically transfer to another regulator; repeat startup, stability and efficiency review. This brief search identifies candidates; it does not establish that any leaded option meets every corner.

USR-10 follow-up: [SC189 evaluation](sc189_evaluation.md) now evaluates SC189 as a candidate for trial, conditional on its 30 µF total-output-capacitance constraint. SOT23 curves do not establish 90% across 100–600 mA.

USR-11: [TPS62046DGQR assessment](tps62046_evaluation.md) adds a promising MSOP PowerPAD candidate. Exposed leads aid rework, but the ground pad must be soldered. SC189 ownership advantage was erroneous and is withdrawn.
