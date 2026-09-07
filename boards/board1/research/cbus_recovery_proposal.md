# Board 1 MCU reset and CBUS recovery proposal

Status: proposed, unaccepted, allocation evidence unverified · Researched 2026-09-07

Scope: unfinished item 3, B1-Q005/013; implements B1-R007/024 and ADR-004/011/023. No accepted ADR, question status, BOM, workbook or CAD was changed. Component names below are review labels, not assigned schematic references.

## Recommendation

Use one **SN74LVC2G06DBVR dual open-drain inverter**, powered by **3V3_SYS**, and one **DMP2035U-7 P-channel MOSFET**. These provide active-high `RESET_REQUEST` and `BOOT_REQUEST` from the already allocated CBUS5 and CBUS6. Add explicit receiving-node defaults and per-MCU reset support; omit physical reset buttons for this first capture. SWD provides four independent resets, CBUS provides gateway recovery, and reset test pads can use the accepted test-access scope.

**The recovery circuit alone does not make the present pad allocation safe in ROM.** The draft PB14 RS-485 DE assignment conflicts with a ROM-driven SPI output. Resolve that allocation and review CAN/USART activity before relying on firmware-independent recovery. The concrete conflicts and recommended disposition are below.

## Proposed wiring

All grounds below join Board 1 ground. Keep both accepted LV125 devices and all their channels intact.

| Element | Connection |
|---|---|
| U_REC SN74LVC2G06DBVR, DBV SOT-23-6 | pin 5 VCC → 3V3_SYS; pin 2 GND → GND; local 100 nF |
| Reset input | FT232HL ACBUS5 pad 29 / B1-P261 → U_REC pin 1 (1A); 2.2 kohm from this input to GND |
| Reset output | U_REC pin 6 (1Y) → 330 ohm → gateway NRST pad 7 / B1-P175; SWD reset reaches NRST directly |
| Gateway NRST node | 10 kohm to 3V3_SYS and 100 nF to GND at STM32; no bridge-domain pull-up |
| Boot input | FT232HL ACBUS6 pad 30 / B1-P262 → U_REC pin 3 (2A); 2.2 kohm from this input to GND |
| Boot gate | U_REC pin 4 (2Y) → Q_BOOT gate; gate pulled to Q_BOOT source by 10 kohm |
| Q_BOOT DMP2035U-7, SOT-23 | source → 3V3_SYS; drain → 2.2 kohm → PB8/BOOT0 pad 61 / B1-P229; BOOT0 → 10 kohm → GND |
| Each SAM reset | RESET pad 40 → independent SWD reset; 2.2 kohm to 3V3_SYS and 100 pF to GND at MCU |

DMP2035U's manufacturer top view places gate/source on the two-lead side and drain on the opposite lead (standard SOT-23 candidate mapping 1=G, 2=S, 3=D). **Confirm the numbered symbol/footprint against the selected manufacturer's package before capture sign-off**; no generic footprint equivalence is marked verified here. The TI pin numbers are tabulated explicitly in its datasheet p.3.

The 330 ohm reset branch limits the discharge current from the STM32 filter capacitor; it is not in series with SWD. The BOOT0 series 2.2 kohm reuses a selected resistor value and limits current if PB8 is accidentally configured as an output. Keep PB8 reserved as boot input in application firmware. Q_BOOT's body diode points from its drain toward its source; BOOT0 has no independent supply to feed it. This interface is not intended to tolerate externally powering BOOT0.

Power U_REC from the **main** rail: its partial-power-down rating permits bridge inputs while main power is off. If the bridge collapses while the main capacitor remains charged, the input pulldowns still select the safe default through valid main-powered logic. Below the logic's 1.65 V operating limit, do not claim a truth-table guarantee; check reset/recovery at bring-up together with MCU POR/BOR; this does not reinstate the withdrawn VCP rail-monitor proposal. Powering the inverter from the bridge instead would leave its outputs unspecified during bridge collapse while the MCU might still run.

## Default truth table and calculations

With 3V3_SYS valid:

