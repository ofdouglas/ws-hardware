# Remaining Board 1 selections and qualification

Status: current index through ADR-042. [Requirements](requirements.md#open-questions--authoritative-register) owns question status; [bom.csv](bom.csv) owns selection and evidence status. Accepted MPNs should not be reselected as routine cleanup.

Use the [unfinished decision checklist](unfinished_decisions.md) for choices to complete before capture; the table below also includes qualification of already selected parts.

| Remaining work | BOM allocation | Question references |
|---|---|---|
| Ordinary MCU reset/boot and SWD support; automated CBUS recovery deferred ADR-042 | B1-B010; B1-B053 excluded | B1-Q005 |
| Enumerate bridge support; implement accepted PWREN# enable and complete receiver defaults and rail-by-rail capacitor counts | B1-B016/017/061/062/063 | B1-Q002/012 |
| Debug adapter input defaults and unpowered-interface support | B1-B060 | B1-Q014 |
| RS-485 DE and /RE defaults, residual support and bias backfeed behavior | B1-B023 | B1-Q009 |
| Determine whether CAN residual protection needs any components beyond accepted TVS arrays | B1-B007 | B1-Q003/004 |
| Fitted scope-ground pin MPN/count/locations; PCB pad locations | B1-B075/011 | B1-Q004 |
| Timing header pad/interrupt allocation and load contract | B1-B059; [timing headers](timing_headers.md) | B1-Q005/010 |
| USB shield bond, capacitor corners, hotplug/startup/suspend and full-load budget | See USB input and decoupling | B1-Q002/011 |
| Oscillator gain/drive/frequency, bus rates, remote kit population, connector/footprint checks | Selected parts retained | B1-Q003/004/008/009 |

The bias, LED and UART_MD resistor selections remain decided. ADR-041 / USR-35 replaces the separate GPIO/debug headers with four combined 1x8 timing/debug headers. One selected 40-position strip supplies all 32 positions. General ADC, SPI/I2C and GPIO breakouts are deferred. Resistor selections and PCB test pads plus fitted scope-ground access from ADR-039 remain in force. Exact timing MCU pads remain TBD under B1-Q005/010; scope-ground pin count/MPN remain layout work.

Current circuits: [USB input](usb_input.md), [USB VCP](usb_vcp.md), [decoupling](decoupling.md), [interfaces](interfaces.md), [termination](termination.md), [bias](rs485_bias.md). [Library checks](../../libraries/symbols/remaining_ic_symbol_checks.md) cover symbols, not complete board qualification. No question is closed by this index.

## Proposed circuit resolution paths

These are unfinished implementation proposals, not new accepted quantities or MPNs:

- RS-485 controls: consider 10 kohm DE pull-down, /RE pull-up for reset shutdown and MCU RX pull-up while RO floats; reuse the selected resistor MPN only after leakage/sequence review (B1-B023).
- MCU reset/boot: retain independent SWD reset and gateway BOOT0-low defaults under B1-B010. Automated CBUS circuitry is deferred to Rev B (ADR-042).
- VCP/debug: complete receiver defaults and hardware off-state isolation in both directions, including an unpowered external adapter. The accepted 24 series resistors are B1-B076 and excluded from residual B1-B060. Series resistors alone do not establish isolation. Rev A uses SWD for programming/reset (B1-B016/017/060).
- Bridge: enumerate the reference circuit pin by pin before assigning capacitor/filter counts. Do not guess additions to B1-B061–063.
- USB shield: direct local ground bonding is a starting proposal for layout/EMC review; no RC or bead is automatically authorized.
- Residual CAN: retire the aggregate only after confirming no parts remain beyond the selected networks. No implicit choke, DNP or extra series parts.

Resolve power-off interfaces and bridge rail enumeration first; those determine the outstanding procurement counts.

Current disposition: ADR-040 settles startup/direct PWREN# enable; ADR-042 specifies header order/series resistors and defers automated recovery. Startup measurements remain bring-up work.
