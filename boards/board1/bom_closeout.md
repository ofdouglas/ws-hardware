Current acceptance: [ADR-039](../../docs/decisions/039-bom-closeout-selections.md) closes bias/LED MPNs, multidrop support, header cuts and PCB-pad test access. Fitted scope ground pins are required in B1-B075; exact MPN/count remain open. The recommendation tables below are retained as review history, not new requests to select these again. GPIO series resistors remain proposed.

# Board 1 BOM closeout recommendations

Reviewed 2026-09-06 after ADR-038. ESDS452DBZR is now accepted in B1-B073, with the disclosed +/-5.5 V bench operating envelope. All other recommendations below remain proposed. The audit covers all proposed rows and accepted rows with unknown MPN/count, plus support hidden behind selected IC rows. Component acceptance and implementation qualification remain separate.

## Next part and scope decisions

| Priority / allocation | Recommended resolution | Remaining qualification |
|---|---|---|
| B1-B071: two bias resistors | TE **CRGP0805F330R**, 330 ohm 1%, 0805, 1/3 W; DigiKey **A130471CT-ND** | Temperature derating, pulse exposure and power-off backfeed |
| B1-B026: five LED resistors | Accept existing **RK73H2ATTD3301F**, 3.3 kohm 1%, 0805, 0.25 W; **2019-RK73H2ATTD3301FCT-ND** | Confirm low-current brightness of selected LEDs |
| B1-B008: multidrop support | Four **RMCF0805FT10K0** /OE pull-ups to 3V3_SYS (reuse existing selected MPN), plus one **RMCF0805FT470R**, 470 ohm 1%, 0805, 0.125 W shared bus pull-up; **RMCF0805FT470RCT-ND** | 470 ohm remains a proposed value; rise-time, aggregate capacitance, enable/reset timing and actual baud must pass |
| B1-B059: four debug headers | Cut four 1x3 sections from already selected **PRPC040SAAN-RC**; keep four placement counts distinct from source-strip purchase count | Final TX/RX/GND order and off-state adapter protection |
| B1-B027: GPIO headers | Adopt proposed four GPIOs plus GND per MCU: four 1x5 sections from the same strip; one 40-position strip covers 20 GPIO-header positions + 12 debug positions = 32 positions | Final pad/mux allocation and cut waste; use the proposed 220 ohm per-GPIO network only after its load contract is accepted |
| B1-B011: test access | Exposed labeled PCB pads for signals and rails; nearby ground pads for scope springs; no purchased signal test-point hardware by default | Final probe access/locations in layout; retain row ID when recording no fitted hardware |
| B1-B007: residual CAN protection | No additional components beyond selected TVS and terminations for the current bench baseline; retire this aggregate after confirming the circuit has no residual parts | Do not silently add chokes, series components or DNP footprints; B1-Q004 transient/layout review remains |

Bias resistor rationale: the 1/3 W TE part gives more continuous-power room than a generic 1/8 W resistor. At a conservative VCC=3.6 V and A=-5.5 V screen, P=(3.6+5.5)^2/(330*0.99)=0.2535 W. This is below nameplate power but still requires derating; it is not fault or pulse qualification. Normal idle dissipation is approximately 6.9 mW per resistor. The exact 330 ohm value is already accepted; only MPN/rating needs a decision.

The proposed 470 ohm bus pull-up draws at most about 7.74 mA at 3.6 V and -1% resistance before output voltage drop, dissipating about 27.9 mW. This is close enough to the LV125's cited 8 mA operating test point that final low-level and timing margins matter. At 100 pF the ideal 10–90% rise estimate is 2.2RC=103 ns; it is not a 12 Mbaud qualification. Reuse the 10 kohm MPN, not quantities already allocated elsewhere.

