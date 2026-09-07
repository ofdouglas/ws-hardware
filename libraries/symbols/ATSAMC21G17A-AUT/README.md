# ATSAMC21G17A-AUT KiCad symbol

`ATSAMC21G17A-AUT.kicad_sym` is a standalone modern KiCad symbol library (KiCad 6 or newer format; loaded and rendered with KiCad 7.0.11).

## Add to KiCad

1. In the Schematic Editor, open **Preferences → Manage Symbol Libraries**.
2. Choose **Project Specific Libraries** (or **Global Libraries**), click **Add existing library**, and select `ATSAMC21G17A-AUT.kicad_sym`.
3. Save the library table. Use **Add Symbol** (`A`) and search for `ATSAMC21G17A-AUT`.

The symbol assigns `Package_QFP:TQFP-48_7x7mm_P0.5mm` from KiCad's standard footprint libraries. No custom footprint is required.

## Symbol details

- One unit, all 48 package pins visible and individually connectable.
- Port A on the left, Port B on the right, supplies at the top, grounds at the bottom.
- GPIO pins use their base port names and bidirectional electrical types. Multiplexed peripheral functions are selected in firmware; consult the datasheet for routing choices.
- RESET (pin 40) is an active-low input.
- VDDCORE (pin 43) is the internal regulator output and uses `power_out` for ERC.
- VDDANA, VDDIN, both VDDIO pins, GNDANA, and all three GND pins use `power_in`.
- No hidden or stacked pins; no exposed-pad pin is added to this TQFP part.

## Sources and verification

Pin numbers and signal names checked against Microchip's [SAM C20/C21 Family Data Sheet, DS60001479J](https://ww1.microchip.com/downloads/en/DeviceDoc/SAM-C20-C21-Family-Data-Sheet-DS60001479J.pdf), section 4.2.1, page 22. TQFP dimensions are documented on page 1155: 48 leads, 7 × 7 mm body, 0.5 mm pitch.

The exact orderable part and package were checked against the [DigiKey listing](https://www.digikey.com/en/products/detail/microchip-technology/ATSAMC21G17A-AUT/6148848).

The companion CSV lists every pin and its electrical type. Verification checked unique pin numbers 1–48, unique connection positions, and successful KiCad SVG export. The rendered preview was visually inspected. This is a symbol/library check; no application circuit or PCB has been validated.
