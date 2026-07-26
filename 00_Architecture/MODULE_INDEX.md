---
Architecture Version: 2.0
Release: Canonical v2
Status: Approved
Last Updated: 2026-07-25
---

# AITOS v2 Module Index

| Order | Module ID | Module Name | Version | Status | Dependencies | Input Modules | Output Modules | Development Stage |
|---|---|---|---|---|---|---|---|---|
| 1 | AITOS-MICRO-08 | Market Microstructure Engine | 1.0 | Production | AITOS-MD-01..07 | AITOS-DATA (market data) | AITOS-MSTRUCT-11, AITOS-EXOTC-09, AITOS-SESSION-10, AITOS-ALPHA, AITOS-CONTEXT, AITOS-EXEC-14, AITOS-MONITOR | Complete |
| 2 | AITOS-EXOTC-09 | Exchange & OTC Venue Management | 1.0 | Production | AITOS-MICRO-08, AITOS-EFF-07, AITOS-RISK (credit) | AITOS-MICRO-08, AITOS-RISK-10, market data feeds | AITOS-SESSION-10, AITOS-EXEC-14, AITOS-MONITOR | Complete |
| 3 | AITOS-SESSION-10 | Trading Session & Market Calendar Engine | 1.0 | Production | AITOS-EXOTC-09, AITOS-MICRO-08, AITOS-EFF-07 | AITOS-EXOTC-09, AITOS-MICRO-08, calendars, time source | AITOS-MSTRUCT-11, AITOS-EXEC-14, AITOS-ALPHA, AITOS-CONTEXT, AITOS-MONITOR | Complete |
| 4 | AITOS-MEF-07 | Market Efficiency Evaluation & Strategy Validation | 4.0 | Production | AITOS-MD-01..06 | AITOS-REGIME, AITOS-RISK, AITOS-EXEC, AITOS-PORT, AITOS-ALPHA, AITOS-MONITOR | AITOS-ALPHA (signal validation), AITOS-CONTEXT | Complete |
| 5 | AITOS-MSTRUCT-11 | Market Structure Engine | 2.0 | Production | AITOS-MICRO-08, AITOS-SESSION-10, AITOS-RISK-10 | AITOS-MICRO-08, AITOS-SESSION-10, AITOS-RISK-10 | AITOS-ALPHA, AITOS-CTA-12, AITOS-WYCKOFF-13, AITOS-CONTEXT, AITOS-MONITOR | Complete |
| 6 | AITOS-CTA-12 | Classical Technical Analysis Engine | 1.0 | Production | AITOS-MICRO-08, AITOS-MSTRUCT-11, AITOS-SESSION-10, AITOS-RISK-10 | AITOS-MSTRUCT-11, AITOS-SESSION-10 | AITOS-ALPHA, AITOS-WYCKOFF-13, AITOS-CONTEXT, AITOS-MONITOR | Complete |
| 7 | AITOS-WYCKOFF-13 | Wyckoff Method Engine | 1.1 | Production | AITOS-MSTRUCT-11, AITOS-CTA-12, AITOS-MICRO-08, AITOS-SESSION-10, AITOS-RISK-10 | AITOS-MSTRUCT-11, AITOS-CTA-12, AITOS-MICRO-EXT (future), AITOS-SESSION-10 | AITOS-ALPHA, AITOS-SMC, AITOS-CONTEXT, AITOS-MONITOR | Complete |
| 8 | AITOS-SMC | Smart Money Concepts Engine | 1.0 | Specification Pending | AITOS-MICRO-08, AITOS-MSTRUCT-11, AITOS-CTA-12, AITOS-WYCKOFF-13, AITOS-SESSION-10, AITOS-MEF-07 | AITOS-MICRO-08, AITOS-MSTRUCT-11, AITOS-CTA-12, AITOS-WYCKOFF-13, AITOS-SESSION-10, AITOS-MEF-07 | AITOS-CONTEXT, AITOS-ALPHA | In Design |
| 9 | AITOS-CONTEXT | Market Context Engine | 1.0 | Specification Pending | AITOS-MSTRUCT-11, AITOS-CTA-12, AITOS-WYCKOFF-13, AITOS-SMC, AITOS-MEF-07, AITOS-MICRO-08, AITOS-SESSION-10 | All analysis modules | AITOS-ALPHA, AITOS-RISK-10, AITOS-PORT, AITOS-AI, AITOS-MONITOR | In Design |
| 10 | AITOS-ALPHA | Alpha Decision Engine | 1.0 | Specification Pending | AITOS-CONTEXT | AITOS-CONTEXT | AITOS-RISK-10, AITOS-PORT | In Design |
| 11 | AITOS-RISK | Risk Management Engine | 1.0 | Specification Pending | AITOS-CONTEXT, AITOS-PORT (as service) | AITOS-CONTEXT, AITOS-PORT (state) | AITOS-PORT (risk constraints), AITOS-MONITOR | In Design |
| 12 | AITOS-PORT | Portfolio Management Engine | 1.0 | Specification Pending | AITOS-ALPHA, AITOS-RISK, AITOS-CONTEXT | AITOS-ALPHA, AITOS-RISK, AITOS-CONTEXT | AITOS-EXEC-14, AITOS-MONITOR | In Design |
| 13 | AITOS-EXEC | Execution Engine | 1.0 | Specification Pending | AITOS-MICRO-08, AITOS-EXOTC-09, AITOS-SESSION-10, AITOS-PORT | AITOS-MICRO-08, AITOS-EXOTC-09, AITOS-SESSION-10, AITOS-PORT | AITOS-MONITOR | In Design |
| 14 | AITOS-MONITOR | Monitoring & Health Engine | 1.0 | Specification Pending | All modules | All modules | AITOS-LEARN, AITOS-AI, alerts | In Design |
| 15 | AITOS-LEARN | Learning Engine | 1.0 | Specification Pending | AITOS-MONITOR, all trainable modules | AITOS-MONITOR, all trainable modules | Updated model parameters to respective modules | In Design |
| 16 | AITOS-AI | AI Decision & Reasoning Engine | 1.0 | Specification Pending | AITOS-CONTEXT, AITOS-ALPHA, AITOS-RISK, AITOS-PORT, AITOS-MONITOR | AITOS-CONTEXT, AITOS-ALPHA, AITOS-RISK, AITOS-PORT, AITOS-MONITOR | AITOS-EXEC-14 (override), AITOS-PORT (override) | In Design |
| 17 | AITOS-DEV-AGENT | AITOS Development Agent | 1.0 | Proposed | All modules | User commands, GitHub Events | Repository updates, PRs, Docs | In Design |
