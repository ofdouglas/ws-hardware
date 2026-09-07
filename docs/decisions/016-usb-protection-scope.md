---
id: ADR-016
title: USB ESD and hot-plug protection scope
status: accepted
scope: Board 1 Rev A USB input
created: 2026-09-06
accepted_by: Explicit user instruction USR-21
supersedes: Earlier polarity request in USR-20 / ADR-015
superseded_by: none
---

# Decision

Provide ESD and hot-plug protection only. Omit reverse-polarity protection and sustained high-voltage fault protection from Rev A. RCLAMP0504S.TCT remains selected for D+/D- under ADR-015. No AP22653 or separate main load switch is reinstated; SC189 EN control remains accepted under ADR-013.

# Remaining implementation work

Select and coordinate VBUS transient suppression/damping; audit directly attached capacitance, attachment inrush, main-rail startup current, VBUS droop and ringing. Validate normal USB voltage operation and transient behavior at both FTDI and SC189. SMF6.0A remains unselected; omission of sustained overvoltage protection does not establish it as an adequate hot-plug clamp. Do not add a polarity MOSFET, blocking diode or high-voltage disconnect as an implied requirement.

# Authority and revisit trigger

USR-21 explicitly says: Skip polarity and high voltage protection, only ESD / hotplug protection. Revisit only with changed user requirements or evidence that the ESD/hot-plug implementation needs revision. Future 24 V source selection remains separately deferred.
