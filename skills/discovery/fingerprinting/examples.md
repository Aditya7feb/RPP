# Fingerprinting Examples

**File:** `skills/discovery/fingerprinting/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-independent examples of the
Fingerprinting Skill in use.

Examples demonstrate policy-gated collection, technology production, confidence
grading, weakness findings, partial results, and evidence.

All examples are illustrative and contain no implementation code.

---

# Example 1 — Identify Technologies

The Recon Agent fingerprints a web application.

## Invocation

```yaml
metadata:
  request_id: req-16001
  assessment_id: asmt-42
  task_id: task-fingerprint
  skill_id: fingerprinting
target: https://app.example.com
asset_id: asset-0030
signals: [headers, body, cookies, tls]
scope_id: scope-asmt-42
roe_id: roe-asmt-42
```

## Result

```yaml
outcome: completed
technologies:
  - technology_id: tech-0001   # nginx 1.24
    confidence: High
  - technology_id: tech-0002   # React
    confidence: Medium
relationships:
  - assetrel-0070  # web-application references nginx
observations:
  - obs-6001
findings: []
```

Technologies are produced as canonical records linked to the Asset with
confidence grades.

---

# Example 2 — Passive Preference

Fingerprinting prefers passive signals; active probing is gated.

## Decision

```yaml
decision: allow
scope_status: in_scope
```

Passive header and TLS analysis proceeds; active probing would require a separate
allow decision.

---

# Example 3 — Outdated Version Finding

An outdated server version is observed.

## Produced Finding

```yaml
finding_id: finding-tech-0003
title: Outdated web server version
category: Vulnerable Component
severity: Medium
confidence: High
evidence:
  - evidence-http-0003
references:
  - CVE-XXXX-XXXX   # referenced informally; deterministic mapping deferred
```

## Produced Risk

```yaml
risk_id: risk-tech-0003
finding_id: finding-tech-0003
likelihood: { rating: Medium }
impact: { rating: Medium }
score: { model: likelihood-impact, value: 5.6, severity: Medium }
```

The Finding references its Evidence; vulnerability identifiers are referenced
informally pending a future knowledge capability.

---

# Example 4 — Version Disclosure Finding

A verbose version banner is disclosed.

## Produced Finding

```yaml
finding_id: finding-tech-0004
title: Verbose version disclosure
category: Information Disclosure
severity: Low
confidence: Verified
evidence:
  - evidence-http-0004
```

The disclosure is confirmed from response headers and backed by Evidence.

---

# Example 5 — Inferred Technology With Lower Confidence

A framework is inferred, not directly observed.

## Result Fragment

```yaml
technologies:
  - technology_id: tech-0005
    name: Express
    confidence: Low
    inferred: true
```

Inferred identifications carry lower confidence than observed ones.

---

# Example 6 — Denied Collection

The Policy Engine denies fingerprinting of an out-of-scope Asset.

## Decision

```yaml
decision: deny
scope_status: out_of_scope
```

No signal collection is performed against the out-of-scope Asset.

---

# Example 7 — Observation Record

A single identification produces the following observation.

```yaml
observation:
  observation_id: obs-6001
  type: http-response
  subject:
    target: https://app.example.com
    asset_id: asset-0030
  content:
    summary: Server header discloses nginx 1.24
    attributes:
      header: Server
      value: nginx/1.24.0
  confidence: High
  evidence:
    - evidence-http-0001
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
- [Technology Schema](../../../schemas/technology.md)
