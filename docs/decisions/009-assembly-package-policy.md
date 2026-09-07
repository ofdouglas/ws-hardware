---
id: ADR-009
title: Packages compatible with available assembly and rework tools
status: accepted
scope: Hardware project part selection and layout
created: 2026-09-06
accepted_on: 2026-09-06
accepted_by: Explicit user instruction USR-09
supersedes: none
superseded_by: none
requirements: []
questions: []
sources: [USR-09]
---

# ADR-009: Assembly and package policy

## Decision
Prefer SMT packages with exposed leads. QFN can be considered only with justification. Exclude BGA unless it is existential to an essential function. Available tools are a soldering iron and hot-air station. Avoid the smallest SMT passives; medium sizes are suitable.

## Consequences
Apply [part selection policy](../PART_SELECTION_POLICY.md#assembly-and-package-constraints--accepted-usr-09--adr-009) to new selections. The proposed TPS62902 is not accepted and must not become the default without package justification. Evaluate leaded alternatives first. Future FPGA interest does not itself authorize BGA or change this rule. Numeric passive-size defaults in the policy are an implementation interpretation, not separately user-frozen dimensions.

## Revisit trigger
An essential function cannot be realized under these constraints, or the user changes available tools/preferences. Record evidence; do not reopen merely for a smaller footprint.

## Maintainer clarification — USR-17

0805 imperial is easy to hand solder; 0603 is doable but small; exclude 0402 and smaller from new selections. Smaller crystal packages are acceptable when they have accessible leads. This makes the earlier medium-passive preference explicit; it does not accept leadless crystals or reopen the existing QFN/BGA policy. Historical text is retained.
