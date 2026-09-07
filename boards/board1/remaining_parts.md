# Remaining Board 1 selections and qualification

Status: current index through ADR-039. [Requirements](requirements.md#open-questions--authoritative-register) owns question status; [bom.csv](bom.csv) owns selection and evidence status. Accepted MPNs should not be reselected as routine cleanup.

| Remaining work | BOM allocation | Question references |
|---|---|---|
| MCU reset/boot support; power-off-safe CBUS reset and BOOT0 interfaces | B1-B010/053 | B1-Q005/013 |
| Enumerate bridge support; settle VCP enables/defaults and rail-by-rail capacitor counts | B1-B016/017/061/062/063 | B1-Q002/012 |
| Debug adapter input defaults and unpowered-interface support | B1-B060 | B1-Q014 |
| RS-485 DE and /RE defaults, residual support and bias backfeed behavior | B1-B023 | B1-Q009 |
| Determine whether CAN residual protection needs any components beyond accepted TVS arrays | B1-B007 | B1-Q003/004 |
| Fitted scope-ground pin MPN/count/locations; PCB pad locations | B1-B075/011 | B1-Q004 |
| GPIO series-resistor proposal, mux and load contract | B1-B026 and pinmap | B1-Q005/010 |
| USB shield bond, capacitor corners, hotplug/startup/suspend and full-load budget | See USB input and decoupling | B1-Q002/011 |
| Oscillator gain/drive/frequency, bus rates, remote kit population, connector/footprint checks | Selected parts retained | B1-Q003/004/008/009 |

The bias resistors, LED resistors, UART_MD resistors, crystals/load capacitors, USB connector and header cut plan are decided. Purchase one PRPC040SAAN-RC strip for four 1x5 GPIO and four 1x3 debug headers; B1-B059 does not add four purchased strips. Scope-ground pins are not yet allocated from the spare positions.

Current circuits: [USB input](usb_input.md), [USB VCP](usb_vcp.md), [decoupling](decoupling.md), [interfaces](interfaces.md), [termination](termination.md), [bias](rs485_bias.md). [Library checks](../../libraries/symbols/remaining_ic_symbol_checks.md) cover symbols, not complete board qualification. No question is closed by this index.
