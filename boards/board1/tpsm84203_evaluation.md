# TPSM84203EAB evaluation

Status: draft / candidate, not selected · Evidence: datasheet review, no hardware measurements · Date: 2026-09-06
Scope: B1-Q002, B1-Q011; USR-12. B1-R023 efficiency target and USB-only Rev A scope remain unchanged.

Sources: [TI datasheet SLUSCV7A, August 2017](https://www.ti.com/lit/ds/symlink/tpsm84203.pdf), sections 6.3–6.7 and 7.3; [DigiKey listing, 296-47073-ND](https://www.digikey.com/en/products/detail/texas-instruments/TPSM84203EAB/7561619). Catalog listing verified; no stock/price commitment or footprint verification.

| Item | Finding |
|---|---|
| Assembly | Three-pin through-hole module; supplier assembles internal regulator/inductor; no underside joint for board assembly |
| Output | Fixed 3.3 V, up to 1.5 A subject to thermal derating; ample versus current approximately 381 mA Rev A estimate |
| Input | Guaranteed 4.5–28 V; misses proposed 4.45 V converter-input boundary after USB cable and local path loss |
| Undervoltage | Rising UVLO 4.1 V typical / 4.4 V maximum; this is not a guarantee of regulated operation below 4.5 V |
| Efficiency | 92% typical at 5 V input / 1 A output; not a guaranteed 90% minimum at our loads and temperatures. Distributor headline 94% must not substitute for the exact variant/operating point |
| Support | TI specifies external input/output capacitors; 3.3 V reference uses two 47 uF output ceramics. Check effective capacitance, tolerances, USB inrush and total downstream capacitance before selecting parts |
| Control | VIN/GND/VOUT only; retain upstream controlled switch. Internal soft start 5 ms typical |

Recommendation: plausible for a regulated local 5 V rail in a later externally powered revision. Do not freeze for USB-only Rev A while the low-input gap and 90% qualification remain open. A typical sample operating at 4.45 V would not extend the manufacturer guarantee.

The future 24 V -> 5 V -> 3.3 V direction means there is no requirement for this downstream converter to withstand 24 V. Source selection and backfeed prevention belong to the later multi-input design; no new circuitry or BOM population is authorized here.
