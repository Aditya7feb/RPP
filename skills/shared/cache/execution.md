# Cache Execution Model

**File:** `skills/shared/cache/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the execution model for the Cache Shared Skill.

The execution model describes how the shared skill processes a cache request
from key derivation through lookup, revalidation, storage, and result
propagation.

The model is deterministic given the same configuration, cache state, and
inputs.

---

# Execution Overview

```
Receive Invocation

↓

Resolve Configuration

↓

Derive Key

↓

Lookup Entry In Scope

↓

Evaluate Freshness

↓

Serve / Revalidate / Produce

↓

Store If Cacheable

↓

Emit Evidence and Events

↓

Return Result
```

---

# Stage 1 — Configuration Resolution

The Cache Shared Skill SHALL resolve namespace, freshness, scope, and eviction
settings using the precedence defined in [configuration.md](configuration.md).

---

# Stage 2 — Key Derivation

The Cache Shared Skill SHALL derive a deterministic key from the normalized
parameters, producing the `parameters_digest` defined in the
[Cache Entry schema](../../../schemas/cache-entry.md).

Secret material SHALL NOT contribute to the key.

---

# Stage 3 — Scoped Lookup

The Cache Shared Skill SHALL look up an entry by key within the resolved scope.

An entry outside the resolved scope SHALL NOT be considered a match.

---

# Stage 4 — Freshness Evaluation

The Cache Shared Skill SHALL classify the lookup.

```
current_time < expires_at → Fresh Hit

expires_at <= current_time < expires_at + stale_while_revalidate → Stale Hit

otherwise → Miss
```

---

# Stage 5 — Serve, Revalidate, Or Produce

```
Fresh Hit → Return Cached Value

Stale Hit
  ├── allow_stale → Return Stale + Trigger Revalidation
  └── else        → Revalidate Or Treat As Miss

Miss → Invoke Producer
```

---

# Stage 6 — Revalidation

Where revalidation is requested and validators are present, the Cache Shared
Skill SHALL invoke the producer with validators.

- A confirmation SHALL refresh entry freshness without re-storing the value
- A fresh value SHALL replace the entry subject to cacheability

---

# Stage 7 — Production On Miss

On a miss, the Cache Shared Skill SHALL invoke the caller-provided producer
exactly once.

The Cache Shared Skill SHALL NOT inspect or modify the producer implementation.

---

# Stage 8 — Storage

The Cache Shared Skill SHALL store the produced value as a
[Cache Entry](../../../schemas/cache-entry.md) only when

- The caller declares the result `cacheable`
- The value contains no secrets
- The operation is deterministic

Otherwise the value SHALL be returned uncached.

---

# Stage 9 — Eviction

The Cache Shared Skill SHALL evict entries when occupancy reaches the configured
high watermark, stopping at the low watermark, following the eviction policy.

Expired entries beyond any revalidation window SHALL be evicted.

---

# Stage 10 — Evidence and Events

The Cache Shared Skill SHOULD emit lookup evidence and lifecycle events
according to configuration. Evidence SHALL exclude cached secrets.

---

# Determinism

Given identical configuration, cache state, and inputs, the Cache Shared Skill
SHALL produce identical lookup decisions and identical keys.

---

# Concurrency

The Cache Shared Skill SHALL coordinate concurrent lookups for the same key so
that a single producer invocation satisfies multiple concurrent misses where
practical, preventing redundant production.

Concurrent revalidation SHALL NOT serve inconsistent values within a scope.

---

# Interaction With Other Shared Skills

- Producers that perform outbound operations SHOULD route through the
  [Rate Limiter](../rate-limiter/README.md) and, where applicable, the
  [Proxy](../proxy/README.md) shared skill.
- Cache misses that fail SHOULD be recovered through the
  [Retry](../retry/README.md) shared skill within the producer.

---

# Failure Handling

Execution failures SHALL be classified according to
[error-model.md](error-model.md).

A producer failure SHALL NOT store a partial or failed value.

A cache backend failure SHALL degrade to a miss so that correctness is preserved
even when caching is unavailable.

---

# Execution Outputs

The execution model SHALL produce

- A normalized cache result
- A lookup decision
- Cache metrics
- Evidence references

Outputs SHALL remain implementation independent.

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Error Model](error-model.md)
- [Cache Entry Schema](../../../schemas/cache-entry.md)
- [Execution Model](../../core/execution-model.md)
