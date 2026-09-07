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

All symbols use default KiCad footprints. Imported files, pinout CSVs and previews came from the maintainer's directories; see ../imports/manifest.json and ../imports/README.md for provenance and the complete archive. Existing verification statements in imported READMEs are historical evidence, not a repeated electrical qualification. No explicit imported-asset license was supplied; redistribution terms remain TBD.

Part-selection acceptance and symbol availability do not mark board allocations verified. Exact footprints, pin mux, electrical limits, errata and implemented connectivity remain review gates under the existing board questions.
