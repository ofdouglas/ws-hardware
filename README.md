# WireSpaces hardware

Status: draft · Owner: project maintainer · Updated: 2026-09-06

Hardware experiments for WireSpaces (WS), starting with a small four-MCU bench board. This repository is a design scaffold, not a fabrication release. Selected parts and project-local symbol libraries exist; Board1 now has a complete draft KiCad schematic and reconciled counts; schematic approval, layout and hardware qualification remain. This is not a validated fabrication or ordering package.

## Start here

1. Read [agent instructions](AGENTS.md) and [document/decision conventions](docs/DESIGN_PRINCIPLES.md).
2. Read [system context](docs/WIRESPACES_SYSTEM_CONTEXT.md) and [family architecture](docs/HARDWARE_ARCHITECTURE.md).
3. Check the [ADR index](docs/decisions/README.md) before changing a decision.
4. Work from [Board 1 requirements](boards/board1/requirements.md), then its [current design overview](boards/board1/README.md), [pinmap](boards/board1/pinmap.md) and [BOM](boards/board1/bom.csv).

```text
ws-hardware/
├── AGENTS.md
├── README.md
├── docs/
│   ├── WIRESPACES_SYSTEM_CONTEXT.md
│   ├── HARDWARE_ARCHITECTURE.md
│   ├── DESIGN_PRINCIPLES.md
│   ├── PART_SELECTION_POLICY.md
│   ├── SOURCE_NOTES.md
│   └── decisions/                 # index, template, numbered ADRs
├── boards/board1/
│   ├── README.md
│   ├── requirements.md
│   ├── pinmap.md
│   ├── bom.csv
│   └── kicad/                    # board CAD workspace; see board status
└── libraries/
    ├── symbols/
    └── footprints/
```

Board 1's Rev A networking scope has one STM32 gateway, three SAM leaves, two shared CAN-FD buses, an onboard multidrop UART, a private SAM UART ring, USB power/VCP, one external RS-485, signal terminals for both CANs and RS-485 with ground, and debug access. The full bench backbone is future work. Exact MVP inclusion is controlled by the requirements status rows, not by this overview.

Use **Host**, `HostId`, `SrcHostId`, and `DestHostId`. A PC is a PC/test controller; a WS Host is a protocol identity and need not be a PC.

See [source provenance](docs/SOURCE_NOTES.md). Source drafts provide context, not automatic approval for added hardware. Keep small, reviewable changes with requirement IDs and evidence. Resolve the blocking questions in Board 1 requirements before schematic freeze.
