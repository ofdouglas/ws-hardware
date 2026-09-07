# Board 1 transceivers and USB power budget

Status: draft implementation/estimate · Decisions: ADR-002, ADR-007 · Input: USR-06

## Scope and part status

- Rev A: eight TCAN3413DR CAN PHYs, all onboard UARTs and VCP, one external RS-485, CAN/RS-485 signal terminals with ground, four MCU LEDs, one main-power LED, and a few GPIO breakouts per MCU.
- Expanded Board 1: nine CAN PHYs total (third CAN has only the STM32 PHY), two RS-485 PHYs total for RS_485_LEFT and RS_485_RIGHT point-to-point segments.
- RS_485_MULTIDROP is outside Board 1's current scope. It remains part of the overall WS bench architecture; older RS485_SHARED is its historical name. No family-level signal or backbone pair has been deleted.
- TCAN3413DR is selected by the user. Do not routinely reopen the 3.3 V CAN choice. Pin/footprint, termination and protection review remain open.
- External RS-485: ST3485EBDR selected by ADR-034; 12 Mbps ceiling retained. Termination topology accepted; electrical/bias/protection and footprint qualification remain open B1-Q009.

ST3485EBDR is the selected half-duplex 3.3 V PHY. Use [ST DS2947 Rev12](https://www.st.com/resource/en/datasheet/st3485eb.pdf) for final loaded-current and bias design. Existing numeric allowances are planning estimates; no savings are taken.

## Current assumptions

Machine-readable model: [power_budget.json](power_budget.json). Inputs remain estimates until the circuit and workload are measured.

| Load / condition | Nominal | Conservative sensitivity | Rail |
|---|---:|---:|---|
| FTDI/EEPROM/always-on controls allowance | 80 mA | 100 mA | USB input |
| STM32 at 168 MHz, including activity allowance | 45 mA | 65 mA | 3.3 V |
| Each SAM, assuming 48 MHz for estimation | 15 mA | 25 mA | 3.3 V |
| Other logic/oscillator/pull-up allowance, excluding LEDs and external loads | 15 mA | 25 mA | 3.3 V |
| Each TCAN3413, recessive including VIO allowance | 7.05 mA | 8.25 mA | 3.3 V |
| Each TCAN3413, dominant including VIO allowance | 42.3 mA | 60.3 mA | 3.3 V |
| Each transmitting RS-485, loaded allowance | 60 mA | 75 mA | 3.3 V |
| Five LEDs, all on | 2.5 mA | 2.5 mA | 3.3 V |
| Aggregate breakout load reservation | 20 mA | 20 mA | 3.3 V |
| USB voltage / buck efficiency assumption | 5 V / 90% | 4.4 V / 85% | NA |

The TCAN figures are based on the datasheet's 60-ohm typical and 50-ohm maximum-load cases; termination is already included. [TCAN3413 §5.6](https://www.ti.com/lit/ds/symlink/tcan3413.pdf). MCU allowances exceed CPU-only reference measurements and are not verified maxima: [ST Table 25](https://www.st.com/resource/en/datasheet/stm32g474rb.pdf), [Microchip Table 45-11](https://ww1.microchip.com/downloads/aemDocuments/documents/MCU32/ProductDocuments/DataSheets/SAM-C20-C21-Family-Data-Sheet-DS60001479J.pdf).

Retain the earlier 60/75 mA loaded RS-485 allowances pending ST3485EBDR circuit qualification; do not claim unmeasured savings from that substitution. The earlier THVD1450 study highlighted the importance of a 54-ohm load. [Original loaded-current reference](https://www.ti.com/lit/ds/symlink/thvd1450.pdf). The revised miscellaneous allowance has the same numeric value as before, with LEDs now explicitly additional; this intentionally takes no savings credit for the previous implicit LED allowance.

## Calculation

```text
I_CAN = N_PHY*I_recessive + N_bus*d*(I_dominant-I_recessive)
I_board_3V3 = I_GW + 3*I_SAM + I_misc + I_CAN + N_RS*I_RS + 5*I_LED
I_USB = I_bridge + 3.3*(I_board_3V3 + I_breakout)/(V_USB*efficiency)
```

Loaded scenarios retain d=0.5, one principal local CAN transmitter per bus and every local RS-485 transmitter continuously enabled. CAN arbitration/ACK/error phases can have multiple drivers; these are workload averages, not instantaneous or bus-fault bounds. RS-485 is assumed half duplex per port, with both point-to-point endpoints terminated. Driver disable while receiving can reduce average draw, but no such saving is credited in the loaded table.

| Scenario | Rev A board only | Rev A + breakout reserve | Expanded board only | Expanded + breakout reserve |
|---|---:|---:|---:|---:|
| Active MCUs, PHYs listening | 201 mA | 215 mA | 206 mA | 221 mA |
| Nominal loaded | 270 mA | 285 mA | 332 mA | 347 mA |
| Conservative loaded sensitivity | 418 mA | 436 mA | 515 mA | 532 mA |

Dropping one transmitting RS-485 saves approximately 44 mA nominal or 66 mA conservative at USB input. Five 0.5 mA LEDs add only 1.8–2.2 mA there. Bare breakout headers have negligible static consumption; the proposed 20 mA external-load reserve adds 14.7–17.6 mA USB input.

Rev A retains useful estimated margin. Expanded Board 1 remains above 500 mA in the conservative loaded sensitivity case, even without an external breakout load. Treat 400 mA sustained USB input as a proposed design target, leaving 100 mA of headroom; it is not yet achieved or accepted as a validated limit. Current TPS560430 efficiency and all load allowances need refinement; SC189 is superseded. Startup, suspend and bus faults require separate budgets.

## Concrete power reductions to carry into design

1. Use high-efficiency LEDs at a proposed 0.5 mA nominal each, not conventional multi-milliamp drive. Put the power LED on 3V3_SYS so it indicates main-board power and turns off in suspend. Each MCU gets its own controllable LED. Select actual LED/resistor values and worst-case current together; PWM may reduce typical draw but all-on is budgeted.
2. Drive RS-485 DE only around frames; disable promptly after the last stop bit and while receiving. Reserve both DE and /RE control. Do not increase termination resistance merely to improve the budget. Compare ST3485EBDR loaded current at our actual rates before claiming savings; keep 3.3 V operation.
3. Expose each CAN PHY standby control. Enter standby only when the experiment does not require that interface; this must not silently disable simultaneous-link capability. Account for re-entry/wakeup timing.
4. Gate unused MCU peripherals, analog blocks and clocks; use DMA and sleep when idle. Preserve 168 MHz gateway/12 Mbaud capability. Replace broad MCU allowances with measured or explicitly itemized currents instead of lowering them to make the arithmetic fit.
5. Check the FTDI domain as a separate optimization. Its 80/100 mA allowance is not a measured current. A future proposed implementation change could use a separate always-on efficient 3.3 V converter if silicon revision permits, but it must preserve independent enumeration power and cannot use switched 3V3_SYS. Do not change the accepted 5 V reference implementation yet; added converter overhead and suspend behavior may outweigh savings. FTDI limits the 3.3 V input configuration to suitable silicon revisions. [FT232H §5.2](https://ftdichip.com/wp-content/uploads/2024/09/DS_FT232H.pdf)

No standby/duty-cycle/firmware/converter saving is booked in the table. In the conservative expanded case with breakout reserve, roughly 32 mA must be removed just to reach 500 mA, and roughly 132 mA to reach the proposed 400 mA design target. If the required continuous workload cannot meet that target, later external power remains the straightforward option.

## LEDs and GPIO breakout implementation

Reserve one LED control per MCU, independently of the requested spare GPIOs. Propose four GPIOs per MCU plus ground on breakout headers, subject to a complete pinmux audit; the user requirement is a few pins, not a frozen count of four. Avoid consuming crystal/SWD/boot pins or changing strap levels. Keep outputs high-impedance by default until firmware configures them. Header signals are logic I/O, not guaranteed power outputs; no new power-export pin is implied.

The 20 mA aggregate allowance is a placeholder covering externally loaded outputs across all four MCUs, not 20 mA per pin or a guarantee of per-port capability. Verify MCU pin/port/package limits, load capacitance, switching power, clamp injection and externally powered peripherals before defining the breakout electrical contract. The GPIO source-strip MPN is decided in B1-B027; cut schedule, protection, series resistance and pins remain open.

## Terminal interface retained

Rev A still exposes both CAN pairs and its one RS-485 pair plus ground(s). Existing 8-position/two-ground proposal remains: FD_CAN_A_H, FD_CAN_A_L, GND, FD_CAN_B_H, FD_CAN_B_L, RS485_A, RS485_B, GND. Phoenix 1989803 and 2.5 mm pitch are decided by 026-reva-connectors.md / B1-B022; final terminal order remains open. Maintain physical-end termination, short stubs and protected external interfaces. Signal grounds are retained regardless of Board 1's omission of the bench multidrop port.

## Updated converter proposal — USR-08

The 4.4 V / 85% cases above remain historical sensitivity estimates. Current [buck proposal](buck_converter.md) uses a 4.5 V USB-B boundary, explicit 50 mV input-path allowance and a proposed 92% converter qualification goal, giving approximately 407 mA Rev A / 495 mA expanded with the same conservative loads. This goal is unqualified; new scenarios are separate in power_budget.json. Rev A retains its one RS-485.
