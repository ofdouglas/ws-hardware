---
id: ADR-011
title: Independent Cortex SWD headers and owned debug probes
status: accepted
scope: Board 1 programming and debug access
created: 2026-09-06
accepted_on: 2026-09-06
accepted_by: Explicit maintainer instruction USR-16
supersedes: none
superseded_by: none
requirements: [B1-R007]
questions: [B1-Q004, B1-Q005]
sources: [USR-16]
---

# Independent Cortex SWD headers and owned debug probes

Use the four independent keyed 10-pin, 1.27 mm Cortex SWD headers proposed in https://github.com/ofdouglas/ws-hardware/blob/dbcaba10831ade0516dba825d2c97d3f0017e0f5/boards/board1/oscillator_debug_options.md, one per MCU, with individual reset access. The maintainer accepts the 10-pin Cortex SWD header approach and plans to use an owned J-Link EDU; a PICkit 5 is also on hand if necessary. These are external bench tools, not new onboard circuitry or procurement items.

Exact connector MPN/footprint, numbering, cable/adapter compatibility, probe revision/software device support and unpowered-target behavior remain B1-Q004/005. No successful flashing or debug test is asserted. Preserve USB-only target power. Do not infer an additional onboard debug connector for PICkit 5; evaluate an external adapter if needed.

The accompanying preference for one common 12 MHz crystal MPN is a selection objective, not acceptance or qualification of a crystal. See the candidate research in https://github.com/ofdouglas/ws-hardware/blob/dbcaba10831ade0516dba825d2c97d3f0017e0f5/boards/board1/crystal_candidates.md.

## Implementation selection — USR-25 / ADR-026 (026-reva-connectors.md)

[ADR-026](026-reva-connectors.md) selects the exact B1-B009 connector MPN. The original decision and its history remain intact; footprint, numbering, adapter/cable and probe behavior checks remain B1-Q004/005.
