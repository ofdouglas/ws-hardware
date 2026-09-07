---
id: ADR-015
title: RCLAMP0504S.TCT USB data ESD protection
status: accepted
scope: Board 1 Rev A USB D+/D-
created: 2026-09-06
accepted_by: Explicit user selection USR-20
supersedes: none
superseded_by: ADR-016 (polarity/high-voltage protection scope only; data ESD retained)
---

# Decision

Select one Semtech RCLAMP0504S.TCT, SOT-23-6, B1-B018. Place close to USB-B with short ground return and minimal data stubs. Internal TVS reference with pin 5 unconnected is the proposed connection; unused I/O channels unconnected. Final pin routing, footprint, signal integrity and ESD qualification remain open. The 5 V-rated reference must not simply be assumed suitable for direct attachment to a 5.5 V VBUS.

# Evidence and scope

USR-20 explicitly selects this device. [Semtech product/datasheet](https://www.semtech.com/products/circuit-protection/low-capacitance/rclamp0504s) specifies USB 2.0 use and internal-reference connection. Selection does not select SMF6.0A or close VBUS protection/inrush questions. User also requests reverse-polarity protection; exact circuit remains open. A unidirectional shunt TVS alone is not a guaranteed reverse-supply blocker or a precision positive overvoltage cutoff.

# Revisit trigger

Verified electrical incompatibility, failed ESD/signal-integrity validation, or sourcing failure. Do not reopen this accepted choice for routine preferences.

## Scope clarification

ADR-016 / USR-21 removes the earlier polarity-protection request. Only ESD and hot-plug protection remain in Rev A. This record was renumbered from the colliding ADR-014 USB entry; the crystal ADR-014 is unchanged.
