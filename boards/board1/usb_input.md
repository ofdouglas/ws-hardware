# Board 1 Rev A USB input circuit

Status: power/USB schematic captured; approval and bench qualification pending. Updated: 2026-09-07. Authority: ADR-021 (buck/current criterion), ADR-022 (input). Current implementation note. Earlier revisions are retained in Git history.

## Circuit and placement

```text
USB-B VBUS -- VBUS_RAW -- TPS22810DBVT -- USB_5V
                |          VIN1 OUT6       |-- FT232HL VREGIN
                |                         |    4.7 uF + 100 nF to GND
                |                         +-- TPS560430X3FDBVR VIN5
                |                              10 uF + 100 nF to GND
                +-- SMF6.0A -- GND
                +-- 1 uF ---- GND
                +-- 1 ohm -- 4.7 uF -- GND

TPS22810: GND2 -> GND; EN3 -> VIN1; CT4 -> 47 nF -> GND;
          QOD5 -> OUT6.
FTDI RESET#34 -> 10 kohm -> FTDI 3.3 V; RESET#34 -> 10 nF -> GND.
FTDI PWREN# -> MC74HC1G14DBVT1G (FTDI_3V3 supply) -> TPS560430 EN4.
Accepted pulls (ADR-028/030): PWREN# 10 kohm to FTDI_3V3; EN 47 kohm to GND.
Inverter local 100 nF is from existing FTDI-domain control allocation (ADR-024).
USB D+/D- -> RCLAMP0504S.TCT -> FTDI D+/D- (ADR-015).
```

No TLV803E or parallel precharge path. The 1 ohm resistor carries damping-capacitor current, not board DC current. TVS cathode to VBUS_RAW, anode to ground; place beside connector with short ground return. Put the direct bypass and damping branch beside switch VIN/GND, and each load's input bypass at its own pins. Use a common ground plane. The draft bonds connector shield directly to GND at entry, a conventional bench implementation; review the physical bond at layout.

Raw input selections: B045 CL21B105KAFNFNE (1 uF 25 V X7R), B046 CL21A475KBQNNNE (4.7 uF 50 V X5R), B047 SG73P2BTTD1R0J (1 ohm +/-5%, 1206 pulse resistor), and CT B048 CL21B473KBCNNNC (47 nF 50 V X7R). ADR-029 accepts the X5R and 5% changes. Effective capacitance and hot-plug qualification remain open. See bom.csv for current exact MPNs; all sourcing through DigiKey.

## Operating estimates and limits

- USB connector design envelope: 4.5–5.5 V. Total configured current <=500 mA; preconfiguration current <=100 mA. The provisional whole DC input-path resistance is 0.12 ohm, not a verified component-corner bound. At 500 mA it drops 60 mV, giving 4.44 V at the buck for a 4.5 V connector. At 5.5 V connector and light load the output can approach 5.5 V; the circuit is not a 5 V regulator.
- TPS22810 VIN operating 2.7–18 V; absolute maximum 20 V. DBV current rating 2 A is not USB current permission or a 500 mA limiter. At 0.5 A, typical switch loss is about 20 mW; about 26 mW with 105 milliohm (5 V, up to 85 C condition). Exact low-VIN/temperature/path corner remains to check.
- FTDI VREGIN operating 3.6–5.5 V for the 5 V configuration. Do not infer a VREGIN transient absolute maximum from a different FTDI pin's rating.
- TPS560430 VIN operating 4–36 V; absolute maximum 38 V; output rating 600 mA. Accepted 12 uH/22 uF output filter and existing distributed bypass total 34.41 uF require loop/startup review. The rating does not permit 600 mA output under every USB operating point.
- CT=47 nF: nominal slew 0.9919 V/ms, 4.03 ms 10–90% at 5 V; linear full-rise estimates 4.54–5.55 ms for 4.5–5.5 V. TI's timing data assume VIN steady before EN; VIN-tied-EN and worst-case slew are unverified. Buck internal soft start is 1.8 ms typical (10–90% reference, specified at 12 V); it begins after EN and is not a reset-release delay.
- Direct ramped input C: 4.8 uF FTDI + 10.1 uF buck = 14.9 uF. Nominal charging current 14.78 mA, or 18.70 mA with capacitance factor 1.265 only; neither is a guaranteed maximum because slew and internal-regulator startup vary. FTDI derived/control caps add 5.71 uF physical and 18.543 uC nominal stored charge; do not count them as direct 5 V caps or omit their startup demand.
- Raw bypass+damping+conservatively counted CT: 5.747 uF nominal, 7.270 uF with factor 1.265, about 39.98 uC at 5.5 V before TVS/parasitics. The resistor does not remove its capacitor's attachment charge. This is a charge screen, not USB inrush qualification.

