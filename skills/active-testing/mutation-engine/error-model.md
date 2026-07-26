# Mutation Engine Error Model

**File:** `skills/active-testing/mutation-engine/error-model.md`

**Version:** 1.0.0

---

# Purpose

This document defines the canonical error categories of the Mutation Engine Capability.

---

# Error Categories

| Category | Meaning | Outcome |
|----------|---------|---------|
| unknown-base | `base_payload_ref` did not resolve | rejected |
| unknown-strategy | A requested strategy is not registered | rejected |
| bounds-invalid | `max_variants` invalid | rejected |
| seed-missing | Determinism requires a seed and none was provided | rejected |

---

# unknown-base

When `base_payload_ref` does not resolve, the capability SHALL reject the request.

---

# unknown-strategy

When a requested strategy is not registered, the capability SHALL reject the request.

---

# bounds-invalid

When `max_variants` is not a positive integer, the capability SHALL reject the request.

---

# seed-missing

When `require_seed` is enabled and no seed is provided, the capability SHALL reject the
request to preserve determinism.

---

# Determinism

Identical error conditions SHALL yield identical categories and outcomes.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [configuration.md](configuration.md)
