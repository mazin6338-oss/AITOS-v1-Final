---
Architecture Version: 2.0
Release: Canonical v2
Status: Approved
Last Updated: 2026-07-25
---

# Core Data Model: Canonical Entities for AITOS v2

## Table of Contents
1.  [Introduction](#1-introduction)
2.  [Purpose](#2-purpose)
3.  [Canonical Data Entities](#3-canonical-data-entities)
    *   [Candle](#candle)
    *   [Tick](#tick)
    *   [Swing](#swing)
    *   [Market Structure](#market-structure)
    *   [Liquidity Zone](#liquidity-zone)
    *   [Order Block](#order-block)
    *   [Fair Value Gap](#fair-value-gap)
    *   [Session](#session)
    *   [Signal](#signal)
    *   [Trade](#trade)
    *   [Position](#position)
    *   [Portfolio](#portfolio)
    *   [Risk Profile](#risk-profile)
4.  [Conclusion](#4-conclusion)

## 1. Introduction
This document defines the core data model for the AITOS v2 platform, establishing a canonical representation for all fundamental entities used across various modules. This model serves as the single source of truth for data definitions, ensuring consistency, interoperability, and clarity throughout the system.

## 2. Purpose
The primary purpose of the Core Data Model is to:
*   **Standardize Data Definitions:** Provide unambiguous definitions for all key data entities.
*   **Ensure Consistency:** Guarantee that all modules interpret and use data in a uniform manner.
*   **Facilitate Integration:** Simplify data exchange and communication between different AITOS components.
*   **Improve Maintainability:** Reduce complexity and potential errors arising from disparate data representations.
*   **Enhance Explainability:** Offer a clear understanding of the data underpinning all system decisions.

## 3. Canonical Data Entities

### Candle
*   **Purpose:** Represents aggregated price action over a specific time interval (e.g., 1-minute, 5-minute, daily).
*   **Attributes:** `timestamp` (start of interval), `open`, `high`, `low`, `close`, `volume`, `vwap` (Volume Weighted Average Price).
*   **Relationships:** Derived from `Tick` data; forms the basis for `Market Structure` and `Swing` analysis.
*   **Lifecycle:** Created upon interval close, immutable.
*   **Validation Rules:** `open`, `high`, `low`, `close` must be positive; `low <= open, close <= high`; `volume >= 0`.

### Tick
*   **Purpose:** Represents the most granular price and volume data, capturing individual transactions or quotes.
*   **Attributes:** `timestamp`, `price`, `size`, `exchange_id`, `bid_price`, `ask_price`, `bid_size`, `ask_size`.
*   **Relationships:** Aggregated to form `Candle` data; direct input for `Microstructure` analysis.
*   **Lifecycle:** Real-time, ephemeral for storage, but persistent for processing.
*   **Validation Rules:** `price`, `size` must be positive; `bid_price <= ask_price`.

### Swing
*   **Purpose:** Identifies significant price turning points (highs and lows) in market data, crucial for trend analysis and structural mapping.
*   **Attributes:** `timestamp`, `type` (high/low), `price`, `strength` (e.g., number of candles confirming).
*   **Relationships:** Derived from `Candle` data; fundamental for `Market Structure` identification.
*   **Lifecycle:** Dynamic, can be re-evaluated as new data arrives.
*   **Validation Rules:** Must adhere to specific swing identification algorithms (e.g., fractal, pivot point).

### Market Structure
*   **Purpose:** Defines the prevailing trend and structural characteristics of the market (e.g., bullish, bearish, ranging, break of structure, change of character).
*   **Attributes:** `timestamp`, `type` (e.g., `BOS` - Break of Structure, `CHoCH` - Change of Character), `direction` (bullish/bearish), `confirmation_level`.
*   **Relationships:** Derived from `Swing` points and `Candle` data; influences `Liquidity Zone` and `Order Block` identification.
*   **Lifecycle:** Continuously updated based on new price action.
*   **Validation Rules:** Must follow established market structure rules (e.g., higher highs/lows for bullish trend).

### Liquidity Zone
*   **Purpose:** Identifies areas in the market where significant buy or sell orders are likely to be accumulated, often associated with swing highs/lows or inefficient price action.
*   **Attributes:** `start_price`, `end_price`, `type` (e.g., buy-side, sell-side), `strength`, `status` (e.g., mitigated, unmitigated).
*   **Relationships:** Influenced by `Market Structure`; attracts `Order Block` formation.
*   **Lifecycle:** Created, then potentially mitigated or invalidated by price action.
*   **Validation Rules:** Must be formed around key price levels or structural points.

### Order Block
*   **Purpose:** Represents specific price ranges where institutional buying or selling pressure is evident, often leading to significant market moves.
*   **Attributes:** `start_price`, `end_price`, `timestamp` (formation), `type` (bullish/bearish), `volume_profile`, `mitigation_status`.
*   **Relationships:** Often found within `Liquidity Zones`; key input for `Fair Value Gap` analysis.
*   **Lifecycle:** Formed, then potentially mitigated or invalidated.
*   **Validation Rules:** Must meet specific criteria (e.g., last down candle before an up move in a bullish trend).

### Fair Value Gap
*   **Purpose:** Identifies price inefficiencies or imbalances in the market, often targeted for future price action.
*   **Attributes:** `start_price`, `end_price`, `timestamp` (formation), `type` (bullish/bearish imbalance), `mitigation_status`.
*   **Relationships:** Often occurs after `Order Block` formation; a target for price to rebalance.
*   **Lifecycle:** Formed, then potentially filled or invalidated.
*   **Validation Rules:** Defined by specific candle patterns (e.g., three-candle pattern where middle candle's range is not fully covered by adjacent candles).

### Session
*   **Purpose:** Defines specific trading periods (e.g., Asian, London, New York sessions) which exhibit distinct market characteristics.
*   **Attributes:** `session_id`, `start_timestamp`, `end_timestamp`, `name`, `volatility_profile`, `volume_profile`.
*   **Relationships:** Provides context for `Candle` and `Tick` data; influences `Signal` generation.
*   **Lifecycle:** Fixed daily/weekly intervals.
*   **Validation Rules:** Must adhere to predefined market session times.

### Signal
*   **Purpose:** An actionable indication generated by an AITOS module, suggesting a potential trading opportunity.
*   **Attributes:** `signal_id`, `timestamp`, `instrument`, `direction` (buy/sell), `entry_price`, `stop_loss`, `take_profit`, `confidence_score`, `source_module`.
*   **Relationships:** Generated by `Alpha Engine`; consumed by `Risk Engine` and `Execution Engine`.
*   **Lifecycle:** Generated, evaluated, potentially executed, then tracked.
*   **Validation Rules:** Must meet minimum confidence thresholds; must pass `Risk Profile` checks.

### Trade
*   **Purpose:** Represents a single executed order or a series of orders forming a complete trading action (e.g., buy and sell to close).
*   **Attributes:** `trade_id`, `signal_id` (if applicable), `instrument`, `direction`, `entry_timestamp`, `entry_price`, `exit_timestamp`, `exit_price`, `quantity`, `profit_loss`, `fees`.
*   **Relationships:** Initiated by `Execution Engine`; contributes to `Position` and `Portfolio`.
*   **Lifecycle:** Opened, managed, closed.
*   **Validation Rules:** Must adhere to `Risk Profile` limits; must be within `Execution` constraints.

### Position
*   **Purpose:** Represents the current holdings of a specific instrument in the portfolio.
*   **Attributes:** `position_id`, `instrument`, `quantity`, `average_entry_price`, `current_market_price`, `unrealized_pnl`, `direction` (long/short).
*   **Relationships:** Updated by `Trade` executions; aggregated into `Portfolio`.
*   **Lifecycle:** Opened, adjusted, closed.
*   **Validation Rules:** `quantity` must be non-negative; `average_entry_price` must be positive.

### Portfolio
*   **Purpose:** Represents the aggregate collection of all assets, liabilities, and positions managed by the system.
*   **Attributes:** `portfolio_id`, `cash_balance`, `total_equity`, `total_pnl`, `risk_exposure`, `list_of_positions`.
*   **Relationships:** Composed of `Position` objects; managed by `Portfolio Management Engine`.
*   **Lifecycle:** Continuously updated.
*   **Validation Rules:** `cash_balance` and `total_equity` must be non-negative.

### Risk Profile
*   **Purpose:** Defines the risk parameters and constraints applicable to a `Portfolio` or individual `Trade`.
*   **Attributes:** `profile_id`, `max_drawdown`, `max_daily_loss`, `max_position_size`, `value_at_risk`, `expected_shortfall`.
*   **Relationships:** Applied by `Risk Engine`; influences `Signal` filtering and `Execution` sizing.
*   **Lifecycle:** Configured, monitored, adjusted.
*   **Validation Rules:** All risk metrics must be within predefined thresholds.

## 4. Conclusion
This Core Data Model provides a robust and consistent foundation for all data-driven operations within AITOS v2. By adhering to these canonical definitions, we ensure clarity, reduce ambiguity, and enhance the overall reliability and scalability of the trading platform.
