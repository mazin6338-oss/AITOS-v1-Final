---
Architecture Version: 2.0
Release: Canonical v2
Status: Approved
Last Updated: 2026-07-25
---

# Module 05: Market Structure Engine (AITOS‑MSTRUCT‑11 v2.0)

Metadata
Module ID: AITOS-MSTRUCT-11
Chapter: 11 – Market Structure (Phase 2)
Version: 2.0
Last Updated: 2026-07-20
Dependencies: AITOS-MICRO-08, AITOS-SESSION-10, AITOS-RISK-10
Status: Production

Purpose
To provide the AI with a rigorous, probabilistic assessment of market structure states—trend, range, reversal, breakout—across multiple timeframes. The
module translates raw price action into a real‑time belief state over market regimes, driving strategy selection, position sizing, and risk management with
quantified uncertainty.

Scope
Detect swing points and classify trend/range using formal hypothesis tests.
Maintain a Bayesian belief vector over structural states, updated on each bar close.
Identify breakouts with a logistic model that fuses price, volume, and volatility.
Model the regime‑switching dynamics as a Markov chain for forward‑looking state anticipation.
Integrate with execution and alpha modules to bias order flow.
Self‑calibrate detection parameters online based on false‑signal rate.

Internal State Representation
Per‑Instrument‑Timeframe State Object
{
"instrument_id": "EUR/USD",
"timeframe": "H1",
"belief_state": {
"prob_uptrend": 0.45,
"prob_downtrend": 0.05,
"prob_range": 0.40,
"prob_breakout_upside": 0.07,
"prob_breakout_downside": 0.03
},
"swing_points": [
{"time": "2026-07-20T10:00", "type": "high", "price": 1.1050},
{"time": "2026-07-20T09:00", "type": "low", "price": 1.0980}
],
"key_levels": {
"support": 1.0980,
"resistance": 1.1050,
"bos_level_up": null,
"bos_level_down": 1.0980
},
"transition_matrix": {
"uptrend_to_uptrend": 0.80
},
"detector_params": {
"swing_window": 3,
"bos_buffer_atr_mult": 0.2
},
"performance_metrics": {
"false_breakout_rate_30d": 0.22,
"trend_detection_lag_bars": 2.1
}

}

Knowledge Representation
Regimes: {UPTREND, DOWNTREND, RANGE, BREAKOUT_UP, BREAKOUT_DOWN, INDETERMINATE}.
Observation Model: For each bar, features x_t (HH count, HL count, distance from swing low/ATR, etc.) are computed. Likelihood P(x_t | R)
modeled via Gaussian mixtures per regime.
Prior & Posterior Update: The prior belief is propagated through a first‑order Markov transition matrix T (online estimate). Then posterior via
Bayes: b_t(R) ∝ P(x_t | R)·b̃_t(R).
Breakout Model: Logistic regression on breakout features to compute probability.

Belief State
Vector b_t of regime probabilities. Entropy H(b_t) used as confidence measure.

State Variables
As in the state object above.

Inputs
OHLCV bars (all timeframes) from AITOS-MICRO-08.
ATR(14) from Risk module.
Volume profile (optional) from AITOS-VOL-16.
Session liquidity score from AITOS-SESSION-10.

Outputs
BeliefState broadcast to Alpha, Execution, Risk.
Key level list (support, resistance, BOS triggers).
Alerts: structural_shift_alert when probability of new regime exceeds 0.7.
Strategy bias: allow_long, allow_short, prefer_mean_reversion derived from thresholds.

Core Reasoning Engine
1. Swing point detection (O(1) per bar).
2. Feature extraction.
3. Bayesian belief update with exponential smoothing of sufficient statistics for likelihoods.
4. Breakout detection with logistic model.
5. BOS/CHoCH as secondary features.

Mathematical Models
Markov transition: b̃t = T^T · b{t−1}
Posterior: b_t(R) = P(x_t | R)·b̃_t(R) / Σ
Breakout probability: p = σ(w·z + b)

Decision Rules
If prob_uptrend > 0.6 and prob_downtrend < 0.1: allow_long = True.
If prob_range > 0.5: prefer_mean_reversion.
If any breakout probability > 0.5: trigger breakout strategy.

If entropy > 1.5: reduce position size by 50%.

Constraint Engine
Not operational during low‑liquidity unless overridden.
Respect tick size for key levels.
For bars <1 min, skip Bayesian update; delegate to MICRO-08.
Rate‑limit updates to bar close.

Validation Engine
Monthly backtest of regime labels vs manually annotated data (accuracy > 80%).
False breakout rate < 0.3; recalibrate if higher.
Reliability diagrams to check calibration.

