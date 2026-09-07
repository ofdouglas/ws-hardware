---
id: ADR-012
title: Common leaded 12 MHz crystal
status: superseded
scope: Board 1 gateway, three SAMs and FT232HL
created: 2026-09-06
accepted_on: 2026-09-06
accepted_by: Explicit maintainer instruction USR-17
supersedes: none
superseded_by: ADR-014
requirements: [B1-R005, B1-R015]
questions: [B1-Q005, B1-Q008]
sources: [USR-17]
---

# Common leaded 12 MHz crystal

Select ECS-120-18-5PX-CKM-TR for all five independent oscillators: gateway, SAM0/SAM1/SAM2 and FT232HL. This implements ADR-005; it does not change its clock architecture. See [candidate evidence](https://github.com/ofdouglas/ws-hardware/blob/dbcaba10831ade0516dba825d2c97d3f0017e0f5/boards/board1/crystal_candidates.md) for manufacturer specifications and dated DigiKey availability. Exact crystal entries are B1-B014/019/020; load networks remain separate and unselected.

The choice fits the maintainer's preference for hand-solderable leads. Smaller leaded packages remain permissible for future evaluation, but no alternative is selected and no alternate footprint is authorized.

Selection is accepted; oscillator implementation remains unverified. B1-Q008 covers gain/startup margin, drive level, frequency accuracy including loading/aging, clock trees and capacitor selection for each device. B1-Q005 covers pad and footprint review. Current source reconciliation and bench checks remain necessary; do not infer identical capacitors from a common crystal MPN. Only verified infeasibility or a changed maintainer requirement should reopen this selection.
