# Wordlists Examples

**File:** `skills/active-testing/wordlists/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the Wordlists Capability.

---

# Example 1 — Select Paths As An Artifact

## Request

```yaml
select:
  list_name: common-web-paths
  selection:
    filter:
      max_length: 32
    max_entries: 500
  emit:
    as_artifact: true
```

## Response

```yaml
select_result:
  list_name: common-web-paths
  list_version: 1.4.0
  entry_count: 500
  artifact_ref: artifact-8101
  metrics_ref: metrics-9101
```

The capability returns a bounded selection of web paths by reference as an Artifact.

---

# Example 2 — Emit Parameter Names As Seeds

## Request

```yaml
select:
  list_name: common-parameters
  selection:
    max_entries: 100
  emit:
    as_seeds: true
```

## Response

```yaml
select_result:
  list_name: common-parameters
  list_version: 2.0.0
  entry_count: 100
  seed_refs:
    - payload-seed-4101
    - payload-seed-4102
  metrics_ref: metrics-9102
```

The capability emits parameter-name candidates as Payload seeds with `lineage.source`
`wordlist`.

---

# Example 3 — Unknown List Rejected

## Request

```yaml
select:
  list_name: nonexistent-list
```

## Response

```yaml
select_result:
  outcome: rejected
  reason: unknown-list
```

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