Sourcing/evidence retrieved during this review:
- [TE CRGP0805F330R exact manufacturer page](https://www.te.com/en/product-1-2176327-9.html); [DigiKey passive-product listing](https://www.digikey.in/en/products/detail/te-connectivity-passive-product/CRGP0805F330R/8577073) showed 21,254. Use A130471CT-ND; the separate AMP listing is a non-stocked large-quantity order and is unsuitable for prototypes.
- [KOA LED resistor](https://www.digikey.com/en/products/detail/koa-speer-electronics-inc/RK73H2ATTD3301F/10234403) confirms exact part/specification; existing manufacturer source is in B1-B026. No fresh stock quantity was captured for this row.
- [Stackpole 470 ohm resistor](https://www.digikey.com/en/products/detail/stackpole-electronics-inc/RMCF0805FT470R/1760300) showed 153,419; exact code/specification confirmed. Series manufacturer PDF retrieval failed this review; existing family selection is not full new-value qualification.
- [Three-position Sullins listing](https://www.digikey.com/en/products/detail/sullins-connector-solutions/PRPC003SAAN-RC/2775251) showed zero stock, while its 40-position alternative showed 48,749. Use the already-selected strip and its linked drawing in B1-B027. The dedicated CAN two-pin headers remain separate and are not counted against this strip.

All availability is page evidence, not reserved inventory; refresh before purchase.

## Circuit decisions that prevent a complete order list

| Allocation | Recommended resolution path |
|---|---|
| B1-B023 RS-485 controls | Propose a 10 kohm DE pull-down for driver-disabled reset. Propose /RE pull-up for receiver disabled/shutdown during reset, plus an RX pull-up to hold MCU input high while RO floats; reuse RMCF0805FT10K0. Review firmware enable sequence, rail state and input leakage before accepting exact quantities. TVS, bias, bypass and termination are already separately counted. |
| B1-B010 MCU reset/boot | Draw each exact MCU's reset/boot circuit before selecting support counts. Reuse selected 10 kohm/100 nF MPNs only where the manufacturer circuit and debug timing require them. Gateway NRST must be one shared open-drain net; do not count another reset network inside B1-B053. Determine whether physical reset buttons are wanted; SWD reset is already provided. |
| B1-B053 CBUS recovery | Recommend an open-drain reset sink and a main-rail-referenced BOOT0 driver with default low and bridge-to-main power-off isolation. Establish polarity/truth table for startup, ROM programming and SWD reset before picking ICs. The two existing quad buffers are fully used; no spare channel may be assumed. |
| B1-B016 VCP support, partly B1-B017 | Complete the /OE/default network so firmware-independent ROM recovery works after USB configuration, and receive inputs stay defined when buffers are disabled. Enumerate each resistor only after checking which side of each channel is powered. Existing bypass is already allocated. |
| B1-B060 debug off-state protection | Recommend hardware isolation of incoming adapter TX while the main rail is off, with defined MCU RX idle levels; examine both signal directions for an unpowered adapter. Series resistors alone do not meet power-off isolation. Choose the isolation topology before an exact IC/count; retain 115200-baud, 3.3 V-only adapters. |
| B1-B017 and B1-B061/062/063 bridge rails | Freeze the FT232HL reference circuit pin by pin, enumerate supply bypasses, derived-rail capacitors and any filters, and assign quantities to the already accepted capacitor rows. Follow current ADRs: TPS560430, 47 nF TPS22810 CT, no external FTDI supervisor. The accumulated USB notes contain historical SC189/1 uF CT/supervisor text; do not use those passages as current BOM authority. No extra capacitor counts should be guessed. |
| USB connector shell | Proposed starting approach: direct shell bond to a short local ground region at the connector for this bench PCB, with chassis/enclosure strategy revisited if applicable. Settle the bond in the layout/EMC review; an RC or bead network should not appear in the BOM without a stated purpose and circuit decision. |

The best next circuit work is the power-off-safe interfaces (CBUS/VCP/debug), followed by FTDI rail enumeration. Those determine several real part counts. Settling resistors and header cuts alone will not make the BOM procurement-ready. CAD reference designators, verified footprints, supported rates, power and hardware qualification remain open across already-decided parts; these are not requests to reselect their MPNs.

Checks performed: read current CSV and accepted decision index, inspected every proposed or accepted-TBD row, compared split allocations, checked exact candidate listings, and calculated the passive screens above. No schematic connectivity, ERC/DRC or bench validation claimed.
