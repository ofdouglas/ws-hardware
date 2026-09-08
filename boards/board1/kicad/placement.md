# Board 1 Rev A — initial component placement

Status: approximate placement revised 2026-09-07 for header/IC spacing and labeled test access; not routed or released.
Authority: current maintainer request to place all components and incorporate
the sketch review refinements. The [native PCB](board1.kicad_pcb) is now the
placement authority; the schematic remains the connectivity authority.

Open [board1.kicad_pro](board1.kicad_pro) in KiCad, then PCB Editor.
[Top-view preview](review/board1-initial-placement.png) ·
[Vector preview](review/board1-initial-placement.svg).

The provisional outline is 155 × 110 mm. All 239 schematic footprints are on
the front, with four additional PCB-only 3.2 mm M3 clearance holes. The holes
are non-plated and excluded from the electrical BOM and placement output.
Their coordinates and the outline are reversible bench-mechanical choices,
not a frozen enclosure or Rev B interface. No extra electrical components,
backbone connectors, 24 V circuitry, or future DNP footprints were added.

There are **zero tracks, vias and copper zones**. Grey CAN corridor guides are
on `Dwgs.User`, not copper. The initial two-copper-layer setting is KiCad's
starting configuration; stack-up and routing rules have not been frozen.

## Placement rationale

| Area | Placement and intended routing |
|---|---|
| USB edge (bottom) | J1 faces outward. D2 sits between its signal pins and U4. Input protection/ramp and the 5 V→3.3 V buck are nearby on the left. FTDI, EEPROM and VCP buffer form a local group leading toward the gateway. |
| Gateway | U7 is below the bus corridor, near the FTDI/VCP group. Its timing header is on the bottom edge; SWD and ground access are beside it. Current part is STM32G473RBT6 per ADR-043. |
| Leaves | U8/U9/U10 form three repeated stations above the buses. Each has its own crystal, supply/core bypasses, reset/default resistors, LED, 1×8 header, SWD, reset/core testpads and ground posts. Header orientations are consistent. |
| CAN | Two SOIC-8 rows provide the eight PHY channels. From the fixed-termination end toward the external connector, each row passes SAM0, SAM1, GW, SAM2. Pads 6/7 face the routing corridors. R59/R65 lie beyond the far-left PHYs; J10/J11 and R60/R66 sit near the terminal end. |
| External terminals (upper-right) | J12 faces outward on the edge opposite USB. D8/D9/D10, RS-485 U20, its bias/defaults and local termination, CAN termination jumpers and bus probe access are in this corner. The gateway-to-RS-485 logic signals can cross the board later. |
| Measurement and assembly | Twelve testpads, seven communications measurement headers and six ground headers are placed. SWD plugs have additional clear space beyond their courtyards. The buck inductor is separated from every crystal; all selected hand-assembly footprints are retained. |

The maintainer's spacing follow-up moves J4/J6/J8 left by 8 mm, increasing
J8-to-J12 courtyard clearance from approximately 4.5 to 12.5 mm. The lower
groups are spread out: U5 and its EEPROM support move right, U6/VCP moves
right/down, U19/UART_MD moves right, and U7 with its MCU support moves 27 mm
right. U4 stays near USB. Headers and annotations follow the gateway as
appropriate. This uses more of the formerly empty lower-right area while
retaining the existing outline; no precise Rev B converter keepout is frozen.

## Test access

The twelve retained power/reset/core testpads have concise function text on `F.SilkS`. Their stable TP
references remain in CAD and on `F.Fab`, so netlist identities are unchanged.
All six ground headers are labeled `GND`. ADR-046 replaces TP13–TP19 with
J19–J25, seven fitted 1×2 0.1-inch PRPC002SAAN-RC headers. The three ring
headers are near their MCU links. The [communication access record](communication_header_access.json)
records pin order and placement. Each header has a function label and adjacent
`H/L`, `A/B` or `SIG/GND` text; the square pad is pin 1. J18 moves 3 mm down
to keep the bus-header bank clear. The
[access record](testpoint_access.json) maps each reference to its label, net,
position and nearest ground post; the checker compares it with the native PCB.

| Printed names | Function / physical group |
|---|---|
| `RAW5V`, `USB5V`, `FT3V3`, `3V3` | Raw USB input, switched USB 5 V, FTDI 3.3 V and main 3.3 V; power/USB area, with J17 ground access |
| `GW_RST`, `BOOT0` | Gateway reset and boot strap; below the gateway support group, beside J13 ground access |
| `S0_RST` / `S0_CORE`, `S1_RST` / `S1_CORE`, `S2_RST` / `S2_CORE` | Reset and regulated core rail for each leaf; above-left of the corresponding MCU, beside its ground header |
| `UART_MD` | J25 beside U19: pin 1 signal, pin 2 GND |
| `RING01`, `RING12`, `RING20` | J22/J23/J24: SAM0→SAM1, SAM1→SAM2, SAM2→SAM0 respectively; pin 1 signal, pin 2 GND |
| `CAN A`, `CAN B`, `RS485` | J19/J20/J21 below the terminal/transceiver group: pin 1 H/H/A, pin 2 L/L/B; J18 ground posts nearby |

