# API Discovery Examples

**File:** `skills/discovery/api-discovery/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-independent examples of the API
Discovery Skill in use.

Examples demonstrate policy-gated discovery, specification location, GraphQL
introspection detection, API-asset production, exposure findings, and evidence.

All examples are illustrative and contain no implementation code.

---

# Example 1 — Locate An OpenAPI Specification

The Recon Agent discovers the API surface of an application.

## Invocation

```yaml
metadata:
  request_id: req-19001
  assessment_id: asmt-42
  task_id: task-api-disc
  skill_id: api-discovery
target: https://app.example.com
definition_hints: [/openapi.json, /swagger.json]
detect_graphql: true
scope_id: scope-asmt-42
roe_id: roe-asmt-42
```

## Result

```yaml
outcome: completed
assets:
  - asset-0090   # api https://app.example.com/api (openapi located)
  - asset-0091   # endpoint GET /api/users
  - asset-0092   # endpoint POST /api/login
relationships:
  - assetrel-0130  # api serves endpoint /api/users
observations:
  - obs-9001
findings: []
```

The located specification yields declared operations as `endpoint` Assets with
provenance to the specification.

---

# Example 2 — Policy Gate For Active Probe

Specification retrieval is an active action; the skill consults the Policy Engine.

## Decision

```yaml
decision: allow
scope_status: in_scope
rate_ceiling_policy_id: ratelimitpolicy-roe-ceiling
```

Retrieval proceeds within the attached rate ceiling.

---

# Example 3 — Public Specification Finding

An API specification is reachable without authentication.

## Produced Finding

```yaml
finding_id: finding-api-0093
title: API specification publicly exposed
category: Information Disclosure
severity: Medium
confidence: Verified
evidence:
  - evidence-http-0093
```

## Produced Risk

```yaml
risk_id: risk-api-0093
finding_id: finding-api-0093
likelihood: { rating: Medium }
impact: { rating: Medium }
score: { model: likelihood-impact, value: 5.2, severity: Medium }
```

The exposure is reported as data; operation testing is out of scope for
discovery.

---

# Example 4 — GraphQL Introspection Enabled

A GraphQL endpoint exposes introspection.

## Produced Finding

```yaml
finding_id: finding-api-0094
title: GraphQL introspection enabled
category: Information Disclosure
severity: Low
confidence: Verified
evidence:
  - evidence-http-0094
```

The introspection query is gated by the Policy Engine as an active action before
execution.

---

# Example 5 — Base-Path Discovery

Common API base paths are probed.

## Result Fragment

```yaml
assets:
  - asset_id: asset-0095
    type: api
    value: https://app.example.com/v1
    state: confirmed
```

Confirmed API base paths are recorded as `api` Assets.

---

# Example 6 — Denied Probe

The Policy Engine denies probing of an out-of-scope target.

## Decision

```yaml
decision: deny
scope_status: out_of_scope
```

No request is issued against the out-of-scope target.

---

# Example 7 — Observation Record

A single discovery produces the following observation.

```yaml
observation:
  observation_id: obs-9001
  type: http-response
  subject:
    target: https://app.example.com/openapi.json
    asset_id: asset-0090
  content:
    summary: 200 OK OpenAPI 3.0 document located
    attributes:
      status_code: 200
      content_type: application/json
      spec_format: openapi-3.0
  confidence: High
  evidence:
    - evidence-http-0090
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
