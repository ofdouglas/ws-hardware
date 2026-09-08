# Board 1 pin/resource allocation

Gateway correction (2026-09-07): STM32G473RBT6 is selected and captured per [ADR-043](../../docs/decisions/043-gateway-part-correction.md). DS12288 references and older workbook/PDF snapshots below are prior G474 evidence, not G473 qualification. Recheck exact G473 AF/electrical limits under B1-Q005/008 before schematic approval.

Status: complete draft allocation, evidence remains unverified. Source CAD owns implemented connectivity. [Corrected allocation workbook](../../outputs/samc21-pin-allocation/samc21_pin_allocation.xlsx), [MCU capture plan](mcu_capture_plan.json), [complete CAD manifest](kicad/complete_manifest.json) and [capture checks](kicad/README.md) agree on MCU allocation. Stable IDs B1-P001–024 remain resource groups; B1-P025–168 are the three48-pad SAMs, B1-P169–232 the64-pad gateway, B1-P233–280 FTDI, and B1-P281–288 EEPROM. Next unused pin ID B1-P289.

The capture review corrected a workbook pad-number error for STM32 pads19–29. The correct sequence is PA5,PA6,PA7,PC4,PC5,PB0,PB1,PB2,VSSA,VREF+,VDDA. LED PA5 is pad19; ground is pad27 and analog supply/reference are28/29. IDs remain tied to physical pad numbers. This corrects implementation data and does not change accepted device choices.

| Function | Gateway physical pads / peripheral | Each SAM physical pads / peripheral |
|---|---|---|
| CAN A | PA12 TX46 / PA11 RX45,FDCAN1 AF9; PC6 STB38 | PA24 TX33 / PA25 RX34,CAN0 muxG; PA20 STB29 |
| CAN B | PB13 TX35 / PB12 RX34,FDCAN2 AF9; PC7 STB39 | PB10 TX19 / PB11 RX20,CAN1 muxG; PA21 STB30 |
| UART_MD | PA9 TX43 / PA10 RX44,USART1 AF7 | PA08 TX13 / PA09 RX14,SERCOM0 muxC |
| Ring | NA | PA16 TX25 / PA17 RX26,SERCOM1 muxC |
| VCP | PA2 TX14 / PA3 RX17 / PA1 RTS13 / PA0 CTS12,USART2 AF7 | NA |
| RS-485 | PC10 TX52 / PC11 RX53,USART3 AF7; PB14 DE36,PC12 RE_N54 | NA |
| Text debug | PB11 TX33 / PB10 RX30,LPUART1 AF8 | PA12 TX21 / PA13 RX22,SERCOM2 muxC |
| SYNC / TRIG | PC0 pad8 EXTI0 / PC1 pad9 EXTI1 | PA02 pad3 EXTINT2 / PA03 pad4 EXTINT3,muxA |
| EVENT0 / EVENT1 | PC2 pad10 / PC3 pad11 | PB08 pad7 / PB09 pad8 |
| LED | PA5 pad19 | PA27 pad39 |
| SWD / reset | PA13 IO49 / PA14 CLK50 / PG10-NRST7 | PA31 IO46 / PA30 CLK45 / RESET40 |
| Main crystal | PF0 IN5 / PF1 OUT6 | PA14 IN23 / PA15 OUT24 |
| Boot | PB8-BOOT0 pad61,10k toGND | No BOOT0 pin |

All four MCU SWD connectors use1VTref,2SWDIO,3GND,4SWCLK,5GND,6NC,7NC/key,8NC,9GND,10RESET. Ordinary reset support and SAM SWCLK defaults are captured. No SWO, ROM/CBUS recovery, extra oscillator, general breakout or future PHY is reserved.

The SAM ring is SAM0→SAM1→SAM2→SAM0. UART_MD is the shared RX net; each private TX drives one LV125 /OE with A grounded. CAN A/B each have four independent PHYs. See [interfaces](interfaces.md), [timing headers](timing_headers.md) and native sheets for connector/default details.

Workbook/plan aliases: `_FD_CAN_`→`_CAN_`, `_UART_MD_TX`→`_MD_TX`, timing/debug `_MCU` suffix removed for MCU-side CAD names; `_HDR` explicitly identifies private connector sides. Shared SYNC/TRIG are always on the header side of four independent resistors. FTDI aliases:3V3_FTDI→FTDI_3V3,USB_5V_PROTECTED→USB_5V,3V3_FTDI_PHY/PLL→FTDI_VPHY/VPLL,FTDI_VCCA_1V8/VCORE_1V8→FTDI_VCCA/VCORE,USB_D_MINUS/PLUS→USB_DM/DP,FTDI_TXD/RXD→FTDI_TX/RX,XTAL_IN/OUT→XTIN/XTOUT,REF_R→FTDI_REF,EEPROM_CS/CLK/DATA/DO→EECS/EECLK/EEDATA/EE_DO. Older workbook bridge-support TBD prose is planning history; the CAD/BOM owns enumerated support.

Evidence: STM32 DS12288Rev6 Fig7p50,Table12pp57–68,AF tables; SAM DS60001479J§4.2.1p22,Table6-2pp29–30 and debug checklist§53.8/Table53-7p1182. Exact sources/muxes per pad are in the JSON/workbook. Independent review compared all208 MCU pads to fresh native KiCad export, plus support/header nets. No hardware or complete electrical qualification is implied.

B1-Q003/005/008/010/014 retain clock/rate and firmware checks, fitted silicon errata, actual signal margins and layout/bring-up. Use SAM EIC synchronous active-run mode and clear flags after enable; DS80000740T limitations do not require extra hardware for this bench use. First programming uses SWD connect-under-reset with external bus peers disconnected; firmware sets TX idle and safe DE/RE/STB before connecting peers.

## Communications measurement access

[ADR-046](../../docs/decisions/046-communications-measurement-headers.md) implements USR-38. All seven headers are 1×2, 0.1-inch pitch; pin 1 carries the first listed signal.

| Reference | Interface | Pin 1 | Pin 2 |
|---|---|---|---|
| J19 | CAN A | FD_CAN_A_H | FD_CAN_A_L |
| J20 | CAN B | FD_CAN_B_H | FD_CAN_B_L |
| J21 | RS-485 | RS485_A | RS485_B |
| J22 | SAM0 → SAM1 ring UART | RING_01 | GND |
| J23 | SAM1 → SAM2 ring UART | RING_12 | GND |
| J24 | SAM2 → SAM0 ring UART | RING_20 | GND |
| J25 | Shared UART_MD | UART_MD | GND |

TP13–TP19 are retired without reference reuse. TP1–TP12 retain rail/reset/boot/core access; J13–J18 retain local scope-ground posts. These observation headers are not jumper links and receive no shunts. Keep concise function/polarity silkscreen, short routed observation branches and local probe-return access. Existing interface operating limits still apply.
