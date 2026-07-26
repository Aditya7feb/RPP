# Payload Generation Error Model

**File:** `skills/active-testing/payload-generation/error-model.md`

**Version:** 1.0.0

---

# Purpose

This document defines the canonical error categories of the Payload Generation Capability.

---

# Error Categories

| Category | Meaning | Outcome |
|----------|---------|---------|
| unknown-template | `template_ref` did not resolve | rejected |
| seed-unavailable | Referenced wordlist did not resolve | partial |
| mutation-unavailable | Mutation strategy did not resolve | partial |
| bounds-invalid | `max_payloads` invalid | rejected |

---

# unknown-template

When `template_ref` does not resolve, the capability SHALL reject the request.

---

# seed-unavailable

When the referenced wordlist cannot be resolved, the capability SHALL produce a partial
result from available inputs.

---

# mutation-unavailable

When a mutation strategy cannot be resolved, the capability SHALL produce a partial result
without that strategy.

---

# bounds-invalid

When `max_payloads` is not a positive integer, the capability SHALL reject the request.

---

# Determinism

Identical error conditions SHALL yield identical categories and outcomes.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [configuration.md](configuration.md)
