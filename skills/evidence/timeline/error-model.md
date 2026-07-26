# Timeline Error Model

**File:** `skills/evidence/timeline/error-model.md`

**Version:** 1.0.0

---

# Purpose

This document defines the canonical error categories of the Timeline Capability.

---

# Error Categories

| Category | Meaning | Outcome |
|----------|---------|---------|
| reference-unavailable | A referenced Observation or Evidence did not resolve | partial |
| bounds-exhausted | Timeline bounds reached | partial |
| uncorrelatable | Items cannot be chronologically ordered | partial |
| promotion-error | Shared Evidence lifecycle could not promote the timeline | partial |

---

# reference-unavailable

When a referenced Observation or Evidence cannot be resolved, the capability SHALL produce a partial
timeline over the resolvable subset.

---

# bounds-exhausted

When timeline bounds are reached, the capability SHALL finalize a partial timeline.

---

# uncorrelatable

When items lack the information required to order them chronologically, the capability SHALL record
them as uncorrelated rather than inferring an order.

---

# promotion-error

When the shared [Evidence](../../shared/evidence/README.md) lifecycle cannot promote the timeline,
the capability SHALL return a partial result retaining the timeline Artifact reference.

---

# Determinism

Identical error conditions SHALL yield identical categories and outcomes.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [configuration.md](configuration.md)
