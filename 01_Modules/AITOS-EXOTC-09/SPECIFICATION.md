---
Architecture Version: 2.0
Release: Canonical v2
Status: Approved
Last Updated: 2026-07-25
---

# Module 03: Exchange & OTC Venue Management (AITOS‑EXOTC‑09)

Metadata
Module ID: AITOS-EXOTC-09
Chapter: 9 – Exchange vs OTC Markets
Version: 1.0
Last Updated: 2026-07-20
Dependencies: AITOS-MICRO-08, AITOS-EFF-07, AITOS-RISK-10
Status: Production

Purpose
Enables the AI to intelligently route orders and manage liquidity across heterogeneous execution venues: regulated exchanges, multilateral trading
facilities (MTFs), dark pools, and bilateral OTC relationships. It models venue‑specific costs, constraints, and risks to achieve best execution while
respecting regulatory and counterparty requirements.

Scope
Maintain a live registry of all accessible venues with static and dynamic attributes.
Construct a consolidated view of liquidity by merging order books from lit exchanges, dark pool indications, and OTC quotes.
Decide per child order the optimal execution venue(s) based on cost, fill probability, toxicity, and counterparty credit exposure.
Manage OTC negotiation workflows (RFQ, streaming prices) where applicable.
Monitor and update beliefs about venue performance (fill rates, slippage, latency, hidden liquidity).
Integrate with settlement and clearing to track OTC settlement risk.

Internal State Representation
Venue Registry (Exchange)
{
"venue_id": "NYSE_ARCA",
"type": "EXCHANGE",
"instruments": ["AAPL", ...],
"trading_hours": {...},
"fee_structure": {"maker_bps": -0.2, "taker_bps": 0.3},
"latency_profile": {"p50_ms": 0.05, "p99_ms": 0.2},
"clearing_house": "NSCC",
"pre_trade_transparency": "FULL",
"post_trade_transparency": "REAL_TIME",
"supported_order_types": ["LIMIT", "MARKET", "IOC", ...],
"dynamic_state": {
"current_status": "OPEN",
"last_outage": null,
"current_spread": 0.01,
"current_depth": 5000,
"toxicity_score": 0.3
}
}

Venue Registry (OTC Dealer)
{
"venue_id": "OTC_BANK_A",
"type": "OTC_DEALER",
"instruments": ["EUR/USD", "AAPL_OIS", ...],
"credit_limit": 50000000,
"current_exposure": 12000000,
"settlement_protocol": "CLS" | "BILATERAL",

"streaming_enabled": true,
"rfq_timeout_sec": 30,
"execution_quality": {"fill_rate": 0.98, "avg_slippage_bps": 0.5}
}

Aggregated LOB: merged sorted list from all venues with venue_ids and constraints.

Knowledge Representation
Venue Preference Score S_{i,v} as a function of expected total cost, fill probability, adverse selection.
CreditExposure tracking per counterparty.
OTCQuoteStream stored as separate order book slices.

Inputs
Real‑time market data from all venues.
Execution quality statistics from AITOS-MICRO-08.
Counterparty credit limits and current exposure from AITOS-RISK-10.
Regulatory constraints.
Order requests from AITOS-EXEC-14.

Outputs
Venue selection decision for each child order (list of venues, allocation fractions).
Aggregated liquidity view.
Alerts when a venue becomes unavailable, toxic, or credit‑constrained.
Real‑time estimated total execution cost.

Core Reasoning Engine
Multi‑objective optimization: For order size Q, side, urgency u, instrument i:
For each eligible venue v, compute expected cost C_v, fill probability P_fill,v, and credit cost.
Objective: minimize Σ w_v (C_v + λ(1−P_fill,v)) subject to credit limits and other constraints.
Solve using linear programming or greedy allocation for low latency.

Decision Rules
Small, non‑urgent orders in liquid instruments → low‑cost exchange with maker rebates, passive limit orders.
Large block orders → dark pools first, then algorithmic slicing.
FX spot → best streaming dealer with sufficient credit.
Bonds/illiquid → RFQ to panel; select best quote after risk check.
If venue toxicity > 0.8 → exclude temporarily.
After hours: only venues with extended hours support.

