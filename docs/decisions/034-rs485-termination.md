---
id: ADR-034
title: ST3485EBDR and Board 1 bus termination
status: accepted
scope: Board 1 Rev A
created: 2026-09-06
accepted_on: 2026-09-06
accepted_by: Explicit maintainer instruction USR-28
supersedes: none
superseded_by: none
requirements: [B1-R016, B1-R021, B1-R026]
questions: [B1-Q003, B1-Q004, B1-Q009]
sources: [USR-28]
---

# ADR-034: ST3485EBDR and bus termination

Select one STMicroelectronics ST3485EBDR for B1-B021, replacing the unaccepted THVD1420DR candidate. Retain the 12 Mbps design ceiling and existing RS-485 bypass allocation B1-B036. No accepted ADR is superseded.

Accept the [termination arrangement](https://github.com/ofdouglas/ws-hardware/blob/dbcaba10831ade0516dba825d2c97d3f0017e0f5/boards/board1/termination_proposal.md): each CAN bus has one fixed 120 ohm resistor at the opposite onboard end and one jumper-removable 120 ohm resistor at the terminal-block end. Route the onboard bus as a linear trunk with short PHY branches. Install the jumper for board-only operation; remove it when a cable extends that end, with termination at the remote cable endpoint. A fixed far onboard terminator excludes tapping the middle of an already terminated external trunk. Each jumper is in series with its resistor branch, never directly across the differential pair.

The RS-485 port is a point-to-point cable endpoint with one fixed local 120 ohm resistor near the terminal block. The remote endpoint needs its own terminator. No RS-485 termination jumper is added.

B1-B067/068/069/070 allocate four CAN resistors, one RS-485 resistor, two jumper headers and two shunts. B1-B007/023 retain only residual protection/control/bias. Exact resistor and jumper MPNs remain unselected; [candidate parts](https://github.com/ofdouglas/ws-hardware/blob/dbcaba10831ade0516dba825d2c97d3f0017e0f5/boards/board1/termination_parts.md) are recommendations, not accepted selections.

[ST DS2947 Rev12, March 2021](https://www.st.com/resource/en/datasheet/st3485eb.pdf), pp.2–6,16,18, provides SO8 pins, 3.0–3.6 V operation, guaranteed 12 Mbps and EBDR ordering. Its guaranteed floating-input fail-safe does not guarantee an idle terminated bus state. B1-Q009 retains bias design, receiver-to-MCU threshold compatibility, DE-/RE defaults/timing, cable faults/protection and loaded current. Power estimates take no savings credit. B1-Q003/004 retain CAN routing and resistor/jumper implementation qualification. All evidence remains unverified; no CAD, ERC/DRC or bench validation was performed.
