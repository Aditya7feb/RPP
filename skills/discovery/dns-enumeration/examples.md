# DNS Enumeration Examples

**File:** `skills/discovery/dns-enumeration/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-independent examples of the DNS
Enumeration Skill in use.

Examples demonstrate policy-gated enumeration, asset production, weakness
findings, out-of-scope handling, partial results, and evidence.

All examples are illustrative and contain no implementation code.

---

# Example 1 — Enumerate And Produce Assets

The Recon Agent enumerates a target domain.

## Invocation

```yaml
metadata:
  request_id: req-12001
  assessment_id: asmt-42
  task_id: task-dns-enum
  skill_id: dns-enumeration
target: example.com
record_types: [A, AAAA, CNAME, MX, NS, TXT]
scope_id: scope-asmt-42
roe_id: roe-asmt-42
```

## Result

```yaml
outcome: completed
assets:
  - asset-0001   # domain example.com
  - asset-0002   # host 93.184.216.34
relationships:
  - assetrel-0010  # example.com resolves-to 93.184.216.34
observations:
  - obs-2001
findings: []
```

Each Asset carries provenance to its Observation and Evidence and a
`scope_status` of `in_scope`.

---

# Example 2 — Policy Gate Allows Passive Query

Before querying, the skill consults the Policy Engine.

## Decision

```yaml
decision: allow
scope_status: in_scope
rate_ceiling_policy_id: ratelimitpolicy-roe-ceiling
```

The passive record query proceeds within the attached rate ceiling.

---

# Example 3 — Zone Transfer Finding

Zone-transfer testing (an active action) is permitted and succeeds against a
misconfigured name server.

## Produced Finding

```yaml
finding_id: finding-dns-0007
title: DNS zone transfer permitted
category: Misconfiguration
severity: Medium
confidence: Verified
evidence:
  - evidence-dns-0007
```

## Produced Risk

```yaml
risk_id: risk-dns-0007
finding_id: finding-dns-0007
likelihood: { rating: Medium }
impact: { rating: Medium }
score: { model: likelihood-impact, value: 5.3, severity: Medium }
```

The Finding references its Evidence; the Risk scores it as a first-class object.

---

# Example 4 — Out-Of-Scope Name Recorded, Not Queried

Enumeration discovers a name outside scope.

## Result Fragment

```yaml
assets:
  - asset_id: asset-0050
    type: subdomain
    value: status.example.com
    scope_status: out_of_scope
```

The out-of-scope Asset is recorded for completeness but SHALL NOT be queried.

---

# Example 5 — Denied Action

The Policy Engine denies an active query outside the maintenance window.

## Result Fragment

```yaml
outcome: partial
denied_actions:
  - target: example.com
    action_class: zone-transfer
    reason: outside maintenance window
```

The denial is recorded as evidence; passive enumeration continues.

---

# Example 6 — Partial Result

One name fails resolution while others succeed.

## Result

```yaml
outcome: partial
assets: [ asset-0001, asset-0002 ]
errors:
  - category: Resolution
    target: mail.example.com
    retryable: true
```

The failure of one name does not abort enumeration of others.

---

# Example 7 — Observation And Evidence Record

A single result produces the following observation.

```yaml
observation:
  observation_id: obs-2001
  type: dns-record
  subject:
    target: example.com
    asset_id: asset-0001
  content:
    summary: A record resolved to 93.184.216.34
    attributes:
      record_type: A
      value: 93.184.216.34
  confidence: High
  evidence:
    - evidence-dns-0001
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
- [DNS Client](../../shared/dns-client/README.md)
