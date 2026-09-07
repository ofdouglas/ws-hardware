# Crystal network proposal

Status: initial fitted capacitor values/MPNs accepted ADR-031, 2026-09-06. Crystal MPNs finalized ADR-030. B1-Q008 owns startup, gain, drive and frequency qualification.

| Oscillator | Crystal CL | Capacitors to ground | Qty / board | Accepted initial part |
|---|---:|---:|---:|---|
| STM32 gateway | 20 pF | 33 pF each side | 2 | KEMET C0805C330F5GACTU |
| Three SAM C21 | 20 pF | 33 pF each side | 6 | KEMET C0805C330F5GACTU |
| FT232HL | 18 pF | 27 pF each side | 2 | KEMET C0805C270F5GACTU |

Both parts are 0805, 50 V, C0G/NP0, +/-1%. Use C0G for frequency-setting capacitors. Eight 33 pF and two 27 pF are accepted allocation quantities, not electrically qualified production values. No extra crystal or auxiliary oscillator added.

For equal external capacitors, CL approximately equals C/2 + Cs, where Cs is equivalent pin/PCB parasitic loading seen across the crystal (do not simply add both pin capacitances or the crystal's own shunt C0). Thus 33 pF implies Cs=3.5 pF for CL20, while 27 pF implies Cs=4.5 pF for CL18. These are initial estimates, not measured device capacitances. The MCU and FTDI estimates differ; even STM32 and SAM may need different final values. A measured Cs of 5 pF would call for approximately 30 pF and 26 pF respectively. FTDI shows 27 pF as an example, not a universal required value.

Place each crystal and two capacitors close to its IC; short quiet traces and short ground returns; keep switching nodes/digital traces away. Do not add generic 1 Mohm feedback resistors or guessed series damping values. Review each IC's oscillator circuit first. An output-side series resistor may be needed if measured drive exceeds crystal rating; its value trades drive against startup margin. Existing core crystal limit is 100 uW; FTDI crystal limit 500 uW per reviewed ECS series documents. SAM XOSC gain/startup settings and STM32 HSE gain margin need review with the selected high-CL crystals before schematic freeze.

Check startup across rails/temperature, drive level, and loaded frequency. FTDI's narrow remaining loading-error budget makes fine adjustment important; 1% capacitors alone do not establish frequency accuracy. Prefer measuring a buffered/divided clock output where available; avoid loading a crystal pin with an ordinary oscilloscope probe. No extra DNP trim footprints are implied by this proposal; change the fitted capacitor values if needed.

Sources: [ST AN2867](https://www.st.com/resource/en/application_note/cd00221665.pdf), [FT232H oscillator example, section 6.3](https://ftdichip.com/wp-content/uploads/2020/07/DS_FT232H.pdf), [33 pF exact manufacturer sheet](https://yageogroup.com/download/specsheet/C0805C330F5GACTU), [27 pF exact manufacturer sheet](https://yageogroup.com/download/specsheet/C0805C270F5GACTU). FTDI source is historical v2.0; reconcile latest revision before sign-off. ECS crystal evidence is in crystal_candidates.md.

DigiKey: [33 pF](https://www.digikey.com/en/products/detail/kemet/C0805C330F5GACTU/2212505), [27 pF](https://www.digikey.com/en/products/detail/kemet/C0805C270F5GACTU/2212364). Listing availability is not a live stock guarantee. No hardware measurements performed.
