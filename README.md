# AITOS-v1 (Version 2.0 Canonical)

AITOS is a layered, event-driven processing pipeline for advanced algorithmic trading.

## Repository Engineering Structure

```
AITOS-v1/
├── .github/                  # GitHub Community & Automation
├── 00_Architecture/          # Master Architecture (v2.0 Freeze)
├── 01_Modules/               # Standardized Module Specifications
│   └── [MODULE-ID]/
│       ├── README.md
│       ├── SPECIFICATION.md
│       ├── INTERFACE.md
│       ├── STATE_MACHINE.md
│       ├── ALGORITHMS.md
│       ├── TEST_PLAN.md
│       ├── CHANGELOG.md
│       ├── diagrams/
│       ├── examples/
│       └── implementation/
├── 02_Datasets/              # Market Data & Training Sets
├── 03_Research/              # Research Library (SMC, Wyckoff, etc.)
├── 04_Tests/                 # unit, integration, simulation, backtesting
├── 05_Implementation/        # python, cpp, rust, shared
├── 06_Interfaces/            # Schema Specifications
├── 07_Standards/             # Naming, Coding, Documentation, Testing
├── 08_Docs/                  # Project-wide Documentation Assets
└── README.md
```

## Current Status
The repository is in the **Architecture Freeze (v2.0)** state. This structure serves as the canonical engineering framework for all future development.

## Core Documents
- [Master Architecture](./00_Architecture/AITOS_Master_Architecture.md)
- [Module Index](./00_Architecture/MODULE_INDEX.md)
- [Development Roadmap](./00_Architecture/DEVELOPMENT_ROADMAP.md)

## License
This project is licensed under the [LICENSE](LICENSE).
