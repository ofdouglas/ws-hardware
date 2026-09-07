---
id: ADR-040
title: Conventional FTDI startup and direct PWREN# VCP enable
status: accepted
scope: Board 1 Rev A
created: 2026-09-07
accepted_by: Explicit maintainer instruction USR-34
supersedes: ADR-013 rail-valid /OE prerequisite only
---

# Decision

FTDI startup timing is settled for design: retain the manufacturer supply/EEPROM arrangement, accepted TPS22810 ramp and FTDI RESET# RC without additional sequencing or a reset supervisor. An undocumented internal startup delay is not evidence of incompatibility.

Connect FTDI PWREN# directly to all four B1-B016 SN74LV125APWR /OE inputs (pins 1, 4, 10, 13). Keep the existing bridge-domain PWREN# pull-up. The existing MC74HC1G14 inverter still drives buck EN. Low PWREN# requests main power and enables the buffers; high disables both. The buffer remains powered by 3V3_SYS. Do not add a SYS pull-up to this cross-domain control net.

This replaces ADR-013's requirement to hold /OE disabled until the rail is valid. No separate rail-valid monitor, NAND gate or delayed enable is required. Power-off isolation remains required; error-free UART traffic during power transitions or arbitrary brownouts is not a requirement.

# Remaining work

Complete bridge supply/support counts and receiver defaults as ordinary implementation work. Check actual pin connections and interface compatibility before schematic approval. Check enumeration, programming/readback, suspend/resume and normal replug at bring-up. These later measurements do not block capture or reopen the settled startup/enable choices by themselves. EEPROM command-voltage restrictions and concrete ROM pin conflicts remain separate issues.

# Evidence and revisit trigger

USR-34: maintainer states FTDI startup timing is fine and VCP buffers can be enabled by PWREN#, then directs correction of the records and workflow rules. Engineering rationale and primary references are in [the reassessment](https://github.com/ofdouglas/ws-hardware/blob/60b7d9173682d060f6f9a2d47fc1587a68000353/boards/board1/research/enable_startup_reassessment.md). No hardware measurements are claimed. Revisit for a concrete incompatible limit, observed failure in intended use, or changed requirement.
