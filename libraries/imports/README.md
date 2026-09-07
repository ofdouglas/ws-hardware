# Hardware migration archive

The maintainer requested consolidation of Design/Boards and Design/WireSpaces/hardware into ws-hardware. Their actual source paths and SHA-256 hashes are recorded in manifest.json. legacy-hardware.tar.gz preserves all 28 files, including the old ws_bench_1 project, autosaves, lock files, preferences, ZIP backups, symbol sources, previews and topology documentation. Every archive member was checked against its source hash before removing the originals.

Usable symbols and their companion evidence/previews are under ../symbols. The bench topology remains available under ../legacy/bench for the WireSpaces code-generator tests. No custom .kicad_mod footprint files existed in either source directory: the two symbols reference default KiCad footprints.

## Historical project conflict

The archived ws_bench_1 schematic uses STM32G473RBTx, whereas accepted ADR-004 and B1-B001 require STM32G474RBT6. It has not been promoted to the current Board 1 CAD or silently corrected. Saved and autosaved files differ; both are retained. Any resumed implementation must reconcile these files with Board 1 requirements and the pinmap (B1-Q005). No ERC/DRC was run on that project.

The archived sym-lib-table has its original absolute Boards path. When restoring the historical project, replace that entry with a relative path to the migrated ATSAMC21G17A-AUT library; do not restore archived lock files into an active project.

Imported assets had no explicit license file. Their existing source attribution is retained; redistribution license remains TBD. Archive copies are preservation evidence, not additional library authorities.

## Migration validation

Both original directories were removed only after archive hashes were rechecked and 24 WireSpaces code-generator tests passed (test_wiring_topology, test_wiring_realizations, test_wiring_models). Four codegen reference files were updated for the sibling ws-hardware topology path; the migrated YAML schema modeline was updated as well. All three libraries exported successfully with KiCad CLI 7.0.11, unique symbol pin numbers/positions matched the standard-footprint pad sets, and the new TPS22810DBVT preview was visually inspected. No board ERC/DRC or hardware validation was performed.
