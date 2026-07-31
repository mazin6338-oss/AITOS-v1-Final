---
Architecture Version: 2.0
Release: Canonical v2
Status: Approved
Last Updated: 2026-07-25
---

# Documentation Standards for AITOS v2

## Table of Contents
1.  [Introduction](#1-introduction)
2.  [Purpose](#2-purpose)
3.  [General Principles](#3-general-principles)
4.  [Document Types and Structure](#4-document-types-and-structure)
    *   [Architectural Documents (00_Architecture)](#architectural-documents-00_architecture)
    *   [Module Specifications (01_Modules)](#module-specifications-01_modules)
    *   [Research Documents (03_Research)](#research-documents-03_research)
    *   [Interface Contracts (06_Interfaces)](#interface-contracts-06_interfaces)
    *   [Standards Documents (07_Standards)](#standards-documents-07_standards)
5.  [Formatting Guidelines](#5-formatting-guidelines)
    *   [Markdown Syntax](#markdown-syntax)
    *   [Headings and Table of Contents](#headings-and-table-of-contents)
    *   [Code Blocks](#code-blocks)
    *   [Diagrams](#diagrams)
    *   [Tables](#tables)
    *   [Cross-Referencing](#cross-referencing)
6.  [Metadata Header](#6-metadata-header)
7.  [Conclusion](#7-conclusion)

## 1. Introduction
This document establishes the mandatory documentation standards for all written artifacts within the AITOS v2 project. High-quality, consistent, and comprehensive documentation is a cornerstone of the "Documentation First" principle and is essential for the long-term success, maintainability, and explainability of the system. Adherence to these standards is enforced as part of the `QUALITY_GATE.md`.

## 2. Purpose
The primary purpose of these documentation standards is to:
*   **Ensure Clarity:** Make all project information easy to understand for developers, researchers, and stakeholders.
*   **Promote Consistency:** Establish a uniform style, structure, and quality across all documents.
*   **Facilitate Knowledge Transfer:** Enable efficient onboarding of new team members and reduce reliance on tribal knowledge.
*   **Support Traceability:** Provide clear links between design decisions, code, and testing.
*   **Enhance Maintainability:** Simplify updates and prevent documentation from becoming stale.
*   **Comply with Governance:** Meet the requirements for auditability and transparency.

## 3. General Principles
*   **Accuracy:** Documentation must always reflect the current state of the system.
*   **Completeness:** All significant aspects of a component or decision must be documented.
*   **Conciseness:** Avoid unnecessary verbosity. Be direct and to the point.
*   **Clarity:** Use simple, unambiguous language. Avoid jargon where possible, or define it clearly.
*   **Audience Awareness:** Tailor the level of detail to the primary audience of the document.
*   **Version Control:** All documentation must be version-controlled alongside the code.
*   **English Language:** All formal documentation must be written in English.

## 4. Document Types and Structure

### Architectural Documents (00_Architecture)
*   **Purpose:** Define the high-level structure, principles, and foundational aspects of the AITOS system.
*   **Structure:** Must include a standard metadata header, Table of Contents, Introduction, Purpose, detailed sections, and Conclusion.
*   **Examples:** `AITOS_Master_Architecture.md`, `PROJECT_PRINCIPLES.md`, `CORE_DATA_MODEL.md`.

### Module Specifications (01_Modules)
*   **Purpose:** Provide detailed technical specifications for individual AITOS modules.
*   **Structure:** Each module directory (`01_Modules/[MODULE-ID]/`) must contain:
    *   `README.md`: High-level overview, purpose, and maturity assessment.
    *   `SPECIFICATION.md`: Detailed functional and non-functional requirements, internal state, inputs/outputs.
    *   `INTERFACE.md`: Formal definition of external interactions.
    *   `STATE_MACHINE.md`: (If applicable) State transitions and behavior.
    *   `ALGORITHMS.md`: Detailed algorithmic logic and mathematical models.
    *   `TEST_PLAN.md`: Testing strategy, scope, and coverage.
    *   `CHANGELOG.md`: Version history and significant changes.
*   **Content:** Must align with `CORE_DATA_MODEL.md` and `06_Interfaces`.

### Research Documents (03_Research)
*   **Purpose:** Document research findings, theoretical models, and experimental results.
*   **Structure:** Flexible, but should include clear problem statements, methodologies, results, and conclusions. Must adhere to metadata header requirements.
*   **Examples:** `03_Research/SMC/BOS/Definition.md`.

### Interface Contracts (06_Interfaces)
*   **Purpose:** Formally define the structure and behavior of data exchanged between modules.
*   **Structure:** Must be JSON Schema files (`.schema`) with clear `title`, `description`, `version`, `properties`, and `required` fields. Must include `compatibility` and `error_behavior` attributes.

### Standards Documents (07_Standards)
*   **Purpose:** Define mandatory rules and guidelines for various aspects of development (e.g., coding, naming, testing).
*   **Structure:** Similar to Architectural Documents, with clear rules, examples, and justifications.

## 5. Formatting Guidelines

### Markdown Syntax
*   Use standard GitHub-flavored Markdown.
*   Avoid excessive use of HTML tags within Markdown.

### Headings and Table of Contents
*   Use `#` for top-level headings, `##` for sub-headings, etc.
*   All documents with more than three sections must include a Table of Contents with internal links.

### Code Blocks
*   Use fenced code blocks (```) with language highlighting (e.g., ```python, ```json, ```mermaid).

### Diagrams
*   Use Mermaid syntax for architectural diagrams, workflows, and state machines where appropriate.
*   Diagrams should be embedded directly in Markdown files.

### Tables
*   Use Markdown pipe tables for structured data.
*   Ensure tables are readable and well-formatted.

### Cross-Referencing
*   Use relative Markdown links for internal references within the repository (e.g., `[PROJECT_PRINCIPLES](./PROJECT_PRINCIPLES.md)`).
*   Explicitly mention the document name when referencing (e.g., "as defined in `CORE_DATA_MODEL.md`").

## 6. Metadata Header
Every architectural and standards document must begin with the following YAML-like metadata header:

```yaml
---
Architecture Version: 2.0
Release: Canonical v2
Status: Approved
Last Updated: YYYY-MM-DD
---
```

## 7. Conclusion
Adherence to these documentation standards is critical for maintaining the clarity, consistency, and long-term value of the AITOS v2 project. Quality documentation is not merely a byproduct of development; it is an integral part of the engineering process, enabling efficient collaboration and ensuring the system\"s explainability and maintainability.
