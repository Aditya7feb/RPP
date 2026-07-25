# Asset Discovery Examples

**File:** `skills/discovery/asset-discovery/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the Asset
Discovery Skill. Examples illustrate the interface and outputs; they contain no
implementation code.

---

# Example 1 — Deduplicating A Host Reported By Two Skills

## Request

```yaml
assets:
  - id: asset-host-dns-01
    type: host
    value: app.example.com
    provenance:
      skill: dns-enumeration
  - id: asset-host-vhost-01
    type: host
    value: app.example.com
    provenance:
      skill: virtual-host-discovery
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
assets:
  - id: asset-host-example-com
    type: host
    value: app.example.com
    scope_status: in-scope
    provenance:
      sources:
        - dns-enumeration
        - virtual-host-discovery
observations:
  - id: obs-ad-4001
    kind: asset-merge
evidence:
  - id: evidence-ad-7001
    observation_ref: obs-ad-4001
findings: []
status: completed
metrics:
  assets_ingested: 2
  duplicates_merged: 1
```

The same host reported by two skills is merged into one canonical Asset that
preserves provenance from both sources.

---

# Example 2 — Conflicting Facts Flagged

## Request

```yaml
assets:
  - id: asset-svc-a
    type: service
    value: tcp/443
    attributes:
      product: nginx
    provenance:
      skill: fingerprinting
  - id: asset-svc-b
    type: service
    value: tcp/443
    attributes:
      product: apache
    provenance:
      skill: port-discovery
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
assets:
  - id: asset-service-443
    type: service
    value: tcp/443
    scope_status: in-scope
findings:
  - id: finding-ad-5001
    title: Conflicting product facts for the same service
    risk_ref: risk-ad-3001
    evidence_refs:
      - evidence-ad-7002
status: completed
metrics:
  assets_ingested: 2
  conflicts_detected: 1
```

The conflicting product facts are merged into one Asset and the conflict is
reported as a Finding with Risk, backed by Evidence. Neither fact is silently
discarded.

---

# Example 3 — Out-Of-Scope Asset Flagged

## Request

```yaml
assets:
  - id: asset-host-external
    type: host
    value: cdn.thirdparty.net
    provenance:
      skill: content-discovery
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
assets: []
findings:
  - id: finding-ad-5002
    title: Out-of-scope host reported by an active skill
    risk_ref: risk-ad-3002
    evidence_refs:
      - evidence-ad-7003
status: completed
metrics:
  assets_ingested: 1
  out_of_scope_flagged: 1
```

The host is confirmed out of scope by the Policy Engine, excluded from the
in-scope graph, and flagged.

---

# Example 4 — Orphan Asset

## Request

```yaml
assets:
  - id: asset-endpoint-orphan
    type: endpoint
    value: https://app.example.com/legacy
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
assets:
  - id: asset-endpoint-orphan
    type: endpoint
    value: https://app.example.com/legacy
    scope_status: in-scope
findings:
  - id: finding-ad-5003
    title: Orphan endpoint with no supporting relationship
    risk_ref: risk-ad-3003
    evidence_refs:
      - evidence-ad-7004
status: completed
metrics:
  assets_ingested: 1
  orphans_detected: 1
```

An endpoint with no provenance or relationship is retained but flagged as an
orphan for review.

---

# Related Documents

- [Interface](interface.md)
- [Execution](execution.md)
- [Configuration](configuration.md)
- [Error Model](error-model.md)
- [Asset Schema](../../../schemas/asset.md)
