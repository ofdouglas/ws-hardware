---
id: ADR-003
title: Host terminology and reduced first PCBA
status: accepted
scope: Repository terminology and Board 1 scope boundary
created: 2026-09-06
accepted_on: 2026-09-06
accepted_by: User instructions restated in current setup request (USR-01 and USR-02)
supersedes: none
superseded_by: none
requirements: [B1-R010]
questions: [B1-Q001]
sources: [USR-01, USR-02]
---

# ADR-003: Host terminology and reduced first PCBA

## Context / decision
The user explicitly updated protocol terminology to **Host**, `HostId`, `SrcHostId`, and `DestHostId`. Apply this throughout authored documents; original references retain historical wording.

The user explicitly stated that the full hardware architecture, including inter-board power/signal buses and fault injection, will not be realized in the first PCBA. Keep those capabilities deferred and clearly separated from MVP requirements. Do not require their footprints or reserve their pins merely because the full draft includes them.

## Alternatives / consequences
Importing the full architecture as rev-1 requirements would contradict the user's scope. The exact reduced feature set still needs acceptance in B1-Q001. CAN3, RS-485, auxiliary output and native USB treatment must be explicit; this decision alone does not settle every optional interface.

## Evidence / acceptance
USR-01 supplies both overrides; USR-02 repeats the terminology and MVP/future separation in the repository setup request. Acceptance records these instructions, not a new hardware design approval.

## Revisit trigger
Explicit user request to revise terminology or expand the first-PCBA scope, recorded through a superseding decision.