## Whole-board current model

Main 3.3 V load: 184.6 mA listening, 279.15 mA nominal loaded, 380.55 mA conservative loaded. Last case includes STM32 65 mA, three SAMs 75 mA, miscellaneous 25 mA, CAN 118.05 mA, RS485 75 mA, five LEDs 2.5 mA and breakout reservation 20 mA. Bridge/control allowance is 80 mA nominal or 100 mA conservative, including allowance for input control/leakage. These are planning loads, not proven maxima. In particular CAN assumes 50% dominant duty and normally one transmitting driver per bus; arbitration/ACK/error overlaps, different workloads and faults require separate review. RS485 allowance remains deliberately coarse.

Using the 0.12 ohm path and solving Iusb=Ibridge+P3v3/[eta*(Vconnector-0.12*Iusb)]:

| Workload | Connector | Buck efficiency assumption | USB current | Margin to 500 mA |
|---|---:|---:|---:|---:|
| Nominal loaded | 5.0 V | 90% | 286 mA | 214 mA |
| Conservative loaded | 4.5 V | 90% | 414 mA | 86 mA |
| Conservative loaded | 4.5 V | 85% | 432 mA | 68 mA |
| Conservative loaded | 4.5 V | 80% | 453 mA | 47 mA |
| Conservative loaded | 4.5 V | 75% | 477 mA | 23 mA |

Break-even at 500 mA and 4.44 V is 70.71% (the previous 4.45 V approximation gave 70.55%). There is no fixed 90% criterion. Current model is in [power_budget.json](power_budget.json) under `current_rev_a_input`. True worst-case board current and minimum converter efficiency remain unverified.

## Unresolved questions / acceptance checks

1. Qualify selected input passives: ceramic bias/tolerance, damping resistor pulse curve, layout, shield connection and TVS behavior. SMF6.0A has a 6 V standoff, not a 6 V clamp. Measure FTDI rail peaks for plug-in, brief interruption/replug and already-powered ESD; switch on-state does not block overvoltage. No sustained high-voltage or polarity protection is in scope.
2. Prove preconfiguration input waveform <=applicable USB inrush/current limits with FTDI startup, and configured startup/resume <=500 mA requirements. The 100 mA bridge allowance alone cannot be used as a startup maximum while adding capacitor current on top.
3. MC74HC1G14DBVT1G is selected (ADR-024); verify accepted support pulls and FTDI reset/high-impedance, suspend and brownout behavior. Keep UART isolation receivers safe during all main-rail transitions. External supervisor is removed; abnormal slow input ramps are not claimed supervised.
4. Validate selected buck LC network, output transient response and efficiency at actual full network load; validate the provisional current, DC-path and ambient envelopes. No bench measurements, current-limit guarantee or final worst-case budget exist yet.
5. Whole-board suspend-current accounting including FTDI, TVS leakage, switch IQ and disabled buck; EEPROM configuration must match bus-power behavior.

## Sources

