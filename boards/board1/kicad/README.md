# KiCad workspace placeholder

Status: project symbol table available; no current Board 1 schematic or PCB exists here. Earlier bench CAD is preserved in the migration archive linked below.

Create the real `board1.kicad_pro`, `board1.kicad_sch`, and `board1.kicad_pcb` with KiCad when the design pass begins. Record KiCad version and assembly revision in the board README. Keep project library tables here with portable `${KIPRJMOD}`-relative paths to shared libraries. Do not fabricate empty CAD files.

Before layout, reconcile the accepted requirements, verified pinmap, schematic and planning BOM. Record actual ERC/DRC findings and reviewed exceptions when tools can run. Keep generated fabrication/assembly outputs tied to a reviewed revision, separate from source CAD.

The portable sym-lib-table registers 12 local libraries, including historical SC189. See [the catalog](../../../libraries/symbols/README.md) and [selected IC coverage](../../../libraries/symbols/remaining_ic_symbol_checks.md). STM32G474RBTx and FT232H use the standard global KiCad libraries. See ../../../libraries/imports/README.md for archived CAD and the STM32G473/STM32G474 conflict.
