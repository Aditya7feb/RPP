# Finding Mapping Error Model

**File:** `skills/reporting/finding-mapping/error-model.md`

**Version:** 1.0.0

---

# Purpose

This document defines the canonical error categories of the Finding Mapping Capability.

---

# Error Categories

| Category | Meaning | Outcome |
|----------|---------|---------|
| finding-unavailable | A referenced Finding did not resolve | partial |
| bounds-exhausted | Mapping bounds reached | partial |
| unmappable | A Finding lacks attributes required to map | partial |

---

# finding-unavailable

When a referenced Finding cannot be resolved, the capability SHALL produce a partial mapping over the
resolvable subset.

---

# bounds-exhausted

When mapping bounds are reached, the capability SHALL finalize a partial mapping.

---

# unmappable

When a Finding lacks the attributes required to map to a framework, the capability SHALL record it as
unmapped rather than inventing a mapping.

---

# Determinism

Identical error conditions SHALL yield identical categories and outcomes.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [configuration.md](configuration.md)
