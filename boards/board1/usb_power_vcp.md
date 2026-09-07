# USB power and VCP — circuit proposal

Current input authority: ADR-022. TPS22810 CT is 47 nF; TLV803E B1-B049 and bypass B1-B050 are omitted (quantity zero). B1-B051 10 kohm RESET# pull-up and existing 10 nF remain. Direct ramped capacitance is 14.9 uF pending final buck CIN review. [Current circuit and operating points](vbus_protection_proposal.md) supersedes earlier input descriptions below.

Current authority: ADR-021 selects TPS560430X3FDBVR and total USB current <=500 mA as the efficiency criterion. SC189-specific converter/filter and 30 uF ceiling statements below are historical; MCU/transceiver decoupling remains. Input-switch simplification is under review, not yet qualified.

Status: draft implementation; current authority ADR-020 (supervised reset), ADR-019 (input), ADR-013 (enable/isolation); power/isolation architecture accepted in ADR-001 · Updated: 2026-09-06 · Decision: ADR-001
Requirements: B1-R005, B1-R006, B1-R012 · Questions: B1-Q002, B1-Q007

User input USR-03: FT232HL is on hand; SC189ZSKTRT was only being considered (USR-11 correction); USB-B is preferred. Use these as design candidates. The user subsequently accepted USB-only operation requiring an active PC for Spin A (B1-Q007). Regulator/support circuitry remains proposed; advanced power and external connectors are deferred to later respins.

## Historical circuit partition (superseded by ADR-013)

```text
USB 2.0 Standard-B
  D+/D- -> low-capacitance ESD -> FT232HL -> UART isolation -> GW UART
  VBUS  -> input protection -> USB_5V
                                |-> FT232HL / configuration EEPROM
                                |     (independent of main-board power)
                                |
                                +-> controlled-ramp load switch -> 5V_SYS
                                      |                            |-> 5 V loads, if selected
                           USB configuration control               +-> main buck -> 3V3_SYS
                                                                        |-> MCU / logic loads
```

Common ground; UART isolation here means power-off signal isolation, not galvanic isolation. Switch control must default OFF independently of MCU firmware. B1-Q007 is resolved: Spin A requires an active PC and is exclusively USB-powered. The proposed switch implementation powers down the main board during suspend. Charger-only use and uninterrupted operation during PC sleep are outside Spin A scope.

## USB connector and bridge

Prefer a full-size, right-angle, through-hole USB 2.0 Standard-B receptacle with mechanical shell anchors. Exact MPN, footprint and shield bonding remain B1-Q004. D+/D- connect only to the bridge; native STM32 USB remains deferred. Use a short matched differential route over continuous reference ground; select ESD parts for USB high-speed use and check routing against the final stackup. Do not copy arbitrary series resistors or crystal capacitances into the schematic.

