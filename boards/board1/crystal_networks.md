# Crystal network proposal

Status: initial fitted values accepted ADR-031; 33 pF MPN replaced by ADR-044 and 27 pF MPN by ADR-045, 2026-09-06. Crystal MPNs finalized ADR-030. B1-Q008 owns startup, gain, drive and frequency qualification.

| Oscillator | Crystal CL | Capacitors to ground | Qty / board | Accepted initial part |
|---|---:|---:|---:|---|
| STM32 gateway | 20 pF | 33 pF each side | 2 | YAGEO CC0805FRNPO9BN330 |
| Three SAM C21 | 20 pF | 33 pF each side | 6 | YAGEO CC0805FRNPO9BN330 |
| FT232HL | 18 pF | 27 pF each side | 2 | YAGEO CC0805FRNPO9BN270 |

Both parts are 0805, 50 V, C0G/NP0, +/-1%. Use C0G for frequency-setting capacitors. Eight 33 pF and two 27 pF are accepted allocation quantities, not electrically qualified production values. No extra crystal or auxiliary oscillator added.

For equal external capacitors, CL approximately equals C/2 + Cs, where Cs is equivalent pin/PCB parasitic loading seen across the crystal (do not simply add both pin capacitances or the crystal's own shunt C0). Thus 33 pF implies Cs=3.5 pF for CL20, while 27 pF implies Cs=4.5 pF for CL18. These are initial estimates, not measured device capacitances. The MCU and FTDI estimates differ; even STM32 and SAM may need different final values. A measured Cs of 5 pF would call for approximately 30 pF and 26 pF respectively. FTDI shows 27 pF as an example, not a universal required value.

Place each crystal and two capacitors close to its IC; short quiet traces and short ground returns; keep switching nodes/digital traces away. Do not add generic 1 Mohm feedback resistors or guessed series damping values. Review each IC's oscillator circuit first. An output-side series resistor may be needed if measured drive exceeds crystal rating; its value trades drive against startup margin. Existing core crystal limit is 100 uW; FTDI crystal limit 500 uW per reviewed ECS series documents. SAM XOSC gain/startup settings and STM32 HSE gain margin need review with the selected high-CL crystals before schematic freeze.

Check startup across rails/temperature, drive level, and loaded frequency. FTDI's narrow remaining loading-error budget makes fine adjustment important; 1% capacitors alone do not establish frequency accuracy. Prefer measuring a buffered/divided clock output where available; avoid loading a crystal pin with an ordinary oscilloscope probe. No extra DNP trim footprints are implied by this proposal; change the fitted capacitor values if needed.

Sources: [ST AN2867](https://www.st.com/resource/en/application_note/cd00221665.pdf), [FT232H oscillator example, section 6.3](https://ftdichip.com/wp-content/uploads/2020/07/DS_FT232H.pdf), [33 pF exact-part listing](https://www.digikey.com/en/products/detail/yageo/CC0805FRNPO9BN330/5883941), [27 pF exact manufacturer sheet](https://yageogroup.com/download/specsheet/CC0805FRNPO9BN270). FTDI source is historical v2.0; reconcile latest revision before sign-off. ECS crystal evidence is retained below.

DigiKey: [33 pF](https://www.digikey.com/en/products/detail/yageo/CC0805FRNPO9BN330/5883941), [27 pF](https://www.digikey.com/en/products/detail/yageo/CC0805FRNPO9BN270/8025262). Listing availability is not a live stock guarantee. No hardware measurements performed.

## Selected crystals and retained accuracy evidence

| Allocation | MPN | Reviewed limits |
|---|---|---|
| Four MCU oscillators | ECS-120-20-3X-EN-TR | 12 MHz, CL 20 pF, ESR 60 ohm, initial +/-30 ppm, temperature +/-50 ppm (-40 to +85 C), first-year aging +/-5 ppm; maximum drive 100 uW |
| FTDI oscillator | ECS-120-18-5PX-CKM-TR | 12 MHz, CL 18 pF, initial +/-10 ppm, temperature +/-10 ppm (-20 to +70 C), first-year aging +/-5 ppm; maximum drive 500 uW |

[ECS CSM-3X Rev.2017](https://ecsxtal.com/store/pdf/CSM-3X.pdf) and [CSM-7X Rev.2020](https://ecsxtal.com/store/pdf/csm-7x.pdf) retain the mechanical, ordering and drive evidence. MCU body is 7.0 x 4.1 x 2.3 mm; FTDI body is 11.4 x 4.8 x 4.3 mm. Both are leaded SMT selections, accepted ADR-014/030. Exact land-pattern review remains open.

FTDI first-year arithmetic is 10+10+5=25 ppm before loading, leaving 5 ppm against the reviewed +/-30 ppm recommendation ([FT232H v2.2 section 6.3](https://www.ftdichip.cn/Support/Documents/DataSheets/ICs/DS_FT232H.pdf)). This is not a lifetime or arbitrary-temperature aging guarantee. Reconcile the current FTDI revision and characterize loading/startup; do not apply FT4222H FAQ ESR limits to FT232H. MCU initial-plus-temperature screen is 80 ppm before aging/loading; complete peer and peripheral timing analysis in clocking.md.
