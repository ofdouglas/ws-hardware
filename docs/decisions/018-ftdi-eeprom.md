---
id: ADR-018
title: AT93C56B-SSHM-B FTDI configuration EEPROM
status: accepted
scope: Board 1 FT232HL bridge
created: 2026-09-06
accepted_on: 2026-09-06
accepted_by: Conditional maintainer selection USR-23 after compatibility review
supersedes: none
superseded_by: none
requirements: [B1-R005, B1-R012]
questions: [B1-Q002, B1-Q012]
sources: [USR-23]
---

# Decision

Select one Microchip AT93C56B-SSHM-B for B1-B013. Use its SOIC-8 package and 128 x 16 organization, with ORG strapped to its VCC. Supply it from the independent FTDI 3.3 V domain. This records the maintainer's instruction to commit to this part if suitable; it accepts the component selection, while circuit and footprint evidence remain unverified.

# Compatibility review

[FTDI's EEPROM guidance](https://ftdichip.com/faq/what-external-eeprom-is-recommended-for-use-with-the-ftdi-usb-hi-speed-ics/) allows 93C56 or 93C66 devices with 16-bit words and 3.3 V I/O. [Microchip DS20006260B](https://ww1.microchip.com/downloads/aemDocuments/documents/MPD/ProductDocuments/DataSheets/AT93C56B-AT93C66B-Microwire-Serial-EEPROM-Industrial-Grade-DS20006260.pdf), pp.3–9 and 31, confirms the exact order code, organization, supply range and exposed-lead package. These meet the selection requirements. The device's 3.3 V logic levels also match the FTDI LVTTL thresholds in FT_000288 v2.2 Table 5.3.

The [DigiKey listing](https://www.digikey.com/en/products/detail/microchip-technology/AT93C56B-SSHM-B/3046221) identifies AT93C56B-SSHM-B-ND in tubes with a quantity-one tier. Stock and price must be refreshed at purchase.

# Implementation and alternatives

Use the draft FTDI sheet linked from the Board 1 pinmap for the 48 bridge pads and eight EEPROM pads. FT_000288 v2.2 Table 3.3 supplies the EEDATA/DI/DO resistor wiring. Program and read back through USB using FT_Prog. A larger 93C66 is unnecessary for the current configuration; a smaller package offers no needed function and reduces hand-assembly convenience.

# Remaining qualification

B1-Q012 tracks EEPROM clock/program timing, startup/reset and rapid power cycling, exact SOIC footprint, current documentation and programming validation. At 3.3 V the clock limit is 1 MHz, not the distributor's 2 MHz headline. Microchip's startup constraints must be satisfied before the FTDI reads configuration. Bulk erase/write instructions require the higher supply range, so verify the actual programming procedure uses supported word operations. Supporting passives remain B1-B017; no new programmer or header is selected. B1-Q002 retains the power budget and default-off SC189 control review. No hardware test or fabrication approval is implied.

Revisit only if those checks demonstrate incompatibility or the maintainer changes requirements.
