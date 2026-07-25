---
Architecture Version: 2.0
Release: Canonical v2
Status: Approved
Last Updated: 2026-07-25
---

# Module 06: Classical Technical Analysis Engine (AITOS‑CTA‑12)

Metadata
Module ID: AITOS-CTA-12
Chapter: 12 – Classical Technical Analysis
Version: 1.0
Last Updated: 2026-07-20
Dependencies: AITOS-MICRO-08, AITOS-MSTRUCT-11, AITOS-SESSION-10, AITOS-RISK-10
Status: Production

Purpose
To detect, classify, and assign probabilistic confidence to classical technical analysis patterns—candlestick formations, chart patterns, trendline breaks,
and static support/resistance—augmenting the AI’s pattern recognition capabilities with well‑established visual structures that human traders use. This
module converts price and volume data into actionable pattern signals with quantified reliability.

Scope
Candlestick patterns: Hammer, Shooting Star, Engulfing, Doji, Morning/Evening Star, Harami, etc.
Chart patterns: Head and Shoulders, Double/Triple Top/Bottom, Triangles, Wedges, Flags, Pennants, Rectangle, Cup & Handle.
Support & Resistance (static): Pivot points, historical swing levels, round numbers, volume‑at‑price nodes.
Trendlines & Channels: Linear regression on swing points, breakouts.
Dow Theory principles: Trend confirmation via higher‑high/higher‑low (overlap with MSTRUCT but handled as classical rule set), volume
confirmation.
Volume confirmation: Volume spike, trend of volume.

Internal State Representation
{
"instrument_id": "AAPL",
"timeframe": "D1",
"active_patterns": [
{
"pattern_id": "HS_TOP_001",
"type": "HEAD_AND_SHOULDERS_TOP",
"status": "FORMING",
"confidence": 0.72,
"entry_level": 145.0,
"target_level": 135.0,
"stop_level": 150.0,
"formation_start_time": "2026-06-10",
"last_update": "2026-07-20",
"volume_confirmation": 0.8,
"quality_score": 0.65
}
],
"candlestick_signals": [
{"time": "2026-07-20T09:30", "type": "BULLISH_ENGULFING", "confidence": 0.85, "context": "AT_SUPPORT"}
],
"support_resistance_levels": {
"static_support": [142.0, 140.5],
"static_resistance": [148.0, 150.2],
"pivot_points": {"R1": 149.0, "S1": 143.0}
},
"trendlines": [
{"type": "uptrend", "start": "2026-06-01", "current_value": 144.8}
]
}

Knowledge Representation
Pattern ontology: Boolean functions of OHLC for candlesticks; geometric templates on swing points for chart patterns.
Bayesian confidence model: Prior based on historical hit rate; posterior updated with features (volume, trend alignment, symmetry). Logistic
regression or Beta posterior.
Pattern Lifecycle State Machine: IDLE → FORMING → CONFIRMED/INVALIDATED.

Belief State
For each pattern, probability of validity updated as new bars arrive.

State Variables
As in the internal state JSON.

Inputs
OHLCV bars from AITOS-MICRO-08.
Swing point list from AITOS-MSTRUCT-11.
Market regime state from MSTRUCT.
Session liquidity from AITOS-SESSION-10.

Outputs
PatternSignal stream: type, direction, confidence, target, stop.
Support/Resistance levels updated on each bar.
Trendline break alerts.
Quality scores for Alpha module.

Core Reasoning Engine
Candlestick pattern recognition via rule‑based classifier.
Chart pattern detection using dynamic programming on swing points (template matching).
Support/resistance from pivot points, historical clusters (KDE), round numbers.
Trendline detection via robust linear regression on swing lows/highs; break when close beyond buffer.

Mathematical Models
Bayesian pattern confidence: log‑odds model log(P/(1−P)) = β₀ + β·f
Pattern quality score: Q = w₁·Conf + w₂·VolConf + w₃·TrendAlign + w₄·Completeness

Decision Rules
Chart pattern CONFIRMED + confidence >0.7 → initiate trade.
Candlestick signals are confirmations only, aligned with regime.
S/R levels fed to Execution for limit orders.
Trendline breaks require volume > 1.2× avg and subsequent bar confirmation.

