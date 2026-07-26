# Payload Generation Execution

**File:** `skills/active-testing/payload-generation/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the deterministic execution model of the Payload Generation Capability.

---

# Execution Stages

```
Stage 1  Resolve Template And Inputs
Stage 2  Compose Seeds
Stage 3  Derive Variants
Stage 4  Apply Encoding
Stage 5  Mark Safety
Stage 6  Emit Payloads And Metrics
```

---

# Stage 1 — Resolve Template And Inputs

The capability SHALL resolve `template_ref` and validate seed and mutation references.

---

# Stage 2 — Compose Seeds

The capability SHALL draw bounded candidate values from
[Wordlists](../wordlists/README.md) and bind them into Payloads.

---

# Stage 3 — Derive Variants

The capability SHALL derive variants through the
[Mutation Engine](../mutation-engine/README.md), preserving lineage.

---

# Stage 4 — Apply Encoding

The capability SHALL apply the requested encoding and record it in
`classification.encoding`.

---

# Stage 5 — Mark Safety

The capability SHALL set `safety.non_destructive` and `safety.requires_approval` and
reference markers and out-of-band values rather than inlining them.

---

# Stage 6 — Emit Payloads And Metrics

The capability SHALL emit generated [Payloads](../../../schemas/payload.md) and
[Metrics](../../../schemas/metrics.md), bounded by `max_payloads`.

---

# Determinism

Given identical template, seeds, mutation seed, and bounds, the capability SHALL produce
identical Payloads.

---

# Idempotence

Generation SHALL NOT alter any target.

---

# Related Documents

- [interface.md](interface.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
- [examples.md](examples.md)