Constraint Engine
Regulatory: MiFID II best execution, Reg NMS; log venue selection rationale.
Credit: pre‑trade check; if trade would breach limit, exclude venue.
Settlement risk: only allowed settlement methods (CLS, DVP).
Venue membership and max order size enforced.

Validation Engine

Backtest venue selection against historical order books.
Compare actual execution costs with pre‑trade estimates; recalibrate if bias.
Monitor OTC RFQ performance (acceptance rate, price improvement).
Weekly audit of credit checks.

Monitoring Rules
Real‑time venue latency, fill rate, rejection rate.
If 5‑min rejection rate >10%, flag as impaired.
OTC dealer: if streaming quotes >100ms stale vs market, suppress use.
Alert on venue outage or status change.

Learning & Adaptation
Fill probability models for dark pools and RFQ: Bayesian posterior update.
Cost model calibration: reinforcement learning (contextual bandits) to adjust venue weights online.
Aggregated LOB prediction for depth beyond top of book.
Venue performance decay tracking.

Failure Modes
Failure

Detection

Response

Primary exchange outage

Market data feed stops, order rejects

Route to alternative venues; halt if no liquidity.

OTC dealer credit breach

Real‑time exposure exceeds limit

Suspend orders to that dealer; rebalance.

RFQ no‑response

Timer expires with no quotes

Increase timeout or switch to streaming dealers.

Aggregated LOB inconsistencies due to latency

Timestamp comparison across venues

Temporarily ignore slow venue.

Regulatory violation detected

Post‑trade analysis

Halt automated routing, human override.

Recovery Procedures
After exchange outage: gradually increase allocation over 10 minutes after status returns to normal.
After credit limit breach: apply for temporary increase or reduce positions; resume OTC routing after re‑validation.
After RFQ timeouts: remove dealer from panel for 30 minutes, then retry with smaller size.

Internal Memory
Short‑term (intraday): venue latency, fill probabilities, real‑time exposure.
Medium‑term (monthly): historical performance metrics per instrument‑venue pair.
Long‑term (annually): parameter estimates for cost models, regression coefficients for aggregated liquidity models.

Explainability Layer
For each parent order, produce a “venue selection justification” showing top venues, scores, and exclusion reasons.
Dashboard: average venue utilization, cost savings vs benchmark, credit usage headroom.

Health Metrics
Venue routing effectiveness: % of orders executed on top‑ranked venues.
Execution cost relative to estimated: within ±20% for 90% of orders.
Credit limit utilization: never exceeding 95%.
SOR decision latency: p99 < 10 µs for exchange routing, < 50 ms for RFQ initiation.
RFQ hit rate: > 90% of RFQs receive at least one response.

Interfaces
AITOS-EXEC-14
AITOS-MICRO-08
AITOS-RISK-10
AITOS-EFF-07
AITOS-SETTLE (future)
AITOS-REGIME

Production-Grade Pseudocode
def route_order(instrument, side, size, urgency):
venues = get_eligible_venues(instrument, side)
venues = [v for v in venues if v.status == 'OPEN' and credit_check(v, size) and v.toxicity < 0.8]
if not venues:
return error("No eligible venue")
cost_probs = []
for v in venues:
cost = estimate_total_cost(v, instrument, size, urgency)
prob = estimate_fill_prob(v, instrument, size)
cost_probs.append((v, cost, prob))
sorted_venues = sorted(cost_probs, key=lambda x: x[1] + penalty*(1-x[2]))
allocation = []
total_size = size
for v, cost, prob in sorted_venues:
alloc = min(total_size, v.max_order_size) if prob > 0.5 else 0
allocation.append((v, alloc))
total_size -= alloc
if total_size == 0: break
if total_size > 0:
allocation.append((primary_exchange, total_size))
return allocation

Knowledge Graph
Exchange & OTC Management
├── VenueRegistry
│
├── Exchanges
│
├── MTFs
│
├── DarkPools
│
└── OTCDealers
├── VenueSelectionEngine
│
├── CostModel
│
├── FillProbabilityModel
│
└── CreditConstraintChecker
├── LiquidityAggregation
│
└── ConsolidatedOrderBook
├── RFQManager
│
├── RequestForQuote
│
├── QuoteCollection
│
└── BestQuoteSelector
├── Monitoring
│
├── VenueHealthChecker
│
└── CreditExposureTracker
└── Interfaces (Execution, Risk, Microstructure)

