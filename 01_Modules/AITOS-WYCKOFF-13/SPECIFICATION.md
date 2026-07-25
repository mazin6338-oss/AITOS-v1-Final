---
Architecture Version: 2.0
Release: Canonical v2
Status: Approved
Last Updated: 2026-07-25
---

# Module 07: Wyckoff Method Engine (AITOS‑WYCKOFF‑13 v1.1)

Metadata
Module ID: AITOS-WYCKOFF-13
Chapter: 13 – Wyckoff Method
Version: 1.1
Last Updated: 2026-07-20
Dependencies: AITOS-MSTRUCT-11, AITOS-CTA-12, AITOS-MICRO-08, AITOS-SESSION-10, AITOS-RISK-10
Status: Production

Purpose
To detect and track Wyckoff accumulation and distribution schematics using a hierarchical probabilistic framework. This module infers the market’s
current phase (Phase A–E) within a Wyckoff cycle, estimates the likelihood of future markup or markdown, and provides early entry/exit signals based
on the interaction of price, volume, and time. It models the battle between composite operators (smart money) and the crowd, enabling the AI to
anticipate institutional‑grade turning points.

Scope
Detection of Accumulation and Distribution patterns across all timeframes.
Phase identification using a Hidden Semi‑Markov Model (HSMM).
Key events: SC, AR, ST, Spring/Upthrust, SOS, SOW, LPS, etc.
Volume and price interaction analysis, including effort vs. result and absorption.
Multi‑timeframe Bayesian hierarchy.
Confidence decay for inactive schematics.
Composite Operator Score (COS) and Institutional Participation Index (IPI).
Event reliability database with online Bayesian updating.
Trading range quality scoring.
Institutional liquidity sweep detection.
Adaptive cause projection.
Context integration for future Smart Money Concepts.

Internal State Representation
Per‑Instrument Wyckoff Tracker (Extended)
{
"instrument_id": "ES",
"timeframe": "H4",
"schematic_type": "ACCUMULATION",
"current_phase": "C",
"phase_probabilities": { "A": 0.05, "B": 0.10, "C": 0.60, "D": 0.20, "E": 0.05 },
"phase_duration_estimates": {
"A": {"mean": 5.2, "std": 2.1},
"B": {"mean": 15.3, "std": 4.5},
"C": {"mean": 3.1, "std": 1.0},
"D": {"mean": 8.2, "std": 2.3},
"E": {"mean": 12.0, "std": 3.8}
},
"key_levels": {
"resistance": 4200.0, "support": 4100.0, "ice": 4150.0,
"spring_low": 4080.0, "upthrust_high": 4220.0
},
"events": [
{"event": "SC", "time": "2026-07-18", "price": 4095.0, "volume_ratio": 2.3},
{"event": "AR", "time": "2026-07-19", "price": 4160.0, "volume_ratio": 1.1}
],

"cause_estimate": 120.0,
"confidence": 0.75,
"confidence_decay_factor": 0.02,
"last_confirming_event_time": "2026-07-19T14:00",
"composite_operator_score": 0.68,
"institutional_participation_index": 0.72,
"trading_range_quality_score": 0.82,
"transition_probabilities": {
"A_to_B": 0.81, "B_to_C": 0.74, "C_to_D": 0.88, "D_to_E": 0.91
},
"event_reliability": {
"Spring": {"success_rate": 0.73, "sample_size": 420},
"Upthrust": {"success_rate": 0.68, "sample_size": 310},
"SOS": {"success_rate": 0.81, "sample_size": 315}
}
}

Knowledge Representation
Wyckoff Schematic Models: canonical accumulation/distribution phases with duration distributions.
Hidden Semi‑Markov Model: hidden states with explicit duration modeling (Gamma/Weibull). Observations include price‑volume features and
microstructure data.
Multi‑Timeframe Hierarchy: higher TF beliefs serve as priors for lower TFs via weighted combination.
Event Reliability Database: Beta‑Binomial posteriors for each event type.
Confidence Decay Model: exponential decay when no confirming events.
Adaptive Cause Projection: dynamic multiplier based on asset class, ATR, volatility, COS, etc.

