Status: historical; superseded by ADR-022. Do not use as the current circuit.

# Board 1 Rev A VBUS input design

## Current review — TPS560430 and faster attachment ramp

ADR-021 selects TPS560430X3FDBVR instead of SC189. The circuit below is the earlier input baseline; substitute the new buck functionally, but reselect its LC network before CAD. The user proposes TPS22919DCKR to eliminate the slow-ramp/reset-supervisor complexity.

TPS22919: typical tON 1.95 ms, 10–90% rise 1.28 ms and slew 3.2 mV/us at 5 V. Values are typical, not guaranteed bounds. The buck's 1.8 ms soft start begins AFTER EN; it is not a delay on PWREN# and does not prove ramp completion. Fast attachment ramp followed by ordinary USB enumeration can avoid the intentional 100 ms ramp race; abnormal slow supply ramps and brownouts are separate cases.

Two unresolved constraints: (1) TPS22919 IN/ON absolute maximum is 6 V, while SMF6.0A does not clamp below 6 V, so it cannot simply replace the 18 V TPS22810 in this raw-input network; (2) old 14.9 uF downstream allocation without supervisor bypass draws 47.68 mA nominal charging current at 3.2 mV/us, before FTDI operating/internal-regulator startup current and capacitor/slew tolerance. Preconfiguration 100 mA must be checked independently of postconfiguration 500 mA.

Proposed simpler alternative: retain TPS22810 but change CT from 1 uF to 47 nF, and omit TLV803E after validating attachment sequencing. Nominal slope becomes 0.9919 V/ms, 4.03 ms 10–90% at 5 V, about 5 ms full swing; 14.9 uF charging is about 14.8 mA. This retains voltage headroom, avoids a deliberately long ramp and reduces charging current relative to TPS22919. It is a proposal, not a BOM population change. Validate VIN-tied-EN power-up, FTDI default-off behavior, USB attach/replug and regulator startup. Buck filter/input capacitance changes must be reflected in these estimates.

The FTDI remains a voltage-sensitive load regardless of buck choice. Neither load switch is an overvoltage cutoff. Raw TVS plus damping remains an ESD/hotplug design requiring downstream waveform validation, not a guarantee of a <=6 V rail. Do not describe this unresolved protection as qualified.

