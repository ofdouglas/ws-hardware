# SC189ZSKTRT KiCad symbol

Standalone KiCad 6+ format symbol library, loaded and rendered with KiCad 7.0.11.

In the Schematic Editor, open **Preferences → Manage Symbol Libraries → Project Specific Libraries**, choose **Add existing library**, and select `SC189ZSKTRT.kicad_sym`. Save, then use **Add Symbol** (`A`) and search for `SC189ZSKTRT`.

Assigned footprint: `Package_TO_SOT_SMD:SOT-23-5` from KiCad's standard libraries.

| Pin | Name | Electrical type | Function |
| --- | --- | --- | --- |
| 1 | VIN | Power input | Input supply |
| 2 | GND | Power input | Ground |
| 3 | EN | Input | Active-high enable |
| 4 | VOUT | Input | Output voltage sense; connect to output after the inductor |
| 5 | LX | Power output | Switching node; connects to the inductor |

The Z suffix selects the fixed 3.3 V version. All five pins are visible, individually connectable, and on a 2.54 mm grid. The SOT-23-5 package has no exposed-pad pin.

Sources: [Semtech SC189 datasheet, August 27, 2010, hosted by Mouser](https://www.mouser.com/datasheet/2/761/sc189-1366204.pdf), page 2 for ordering and pin configuration, page 14 for pin descriptions; [exact DigiKey part](https://www.digikey.com/en/products/detail/semtech-corporation/SC189ZSKTRT/2182360).

Verified five unique pin numbers 1–5, matching standard footprint pad numbers, successful KiCad SVG export, and visual preview. No application circuit or PCB was validated.

## Migration status

Preserved from WireSpaces/hardware/kicad. Historical component: TPS560430 supersedes SC189 for Board 1 under ADR-021. This import does not reintroduce SC189 circuitry. Original source/license provenance is recorded in ../../imports/README.md.
