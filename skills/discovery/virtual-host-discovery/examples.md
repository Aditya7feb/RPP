# Virtual Host Discovery Examples

**File:** `skills/discovery/virtual-host-discovery/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-independent examples of the
Virtual Host Discovery Skill in use.

Examples demonstrate baseline establishment, policy-gated probing, differential
detection, virtual-host-asset production, hidden-host findings, and evidence.

All examples are illustrative and contain no implementation code.

---

# Example 1 — Discover A Virtual Host

The Recon Agent probes candidate host names against an address.

## Invocation

```yaml
metadata:
  request_id: req-18001
  assessment_id: asmt-42
  task_id: task-vhost
  skill_id: virtual-host-discovery
target_address: 93.184.216.34
host_candidates_ref: wordlist-vhosts
base_scheme: [https]
scope_id: scope-asmt-42
roe_id: roe-asmt-42
```

## Result

```yaml
outcome: completed
assets:
  - asset-0080   # web-application admin.example.com on 93.184.216.34
relationships:
  - assetrel-0110  # address serves admin.example.com
observations:
  - obs-8001
findings: []
```

A candidate whose response differs from the baseline is recorded as a distinct
virtual host.

---

# Example 2 — Baseline Comparison

The skill establishes a baseline before probing candidates.

## Behavior

```
Probe with random host → baseline (404 default)

Probe with admin.example.com → 200 distinct application → distinct virtual host
```

Differential comparison distinguishes real virtual hosts from the default
response.

---

# Example 3 — Wildcard Response Discounted

The address returns identical responses for all host names.

## Result Fragment

```yaml
outcome: completed
assets: []
notes: wildcard response detected; candidates discounted
```

Wildcard responses are detected and discounted to reduce false positives.

---

# Example 4 — Hidden Host Finding

An internal virtual host is reachable publicly.

## Produced Finding

```yaml
finding_id: finding-vhost-0081
title: Internal virtual host publicly reachable
category: Exposure
severity: Medium
confidence: Verified
evidence:
  - evidence-http-0081
```

## Produced Risk

```yaml
risk_id: risk-vhost-0081
finding_id: finding-vhost-0081
likelihood: { rating: Medium }
impact: { rating: Medium }
score: { model: likelihood-impact, value: 5.0, severity: Medium }
```

The exposure is reported as data; exploitation is out of scope.

---

# Example 5 — Denied Probe

The Policy Engine denies probing of an out-of-scope address.

## Decision

```yaml
decision: deny
scope_status: out_of_scope
```

No probe is issued against the out-of-scope address.

---

# Example 6 — Partial Result

Some candidates fail while others succeed.

## Result

```yaml
outcome: partial
assets: [ asset-0080 ]
errors:
  - category: Probe
    target_address: 93.184.216.34
    host: staging.example.com
    retryable: true
```

The failure of one candidate does not abort probing of others.

---

# Example 7 — Observation Record

A single probe produces the following observation.

```yaml
observation:
  observation_id: obs-8001
  type: http-response
  subject:
    target: 93.184.216.34
    asset_id: asset-0080
  content:
    summary: Host admin.example.com returns a distinct 200 response
    attributes:
      host: admin.example.com
      status_code: 200
      differs_from_baseline: true
  confidence: High
  evidence:
    - evidence-http-0080
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
- [HTTP Client](../../shared/http-client/README.md)
