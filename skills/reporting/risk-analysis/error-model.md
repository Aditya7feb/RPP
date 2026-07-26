# Risk Analysis Error Model

**File:** `skills/reporting/risk-analysis/error-model.md`

**Version:** 1.0.0

---

# Purpose

This document defines the canonical error categories of the Risk Analysis Capability.

---

# Error Categories

| Category | Meaning | Outcome |
|----------|---------|---------|
| input-unavailable | A referenced Finding or Risk did not resolve | partial |
| bounds-exhausted | Analysis bounds reached | partial |
| insufficient-data | Inputs lack data required for a calculation | partial |

---

# input-unavailable

When a referenced Finding or Risk cannot be resolved, the capability SHALL produce a partial analysis
over the resolvable subset.

---

# bounds-exhausted

When analysis bounds are reached, the capability SHALL finalize a partial analysis.

---

# insufficient-data

When inputs lack the data required for a calculation such as CVSS, the capability SHALL omit that
derived value rather than inventing one, and canonical Risk remains authoritative.

---

# Determinism

Identical error conditions SHALL yield identical categories and outcomes.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [configuration.md](configuration.md)
