# Remaining Board 1 component decisions

Reviewed 2026-09-06 through ADR-038. CAN and RS-485 TVS parts are decided in B1-B072/073. See the [BOM closeout review](bom_closeout.md) for recommended parts, quantities, sourcing and qualification limits.

The next simple decisions are the two 330 ohm bias resistor MPNs, five LED resistors, multidrop support resistors, GPIO/debug header cut schedule, and PCB-pad test access. These recommendations remain proposed; prior MPN/value acceptance is preserved.

Circuit work remains for reset/BOOT0 recovery, VCP defaults, debug adapter power-off isolation, RS-485 control defaults, FTDI derived-rail/bypass counts and USB shell bonding. B1-B007 can be retired as an empty residual allocation once the CAN circuit is confirmed. No additional chokes or DNP options are implied.

The closeout review covers all proposed rows and all accepted rows with TBD MPN or count. Exact MPN acceptance is distinct from implementation verification; do not reopen already selected parts simply because footprint, timing or power qualification is unfinished.
