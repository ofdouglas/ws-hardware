# Source provenance and interpretation

Status: draft provenance record · Reviewed for this scaffold: 2026-09-06

The source attachments were read from the referenced conversation “Design Board 1 MVP”, conversation ID `6a9db131-0c14-83e8-a243-a4fee3e7eb7e`. Original files are not edited or copied into this repository. This scaffold is self-contained for planning; recover the exact originals from that conversation or the project source mirror for detailed review. Temporary attachment paths are not repository dependencies.

| ID | Source | Authority / treatment |
|---|---|---|
| SRC-ARCH | WireSpaces_Board1_Bench_Architecture_First_Draft_v2.md; dated 2026-09-01 | First draft; written MCU/topology baseline plus full future bench; not a schematic spec |
| SRC-INTRO | introduction.md; “WireSpaces — Introduction” | Provisional protocol orientation; normalize terminology in authored summaries |
| SRC-DIAGRAM | WS_Board1.drawio(1).png | Topology sketch; MCU labels differ from written source |
| USR-01 | Initial user message in referenced conversation | Explicit Host terminology and reduced first-PCBA scope |
| USR-02 | Current repository setup request | Requested tree, corrected context filename, concise status/authority conventions and ADR discipline |

## Source fingerprints (SHA-256)

- `SRC-ARCH`: `22bbe6904402d59bc3ea00866a3a29f58cf57fb0ac0338f02b116f973b3e5988`
- `SRC-INTRO`: `bf625af21dbffad43e1a756068084ceab8a076983a71b15e26e32f382d7e9ebb`
- `SRC-DIAGRAM`: `29028b82e6f701de227ac75ce9e915da4024b4e5d40087c3879c0641036911a4`

## Interpretation limits

The diagram labels STM32G473CBT6 and SAMC21E15A; the written draft specifies STM32G474RBT6 and ATSAMC21G17A-AUT. The MCU selection follows the written text and is now explicitly accepted by USR-15 (ADR-004). The written ring is directed and excludes the gateway; do not derive direction from the sketch's arrowheads.

The full draft's freeze summary includes backbone, power and test features beyond the user's reduced MVP. ADR-003 records the override; Board 1 requirements explicitly mark remaining scope questions. USB/VCP, debug and the four-node networking core are proposed carry-forward items, not newly claimed approvals.

No current manufacturer datasheet, erratum, distributor inventory, KiCad symbol or footprint was validated in this setup pass. Source-stated packages/resources and electrical targets remain unverified until the corresponding design work is completed. The protocol documents mentioned by the introduction were not supplied and are not treated as reviewed.

## USR-03 — USB design input (2026-09-06)

User has FT232HL (DigiKey 768-1101-1-ND) and is considering SC189ZSKTRT (SC189ZSKCT-ND; ownership corrected by USR-11), prefers USB-B, and requests USB power/VCP design. The circuit proposal records manufacturer-indexed evidence and retrieval limitations. Earlier statements about no datasheet validation describe the initial scaffold; this follow-up adds limited excerpt review, not complete part/pin validation.

User follow-up resolves B1-Q007: Board 1 Spin A can be exclusively USB-powered and requires the PC on; later respins add external connectors and advanced power. Prefer adaptable components but defer detailed future-power design. This accepts operating scope, not every part or circuit in the proposal.

## USR-04 — accepted power architecture, VCP speed and crystals (2026-09-06)

User accepts the power architecture and power-off UART isolation. Requests 12 Mbaud gateway VCP, STM32 at 168 MHz, short traces and hardware flow-control signals. All four MCUs must have external crystals. Onboard UARTs target several Mbaud with exact rates unspecified; only gateway VCP needs 12 Mbaud. ADR-001 records power acceptance; ADR-005 records clock/speed requirements. Calculations and reviewed primary-source excerpts are linked in boards/board1/clocking.md; acceptance is distinct from component/pin/bench validation.

## USR-05 — Rev A external buses and expanded USB estimate (2026-09-06)

User specifies FD_CAN_A, FD_CAN_B, all onboard UARTs, VCP and one external RS-485 in Rev A. Both CANs and RS-485 go to terminal connections with ground(s). Added transceivers and connections belong to later revisions. Requests a transceiver search and 500 mA USB estimate for all planned RS-485 plus STM32-only CAN3. Expanded calculation assumes three total RS-485 PHYs from the full draft and nine CAN PHYs total. Primary-source links, dated sourcing limitations and numerical assumptions are in boards/board1/transceivers_and_power.md. ADR-006 records scope; part choices remain proposed.

## USR-06 — Board 1 power reduction and family-scope clarification

User selects TCAN3413DR, limits external RS-485 to 12 Mbps, and descopes the multidrop RS-485 from Board 1's expanded design while retaining LEFT/RIGHT p2p ports. Explicit follow-up: this does not remove RS_485_MULTIDROP from the overall WS bench architecture. Requires one LED per MCU, a board power LED and a few GPIOs per MCU on breakouts. LED current, exact GPIO count/load allowance and THVD1420 selection are assistant proposals, not accepted component specifications.

