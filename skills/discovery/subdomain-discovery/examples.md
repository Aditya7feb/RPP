# Subdomain Discovery Examples

**File:** `skills/discovery/subdomain-discovery/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-independent examples of the
Subdomain Discovery Skill in use.

Examples demonstrate passive collection, policy-gated resolution, subdomain-asset
production, takeover findings, out-of-scope handling, and evidence.

All examples are illustrative and contain no implementation code.

---

# Example 1 — Discover And Confirm Subdomains

The Recon Agent discovers subdomains of an apex domain.

## Invocation

```yaml
metadata:
  request_id: req-17001
  assessment_id: asmt-42
  task_id: task-subdomain
  skill_id: subdomain-discovery
apex_domain: example.com
sources:
  passive: [certificate-transparency, passive-dns]
  active_resolution: true
wordlist_ref: wordlist-subdomains
scope_id: scope-asmt-42
roe_id: roe-asmt-42
```

## Result

```yaml
outcome: completed
assets:
  - asset-0060   # subdomain api.example.com (confirmed)
  - asset-0061   # subdomain legacy.example.com (suspected)
relationships:
  - assetrel-0090  # api.example.com resolves-to 93.184.216.34
observations:
  - obs-7001
findings: []
```

Resolved names are `confirmed`; passive-only names are `suspected`.

---

# Example 2 — Passive Candidate Suspected

A certificate-transparency candidate is recorded before resolution.

## Result Fragment

```yaml
assets:
  - asset_id: asset-0061
    type: subdomain
    value: legacy.example.com
    state: suspected
    confidence: Low
```

Passive-only candidates are recorded as suspected until resolved.

---

# Example 3 — Policy Gate For Active Resolution

Active resolution is an active action; the skill consults the Policy Engine.

## Decision

```yaml
decision: allow
scope_status: in_scope
rate_ceiling_policy_id: ratelimitpolicy-roe-ceiling
```

Resolution proceeds within the attached rate ceiling.

---

# Example 4 — Subdomain Takeover Finding

A subdomain has a dangling CNAME to an unclaimed resource.

## Produced Finding

```yaml
finding_id: finding-takeover-0062
title: Potential subdomain takeover
category: Misconfiguration
severity: High
confidence: High
evidence:
  - evidence-dns-0062
```

## Produced Risk

```yaml
risk_id: risk-takeover-0062
finding_id: finding-takeover-0062
likelihood: { rating: Medium }
impact: { rating: High }
score: { model: likelihood-impact, value: 7.0, severity: High }
```

Takeover potential is reported as data; exploitation is out of scope.

---

# Example 5 — Out-Of-Scope Candidate Recorded

A candidate resolves outside scope.

## Result Fragment

```yaml
assets:
  - asset_id: asset-0070
    type: subdomain
    value: partner.other.com
    scope_status: out_of_scope
    state: suspected
```

The out-of-scope candidate is recorded but not actively probed.

---

# Example 6 — Denied Resolution

The Policy Engine denies active resolution outside the maintenance window.

## Result Fragment

```yaml
outcome: partial
denied_actions:
  - candidate: dev.example.com
    reason: outside maintenance window
```

The candidate is recorded as suspected; resolution resumes within the window.

---

# Example 7 — Observation Record

A single resolution produces the following observation.

```yaml
observation:
  observation_id: obs-7001
  type: dns-record
  subject:
    target: api.example.com
    asset_id: asset-0060
  content:
    summary: A record resolved to 93.184.216.34
    attributes:
      record_type: A
      value: 93.184.216.34
  confidence: High
  evidence:
    - evidence-dns-0060
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
