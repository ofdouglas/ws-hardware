# Board 1 remaining qualification

Complete schematic capture has enumerated all components, connectors and support networks. [CSV](bom.csv) owns quantities/MPNs; [CAD notes](kicad/README.md) describe239objects/872pins and checks. No fitted-component count or connectivity choice remains TBD. B007/B010/B017 are zero residual aggregates; B023/B060 are actual default resistors; B075 is six dedicated two-post ground headers.

Remaining work is approval and bring-up: Eeschema ERC, exact electrical/errata checks, final connector sample/cable/land-pattern and probe-clearance review, layout/DRC, power/current/startup measurements, oscillator qualification, firmware and link-rate tests. [Requirements](requirements.md) owns question status. Measurements and physical layout do not prevent complete draft capture.

Selection/evidence status is intentionally not upgraded merely because a part was captured. New default networks reuse existing selected MPNs as routine engineering choices. All sourcing remains DigiKey, with stock refresh before ordering. No fabrication release or procurement-ready BOM is claimed.
