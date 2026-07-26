# gRPC API Security Skill Examples

**File:** `skills/api-security/grpc/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the gRPC API
Security Skill. Identifiers are stable and illustrative.

---

# Example 1 — Reflection Enabled In Production

## Request

```yaml
assess:
  target: grpc://api.example.com:443
  assets:
    - asset-api-3001
    - asset-service-3002
  scope_id: scope-2201
  roe_id: roe-2201
  options:
    check_reflection: true
```

## Result

```yaml
assess_result:
  target: grpc://api.example.com:443
  findings:
    - finding-grpc-4001
  evidence_refs:
    - evidence-grpc-5001
  decision_summary:
    allow: 2
    denied: 0
```

## Finding

```yaml
finding-grpc-4001:
  weakness: CWE-200
  owasp_api: "API8:2023 - Security Misconfiguration"
  title: Server reflection enabled in production
  asset: asset-api-3001
  risk:
    severity: medium
  evidence:
    - evidence-grpc-5001
```

---

# Example 2 — Broken Function Level Authorization

## Request

```yaml
assess:
  target: grpc://api.example.com:443
  assets:
    - asset-api-3001
  identities_ref: identities-set-2201
  descriptor_ref: descriptor-2201
  scope_id: scope-2201
  roe_id: roe-2201
  options:
    check_method_authorization: true
```

## Result

```yaml
assess_result:
  target: grpc://api.example.com:443
  findings:
    - finding-grpc-4002
  evidence_refs:
    - evidence-grpc-5002
  decision_summary:
    allow: 3
    denied: 0
```

## Finding

```yaml
finding-grpc-4002:
  weakness: CWE-285
  owasp_api: "API5:2023 - Broken Function Level Authorization"
  title: Administrative method callable by low-privilege identity
  asset: asset-api-3001
  risk:
    severity: high
  evidence:
    - evidence-grpc-5002
  notes: >
    Confirmed with a single controlled invocation. No further methods were
    enumerated.
```

---

# Example 3 — Missing Message-Size Limit

## Request

```yaml
assess:
  target: grpc://api.example.com:443
  assets:
    - asset-api-3001
  scope_id: scope-2201
  roe_id: roe-2201
  options:
    check_resource_consumption: true
```

## Result

```yaml
assess_result:
  target: grpc://api.example.com:443
  findings:
    - finding-grpc-4003
  evidence_refs:
    - evidence-grpc-5003
  decision_summary:
    allow: 4
    denied: 0
```

## Finding

```yaml
finding-grpc-4003:
  weakness: CWE-770
  owasp_api: "API4:2023 - Unrestricted Resource Consumption"
  title: No message-size limit on unary method
  asset: asset-api-3001
  risk:
    severity: medium
  evidence:
    - evidence-grpc-5003
  notes: >
    Confirmed with bounded, incrementally larger messages within the configured
    ceiling. No denial of service was induced.
```

---

# Example 4 — Deferred For Approval

## Request

```yaml
assess:
  target: grpc://api.example.com:443
  assets:
    - asset-api-3001
  identities_ref: identities-set-2201
  scope_id: scope-2201
  roe_id: roe-2201
  options:
    check_object_authorization: true
```

## Result

```yaml
assess_result:
  target: grpc://api.example.com:443
  findings: []
  evidence_refs:
    - evidence-grpc-5004
  decision_summary:
    allow: 0
    awaiting_approval: 1
```

Object-level authorization testing required approval and was deferred rather than
executed.

---

# Example 5 — Inconclusive Transport Signal

## Result

```yaml
assess_result:
  target: grpc://api.example.com:443
  findings: []
  evidence_refs:
    - evidence-grpc-5005
  observations:
    - observation-grpc-6005
  decision_summary:
    allow: 1
    denied: 0
```

The transport signal was ambiguous, so the skill recorded an inconclusive Observation
rather than emitting a Finding.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
