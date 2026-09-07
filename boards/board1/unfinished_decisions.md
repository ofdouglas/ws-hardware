# Board 1 unfinished implementation decisions

Status: working checklist · Updated: 2026-09-07 · Baseline: accepted decisions through ADR-042

This file identifies choices still needed for schematic capture. [Requirements](requirements.md#open-questions--authoritative-register) remains the authority for question status; this checklist neither accepts proposals nor closes questions. [BOM](bom.csv) owns parts and quantities, and [remaining parts](remaining_parts.md) maps residual BOM allocations to qualification work.

ADR-040 settles FTDI startup and direct PWREN# VCP enable. ADR-042 settles header wiring and defers automated CBUS recovery. Pending bring-up measurements do not block draft capture.

## Choices to complete

| Existing question IDs | Item to decide or specify | Required result / affected records |
|---|---|---|
| B1-Q002/012 | Captured FTDI support and configuration | Support/filter/capacitor enumeration is complete in [CAD](kicad/README.md); EEPROM settings and programming procedure are in [USB VCP](usb_vcp.md). Remaining electrical/errata checks at approval; programming/readback/startup at bring-up. |
| B1-Q002/008 | Captured VCP isolation | Direct PWREN# control, all four channels and six receiving-domain defaults are captured. Remaining threshold/timing qualification at approval and bring-up. |
| B1-Q005 | Ordinary MCU reset/boot | Complete manufacturer reset/boot support B1-B010, independent SWD reset and gateway BOOT0-low defaults. Automated CBUS recovery is deferred to Rev B by ADR-042; B1-B053 has no Rev A parts/footprints. |
| B1-Q003/005/008 | Simultaneous MCU allocation and link clocks | Finalize the draft pad/mux allocation, PHY standby GPIOs, DMA/resources and clock trees. Choose CAN arbitration/data rates and SAM ring/UART_MD rates from compatible timing and electrical limits. Keep the accepted gateway VCP and debug targets. See [pinmap](pinmap.md). |
| B1-Q003/004 | CAN control defaults and residual support | Specify reset/standby behavior and determine whether B1-B007 has any remaining components beyond the accepted networks. Retain the fixed-plus-jumper termination arrangement and selected TVS arrays; no extra choke, series part or DNP footprint is implied. See [interfaces](interfaces.md). |
| B1-Q009 | RS-485 controls and remote-powered behavior | Set DE and /RE defaults, receiver pulls, turnaround timing and B1-B023 support. Resolve backfeed through the accepted bias network when 3V3_SYS is off. Identify the owned remote kit, cable/polarity, termination/bias ownership and supported operating rate within the accepted voltage envelope. See [RS-485 bias](rs485_bias.md). |
| B1-Q014 | Dedicated debug UART electrical contract | Implement the accepted ADR-042 header order and 330 ohm series resistors B1-B076; finalize framing, adapter assumptions, input defaults and residual off-state support B1-B060 (excluding B1-B076), including an unpowered adapter. The four headers and 115200-baud target are already accepted. |
| B1-Q005/010 | Timing header implementation | Assign and verify independent interrupt-capable SYNC/TRIG inputs and private EVENT outputs per MCU; implement the two shared 10 kohm pull-downs B1-B077 and review load and external-drive/off-state contract. See [timing headers](timing_headers.md). Retain LED qualification. |
| B1-Q004 | Connectors, mechanics and probe access | Finalize terminal numbering and polarity, SWD cable/key compatibility, board outline/mounting/clearances, PCB test-pad positions and fitted scope-ground pin MPN/count/locations B1-B075. The eight spare source-strip positions remain unallocated. |
| B1-Q002/004/011 | Power operating envelope | Direct USB shield bond is captured. Document ambient, permitted timing-header load and traffic assumptions for whole-board review. Captured bridge capacitance agrees with the nominal model. |
| B1-Q006 | Experiment acceptance | Specify representative simultaneous traffic, bare-metal/RTOS workloads, queue/memory reporting and pass thresholds. These guide bring-up and later tests; they do not add circuitry. |

Bridge support and receiver defaults are captured. Complete ordinary MCU reset/boot during the next relevant capture stage. Track unresolved connectivity explicitly; do not delay drawing settled circuitry until all implementation details or bench tests are complete.

## Settled choices that remain subject to verification

Keep the accepted MCU/PHY selections, TPS22810 input ramp, TPS560430 buck, separate bridge domain, both fully occupied LV125 buffers, crystals and initial load capacitors, termination/bias/TVS networks, LED resistors and header cut plan. Their exact allocations are in the BOM and [ADR authority map](../../docs/decisions/README.md). Selection is not a reason to reopen these decisions routinely.

Remaining verification includes exact datasheet/errata and pinmux review, electrical thresholds and power-off behavior, oscillator gain/drive/loading, effective capacitance and regulator stability, package/land-pattern checks, USB current/transients and real link performance. These checks remain under B1-Q002–006, B1-Q008–012 and B1-Q014; B1-Q001/007 are resolved and B1-Q013 is resolved by Rev A recovery deferral. New evidence requiring a changed accepted decision must be recorded in a new numbered ADR with explicit maintainer acceptance.

Board 1 has a two-sheet power/USB schematic; other sections and PCB are not yet created. Captured pin/BOM/netlist reconciliation passes. ERC, complete-board review, layout/DRC and hardware bring-up remain later gates. The archived STM32G473 bench project is not the accepted STM32G474 implementation.