FT232H facts reviewed from indexed manufacturer datasheet v2.2: with VREGIN at 5 V, VCCD is a 3.3 V output; all VCCIO pins require supply; VPHY/VPLL require the documented filtered supply arrangement; VCORE/VCCA are internal 1.8 V outputs. Proposed: use the documented 5 V bus-powered circuit for the bridge and keep its supply separate from 3V3_SYS. Do not tie the two regulator outputs together or use the bridge regulator for the main board. [FTDI §3.3 and §6.1](https://ftdichip.com/wp-content/uploads/2024/09/DS_FT232H.pdf)

Plan an external 12 MHz crystal with load components selected for its actual specification. [FTDI H-series factsheet](https://ftdichip.com/wp-content/uploads/2025/08/h-chip-series-factsheet-en-v1.pdf)

Fit B1-B013, the selected AT93C56B-SSHM-B per [ADR-018](../../docs/decisions/018-ftdi-eeprom.md). Strap ORG to VCC for 16-bit organization and power it from FTDI VCCD (3V3_FTDI), independently of 3V3_SYS. The FTDI sheet linked in [pinmap](pinmap.md#draft-ftdi-and-eeprom-allocation) includes all eight EEPROM pads.

EEDATA connects directly to DI and through 2.2 kohm to DO; a 10 kohm pull-up goes from DO to 3V3_FTDI (FT_000288 v2.2 Table 3.3). Propose a local 100 nF 0805 bypass, counted with the EEPROM resistors in B1-B017, separate from main-rail capacitance. Exact MPNs and full support circuit remain TBD.

B1-Q012 tracks DS20006260B pp.8–11 constraints: maximum 1 MHz at 3.3 V, up to 5 ms word-write cycle, supply rise no faster than 0.1 V/us, at least 100 us after stable supply before commands, and at least 500 ms at 0 V between full power cycles. Check FTDI reset/read timing and unplug/replug recovery. Confirm FT_Prog word programming/readback at 3.3 V; bulk erase/write require the higher supply range. The part selection is accepted; these circuit checks remain unverified.

Programming proposal: UART mode; VCP enabled; bus-powered descriptor sized to actual approved load; unique board serial; an ACBUS output assigned PWREN#; suspend pull-down enabled. PWREN# is active low after configuration and inactive in suspend. [FTDI §3.4, §7](https://ftdichip.com/wp-content/uploads/2024/09/DS_FT232H.pdf)

Route TX/RX through circuitry with specified partial-power-down behavior; provide RTS/CTS alongside TX/RX per ADR-005. Do not directly attach DTR/RTS to MCU reset/boot by default. Keep signal paths disabled until the main rail is valid and prevent injection into an unpowered MCU. A resistor alone is not proof of power-off isolation. Isolation component, direction, enables and default pulls need review.

## Historical buck proposal (superseded by ADR-010)

USR-08 adds the 90% minimum efficiency target. [buck_converter.md](buck_converter.md) proposes TPS62902RPJR and a complete passive/control network under ADR-008. Its 92% qualification goal leaves input-path margin. Component selection and measurements remain pending. The following SC189 section is retained as the earlier assessment, not the preferred current implementation.

## Earlier SC189 assessment

The candidate is fixed 3.3 V in SOT23-5. The SC189 family specifies 2.9–5.5 V input, up to 1.5 A output, 2.5 MHz switching, enable and internal soft start. These features are suitable in principle for USB-derived 5 V to 3.3 V. [Semtech overview](https://www.semtech.com/products/power-management/buck-converters/sc189); exact variant supplied by user.

Proposed connection: VIN from switched 5V_SYS; output network to 3V3_SYS; EN defaults inactive until its local supply/control is valid. Do not drive EN above its permitted voltage while VIN is off. A simple EN-to-local-VIN arrangement is a candidate if upstream switching provides the required sequence. Final SOT23-5 pin mapping and L/C values remain unverified. Select the inductor for peak/saturation current and DCR; capacitors for effective capacitance under DC bias; verify ripple, load-step response and thermal rise with the actual PCB. Avoid sizing from the current headline alone.

A buck is preferable to a main-board LDO if measured load is substantial: at an illustrative 300 mA, a 5 V -> 3.3 V LDO dissipates (5-3.3)*0.3 = 0.51 W. That is our calculation, not a Board 1 load estimate. The SC189 needs layout and passive-component review; no evidence found in this pass justifies discarding the SC189 candidate before those checks.

## USB power states and budget

Implementation update: ADR-013 replaces all load-switch instructions below with SC189 EN control. SC189 input capacitance is directly attached to USB; input protection and inrush/startup validation remain open.

For the ordinary USB data-port model, budget no more than 100 mA before configuration, no more than the declared/allowed current up to 500 mA afterward, and at most 2.5 mA during suspend. These apply to the entire device at VBUS, not each rail. [USB-IF interoperability procedure §2.2](https://www.usb.org/sites/default/files/3.2%20Interoperability%20Testing%20v0.99%20w%20USB%20Type-C.pdf)

| State | Bridge domain | Main board | Required behavior |
|---|---|---|---|
| Cable absent | Off | Off | No alternative power injection in this proposal |
| Attached, unconfigured | On | Off | Enumerate and permit EEPROM programming within startup budget |
| Configured, active | On | On, controlled ramp | Total draw within descriptor and port allowance |
| USB suspend | Low-power state | Off | Isolation and leakage must meet total suspend budget |
| Resume | On | Restart | Reset/rail sequencing; firmware restarts cleanly |
| USB charger without enumeration | May receive VBUS | Off | Outside Spin A operating scope |

PWREN#-controlled load switching and independent bridge I/O power follow FTDI's bus-powered module guidance. Keep main input capacitance behind the switch; account separately for directly attached capacitance and both attachment/startup inrush. Program and read back the EEPROM before expecting the main board to start. Blank EEPROM behavior must keep the switch safely off. [UM232H §7.2](https://ftdichip.com/wp-content/uploads/2020/07/DS_UM232H.pdf)

Select a switch with suitable enable polarity/level, default OFF, controlled ramp and fault behavior. Do not assume a 3.3 V control can fully turn off a discrete PMOS whose source is at 5 V; use a reviewed level interface or a compatible integrated switch. Input protection and the main switch have separate jobs. A polyfuse alone does not establish USB current compliance.

Planning equation (currents at their named rails):

```text
I_USB = I_bridge_domain + I_direct_5V_loads
      + (3.3 * I_3V3_SYS) / (V_USB * efficiency) + other_losses
```

For illustration only: V_USB=5 V, efficiency=0.90, bridge/control allowance=80 mA, direct 5 V loads=100 mA, total ceiling=500 mA gives I_3V3_SYS <= 436 mA before margin. None of those load allowances is a verified Board 1 maximum. Lower input voltage or efficiency reduces the result. The regulator's 1.5 A capacity does not guarantee a 1.5 A USB-powered rail. CAN PHY selection and simultaneous dominant-state currents are major remaining inputs.

## Evidence limits and next checks

Manufacturer-indexed excerpts were accessible; direct downloads were blocked. FTDI currently lists v2.3, while reviewed technical excerpts are v2.2. Reconcile the current full datasheet and TN_130 against the on-hand silicon revision before schematic pin assignment. Read the complete SC189 datasheet, exact package drawing and application network before freezing passives. No full datasheet/errata sign-off, CAD, electrical simulation, or bench measurement has been performed.

B1-Q007 records the accepted operating scope; B1-Q002 remains responsible for the complete budget, support parts, controlled switching and validation. Bench checks: pre-configuration current, EEPROM readback, main-rail ramp, worst-case active draw, suspend current, resume behavior, serial loopback/traffic, off-state UART leakage, regulator ripple and temperature.

## Later respins

Keep USB_5V, the bridge's local supply and 5V_SYS/3V3_SYS distinct in naming and layout. Future external power can feed a redesigned main power path while preserving the VCP function. Candidate parts should be reviewed for supply sequencing and unpowered I/O tolerance; this does not imply the current circuit is already multi-source capable. Revisit source isolation, VBUS detection, bridge self/bus-power mode, descriptors, signal isolation and regulator reverse-current paths when external input is introduced. Do not add external-power connectors, ORing, 24 V conversion or debug-power injection now. ADR-006 explicitly adds Rev A signal terminals for two CANs and one RS-485. The SC189 could remain a downstream 3.3 V converter behind a suitable future 5 V supply; it is not a future high-voltage input stage.

## USR-04 acceptance and speed update

The user accepts independent bridge power, controlled main-board power and UART power-off isolation. All four UART signals (TX/RX/RTS/CTS) cross that boundary. The gateway VCP must support 12 Mbaud with a 168 MHz STM32 and suitable USART clocking; see [clocking.md](clocking.md) and ADR-005. Exact support components and power budget remain unverified implementation details. Accepted architecture is not reopened merely because component selection is unfinished.

Updated whole-board estimate: [transceivers_and_power.md](transceivers_and_power.md). This includes Rev A terminal access and one RS-485, and separately evaluates future added PHYs.

## SC189 follow-up — USR-10

[Detailed SC189 evaluation](sc189_evaluation.md) now reviews SOT23 curves, exact pin functions, passive constraints and 100 µs internal soft start. The 30 µF total-output-capacitance recommendation must be audited against all main-rail decoupling. This is an evaluation candidate, not an accepted replacement or a qualified 90% floor.

Current selection — USR-19 / [ADR-014](../../docs/decisions/014-smaller-12mhz-crystal.md): smaller common crystal selected for the four MCU oscillators; ADR-017 separately proposes an accurate FT232HL crystal; qualification remains B1-Q008; see BOM B1-B014/019/020. Earlier candidate/unselected statements are historical. Load networks and electrical/pad/footprint qualification remain open under B1-Q008/B1-Q005. Assembly: 0805 preferred, 0603 acceptable, no 0402 or smaller; smaller crystals may be considered if leaded.

## Earlier implementation — ADR-013 (input attachment superseded by ADR-019)

USB input protection -> USB_5V -> independent FTDI branch and SC189 VIN. FTDI PWREN# -> always-powered default-off inverter/control -> SC189 EN. No AP22653 or separate main load switch. SN74LV125APWR powered from 3V3_SYS isolates all four UART signals. See ADR-013 for accepted choices and remaining verification. SC189 and its decoupling are selected under ADR-010; older candidate statements above are historical.

## USB data ESD selection — ADR-015

RCLAMP0504S.TCT selected for D+/D-. ADR-016 limits VBUS protection to ESD/hot-plug; polarity and sustained high-voltage fault protection are omitted. VBUS transient suppression/damping and inrush validation remain open. Do not treat SMF6.0A as a guaranteed polarity blocker or SC189 overvoltage limiter.

## Proposed insertion protection and reconciled input capacitors

See [VBUS protection proposal](vbus_protection_proposal.md): SMF6.0A plus delayed TPS22810DBVT ramp upstream of both power domains. This proposes a change to ADR-013 based on input-capacitance/inrush reconciliation; it is not accepted and does not change the selected BOM. FTDI v2.2 Figure 6.1 was visually checked. The proposal includes component values, capacitor accounting, model assumptions and qualification limits.

## Current input baseline — ADR-019

Use [the finalized VBUS circuit](vbus_protection_proposal.md): SMF6.0A, TPS22810DBVT, 1 uF CT, EN tied to VIN, direct 1 uF bypass and shunt 1 ohm + 4.7 uF. This supersedes earlier input-path and unaccepted-proposal statements above. Both FTDI and SC189 input capacitance are behind the ramp; PWREN# still controls SC189 EN. Exact passive MPNs and hardware qualification remain open.

## FTDI reset sequencing — ADR-020

Select TLV803EA42RDBZR powered from USB_5V, holding FTDI RESET# low until the 4.2 V threshold plus hysteresis and internal 200 ms nominal release delay are satisfied. Open-drain output uses a 10 kohm pull-up to independent FTDI 3.3 V. Add one 100 nF on USB_5V; retain existing 10 nF RESET# capacitor. FTDI reset/high-impedance must leave SC189 disabled. [ADR-020](../../docs/decisions/020-ftdi-supply-reset.md) supersedes unsupervised-startup assumptions; TPS22810 remains selected.


## Gateway reset and ROM boot control — ADR-023

Dedicated CBUS GPIOs control gateway reset and BOOT0 via B1-B053; see [pinmap](pinmap.md#dedicated-gateway-recovery-controls). Keep both paths safe while the main domain is off. Defaults are reset released and BOOT0 low. Reset must coexist with the SWD probe without driving NRST high. Exact interfaces/polarity remain B1-Q013. Existing SN74LV125 UART channels are fully allocated.

USR-24 confirms UART buffers enable after USB configuration while the main domain is off beforehand; no application-firmware enable is required for ROM communication. On Linux use ftdi_sio/libgpiod for CBUS and the tty interface for programming, preserving RTS/CTS for application traffic. Verify option bytes and keep other ROM-probed interfaces quiet during recovery.
