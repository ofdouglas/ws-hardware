Current authority: ADR-030 finalizes ECS-120-18-5PX-CKM-TR for FTDI and retains the four MCU ECS-120-20-3X-EN-TR crystals. Historical proposed wording below no longer controls MPN status. See [network proposal](crystal_networks.md); qualification remains open.

# Common 12 MHz crystal candidates

Status: ECS-120-20-3X-EN-TR selected for four MCUs; separate FT232HL candidate proposed under ADR-017; qualification unresolved
Research date: 2026-09-06 · Related: USR-16; ADR-005/009; B1-Q008; BOM B1-B014/019/020

Selected: ECS-120-20-3X-EN-TR used four times: gateway and three SAMs (USR-19 / ADR-014). USR-22 / ADR-017 separates the FT232HL crystal; ECS-120-18-5PX-CKM-TR is proposed for that one oscillator. All oscillators remain independent; their load capacitors may differ. The research below retains pre-selection comparisons; earlier statements of no selection are historical.

## Smaller leaded package search — 2026-09-06

The maintainer requested an alternative closer to 0805 or 12xx dimensions because the selected 11.4 x 4.8 mm package is larger than necessary. This paragraph records pre-selection research. USR-19 subsequently selected the smaller part under ADR-014; the electrical limitations below remain current.

