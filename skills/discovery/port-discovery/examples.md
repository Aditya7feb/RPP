# Port Discovery Examples

**File:** `skills/discovery/port-discovery/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-independent examples of the Port
Discovery Skill in use.

Examples demonstrate policy-gated probing, service-asset production, exposure
findings, out-of-scope handling, partial results, and evidence.

All examples are illustrative and contain no implementation code.

---

# Example 1 — Probe And Produce Service Assets

The Recon Agent probes a host for common TCP services.

## Invocation

```yaml
metadata:
  request_id: req-13001
  assessment_id: asmt-42
  task_id: task-port-disc
  skill_id: port-discovery
target: 93.184.216.34
ports: common-services
protocols: [tcp]
scope_id: scope-asmt-42
roe_id: roe-asmt-42
```

## Result

```yaml
outcome: completed
assets:
  - asset-0007   # service https on :443
  - asset-0008   # service ssh on :22
relationships:
  - assetrel-0031  # host exposes service :443
observations:
  - obs-3001
  - obs-3002
findings: []
```

Open ports yield `service` Assets linked to the host by `exposes` relationships.

---

# Example 2 — Policy Gate For Active Probe

Port probing is an active action; the skill consults the Policy Engine.

## Decision

```yaml
decision: allow
scope_status: in_scope
rate_ceiling_policy_id: ratelimitpolicy-roe-ceiling
```

Probing proceeds within the attached rate ceiling.

---

# Example 3 — Exposure Finding

An administrative service is exposed to an untrusted network.

## Produced Finding

```yaml
finding_id: finding-exposure-0008
title: Administrative service exposed to untrusted network
category: Exposure
severity: High
confidence: Verified
evidence:
  - evidence-tcp-0008
```

## Produced Risk

```yaml
risk_id: risk-exposure-0008
finding_id: finding-exposure-0008
likelihood: { rating: Medium }
impact: { rating: High }
score: { model: likelihood-impact, value: 7.1, severity: High }
```

The Finding references its Evidence; Risk scores it as a first-class object.

---

# Example 4 — Out-Of-Scope Host Denied

An action targets a host outside scope.

## Decision

```yaml
decision: deny
scope_status: out_of_scope
```

No probe is issued against the out-of-scope host.

---

# Example 5 — Denied Outside Maintenance Window

Active probing is requested outside the permitted window.

## Result Fragment

```yaml
outcome: partial
denied_actions:
  - target: 93.184.216.34
    reason: outside maintenance window
```

The denial is recorded; probing resumes within the window.

---

# Example 6 — Partial Result

Some ports fail to probe while others succeed.

## Result

```yaml
outcome: partial
assets: [ asset-0007 ]
errors:
  - category: Probe
    target: 93.184.216.34
    port: 3306
    retryable: true
```

The failure of one port does not abort probing of others.

---

# Example 7 — Observation Record

A single probe produces the following observation.

```yaml
observation:
  observation_id: obs-3001
  type: open-port
  subject:
    target: 93.184.216.34:443
    asset_id: asset-0007
  content:
    summary: TCP port 443 open; TLS service responded
    attributes:
      protocol: tcp
      port: 443
      state: open
  confidence: High
  evidence:
    - evidence-tcp-0007
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
- [TCP Client](../../shared/tcp-client/README.md)
