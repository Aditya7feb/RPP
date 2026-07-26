# Finding Correlation Error Model

**File:** `skills/reporting/finding-correlation/error-model.md`

**Version:** 1.0.0

---

# Purpose

This document defines the canonical error categories of the Finding Correlation Capability.

---

# Error Categories

| Category | Meaning | Outcome |
|----------|---------|---------|
| finding-unavailable | A referenced Finding did not resolve | partial |
| bounds-exhausted | Correlation bounds reached | partial |
| uncorrelatable | Findings share no correlatable attribute | partial |

---

# finding-unavailable

When a referenced Finding cannot be resolved, the capability SHALL produce a partial correlation
over the resolvable subset.

---

# bounds-exhausted

When correlation bounds are reached, the capability SHALL finalize a partial correlation.

---

# uncorrelatable

When Findings share no correlatable attribute, the capability SHALL record them as uncorrelated
rather than inventing a relationship.

---

# Determinism

Identical error conditions SHALL yield identical categories and outcomes.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [configuration.md](configuration.md)