The smaller stocked leaded candidate located was [ECS-120-20-3X-EN-TR](https://www.digikey.com/en/products/detail/ecs-inc/ECS-120-20-3X-EN-TR/2676617): 7.0 x 4.1 x 2.3 mm miniature HC-49/US SMT, 12 MHz fundamental, CL 20 pF, ESR 60 ohms, initial tolerance ±30 ppm and temperature stability ±50 ppm over -40 to +85°C. DigiKey's live listing showed 499,092 available and quantity-one cut tape at USD $0.37, order code XC1787CT-ND, on the research date. Stock and pricing are snapshots, excluding shipping/taxes.

This reduces listed body area by about 48%, but is still substantially larger than an imperial 1206 passive. Its tolerance specifications fail the conservative FT232HL ±30 ppm common-crystal screen before aging/loading error, so it is not recommended as the common replacement. MCU-only use would require separate qualification under B1-Q008. [ECS CSM-3X Rev.2017, pp.1–2](https://ecsxtal.com/store/pdf/CSM-3X.pdf) provides the mechanical drawing, frequency-dependent ESR, 100 uW maximum drive and ±5 ppm first-year aging. Tighter options exist in the series ordering table, but an exact stocked quantity-one orderable part meeting the common accuracy screen was not located.

No verified match combining near-0805/12xx dimensions, projecting leads, suitable common-part accuracy and DigiKey quantity-one availability was found in this search. The previously identified 3.2 x 2.5 mm candidates have four underside pads rather than projecting leads. Footprint access, oscillator startup/drive and load capacitors remain unverified (B1-Q005/B1-Q008); no CAD or hardware validation was performed.

## Hand-solderable alternatives — preferred follow-up shortlist

The maintainer finds the 3.2 x 2.5 mm candidates difficult to hand solder. The following live DigiKey US/USD listings were checked on 2026-09-06, including quantity-one cut-tape pricing. These replace the earlier small-ceramic recommendation as the preferred candidates for qualification; no MPN is selected.

| Candidate | Assembly | Live stock | Qty 1 USD | DigiKey order code |
|---|---|---:|---:|---|
| [ECS-120-18-5PX-CKM-TR](https://www.digikey.com/en/products/detail/ecs-inc/ECS-120-18-5PX-CKM-TR/12349445) | HC-49/US leaded SMT; 11.4 x 4.8 x 4.3 mm | 2,149 | $0.54 | 50-ECS-120-18-5PX-CKM-CT-ND |
| [ABL-12.000MHZ-B1U-T](https://www.digikey.com/en/products/detail/abracon-llc/ABL-12-000MHZ-B1U-T/16357670) | HC-49/US through-hole; 11.5 x 5.0 x 3.5 mm | 590 | $0.57 | 535-ABL-12.000MHZ-B1U-TCT-ND |

Both are 12 MHz fundamental crystals, CL 18 pF, ESR 50 ohms, initial tolerance ±10 ppm and temperature stability ±10 ppm over -20 to +70°C. Prices exclude shipping/tax/tariffs. The through-hole Abracon **ABL** part is different from the previously screened SMT **ABLS** part and its looser tolerance suffix.

Recommend the ECS part first for retaining SMT with accessible terminals; the Abracon is the easiest iron-only assembly option. Their larger area is the main tradeoff. Five devices at the observed prices cost $2.70 or $2.85, respectively. Keep them close to their MCUs/bridge with short crystal loops. Exact land patterns and assembly access remain unverified.

Primary evidence: [ECS CSM-7X Rev.2020, p.1](https://ecsxtal.com/store/pdf/csm-7x.pdf) decodes C/K/M, gives the 12 MHz ESR band, 500 uW maximum drive, ±5 ppm first-year aging, mechanical outline and suggested land pattern. [Abracon exact-part page](https://abracon.com/parametric/crystals/ABL-12.000MHZ-B1U-T) confirms the stated electrical values and two-pin through-hole package; full ABL datasheet revision/aging/drive/footprint reconciliation is still pending.

The ECS first-year conservative accuracy screen is 10 + 10 + 5 = 25 ppm before loading error, leaving 5 ppm against the FT232H ±30 ppm screen. That is tighter loading margin than the earlier ECS-33B candidate, not a completed accuracy qualification. Full startup/gain/drive checks on STM32, SAM C21 and FT232HL and individual capacitor selection remain B1-Q008. Neither part is marked verified for common use.

The earlier rationale for considering leadless crystals no longer supports preferring them: a tighter search found leaded alternatives with the required initial/temperature specifications. No change to ADR-009 is needed; this implements its existing assembly preference.

## Earlier small-ceramic DigiKey availability

The following US/USD stock counts and quantity-one cut-tape prices were read from live DigiKey browser pages on the research date. Search-index snapshots disagreed with some stock/prices; the live pages below take precedence. Prices exclude shipping/tax and any applicable tariff. Select cut tape, not Digi-Reel or full reel.

| Candidate MPN | DigiKey cut-tape order code | Live stock | Qty 1 USD | CL | Initial / temperature tolerance | Listed ESR max |
|---|---|---:|---:|---|---|---|
| [ECS-120-10-33B-CKM-TR](https://www.digikey.com/en/products/detail/ecs-inc/ECS-120-10-33B-CKM-TR/8023361) | XC2426CT-ND | 24,784 | $0.44 | 10 pF | ±10 / ±10 ppm | 100 ohm |
| [ABM8-12.000MHZ-12-B1U-T](https://www.digikey.com/en/products/detail/abracon-llc/ABM8-12-000MHZ-12-B1U-T/9997870) | 535-14962-1-ND | 12,206 | $0.47 | 12 pF | ±10 / ±10 ppm | 120 ohm |
| [C3E-12.000-8-1010-R](https://www.digikey.com/en/products/detail/aker-technology-corp/C3E-12-000-8-1010-R/12738183) | 3997-C3E-12.000-8-1010-RCT-ND | 1,338 | $0.42 | 8 pF | ±10 / ±10 ppm | 100 ohm; manufacturer series table differs |

All three are 12 MHz fundamental-mode, 3.2 x 2.5 mm ceramic four-pad leadless crystals, listed for -20 to +70°C. That is a candidate operating envelope, not a newly accepted board temperature rating.

## Recommendation and evidence

Historical first-pass recommendation (replaced by the hand-solderable shortlist above): **ECS-120-10-33B-CKM-TR**: low first-year aging, a moderate load capacitance and substantial stock make it a useful common-part candidate. [Manufacturer ECS-33B Rev.2023, pp.1–2](https://ecsxtal.com/store/pdf/ECS-33B.pdf) documents option codes C/K/M, 100-ohm ESR at 12 MHz, 200 uW maximum drive and ±1 ppm first-year aging. Five crystals cost $2.20 at the observed quantity-one price, before other costs. This is not a claim of oscillator compatibility.

The Abracon alternative has a higher ESR and loading requirement. [Manufacturer ABM8 sheet, revised 2020-07-29, p.1, hosted by DigiKey](https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/6536/ABM8_Datasheet.pdf) decodes B/1/U and lists 120-ohm ESR, 100 uW maximum drive and ±2 ppm first-year aging.

Aker offers the lowest listed CL, but has an evidence conflict: DigiKey lists 100 ohms, while [C3E general specification, 2022-08-01, p.1](https://aker-usa.com/files/content/products/crystals/C3E-General-Specification.pdf) lists 80 ohms in the 12–15.999 MHz band. It also has temperature-option wording needing exact-order reconciliation (p.4). Use 100 ohms conservatively for preliminary calculations; obtain exact-part clarification before qualification. The series sheet lists 100 uW maximum drive and ±3 ppm/year aging.

[FT232H v2.2, section 6.3, p.48](https://www.ftdichip.cn/Support/Documents/DataSheets/ICs/DS_FT232H.pdf) specifies a 12 MHz ±0.003% crystal and recommends fundamental parallel operation, with capacitors selected for the crystal. FTDI's current datasheet index reports v2.3; the current file could not be retrieved, so reconcile it before sign-off. Do not apply FT4222H-specific FAQ ESR limits to FT232H.

Conservative screening budgets initial error + temperature stability + aging + loading error against ±30 ppm. ECS uses 21 ppm before loading in a first-year screen, leaving 9 ppm; this is an arithmetic allocation, not measured accuracy or a lifetime guarantee. Manufacturer aging conditions and the eventual board temperature/lifetime envelope must be respected.

## Assembly tradeoff and rejected comparison

Under ADR-009, leaded SMT remains preferred. [ABLS-12.000MHZ-B2-T](https://abracon.com/parametric/crystals/ABLS-12.000MHZ-B2-T) is an easier-to-rework HC-49/US SMT option, but its ±20 ppm initial and ±50 ppm temperature specifications cannot support the conservative common-part ±30 ppm screen. Its DigiKey indexed page listed stock and single-piece pricing; it was not live-stock-qualified for this shortlist.

The provisional justification for considering the leadless candidates is their tighter combined accuracy for sharing a crystal with the FT232HL; the examined leaded option lacks that margin. This is not an exhaustive claim that no suitable leaded crystal exists, nor blanket acceptance of a leadless package. Hot-air access and inspectable pad extensions need footprint/layout review. No DNP alternative footprints are authorized.

## Remaining qualification

B1-Q008 remains open: exact current documents, MCU oscillator gain/startup margins at 12 MHz and the selected CL/ESR, FTDI drive/startup behavior, crystal drive limits, loading/parasitics, clock-tree/divisor review, temperature/aging budget, and startup/frequency measurements. B1-Q005 retains package/mux/footprint review. Crystal load capacitors are TBD; do not copy FTDI's example 27 pF values to every device.

No CAD, ERC/DRC, bench tests or purchasing was performed. Candidate MPNs remain in this research note rather than replacing the unselected crystal BOM rows.

## Separate FT232HL candidate — USR-22

Recommend [ECS-120-18-5PX-CKM-TR](https://www.digikey.com/en/products/detail/ecs-inc/ECS-120-18-5PX-CKM-TR/12349445) for the FTDI alone. The browser listing checked on 2026-09-06 showed 2,149 available at USD $0.54 for one cut-tape part, order code 50-ECS-120-18-5PX-CKM-CT-ND. Search-index stock differed; the browser observation is recorded here. No purchase occurred.

The [ECS CSM-7X Rev.2020 p.1](https://ecsxtal.com/store/pdf/csm-7x.pdf) C/K/M options give ±10 ppm initial, ±10 ppm stability over -20 to +70°C, and ±5 ppm first-year aging at the stated aging conditions. Worst-case arithmetic gives 25 ppm before loading error, leaving 5 ppm against the [FT232H v2.2 §6.3 p.48](https://www.ftdichip.cn/Support/Documents/DataSheets/ICs/DS_FT232H.pdf) ±0.003% crystal recommendation. This fits the preliminary first-year budget if loading error is held within that remainder. It is not a lifetime or full-temperature aging guarantee. Reconcile the current FTDI revision, characterize loading and startup/drive, and validate the assembled oscillator under B1-Q008.

This requires only one larger leaded crystal (11.4 x 4.8 mm), while all four MCU crystals retain the smaller selected package. B1-B014 is proposed/unverified, not implicitly re-accepted from historical ADR-012. CL is 18 pF for FTDI versus 20 pF for the MCU crystals; individual capacitors remain TBD.
