# Board 1 BOM reconciliation

Reviewed 2026-09-06 against accepted decisions through ADR-032 and the maintainer's request to correct provisional/decided status. Scope: documentation, allocation accounting and candidate research; not electrical release qualification.

## Corrections

- Rebuilt BOM.md from the current CSV. The prior readable version still labeled the selected USB connector, FTDI crystal, LEDs, buck passives, ceramic bypass/core capacitors, and oscillator load capacitors as unresolved or provisional. They now appear as decided exact MPNs, with their existing acceptance authorities.
- Exposed five already-decided bridge allocations hidden inside provisional B1-B017: B1-B061–064 are the ADR-027 capacitor MPNs; B1-B065 is the ADR-028 EEPROM pull-up. RESET# capacitor and EEPROM pull-up retain one each. Remaining bridge capacitor quantities stay TBD pending rail-by-rail enumeration. This is a split, not added circuitry.
- Removed stale B1-B017 language proposing already-decided oscillator capacitors and duplicating EEPROM/REF/crystal components moved to B1-B056–058. Updated linked reset/EEPROM/inverter support references.
- Corrected B1-B023 from superseded ADR-006 to ADR-007; linked B1-B054/055 to their power/VCP requirements; removed GPIO requirement references from LED-only rows. VBUS TVS/current input references now identify their actual accepting decisions.
- Filled the Phoenix terminal's DigiKey order code from its listing. Recorded current out-of-stock evidence for the unaccepted THVD1420DR candidate and linked the stocked alternative review.
- Normalized the two removed supervisor rows' unsupported `assembly=omit` value to allowed `tbd`, consistently with the four historical converter rows. All six remain quantity zero and superseded, explicitly excluded from procurement/population.
- Replaced stale SC189 capacitance claims in the readable BOM with the current 34.61 uF nominal allocation and 46.31165 uF positive tolerance/temperature screen. Removed obsolete “use supervisor” instructions from the current BOM view; historical decisions remain intact.
- Consolidated the ADR index table and made references to its two historical ADR-026 entries filename-specific. Both original IDs and histories are retained, not renumbered.

## Decisions deliberately not invented

RK73H2ATTD3301F LED resistors remain provisional: ADR-029/030 explicitly leave them unaccepted. GPIO 220 ohm series resistors remain a proposal, not a new decided BOM allocation. RS-485 and UART multidrop candidates remain unaccepted. B1-B059 debug UART headers are decided as a category only; acceptance of the GPIO source strip does not automatically decide a new header MPN or cut schedule. B1-B017 retains only unenumerated residual support, so its remaining provisional status is intentional.

Existing exact selected CSV rows were already `accepted`; the main status defects were the stale readable BOM and accepted parts hidden in an aggregate. No evidence status was upgraded to verified.

## Open work

- Bridge rail-by-rail counts and final source-CAD reconciliation remain B1-Q002/012. Header cut schedules, GPIO loads and debug adapter off-state behavior remain B1-Q004/010/014.
- CAN/RS-485 termination and protection, UART multidrop topology/rate, and reset/boot/CBUS component choices remain B1-Q003/009/013.
- Many selected rows still lack verified symbol/footprint and exact DigiKey pack codes. This audit did not requalify every datasheet or refresh stock for the entire BOM.
- [Interface candidates](rs485_uart_candidates.md) recommends THVD1450DR and SN74LVC1G07DBVR, with a hex-driver alternative, without accepting them or adding alternative footprints.

## Checks

CSV schema, stable unique BOM IDs, allowed status values, zero-quantity superseded rows, complete readable-BOM row coverage, decision/source links and split-row accounting are checked in this audit. Source CAD is absent; no ERC/DRC or hardware validation is claimed.

## Follow-up consistency check

Rechecked the current CSV and readable BOM against maintainer decisions through ADR-032. All explicitly accepted exact MPNs are already accepted; no remaining recommendation was promoted without evidence. Corrected B043's misleading "six pairs" description to six individual capacitors (three pairs), and removed header-count language from B060's support-component allocation. Added previously researched DigiKey links to oscillator capacitor rows and clarified that the TPS560430 filter MPNs are selected while filter qualification remains open.

Validated nonempty/schema fields, unique IDs, allowed status/assembly values, nonnegative or explicitly unknown quantities, zero-quantity superseded rows, ADR existence, one-to-one CSV/readable-table coverage, and the recent exact selections. No quantities or circuit topology changed. No stock refresh, new part qualification or hardware tests were performed in this follow-up.

Current totals: 65 planning rows; 48 decided exact-MPN rows, 2 decided category rows, 9 provisional rows and 6 superseded zero-quantity rows. These are BOM rows, not component or unique-MPN counts.
