# Payload Generation Examples

**File:** `skills/active-testing/payload-generation/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the Payload Generation
Capability.

---

# Example 1 — Generate Encoded Traversal Payloads

## Request

```yaml
generate:
  template_ref: template-traversal-default
  seeds:
    wordlist_name: traversal-prefixes
    max_entries: 50
  mutation:
    strategies:
      - encoding
    max_variants: 4
    seed: 77
  encoding: url
  bounds:
    max_payloads: 200
```

## Response

```yaml
generate_result:
  payload_refs:
    - payload-4301
    - payload-4302
  payload_count: 200
  metrics_ref: metrics-9301
```

The capability composes URL-encoded traversal Payloads from seeds and mutations, each with
lineage and `safety.non_destructive: true`.

---

# Example 2 — Marker-Based Out-Of-Band Payloads

## Request

```yaml
generate:
  template_ref: template-oob-marker
  bounds:
    max_payloads: 10
```

## Response

```yaml
generate_result:
  payload_refs:
    - payload-4401
  payload_count: 10
  metrics_ref: metrics-9302
```

Each Payload references an out-of-band marker by reference; the marker value is never inlined.

---

# Example 3 — Unknown Template Rejected

## Request

```yaml
generate:
  template_ref: template-nonexistent
```

## Response

```yaml
generate_result:
  outcome: rejected
  reason: unknown-template
```

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
