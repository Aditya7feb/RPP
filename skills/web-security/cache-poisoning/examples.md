# Web Cache Poisoning Examples

**File:** `skills/web-security/cache-poisoning/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the Web Cache
Poisoning Skill. Examples illustrate the interface and outputs; they contain no
implementation code.

---

# Example 1 — Unkeyed Header Reflected Into Cache

## Request

```yaml
target: https://app.example.com
marker_ref: benign-cache-marker
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-cp-5001
    title: Unkeyed header reflected into a cached response
    weakness: CWE-444
    risk_ref: risk-cp-3001
    evidence_refs:
      - evidence-cp-7001
observations:
  - id: obs-cp-4001
    kind: cache-reflection-analysis
evidence:
  - id: evidence-cp-7001
    observation_ref: obs-cp-4001
status: completed
metrics:
  endpoints_tested: 3
  findings: 1
```

An unkeyed request header influences the response and is served from the cache under a
controlled cache key, confirming cache poisoning without affecting real users.

---

# Example 2 — Influential Input Omitted From Cache Key

## Request

```yaml
target: https://app.example.com
marker_ref: benign-cache-marker
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-cp-5002
    title: Security-relevant input omitted from cache key
    weakness: CWE-444
    risk_ref: risk-cp-3002
    evidence_refs:
      - evidence-cp-7002
status: completed
metrics:
  endpoints_tested: 3
  findings: 1
```

An input that changes the response is excluded from the cache key, enabling a poisoned
entry to be served, confirmed under a controlled cache key.

---

# Example 3 — Requires Approval

## Request

```yaml
target: https://app.example.com
marker_ref: benign-cache-marker
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings: []
status: awaiting_approval
metrics:
  approvals_requested: 1
```

Cache-poisoning testing is higher impact; the Rules of Engagement require approval, so
the skill defers until approval is granted.

---

# Example 4 — Policy Denial

## Request

```yaml
target: https://out-of-scope.example.net
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings: []
status: denied
metrics:
  policy_denials: 1
```

The target is out of scope. The Policy Engine denies the action and no testing is
performed.

---

# Related Documents

- [Interface](interface.md)
- [Execution](execution.md)
- [Configuration](configuration.md)
- [Error Model](error-model.md)
- [HTTP Header Schema](../../../schemas/http-header.md)
