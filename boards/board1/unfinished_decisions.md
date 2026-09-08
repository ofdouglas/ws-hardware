# Board 1 remaining review and bring-up

The Rev A schematic is fully captured. MCU pin allocation, timing interrupts, ordinary reset/boot, receiver/default networks, connector numbering and capacitor counts are implemented in [KiCad](kicad/README.md). The corrected [pinmap](pinmap.md) and BOM agree with native export. Current authority is the ADR register; ADR-046 records the maintainer-requested communications measurement headers.

| Existing question IDs | Remaining stage / check |
|---|---|
| B1-Q002/011/012 | Schematic approval: power/bridge limits and errata; Eeschema ERC. Bring-up: current, EEPROM readback, startup/suspend/replug and converter behavior. |
| B1-Q003/005/008 | Schematic approval: fitted-device errata and timing margins. Firmware/bring-up: clock trees, CAN arbitration/data and UART/ring rates, DMA and simultaneous traffic. |
| B1-Q004 | Layout approval: connector physical key/pin1/mating, footprint fit, board outline, bus topology, probe locations and ground-clip clearance. |
| B1-Q009 | Bring-up: peer/cable and selected RS-485 rate, bias/termination loading and turnaround. Respect the powered-peer/backfeed and±5.5V bench limits in the circuit notes. |
| B1-Q010/014 | Bring-up: timing interrupts/events, debug and LED behavior. External header sources are3.3V and only drive while main power is on. |
| B1-Q006 | Firmware/experiment: representative traffic, bare-metal/RTOS workloads, reporting and pass criteria. |

No PCB layout or hardware validation is complete. ERC has not run because the installed KiCad7 CLI lacks the command. These are later checks, not missing circuit sections. Automated CBUS recovery and general GPIO breakouts remain deferred; no DNP footprints were added.
