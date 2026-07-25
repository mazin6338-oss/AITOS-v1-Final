---
Architecture Version: 2.0
Release: Canonical v2
Status: Approved
Last Updated: 2026-07-25
---

# Module 02: Market Microstructure Engine (AITOS‑MICRO‑08)

Metadata
Module ID: AITOS-MICRO-08
Chapter: 8 – Market Microstructure
Version: 1.0
Last Updated: 2026-07-20
Dependencies: AITOS-MD-01..07
Status: Production

Purpose
To equip the AI with a real‑time, quantitative model of how orders interact to form prices, spreads, and liquidity. This module enables the system to
reason about execution cost, information leakage, order flow toxicity, and optimal order placement.

Scope
Internal representation of limit order books (LOB) for all traded instruments.
Real‑time estimation of micro‑level variables: spread, depth, order flow imbalance (OFI), queue position, trade direction, microprice.
Detection and exploitation of short‑term microstructure patterns for execution optimization.
Classification of order flow toxicity and adverse selection risk.
Inference of hidden liquidity (iceberg orders, dark pool activity).
Interface with execution algorithms to select order type, venue, and aggression.

Internal State Representation
LOB Snapshot
For each instrument, a tick‑by‑tick representation:
LOB {
symbol,
timestamp,
bids: sorted list of {price, displayed_size, hidden_size_estimate},
asks: sorted list of {price, displayed_size, hidden_size_estimate},
last_trade: {price, size, aggressor_side},
imbalance: float ∈ [-1, 1],
microprice: float,
spread: float,
depth_top: float,
depth_full: float[],
toxicity: float,
queue_position: per order if own orders outstanding
}

Derived Quantities
Order Flow Imbalance (OFI): net aggressive volume at the best bid/ask over a short window.
Microprice: weighted average of best bid and ask, with weights inversely proportional to displayed size or dynamically adjusted by queue
dynamics.
Queue Position: for each of the AI’s own limit orders, estimate of priority based on time‑stamp or pro‑rata rules.
Toxic Flow Probability: estimated probability that an incoming aggressive order is informed.

Knowledge Representation
Observation Model: Bayesian inference of hidden iceberg orders from sequential fills and refill patterns.

Adverse selection model: Glosten‑Milgrom framework to estimate PIN.
Price impact model: Kyle’s lambda for permanent impact, order book depth for temporary impact.

Belief State
For each instrument, the AI maintains:
liquidity_regime: {NORMAL, LOW, STRESSED}
hidden_liquidity_density: estimated proportion of total liquidity that is hidden.
adverse_selection_level: expected permanent price impact per unit of aggressive volume.
resiliency_halflife: time in seconds for spread to return to baseline after a liquidity‑taking trade.
queue_replenishment_rate: speed at which canceled/executed limit orders are replaced.
sor_effectiveness: belief about the performance of different venues.
All beliefs are updated via exponential smoothing of observed outcomes.

State Variables
Variable

Type

Update Frequency

best_bid, best_ask

float

Real‑time (every tick)

spread

float

Real‑time

OFI

float

Every second

microprice

float

Real‑time

queue_position

int or fraction

On each order placement/change

toxicity_score

float ∈ [0,1]

Every minute

hidden_volume_estimate

float

Updated on each trade that consumes hidden liquidity

resiliency_halflife

float

Updated after each large trade

liquidity_regime

categorical

Every minute

Inputs
Market data feeds (tick data) from exchange gateways.
Order book snapshots (full depth whenever possible).
Own order status updates.

Outputs
Real‑time microstructure metrics (spread, OFI, microprice, toxicity) pushed to other modules.
Queue position and expected fill probability for own orders.
Hidden liquidity estimates for SOR.
Recommended order type, aggression level, and venue ranking per child order.

Core Reasoning Engine
Order book update: maintain best bid/ask, depth, spread, microprice.
Hidden liquidity estimation: detect iceberg refills and adjust depth estimates.
Toxicity scoring: compute PIN via Glosten‑Milgrom; update rolling estimate.
Queue dynamics: track position and replishment rate.
Liquidity regime detection: based on spread widening, depth thinning, resiliency changes.

Mathematical Models
Kyle’s lambda: λ = 2σ_v / σ_u from regression on order flow.
PIN estimation: PIN = αμ / (αμ + 2ε)

Microprice: P_micro = (P_bid·Q_ask + P_ask·Q_bid) / (Q_bid + Q_ask) (or dynamic weights).
Effective spread: 2|P_trade − M| etc.

Decision Rules
Order type selection based on toxicity, urgency, and liquidity regime.
Venue selection (SOR) to minimize expected execution cost.
Queue management: cancel and replace if far behind or unlikely to fill.

Constraint Engine
Regulatory: no spoofing, layering, quote stuffing.
Venue limits: max order size, min tick size, allowed order types.
Risk limits: position size and capital allocation.
Latency budget: SOR decisions within 50 µs.

Validation Engine
Backtest execution performance against historical order book data.
Monitor realized spread vs effective spread; if negative, recalibrate toxicity.
Retrain PIN estimation model monthly.

