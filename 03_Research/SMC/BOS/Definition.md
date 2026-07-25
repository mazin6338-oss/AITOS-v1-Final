# BOS (Break Of Structure) Definition

## Overview
Break of Structure (BOS) is a core concept in Smart Money Concepts (SMC) that indicates the continuation of a trend.

## Mathematical Definition
*   **Bullish BOS:** Occurs when the price closes above the previous Swing High in an uptrend.
*   **Bearish BOS:** Occurs when the price closes below the previous Swing Low in a downtrend.

## Algorithm
1. Identify the current market trend (Bullish/Bearish).
2. Mark the most recent Swing High and Swing Low.
3. Monitor for a candle close beyond the identified Swing point.
4. Confirm the break with volume or follow-through.

## Unit Tests
*   Test with clear trend break.
*   Test with wick-only break (False BOS).
*   Test in ranging market.
