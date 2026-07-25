---
Architecture Version: 2.0
Release: Canonical v2
Status: Approved
Last Updated: 2026-07-25
---

# AITOS v2 Architecture Rules

These rules govern the development and integration of all AITOS v2 modules.

1.  **Immutability:** Upstream data must be treated as immutable by downstream modules.
2.  **Statelessness:** Where possible, modules should be stateless or manage state through a centralized persistence layer.
3.  **Error Handling:** Every module must implement standardized error reporting to the `AITOS-MONITOR` engine.
4.  **Isolation:** Modules must not have side effects on other modules except through defined output streams.
5.  **Validation:** All inputs must be validated against the defined schema before processing.
