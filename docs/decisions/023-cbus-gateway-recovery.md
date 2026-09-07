---
id: ADR-023
title: Dedicated CBUS gateway reset and BOOT0
status: accepted
scope: Board 1 gateway recovery
created: 2026-09-06
accepted_on: 2026-09-06
accepted_by: Explicit maintainer instruction USR-24
supersedes: none
superseded_by: none
requirements: [B1-R024]
questions: [B1-Q013]
---

# Decision

Allocate FT232HL ACBUS5 (pad 29, B1-P261) to gateway reset and ACBUS6 (pad 30, B1-P262) to gateway BOOT0. The endpoints are STM32 NRST (pad 7, B1-P175) and PB8/BOOT0 (pad 61, B1-P229). Configure both CBUS pins as GPIO in EEPROM. Preserve UART TX/RX/RTS/CTS and independent SWD access.

B1-B053 covers the control interfaces, with components and polarity TBD. Reset must assert low or release NRST without fighting SWD. Require default reset released and BOOT0 low, including absent PC software. Prevent back-powering the main domain from the independent bridge. The existing quad UART buffer has no spare channels.

The maintainer confirms UART buffers become enabled after USB configuration, with the main 3.3 V domain off beforehand. Buffer enabling must not require STM32 application firmware, so ROM programming works once the rail is valid.

# Evidence and process

[FT_000288 v2.2](https://www.ftdichip.cn/Support/Documents/DataSheets/ICs/DS_FT232H.pdf), Tables 3.4–3.5 pp.12–13, supports these GPIOs. [AN2606 Rev.70](https://www.st.com/resource/en/application_note/an2606-introduction-to-system-memory-boot-mode-on-stm32-mcus-stmicroelectronics.pdf), Pattern 14 p.35 and Table 117 p.279, confirms pin-controlled ROM boot and USART2 PA2/PA3. Verify nSWBOOT0=1, nBOOT1=1 and BOOT_LOCK=0; retain NRST reset mode.

Linux ftdi_sio exposes ACBUS5/6 as offsets 0/1 of ftdi-cbus. Use libgpiod alongside the tty UART. Identify the board by serial number and retain GPIO ownership during programming. [Kernel implementation](https://github.com/torvalds/linux/blob/master/drivers/usb/serial/ftdi_sio.c).

Sequence: assert reset, raise BOOT0, release reset, program through USART2; then lower BOOT0 and reset again. Actual control polarities and delays await the circuit. Keep other nodes/PHYs quiet and review ROM-probed pins for contention or unintended peripheral enable.

# Alternatives and remaining checks

Dedicated CBUS control avoids DTR changes from serial applications and preserves RTS/CTS. SWD remains an independent recovery/debug path. B1-Q013 tracks components, power transitions, reset sharing, boot defaults, option bytes, ROM interface selection and Linux programming tests. Scope is accepted; all pin/electrical/errata/footprint evidence remains unverified. No CAD, ERC/DRC or hardware validation is claimed.
