# Proposed FTDI supply support and EEPROM completion

Startup is settled by ADR-040. Support counts and programming details below remain proposals; no additional startup sequencer or fixture is required.

Status: proposed engineering resolution; not accepted or electrically verified. Date: 2026-09-07. Applies to unfinished item 1, B1-Q002/012, and B1-R005/012. No BOM, requirement, ADR, pinmap or workbook authority is changed by this note.

Retain the accepted FT232HL-REEL, AT93C56B-SSHM-B, independent bridge domain, TPS22810 CT=47 nF and FTDI RESET# 10 kohm/10 nF without an external supervisor. The recommended capture allocation is **eleven 100 nF capacitors, zero 1 uF capacitors, two 4.7 uF capacitors, two analog-supply ferrite beads and one EEPROM CS pull-down**. The supply-capacitor count reproduces the existing power model exactly. Startup timing is accepted under ADR-040 and does not block capture.

## Evidence reviewed

Printed page numbers are used below. Sources were accessed on 2026-09-07.

| Source | Revision and relevant pages | Review result |
|---|---|---|
| [FT232H datasheet](https://ftdichip.com/wp-content/uploads/2024/09/DS_FT232H.pdf); accessible [FTDI regional copy](https://www.ftdichip.cn/Support/Documents/DataSheets/ICs/DS_FT232H.pdf), saved as [DS_FT232H.pdf](ftdi_support_sources/DS_FT232H.pdf) | FT_000288 v2.2, 2024-09-06; pp.3, 9–14, 42–43, 45, 49–50, 52, 57 | Exact LQFP order-code family; power/EEPROM pins; bus-power drawing; defaults; electrical characteristics. Figure 6.1 was rendered and visually inspected. |
| [FTDI current product index](https://ftdichip.com/products/ft232hq/) | Current web listing advertises shared FT232H datasheet v2.3 and TN_130 v1.2 | **Document discrepancy:** the discoverable 2024 datasheet and regional download remain v2.2. Direct current product/PDF retrieval returned HTTP 403. Reconcile v2.3 before allocation verification; do not describe v2.2 as confirmed latest. |
| [TN_130 FT232H errata](https://ftdichip.com/wp-content/uploads/2020/07/TN_130_FT232H-Errata-Technical-Note.pdf); saved [TN_130.pdf](ftdi_support_sources/TN_130.pdf) from FTDI regional site | FT_000405 v1.2, 2013-03-15; pp.2–3, 7, 10–11 | Revision C has no listed electrical/timing deviations; its FT1248 status issue is outside UART mode. Revision B has a 4.3 V minimum VREGIN workaround for its internal regulator. Inspect on-hand silicon marking; do not assume C from package name. |
| [Microchip AT93C56B/AT93C66B](https://ww1.microchip.com/downloads/aemDocuments/documents/MPD/ProductDocuments/DataSheets/AT93C56B-AT93C66B-Microwire-Serial-EEPROM-Industrial-Grade-DS20006260.pdf), saved [DS20006260B.pdf](ftdi_support_sources/DS20006260B.pdf) | DS20006260B, February 2024; pp.3–9, 11–14, 17–19, 29, 31 | Exact industrial SOIC part, x16 strap, timing, startup, word/bulk commands, outline/land pattern. No separate applicable EEPROM errata was located in the [manufacturer product documentation](https://www.microchip.com/en-us/product/at93c56b); that is not a warranty that none exists. |
| [Murata ferrite specification](https://pim.murata.com/asset/pim4/ferriteBeadInductortypefilter/ENFA0005_PDF_FERRITEBEADINDUCTORTYPEFILTER?lastModifiedDatetime=20260105172120) | JENF243A_0005AE-01; pp.1, 3, 8–10 | Exact BLM21PG601SN1D electrical row, size/derating and mounting guidance. |
| [FTDI EEPROM recommendation](https://ftdichip.com/faq/what-external-eeprom-is-recommended-for-use-with-the-ftdi-usb-hi-speed-ics/) | Web FAQ | FT232H requires 93C56/66 with 16-bit words and 3.3 V I/O; not 93C46. The generic [FT_Prog troubleshooting FAQ](https://ftdichip.com/faq/what-should-i-do-when-i-cannot-program-eeprom-using-the-ft_prog-utility/) groups several devices; its generic 93C46 wording does not override FT232H-specific restrictions. |

The UM232H download was unavailable during this review. No claim below relies on uninspected module circuitry. Datasheet electrical values are used as limits only where the table actually gives limits, not where it gives a typical value.

## Supply connections and capacitor counts

Use FTDI Table 3.1 and Figure 6.1's **5 V bus-powered** arrangement. `FTDI_3V3` is VCCD's output in this arrangement, never the main rail. The following names are proposed schematic net names, not allocated reference designators.

| Device/pin | Connection | Local capacitor to GND | BOM allocation |
|---|---|---|---|
| FT232HL VREGIN 40 | Ramped `USB_5V` | 4.7 uF + 100 nF | B1-B063 x1, B1-B061 x1 |
| FT232HL VCCD 39 | Output `FTDI_3V3` | 4.7 uF + 100 nF | B1-B063 x1, B1-B061 x1 |
| FT232HL VCCIO 12 | `FTDI_3V3` | 100 nF at pin | B1-B061 x1 |
| FT232HL VCCIO 24 | `FTDI_3V3` | 100 nF at pin | B1-B061 x1 |
| FT232HL VCCIO 46 | `FTDI_3V3` | 100 nF at pin | B1-B061 x1 |
| FT232HL VPHY 3 | `FTDI_3V3` through dedicated bead to `FTDI_VPHY` | 100 nF on pin side of bead | B1-B061 x1; residual B1-B017 bead x1 |
| FT232HL VPLL 8 | `FTDI_3V3` through separate bead to `FTDI_VPLL` | 100 nF on pin side of bead | B1-B061 x1; residual B1-B017 bead x1 |
| FT232HL VCCA 37 | Separate internal 1.8 V output, no load | 100 nF at pin | B1-B061 x1 |
| FT232HL VCORE 38 | Separate internal 1.8 V output, no load | 100 nF at pin | B1-B061 x1 |
| EEPROM VCC 8 / GND 5 | `FTDI_3V3` / GND | 100 nF at package | B1-B061 x1 |
| MC74HC1G14DBVT1G VCC 5 / GND 3 | `FTDI_3V3` / GND | 100 nF at package | B1-B061 x1 |

Connect FT232HL AGND 4/9/41 and GND 10/11/22/23/35/36/47/48 to the common ground plane with short returns. TEST 42 goes directly to GND. Keep VCCA and VCORE separate. Do not export either internal 1.8 V output. Supply all three VCCIO pins. Put both beads in the 3.3 V supply branches; no additional raw-VBUS bead is proposed because the accepted attachment network already owns that circuit.

Figure 6.1 shows optional 4.7 uF positions at VPHY/VPLL as not fitted. No such footprints are proposed for Board 1. It calls for 100 nF, not 1 uF, at VCCA/VCORE. Therefore B1-B062 has **proposed quantity zero for this allocation**: retain its stable ID and accepted capacitor MPN history, which remains in use elsewhere. This is not a proposal to replace accepted capacitor MPNs or to delete an authoritative row without reconciliation.

| Existing row | Current quantity | Proposed quantity | Exact accepted MPN |
|---|---:|---:|---|
| B1-B061 | TBD | 11 | KGM21NR71E104KT |
| B1-B062 | TBD | 0 | CL21B105KAFNFNE, no required position identified here |
| B1-B063 | TBD | 2 | GRM21BR71C475KE51L |
| B1-B064 | 1 | 1, unchanged | CL21B103KBANNNC, RESET# only |

Other circuitry proposed for VCP/reset must account for its own extra capacitors separately. These counts include only the existing bridge, EEPROM and PWREN inverter.

### Residual B1-B017

Propose **two Murata BLM21PG601SN1D**, one for each VPHY/VPLL branch. Manufacturer specification p.1 gives 600 ohm ±25% at 100 MHz, 1.4 A at 85°C, 0.9 A at 125°C, and maximum DC resistance 0.14 ohm initially / 0.2 ohm after the listed tests. This is an 0805/2012 part. FTDI's reference uses 600-ohm/0.5-A beads; the candidate preserves that nominal impedance with adequate current capability. It is a dissipative high-frequency bead, not a 600-ohm DC resistor or an ideal inductor.

[DigiKey](https://www.digikey.com/en/products/detail/murata-electronics/BLM21PG601SN1D/24763118) lists exact cut-tape code `490-BLM21PG601SN1DCT-ND` (observed 2026-09-07; refresh availability before purchase). Candidate footprint: project-local equivalent of `Inductor_SMD:L_0805_2012Metric`, two nonpolar pads, with land dimensions checked against Murata's mounting guidance before verification.

At the FTDI PHY maximum 60 mA, the conservative 0.2-ohm bead bound gives 12 mV drop and 0.72 mW. A deliberately conservative 100 mA branch screen gives 20 mV and 2 mW; it is not a measured PLL current. Actual VPHY and VPLL must each stay inside 3.0–3.6 V. VCCIO's 2.97–3.63 V operating range is not a VCCD regulator-output guarantee and is not sufficient by itself to qualify the analog rails. Review the bead impedance under DC bias, MLCC effective capacitance and transient ringing when layout exists.

Propose **one additional RMCF0805FT10K0 from EEPROM CS 1 to GND**. FTDI EECS is tri-stated during reset, so this holds the active-high CS inactive without changing the accepted read/write network. At 3.63 V with 1% resistor tolerance, its maximum driven-high load is 0.367 mA; it consumes no intentional standby current when CS is low. Combined ±10 uA FTDI leakage and 3 uA EEPROM input leakage would create at most 0.131 V through 10.1 kohm, below the EEPROM 0.8 V low limit. Confirmation of any undocumented EEPROM-interface pull state remains part of capture/bench review. Do not add CS/SK pull-ups copied from optional reference positions. SK can be inactive/tri-state while CS is held low.

B1-B017 thus becomes a proposed three-part residual allocation, eventually split into stable component rows after approval. It excludes all already split B1-B051/054–058/061–065 and all new VCP/CBUS support. No supervisor, optional filter bulk capacitor or programming header is proposed.

### Charge accounting

Nominal charge arithmetic, not startup-waveform validation:

```text
FTDI direct USB_5V capacitance = 4.7 + 0.1 = 4.8 uF
Whole direct ramped capacitance = 4.8 + 10.1 (buck) = 14.9 uF
Derived 3.3 V capacitance = 4.7 + 8(0.1) + 0.01(reset) = 5.51 uF
Derived 1.8 V capacitance = 2(0.1) = 0.20 uF
Derived physical capacitance = 5.71 uF
Derived nominal stored charge = 5.51(3.3) + 0.20(1.8) = 18.543 uC
```

Those are exactly the existing `usb_input.md` planning totals; this allocation creates no nominal charge delta. Dividing 18.543 uC by a nominal 5 ms ramp gives 3.71 mA average charging demand, but the internal regulator can deliver that charge in a shorter interval. Do not add it to a 100 mA allowance and call the result USB compliant. The FTDI 54 mA VREGIN value is typical, not a guaranteed maximum; the complete initial/programmed/suspend current envelope remains B1-Q002.

## EEPROM wiring and configuration

| AT93C56B SOIC pin | Proposed connection |
|---|---|
| 1 CS | FT232HL EECS 45, plus proposed 10 kohm to GND |
| 2 SK | FT232HL EECLK 44 |
| 3 DI | FT232HL EEDATA 43 directly |
| 4 DO | EEDATA through accepted RC0805FR-072K2L 2.2 kohm; accepted B1-B065 10 kohm from DO to `FTDI_3V3` |
| 5 GND | GND |
| 6 ORG | VCC 8 directly, 128 x 16 organization |
| 7 NC | Unconnected; explicit no-connect marker |
| 8 VCC | `FTDI_3V3`, with listed 100 nF |

This follows FTDI Table 3.3, not the 2-kohm illustration in Figure 6.1. Microchip's x16 command sends eight address bits; A7 is a don't-care for 93C56B but its clock is still required. The exact `-SSHM-B` order code is industrial SOIC in bulk packaging. DS20006260B pp.17–19 show 3.9 mm body and 1.27 mm pitch; compare the existing `Package_SO:SOIC-8_3.9x4.9mm_P1.27mm` against the actual land pattern and pin-1 orientation before footprint verification.

Proposed programming profile:

| Setting | Proposed value / reason |
|---|---|
| Interface / driver | UART, VCP enabled; preserve D2XX provisioning access |
| Power | Bus-powered, 500 mA descriptor; preconfiguration operation remains limited independently of descriptor |
| Remote wake / suspend-on-ACBUS7-low | Disabled / disabled; active-PC, bus-powered scope |
| Suspend interface pull-downs | Enabled as FTDI recommends when PWREN# switches external logic; VCP receiver-pull design must account for these |
| ACBUS0 / pin 21 | PWREN#, plus existing external 10 kohm pull-up |
| ACBUS5 / pin 29; ACBUS6 / pin 30 | I/O mode for accepted reset/BOOT0 assignments; external circuits determine safe defaults |
| Other configurable ACBUS | TriSt-PU; no unused clock or LED outputs |
| UART polarity | Normal TX/RX and active-low RTS#/CTS#; baud/framing/flow control are configured by the PC application, not assumed persistent EEPROM baud settings |
| Output strength | Start at 4 mA, fast slew for the 12-Mbaud paths; confirm timing and thresholds with the isolation proposal |
| VID/PID / strings | Preserve FTDI standard identity for initial bring-up; explicit Board 1 product string and a unique recorded serial per board. Do not invent a production VID allocation. |

Absent/blank EEPROM is documented to enumerate in UART mode with VID 0403/PID 6014, no serial, bus power, 500 mA descriptor and configurable CBUS pins as pulled-up inputs. Consequently blank EEPROM does **not** provide PWREN# on ACBUS0: its external 10 kohm pull-up leaves the inverter output low and main rail off, including after blank-device enumeration. USB programming is possible while the main board remains off.

An invalid-checksum EEPROM is a separate case. The inspected FT232H documentation does not explicitly guarantee every invalid image falls back to those electrical defaults. Do not import FT-X MTP checksum behavior into FT232H. Test invalid-checksum images and interrupted word programming, then obtain manufacturer clarification if needed. A valid but wrongly programmed image is a provisioning error: assigning Drive0 to ACBUS0 defeats the intended default-off policy. The proposed resolution is an approved profile, exact readback and a recorded initial-enumeration/PWREN check, rather than claiming immunity to arbitrary valid configuration data.

## Startup and programming

Use the conventional FTDI startup arrangement accepted in ADR-040. FTDI documents integrated power-on reset and the external EEPROM interface; absence of a separately guaranteed internal read delay is not demonstrated incompatibility. No reset fixture or new sequencing circuit is required.

Complete the normal programming/readback procedure. Microchip specifies individual WRITE/ERASE over 1.7–5.5 V, but ERAL/WRAL only at 4.5–5.5 V: preserve this concrete command restriction for the 3.3 V EEPROM. Verify the tool uses supported operations during provisioning; do not change the shared EEPROM rail to 5 V.

At bring-up, check blank-device enumeration, program/readback of the reviewed profile, normal power-cycle startup and suspend/resume. Use datasheet power-cycle guidance for recovery. Investigate detailed timing or corrupt-image cases if observations warrant it; they are not prerequisites to capture.

## Remaining implementation

Finalize enumerated supply connections, capacitor counts, beads, CS default and programming profile. Retain source revision and silicon checks without treating a newer-document retrieval failure as an electrical fault. B1-Q002/012 remain open for these details and later bring-up; their startup decision is settled. No new parts or quantities are accepted by this note.

Checks performed: read current authority map and applicable scope records; inspected exact manufacturer pin/command tables and rendered FTDI power drawing; reviewed TN_130; reconciled capacitor counts and stored-charge arithmetic; checked candidate bead's exact manufacturer row and DigiKey code. No schematic exists to compare for implemented connectivity, and no ERC, hardware timing, FT_Prog programming or USB compliance test was performed.