Monitoring Rules
Real‑time entropy tracking.
Alert if belief oscillates rapidly.
Monitor transition matrix stability.
Latency check: if update >1 ms per instrument, investigate.

Learning & Adaptation
Online likelihood model update: exponential smoothing of mean/covariance.
Transition matrix update: T_ij(new) = (1−β)·T_ij(old) + β·I
Parameter tuning (swing window, BOS buffer) via grid search on validation set monthly.
Breakout model retrained weekly.

Failure Modes
Failure

Detection

Response

Regime belief stuck

Entropy near 0 for long period

Inject random noise or reset model.

Frequent false breakouts

False breakout rate > 0.3

Increase threshold, retrain model.

Data gap

Gap detected

Discard updates during gap; reinitialize from current price
structure.

Latency

Computation time >1 ms

Simplify features, offload to GPU.

Recovery Procedures
Belief stuck: soft reset, widen prior, disable transition matrix for 5 bars.
Model drift: emergency batch retrain over past 3 months.
After market halt: use first 10 bars to re‑establish swing points.

Internal Memory
Ring buffer of last 200 bars, swing points, belief states.
Sufficient statistics for online Gaussians.
Transition count matrix (smoothed).
Performance log of false breakout events.

Explainability Layer

Log top 3 features contributing to regime change and likelihood ratios.
Dashboard: price chart overlaid with colored regime shading.

Health Metrics
Regime classification accuracy vs higher‑TF consensus: > 80%.
False breakout rate (30‑day): < 25%.
Belief calibration error (Brier score) < 0.05.
Avg update latency per instrument: < 0.5 ms.

Interfaces
AITOS-ALPHA
AITOS-EXEC-14
AITOS-RISK-10
AITOS-SESSION-10
AITOS-REGIME

Production-Grade Pseudocode
class MarketStructureEngine:
def __init__(self, instrument, timeframe):
self.instr = instrument
self.tf = timeframe
self.belief = np.ones(6)/6
self.transition = np.eye(6) * 0.9 + 0.1/6
self.likelihood = GaussianLikelihood(num_regimes=6, feature_dim=6)
self.swing_detector = SwingDetector(window=3)
self.breakout_model = LogisticBreakoutModel()
self.online_stats = OnlineSufficientStats(decay=0.05)
def on_bar_close(self, bar):
swings = self.swing_detector.update(bar)
x = self.extract_features(swings, bar)
pred_belief = self.transition.T @ self.belief
log_likes = self.likelihood.log_prob(x)
log_posterior = np.log(pred_belief + 1e-10) + log_likes
log_posterior -= np.max(log_posterior)
posterior = np.exp(log_posterior)
self.belief = posterior / posterior.sum()
dominant_regime = np.argmax(self.belief)
self.online_stats.update(dominant_regime, x)
if hasattr(self, 'prev_regime'):
self.transition[self.prev_regime, dominant_regime] = 0.9 * self.transition[self.prev_regime, dominant_regime]
0.1
self.prev_regime = dominant_regime
brk_prob = self.breakout_model.predict(bar, self.key_levels)
if brk_prob > 0.5:
self.belief[REGIME.BREAKOUT_UP if bar.close > self.resistance else REGIME.BREAKOUT_DOWN] = brk_prob
self.belief /= self.belief.sum()
self.publish_belief()
def extract_features(self, swings, bar):
# returns vector of 6 features
pass

Knowledge Graph
MarketStructureEngine
├── BeliefState (Bayesian posterior)
│
├── regime probabilities
│
└── entropy
├── ObservationModel
│
├── Gaussian likelihoods per regime
│
└── online sufficient statistics

├── TransitionMatrix (Markov)
├── SwingDetector (deterministic)
├── BreakoutDetector (logistic)
├── KeyLevels (support/resistance)
├── PerformanceMonitor
└── Interfaces (Alpha, Execution, Risk, Session)

Machine‑Readable JSON Schema
{
"module_id": "AITOS-MSTRUCT-11",
"version": "2.0",
"state": {
"instrument_states": {
"type": "dict",
"value": {
"belief": "float[6]",
"entropy": "float",
"key_levels": {"support": "float", "resistance": "float"},
"swings": "list[swing]",
"transition": "float[6][6]",
"perf": {"false_breakout_rate": "float"}
}
}
},
"inputs": ["ohlcv", "atr", "session_score"],
"outputs": ["belief_state", "key_levels", "strategy_bias"],
"decision_rules": "threshold on belief + entropy",
"interfaces": ["AITOS-ALPHA", "AITOS-EXEC-14", "AITOS-RISK-10", "AITOS-SESSION-10"]
}

Changelog
v2.0 (from v1.0): Converted from rule‑based to full Bayesian framework with Markov transitions, online likelihood updates, deflated Sharpe
validation, and self‑calibration.
