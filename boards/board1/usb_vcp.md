# USB bridge, VCP and gateway recovery

Status: selected baseline with implementation checks open. Authority: ADR-001/005/013/015/018/022/024/027/028/030/031/040/042. See [USB input](usb_input.md) for the attachment ramp, buck enable circuit and current model; this note does not reinstate earlier converter or supervisor proposals.

## Power domains and control

USB-B USB-B1HSB6 feeds TPS22810DBVT and the ramped USB_5V rail. FT232HL-REEL VREGIN uses USB_5V. Its independent FTDI_3V3 supply remains available while 3V3_SYS is off. Use the documented FTDI 5 V bus-powered arrangement: VCCD is the 3.3 V output, supply every VCCIO, implement the specified VPHY/VPLL supply filtering, and treat VCORE/VCCA as internal 1.8 V outputs. Do not join regulator outputs or power the main board from VCCD. The [captured schematic](kicad/README.md) supplies the exact rail/pin allocation; B1-Q002 retains electrical qualification.

FTDI PWREN# -> MC74HC1G14DBVT1G on FTDI_3V3 -> TPS560430 EN. RMCF0805FT10K0 pulls PWREN# up; ERJ-6GEYJ473V pulls EN down. RESET# has RMCF0805FT10K0 to FTDI_3V3 and CL21B103KBANNNC (10 nF) to ground. No external reset supervisor is fitted. Input switch EN is tied to VIN: it controls attachment slew, while PWREN# controls main-board operation.

| State | Bridge | Main rail | Required behavior |
|---|---|---|---|
| Unplugged | Off | Off | External signal paths must not back-power rails |
| Attached, unconfigured | On | Off | Enumeration and EEPROM access within startup budget |
| Configured | On | On | VCP and networking within allowed USB current |
| Suspend | Low-power state | Off | Whole-device leakage/current within suspend budget |
| Resume | Active | Restarts | Safe reset, enable and interface sequencing |

Rev A requires an active PC. USB limits apply to the whole device: 100 mA before configuration, permitted descriptor current up to 500 mA afterward, and the applicable suspend limit (2.5 mA budget). Startup charging is additional demand to account for, not extra permission.

## EEPROM and bridge passives

AT93C56B-SSHM-B uses FTDI VCCD and ORG strapped to VCC for x16 organization. Connect EEDATA directly to DI and through RC0805FR-072K2L (2.2 kohm) to DO; RMCF0805FT10K0 pulls DO to the EEPROM supply. REF uses RMCF0805FT12K0 (12 kohm, 1%) to ground. The FTDI crystal and its two 27 pF capacitors are selected in [crystal networks](crystal_networks.md).

The completed reference-circuit enumeration is recorded in the CSV and native CAD: B1-B061 has 11 x 100 nF, B1-B063 has 2 x 4.7 uF, B1-B062 has zero parts. EEPROM/inverter bypass is included once. Two separate 600 ohm ferrites B1-B078 feed VPHY and VPLL. B1-B017 now has zero residual parts; optional post-bead bulk is not fitted and has no DNP footprints.

B1-Q012 retains the EEPROM datasheet checks (DS20006260B pp.8–11): maximum 1 MHz clock at 3.3 V, up to 5 ms word-write, supply rise no faster than 0.1 V/us, at least 100 us stable supply before commands and at least 500 ms at 0 V between full power cycles. Verify FTDI read timing, programming/readback and rapid replug recovery. Bulk erase/write have higher supply requirements; word programming at 3.3 V needs verification in the actual setup.

Captured configuration contract: UART mode with VCP enabled; bus powered, 500 mA descriptor; unique serial; ACBUS0 (pin 21) = PWREN#. Keep unused ACBUS pins at TriSt-PU, except ACBUS7 at its default pull-down; disable “Suspend on ACBUS7 Low” and remote wake. Enable the FTDI interface pull-down-in-suspend option recommended with PWREN#. ACBUS5/6 remain physically unconnected for Rev A.

Bring-up procedure: enumerate on the active PC, use FT_PROG to scan/read and save the original settings, program the x16 EEPROM with the above settings using normal word programming, then read back and save the resulting configuration. Unplug for at least 500 ms at zero supply, reconnect and confirm ACBUS0 stays high before configuration and goes low after configuration. Verify suspend switches off 3V3_SYS and resume restarts it. With no valid EEPROM, the documented ACBUS0 default is TriSt-PU, reinforced by R2, so the intended main-rail default is off. No programming/readback or waveform test has been performed.

## VCP isolation and recovery

SN74LV125APWR B1-B016 is powered by 3V3_SYS and uses all four channels for TX/RX/RTS/CTS, two in each direction. This is power-off signal isolation, not galvanic isolation. ADR-040 accepts PWREN# directly to all four /OE inputs, with the existing bridge-domain pull-up; no separate rail-valid logic or SYS pull-up is required. Six captured 10 kohm defaults B1-B079 pull the two gateway-bound outputs and two gateway-driven buffer inputs to 3V3_SYS, and FTDI RX/CTS inputs to FTDI_3V3. Startup timing is settled; retain the existing FTDI reset RC and input ramp. The VCP enable remains independent of application firmware. Verify thresholds, leakage and propagation at 12 Mbaud with short gateway/FTDI routes (B1-Q002/008).

[ADR-042](../../docs/decisions/042-header-resistors-recovery-scope.md) defers automated CBUS reset/BOOT0 recovery to Rev B. Leave ACBUS5/6 unconnected; B1-B053 has zero Rev A parts/footprints. Retain default-low gateway BOOT0 and NRST shared with SWD under B1-B010/B1-Q005. No Linux CBUS control or ROM-programming sign-off is required for Rev A.

## Evidence and completion

[FT232H datasheet](https://ftdichip.com/wp-content/uploads/2024/09/DS_FT232H.pdf), [UM232H bus-power guidance](https://ftdichip.com/wp-content/uploads/2020/07/DS_UM232H.pdf), and [EEPROM ADR/evidence](../../docs/decisions/018-ftdi-eeprom.md) are retained sources. Earlier review used FT_000288 v2.2; current datasheet/errata reconciliation remains open. Earlier research is retained in Git history.

Validate current waveforms, EEPROM/reset timing, full-duplex VCP/flow control, off-state leakage and resume and SWD programming. No schematic or bench sign-off is asserted; [requirements](requirements.md) retains B1-Q002/008/012; B1-Q013 is resolved by Rev A deferral.

Current disposition: ADR-040 settles startup/direct PWREN# enable; ADR-042 defers automated recovery. Power/USB support and all four isolation channels are now captured; remaining qualification is staged in [capture notes](kicad/README.md), and measurements belong to bring-up.
