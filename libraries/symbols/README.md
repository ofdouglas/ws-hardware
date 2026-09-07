# Shared KiCad symbols

Project-local libraries are registered in ../../boards/board1/kicad/sym-lib-table using portable `${KIPRJMOD}` paths. Use the library ID below in the symbol chooser.

| Library ID | Status / evidence |
|---|---|
| `ATSAMC21G17A-AUT:ATSAMC21G17A-AUT` | Imported existing symbol; [original pin review and sources](ATSAMC21G17A-AUT/README.md); B1-B002 / ADR-004 |
| `TPS22810DBVT:TPS22810DBVT` | New DBV-specific symbol; [pin review](TPS22810DBVT/README.md); B1-B044 / ADR-019/022 |
| `SC189ZSKTRT:SC189ZSKTRT` | Historical imported symbol; [sources](SC189ZSKTRT/README.md); superseded for Board 1 by ADR-021 |
| `TCAN3413DR:TCAN3413DR` | New exact-part symbol; [pin evidence](TCAN3413DR/README.md); B1-B003 / ADR-002 |
| `TPS560430X3FDBVR:TPS560430X3FDBVR` | New exact-part symbol; [pin evidence](TPS560430X3FDBVR/README.md); B1-B012 / ADR-021 |
| `AT93C56B-SSHM-B:AT93C56B-SSHM-B` | New exact-part symbol; [pin evidence](AT93C56B-SSHM-B/README.md); B1-B013 / ADR-018 |
| `MC74HC1G14DBVT1G:MC74HC1G14DBVT1G` | [Pin evidence](MC74HC1G14DBVT1G/README.md); B1-B015 / ADR-013; ADR-024 |
| `SN74LV125APWR:SN74LV125APWR` | [Pin evidence](SN74LV125APWR/README.md); B1-B016; B1-B066 / ADR-001; ADR-013; ADR-033 |
| `ST3485EBDR:ST3485EBDR` | [Pin evidence](ST3485EBDR/README.md); B1-B021 / ADR-007; ADR-034 |
| `RCLAMP0504S.TCT:RCLAMP0504S.TCT` | [Pin evidence](RCLAMP0504S.TCT/README.md); B1-B018 / ADR-015 |
| `ESD2CAN24DBZRQ1:ESD2CAN24DBZRQ1` | [Pin evidence](ESD2CAN24DBZRQ1/README.md); B1-B072 / ADR-037 |
| `ESDS452DBZR:ESDS452DBZR` | [Pin evidence](ESDS452DBZR/README.md); B1-B073 / ADR-038 |

All symbols use default KiCad footprints. Imported files, pinout CSVs and previews came from the maintainer's directories; see ../imports/manifest.json and ../imports/README.md for provenance and the complete archive. Existing verification statements in imported READMEs are historical evidence, not a repeated electrical qualification. No explicit imported-asset license was supplied; redistribution terms remain TBD.

Part-selection acceptance and symbol availability do not mark board allocations verified. Exact footprints, pin mux, electrical limits, errata and implemented connectivity remain review gates under the existing board questions.

[Remaining IC checks and complete selected IC/array coverage](remaining_ic_symbol_checks.md), including default-library STM32 and FTDI entries.
