---
id: ADR-026
title: Ceramic SAM VDDCORE capacitors
status: accepted
scope: Board 1 SAM core regulator decoupling
created: 2026-09-06
accepted_by: Explicit user instruction to use ceramic instead of tantalum
supersedes: ADR-010 SAM core capacitor dielectric restriction only
superseded_by: none
---

# Decision

Use ceramic X7R for the three B040 SAM VDDCORE bulk capacitors. Retain 1 uF nominal plus each existing B041 100 nF bypass, placed at the local VDDCORE/GND pair. The three 1.2 V core outputs remain separate from each other and from 3V3_SYS. Remove the tantalum-only procurement restriction; T491A105K020AT is not selected.

CL21B105KAFNFNE (1 uF, 25 V, +/-10%, X7R, 0805) is the candidate for consolidation with the main-rail bulk caps, not an accepted exact MPN yet. Its effective capacitance at approximately 1.23 V, temperature/tolerance/aging and the regulator requirements must be checked before qualification. Retain low ESR (<=0.5 ohm project screen).

# Evidence and boundary

Locally reviewed Microchip DS60001479J p.1038 Table 45-21 labels the 0.8/1/1.2 uF output row as tantalum/electrolytic and separately lists 100 nF X7R. Its note recommends low-series-resistance ceramic X7R, tantalum or electrolytic capacitors, although that note is keyed to Cin. Thus the previous categorical statement that tantalum is required was too strong. Do not represent the table as an unambiguous manufacturer guarantee for an arbitrary 1 uF ceramic replacement. Ceramic is the accepted engineering choice; review effective C and verify core regulator startup/transient behavior. The legacy 0.8–1.2 uF row remains a qualification reference rather than an invented ceramic-specific datasheet limit.

Source: /home/ofdouglas/Downloads/SAM-C20-C21-Family-Data-Sheet-DS60001479J.pdf, p.1038, section 45.10.3. No hardware test performed. No change to main buck output nominal capacitance.

Subsequent selection: ADR-027 accepts CL21B105KAFNFNE as the exact MPN; the qualification boundary above remains applicable.
