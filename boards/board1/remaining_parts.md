# Remaining Board 1 selections and qualification

Status: current index through ADR-039. [Requirements](requirements.md#open-questions--authoritative-register) owns question status; [bom.csv](bom.csv) owns selection and evidence status. Accepted MPNs should not be reselected as routine cleanup.

Use the [unfinished decision checklist](unfinished_decisions.md) for choices to complete before capture; the table below also includes qualification of already selected parts.

| Remaining work | BOM allocation | Question references |
|---|---|---|
| MCU reset/boot support; power-off-safe CBUS reset and BOOT0 interfaces | B1-B010/053 | B1-Q005/013 |
| Enumerate bridge support; implement accepted PWREN# enable and complete receiver defaults and rail-by-rail capacitor counts | B1-B016/017/061/062/063 | B1-Q002/012 |
| Debug adapter input defaults and unpowered-interface support | B1-B060 | B1-Q014 |
| RS-485 DE and /RE defaults, residual support and bias backfeed behavior | B1-B023 | B1-Q009 |
| Determine whether CAN residual protection needs any components beyond accepted TVS arrays | B1-B007 | B1-Q003/004 |
| Fitted scope-ground pin MPN/count/locations; PCB pad locations | B1-B075/011 | B1-Q004 |
| GPIO series-resistor proposal, mux and load contract | B1-B027 headers; [resistor proposal](gpio_breakouts.md) has no BOM allocation; pinmap | B1-Q005/010 |
| USB shield bond, capacitor corners, hotplug/startup/suspend and full-load budget | See USB input and decoupling | B1-Q002/011 |
| Oscillator gain/drive/frequency, bus rates, remote kit population, connector/footprint checks | Selected parts retained | B1-Q003/004/008/009 |

The bias resistors, LED resistors, UART_MD resistors, crystals/load capacitors, USB connector and header cut plan are decided. Purchase one PRPC040SAAN-RC strip for four 1x5 GPIO and four 1x3 debug headers; B1-B059 does not add four purchased strips. Scope-ground pins are not yet allocated from the spare positions.

Current circuits: [USB input](usb_input.md), [USB VCP](usb_vcp.md), [decoupling](decoupling.md), [interfaces](interfaces.md), [termination](termination.md), [bias](rs485_bias.md). [Library checks](../../libraries/symbols/remaining_ic_symbol_checks.md) cover symbols, not complete board qualification. No question is closed by this index.

## Proposed circuit resolution paths

These are unfinished implementation proposals, not new accepted quantities or MPNs:

- RS-485 controls: consider 10 kohm DE pull-down, /RE pull-up for reset shutdown and MCU RX pull-up while RO floats; reuse the selected resistor MPN only after leakage/sequence review (B1-B023).
- MCU/CBUS: draw one shared gateway NRST network with open-drain sinks; use a main-rail-referenced, default-low BOOT0 driver with power-off-safe control. Decide whether physical reset buttons are wanted. Both quad buffers are fully allocated (B1-B010/053).
- VCP/debug: complete receiver defaults and hardware off-state isolation in both directions, including an unpowered external adapter. Series resistors alone do not establish isolation. ROM recovery must work without application firmware (B1-B016/017/060).
- Bridge: enumerate the reference circuit pin by pin before assigning capacitor/filter counts. Do not guess additions to B1-B061–063.
- USB shield: direct local ground bonding is a starting proposal for layout/EMC review; no RC or bead is automatically authorized.
- Residual CAN: retire the aggregate only after confirming no parts remain beyond the selected networks. No implicit choke, DNP or extra series parts.

Resolve power-off interfaces and bridge rail enumeration first; those determine the outstanding procurement counts.

Research update: [current dispositions](research/README.md) records accepted startup/direct PWREN# enable (ADR-040), remaining support details and separate MCU/CBUS recovery proposals. ROM pin conflicts remain for targeted review; startup measurements are bring-up work.
