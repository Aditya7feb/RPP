# Cache Error Model

**File:** `skills/shared/cache/error-model.md`

**Version:** 1.0.0

---

# Purpose

This document defines the error model for the Cache Shared Skill.

The error model classifies the failure conditions the shared skill MAY produce
and aligns them with
[the platform error handling model](../../core/error-handling.md).

All errors SHALL be normalized and implementation independent.

---

# Error Philosophy

The Cache Shared Skill SHALL

- Produce canonical, structured errors
- Degrade safely to a miss when caching is unavailable
- Preserve correctness over cache availability
- Never leak cached secrets

---

# Error Categories

The Cache Shared Skill maps its failures onto the canonical categories.

```
Configuration

Validation

Storage

Producer

Adapter

Internal
```

---

# Configuration Errors

Raised when configuration is invalid or incomplete.

Conditions

- A referenced namespace does not exist
- `low_watermark` is not less than `high_watermark`
- An invalid eviction policy is configured

Configuration errors SHALL be non-retryable.

---

# Validation Errors

Raised when an invocation is malformed.

Conditions

- Missing key components
- Secret material present in parameters
- Missing producer callback

Validation errors SHALL be non-retryable.

---

# Storage Errors

Raised when an entry cannot be stored or retrieved.

Conditions

- Value exceeds namespace `max_bytes`
- Backend rejects the entry

Storage errors SHALL degrade to a miss for retrieval and SHALL return the
produced value uncached for storage, preserving correctness.

---

# Producer Errors

Raised when the caller-provided producer fails on a miss.

Producer errors SHALL be propagated using the producer's canonical error.

Producer errors MAY be retryable subject to the caller policy.

---

# Adapter Errors

Raised when an underlying cache backend fails unexpectedly.

Adapter errors SHALL be normalized and SHALL degrade to a miss so that
correctness is preserved.

---

# Internal Errors

Raised for unexpected conditions within the Cache Shared Skill.

Internal errors SHALL be treated as non-retryable and SHOULD be reported for
diagnosis.

---

# Error Structure

Every error SHALL conform to the canonical error structure.

```yaml
category:

code:

message:

retryable:

namespace:

scope:
```

`category` SHALL be one of the canonical categories.

`retryable` SHALL indicate whether the operation MAY be attempted again.

Errors SHALL NOT contain cached secrets.

---

# Outcome Mapping

| Outcome | Category | Retryable |
|---------|----------|-----------|
| namespace_missing | Configuration | No |
| invalid_key | Validation | No |
| secret_in_parameters | Validation | No |
| value_too_large | Storage | No (uncached) |
| backend_unavailable | Adapter | Degrades to miss |
| producer_failed | Producer | Policy dependent |
| unexpected | Internal | No |

---

# Degradation Principle

Cache failures SHALL NOT cause operation failures on their own.

When the cache is unavailable, the Cache Shared Skill SHALL behave as a miss so
that the producer still yields a correct result.

Only a failing producer SHALL cause the overall invocation to fail.

---

# Evidence

Errors SHOULD be captured as evidence conforming to the
[Evidence schema](../../../schemas/evidence.md), including the category,
namespace, and scope, and SHALL exclude cached secrets.

---

# Related Documents

- [Interface](interface.md)
- [Execution](execution.md)
- [Error Handling Model](../../core/error-handling.md)
- [Cache Entry Schema](../../../schemas/cache-entry.md)