## USR-07 — Rev A dual-gateway lab rationale

User reaffirms one external STM32 RS-485 port in Rev A after considering its removal for power savings. User owns a Digi ConnectCore 93 development kit, reported to expose two CAN-FD interfaces and one RS-485 interface. Connecting Board 1 to all three enables a dual-gateway lab. This is user-provided equipment context; exact kit revision, pinout, electrical mode, supported rates and termination have not been verified. The zero-RS485 alternative was discussed but not accepted. Existing USB-only Rev A scope remains in force; adding 24 V was discussed, not accepted.

## USR-08 — converter efficiency design target

User requests a concrete buck converter design to meet the new 90% worst-case efficiency target and permits an alternate IC. This accepts the efficiency objective, not the assistant-proposed TPS62902, passive choices, 92% internal qualification margin or temperature/load envelope. Manufacturer sources and USB maximum-voltage correction are recorded in buck_converter.md.

## USR-09 — assembly constraints and brief converter search

User finds the proposed QFN difficult to solder and requests a brief search for efficient, easier-to-solder bucks. Explicit project rule: prefer exposed SMT leads; QFN needs justification; BGA excluded unless existential. Available tools are soldering iron and hot air; avoid the smallest passives. ADR-009 records this. No replacement converter is selected by this instruction.

## USR-10 — SC189 evaluation

User supplies typical SC189 efficiency plots and requests further evaluation. The plots are reference data, not instructions or approval. Full SOT23-specific curves and passive/startup constraints are discussed in boards/board1/sc189_evaluation.md. No MPN is newly accepted and the 90% target is not narrowed.

## USR-11 — SC189 ownership correction and TPS62046 candidate

User explicitly corrects earlier ownership interpretation: SC189 is not on hand and was only being considered. FT232HL ownership is unchanged. User proposes TPS62046DGQR for evaluation, noting its underside pad. No converter is selected by this message. Current notes have been corrected; ADR-001 historical text has a correction addendum.

## USR-12 — DigiKey sourcing and future two-stage power

User requires all parts to be sourced from DigiKey, proposes TPSM84203EAB for consideration, and clarifies the intended future power chain: 24 V input -> protection -> 5 V buck -> bridge/sequencing and 3.3 V buck -> MCUs/transceivers. This records future direction, not promotion of external power into Rev A or acceptance of the candidate converter. See boards/board1/tpsm84203_evaluation.md.

## USR-13 — full-load efficiency and SC189 capacitance

User clarifies that light-load efficiency is irrelevant: efficiency matters to support all transceivers at full load from VBUS. SC189 is promising if capacitance permits; asks for a decoupling proposal under 30 uF. B1-R023 now explicitly uses this full-load criterion. Earlier 100–600 mA efficiency-floor interpretations are superseded by this clarification; no exact SC189/passive selection is accepted yet.

## USR-14 — SC189 selection and current BOM

User accepts proceeding with SC189 and the proposed decoupling, and requests a readable BOM containing exact and category-only selections. The accepted conversation revision shares STM32 analog bulk and increases each SAM bulk to 1 uF. Retain the 10 uF buck capacitor; 2x4.7 uF was not accepted. Preferred values are a convenience, not a reason to violate electrical requirements. ADR-010 records selection separately from pending validation.

## USR-15 — official MCU selection (2026-09-06)

In the current MCU-pinout task, the maintainer states: “`STM32G474RBT6` and three `ATSAMC21G17A-AUT` are officially selected, update the documents to record that.” This accepts one gateway and three leaves under ADR-004 / B1-R001. The accompanying request for oscillator and SWD/debug/flash options authorizes proposals, not acceptance of those implementation choices. Pin allocations and exact-device implementation evidence remain unverified.

## USR-16 — owned probes, SWD headers and common crystal preference

Maintainer owns a J-Link EDU and plans to use it for this project, has a PICkit 5 if needed, and accepts the proposed 10-pin Cortex SWD headers. ADR-011 records the debug access choice. Maintainer prefers the same 12 MHz crystal for all devices and requests candidates available from DigiKey in quantity one. No exact crystal MPN is selected.

## USR-17 — common crystal selection and assembly sizes

Maintainer accepts ECS-120-18-5PX-CKM-TR in the context of a common crystal for the gateway, three SAMs and FT232HL. Smaller crystal packages are acceptable if they have leads. Maintainer finds 0805 easy, 0603 doable but small, and 0402 or smaller too small. The abbreviated “06” and “04” are interpreted as imperial 0603 and 0402 in this package discussion. ADR-012 records the crystal selection; ADR-009 has an assembly-preference clarification. Electrical qualification and load capacitors remain open.

## USR-18 — enable-only main power and UART buffer selection

Maintainer explicitly accepts omission of AP22653 from Rev A and selects SN74LV125APWR. USB protection remains open; previously suggested ESD options were unavailable at DigiKey. See ADR-013.

## USR-19 — smaller crystal selection and draft SAM allocation

