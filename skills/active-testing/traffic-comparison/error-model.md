# Traffic Comparison Error Model

**File:** `skills/active-testing/traffic-comparison/error-model.md`

**Version:** 1.0.0

---

# Purpose

This document defines the canonical error categories of the Traffic Comparison Capability.

---

# Error Categories

| Category | Meaning | Outcome |
|----------|---------|---------|
| recording-unavailable | A referenced recording did not resolve | rejected |
| incompatible-recordings | Recordings cannot be aligned | partial |
| bounds-exhausted | Comparison bounds reached | partial |
| storage-error | Difference Artifact could not be written | partial |

---

# recording-unavailable

When a referenced recording cannot be resolved, the capability SHALL reject the request.

---

# incompatible-recordings

When recordings cannot be aligned, the capability SHALL produce a partial difference over the
alignable subset.

---

# bounds-exhausted

When comparison bounds are reached, the capability SHALL finalize a partial difference.

---

# storage-error

When the difference Artifact cannot be written, the capability SHALL return a partial result.

---

# Determinism

Identical error conditions SHALL yield identical categories and outcomes.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [configuration.md](configuration.md)