Belief State
Phase probability vectors per timeframe.
Schematic confidence (decayable).
COS, IPI, range quality.
Event reliability priors.

State Variables
As detailed in the internal state JSON.

Inputs
OHLCV bars per timeframe from MICRO-08.
Swing points from MSTRUCT-11.
Microstructure data (OFI, iceberg flags, stop‑hunt signals) from MICRO-EXT (future).
Volume profile from VOL-16 (future).
Session liquidity from SESSION-10.

Outputs
Phase probabilities, COS, IPI.
Signals (entry, target, stop) when Phase D confidence > threshold.
Key levels and cause projections.
Context variables for Context Engine.

Core Reasoning Engine
1. Trading range detection with quality scoring: range must have quality > threshold.
2. Wyckoff event detection: classifiers for Spring, Upthrust, SOS, etc., boosted by liquidity sweeps and event reliability priors.

3. HSMM forward update: uses Gaussian mixture emissions, directional transition constraints, duration distributions. Multi‑timeframe prior injected
as pseudo‑observation.
4. Confidence decay: C_t = C_{t−1}·e^(−λΔt), reset on confirming events.
5. COS computation: logistic ensemble of effort/result, absorption, OFI, iceberg flags, delta imbalance.
6. IPI: weighted combination of COS, liquidity sweeps, session liquidity.
7. Adaptive cause projection: learned model k = f(asset_class, …) predicts expansion factor.

Mathematical Models
HSMM forward recursion (directional): α_t(j) = Σ_d α_{t−d}(i)·a_{i,j}·p_j(d)·Π_s b_j(x_s)
Confidence decay: C_t = C_{t−1}·e^(−λΔt) + event_boost
Event reliability: Beta posterior update.
Range quality: Q = Σ w_i·q_i
Cause projection: k = f(features) (gradient boosting or neural net).

Decision Rules
Signals only if schematic confidence >0.6, range quality >0.6, COS >0.5.
Phase transition probability (C→D) used to scale position size.
If multi‑TF hierarchy shows disagreement (e.g., Daily Accumulation vs H1 Distribution), reduce positions to 25% until alignment.
If confidence decays below 0.3, exit positions and discard schematic.

Constraint Engine
Min range quality threshold for Wyckoff analysis.
Confidence decay may auto‑remove inactive schematics.
Multi‑TF disagreement constraint.

Validation Engine
Backtest HSMM vs HMM for phase classification accuracy.
Validate confidence decay fit to typical inactivity periods.
Adaptive cause projection: regression residuals uncorrelated.
Monitor COS/IPI discrimination: AUC >0.65 for successful signals.

Monitoring Rules
Track confidence decay curves; alert if many decay quickly.
Monitor COS/IPI distribution across instruments; alert on widespread spikes.
HSMM duration estimates updated daily; monitor for shifts.
Event reliability database: flag if success rate drops below 0.5.

Learning & Adaptation
Online HSMM parameter update via stochastic EM on sliding window.
Adaptive cause model retrained monthly.
COS weights adjusted via contextual bandit.
Event reliability Beta parameters updated after every completed trade.

Failure Modes (Extended)
Failure

Response

HSMM computational lag

Fallback to HMM if latency >2 ms.

COS/IPI signals collapse (missing micro data)

Use classical Wyckoff rules without micro enhancement.

Multi‑TF hierarchy over‑regularizes

Reduce prior weight w temporarily when lower TF evidence accumulates.

Recovery Procedures
If HSMM becomes unstable, revert to HMM with last known good parameters.
If COS model fails, degrade gracefully with default COS of 0.5.
Event reliability DB corruption: reload from backup; assume flat priors.

Internal Memory
Circular buffer of HSMM alpha values.
Duration distribution parameters per phase per instrument.
Event reliability database (persisted).
Recent COS and IPI values for trend analysis.

Explainability Layer
Visualization includes confidence decay curve.
For each signal, include COS and IPI values.
Multi‑timeframe dashboard with phase belief alignment indicator.

Health Metrics
Metric

KPI

HSMM update latency (with D_max=20)

< 1 ms per bar per instrument

Confidence decay fit R²

≥ 0.8

COS/IPI AUC for successful signals

≥ 0.65

Adaptive cause projection MAPE

