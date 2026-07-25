# TLS Analysis Examples

**File:** `skills/discovery/tls-analysis/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-independent examples of the TLS
Analysis Skill in use.

Examples demonstrate policy-gated analysis, certificate-asset production, TLS
weakness findings, interception handling, partial results, and evidence.

All examples are illustrative and contain no implementation code.

---

# Example 1 — Analyze And Produce A Certificate Asset

The Recon Agent analyzes a TLS service.

## Invocation

```yaml
metadata:
  request_id: req-14001
  assessment_id: asmt-42
  task_id: task-tls-analysis
  skill_id: tls-analysis
target: https://app.example.com
service_asset_id: asset-0007
checks: [protocols, ciphers, certificate, validation]
scope_id: scope-asmt-42
roe_id: roe-asmt-42
```

## Result

```yaml
outcome: completed
assets:
  - asset-0020   # certificate for app.example.com
relationships:
  - assetrel-0044  # certificate serves service asset-0007
tls_summary:
  protocols: [TLS1.2, TLS1.3]
  weak_ciphers: []
  validation: valid
findings: []
```

The certificate is produced as a canonical Asset linked to its service.

---

# Example 2 — Deprecated Protocol Finding

The service offers a deprecated protocol version.

## Produced Finding

```yaml
finding_id: finding-tls-0021
title: Deprecated TLS protocol offered
category: Cryptography
severity: Medium
confidence: Verified
evidence:
  - evidence-tls-0021
```

## Produced Risk

```yaml
risk_id: risk-tls-0021
finding_id: finding-tls-0021
likelihood: { rating: Low }
impact: { rating: Medium }
score: { model: likelihood-impact, value: 4.8, severity: Medium }
```

The Finding references its Evidence; Risk scores it as a first-class object.

---

# Example 3 — Interception Boundary Honored

A testing proxy intercepts TLS; the reported boundary is not flagged.

## Result Fragment

```yaml
tls_summary:
  validation: intercepted
findings: []
notes: interception boundary honored; not reported as a certificate weakness
```

The legitimate interception boundary is honored, avoiding a spurious finding.

---

# Example 4 — Expired Certificate Finding

The certificate is expired.

## Produced Finding

```yaml
finding_id: finding-tls-0022
title: Expired TLS certificate
category: Cryptography
severity: High
confidence: Verified
evidence:
  - evidence-tls-0022
```

The expiry is confirmed from the certificate Asset and backed by Evidence.

---

# Example 5 — Denied Analysis

The Policy Engine denies analysis of an out-of-scope service.

## Decision

```yaml
decision: deny
scope_status: out_of_scope
```

No analysis is performed against the out-of-scope service.

---

# Example 6 — Partial Result

The certificate check succeeds while the cipher check fails.

## Result

```yaml
outcome: partial
assets: [ asset-0020 ]
errors:
  - category: Handshake
    target: https://app.example.com
    retryable: true
```

The failure of one check does not abort the others.

---

# Example 7 — Observation Record

A single analysis produces the following observation.

```yaml
observation:
  observation_id: obs-4001
  type: tls-certificate
  subject:
    target: https://app.example.com
    asset_id: asset-0020
  content:
    summary: Certificate valid; issued by trusted CA; expires in 20 days
    attributes:
      not_after: 2026-08-14T00:00:00Z
      issuer: Example CA
  confidence: High
  evidence:
    - evidence-tls-0020
```

The observation conforms to the canonical
[Observation schema](../../../schemas/observation.md) and is promoted to
[Evidence](../../../schemas/evidence.md).

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Execution](execution.md)
- [Error Model](error-model.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [TLS Client](../../shared/tls-client/README.md)
