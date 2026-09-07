# WireSpaces system context

Status: draft · Authority: orientation only · Sources: SRC-INTRO, USR-01

WireSpaces (WS) is a lightweight embedded communication fabric for small MCU networks, gateways, multicore devices, and FPGA implementations. It carries bounded datagrams such as commands, telemetry, events, logs, and firmware segments across different physical media while preserving an Endpoint/Service model.

A **Wire** is a loop-free logical bus formed from configured Links. It may span heterogeneous Links, coincide with one Link, or exist inside one device. Several Wires may overlap on a Link. Forwarding follows static/read-mostly Wire topology; destination identity controls acceptance rather than ordinary next-hop routing.

An Endpoint Domain has one deployment-scoped **HostId**, used on every Wire it joins. Addressed PDUs identify `SrcHostId` and `DestHostId`. Multiple Hosts can originate traffic. Gateway/leaf are hardware roles, not distinct identity classes. Physical node labels such as `SAM0` do not assign numeric HostIds; deployment configuration does that.

The model favors bounded storage, visible resource exhaustion, simple local execution, and PC-side configuration/validation. A single PC-to-device Link should be useful before a full deployment is modeled. `kLocalBus` supports local one-Link bring-up with valid Host identity; it is not transparently forwarded. Exact packet layouts, bindings, and protocol conformance belong to the protocol project, not this hardware repository.

## Why these boards exist

Board 1 provides real simultaneous links on constrained MCUs so WS can be measured while forwarding, buffering, and servicing traffic. It supports comparisons between bare-metal/superloop and RTOS execution. It does not establish the smallest supported WS device.

The proposed first platform is a PC/VCP-connected STM32 gateway and three SAM leaves. All four share two CAN-FD buses and an open-drain UART; the leaves additionally form a directed UART ring. See the board requirements for node/link IDs and inclusion status.

A physical ring or two parallel CAN buses do not make cyclic logical Wires valid. Firmware deployment must construct loop-free propagation domains even when the hardware offers cycles or redundant paths.

## Broader direction, not Board 1 obligations

Future experiments may include Classical CAN/CAN FD/CAN XL, RS-485, native USB or FIFO interfaces, Ethernet/T1S, shared memory, FPGA softcores and RTL Endpoints, wireless bridges, repeaters, and smaller-memory targets. Not all are supported by Board 1 silicon or its MVP.

The full bench concept adds shared signal/power interconnects and independent instrumentation for reproducible timing and fault experiments. Those features remain separate from ordinary WS operation. Do not freeze speculative protocol features or enlarge the first PCB to realize the whole ecosystem.
