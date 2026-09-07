# Shared footprints

The imported ATSAMC21G17A-AUT and SC189ZSKTRT assets are symbols, not custom footprints. They assign default `Package_QFP:TQFP-48_7x7mm_P0.5mm` and `Package_TO_SOT_SMD:SOT-23-5` respectively. The new TPS22810DBVT symbol assigns default `Package_TO_SOT_SMD:SOT-23-6`. No .kicad_mod files existed in the migrated directories.

Future custom .pretty libraries belong here with project-relative library-table paths. Record exact MPN compatibility, upstream URL/license, land-pattern source, pad numbering, pin-1 orientation, exposed-pad treatment, dimensions and review evidence. Existing default-footprint assignment does not complete footprint qualification.

TCAN3413DR and AT93C56B-SSHM-B also assign default `Package_SO:SOIC-8_3.9x4.9mm_P1.27mm`; TPS560430X3FDBVR assigns default `Package_TO_SOT_SMD:SOT-23-6`. These assignments have matching pad sets; full land-pattern qualification remains open.
