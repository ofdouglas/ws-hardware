---
id: ADR-021
title: TPS560430X3FDBVR main buck and USB-current efficiency criterion
status: accepted
scope: Board 1 Rev A
created: 2026-09-06
accepted_by: User explicitly committed to TPS560430X3FDBVR
supersedes: ADR-010 converter/filter selection and 30 uF restriction; previous 90 percent efficiency floor
superseded_by: none
---

# Decision

Select TI TPS560430X3FDBVR, fixed 3.3 V, 600 mA, 1.1 MHz forced PWM, SOT-23-6. Retain MCU/transceiver decoupling locations and independent USB bridge / PWREN# main-enable architecture. SC189ZSKTRT and its specific LC network are superseded. Datasheet starting filter is 12 uH and 22 uF local output; these are proposed values pending stability, effective capacitance and sourcing review, not qualified final components. Add required 100 nF bootstrap capacitor between CB and SW. Do not copy SC189 footprint/pin numbers. No 30 uF limit is carried forward.

The efficiency acceptance criterion is total USB input <=500 mA at the conservative operating load, not a 90% buck floor. At 380.55 mA on 3.3 V, 100 mA bridge/control allowance and 4.45 V converter input, break-even efficiency is 70.5514%. At 80% it is about 453 mA total USB; at 85%, 432 mA. This is a steady-state planning estimate; input-path losses, actual converter performance, new support loads and startup peaks must be included in final qualification.

# Input design status

The user is considering TPS22919DCKR and removal of the external FTDI reset supervisor. This is under evaluation, not a silently accepted replacement for ADR-019/020. See the input-design review in vbus_protection_proposal.md. TPS22919's 6 V absolute maximum makes it incompatible with treating the existing SMF6.0A as sufficient raw-input clamping. Faster turn-on may remove the motivation for a reset supervisor but does not itself qualify input inrush or ESD/hotplug behavior.

# Evidence / remaining work

[TI TPS560430 datasheet](https://www.ti.com/lit/ds/symlink/tps560430.pdf); [DigiKey exact part](https://www.digikey.com/en/products/detail/texas-instruments/TPS560430X3FDBVR/9094603), cut tape 296-51994-1-ND. Electrical review, inductor/capacitor MPNs, LC stability, input protection, sequencing, USB startup and board tests remain unverified. Do not reopen the buck choice based on light-load efficiency or an obsolete 90% target.
