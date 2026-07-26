# Wordlists Error Model

**File:** `skills/active-testing/wordlists/error-model.md`

**Version:** 1.0.0

---

# Purpose

This document defines the canonical error categories of the Wordlists Capability.

---

# Error Categories

| Category | Meaning | Outcome |
|----------|---------|---------|
| unknown-list | `list_name` not registered | rejected |
| empty-selection | Filter matched no entries | empty |
| bounds-invalid | `max_entries` invalid | rejected |
| artifact-store-error | Artifact could not be stored | partial |

---

# unknown-list

When `list_name` does not resolve, the capability SHALL reject the request.

---

# empty-selection

When the filter matches no entries, the capability SHALL return an empty result with
metrics.

---

# bounds-invalid

When `max_entries` is not a positive integer, the capability SHALL reject the request.

---

# artifact-store-error

When an Artifact cannot be stored, the capability SHALL return a partial result and MAY
provide seeds instead.

---

# Determinism

Identical error conditions SHALL yield identical categories and outcomes.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [configuration.md](configuration.md)
