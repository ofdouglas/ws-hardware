# BOM allocation and sourcing notes

- B1-B027 buys one 40-position PRPC040SAAN-RC strip; B1-B059 counts four included 1x8 timing/debug placement pieces (32 positions). Eight positions remain unallocated. Dedicated CAN jumper headers B1-B069 are separate.
- B1-B011 represents PCB test pads and has zero purchased components. B1-B075 fitted scope-ground pins are accepted scope with MPN/count/locations TBD; spare strip posts are not yet allocated.
- B1-B061–065 expose existing bridge allocations formerly in B1-B017. The residual row excludes all split parts; capacitor counts B1-B061–063 remain TBD. B1-B053 is excluded from Rev A by ADR-042 (zero components/footprints).
- B1-B036 contains 39 main-rail 100 nF positions, including four auxiliary reserves: VCP and UART_MD buffers consume two, leaving two. [Decoupling](decoupling.md) owns the allocation explanation and 34.61 uF nominal main-rail calculation. Core, bridge, buck-input and bootstrap capacitance are separate.
- Two SN74LV125APWR ICs serve VCP and UART_MD separately. B1-B008 is exactly four accepted 10 kohm /OE pull-ups; B1-B074 is the accepted shared 470 ohm pull-up.
- [Termination](termination.md), [bias](rs485_bias.md) and [interfaces](interfaces.md) describe accepted bus networks. Residual B1-B007/023 exclude their separately listed resistors, jumpers and TVS arrays.
- Superseded rows preserve stable IDs with zero quantities. Their assembly=tbd field does not authorize fitted or DNP footprints.
- [Symbol catalog](../../libraries/symbols/README.md), [exact-part checks](../../libraries/symbols/symbol_checks.md) and [remaining IC coverage](../../libraries/symbols/remaining_ic_symbol_checks.md) describe real library artifacts. Library checks do not verify board allocation or complete schematic/layout sign-off.
- [Remaining selections](remaining_parts.md) indexes unresolved work; [requirements](requirements.md) owns question status. No quantities, choices or verification statuses were changed by this view.

- B1-B076 adds 24 CRGP0805F330R series resistors: six per MCU beside its signal pins. B1-B071 retains two separate RS-485 bias resistors, giving 26 of this MPN total. B1-B060 excludes the eight debug series resistors already in B1-B076. No static pull-up load is added by a series resistor alone; retain the existing provisional external-load allowance until actual loads are specified.

- B1-B077 is two shared timing-input pull-downs, one per global SYNC/TRIG net. Each is 10 kohm to GND, on the header side of the four series branches. Reuse RMCF0805FT10K0; these are additional to existing FTDI/UART pull resistors. Their high-state load is supplied by the external timing driver, so no permanent 3V3_SYS pull-up current is added.