Monitoring Rules
Real‑time tracking of queue position and fill rate.
Compare predicted vs actual execution costs.
Sudden spike in OFI without price change may indicate manipulation.
Track resiliency halflife; if doubles, flag regime change.

Learning & Adaptation
Reinforcement learning for order placement policy (reward = -slippage).
Supervised model to predict iceberg probability from trade sequence.
Microprice weight update via online regression.

Failure Modes
Failure

Detection

Response

Data feed latency/gaps

Missing ticks

Use last known good state; cancel all active orders if gap
> 100ms.

Spoofing attack

Rapid cancellations at best bid/ask

Ignore those levels in microprice; increase toxicity score.

Hidden liquidity mis‑estimation

Realized impact higher than predicted

Fall back to displayed depth only; reduce aggression.

Flash crash

Spread >10x normal, depth near zero

Suspend all execution; only market‑make with wide
quotes if capital allows.

Queue position priority error

Lower than expected fill rate for early orders

Re‑validate exchange matching rules.

Recovery Procedures
After flash crash: gradually re‑enter with passive orders, monitor resiliency; resume normal trading only after spread/depth return to 2x normal for
5 minutes.
After data gap: re‑sync order book from exchange snapshot, cross‑check with recent trades, resume after 1‑second stability check.
After spoofing detection: reduce displayed size, use dark pools for 5 minutes.

Internal Memory
Short‑term: tick‑by‑tick LOB data for past 1 day.
Medium‑term: aggregated microstructure stats per 30‑minute bucket, retained 1 year.
Long‑term: parameters of impact models, PIN estimates, SOR performance per instrument, updated monthly.

Explainability Layer
For each execution child order, log rationale: chosen venue, order type, top 3 influencing factors.
Post‑trade attribution: spread cost, temporary impact, permanent impact, delay cost.
Dashboard: microprice, toxicity heatmap, hidden liquidity density.

Health Metrics
Execution cost relative to arrival price (bps) – target < 3 bps for liquid stocks.
Fill rate of passive orders – target > 80%.
Microprice prediction R² – target > 0.9 on 1‑second horizon.
Toxicity model accuracy – ROC‑AUC > 0.75.
SOR latency – must be < 50 µs p99.

Interfaces
AITOS-EXEC-14 (Execution Algorithms)
AITOS-RISK-10 (Risk Management)
AITOS-EFF-07 (Market Efficiency)
AITOS-ALPHA (Alpha Generation)
AITOS-DATA (Market Data)
AITOS-REGIME

Production-Grade Pseudocode
def on_order_book_update(instrument, bids, asks):
lob = get_lob(instrument)
lob.bids = bids
lob.asks = asks
lob.spread = asks[0].price - bids[0].price
lob.depth_top = bids[0].size + asks[0].size
lob.microprice = compute_microprice(bids, asks)
lob.imbalance = compute_ofi(lob)
update_toxicity(lob)
update_hidden_liquidity_estimate(lob)
check_regime_change(lob)
def decide_order(instrument, size, urgency):
lob = get_lob(instrument)
if lob.liquidity_regime == STRESSED:
return Order(type='IOC', venues=['dark_pool_A', 'lit_venue'], aggression=0.9)
if lob.toxicity > 0.7 and urgency > 0.5:
return Order(type='marketable_limit', price=current_ask, size=min(size, lob.depth_ask))
if urgency < 0.3:
display = min(size * 0.1, max_display)
return Order(type='iceberg', side='buy', price=best_bid, size=size, display=display)
return sor_route(lob, size, urgency)

Knowledge Graph
MarketMicrostructure
├── LimitOrderBook
│
├── BestBidAsk

│
├── DepthLevels
│
├── Microprice
│
└── HiddenLiquidity
├── OrderFlow
│
├── OFI
│
├── TradeDirection
│
└── ToxicFlow
├── PriceImpact
│
├── TemporaryImpact
│
└── PermanentImpact (Kyle's Lambda)
├── LiquidityRegime
│
├── Normal
│
├── Low
│
└── Stressed
├── QueueDynamics
│
├── TimePriority
│
├── ProRata
│
└── ReplenishmentRate
└── ExecutionConnectors
├── OrderTypeSelection
├── VenueSelection (SOR)
└── QueueManagement

Machine‑Readable JSON Schema
{
"module": "AITOS-MICRO-08",
"version": "1.0",
"state": {
"lob_snapshots": { "type": "dict", "key": "symbol", "value": "LOB" },
"liquidity_regime": "enum",
"toxicity_scores": "dict[float]",
"hidden_liquidity_density": "dict[float]"
},
"decision_rules": {
"order_type_selection": "function(instrument, size, urgency) -> Order",
"venue_selection": "function(instrument, order) -> list[Venue]"
},
"validation": {
"slippage_benchmark": "arrival_price",
"retraining_frequency": "monthly"
},
"interfaces": ["AITOS-EXEC-14", "AITOS-RISK-10", "AITOS-EFF-07", "AITOS-DATA"]
}

Changelog
v1.0: Initial production specification. Implemented full LOB tracking, toxicity estimation, hidden liquidity inference, SOR decision, and online
learning.
