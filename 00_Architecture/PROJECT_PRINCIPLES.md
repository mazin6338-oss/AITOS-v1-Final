---
Architecture Version: 2.0
Release: Canonical v2
Status: Approved
Last Updated: 2026-07-25
---

# Project Principles: Guiding the AITOS v2 Development

## Table of Contents
1.  [Introduction](#1-introduction)
2.  [Vision](#2-vision)
3.  [Mission](#3-mission)
4.  [Project Goals](#4-project-goals)
5.  [Non-Negotiable Principles](#5-non-negotiable-principles)
    *   [Market First Philosophy](#market-first-philosophy)
    *   [Data Driven Development](#data-driven-development)
    *   [Documentation First](#documentation-first)
    *   [Algorithm First](#algorithm-first)
    *   [Test First](#test-first)
    *   [Explainability](#explainability)
    *   [Modularity](#modularity)
    *   [Single Source of Truth](#single-source-of-truth)
    *   [Performance Philosophy](#performance-philosophy)
    *   [AI Philosophy](#ai-philosophy)
    *   [Research Philosophy](#research-philosophy)
    *   [Coding Philosophy](#coding-philosophy)
6.  [Definition of Done](#6-definition-of-done)
7.  [Conclusion](#7-conclusion)

## 1. Introduction
This document outlines the foundational principles that guide the development of the AITOS v2 project. These principles serve as a compass for all decisions, ensuring alignment with the project's long-term vision and objectives. Adherence to these guidelines is crucial for maintaining the integrity, quality, and scalability of the AITOS system.

## 2. Vision
To build the most advanced, transparent, and self-evolving algorithmic trading system that consistently generates alpha while maintaining robust risk management and explainability.

## 3. Mission
Our mission is to develop a modular, data-driven, and AI-powered trading platform that leverages cutting-edge research and engineering practices to adapt to dynamic market conditions and deliver superior performance.

## 4. Project Goals
*   Achieve consistent, risk-adjusted returns in diverse market regimes.
*   Ensure high levels of system reliability, scalability, and maintainability.
*   Foster a culture of continuous improvement through data-driven insights and rigorous testing.
*   Maintain full explainability and traceability of all trading decisions.
*   Enable partial self-evolution capabilities through an integrated Development Agent.

## 5. Non-Negotiable Principles

### Market First Philosophy
All development efforts must be grounded in a deep understanding of market dynamics, participant behavior, and economic theory. The system's design and algorithms must reflect real-world market phenomena.

### Data Driven Development
Decisions regarding algorithm design, parameter tuning, and system optimization must be supported by empirical evidence derived from rigorous data analysis and backtesting.

### Documentation First
Comprehensive and up-to-date documentation is paramount. Every module, interface, algorithm, and architectural decision must be thoroughly documented before implementation begins. Documentation serves as the primary source of truth.

### Algorithm First
Clear, well-defined algorithms must precede any code implementation. The mathematical and logical foundations of each component should be established and validated independently.

### Test First
All code must be developed with a test-driven approach. Unit tests, integration tests, and comprehensive backtests are integral to the development process, ensuring correctness and robustness.

### Explainability
The system must be designed to provide clear, human-understandable explanations for its decisions and actions. This is critical for trust, debugging, and regulatory compliance.

### Modularity
The system should be composed of loosely coupled, highly cohesive modules. This promotes reusability, simplifies maintenance, and facilitates independent development and testing.

### Single Source of Truth
For any given piece of information (e.g., module specification, architectural decision), there must be one and only one authoritative source within the repository. Duplication of information is to be avoided.

### Performance Philosophy
While correctness and explainability are primary, performance is a critical consideration. Algorithms and implementations should be optimized for speed and efficiency where market conditions demand it, without compromising other core principles.

### AI Philosophy
AI components should augment human decision-making and automate complex tasks, not replace fundamental understanding. AI models must be interpretable, auditable, and integrated responsibly.

### Research Philosophy
Continuous research into new market phenomena, quantitative techniques, and technological advancements is essential. Research findings must be systematically documented and integrated into the development workflow.

### Coding Philosophy
Code must be clean, readable, maintainable, and adhere to established coding standards. Consistency in style and structure across the codebase is mandatory.

## 6. Definition of Done
A module or feature is considered "Done" only when it has successfully passed all stages of the Development Workflow and met all criteria outlined in the `QUALITY_GATE.md` document.

## 7. Conclusion
These project principles form the bedrock of AITOS v2 development. By adhering to them, we ensure that the system evolves into a robust, intelligent, and reliable platform capable of navigating the complexities of financial markets.
