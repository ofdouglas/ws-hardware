# Board 1 unfinished implementation decisions

Status: working checklist · Updated: 2026-09-07 · Baseline: accepted decisions through ADR-040

This file identifies choices still needed for schematic capture. [Requirements](requirements.md#open-questions--authoritative-register) remains the authority for question status; this checklist neither accepts proposals nor closes questions. [BOM](bom.csv) owns parts and quantities, and [remaining parts](remaining_parts.md) maps residual BOM allocations to qualification work.

Research for the first three entries is now available in the [combined resolution review](research/README.md). ADR-040 settles FTDI startup and direct PWREN# VCP enable. Other support and recovery proposals remain proposals. Pending bring-up measurements do not block draft capture.

## Choices to complete

| Existing question IDs | Item to decide or specify | Required result / affected records |
|---|---|---|
| B1-Q002/012 | FTDI rail support and configuration | Enumerate each supply, filter and bypass connection; settle capacitor counts B1-B061–063 and residual B1-B017. Specify EEPROM settings and normal programming/readback procedure. Startup timing is settled by ADR-040; enumeration and replug checks belong to bring-up. Retain the accepted input ramp and RESET# RC without an external supervisor. See [USB VCP](usb_vcp.md) and the [support proposal](research/ftdi_support_proposal.md). |
| B1-Q002/008 | VCP buffer enables and receiver defaults | Implement accepted direct PWREN# /OE control (ADR-040); complete receiving-domain defaults. No rail monitors or delayed enable are required. Preserve all four signals and firmware-independent ROM access. B1-B016 uses all four channels. See [clocking](clocking.md) and the [enable proposal](research/vcp_enable_proposal.md). |
| B1-Q005/013 | MCU reset/boot and gateway CBUS circuits | Complete shared open-drain NRST and default-low BOOT0 interfaces, polarities, pulls and exact components B1-B010/053. Set option-byte and ROM-entry policy; decide whether physical reset buttons are wanted. Keep reset released and BOOT0 low by default. See [ADR-023](../../docs/decisions/023-cbus-gateway-recovery.md) and the [recovery proposal, including ROM pin conflicts](research/cbus_recovery_proposal.md). |
| B1-Q003/005/008 | Simultaneous MCU allocation and link clocks | Finalize the draft pad/mux allocation, PHY standby GPIOs, DMA/resources and clock trees. Choose CAN arbitration/data rates and SAM ring/UART_MD rates from compatible timing and electrical limits. Keep the accepted gateway VCP and debug targets. See [pinmap](pinmap.md). |
| B1-Q003/004 | CAN control defaults and residual support | Specify reset/standby behavior and determine whether B1-B007 has any remaining components beyond the accepted networks. Retain the fixed-plus-jumper termination arrangement and selected TVS arrays; no extra choke, series part or DNP footprint is implied. See [interfaces](interfaces.md). |
| B1-Q009 | RS-485 controls and remote-powered behavior | Set DE and /RE defaults, receiver pulls, turnaround timing and B1-B023 support. Resolve backfeed through the accepted bias network when 3V3_SYS is off. Identify the owned remote kit, cable/polarity, termination/bias ownership and supported operating rate within the accepted voltage envelope. See [RS-485 bias](rs485_bias.md). |
| B1-Q014 | Dedicated debug UART electrical contract | Finalize header order, framing, adapter assumptions, input defaults and off-state support B1-B060, including an unpowered adapter. The four headers and 115200-baud target are already accepted. |
| B1-Q005/010 | GPIO breakout implementation | Finalize which four pads per MCU reach the headers, signal order, allowed loads and external-drive/power-off contract. Decide the [proposed series resistors](gpio_breakouts.md); they are not accepted parts or footprints. Verify the accepted LED network's drive polarity/current and visibility. |
| B1-Q004 | Connectors, mechanics and probe access | Finalize terminal numbering and polarity, SWD cable/key compatibility, board outline/mounting/clearances, PCB test-pad positions and fitted scope-ground pin MPN/count/locations B1-B075. The eight spare source-strip positions remain unallocated. |
| B1-Q002/004/011 | USB shield and power operating envelope | Decide shield bonding and document ambient, permitted external GPIO load, representative worst-case traffic and startup/suspend assumptions. Reconcile pull-up/bias loads and final capacitor counts into the power model. See [USB input](usb_input.md). |
| B1-Q006 | Experiment acceptance | Specify representative simultaneous traffic, bare-metal/RTOS workloads, queue/memory reporting and pass thresholds. These guide bring-up and later tests; they do not add circuitry. |

Complete bridge support, receiver defaults and reset/boot circuits during capture. Track unresolved connectivity explicitly; do not delay drawing settled circuitry until all implementation details or bench tests are complete.

## Settled choices that remain subject to verification

Keep the accepted MCU/PHY selections, TPS22810 input ramp, TPS560430 buck, separate bridge domain, both fully occupied LV125 buffers, crystals and initial load capacitors, termination/bias/TVS networks, LED resistors and header cut plan. Their exact allocations are in the BOM and [ADR authority map](../../docs/decisions/README.md). Selection is not a reason to reopen these decisions routinely.

Remaining verification includes exact datasheet/errata and pinmux review, electrical thresholds and power-off behavior, oscillator gain/drive/loading, effective capacitance and regulator stability, package/land-pattern checks, USB current/transients and real link performance. These checks remain under B1-Q002–006 and B1-Q008–014; B1-Q001/007 remain resolved. New evidence requiring a changed accepted decision must be recorded in a new numbered ADR with explicit maintainer acceptance.

No current Board 1 schematic or PCB exists. Schematic/pinmap/BOM reconciliation, ERC, layout/DRC and hardware bring-up remain later gates. The archived STM32G473 bench project is not the accepted STM32G474 implementation.
