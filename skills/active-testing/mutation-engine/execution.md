# Mutation Engine Execution

**File:** `skills/active-testing/mutation-engine/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the deterministic execution model of the Mutation Engine Capability.

---

# Execution Stages

```
Stage 1  Resolve Base And Strategies
Stage 2  Apply Mutations (bounded)
Stage 3  Record Lineage
Stage 4  Preserve Safety Markers
Stage 5  Emit Payloads And Metrics
```

---

# Stage 1 — Resolve Base And Strategies

The capability SHALL resolve `base_payload_ref` and the requested strategies.

---

# Stage 2 — Apply Mutations (bounded)

The capability SHALL apply strategies deterministically using `seed`, producing at most
`max_variants` variants.

---

# Stage 3 — Record Lineage

The capability SHALL record `lineage.source` `mutated`, `base_payload_id`, and
`mutation_ref` on each variant.

---

# Stage 4 — Preserve Safety Markers

The capability SHALL preserve `safety.non_destructive` and set `requires_approval` where a
mutation could alter target state.

---

# Stage 5 — Emit Payloads And Metrics

The capability SHALL emit derived [Payloads](../../../schemas/payload.md) and
[Metrics](../../../schemas/metrics.md).

---

# Determinism

Given identical base, strategies, bounds, and seed, the capability SHALL produce identical
variants.

---

# Idempotence

Mutation SHALL NOT alter any target or the base Payload.

---

# Related Documents

- [interface.md](interface.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
- [examples.md](examples.md)
