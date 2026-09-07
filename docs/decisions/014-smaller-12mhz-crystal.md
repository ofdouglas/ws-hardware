---
id: ADR-014
title: Smaller leaded 12 MHz crystal
status: accepted
scope: Board 1 gateway, three SAMs and FT232HL selection
created: 2026-09-06
accepted_on: 2026-09-06
accepted_by: Explicit maintainer selection USR-19
supersedes: ADR-012
superseded_by: ADR-017 (FT232HL scope only; MCU selection retained)
requirements: [B1-R005, B1-R015]
questions: [B1-Q005, B1-Q008]
sources: [USR-19]
---

# Smaller leaded 12 MHz crystal

Select ECS-120-20-3X-EN-TR in place of ECS-120-18-5PX-CKM-TR for the existing common-crystal plan. Retain five independent oscillators and separate load networks. Exact entries are BOM B1-B014/019/020. The maintainer explicitly selects this part after the smaller-package comparison. This supersedes ADR-012's MPN selection and preserves its history.

The 7.0 x 4.1 x 2.3 mm leaded package reduces assembly area. It changes CL from 18 to 20 pF, maximum ESR from 50 to 60 ohms, and maximum crystal drive from 500 to 100 uW. Recalculate each load network and oscillator startup/drive margin. Source: [ECS CSM-3X Rev.2017, pp.1–2](https://ecsxtal.com/store/pdf/CSM-3X.pdf) and [dated exact-part evidence](../../boards/board1/crystal_candidates.md).

Selection acceptance does not resolve the known accuracy conflict: ±30 ppm initial plus ±50 ppm temperature stability already exceeds the conservative FT232HL ±30 ppm screen, before aging and loading error. B1-Q008 blocks clock implementation sign-off, especially the FTDI oscillator. No waiver of FTDI electrical requirements is inferred. Resolve with evidence and, if necessary, a separately accepted FTDI crystal exception before schematic freeze. MCU compatibility also remains unverified. No alternate footprint is authorized.

## Scope update — USR-22

ADR-017 removes FT232HL from this common-MPN selection. This ADR remains accepted for the four MCU crystals. Earlier all-five language is retained as history.
