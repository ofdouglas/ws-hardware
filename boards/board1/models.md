# Board 1 model and BOM maintenance

Status: planning calculations, not measured maxima or compliance evidence. Authority: ADR-021/022/025 and current BOM/requirements.

| Artifact | Role |
|---|---|
| [power_budget.json](power_budget.json) | Schema v2; active_model names current_rev_a_input, the sole current Rev A steady-state model. Includes original load assumptions, explicit path resistance and rounded reference results. |
| [power_budget_future.json](power_budget_future.json) | Deferred expanded Board 1 sensitivities; original no-path-loss arithmetic retained. Not a current power design or an efficiency requirement. |
| [vbus_hotplug_model.py](vbus_hotplug_model.py), [snapshot](vbus_hotplug_model.json) | Exploratory ideal cable/RC sweep, excluding the actual TVS, switch, loads and contact bounce. Peak voltage is not the protected FTDI rail prediction. |
| [bom.csv](bom.csv) | Authoritative part selections, planning quantities and verification status. |
| [bom_quantity_rules.json](bom_quantity_rules.json) | ADR-039 exceptions: strip purchase versus cut placement counts, non-purchased PCB pads. Unknown quantities stay TBD. |
| [bom_allocation_notes.md](bom_allocation_notes.md) | Editable allocation prose included in the generated BOM view. |

From the repository root, using Python 3 (standard library only):

```sh
python3 scripts/board1_documents.py --write
python3 scripts/board1_documents.py
python3 -m unittest discover -s scripts -p 'test_*.py'
python3 boards/board1/vbus_hotplug_model.py --check
```

The first command regenerates BOM.md and audits; the second checks without modifying files. Neither generates an order list. Header purchases are one strip total; four combined 1x8 timing/debug pieces are the placement count. Fitted ground-pin count/MPN remain unknown, and the eight spare strip positions are unallocated. Superseded parts have zero buy/place counts. Each quantity override declares whether its CSV quantity counts purchases or placements; the audit compares that quantity with the override and checks placed header pieces against the cut schedule. The unittest command exercises conflicting quantities and stale scenario results in temporary copies.

Current power equation uses amperes: Iusb = Ibridge + (3.3*I3v3)/(eta*(Vconnector-Rpath*Iusb)). The audit checks its low-current root against retained rounded results (0.002 mA tolerance), plus break-even at 500 mA. Each result names its load scenario; main-load and bridge-current fields must match that scenario before the current calculation is checked. The conservative bridge allowance must also match the break-even input. It also checks original future-scenario arithmetic with zero path resistance. Numerical reproduction does not qualify allowances, converter efficiency, bias currents, inrush or suspend behavior.

Migration: the former top-level scenarios/results/buck_proposal keys are removed from power_budget.json. In-repository consumers were Markdown references only; no existing code read those keys. Expanded inputs/results are in power_budget_future.json. Obsolete converter/efficiency proposals and old Rev A no-path results are available in Git history. The active current_rev_a_input key and existing numerical operating points are preserved. The hotplug paths and numerical snapshot are unchanged; its script now supports explicit output paths instead of always writing /tmp.

External scripts outside this repository, if any, need migration to schema v2. The documented audit checks local file targets, not remote availability or every Markdown fragment. CAD library checks do not establish pinmux, footprint or board electrical qualification. Open questions remain in requirements.md.
