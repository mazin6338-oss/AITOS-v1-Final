---
Architecture Version: 2.0
Release: Canonical v2
Status: Approved
Last Updated: 2026-07-25
---

# AITOS v2 Interface Contracts

This document defines the standardized interface contracts for all AITOS v2 modules.

## 1. Data Exchange Format
All modules MUST use JSON for inter-module communication.

## 2. Event Structure
Every event emitted by a module MUST include:
- `timestamp`: RFC3339 format.
- `module_id`: The source module identifier.
- `event_type`: Categorized type of event.
- `payload`: The actual data being transmitted.

## 3. Subscription Model
Modules subscribe to specific output streams of their upstream dependencies as defined in the `MODULE_INDEX.md`.
