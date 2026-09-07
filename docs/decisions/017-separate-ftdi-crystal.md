---
id: ADR-017
title: Separate accurate FT232HL crystal
status: accepted
scope: Board 1 crystal selection strategy
created: 2026-09-06
accepted_on: 2026-09-06
accepted_by: Explicit maintainer direction USR-22
supersedes: ADR-014 FT232HL common-part scope only
superseded_by: none
requirements: [B1-R005, B1-R015]
questions: [B1-Q005, B1-Q008]
sources: [USR-22]
---

# Separate accurate FT232HL crystal

Retain ECS-120-20-3X-EN-TR for the four MCU oscillators. Find a separate FT232HL crystal within its accuracy budget, as explicitly requested by the maintainer. This replaces only ADR-014's extension of that smaller MPN to the FTDI. The four-MCU selection and independent oscillator architecture remain accepted.

Propose ECS-120-18-5PX-CKM-TR for B1-B014 (quantity one). This exact replacement is proposed, not accepted by this strategy decision. It retains accessible leads at the expense of one larger package. The first-year conservative screen is 10 ppm initial + 10 ppm temperature + 5 ppm aging = 25 ppm, leaving 5 ppm for loading error against ±30 ppm. Validity is limited to the specified -20 to +70°C range and aging conditions; longer life and complete operating accuracy remain unqualified.

Evidence and dated DigiKey sourcing: [crystal candidates](../../boards/board1/crystal_candidates.md#separate-ft232hl-candidate--usr-22). B1-Q008 remains open for exact loading, drive/startup, temperature/lifetime and FTDI current-document reconciliation. B1-Q005 retains footprint review. A selected candidate and arithmetic margin do not establish hardware validation.
