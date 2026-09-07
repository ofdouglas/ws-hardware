# VCP enable implementation

Status: enable policy accepted ADR-040; receiver defaults and physical allocation remain implementation work.

Connect FTDI PWREN# to B016 /OE pins 1, 4, 10, 13. Retain the bridge-domain PWREN# pull-up, SYS-powered B016 and existing inverter to buck EN. Do not add a SYS pull-up on PWREN#. No monitor, NAND or delay circuit is required.

Proposed channel allocation: 1A/1Y pins 2/3: FTDI TXD to STM32 RX; 2A/2Y pins 5/6: FTDI RTS# to STM32 CTS; 3A/3Y pins 9/8: STM32 TX to FTDI RXD; 4A/4Y pins 12/11: STM32 RTS to FTDI CTS#. Pin 14 is 3V3_SYS and pin 7 GND; retain the allocated bypass. Check against the pinmap when capturing.

Complete receiver defaults with the minimum required pulls, accounting for existing internal pulls. Confirm interface levels and 12 Mbaud timing under intended operating conditions before schematic approval. Normal startup/suspend/resume tests belong to bring-up. Valid UART traffic through power transitions is not required.

The dual-monitor/NAND proposal and its added BOM/power allocations are withdrawn. No support resistor quantities from that proposal are accepted implicitly. See [ADR-040](../../../docs/decisions/040-startup-and-vcp-enable.md) and [rationale/sources](enable_startup_reassessment.md).