Machine‑Readable JSON Schema
{
"module_id": "AITOS-EXOTC-09",
"version": "1.0",
"state": {
"venue_registry": "list[Venue]",
"credit_limits": "dict[string, float]",
"aggregated_lob": "dict[string, ConsolidatedLOB]"
},
"inputs": ["market_data_feeds", "order_requests", "credit_updates"],
"outputs": ["venue_allocations", "liquidity_views", "alerts"],

"decision_engine": {
"algorithm": "multi-objective optimization",
"objective": "minimize expected execution cost subject to constraints",
"constraints": ["credit", "regulatory", "size_limits"]
},
"interfaces": ["AITOS-EXEC-14", "AITOS-MICRO-08", "AITOS-RISK-10"]
}

Changelog
v1.0: Initial production specification covering exchange and OTC venue management, SOR, RFQ, credit limits, and venue performance
monitoring.

Module 04: Trading Session & Market Calendar Engine
(AITOS‑SESSION‑10)
Metadata
Module ID: AITOS-SESSION-10
Chapter: 10 – Trading Sessions
Version: 1.0
Last Updated: 2026-07-20
Dependencies: AITOS-EXOTC-09, AITOS-MICRO-08, AITOS-EFF-07
Status: Production

Purpose
To provide all other AITOS modules with a precise, real‑time model of market session state for every traded instrument. The module encapsulates
trading calendars, intraday volume/volatility curves, holiday schedules, and session‑specific behaviors so that execution, alpha, and risk modules can
adapt their strategies to the current market environment.

Scope
Maintain a global calendar of trading sessions for all exchanges and OTC markets.
Define standard session types: PRE‑MARKET, REGULAR, AFTER‑HOURS, CLOSED, AUCTION, MAINTENANCE.
Provide a real‑time session state with expected remaining time and transition probabilities.
Provide intraday volume profiles normalized to ADV for each session phase.
Model typical spread, depth, and volatility patterns as functions of session type and time within session.
Support session‑aware routing decisions, risk limits, and alpha decay.

Internal State Representation
Global Session Clock
{
"timestamp": "2026-07-20T14:32:01.123Z",
"active_sessions": {
"US_EQUITIES": {
"session_type": "REGULAR",
"start_time": "09:30:00 EST",
"end_time": "16:00:00 EST",
"next_transition": "16:00:00 EST",
"time_to_next": 5280.0
}
}
}

Per‑Instrument Session Object
{
"instrument_id": "AAPL",
"market_venue": "NASDAQ",
"session_type": "REGULAR",
"sub_phase": "MID_DAY",
"time_to_close_sec": 5280,
"is_auction_period": false,
"volume_profile_weight": 0.05,
"typical_spread_multiplier": 1.0,
"typical_impact_multiplier": 1.0,
"holiday_risk_flag": false
}

Knowledge Representation
Trading Calendar: deterministic schedule from exchange rules, with holiday exceptions. Represented as a decision tree.
Volume Curve Model: piecewise linear or spline function V(t) giving fraction of ADV traded up to time t.
Session Transition Probability: small probability of unscheduled closures.
Liquidity Parameter Curves: spread_factor(t), depth_factor(t), vol_factor(t) as functions of normalized session time τ.

Inputs
Venue status and schedule from AITOS-EXOTC-09.
Real‑time exchange notifications (halts, technical issues).
Current UTC timestamp (atomic).
Historical intraday volume data for calibration.
Holiday/early‑close calendars.

Outputs
Continuous stream of session state updates.
Session‑based parameters: volume weight, spread multiplier, volatility multiplier.
Time‑to‑event triggers (e.g., “closing auction in 5 minutes”).
Risk module alerts when session is about to close and positions remain.
Pre‑market/post‑market liquidity warnings.

Core Reasoning Engine
Finite‑state machine (FSM) for each instrument, with deterministic scheduled transitions and probabilistic halts.
States: CLOSED, PRE_MARKET, REGULAR (with sub‑states OPEN_AUCTION, CONTINUOUS, CLOSE_AUCTION), AFTER_HOURS,
HALTED, CLOSED_EARLY.
Session‑aware liquidity estimation:
σ(τ) = σ_base · g(τ)
impact_factor(τ) = h(τ) · (volume_weight(τ))^(−γ)

