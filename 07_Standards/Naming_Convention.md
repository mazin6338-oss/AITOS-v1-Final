---
Architecture Version: 2.0
Release: Canonical v2
Status: Approved
Last Updated: 2026-07-25
---

# Naming Convention Standards for AITOS v2

## Table of Contents
1.  [Introduction](#1-introduction)
2.  [Purpose](#2-purpose)
3.  [General Principles](#3-general-principles)
4.  [Specific Naming Rules](#4-specific-naming-rules)
    *   [Modules](#modules)
    *   [Files and Directories](#files-and-directories)
    *   [Variables and Constants](#variables-and-constants)
    *   [Functions and Methods](#functions-and-methods)
    *   [Classes and Objects](#classes-and-objects)
    *   [Interfaces and Schemas](#interfaces-and-schemas)
    *   [Events](#events)
    *   [Database Entities](#database-entities)
    *   [Git Branches and Commits](#git-branches-and-commits)
5.  [Conclusion](#5-conclusion)

## 1. Introduction
This document establishes the mandatory naming conventions for all components within the AITOS v2 project. Consistent naming is crucial for enhancing code readability, maintainability, and reducing cognitive load for developers and researchers. Adherence to these standards is a prerequisite for passing the `QUALITY_GATE.md`.

## 2. Purpose
The primary purpose of these naming conventions is to:
*   **Improve Readability:** Make code and documentation easier to understand at a glance.
*   **Enhance Maintainability:** Reduce ambiguity and simplify future modifications.
*   **Ensure Consistency:** Establish a uniform style across the entire codebase and documentation.
*   **Facilitate Collaboration:** Enable seamless collaboration among team members by providing clear guidelines.
*   **Support Automation:** Allow automated tools (e.g., linters, code generators) to process the codebase effectively.

## 3. General Principles
*   **Clarity over Brevity:** Names should be descriptive and unambiguous, even if slightly longer.
*   **Consistency:** Always follow the established convention for a given type of entity.
*   **Meaningful:** Names should convey the purpose or intent of the entity.
*   **Avoid Abbreviations:** Use full words unless the abbreviation is universally understood within the domain (e.g., `ID`, `API`).
*   **English Language:** All names must be in English.

## 4. Specific Naming Rules

### Modules
*   **Format:** `AITOS-<CONCEPT>-<NUMBER>` (e.g., `AITOS-MICRO-08`, `AITOS-SMC`).
*   **Usage:** Used for top-level module directories and their primary identifiers in `MODULE_INDEX.md`.

### Files and Directories
*   **General:** `snake_case` for files (e.g., `my_file.py`, `naming_convention.md`).
*   **Directories:** `snake_case` or `kebab-case` for directories (e.g., `unit_tests/`, `market-data/`). Prefer `kebab-case` for top-level architectural directories (e.g., `00_Architecture/`).
*   **Documentation Files:** Use `PascalCase` for main architectural documents (e.g., `PROJECT_PRINCIPLES.md`, `CORE_DATA_MODEL.md`).

### Variables and Constants
*   **Local Variables:** `snake_case` (e.g., `market_price`, `order_quantity`).
*   **Global Constants:** `SCREAMING_SNAKE_CASE` (e.g., `MAX_RETRIES`, `DEFAULT_TIMEOUT`).
*   **Class Attributes:** `snake_case` (e.g., `self.instrument_id`).

### Functions and Methods
*   **Format:** `snake_case` (e.g., `calculate_vwap()`, `process_market_data()`).
*   **Private Methods:** Prefix with a single underscore (e.g., `_validate_input()`).

### Classes and Objects
*   **Format:** `PascalCase` (e.g., `MarketDataProcessor`, `TradingSignal`).
*   **Abstract Classes:** Prefix with `Abstract` (e.g., `AbstractEngine`).

### Interfaces and Schemas
*   **Files:** `PascalCase.schema` (e.g., `MarketData.schema`, `Signal.schema`).
*   **JSON Schema Definitions:** `PascalCase` for main definitions (e.g., `Candle`, `Tick`).

### Events
*   **Format:** `PascalCase` in past tense (e.g., `CandleClosed`, `SignalGenerated`, `TradeExecuted`).
*   **Usage:** Used for `event_type` in `EVENT_BUS.md` and `MarketData.schema`.

### Database Entities
*   **Tables:** `snake_case_plural` (e.g., `market_data_candles`, `trading_positions`).
*   **Columns:** `snake_case` (e.g., `instrument_id`, `entry_price`).

### Git Branches and Commits
*   **Branches:** `feature/<feature-name>`, `bugfix/<bug-description>`, `docs/<doc-update>` (e.g., `feature/add-smc-module`, `bugfix/fix-risk-calc`).
*   **Commits:** Conventional Commits specification (e.g., `feat(module): add new feature`, `docs(governance): update principles`).

## 5. Conclusion
Adherence to these naming conventions is vital for maintaining the high quality and consistency expected of an enterprise-grade system like AITOS v2. These rules are enforced as part of the `QUALITY_GATE.md` and contribute directly to the project\'s long-term maintainability and scalability.
