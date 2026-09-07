---
id: ADR-013
title: SC189 enable control and SN74LV125APWR UART isolation
status: accepted
scope: Board 1 Rev A
created: 2026-09-06
accepted_by: Explicit user approval USR-18
supersedes: ADR-001 main-switch implementation only
superseded_by: ADR-019 (direct input-capacitance attachment only)
---

# Current scope

ADR-019 adds an upstream attachment-ramp switch for both domains. The SC189 EN and UART isolation decisions below remain accepted; direct-attachment statements are historical.

# Decision

Omit AP22653 and the separate main load switch from Rev A. Connect SC189 VIN to the protected USB supply and control EN from FT232H PWREN# through an always-powered, default-off polarity interface. Preserve the independent bridge domain and USB configuration/suspend policy from ADR-001. Future 24 V-derived 5 V / USB source selection and reverse-current blocking are deferred.

Select one Texas Instruments SN74LV125APWR (TSSOP-14) for TX/RX/RTS/CTS power-off isolation: two channels each direction, powered from 3V3_SYS. Allocate one 100 nF bypass from the existing four auxiliary reserves in B1-B036; no increase to the 22.61 uF direct output allocation. Keep /OE disabled until the rail is valid and receiver pulls referenced to their receiving domains. Exact enable logic, pulls, FTDI VOH versus buffer VIH margin, ramp behavior and 12 Mbaud timing remain implementation checks. Selection is accepted, not electrically qualified.

# Consequences and remaining checks

SC189 input capacitance now attaches directly to VBUS; audit combined bridge/buck attachment inrush. Validate startup current, VBUS droop, suspend leakage and rail decay. SC189 soft start is not a 500 mA USB input limiter, and EN does not guarantee active output discharge. Input protection remains unselected. USB data ESD and VBUS protection are separate requirements.

# Evidence / revisit trigger

USR-18 explicitly says to omit AP22653 and commit to SN74LV125APWR. [TI datasheet](https://www.ti.com/lit/ds/symlink/sn74lv125a.pdf) specifies partial-power-down Ioff. [Semtech datasheet](https://www.kstmicro.com/wp-content/uploads/2025/03/SC189ZSKTRT.pdf) specifies shutdown and soft start. Revisit only for demonstrated electrical incompatibility, failed inrush/startup validation or changed power scope; do not reopen accepted choices for routine preference changes.
