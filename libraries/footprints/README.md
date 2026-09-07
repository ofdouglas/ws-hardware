# Shared footprints

The imported ATSAMC21G17A-AUT and SC189ZSKTRT assets are symbols, not custom footprints. They assign default `Package_QFP:TQFP-48_7x7mm_P0.5mm` and `Package_TO_SOT_SMD:SOT-23-5` respectively. The new TPS22810DBVT symbol assigns default `Package_TO_SOT_SMD:SOT-23-6`. No .kicad_mod files existed in the migrated directories.

Future custom .pretty libraries belong here with project-relative library-table paths. Record exact MPN compatibility, upstream URL/license, land-pattern source, pad numbering, pin-1 orientation, exposed-pad treatment, dimensions and review evidence. Existing default-footprint assignment does not complete footprint qualification.

TCAN3413DR and AT93C56B-SSHM-B also assign default `Package_SO:SOIC-8_3.9x4.9mm_P1.27mm`; TPS560430X3FDBVR assigns default `Package_TO_SOT_SMD:SOT-23-6`. These assignments have matching pad sets; full land-pattern qualification remains open.

Remaining IC symbols assign default SOT-23-5 (MC74HC1G14DBVT1G), TSSOP-14_4.4x5mm_P0.65mm (SN74LV125APWR), SOIC-8_3.9x4.9mm_P1.27mm (ST3485EBDR), SOT-23-6 (RCLAMP0504S.TCT), and SOT-23 (ESD2CAN24DBZRQ1). Numbered pad sets match; see ../symbols/remaining_ic_symbol_checks.md for scope and remaining qualification.

ESDS452DBZR (B1-B073 / ADR-038) also assigns standard SOT-23 with pads 1/2/3; full qualification remains open.