| CBUS5 | CBUS6 | Gateway NRST | BOOT0 | Intended use |
|---|---|---|---|---|
| Low or high-Z | Low or high-Z | Released; SWD may still assert | Low | Normal/default |
| High | Low | Asserted | Low | Hold/reset normal boot |
| High | High | Asserted | High | Prepare ROM entry |
| Low | High | Released | High | ROM programming |

With 3V3_SYS off, U_REC is unpowered, its outputs are high impedance within its Ioff specification, and Q_BOOT cannot source from the absent main rail. CBUS outputs therefore have no intended DC supply path into STM32 reset/boot. Leakage and transitions must still be included in the power budget.

Using the FTDI Table 5.3 limits (40 kohm minimum internal pull-up; 3.6 V rail upper bound; ±10 uA tristate leakage) and TI ±5 uA input leakage, a 2.2 kohm +1% input pulldown gives a conservative high-Z input estimate:

`Vdefault <= 3.6 × 2222/(40000+2222) + 15 uA × 2222 = 0.223 V`.

This is below TI's 0.8 V VIL limit at 3.0–3.6 V. At an actively driven FTDI low, 0.4 V remains below that limit. FTDI's 2.4 V minimum high exceeds TI's 2.0 V VIH. The pulldown draws at most about 1.65 mA at 3.6 V, within FTDI's 2 mA output-voltage test load. These are datasheet arithmetic checks, not measured results.

At nominal 3.3 V, BOOT0 high is approximately `3.3 × 10/(10+2.2) = 2.70 V`; minimum resistor-ratio fraction with 1% resistors is 0.817. This exceeds the STM32 0.7×VDD CMOS high requirement; account for input leakage, MOSFET on resistance and any enabled internal pull before verification. BOOT0 source current is approximately 0.27 mA; Q_BOOT gate pull current while asserted is approximately 0.33 mA.

TI guarantees VOL ≤0.4 V at a much larger 16 mA load with VCC=3 V. Conservatively combining that bound with the 330 ohm branch and gateway pull-ups (10 kohm external in parallel with 25 kohm minimum internal) gives NRST about 0.54 V at 3.6 V, below 0.3×VDD. The nominal gateway release time constant is about `(10k || 40k) ×100nF = 0.8 ms`. Proposed software waits of 10 ms around reset comfortably exceed this estimate; they are initial settings to verify.

## Parts and ownership for later reconciliation

Every quantity here is a **proposal delta/detail**, not a procurement-ready BOM. Reuse of an accepted MPN does not accept its new use. Retain B010/B053 IDs when splitting their placeholders into detailed rows later.

| Owner | Proposed item | Quantity | Purpose |
|---|---|---:|---|
| B1-B053 | Texas Instruments SN74LVC2G06DBVR, SOT-23-6 | 1 | Two digital-threshold open-drain control channels |
| B1-B053 | Diodes Incorporated DMP2035U-7, SOT-23 | 1 | Main-supplied BOOT0 source switch |
| B1-B053 | Yageo RC0805FR-072K2L, 2.2 kohm 1% 0805 | 3 | Two CBUS input pulldowns and BOOT0 series resistor |
| B1-B053 | Stackpole RMCF0805FT10K0, 10 kohm 1% 0805 | 2 | Q_BOOT gate pull-up and BOOT0 pulldown |
| B1-B053 | Stackpole RMCF0805FT330R, 330 ohm 1% 0805 | 1 | Reset sink branch |
| B1-B010 | RMCF0805FT10K0 | 1 | Gateway NRST pull-up |
| B1-B010 | RC0805FR-072K2L | 3 | Three SAM RESET pull-ups |
| B1-B010 | KEMET C0805C101J5GACTU, 100 pF 5% 50 V C0G 0805 | 3 | Three SAM reset filters |
| B1-B010 | KYOCERA AVX KGM21NR71E104KT, 100 nF 25 V X7R 0805 | 1 | Gateway reset filter, additional to supply bypass allocation |
| B1-B036 | KGM21NR71E104KT | 1 existing reserve | U_REC supply bypass; claim one of the two remaining auxiliary reserves, coordinate with VCP enable logic |

No pushbutton, button resistor, spare buffer channel, extra connector or DNP footprint is proposed. All new package choices have exposed SMT leads or 0805 terminations. Exact footprint review and DigiKey sourcing refresh remain pending; no stock or price is claimed.

