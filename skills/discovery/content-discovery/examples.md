# Content Discovery Examples

**File:** `skills/discovery/content-discovery/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-independent examples of the
Content Discovery Skill in use.

Examples demonstrate policy-gated probing, endpoint-asset production, exposure
findings, scope-confined crawling, partial results, and evidence.

All examples are illustrative and contain no implementation code.

---

# Example 1 — Enumerate And Produce Endpoint Assets

The Recon Agent enumerates content on a web application.

## Invocation

```yaml
metadata:
  request_id: req-15001
  assessment_id: asmt-42
  task_id: task-content-disc
  skill_id: content-discovery
target: https://app.example.com
wordlist_ref: wordlist-common-paths
follow_links: true
scope_id: scope-asmt-42
roe_id: roe-asmt-42
```

## Result

```yaml
outcome: completed
assets:
  - asset-0030   # web-application app.example.com
  - asset-0031   # endpoint /login
  - asset-0032   # endpoint /admin
relationships:
  - assetrel-0060  # application serves endpoint /login
observations:
  - obs-5001
findings: []
```

Present content yields `endpoint` Assets linked to the application.

---

# Example 2 — Policy Gate For Active Probe

Content probing is an active action; the skill consults the Policy Engine.

## Decision

```yaml
decision: allow
scope_status: in_scope
rate_ceiling_policy_id: ratelimitpolicy-roe-ceiling
```

Probing proceeds within the attached rate ceiling.

---

# Example 3 — Directory Listing Finding

A directory returns an index listing.

## Produced Finding

```yaml
finding_id: finding-content-0033
title: Directory listing enabled
category: Information Disclosure
severity: Low
confidence: Verified
evidence:
  - evidence-http-0033
```

## Produced Risk

```yaml
risk_id: risk-content-0033
finding_id: finding-content-0033
likelihood: { rating: Medium }
impact: { rating: Low }
score: { model: likelihood-impact, value: 3.4, severity: Low }
```

The Finding references its Evidence; Risk scores it as a first-class object.

---

# Example 4 — Backup File Exposed

A backup file is reachable.

## Produced Finding

```yaml
finding_id: finding-content-0034
title: Exposed backup file
category: Information Disclosure
severity: Medium
confidence: Verified
evidence:
  - evidence-http-0034
```

Sensitive content is redacted in the evidence per Rules of Engagement.

---

# Example 5 — Out-Of-Scope Link Not Followed

A discovered link points outside scope.

## Result Fragment

```yaml
assets:
  - asset_id: asset-0050
    type: endpoint
    value: https://cdn.other.com/app.js
    scope_status: out_of_scope
```

The out-of-scope link is recorded but not followed.

---

# Example 6 — Partial Result

Some paths fail while others succeed.

## Result

```yaml
outcome: partial
assets: [ asset-0031, asset-0032 ]
errors:
  - category: Request
    target: https://app.example.com
    path: /reports
    retryable: true
```

The failure of one path does not abort probing of others.

---

# Example 7 — Observation Record

A single probe produces the following observation.

```yaml
observation:
  observation_id: obs-5001
  type: http-response
  subject:
    target: https://app.example.com/login
    asset_id: asset-0031
  content:
    summary: 200 OK login form present
    attributes:
      status_code: 200
      content_type: text/html
  confidence: High
  evidence:
    - evidence-http-0031
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