Constraint Engine
Timeframe weighting (higher TFs more weight).
Low‑liquidity sessions: down‑weight confidence.

Adjust stops/targets away from round‑number clusters.
Max 5 active patterns per instrument.

Validation Engine
Historical pattern database with outcomes; backtest hit rate, profit factor, MAE.
Bayesian model calibration: reliability curve.
Static S/R level bounce frequency.
Walk‑forward validation to avoid overfitting.

Monitoring Rules
False breakout rate from trendlines/chart patterns; if >40%, increase thresholds.
Detection latency <1 ms per bar.
Alert on many patterns simultaneously.

Learning & Adaptation
Online learning of pattern reliability: Beta posterior updated with each trade outcome.
Parameter optimization quarterly via Bayesian optimization.
Personalized pattern weighting: if pattern underperforms on an instrument, reduce weight.

Failure Modes
Failure

Response

False pattern detection due to noise

Increase smoothing; require more extreme values.

Overfitting

Regularization; raise min confidence threshold.

Misalignment of trendline due to outlier

Use robust regression (Huber); discard outliers.

Excessive computation

Optimize with vectorized ops; use GPU.

Recovery Procedures
Invalidate pattern: cancel contingent orders; log for learning.
Poor performance period: reduce capital allocation by 50% temporarily.
Major regime change: reinitialize detection parameters.

Internal Memory
Pattern history (last 500 instances with features/outcomes).
Swing point cache (reused from MSTRUCT).
Pivot point cache (daily).

Explainability Layer
Textual justification: “Bullish Engulfing at support S1 (143.0) during uptrend, volume confirmation 1.8× avg, confidence 85%.”
Visualization of patterns on chart.

Health Metrics
Overall pattern hit rate (profit factor >1) > 0.55.
False breakout rate < 0.35.
Confidence calibration error (Brier score) < 0.05.
Detection latency < 0.5 ms per bar.

Interfaces
AITOS-MSTRUCT-11
AITOS-ALPHA
AITOS-EXEC-14
AITOS-RISK-10
AITOS-SESSION-10
AITOS-VOL-16 (future)

Production-Grade Pseudocode
class ClassicalTechnicalAnalysis:
def __init__(self, instrument):
self.instr = instrument
self.patterns = []
self.sr_levels = SREngine()
self.trendline_mgr = TrendlineManager()
self.candle_recognizer = CandlestickRecognizer()
self.bayesian_model = BayesianPatternModel()
def on_bar(self, bar, swings, regime):
candles = self.candle_recognizer.detect(bar, self.prev_bars)
for c in candles:
c.confidence = self.bayesian_model.get_confidence(c.type, c.features, regime)
self.emit_signal(c)
self.update_patterns(swings, bar.volume)
self.sr_levels.update(bar, swings)
self.trendline_mgr.update(swings, bar.close, bar.volume)
self.update_beliefs()

Knowledge Graph
ClassicalTechnicalAnalysisEngine
├── CandlestickPatterns
├── ChartPatterns
├── SupportResistance
├── Trendlines & Channels
├── BayesianConfidenceModel
└── Interfaces (Alpha, Execution, Risk)

Machine‑Readable JSON Schema
{
"module_id": "AITOS-CTA-12",
"version": "1.0",
"state": {
"active_patterns": "list[Pattern]",
"sr_levels": {"support": "list[float]", "resistance": "list[float]"},
"trendlines": "list[Trendline]",
"candlestick_signals": "list[Signal]"
},
"inputs": ["OHLCV_bars", "swing_points", "regime_state", "session_liquidity"],
"outputs": ["pattern_signals", "support_resistance_levels", "trendline_breaks"],
"decision_rules": "use quality and confidence to size positions",
"interfaces": ["AITOS-MSTRUCT-11", "AITOS-ALPHA", "AITOS-EXEC-14", "AITOS-RISK-10", "AITOS-SESSION-10"]
}

Changelog
v1.0: Initial implementation of classical TA patterns with Bayesian confidence, lifecycle management, and integration with MSTRUCT.
