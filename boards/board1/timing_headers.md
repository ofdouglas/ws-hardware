# Rev A timing and debug headers

Scope accepted in [ADR-041](../../docs/decisions/041-timing-debug-headers.md), B1-R027. Each of GW, SAM0, SAM1 and SAM2 gets one 1x8, 2.54 mm male header cut from the selected PRPC040SAAN-RC. This replaces both previous per-MCU headers.

The following order is specified by the maintainer (USR-36 / [ADR-042](../../docs/decisions/042-header-resistors-recovery-scope.md)); MCU directions are shown:

| Pin | Signal | Direction / ownership |
|---|---|---|
| 1 | DEBUG_RX | Input to this MCU |
| 2 | DEBUG_TX | Output from this MCU |
| 3 | GND | Board ground |
| 4 | SYNC | Shared input to all four MCUs |
| 5 | TRIG | Shared input to all four MCUs |
| 6 | GND | Board ground |
| 7 | EVENT0 | Private output from this MCU |
| 8 | EVENT1 | Private output from this MCU |

Fit one 330 ohm resistor close to each MCU pin for DEBUG_RX, DEBUG_TX, SYNC, TRIG, EVENT0 and EVENT1. Six per MCU gives 24 total in B1-B076. Reuse CRGP0805F330R (0805, 1%) as an engineering implementation choice; the existing two RS-485 bias resistors B1-B071 are additional. Grounds connect directly.

SYNC and TRIG are separate board-wide nets, repeated at every header. Each shared header-side net branches through four individual 330 ohm resistors, one beside each MCU input. Do not use one common resistor ahead of the fanout or directly join the four MCU-side nodes. Private debug/event signals each have their own resistor between the MCU and its header. Use one external driver per shared net; configure all MCU connections as inputs. EVENT nets stay separate: GW_EVENT0/1, SAM0_EVENT0/1, SAM1_EVENT0/1 and SAM2_EVENT0/1. Debug RX/TX are also private. Interfaces use 3.3 V logic with no power-export pin. Retain 115200 baud, 8N1/no flow control for text UARTs and independent Cortex SWD access.

Fit one 10 kohm pull-down from shared SYNC to GND and one from shared TRIG to GND, on the header side of the four per-MCU 330 ohm branches. Place the pair together near a timing header or the shared-net fanout; neither needs to be repeated at each MCU. B1-B077 owns the two RMCF0805FT10K0 (0805, 1%) resistors. USR-37 requires the pull-downs; 10 kohm and reuse of the existing resistor MPN are routine engineering choices. This gives an idle-low state with an absent/high-impedance driver and internal MCU pulls disabled. Each externally driven 3.3 V high adds 0.33 mA load to that external driver. Confirm aggregate input leakage and disable conflicting internal pulls during schematic/firmware review; no extra buffer is implied.

Before schematic approval, assign two interrupt-capable inputs and two output GPIOs per MCU, verify EIC/EXTI line availability for simultaneous SYNC/TRIG interrupts and conflicts with existing functions (B1-Q005/010). Previously proposed spare pads are candidate locations only, marked TEST_IO_TBD in the draft workbook. Keep current debug UART mappings subject to B1-Q014 qualification. No precision skew, timer-capture peripheral or additional buffer requirement is inferred.

Before layout approval, check cut-strip footprints, pin-1 marking and scope access. The two GND posts provide probe-ground clip locations; retain B1-B075 until layout determines whether additional fitted ground pins are needed near measured circuits. Keep short local probe return paths for edge measurements. Unallocated strip posts are not counted as fitted ground pins. B1-Q010/014 retain external-drive, load and unpowered-interface review. At bring-up, exercise shared stimuli and observe each MCU's private event outputs.

General ADC, SPI/I2C and spare GPIO breakouts and their proposed support resistors are deferred. Only the 24 required signal series resistors are added by USR-36; no general-breakout support is restored. The resistors limit current and affect edge timing but do not provide power-off isolation. Use 3.3 V bench signals, high-impedance measurement inputs and one driver for each shared net; external-drive/off-state details remain schematic checks, not a requirement for extra buffers. Verify event timing at the header during bring-up. No edge-rate or skew guarantee is added.
