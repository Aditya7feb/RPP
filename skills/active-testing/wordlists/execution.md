# Wordlists Execution

**File:** `skills/active-testing/wordlists/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the deterministic execution model of the Wordlists Capability.

---

# Execution Stages

```
Stage 1  Resolve List
Stage 2  Apply Selection And Filter
Stage 3  Bounded Sampling
Stage 4  Emit Artifact Or Seeds
Stage 5  Emit Metrics
```

---

# Stage 1 — Resolve List

The capability SHALL resolve `list_name` to a registered list version.

---

# Stage 2 — Apply Selection And Filter

The capability SHALL apply the requested filter criteria to the list entries.

---

# Stage 3 — Bounded Sampling

The capability SHALL sample at most `max_entries` entries, deterministically given identical
inputs.

---

# Stage 4 — Emit Artifact Or Seeds

The capability SHALL emit the selected content as an
[Artifact](../../../schemas/artifact.md) or as [Payload](../../../schemas/payload.md) seeds
per the request.

---

# Stage 5 — Emit Metrics

The capability SHALL emit [Metrics](../../../schemas/metrics.md) describing selection counts.

---

# Determinism

Given identical list version, filter, and bounds, the capability SHALL produce identical
output.

---

# Idempotence

Selection SHALL NOT alter any target or list content.

---

# Related Documents

- [interface.md](interface.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
- [examples.md](examples.md)
