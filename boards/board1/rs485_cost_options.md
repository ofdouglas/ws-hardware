Current decision: **ST3485EBDR selected**, USR-28 / [ADR-034](../../docs/decisions/034-rs485-termination.md). Termination topology accepted; exact passive/jumper MPNs remain open. The research below is historical; TI fail-safe claims do not apply to ST3485EBDR.

# Lower-cost RS-485 options

Research: 2026-09-06. Proposed only. User allows considering 10 Mbps for a good inexpensive device; no part or reduced final rate accepted yet. Retain existing power allowance until loaded-current and bias calculations are complete.

| Exact part | DigiKey qty1 / qty10 USD | Stock shown | Recommendation |
|---|---|---:|---|
| ST3485EBDR | 1.48 / 1.08 | 25,999 | Preferred cost reduction retaining guaranteed 12 Mbps |
| SP3485CN-L (MaxLinear) | 0.89 / 0.64 | 10,693 | Cheapest well-documented candidate found; 10 Mbps, 0 to 70 C |
| SP3485EN-L/TR (MaxLinear) | 0.95 / 0.683 | 0 | 10 Mbps industrial-temperature version; unavailable |
| SP3485EN-L (tube) | 1.22 / not recorded | 0 | Also unavailable |
| THVD1450DR | 2.17 / 1.597 | 17,382 | Existing reference recommendation |

Prices exclude shipping/taxes/tariffs; page snapshots, not reserved inventory. Current exact pages override older search-index stock. All listed alternatives use SOIC-8 and 3.3 V-compatible supplies. UMW SP3485EET remains a cheaper 12 Mbps option with unresolved documentation issues in its separate review; do not confuse it with MaxLinear.

ST3485EBDR: ST DS2947 Rev12 guarantees 12 Mbps (DigiKey lists 15 Mbps; design to manufacturer guarantee). 3.0–3.6 V supply; -40 to +85 C; separate DE and /RE. IEC ESD ratings are +/-15 kV air and +/-8 kV contact, not assembled-board certification. Only floating-input receiver fail-safe is guaranteed; terminated-idle operation needs bias analysis. Receiver VOH minimum is 2 V at 4 mA, so verify actual MCU input/loading margin. No-load supply current maximum 2.2 mA with driver enabled and 1.9 mA receiver-only; these exclude termination current. Savings versus TI: USD 0.69 (32%) per board before extra bias/support parts. Loaded-current/bias and pin/footprint review remain B1-Q009.

MaxLinear SP3485CN-L: lower-cost choice if 10 Mbps and 0–70 C are acceptable. Datasheet Rev2.0.2 specifies 10 Mbps under load, open-input fail-safe and short-circuit protection. Do not assume shorted/terminated-idle fail-safe or enhanced IEC ESD from the similar UMW name. Budget any necessary external bias and terminal protection. USD 1.28 (59%) IC saving versus TI; could be reduced by support circuitry. Both the ST and MaxLinear parts require idle-bias review; the TI recommendation already includes terminated-idle fail-safe.

Sources:
- https://www.st.com/resource/en/datasheet/st3485eb.pdf
- https://www.maxlinear.com/ds/sp3485.pdf
- https://www.digikey.com/en/products/detail/stmicroelectronics/ST3485EBDR/599097
- https://www.digikey.com/en/products/detail/maxlinear-inc/SP3485CN-L/2411076
- https://www.digikey.com/en/products/detail/maxlinear-inc/SP3485EN-L-TR/2471929
- https://www.digikey.com/en/products/detail/maxlinear-inc/SP3485EN-L/2411077
- https://www.digikey.com/en/products/detail/texas-instruments/THVD1450DR/9356550

No BOM selection or qualification status changed. Recommend ST3485EBDR for retaining speed and quantified ESD; SP3485CN-L when lowest IC cost is the priority and reduced temperature/speed envelope is acceptable.