Decision Rules
Execution module: adapt order types per session (only limit orders in pre‑/after‑hours).
Risk module: reduce position limits near close.
Alpha: use session‑specific alpha decay; first and last 30 minutes more reliable.
Portfolio rebalancing: prefer close (MOC) orders.

Constraint Engine
Must respect exchange‑specific calendar nuances.
Must not allow trading outside allowed times.
Multi‑asset session coordination for baskets.
Circuit breaker rules: after Level 3 halt, all instruments to HALTED.

Validation Engine
Daily consistency check of session state changes.
Backtest volume curves; recalibrate if RMSE exceeds threshold.

Simulate holiday impact.

Monitoring Rules
Alert if session state change does not occur at scheduled time.
Monitor spread/depth predictions against actual.
Log every session transition.

Learning & Adaptation
Volume curve update monthly.
Spread/depth curve quarterly.
Unscheduled halt model: update Poisson parameter.
Holiday corrections annually.

Failure Modes
Failure

Detection

Response

Exchange calendar data error

Mismatch between state and actual

Flag emergency; pause trading for that instrument.

Incorrect volume profile

Large slippage relative to expectation

Recalibrate, reduce order sizes.

Delayed session opening

Market data not arriving

Extend pre‑market; do not send orders until first trade.

Early unscheduled close

Exchange announcement

Cancel open orders, liquidate if risk mandates.

Recovery Procedures
After delayed open: wait 2 minutes for order book stability.
After erroneous holiday flag: manual override.
After data gap: fall back to generic session curve.

Internal Memory
Session state log.
Calibration cache (volume/spread curves per instrument and session type).
Holiday database for 5 years.

Explainability Layer
Log session type, volume weight, spread multiplier for each trade.
Dashboard: world clock with session indicators, color‑coded by liquidity regime.

Health Metrics
Session state accuracy: > 99.99% match to actual market status.
Volume prediction error (MAPE) per 5‑min bucket < 20%.
Execution cost attributable to session mis‑prediction < 1 bp.

Interfaces
AITOS-EXEC-14
AITOS-RISK-10
AITOS-ALPHA
AITOS-MICRO-08
AITOS-PORT

Production-Grade Pseudocode
def update_session_state(instrument, current_time):
calendar = get_calendar(instrument)
session_times = calendar.get_sessions(current_time.date())
if session_times is None:
instrument.session_type = 'CLOSED'
return
for session in session_times:
if session.start <= current_time < session.end:
instrument.session_type = session.type
instrument.time_to_next = (session.end - current_time).seconds
tau = (current_time - session.start).total_seconds() / session.duration_seconds
instrument.volume_weight = volume_curve(session.type, tau)
instrument.spread_multiplier = spread_curve(session.type, tau)
instrument.impact_multiplier = impact_curve(session.type, tau, instrument.volume_weight)
return
instrument.session_type = 'CLOSED'

Knowledge Graph
Trading Session Engine
├── SessionStateMachine
│
├── States (CLOSED, PRE_MARKET, REGULAR, AFTER_HOURS, HALTED)
│
└── Transitions (scheduled, unscheduled)
├── SessionAwareLiquidity
│
├── VolumeCurve
│
├── SpreadCurve
│
└── ImpactCurve
├── CalendarDB
│
├── ExchangeCalendars
│
└── HolidayExceptions
└── InterfaceContracts
├── SessionStatePush
└── SessionParameterQuery

Machine‑Readable JSON Schema
{
"module_id": "AITOS-SESSION-10",
"version": "1.0",
"state": {
"instrument_sessions": {
"type": "dict",
"value": {
"session_type": "string",
"tau": "float",
"volume_weight": "float",
"spread_multiplier": "float",
"impact_multiplier": "float",
"time_to_next_sec": "float",
"is_auction": "bool"
}
},
"global_calendar": "CalendarDB"
},
"inputs": ["current_time", "venue_status", "holiday_updates"],
"outputs": ["session_state_stream", "session_parameters"],
"decision_rules": {
"execution": "adapt order type per session",
"risk": "reduce limits near close"
},
"interfaces": ["AITOS-EXEC-14", "AITOS-RISK-10", "AITOS-ALPHA", "AITOS-MICRO-08"]
}

Changelog
v1.0: Initial production specification. FSM with calendar, volume curves, session‑aware liquidity estimation.
