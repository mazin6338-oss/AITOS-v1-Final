---
Architecture Version: 2.0
Release: Canonical v2
Status: Approved
Last Updated: 2026-07-25
---

# Coding Standards for AITOS v2

## Table of Contents
1.  [Introduction](#1-introduction)
2.  [Purpose](#2-purpose)
3.  [General Principles](#3-general-principles)
4.  [Language-Specific Guidelines](#4-language-specific-guidelines)
    *   [Python](#python)
    *   [C++](#c)
    *   [Rust](#rust)
5.  [Code Structure and Organization](#5-code-structure-and-organization)
6.  [Error Handling](#6-error-handling)
7.  [Performance Considerations](#7-performance-considerations)
8.  [Security Best Practices](#8-security-best-practices)
9.  [Conclusion](#9-conclusion)

## 1. Introduction
This document establishes the mandatory coding standards for all source code developed within the AITOS v2 project. Adherence to these standards ensures consistency, readability, maintainability, and high quality across the entire codebase. These standards are enforced as part of the `QUALITY_GATE.md` and are crucial for collaborative development and long-term project success.

## 2. Purpose
The primary purpose of these coding standards is to:
*   **Enhance Readability:** Make code easy to understand for all developers.
*   **Improve Maintainability:** Simplify debugging, refactoring, and future enhancements.
*   **Ensure Consistency:** Establish a uniform style across different modules and programming languages.
*   **Facilitate Collaboration:** Enable seamless teamwork by reducing stylistic conflicts.
*   **Reduce Defects:** Promote best practices that minimize common programming errors.
*   **Support Automation:** Allow automated tools (linters, formatters) to enforce standards.

## 3. General Principles
*   **Clarity:** Code should be self-documenting where possible. Avoid clever but obscure constructs.
*   **Simplicity:** Prefer simple, straightforward solutions over complex ones. Avoid unnecessary abstraction.
*   **Modularity:** Design code in small, focused functions and classes with clear responsibilities.
*   **DRY (Don\'t Repeat Yourself):** Avoid code duplication. Abstract common logic into reusable components.
*   **SOLID Principles:** Adhere to Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, and Dependency Inversion principles.
*   **Testability:** Write code that is easy to test. Design for testability from the outset.
*   **Performance:** Optimize for performance where critical, but not at the expense of readability or correctness.
*   **Security:** Implement secure coding practices to prevent vulnerabilities.

## 4. Language-Specific Guidelines

### Python
*   **PEP 8:** Adhere strictly to PEP 8 style guide for Python code.
*   **Type Hinting:** Use type hints for all function arguments and return values.
*   **Docstrings:** Use Google-style or NumPy-style docstrings for all modules, classes, and functions.
*   **Imports:** Organize imports according to PEP 8 (standard library, third-party, local application, relative imports).
*   **Logging:** Use the standard `logging` module for all logging. Avoid `print()` for debugging in production code.

### C++
*   **Google C++ Style Guide:** Follow the Google C++ Style Guide, with specific project-level deviations documented.
*   **Modern C++:** Utilize C++11/14/17/20 features where appropriate to write cleaner, safer, and more efficient code.
*   **Smart Pointers:** Prefer `std::unique_ptr` and `std::shared_ptr` over raw pointers for memory management.
*   **Error Handling:** Use exceptions for exceptional conditions, and `std::optional` or `std::expected` for expected failures.

### Rust
*   **Rustfmt:** Use `rustfmt` for automatic code formatting.
*   **Clippy:** Adhere to `clippy` lints and warnings.
*   **Error Handling:** Prefer `Result<T, E>` and `Option<T>` for error handling and absence of values.
*   **Ownership and Borrowing:** Understand and correctly apply Rust\'s ownership and borrowing rules.

## 5. Code Structure and Organization
*   **Module Directories:** Code for each AITOS module resides in `01_Modules/[MODULE-ID]/implementation/`.
*   **File Naming:** Follow `07_Standards/Naming_Convention.md`.
*   **Directory Structure:** Organize code logically within subdirectories (e.g., `src/`, `tests/`, `models/`).

## 6. Error Handling
*   **Consistent Strategy:** Implement a consistent error handling strategy across the system (e.g., exceptions in Python/C++, `Result` in Rust).
*   **Informative Errors:** Error messages should be clear, concise, and provide sufficient context for debugging.
*   **Graceful Degradation:** Design modules to degrade gracefully in the face of errors, preventing cascading failures.

## 7. Performance Considerations
*   **Profiling:** Profile code to identify performance bottlenecks before optimizing.
*   **Algorithmic Complexity:** Be mindful of algorithmic complexity (Big O notation) when choosing data structures and algorithms.
*   **Resource Management:** Efficiently manage memory, CPU, and network resources.

## 8. Security Best Practices
*   **Input Validation:** Validate all external inputs to prevent injection attacks and unexpected behavior.
*   **Least Privilege:** Code should operate with the minimum necessary permissions.
*   **Secrets Management:** Never hardcode sensitive information. Use secure configuration management (e.g., environment variables, secret stores).
*   **Dependency Management:** Regularly update and scan third-party dependencies for vulnerabilities.

## 9. Conclusion
Adherence to these coding standards is paramount for building a robust, maintainable, and high-performance algorithmic trading system. These guidelines are actively enforced through code reviews and automated checks, contributing directly to the long-term success and scalability of AITOS v2.
