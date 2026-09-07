# FTDI startup and VCP enable reassessment

Status: rationale for accepted ADR-040; no hardware validation · 2026-09-07

This revises the recommendations in the first two research proposals after maintainer questions about startup sequencing and using PWREN# directly. It does not change the BOM, accepted ADRs or pin allocations.

## EEPROM startup

The 100 us requirement is real: Microchip DS20006260B §4.6.1/Table 4-4 specifies a delay after stable EEPROM VCC before commands. However, analyzing the external 10 kohm/10 nF RC alone does not establish when the FT232H reads EEPROM. FTDI FT_000288 v2.2 §4.2 explicitly describes an integrated power-on reset and permits RESET# tied to VCCIO when external reset is unused. The same section describes a 16-bit 93LC56B or equivalent supporting a 1 Mbit/s clock and programming through FT_PROG; §7 gives the ordinary EEPROM interface.

The prior review gave too much weight to the absence of a separately tabulated internal read delay. No incompatible startup timing or requirement for a bespoke sequencer has been demonstrated. Follow the manufacturer supply/interface arrangement and retain the accepted RC/input ramp. Treat ordinary startup and replug checks as bring-up validation, not a demand to design a new sequencer or use a special reset fixture for normal provisioning. The earlier fixture is optional diagnostic equipment only if a problem is observed.

Part-name precision: the inspected FTDI datasheet names 93LC56B or equivalent, while its FAQ names the 93C56/93C66 class. Neither establishes an explicit endorsement of the exact AT93C56B-SSHM-B suffix. The selected part is evaluated as an equivalent; this distinction alone is not evidence of incompatibility. The prior note's claim that no clock guidance was found was too broad: §4.2 does provide the 1 Mbit/s capability requirement, though it does not tabulate every interface waveform.

## VCP enable

The simple circuit to evaluate first is PWREN# directly to all four active-low B016 /OE inputs, retaining the existing bridge-domain PWREN# pull-up. The existing inverter continues to drive the active-high buck EN. Low PWREN# starts the buck and requests buffer enable; high disables both. Avoid adding a SYS pull-up on this directly driven cross-domain net without reviewing the resulting path. Retain appropriate receiver defaults.

This provides USB-configuration/suspend control without firmware. Because B016 is main-powered and has specified Ioff at zero supply, its enable request does not by itself produce a full-voltage output while SYS is absent. Its inputs accept signals above its own supply within the stated limits.

ADR-040 accepts this control policy and replaces the prior literal rail-valid disable prerequisite. PWREN# is a permission signal; separate rail monitoring is not required. Normal startup/suspend/replug checks remain bring-up work. Receiver defaults and ordinary interface compatibility remain implementation checks. The dual-monitor/NAND recommendation is withdrawn.

## Sources

- [FTDI FT232H v2.2](https://www.ftdichip.cn/Support/Documents/DataSheets/ICs/DS_FT232H.pdf), §4.2 p.21, §3.4 p.13, §7 pp.49–50.
- [FTDI EEPROM FAQ](https://ftdichip.com/faq/what-external-eeprom-is-recommended-for-use-with-the-ftdi-usb-hi-speed-ics/), indexed text retrieved 2026-09-07; direct fetch returned 403.
- [Microchip DS20006260B](https://www.microchip.com/content/dam/mchp/documents/MPD/ProductDocuments/DataSheets/AT93C56B-AT93C66B-Microwire-Serial-EEPROM-Industrial-Grade-DS20006260.pdf), §4.6.1 p.9.
- [TI SN74LV125A SCES124O](https://www.ti.com/lit/ds/symlink/sn74lv125a.pdf), operating/electrical tables and §8.1 p.9.

Checks: reread primary documentation and compared the two control policies. No hardware measurements or verified allocation changes.