< 15%

Interfaces
AITOS-MSTRUCT-11
AITOS-CTA-12
AITOS-MICRO-EXT (future)
AITOS-ALPHA
AITOS-EXEC-14
AITOS-RISK-10
AITOS-CONTEXT (future)
AITOS-SMC (future)

Production-Grade Pseudocode
class WyckoffEngineV1_1:
def __init__(self, instrument, timeframes=['D','H4','H1','M15']):
self.instr = instrument
self.timeframes = timeframes
self.hsmms = {tf: HSMM(num_states=6) for tf in timeframes}
self.event_clfs = {...}
self.event_reliability = EventReliabilityDB()
self.cause_model = AdaptiveCauseModel()
self.cos_model = CompositeOperatorScoreModel()
self.range_quality = RangeQualityScorer()
self.beliefs = {tf: np.ones(6)/6 for tf in timeframes}
self.confidences = {tf: 0.5 for tf in timeframes}

self.last_events = {tf: None for tf in timeframes}
def on_bar(self, tf, bar, swings, regime, micro_data=None):
range_info = self.update_trading_range(tf, bar, swings)
quality = self.range_quality.score(range_info, swings, bar)
events = self.detect_events(bar, swings, micro_data)
if events.empty():
self.confidences[tf] *= exp(-self.decay_lambda[tf])
else:
self.confidences[tf] = min(1.0, self.confidences[tf] + 0.1)
self.last_events[tf] = bar.index
features = self.extract_features(bar, range_info, micro_data)
prior = self.get_higher_tf_prior(tf)
self.beliefs[tf] = self.hsmms[tf].forward_step(self.beliefs[tf], features, prior)
cos = self.cos_model.compute(features, micro_data)
ipi = self.compute_ipi(cos, events, micro_data)
if (self.beliefs[tf][PHASE.D] > 0.7 and self.confidences[tf] > 0.6 and quality > 0.6):
direction = 'LONG' if self.schematic_type[tf] == 'ACCUMULATION' else 'SHORT'
target = self.cause_model.predict(range_info.height, features)
stop = self.determine_stop(direction)
self.emit_signal(direction, target, stop, self.beliefs[tf][PHASE.D],
cos=cos, ipi=ipi, transition_prob=self.transition_prob('C','D'))

Knowledge Graph
WyckoffEngine_v1.1
├── RangeQualityScorer
├── EventDetectors (extended with liquidity sweeps)
├── HSMM (with duration modeling)
├── MultiTimeframeBayesianHierarchy
├── ConfidenceDecayModel
├── CompositeOperatorScoreModel
├── InstitutionalParticipationIndex
├── EventReliabilityDB
├── AdaptiveCauseProjection
├── PhaseTransitionProbabilities
└── ContextIntegrationLayer

Machine‑Readable JSON Schema (Extended)
{
"module_id": "AITOS-WYCKOFF-13",
"version": "1.1",
"state": {
"timeframes": {
"type": "dict",
"value": {
"beliefs": "float[6]",
"confidence": "float",
"confidence_decay_lambda": "float",
"last_event_index": "int",
"range_quality": "float",
"composite_operator_score": "float",
"institutional_participation_index": "float",
"phase_duration_estimates": "dict",
"transition_probabilities": "dict"
}
},
"event_reliability": "dict"
},
"inputs": ["OHLCV", "swings", "regime", "micro_data", "session_score"],
"outputs": ["signals", "phase_beliefs", "context_vars", "cos", "ipi"],
"decision_rules": "thresholds + multi-tf alignment",
"interfaces": ["AITOS-MSTRUCT-11", "AITOS-CTA-12", "AITOS-MICRO-EXT", "AITOS-ALPHA", "AITOS-EXEC-14", "AITOS-RISK-10",
"AITOS-SMC", "AITOS-CONTEXT"]
}

Changelog
v1.0: Initial HSMM with classical Wyckoff phases, Bayesian phase tracking.
v1.1: Added confidence decay, COS, IPI, multi‑timeframe hierarchy, HSMM duration modeling, event reliability database, trading range quality,

institutional liquidity sweep detection, adaptive cause projection, and context integration layer.

End of reconstructed AITOS v1 specification.
