---
id: ADR-020
title: FTDI supply-qualified reset with TLV803E
status: superseded
scope: Board 1 Rev A
created: 2026-09-06
accepted_by: User explicitly requested proceeding with TPS22810 plus TLV803
supersedes: ADR-019 FTDI startup without an external supervisor only
superseded_by: ADR-022
---

# Decision

Retain TPS22810DBVT and its ADR-019 passives. Add TI TLV803EA42RDBZR (SOT-23-3, R pinout), the 4.2 V / 200 ms variant of the newer TLV803E family. This exact variant is an engineering implementation of the user's approved supervisor architecture. Do not substitute legacy TLV803M or other pinout/threshold/delay suffixes.

Power/sense the supervisor from ramped USB_5V. Connect pin 1 RESET# to FT232HL pin 34 RESET#, pin 2 to ground, pin 3 VDD to USB_5V. Add local 100 nF bypass. Pull RESET# up with 10 kohm to independent FTDI 3.3 V (VCCD/VCCIO), never main 3V3_SYS or 5 V. Retain the existing 10 nF FTDI reset capacitor; it is not the sequencing timer. The supervisor's timer is internal.

Sequence: ramp USB_5V; hold FTDI reset until voltage qualifies and timeout expires; FTDI initializes and enumerates; PWREN# through the existing default-off interface enables SC189 only after configuration. Require that interface to hold SC189 off for FTDI reset/high-impedance/unpowered states and suspend. A supply dip asserts FTDI reset and must consequently disable the main domain; qualify the propagation and reset defaults before fabrication.

# Threshold, timing and sourcing evidence

The selected device's nominal falling threshold is 4.2 V, with +/-2% accuracy and hysteresis 0.9–1.5% of threshold. Conservative maximum rising threshold: 4.2*1.02*1.015 = 4.34826 V, leaving about 102 mV to the provisional 4.45 V minimum USB_5V. Falling threshold spans 4.116–4.284 V. The legacy TLV803M has a falling threshold up to 4.48 V before hysteresis, incompatible with that margin.

A-option reset delay is 200 ms nominal, 130–270 ms under TI's stated measurement conditions (10% overdrive). Minimum-voltage/slow-ramp timing remains a hardware check; do not claim those timing limits were separately characterized at our 4.45 V rail. TPS22810's nominal remaining rise after 4.15 V to a 5.5 V endpoint is about 29 ms with CT=1 uF, substantially shorter than nominal supervisor delay, but its worst-case slew is not established. This design guarantees a voltage qualification mechanism, not an exact 5 V endpoint under arbitrary source ramps.

DigiKey ordering code: 296-TLV803EA42RDBZRCT-ND. Listing accessed 2026-09-06 indicated 7,178 and $0.44 quantity one; cached observation, not reserved or live inventory guarantee. Passive MPNs remain TBD. Added 100 nF is behind TPS22810, making direct ramped 5 V capacitance 15.0 uF. Main SC189 output remains 22.61 uF.

# Sources and remaining checks

- [TI TLV803E Rev J, pinout, electrical characteristics and timing](https://www.ti.com/lit/ds/symlink/tlv803e.pdf).
- [TI legacy TLV803 Rev E, threshold table](https://www.ti.com/lit/ds/symlink/tlv803.pdf).
- [DigiKey exact supervisor](https://www.digikey.com/en/products/detail/texas-instruments/TLV803EA42RDBZR/13545339).
- [Current input circuit](../../boards/board1/vbus_protection_proposal.md).

Verify schematic pinout, reset loading/edge behavior with the existing 10 nF, all startup and brownout defaults, USB attach/enumeration, preconfiguration current while in reset, low-voltage full-load stability, ramp completion before enable, suspend and ESD/hotplug performance. These remain unverified. The supervisor does not suppress overvoltage or limit buck startup current.

# Revisit trigger

Failed electrical/startup measurements, insufficient threshold margin, sourcing failure or changed power scope. Do not reopen this architecture merely to consolidate two ICs into a leadless device.