Microchip DS60001479M §53.5 pp.1226–1228 distinguishes a basic example (100 kohm/39 ohm/4.7 nF) from an EFT example (2.2 kohm/330 ohm/100 pF). The recommendation above uses the latter pull/filter values with no button. Its 330 ohm **button branch** is absent because there is no button. It is not a debounce circuit or a claimed EFT qualification. ST DS12288 Rev.6 pp.133–134 recommends 100 nF at NRST and documents the internal pull-up; the added 10 kohm external pull is a Board 1 implementation proposal.

## ROM-entry policy and pin conflicts

Retain STM32G474RBT6, CBUS endpoints and USART2 PA2 TX / PA3 RX. During initial SWD provisioning, read back and explicitly set/check `nSWBOOT0=1`, `nBOOT1=1`, `BOOT_LOCK=0`, and `NRST_MODE=0b11` (reset input/output). Retain ordinary user-flash boot with BOOT0 low. Keep `nBOOT0=1` as a fallback if software-selected boot is later used; do not silently enable bank swapping or protection. Do not set irreversible readout protection. These settings need exact-device option-byte readback; factory defaults must not be assumed.

AN2606 Rev.70, Pattern 14 p.35 and Table 117 pp.279–281, supports pin-controlled ROM entry and USART2. Its ROM runs from internal clocks at 72 MHz; the application 168 MHz/12 Mbaud plan does not apply. Start programming at **115200 baud, 8E1, no hardware flow control**, using the USART synchronization byte 0x7F and a supported STM32 ROM programming tool. The selected VCP buffer must enable without application firmware. Check actual ROM ID and limitations before deciding supported programming commands/rates.

The following are consequences of comparing AN2606's ROM initialization with the current workbook, not accepted reallocations:

| Draft allocation | ROM behavior / issue | Proposed disposition |
|---|---|---|
| PB14 = RS-485 DE | SPI2 MISO can actively go high on ROM startup | Move DE to PD2, LQFP64 pad 55 / B1-P223, currently UNUSED: use GPIO software DE with 10 kohm pulldown. DS12288 Table 12 p.69 confirms the package pad; it is absent from ROM Table 117. Set DE before transmitting and clear only after USART TC, with PHY delays included. A weak pulldown on the old PB14 cannot defeat its active output. |
| PC6/PC7 = CAN PHY standby | I2C4 open-drain pins with pulls | Move the two gateway standby controls to PB7 pad 60 / B1-P228 and PB9 pad 62 / B1-P230, both currently UNUSED and absent from ROM Table 117; fit 10 kohm pull-ups and leave high until application firmware enables the PHYs. Exact pin/package and electrical checks remain B1-Q005/013. Do not assume a pull-up overrides an actively low ROM I2C output. |
| PA11/PA12 = CAN1 RX/TX | USB DFU initializes these pads | Demonstrate no output contention with the RX driver and no harmful CAN transmission. Disable/isolate the gateway PHY in recovery or change the draft mapping if required. Merely disconnecting the external CAN cable does not remove the local transceiver. |
| PB12/PB13 = CAN2 RX/TX | SPI2 NSS/SCK inputs | Check local RX activity cannot select the wrong bootloader and ensure PHY standby/default TX remains safe. |
| PA9/PA10 = UART_MD TX/RX | ROM also probes USART1 | Keep all SAM transmitters quiet until USART2 synchronization succeeds. This operational constraint must be part of the supported bench recovery setup. |
| PC10/PC11 = RS-485 TX/RX | ROM also probes USART3 | Keep RS-485 disabled and its receive side quiet during ROM selection. |
| PA5 = LED | ROM SPI1 clock input | Temporary LED behavior is acceptable for recovery, but check its loading cannot cause false SPI selection. |

Recommended dependent-control allocation is therefore PD2→RS-485 DE, PB7→gateway CAN A STB, PB9→gateway CAN B STB. PC12 remains /RE with an explicit high default. Their three new 10 kohm pulls belong to residual interface support B023/B007, not B010/B053; the /RE default belongs to the separate RS-485 control closeout. Preserve stable pad IDs and mark the old PB14/PC6/PC7 functions unused only when the coordinated proposal is accepted/implemented. GPIO DE trades hardware timing for software turnaround, so test USART TC handling at the selected RS-485 rate. PC8 is unsuitable as a supposedly ROM-unused alternative because ROM uses it for I2C3.