Sources: [TPS22919](https://www.ti.com/lit/ds/symlink/tps22919.pdf), [TPS22810](https://www.ti.com/lit/ds/symlink/tps22810.pdf), [TPS560430](https://www.ti.com/lit/ds/symlink/tps560430.pdf).

## Earlier selected input baseline — under review

Status: selected implementation baseline; electrical qualification pending. Date: 2026-09-06. Authority: ADR-019 (input ramp), ADR-020 (supervised reset). Filename retained for existing links. Supersedes the earlier delayed-enable proposal and its passive values.

## Circuit

```text
USB-B VBUS ---- VBUS_RAW ---- TPS22810DBVT ---- USB_5V
                  |            VIN1 VOUT6        |-- FT232H VREGIN: 4.7 uF + 100 nF
                  |                             |-- SC189 VIN: 10 uF + 100 nF
                  +-- SMF6.0A -------- GND
                  +-- 1 uF ---------- GND
                  +-- 1 ohm -- 4.7 uF -- GND

TPS22810DBVT: GND2 -> GND; EN3 -> VIN1; CT4 -> 1 uF -> GND;
              QOD5 -> VOUT6.
TLV803EA42RDBZR: VDD3 -> USB_5V; GND2 -> GND; RESET1 -> FTDI RESET#34.
                 VDD3 -> 100 nF -> GND; RESET1 -> 10 kohm -> FTDI 3.3 V.
FTDI PWREN# -> default-off inversion/control -> SC189 EN (ADR-013/020).
```

TVS cathode to raw VBUS, anode to ground. The 1 ohm resistor is ONLY in the capacitor shunt, never in the board's DC supply path. Place TVS at the connector with a short ground return; place bypass, damping network and switch together. Retain SC189 and FTDI local input capacitors at their respective pins.

Remove the previous 220 kohm / 100 kohm divider, EN capacitor, discharge diode and 1 kohm resistor. No parallel precharge resistor. EN follows VIN using the switch's internal UVLO. QOD uses the internal discharge resistor. TPS22810 stays enabled during USB suspend; SC189 EN controls the main domain. UART isolation and USB data protection remain ADR-013/015.

## Selected input parts

| Item | Selection | Assembly / rating |
|---|---|---|
| VBUS TVS | SMF6.0A | SOD-123F |
| Slew-controlled switch | TPS22810DBVT | SOT-23-6; use DBV pinout above |
| Direct VIN bypass | 1 uF X7R, <=10%, 25 V | 0805/1206; select for >=1 uF effective at 5.5 V if practicable; nominal value is not effective capacitance |
| Damping branch | 1 ohm, 1%, pulse-rated + 4.7 uF X7R, <=10%, 25 V | 1206 preferred; qualify resistor pulse curve and ceramic DC bias |
| CT | 1 uF X7R, <=10%, >=10 V | 0805 preferred; verify effective capacitance at up to 2.5 V |

Exact passive MPNs remain TBD, sourced from DigiKey. The direct bypass is retained because TI section 12 calls for low-ESR ceramic bypass at VIN; the 1 ohm damping branch does not replace that recommendation. One 1 uF replaces the earlier two. No new capacitance is added to the SC189 3.3 V output allocation.

## Timing and power

CT = 1 uF gives an estimated slew of 0.04662 V/ms using TI's approximate formula. At 5 V this is 85.8 ms from 10% to 90%, or roughly 107 ms across the full swing if extrapolated linearly. This is a nominal sizing estimate: TI's tabulated data stop at 27 nF and assume VIN stable before EN; this design ties EN to VIN. Confirm actual insertion behavior on hardware, rather than claiming a guaranteed 100 ms delay or monotonicity from this calculation.

The direct 15.0 uF (including supervisor bypass) charges at approximately 0.699 mA at that nominal slope, about 0.885 mA with the 1.265 capacitance upper factor. FTDI operating current and internal regulator startup add to this; the result is not total USB inrush. Slowly charging the bulk capacitors creates margin without a separate precharge timer.

TLV803EA42RDBZR holds FTDI in reset until USB_5V crosses its rising threshold and the internal reset delay expires. Nominal falling threshold is 4.2 V; rising is about 4.25 V, conservatively at most 4.34826 V including accuracy/hysteresis. Delay is nominally 200 ms (130–270 ms at datasheet test conditions). See ADR-020 for timing-condition limits. FTDI then enumerates, and PWREN# enables SC189 through the default-off interface. SC189 must remain disabled while FTDI is reset/high-impedance/unpowered and during suspend. A brownout resets FTDI and must shut down the main domain.

PWREN# alone is not power-good. The supervisor removes dependence on enumeration taking longer than the ramp; actual ramp completion and low-voltage behavior remain prototype checks. Do not claim an exact 5 V release threshold. The selected E-series part differs from legacy TLV803M and uses the R pinout. Retain the existing 10 nF reset capacitor and count the 10 kohm pull-up once under B1-B051.

At 0.42 A switch loss is about 14 mW typical / 19 mW using 105 milliohm, with a 33/44 mV drop. Retain the previous provisional 0.12 ohm total input path allowance and approximately 414 mA configured full-load estimate at 4.5 V connector / 90% buck efficiency. These are estimates, not measured worst-case guarantees.

## Capacitance reconciliation

FTDI v2.2 Figure 6.1 (page 45) was visually inspected. It shows 4.7 uF + 100 nF on VREGIN, 4.7 uF + 100 nF on VCCD, 100 nF on VCORE and VCCA, and 100 nF on each VCCIO. VPHY and VPLL each use a 600 ohm / 0.5 A ferrite and 100 nF; the additional 4.7 uF at each is explicitly N.F. (not fitted). Retain that baseline. Use X7R capacitors with effective capacitance verified for the internal regulator; the figure itself is not a ceramic-bias qualification. An additional 100 nF for our PWREN control is a design reserve. The 10 nF RESET# node is counted separately, and oscillator pF capacitors are negligible at this budget resolution. The old reference's common VBUS bead / 10 nF bypass is replaced by the input network in this proposal; do not duplicate it. Propose 0805 ferrites for the two analog branches, exact MPN pending impedance/DCR review.

| Domain / location | Selected allocation | Nominal total | Attachment behavior |
|---|---|---:|---|
| VBUS_RAW bypass | 1 x 1 uF | 1.00 uF | Direct, low-ESR local bypass |
| VBUS_RAW damping branch | 4.7 uF + series 1 ohm | 4.70 uF | Count in attachment charge despite resistor |
| Input-switch controls | 1 uF CT | 1.00 uF | Conservatively count as if charged to raw VBUS voltage |
| TLV803E VDD | 100 nF | 0.10 uF | Behind input ramp; B1-B050 |
| SC189 VIN | existing 10 uF + 100 nF | 10.10 uF | Behind input ramp; retained |
| FT232H VREGIN | 4.7 uF + 100 nF | 4.80 uF | Behind input ramp; proposed |
| FTDI VCCD / 3.3 V | 4.7 uF + 100 nF | 4.80 uF | Behind FTDI regulator |
| FTDI VCCIO | 100 nF at each of 3 pins | 0.30 uF | Behind FTDI regulator |
| FTDI VPHY | 100 nF; optional 4.7 uF NOT fitted | 0.10 uF | Behind 600 ohm at 100 MHz / 0.5 A ferrite; exact MPN pending |
| FTDI VPLL | 100 nF; optional 4.7 uF NOT fitted | 0.10 uF | Behind separate 600 ohm at 100 MHz / 0.5 A ferrite; exact MPN pending |
| FTDI VCORE | 100 nF | 0.10 uF | Internal 1.8 V rail |
| FTDI VCCA | 100 nF | 0.10 uF | Internal 1.8 V rail |
| FTDI EEPROM | 100 nF | 0.10 uF | FTDI 3.3 V domain |
| PWREN inversion/control reserve | 100 nF | 0.10 uF | FTDI 3.3 V domain |
| FTDI RESET# | 10 nF through 10 kohm pull-up | 0.01 uF | Charge from FTDI 3.3 V; not direct VBUS |
| Main SC189 output | existing allocation | 22.61 uF | Disabled until configuration; unchanged |

Direct raw/control allocation is 6.7 uF nominal, conservatively counting CT as if charged to VBUS. With +10% initial and +15% temperature it is 8.4755 uF, or 46.615 uC at 5.5 V, before TVS/parasitics. CT actually operates at a lower voltage. This is a conservative charge screen, not proof of USB inrush compliance; the resistor does not remove the damping capacitor's charge from the accounting.

The direct ramped 5 V allocation is now 15.0 uF (previous 14.9 uF plus supervisor bypass). FTDI derived/control capacitors add 5.71 uF physical (5.51 uF at 3.3 V plus 0.2 uF at 1.8 V), storing 18.543 uC nominal. The main 22.61 uF and SAM core capacitors start separately when SC189 is enabled.

## Implementation checks

- Select exact DigiKey passives, checking effective capacitance and damping-resistor pulse capability. A 5.5 V charge of 4.7 uF stores about 71 uJ nominal; ringing/contact bounce and peak pulse power must also be considered.
- Measure insertion/replug/brownout, FTDI enumeration and SC189 startup/resume over supply, cable and load variation. Check preconfiguration 100 mA, configured 500 mA and total suspend budget, including switch IQ and TVS leakage.
- Check input/output overshoot, undershoot and unplug reverse body-diode current. QOD is not reverse-current blocking. The old vbus_hotplug_model.py/json describe the superseded network and do not validate this simplified circuit.
- Validate board-level ESD with actual layout. SMF6.0A's specified pulse clamp can exceed SC189's 6 V absolute maximum; TPS22810 is not an overvoltage cutoff when on. Downstream transient voltage therefore remains a measurement requirement, not a guaranteed clamp claim. Sustained overvoltage and polarity protection remain out of scope under ADR-016.

The circuit and nominal values are settled for schematic implementation. Layout, exact passive sourcing and prototype qualification remain explicit work; they are not implied complete by selection.

## Sources

- [TI TPS22810 Rev C, sections 9.3.3–9.3.4, 10.3–10.4 and 12](https://www.ti.com/lit/ds/symlink/tps22810.pdf).
- [FTDI FT232H v2.2, Figure 6.1](https://www.mouser.com/datasheet/3/35/1/DS_FT232H.pdf).
- [Littelfuse SMF datasheet](https://www.mouser.com/datasheet/2/240/Littelfuse_TVS_Diode_SMF_Datasheet.pdf-1698977.pdf).
- [USB-IF specification and ECNs](https://www.usb.org/documents?search=usb+2.0).

See [ADR-020](../../docs/decisions/020-ftdi-supply-reset.md) for supervisor threshold margins, exact DigiKey ordering code and reset qualification.
