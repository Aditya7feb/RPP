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
target: grpc://api.example.com:443
assets:
  - asset-api-3001
  - asset-service-3002
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-grpc-5001
    title: Server reflection enabled in production, disclosing services and methods
    weakness: CWE-200
    owasp_api: API8:2023 - Security Misconfiguration
    risk_ref: risk-grpc-3001
    evidence_refs:
      - evidence-grpc-7001
observations:
  - id: obs-grpc-4001
    kind: reflection-analysis
evidence:
  - id: evidence-grpc-7001
    observation_ref: obs-grpc-4001
status: completed
metrics:
  methods_tested: 6
  findings: 1
```

Server reflection answers in a production environment, disclosing service and method
detail that should not be exposed.

---

# Example 2 — Broken Function Level Authorization

## Request

```yaml
target: grpc://api.example.com:443
assets:
  - asset-api-3001
identities_ref: grpc-test-identities
descriptor_ref: descriptor-example
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-grpc-5002
    title: Administrative method callable by low-privilege identity
    weakness: CWE-285
    owasp_api: API5:2023 - Broken Function Level Authorization
    risk_ref: risk-grpc-3002
    evidence_refs:
      - evidence-grpc-7002
observations:
  - id: obs-grpc-4002
    kind: method-authorization-analysis
evidence:
  - id: evidence-grpc-7002
    observation_ref: obs-grpc-4002
status: completed
metrics:
  methods_tested: 6
  findings: 1
```

A single controlled invocation with the low-privilege identity confirms that an
administrative method is callable. No further methods are enumerated.

---

# Example 3 — Missing Message-Size Limit

## Request

```yaml
target: grpc://api.example.com:443
assets:
  - asset-api-3001
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-grpc-5003
    title: No message-size limit on unary method
    weakness: CWE-770
    owasp_api: API4:2023 - Unrestricted Resource Consumption
    risk_ref: risk-grpc-3003
    evidence_refs:
      - evidence-grpc-7003
status: completed
metrics:
  methods_tested: 6
  findings: 1
```

Bounded, incrementally larger messages within the configured ceiling show no
message-size limit, indicating unrestricted resource consumption. The probe remains
bounded and does not deny service.

---

# Example 4 — Requires Approval

## Request

```yaml
target: grpc://api.example.com:443
assets:
  - asset-api-3001
identities_ref: grpc-test-identities
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

The Rules of Engagement require approval before active object-level authorization
testing; the skill defers until approval is granted.

---

# Example 5 — Inconclusive Transport Signal

## Request

```yaml
target: grpc://api.example.com:443
assets:
  - asset-api-3001
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings: []
observations:
  - id: obs-grpc-4005
    kind: transport-analysis
evidence:
  - id: evidence-grpc-7005
    observation_ref: obs-grpc-4005
status: completed
metrics:
  methods_tested: 1
  findings: 0
```

The transport signal is ambiguous, so the skill records an inconclusive Observation
rather than emitting a Finding.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
