# Connector and crystal footprint checks

Board-authored footprints live in [Board1.pretty](Board1.pretty), registered with `${KIPRJMOD}` in [fp-lib-table](fp-lib-table). Both parsed successfully in pcbnew and are used in the [initial unrouted placement](placement.md). Standard libraries are also explicitly registered with portable KiCad paths. Placement checks do not establish final mechanical qualification.

| Part | Drawing and checked geometry | Footprint |
|---|---|---|
| CNC Tech3220-10-0100-00 | [Manufacturer drawing](https://www.cnctech.us/pdfs/3220-XX-0100-00_.pdf),2020-02-05,p1:1.27mm grid,0.70mm drills,12.70x5.00mm body | Board1:CNC_Tech_3220-10-0100-00_2x05_P1.27mm_Vertical |
| Phoenix1989803 | [Manufacturer product](https://www.phoenixcontact.com/en-us/products/printed-circuit-board-terminal-ptsa-05-8-25-f-1989803), body drawing42764 and drill drawing21170:21.5x12mm body,2.5mm pitch,1.0mm drills,row7.3mm from rear,first pad2.75mm from left edge | Board1:PhoenixContact_PTSA_0.5_8-2.5-F_1989803 |
| ECS-120-20-3X-EN-TR | [CSM-3X Rev2017](https://www.ecsxtal.com/store/pdf/CSM-3X.pdf),p1Fig2:3.5x1.2mm pads centered±2.75mm | Standard Crystal:Crystal_SMD_ECS_CSM3X-2Pin_7.6x4.1mm matches |
| PRPC040SAAN-RC cut sections / PRPC002SAAN-RC |2.54mm through-hole grid; four8-position cuts, two2-position CAN jumpers and six dedicated2-position ground headers | Standard vertical1x08/1x02 P2.54 footprints |

Before layout approval, confirm physical connector pin1/wire orientation, housing clearance, terminal actuation access and the actual Cortex cable key. SWD pin7 is electrically NC but the selected header has a physical contact; check whether the owned cable blocks position7 and prepare the mating contact as necessary. No claim of physical sample fit or assembled-board testing.

Existing power/USB footprints remain unchanged and retain their earlier layout qualification notes. Numbered-pad coverage is checked for every full-board symbol by the native-netlist checker; mechanical dimensions and electrical qualification are separate.
