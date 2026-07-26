# Report Generation Error Model

**File:** `skills/reporting/report-generation/error-model.md`

**Version:** 1.0.0

---

# Purpose

This document defines the canonical error categories of the Report Generation Capability.

---

# Error Categories

| Category | Meaning | Outcome |
|----------|---------|---------|
| input-unavailable | A referenced canonical object or content did not resolve | partial |
| template-unavailable | The referenced template did not resolve | rejected |
| unsupported-format | A requested format is not supported | partial |
| serialization-error | The shared Reporting package could not serialize a format | partial |

---

# input-unavailable

When a referenced canonical object or content cannot be resolved, the capability SHALL generate a
partial report over the resolvable inputs.

---

# template-unavailable

When the referenced template cannot be resolved, the capability SHALL reject the request.

---

# unsupported-format

When a requested format is not supported by the shared Reporting package, the capability SHALL omit
that format and produce the remaining serializations.

---

# serialization-error

When the shared [Reporting](../../shared/reporting/README.md) package cannot serialize a format, the
capability SHALL return a partial result with the remaining serializations.

---

# Determinism

Identical error conditions SHALL yield identical categories and outcomes.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [configuration.md](configuration.md)
