# Log Collection Error Model

**File:** `skills/evidence/log-collection/error-model.md`

**Version:** 1.0.0

---

# Purpose

This document defines the canonical error categories of the Log Collection Capability.

---

# Error Categories

| Category | Meaning | Outcome |
|----------|---------|---------|
| unauthorized-source | Source outside authorized sources or Scope | rejected |
| bounds-exhausted | Collection bounds reached | partial |
| read-error | Logging package could not read a source | retry-or-partial |
| promotion-error | Shared Evidence lifecycle could not promote the collection | partial |

---

# unauthorized-source

When a source is outside authorized sources or [Scope](../../../schemas/scope.md), the capability
SHALL reject collection from that source.

---

# bounds-exhausted

When collection bounds are reached, the capability SHALL finalize a partial collection.

---

# read-error

When the shared [Logging](../../shared/logging/README.md) package cannot read a source, the
capability MAY retry within limits; persistent failure SHALL yield a partial result.

---

# promotion-error

When the shared [Evidence](../../shared/evidence/README.md) lifecycle cannot promote the collection,
the capability SHALL return a partial result retaining the Artifact reference.

---

# Determinism

Identical error conditions SHALL yield identical categories and outcomes.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [configuration.md](configuration.md)