Testpad centers are at least 6 mm apart. Nearest ground-post distances range
from 5.8 to 14.8 mm; most are below 10 mm. These are geometric access checks,
not a claim about a particular probe's high-frequency ground-loop performance.
Function labels are at least 0.8 mm high and within 6 mm of their pads. The
revised silkscreen has no overlap or copper-clipping findings, apart from the
previously recorded USB connector outline at the board edge.

All six 330 Ω branches per MCU are in its local component group, rather than
at the external header. Independent review measured straight pad-to-pad
distances of approximately 2.8–8.3 mm; these are placement distances, not routed
lengths. Tighten the longer gateway EVENT and SAM debug-TX paths when doing
pin-level placement. Likewise refine bypass pad orientation, crystal loops,
FTDI ferrite/supply groups, and the buck switching/feedback loops before routing.
This phase establishes plausible areas and ordering, not final local routing.

The terminal and USB bodies were oriented from their actual footprint geometry:
USB mouth at local +X, terminal front at local +Y. SAM SWD-to-timing courtyard
gaps are about 4.5 mm; the gateway headers are farther apart. Additional plug
and probe allowances are engineering estimates. Actual cable/key fit, wire
insertion/actuation, mounting hardware and final board dimensions remain
layout approval under B1-Q004. No exact cable envelope or sample fit is claimed.

## Checks performed

Run `/usr/bin/python3 scripts/check_board1_placement.py` from the repository root.
It exports a fresh schematic netlist, loads the saved PCB, and checks every
reference, footprint ID, value, exported property, schematic UUID path and
pad net. All 879 schematic pins match; J1's two shield pads share number 5,
so the PCB contains 880 numbered physical pads. H1–H4 are the only additions.
The outline is closed, all pads are inside it, all components are on the front,
and there are no tracks/vias/zones or copper drawings. The spacing revision also
checks all 12 testpad function labels and seven communication header labels against their nets, minimum testpad spacing,
and nearby ground access.

KiCad 7.0.11 PCB DRC was actually run through `pcbnew.WriteDRCReport` in a fresh
process. [Results](review/board1-initial-placement-checks.json) and the
[full report](review/board1-initial-placement-drc.txt) are retained. There are
no courtyard overlaps, inter-component copper-clearance violations, solder-mask
bridges, missing footprints or overlapping silkscreen. Independent review also
checked real courtyard bounds, connector orientation/access, all eight CAN PHYs,
MCU-side branches, power/crystal separation and the schematic-to-PCB import.
The native preview was visually reviewed.

Full DRC is **not clean**, as expected at this stage:

- 499 unconnected-item findings: all connections intentionally remain unrouted.
- 48 clearance findings inside the four SWD footprints: their 1.27 mm pitch and
  1.10 mm pads leave 0.17 mm copper gaps, below the current default 0.20 mm rule.
  This is existing land-pattern geometry, not a placement collision. Resolve
  fabrication capability/rule scope or the land-pattern annulus before layout
  approval; no rule was relaxed and no finding was excluded during this task.
- Two USB footprint silkscreen segments reach the board edge at the connector
  mouth. Clip the silk to the final outline during release cleanup.

Schematic ERC and hardware validation have not been performed. The existing
schematic/part qualification items retain their stages; none blocks approximate
placement merely because it remains open.

## Editing and provenance

Edit `board1.kicad_pcb` directly from now on. The
[placement snapshot](initial_placement.json) records the original initial coordinates
and local spacing adjustments; it intentionally predates the subsequent header,
IC and test-access edits. Use the PCB for current placement and
`testpoint_access.json` for current test access. `scripts/place_board1_initial.py` is one-time
generation provenance and refuses to overwrite an existing PCB without an
explicit `--replace`; do not rerun it over subsequent layout edits. Real library
footprints are embedded in the board and registered with portable KiCad paths
in [fp-lib-table](fp-lib-table).

This implements the accepted connector/debug, bus termination/protection and
assembly decisions, notably ADR-009/011/021/026/034/037/038/041/042. Exact local
connector drawing evidence remains in [footprint_checks.md](footprint_checks.md).
The native import path was independently checked against KiCad 7.0.11's
[sheet-path export](https://github.com/KiCad/kicad-source-mirror/blob/7.0.11/eeschema/sch_sheet_path.cpp#L265)
and [PCB updater](https://github.com/KiCad/kicad-source-mirror/blob/7.0.11/pcbnew/netlist_reader/board_netlist_updater.cpp#L318).
The communications-header revision implements ADR-046 and updates the schematic, BOM and pinmap together.

The fresh schematic-to-PCB and independent topology checks pass after ADR-046.
The full schematic/BOM check currently stops at the preexisting J2/B059 MPN
mismatch (BOM PH1-08-UA versus captured strip stock). Document/purchasing audits
also flag B027's superseded row with quantity one. Those unrelated substitutions
remain a BOM/CAD reconciliation item before schematic approval; no header-change
validation is being represented as a full BOM audit pass.
