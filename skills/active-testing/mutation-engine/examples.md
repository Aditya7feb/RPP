# Mutation Engine Examples

**File:** `skills/active-testing/mutation-engine/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the Mutation Engine
Capability.

---

# Example 1 — Encoding And Boundary Variants

## Request

```yaml
mutate:
  base_payload_ref: payload-4001
  strategies:
    - encoding
    - boundary
  bounds:
    max_variants: 20
  seed: 4242
```

## Response

```yaml
mutate_result:
  base_payload_ref: payload-4001
  variant_refs:
    - payload-4101
    - payload-4102
  variant_count: 20
  metrics_ref: metrics-9201
```

The capability produces 20 deterministic variants with lineage referencing `payload-4001`.

---

# Example 2 — Destructive Mutation Marked For Approval

## Request

```yaml
mutate:
  base_payload_ref: payload-4500
  strategies:
    - structural
  bounds:
    max_variants: 5
  seed: 11
```

## Response

```yaml
mutate_result:
  base_payload_ref: payload-4500
  variant_refs:
    - payload-4600
  variant_count: 5
  metrics_ref: metrics-9202
```

A structural mutation that could alter target state carries `safety.requires_approval: true`
so downstream delivery is gated by the Policy Engine.

---

# Example 3 — Missing Seed Rejected

## Request

```yaml
mutate:
  base_payload_ref: payload-4001
  strategies:
    - case
```

## Response

```yaml
mutate_result:
  outcome: rejected
  reason: seed-missing
```

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