The proposed **bench recovery contract** requires no external CAN frames during entry, RS-485 DE low and /RE high, and SAM transmitters held reset through the independent SWD interfaces or otherwise known quiet. Send USART2 synchronization before releasing other traffic. This makes the operational boundary explicit; it does not claim automatic gateway recovery amid arbitrary hostile/failed-node traffic. If arbitrary traffic must remain supported, qualify additional receive isolation or a different ROM-safe CAN pin allocation under B1-Q005/013. Standby alone does not establish that a transceiver RX output is high impedance, and unplugging a remote cable does not disconnect a local RX driver.

This is a **capture blocker for the existing unverified allocation**, not evidence that the accepted MCU or recovery architecture is infeasible. Resolve under B1-Q005/013 together with B1-Q003/009; no accepted ADR needs routine reopening. The later schematic must implement the reconciled allocation, rather than copying the present workbook blindly.

## Linux control policy

Inspection of upstream `ftdi_sio.c` and `ftdi_sio.h`, downloaded 2026-09-07, confirms CBUS GPIO support requires CONFIG_GPIOLIB and EEPROM I/O-mode assignment. FT232H GPIO offsets **0,1,2,3 map to ACBUS5,6,8,9**; physical pin numbers are not GPIO offsets. The driver reads configuration at EEPROM byte addresses 0x1a–0x1d, exposes valid GPIOs as `ftdi-cbus`, and uses runtime PM around USB control messages.

At the first GPIO request the driver writes input directions and zero data before applying requested output directions. Pulldowns make this intermediate high-Z state safe. Its removal code explicitly notes that exiting CBUS mode does not reset pin states. There is no GPIO free callback that guarantees default release: closing a GPIO handle, crashing a process or unloading a driver is **not** a hardware reset guarantee. Use one persistent libgpiod owner, initialize both outputs low, and explicitly restore both low on successful completion and handled failures. After an unhandled crash, the recovery utility can reacquire and drive safe states; physical re-enumeration behavior must be tested.

Opening the tty sends FTDI Reset SIO, which resets flow control, buffers and RTS/DTR according to the driver's header; this is separate from CBUS selection. Open/configure the tty before the reset/boot sequence, keep it open through programming, identify tty and GPIO chip by the same USB serial/device ancestry, and inhibit autosuspend for the transaction. Do not hardcode gpiochip numbers. Recheck the installed distribution kernel and libgpiod API; no real device operation was performed here.

Proposed transaction: open/configure tty; acquire both lines low; ensure main rail and VCP path valid; assert reset; wait 10 ms; raise BOOT0; wait 10 ms; release reset; wait 10 ms; synchronize/program/verify; assert reset, lower BOOT0, wait 10 ms, release reset; explicitly leave both requests low. GPIO line readback only observes CBUS, not actual NRST/BOOT0, so scope or probe checks are still required.

## Alternatives and remaining finite checks

A single N-MOS reset sink plus an N-MOS/P-MOS BOOT0 translator is electrically attractive and has the same truth table. Examined DMN1019USN-7 and DMN2056U-7 low-voltage parts with a 1 kohm/2.2 kohm input divider: FTDI's minimum high produces about 1.65 V, and maximum low about 0.275 V. However, threshold minima are specified at a particular drain current/25°C, not a guaranteed full-temperature off-state logic threshold; subthreshold leakage can matter against reset/gate pulls. **Prefer the dual logic inverter**, whose input thresholds and Ioff are specified, instead of claiming the discrete alternative proven from VGS(th). Generic BSS138/2N7002 substitutions also need exact low-voltage on-state review.

Before accepting these details for capture:

1. Resolve the ROM pin conflicts above and define a recovery setup that remains safe without application firmware; audit simultaneous outputs using the actual ROM version.
2. Reconcile U_REC bypass ownership with VCP enable circuitry, add its leakage/current and the reset capacitors to the power model, and check all supply-order transitions and MCU POR/BOR thresholds.
3. Verify U_REC output high-Z leakage, Q_BOOT leakage/threshold over the accepted ambient range, and resulting NRST/BOOT0 levels. Scope blank EEPROM, high-Z inputs, suspend/resume, rapid replug, brownout, bridge-first and main-first collapse.
4. Review exact symbol/footprint pin numbering and parts; verify SWD reset polarity and probe electrical behavior with target unpowered. Complete applicable STM32 ES0430 and SAMC21 errata review against actual silicon revisions.
5. Read/write/read-back EEPROM and option bytes; test Linux tty+GPIO ownership, open/close, crash cleanup and re-enumeration; demonstrate ROM flash/program/verify and return to user flash with buffers enabled solely by hardware.

These are targeted pre-capture/bring-up checks. No ERC, DRC, circuit simulation or hardware qualification was performed.

## Primary evidence

- [TI SN74LVC2G06 SCES307J, July 2015](https://www.ti.com/lit/ds/symlink/sn74lvc2g06.pdf): pp.3,5–6,9,11; DBVR orderable appendix refreshed July 2026; pin table, input/output limits, Ioff, bypass and function table.
- [Diodes DMP2035U DS31830 Rev.11-2, June 2025](https://www.diodes.com/datasheet/download/DMP2035U.pdf): pp.1–2,6; exact -7 order code, package, gate/drain limits and suggested pads. On resistance specified at -1.8 V; final leakage/ambient review remains open.
- [FTDI FT_000288 v2.2](https://ftdichip.cn/Support/Documents/DataSheets/ICs/DS_FT232H.pdf): pp.9,12–13,43,49,55; CBUS startup, I/O limits and EEPROM I/O-mode value. Shared downloaded source in `ftdi_support_sources/`; v2.3/current errata reconciliation belongs to item 1.
- [ST AN2606 Rev.70, February 2026](https://www.st.com/resource/en/application_note/an2606-stm32-microcontroller-system-memory-boot-mode-stmicroelectronics.pdf): Pattern 14 p.35; Table 117 pp.279–281; Figure 69 p.282; ROM versions pp.283–284.
- [ST RM0440](https://www.st.com/resource/en/reference_manual/rm0440-stm32g4-series-advanced-armbased-32bit-mcus-stmicroelectronics.pdf): boot configuration and FLASH_OPTR category-3 fields. Search-visible Rev.9 exists; exact category-3 page/current PDF retrieval remains pending, so option-byte allocation is unverified.
- [ST DS12288 Rev.6](https://www.st.com/resource/en/datasheet/stm32g474rb.pdf): LQFP64 pinout p.50, GPIO limits pp.128–130, NRST pp.133–134.
- [Microchip DS60001479M, 2025](https://ww1.microchip.com/downloads/aemDocuments/documents/MCU32/ProductDocuments/DataSheets/SAM-C20-C21-Family-Data-Sheet-DS60001479.pdf): §53.5 pp.1226–1228; current downloaded PDF and text in `cbus_recovery_sources/`. This updates earlier Rev.J reset-checklist evidence without changing allocations.
- [KEMET exact 100 pF component sheet](https://search.kemet.com/component-documentation/download/specsheet/C0805C101J5GACTU): generated 2025-11-15, p.1, exact 0805 capacitance/tolerance/rating.
- [Linux upstream ftdi_sio.c](https://raw.githubusercontent.com/torvalds/linux/master/drivers/usb/serial/ftdi_sio.c) and [ftdi_sio.h](https://raw.githubusercontent.com/torvalds/linux/master/drivers/usb/serial/ftdi_sio.h): local dated snapshots in `cbus_recovery_sources/`; inspect `ftdi_gpio_init_ft232h`, `ftdi_gpio_request`, `ftdi_gpio_remove`, `ftdi_open` and Reset SIO documentation. Upstream master is mutable; compare the installed kernel before testing.
- [Diodes DMN2056U DS38480 Rev.2-2, July 2021](https://www.diodes.com/datasheet/download/DMN2056U.pdf): pp.1–3; discrete alternative comparison only, not proposed for fitting.