On 2026-09-06 the maintainer explicitly says “commit to ECS-120-20-3X-EN-TR” after the smaller-package comparison, and requests a draft SAMC21 pin-allocation spreadsheet. ADR-014 records the replacement common-part selection. The previously disclosed FT232HL accuracy conflict remains open; this instruction does not establish electrical compatibility or acceptance of the generated pin assignments.

## USR-20 — USB ESD selection and protection scope

Maintainer selects RCLAMP0504S.TCT and requests polarity protection plus an assessment of required overvoltage robustness against USB 2.0. SMF6.0A is not selected. ADR-015 records data ESD selection; exact VBUS polarity/overvoltage circuit remains open.

## USR-21 — Rev A ESD / hot-plug scope

Maintainer explicitly omits polarity and high-voltage protection, retaining only ESD / hot-plug protection. ADR-016 records this scope. USB ESD source and ADR identifiers were renumbered to resolve collisions with the independent crystal records; crystal decisions are unchanged.

## USR-22 — FT232HL crystal accuracy exception

Maintainer asks to continue the SAM spreadsheet and find a crystal within the FT232HL accuracy budget. This authorizes a separate FTDI candidate while retaining the smaller selected MCU crystals. The proposed exact FTDI replacement is not yet expressly selected. See ADR-017.

## USR-23 — FTDI EEPROM selection and pin allocation

Maintainer has AT93C56B-SSHM-B selected on DigiKey and instructs: review it and, if suitable, commit to using it and add an FTDI pinout sheet to the existing workbook. ADR-018 records selection following compatibility review. The generated per-pad allocation is a draft, not maintainer acceptance of implemented connectivity.


## USR-24 — dedicated CBUS recovery controls

Maintainer explicitly instructs: “add dedicated CBUS GPIOs for both reset and BOOT0,” accepting the preceding ACBUS5/reset and ACBUS6/BOOT0 proposal. The maintainer confirms UART buffers are enabled after USB configuration, with the main 3.3 V domain off beforehand. ADR-023 records the selection; interface components/polarity and hardware qualification remain open.

## USR-25 — Rev A connector MPN selections (2026-09-06)

In the connector-selection task, the maintainer explicitly requests adding CNC Tech 3220-10-0100-00 (DigiKey 1175-1627-ND), Phoenix Contact 1989803, and Sullins PRPC040SAAN-RC (DigiKey S1011EC-40-ND) to the BOM as “decided.” ADR-026 records these exact MPNs as accepted in the existing debug, bus-terminal and GPIO rows. This does not accept the preceding proposed terminal order or GPIO cut schedule, or assert verified footprints/pin allocations.

## USR-26 — per-MCU debug UARTs

Maintainer requests each MCU expose a TX/RX/GND text-debug UART, assumes 115200 baud, and accepts 0.1-inch headers. ADR-032 records the scope; 8N1, electrical interface and numbered header order are implementation proposals.

## BOM reconciliation request (2026-09-06)

Maintainer requests review/correction of the BOM, promotion of already-decided choices, and candidate research for RS-485 and UART multidrop. This authorizes documentation reconciliation and proposals, not acceptance of new driver/transceiver parts. Existing ADR-027/028 authority supports splitting bridge allocations into B1-B061–065.

## USR-27 — second buffer for open-drain UART

Maintainer explicitly instructs: “commit the second SN74LV125APWR for OD UART to record,” following the grounded-A/TX-to-/OE discussion and confirmation that all four MCUs are close together. ADR-033 records the selected extra quad buffer separately from the VCP device. The accompanying CAN jumper/RS-485 fixed-termination note is a topology question and proposal, not acceptance of exact termination parts or final topology.

## USR-28 — RS-485 PHY and termination acceptance

2026-09-06: Maintainer instructs “Commit to ST3485EBDR. Commit to the termination proposal. Suggest parts for the termination resistors and jumpers.” ADR-034 accepts the PHY and previously proposed topology/counts/120 ohm value; exact resistor, header and shunt candidates remain proposed.

## USR-29 — termination part acceptance and bias investigation

2026-09-06: Maintainer asks to commit all three recommended termination parts to the BOM and investigate RS-485 idle-bus bias. ADR-035 records explicit MPN acceptance. Bias values remain recommendations pending review.

## USR-30 — RS-485 bias acceptance and TVS research

2026-09-06: Maintainer accepts the recommended 330 ohm RS-485 bias and requests CAN/RS-485 TVS recommendations. ADR-036 accepts network/value, not an unspecified bias MPN or TVS selection.

## USR-31 — CAN TVS acceptance and RS-485 TVS alternatives

2026-09-06: Maintainer selects TI ESD2CAN24DBZRQ1 and asks for another RS-485 part that fits better. In the TVS discussion this authorizes alternative protection research; it does not select a replacement transceiver or restricted common-mode envelope. ADR-037 records CAN acceptance.

## USR-32 — RS-485 TVS acceptance and remaining BOM review

2026-09-06: Maintainer accepts TI ESDS452DBZR following disclosure of its +/-5.5 V working range, then requests suggestions for unresolved BOM items. ADR-038 records selection and its disclosed interface restriction. Additional closeout proposals are not accepted.
