---
id: ADR-043
title: Correct gateway MCU transcription to STM32G473RBT6
status: accepted
scope: Board 1 gateway exact part selection
created: 2026-09-07
accepted_on: 2026-09-07
accepted_by: Explicit maintainer correction in this conversation
supersedes: ADR-004 (gateway MPN only)
superseded_by: none
requirements: [B1-R001]
questions: [B1-Q005, B1-Q008]
---

# ADR-043: Correct gateway MCU transcription

The maintainer states: “STM32G473RBT6 was the intended chip all along, '4' must have been written in error.” Select STM32G473RBT6 for B1-N01 / B1-B001 / U7. This supersedes only ADR-004's gateway part number; the three SAM selections and all existing interface requirements remain.

The internal and DigiKey BOMs, current requirement/overview, MCU plan and native CAD now identify G473. The installed KiCad exact G473RBTx symbol replaces the embedded G474 symbol. All 64 base pin definitions (number, name, type and geometry) compare identically; alternate-function metadata comes from the actual G473 symbol. Existing wires and footprint remain. This establishes draft library/connectivity consistency, not exact-device electrical or AF qualification.

Primary source: [ST DS12712 Rev 5](https://www.st.com/resource/en/datasheet/stm32g473rb.pdf). Before schematic approval, review the retained allocations against G473 pin/AF tables and electrical limits, and applicable [ES0430 errata](https://www.st.com/resource/en/errata_sheet/es0430-stm32g471xx473xx474xx483xx484xx-device-errata-stmicroelectronics.pdf), under B1-Q005/008. Older DS12288 calculations and the allocation workbook/review PDFs are G474 capture history; they are not G473 verification. No additional circuitry is authorized or needed merely by this transcription correction.

Sourcing: the supplied DigiKey CSV already contains the correct G473 MPN. The eBay FTDI listing is being considered only; this correction does not accept a new bridge supplier or claim authenticity.
