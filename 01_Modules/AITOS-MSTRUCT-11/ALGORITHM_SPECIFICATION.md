---
Module: AITOS-MSTRUCT-11
Module Name: Market Structure Engine
Version: 1.0.0
Status: Draft
Step: 03 - Algorithm Specification
Date: 2026-08-08
Authority: Implementation Engineer
Architecture Freeze: 🔒 ACTIVE
---

# AITOS-MSTRUCT-11: Algorithm Specification

## 1. Document Control
This document serves as the authoritative, deterministic algorithm specification for the Market Structure Engine. It translates architectural principles and research findings into precise engineering rules for implementation.

## 2. Algorithm Scope
The algorithm identifies market structural elements (Swing Points, BOS, CHoCH, Key Levels) and classifies market regimes using a Hidden Markov Model (HMM) based on closed-bar processing.

## 3. Input Preconditions
Adheres to Step 02 validated contracts:
- `OHLCVBar.schema`
- `SessionLiquidity.schema`
- Required metadata: `TickSize`.

## 4. Processing Lifecycle (Per Closed Bar $t$)
1.  **Validation:** Verify chronological order and data integrity.
2.  **Indicators:** Update ATR(14), ADX(14), and rolling volume averages.
3.  **Swing Detection:** Detect confirmed swings at bar $t-N$.
4.  **Structural State:** Update active trend, range, and key levels.
5.  **Events:** Detect BOS, CHoCH, or Liquidity Sweeps.
6.  **Features:** Extract normalized feature vector $\mathbf{f}_t$.
7.  **Inference:** Execute HMM forward filter update.
8.  **Output:** Map results to validated interface schemas.

## 5. Data Validation
- **Out-of-Order:** If $Timestamp_t \le Timestamp_{t-1}$, reject bar.
- **Duplicate:** If $Timestamp_t = Timestamp_{t-1}$, use latest (overwrite).
- **Invalid OHLCV:** If $High < Low$ or $NaN$ present, skip bar, output `INDETERMINATE`.
- **Zero Range:** If $High = Low$, use $TickSize$ as denominator guard for indicators.
- **Missing Metadata:** If `TickSize` is missing, throw configuration error.

## 6. Indicator Computation
- **ATR(14):** Wilder's smoothed Average True Range.
- **ADX(14):** Standard Average Directional Index.
- **Volume Average:** 20-period simple moving average of volume.

## 7. Swing Detection
- **Window:** Fixed $N = 3$.
- **Swing High at $i$:** $High_i > High_{i \pm 1,2,3}$. Confirmed at close of bar $t = i + 3$.
- **Swing Low at $i$:** $Low_i < Low_{i \pm 1,2,3}$. Confirmed at close of bar $t = i + 3$.
- **Tie-Breaking:** If $High_i = High_j$, the earlier index is the swing point.
- **Equality:** $|P_1 - P_2| \le \epsilon_t$, where $\epsilon_t = TickSize \times 1.0$.

## 8. Structural State Formation
- **Structural Leg:** The price movement between a confirmed Swing Low and the subsequent confirmed Swing High (Bullish Leg) or vice versa.
- **Key Structural Leg:** The leg responsible for the current $SH_{max}$ (in uptrend) or $SL_{min}$ (in downtrend).
- **Support/Resistance:** Derived from the latest confirmed swing points.

## 9. BOS Detection
- **Buffer:** $\delta_t = 0.2 \times ATR(14)$.
- **Bullish BOS:** $Close_t > SH_{last} + \delta_t$ (Active in UPTREND/RANGE).
- **Bearish BOS:** $Close_t < SL_{last} - \delta_t$ (Active in DOWNTREND/RANGE).

## 10. CHoCH Detection
- **Bearish CHoCH:** In UPTREND, $Close_t < SL_{key} - \delta_t$, where $SL_{key}$ initiated the leg to $SH_{max}$.
- **Bullish CHoCH:** In DOWNTREND, $Close_t > SH_{key} + \delta_t$, where $SH_{key}$ initiated the leg to $SL_{min}$.

## 11. Liquidity Sweep Classification
- If $High_t > SH_{key}$ but $Close_t \le SH_{key} + \delta_t$, it is a **Liquidity Sweep**, not a CHoCH.

## 12. Feature Extraction ($\mathbf{f}_t$)
- **f1 (HH Ratio):** Count of consecutive higher-highs in last 10 bars / 10.
- **f2 (HL Ratio):** Count of consecutive higher-lows in last 10 bars / 10.
- **f3 (Range Pos):** $(Close_t - SL_{active}) / (SH_{active} - SL_{active})$. Guard: if denom=0, $f3=0.5$.
- **f4 (Slope):** Z-scored slope of log-price regression over last 5 confirmed swings.
- **f5 (ADX):** $ADX(14) / 100$.
- **f6 (Event):** Categorical encoding: $+1$ (BOS_UP), $-1$ (BOS_DOWN), $+2$ (CHoCH_UP), $-2$ (CHoCH_DOWN), $0$ (None).

## 13. HMM Model
- **States:** UPTREND(1), DOWNTREND(2), RANGE(3), BREAKOUT_UP(4), BREAKOUT_DOWN(5), INDETERMINATE(6).
- **Prediction:** $\hat{\pi}_t = A^T \pi_{t-1}$.
- **Correction:** $\pi_t(k) \propto \hat{\pi}_t(k) \times \mathcal{N}(\mathbf{f}_t | \mu_k, \Sigma_k)$.
- **Stability:** Floor probabilities at $1e-10$ before normalization.

## 14. Offline Calibration
- **Transition Matrix $A$:** Estimated via Baum-Welch on historical observation sequences.
- **Emission ($\mu_k, \Sigma_k$):** Estimated via Maximum Likelihood Estimation (MLE) on labeled regime segments.

## 15. Runtime Inference
- Matrix $A$ and Gaussian parameters are **FROZEN** at runtime.
- Only recursive forward filtering is executed.

## 16. Multi-Timeframe Isolation
- Each timeframe maintains its own state object (buffers, swings, belief vector).
- No cross-contamination permitted.

## 17. Warm-Up and Readiness
- **$N_{warmup} = 100$** closed bars.
- No outputs emitted until $t \ge 100$.

## 18. Look-Ahead / Leakage Prevention
- [ ] Swings confirmed only after $N$ bars.
- [ ] Features use only closed-bar data.
- [ ] $f3$ uses levels from bar $t-1$.
- [ ] Multi-TF uses only closed higher-TF bars.

## 19. Determinism & Reproducibility
- Use IEEE 754 float64.
- Fixed seed for any initialization.
- State serialization for replay.

## 20. Output Mapping
- Map $\pi_t$ to `BeliefState`.
- Map levels to `KeyLevels`.
- Map BOS/CHoCH to `StructuralAlert`.
- Map bias to `StrategyBias`.

## 21. Suspended Components
- **Adaptive N:** SUSPENDED (Needs calibration).
- **Breakout ML:** SUSPENDED (Undefined horizon).
- **Online Learning:** PROHIBITED (Prevents drift).

## 22. Open Decisions
- **OPEN SPECIFICATION ITEM:** Final values for $\mu_k, \Sigma_k$ (Requires offline training run).

## 23. Algorithm Pipeline
1. Ingest bar $t$.
2. Validate timestamp $> t-1$.
3. Update ATR/ADX.
4. Check for swing at $t-3$.
5. Evaluate BOS/CHoCH conditions.
6. Extract features $f_1 \dots f_6$.
7. Run HMM Predict & Correct.
8. Publish outputs.
