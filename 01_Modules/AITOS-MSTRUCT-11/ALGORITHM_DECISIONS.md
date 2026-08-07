---
Module: AITOS-MSTRUCT-11
Version: 1.0.0
Status: Approved
Date: 2026-08-08
---

# MSTRUCT-11: Algorithmic Decisions & Engineering Resolution

## 1. Executive Summary
This document records the final engineering decisions made during Step 03 (Algorithm Specification) to resolve research ambiguities and establish a deterministic implementation baseline.

## 2. Decision Matrix

| Component | Decision | Justification |
|---|---|---|
| **Swing Detection** | Fixed $N=3$ | Guarantees determinism; prevents unstable adaptive windows. |
| **Confirmation Delay** | $N$ bars | Eliminates look-ahead bias and repainting. |
| **BOS Confirmation** | Candle Close | Reduces noise compared to wick-only breaches. |
| **Price Equality** | $1.0 \times TickSize$ | Aligns with instrument precision; bans magic number fallbacks. |
| **HMM Update** | Offline Calibration Only | Prevents online probability drift and feedback loops. |
| **ML Models** | SUSPENDED | Pending formal target definitions and labeled datasets. |
| **Warm-up** | 100 Bars | Derived lower bound for indicator and filter stability. |

## 3. Conflict Resolution: BOS vs CHoCH
**Decision:** **CHoCH overrides BOS.**
**Rationale:** A Change of Character represents a fundamental shift in the structural leg origin, which occupies a higher hierarchical level than a simple Break of Structure (trend continuation). If both conditions are met, the reversal (CHoCH) is the authoritative state transition.

## 4. Feature f6 Encoding
**Decision:** **Signed Categorical Encoding.**
*   $+1$: Bullish BOS
*   $-1$: Bearish BOS
*   $+2$: Bullish CHoCH
*   $-2$: Bearish CHoCH
*   $0$: No Structural Event
**Rationale:** Provides a clear, non-ambiguous input for the HMM emission model to distinguish between continuation and reversal events.

## 5. Metadata Dependency
**Decision:** **Strict Precision Contract.**
The engine will not "guess" decimal places for Forex or other assets. It requires the `TickSize` metadata from the input stream. Failure to provide this results in an `UNRECOVERABLE_CONFIG_ERROR`.

---
*Authorized by: Chief Systems Architect*
