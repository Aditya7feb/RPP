# Evidence Bundle Error Model

**File:** `skills/reporting/evidence-bundle/error-model.md`

**Version:** 1.0.0

---

# Purpose

This document defines the canonical error categories of the Evidence Bundle Capability.

---

# Error Categories

| Category | Meaning | Outcome |
|----------|---------|---------|
| evidence-unavailable | A referenced Evidence object did not resolve | partial |
| integrity-failed | Integrity verification failed for an Evidence object | partial |
| bounds-exhausted | Bundle bounds reached | partial |
| assembly-error | The shared Reporting package could not assemble the bundle | partial |

---

# evidence-unavailable

When a referenced Evidence object cannot be resolved, the capability SHALL assemble a partial bundle
over the resolvable subset.

---

# integrity-failed

When integrity verification fails for an Evidence object, the capability SHALL exclude that object
and record the integrity failure in the bundle metadata.

---

# bounds-exhausted

When bundle bounds are reached, the capability SHALL finalize a partial bundle.

---

# assembly-error

When the shared [Reporting](../../shared/reporting/README.md) package cannot assemble the bundle, the
capability SHALL return a partial result.

---

# Determinism

Identical error conditions SHALL yield identical categories and outcomes.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [configuration.md](configuration.md)
