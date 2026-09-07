# GPIO breakout series resistors

Status: proposed, 2026-09-06. B1-R020 / B1-Q010. Applies to spare GPIO breakout signals, not ground, power, dedicated SWD, crystal pins or differential bus terminals. ADR-039 now accepts four GPIO signals plus GND per MCU (16 GPIO signals total). This series-resistor proposal remains unaccepted.

Recommend one TE CRGCQ0805F220R (220 ohm +/-1%, 0805, 0.125 W) per spare GPIO signal as the default for low-current digital experimentation. Place close to MCU, MCU GPIO -> resistor -> header. This gives a removable isolation point and reduces short/contention current and edge speed. It is not a matched transmission-line termination, guaranteed MCU fault protection, level shifting or power-off isolation.

Calculated screens ignoring output-driver resistance:
- 3.3 V output shorted to ground: 15 mA and 49.5 mW in 220 ohm. Actual current is driver-dependent; this calculation does not establish a safe MCU pin or aggregate fault current.
- Two opposite 3.3 V outputs each behind 220 ohm: 7.5 mA through 440 ohm.
- 1 mA load causes 0.22 V drop; 5 mA causes 1.1 V. Use these headers for logic signals, not direct high-current loads.
- Added RC 10–90% rise-time estimate 2.2RC: about 24 ns at 50 pF and 48 ns at 100 pF, excluding driver resistance. Review fast SPI/clock/UART use and long jumpers separately; no blanket baud limit inferred.

For ADC use, include the 220 ohm plus external source impedance in acquisition-time/settling analysis. For open-drain signals, include the resistor drop in VOL and pull-up analysis. GPIO voltage limits remain those of the exact MCU pin; no blanket 5 V tolerance. External drive while the board is off can still back-power through pin structures. A resistor alone is not ESD protection.

Quantity is one per finally allocated spare GPIO signal (16 only if the proposed four signals per MCU is adopted). No additional signal-breakout scope, alternative/DNP footprints or protection ICs are authorized by this proposal. Keep final current, capacitance, off-state and pin-function contracts under B1-Q010.

Primary part source: https://www.te.com.cn/chn-zh/product-1-2176341-7.html ; DigiKey: https://www.digikey.com/en/products/detail/te-connectivity-passive-product/CRGCQ0805F220R/8576343 . Calculations are ideal lumped-circuit estimates, not hardware validation.
