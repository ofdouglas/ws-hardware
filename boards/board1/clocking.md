# Clocking and VCP timing

Status: draft implementation note · Requirements: B1-R014, B1-R015 · Decision: ADR-005
Updated: 2026-09-06 · Physical allocation and bench validation: pending

## Gateway VCP configuration

| Parameter | Design target |
|---|---|
| STM32 SYSCLK / core clock | 168 MHz |
| VCP USART kernel clock | 168 MHz; explicitly select a suitable kernel source |
| USART prescaler | Divide by 1 |
| Oversampling | 8x (OVER8=1) |
| Wire baud rate | 12,000,000 baud |
| Flow-control wiring | TX, RX, RTS, CTS, all with power-off isolation |
| Nominal frame for initial validation | 8N1 (implementation proposal) |

ST describes independent USART clock domains, DMA and hardware flow control in [DS12288, §3.29](https://www.st.com/resource/en/datasheet/stm32g474rb.pdf). Confirm the selected instance's clock mux and all four signals in the exact LQFP64 allocation; draft assignments are in pinmap.md, with exact mux/pad verification still open. Do not substitute LPUART without a separate feasibility review.

Calculated from 168 MHz and 12 Mbaud:

```text
effective bit-period division = 168,000,000 / 12,000,000 = 14
8x mode USARTDIV = 2 * 168,000,000 / 12,000,000 = 28 = 0x001C
BRR = (0x001C & 0xFFF0) | ((0x001C & 0x000F) >> 1) = 0x0016
nominal baud quantization error = 0%
bit time = 83.333 ns
8N1 raw byte ceiling = 12,000,000 / 10 = 1,200,000 bytes/s per direction
```

BRR encoding follows [RM0440 Rev 9, USART baud generation, p.1708](https://www.st.com/content/ccc/resource/technical/document/reference_manual/group0/7c/b0/25/29/1b/a2/42/b2/DM00355726/files/DM00355726.pdf/jcr%3Acontent/translations/en.DM00355726.pdf). With 16x sampling the ceiling would be 168/16 = 10.5 Mbaud; 8x is required. ST notes reduced clock-deviation tolerance at 8x. [STM32G4 USART training, slide 8](https://www.st.com/content/ccc/resource/training/technical/product_training/group0/99/1b/d4/d6/84/c0/4d/82/STM32G4-Peripheral-USART_interface_USART/files/STM32G4-Peripheral-USART_interface_USART.pdf/jcr%3Acontent/translations/en.STM32G4-Peripheral-USART_interface_USART.pdf)

Zero divider error does not mean zero oscillator error or a guaranteed application throughput. Budget crystal initial tolerance, temperature, aging, loading, clock-generation effects and receiver limits on both ends. Actual payload throughput includes framing/protocol overhead and PC scheduling/backpressure.

## Signal directions and isolation

| Origin | Destination | Isolation requirement |
|---|---|---|
| FT232H TXD | STM32 USART RX | Bridge -> main board |
| STM32 USART TX | FT232H RXD | Main board -> bridge |
| FT232H RTS# | STM32 USART CTS | Bridge -> main board |
| STM32 USART RTS | FT232H CTS# | Main board -> bridge |

FTDI pin-function directions are documented in [FT232H v2.2 §3.5.1](https://ftdichip.com/wp-content/uploads/2024/09/DS_FT232H.pdf); physical implementation still requires current-datasheet reconciliation. Preserve active-low handshake semantics; do not connect RTS output to RTS output. Use two channels in each direction. Hardware flow control is required wiring capability; enable the corresponding STM32 and PC-driver modes for high-rate tests.

Place the bridge and isolation close to the STM32. Choose non-inverting isolation with specified power-off behavior, propagation delay, pulse-width distortion and loading adequate for the 83 ns bit period. Default CTS to inactive on the powered receiving side while disconnected; default RX to idle high where appropriate. Pulls must be referenced to the appropriate powered domain. Do not let added pulls defeat isolation or suspend-current limits. SN74LV125APWR is selected ADR-013; OE/default logic, pulls and timing qualification remain B1-Q002.

Plan DMA and bounded buffering for sustained traffic. Verify RTS/CTS reaction time and bytes already in flight under USB stalls and simultaneous CAN/UART load. Peripheral automatic RTS must not be assumed to protect an arbitrary software DMA ring from overflow.

## Crystal policy and clock-tree work

| Device | Reference requirement | Unresolved implementation |
|---|---|---|
| GW | Dedicated external main crystal -> PLL -> 168 MHz core and VCP kernel | Selected 12 MHz crystal; PLL and FDCAN clocks, voltage scaling/boost and flash settings |
| SAM0 | Dedicated external main crystal -> link clock tree | Selected 12 MHz crystal; DPLL/GCLK/SERCOM/CAN settings |
| SAM1 | Same policy; independent crystal | Same review as SAM0 |
| SAM2 | Same policy; independent crystal | Same review as SAM0 |
| FT232HL | Selected independent 12 MHz crystal | Loading/startup qualification |

SAM C21 includes a 0.4–32 MHz main crystal oscillator and frequency synthesis; consult the exact ordering variant and electrical limits when setting core and peripheral speeds. [Microchip DS60001479J, configuration summary](https://ww1.microchip.com/downloads/aemDocuments/documents/MCU32/ProductDocuments/DataSheets/SAM-C20-C21-Family-Data-Sheet-DS60001479J.pdf)

Select frequencies jointly with CAN timing and onboard UART divisors. Reuse crystal MPNs only where each oscillator's load, ESR and drive requirements permit; separate crystals may use different load capacitors. Reserve two oscillator pads per MCU before assigning general I/O. External references must actually feed the high-speed peripherals; fitting a crystal while leaving UART/CAN on an unrelated RC clock does not fulfill the requirement. Wait for reference/PLL readiness before high-speed links are enabled; clock failure must not silently preserve a claimed accurate link rate. This decision does not require RTC/32.768 kHz crystals.

The SAM ring and shared open-drain UART target several Mbaud, with exact values open in B1-Q003. Verify the shared medium's pull-up, capacitance, drive strength and rise time separately; clock precision alone cannot establish its maximum baud.

## Verification still required

B1-Q008 owns full clock-tree/crystal implementation. Verify exact part and errata, PLL operating limits, high-speed voltage/flash configuration, simultaneous peripheral clocks, oscillator startup/drive margin, component tolerances and load networks. Then test full-duplex 12 Mbaud with flow-control stalls, power transitions and competing traffic. No pinmux, crystal selection or end-to-end timing sign-off is implied by the arithmetic above.

Current crystals and initial load capacitors are accepted ADR-014/030/031; see [crystal networks](crystal_networks.md). Clock-tree and oscillator qualification remain open.

## Smaller crystal accuracy screen for MCU links

The selected crystal initial plus temperature bound is 80 ppm (0.008%), before aging/loading. At 12 Mbaud this is 960 baud absolute error; two opposite 80 ppm clocks differ by 160 ppm (0.016%). With a 168 MHz USART kernel and 8x oversampling, 12 Mbaud has an exact nominal divisor of 14, so no baud-quantization error is required. This crystal accuracy is adequate as a preliminary UART design input; receiver configuration, peer accuracy, PLL jitter and board timing remain to validate.

For 8 Mbit/s CAN FD data, 80 ppm is 640 bit/s error. This is a reasonable crystal accuracy for design, but CAN acceptance requires the complete nominal/data timing and oscillator-tolerance calculation at both endpoints, including SJW, propagation, transceiver delay compensation and jitter. 8 Mbit/s is a data-phase target, not an arbitration rate or newly accepted bus requirement. An illustrative 168 MHz FDCAN time-quanta clock permits exactly 21 quanta per 8 Mbit/s bit; clock routing, legal segment settings and SAM interoperability remain B1-Q003/008.

Sources: [ST RM0440 USART receiver tolerance section](https://www.st.com/resource/en/reference_manual/dm00355726.pdf), [ST AN5348 Rev.6, FDCAN bit timing and delay compensation](https://www.st.com/resource/en/application_note/an5348-introduction-to-fdcan-peripherals-for-stm32-mcus-stmicroelectronics.pdf). These are engineering screens, not measured link performance or completed oscillator qualification.
