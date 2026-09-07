---
id: ADR-024
title: MC74HC1G14DBVT1G main buck enable inverter
status: accepted
scope: Board 1 Rev A
created: 2026-09-06
accepted_by: Explicit user instruction to commit to MC74HC1G14DBVT1G
supersedes: none; implements ADR-013 enable inversion
superseded_by: ADR-030 (47 kohm tolerance only)
---

# Decision

Use onsemi MC74HC1G14DBVT1G, SC-74A, to invert FTDI PWREN# into TPS560430 EN. Supply pin 5 from independent FTDI_3V3 (same rail as VCCIO), pin 3 ground, pin 2 PWREN#, pin 4 EN, pin 1 NC. Proposed support: 10 kohm input pull-up to FTDI_3V3, 47 kohm EN pull-down, 100 nF local supply bypass allocated from the existing FTDI-domain control allowance. No P-channel MOSFET inverter. Keep SMF6.0A as the sole VBUS TVS; CUHZ candidates are not selected.

The selected inverter has exposed leads at 0.95 mm pitch. Input pull-up requests main power off for a floating PWREN#; output pull-down biases EN off when undriven. Logic operation below 2 V is unspecified: these pulls do not prove glitch-free startup. Verify reset, startup, suspend, brownout and unplug, including EN <= VIN + 0.3 V as rails collapse. Do not supply from switched main 3.3 V or USB_5V. Schmitt thresholds are supply dependent; do not misapply the datasheet's 3.0 V threshold limits as guaranteed 3.3 V limits. Check actual high level with the pull-up and any FTDI internal pulls. No new supervisor is selected.

# Evidence

[onsemi datasheet](https://www.onsemi.com/pdf/datasheet/mc74hc1g14-d.pdf), pp.1–3, 5–6. Selection is accepted; support values, footprint and electrical qualification remain proposed/unverified. Do not reopen the selected IC without new evidence or maintainer direction.