[TI TPS22810](https://www.ti.com/lit/ds/symlink/tps22810.pdf), [TI TPS560430](https://www.ti.com/lit/ds/symlink/tps560430.pdf), [FTDI FT232H v2.2](https://www.mouser.com/datasheet/3/35/1/DS_FT232H.pdf). Main-current assumptions and primary sources are retained below. Selection is not qualification.

## Related implementation

[USB bridge and isolation](usb_vcp.md), [buck passives](buck_tps560430.md), [decoupling](decoupling.md), [current BOM](BOM.md). PWREN# pull-up is RMCF0805FT10K0; EN pull-down is ERJ-6GEYJ473V. The captured B1-B061–063 counts reconcile to the existing 14.9 uF direct input and 5.71 uF derived/control allocation (18.543 uC), so the nominal charge model is unchanged. The six B1-B079 pull-ups add at most 1.32 mA on main 3.3 V and 0.66 mA on FTDI_3V3 when held low; these fit inside the existing miscellaneous/bridge planning allowances, not an independently validated maximum budget. Reconcile the accepted RS-485 bias and UART_MD pull-up loads with the existing allowances before claiming a worst-case budget. Question status remains in [requirements](requirements.md) (B1-Q002/011).

## Retained load and passive qualification evidence

Planning 3.3 V allowances (nominal/conservative): gateway 45/65 mA; each SAM at an assumed 48 MHz 15/25 mA; miscellaneous logic 15/25 mA; each recessive CAN PHY including VIO 7.05/8.25 mA; each dominant PHY including VIO 42.3/60.3 mA; loaded RS-485 60/75 mA. Five LEDs add 2.5 mA and aggregate breakout reservation adds 20 mA. Neither reservation is a per-pin rating. CAN calculation is N_PHY*I_recessive + N_bus*0.5*(I_dominant-I_recessive), not a simultaneous-all-drivers fault bound.

Sources: [TCAN3413 section 5.6](https://www.ti.com/lit/ds/symlink/tcan3413.pdf) (60-ohm typical/50-ohm maximum-load cases), [ST MCU Table 25](https://www.st.com/resource/en/datasheet/stm32g474rb.pdf), [SAM Table 45-11](https://ww1.microchip.com/downloads/aemDocuments/documents/MCU32/ProductDocuments/DataSheets/SAM-C20-C21-Family-Data-Sheet-DS60001479J.pdf). The RS-485 allowance originated in a [loaded THVD1450 study](https://www.ti.com/lit/ds/symlink/thvd1450.pdf); retaining it for ST3485EBDR is a planning assumption, not an exact-part maximum. No firmware duty-cycle or standby savings are booked.

For the selected SG73P2BTTD1R0J damping branch, a 5.5 V ideal step and 0.95 ohm minimum R give 31.84 W initial pulse power. Upper screened C=4.7*1.10*1.15=5.9455 uF stores 89.93 uJ; nominal-C RC spans 4.465–4.935 us from resistor tolerance alone. [KOA SG73P pp.1–2](https://www.koaspeer.com/pdfs/SG73P.pdf), reviewed 04/16/26, rates 2B at 1 W with applicable temperature derating and a one-pulse curve reaching 1 us. Numerical curve margin and repeated-hotplug drift remain unverified; these ideal RC calculations do not bound cable ringing or ESD. [Samsung B046 evidence](https://product.samsungsem.com/mlcc/CL21A475KBQNNN.do) specifies X5R: retain its -55 to +85 C range and check bias/aging, not just voltage rating.

The five CSL1901DW1 LEDs use accepted RK73H2ATTD3301F 3.3 kohm resistors. At assumed Vf=1.8 V, current is 0.455 mA and resistor power 0.682 mW. [ROHM](https://www.rohm.com/products/led/chip-leds-mono-color-type/standard/csl1901dw-product) specifies typical brightness/Vf at 2 mA; visibility and Vf at this lower current are not guaranteed. Power LED uses 3V3_SYS; MCU LEDs have separate controls from spare GPIOs. Verify all-on current and GPIO drop under B1-Q010.

Expanded Board 1 (future scope only) has nine CAN PHYs and two point-to-point RS-485 PHYs. Legacy expanded sensitivities are isolated in [power_budget_future.json](power_budget_future.json); they are not current Rev A limits. See [model conventions](models.md).


Complete-capture support-current screen:32 main-domain10k pull resistors at3.35V and-1% resistance draw at most10.83mA when every relevant signal opposes its pull. The470ohm UART_MD pull-up adds at most7.20mA held low, totaling18.03mA within the existing25mA conservative miscellaneous allowance. The RS-485330ohm bias pair draws approximately4.7mA with two120ohm terminations and low resistor corners; retain it inside the deliberately coarse75mA loaded RS-485 allowance pending measurement. These are allocation screens, not validated whole-board maxima. The20mA external-load reservation remains conservative; no new load allowance or efficiency criterion is introduced.
