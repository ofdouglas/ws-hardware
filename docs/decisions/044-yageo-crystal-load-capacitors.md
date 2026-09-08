---
id: ADR-044
title: YAGEO 33 pF crystal load capacitors
status: accepted
scope: Board 1 B1-B042 and B1-B043
created: 2026-09-07
accepted_on: 2026-09-07
accepted_by: Explicit maintainer instruction in this conversation to use YAGEO CC0805FRNPO9BN330
supersedes: ADR-031 (33 pF capacitor MPN only)
superseded_by: none
requirements: [B1-R015]
questions: [B1-Q008]
---

# ADR-044: YAGEO 33 pF crystal load capacitors

Replace KEMET C0805C330F5GACTU with YAGEO CC0805FRNPO9BN330 for the eight MCU oscillator capacitors in B1-B042/043. DigiKey cut-tape code: **311-4175-1-ND**. The maintainer explicitly requests this change after the cost comparison.

The [exact DigiKey listing](https://www.digikey.com/en/products/detail/yageo/CC0805FRNPO9BN330/5883941) specifies the same 33 pF, +/-1%, 50 V, C0G/NP0, 0805 attributes. Retrieved quantity-50 pricing was USD 6.09 total, compared with USD 28.35 for the previous part; refresh before ordering. This decision does not increase the purchase quantity to 50.

Keep two capacitors per MCU, the existing Device:C symbol and 0805 footprint, and all wiring. Update native schematic/PCB MPN fields and the manifest with the BOM. The 27 pF FTDI capacitors and REF resistor remain governed by ADR-031.

Selection acceptance does not establish oscillator startup, loaded frequency or drive qualification. B1-Q008 and existing footprint review remain open; evidence status stays unverified. No ERC/DRC or hardware validation is implied.
