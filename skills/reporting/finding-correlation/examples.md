# Finding Correlation Examples

**File:** `skills/reporting/finding-correlation/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the Finding Correlation
Capability.

---

# Example 1 — Deduplicate And Chain

## Request

```yaml
correlate:
  finding_refs:
    - finding-xss-5001
    - finding-xss-5002
    - finding-idor-5010
  correlation:
    deduplicate: true
    relate: true
    build_chains: true
  bounds:
    max_findings: 500
```

## Response

```yaml
correlate_result:
  correlation_ref: correlation-rp-9001
  deduplicated_groups:
    - group: reflected-xss-login
      findings:
        - finding-xss-5001
        - finding-xss-5002
  related_links:
    - from: finding-idor-5010
      to: finding-xss-5001
      relation: shared-target
  attack_chains:
    - chain: account-takeover
      steps:
        - finding-idor-5010
        - finding-xss-5001
  metrics_ref: metrics-rp-7001
```

The capability deduplicates two XSS Findings and constructs an attack chain, referencing Findings by
identifier without modifying them.

---

# Example 2 — Partial On Missing Finding

## Request

```yaml
correlate:
  finding_refs:
    - finding-xss-5001
    - finding-missing-0000
```

## Response

```yaml
correlate_result:
  correlation_ref: correlation-rp-9002
  deduplicated_groups: []
  metrics_ref: metrics-rp-7002
```

One referenced Finding could not be resolved, so the capability produces a partial correlation over
the resolvable subset.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
