---
id: ADR-045
title: YAGEO 27 pF FTDI crystal capacitors
status: accepted
scope: Board 1 B1-B058, C12/C13
created: 2026-09-07
accepted_on: 2026-09-07
accepted_by: Explicit maintainer instruction in this conversation to replace the 27 pF 1% KEMET part with the equivalent YAGEO part
supersedes: ADR-031 (27 pF capacitor MPN only)
superseded_by: none
requirements: [B1-R005, B1-R012]
questions: [B1-Q008]
---

# ADR-045: YAGEO 27 pF FTDI crystal capacitors

Replace C0805C270F5GACTU with YAGEO CC0805FRNPO9BN270, DigiKey cut-tape code 311-4173-1-ND, for C12/C13. Purchase quantity remains two per board.

The [manufacturer sheet, p.1](https://yageogroup.com/download/specsheet/CC0805FRNPO9BN270) specifies 27 pF, +/-1%, 50 VDC, C0G, 0805 (2.00 x 1.25 mm). Retain Device:C, the existing 0805 footprint, values and wiring. This is a cost substitution accepted explicitly by the maintainer; no tolerance relaxation or new circuitry is involved.

[Exact DigiKey listing](https://www.digikey.com/en/products/detail/yageo/CC0805FRNPO9BN270/8025262). Refresh stock and pricing before purchase. Native schematic/PCB MPN fields and the current complete manifest follow the BOM. The original capture_manifest.json remains historical evidence of the initial power/USB capture, not the current procurement list.

B1-Q008 retains loaded-frequency, startup and drive qualification. Evidence stays unverified; no ERC/DRC or hardware validation is asserted. The separately discussed 10 uF buck input part is unchanged.
