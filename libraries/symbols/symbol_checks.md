# Symbol checks — TCAN3413DR, TPS560430X3FDBVR, AT93C56B-SSHM-B

Tool version: KiCad CLI 7.0.11. Scope: B1-B003/012/013; ADR-002/021/018. Manufacturer datasheet revisions and pages are linked in each part README.

All three libraries passed:

- Native KiCad SVG export, followed by visual inspection of rendered PNGs. Preview SVG viewports were fitted to the exported drawing bounds with margins to correct exporter whitespace/clipping; symbol geometry was not changed.
- Complete S-expression parsing; pin numbers/names checked against independently transcribed manufacturer pin tables.
- Unique visible pins and connection positions on the 1.27 mm grid; matching companion CSV names and electrical types.
- Exact MPN/value and assigned standard-footprint pad sets (eight, six, eight); no extra exposed pads.
- BOM symbol/footprint agreement and portable project library-table paths. All six library entries resolve, without duplicate names.

BOM selection remains accepted and allocation evidence remains unverified. Package land-pattern dimensions, electrical application limits, current errata and implemented board connectivity are not qualified by this check. Existing questions B1-Q002/003/004/011/012 remain open. No schematic ERC, PCB DRC or hardware validation was performed.
