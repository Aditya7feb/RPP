# Kubernetes Client Configuration

**File:** `skills/shared/kubernetes-client/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the configuration model for the Kubernetes Client Shared
Skill.

Configuration determines clusters, authorized namespace and resource scopes,
mutation gating, result and watch bounds, governance policy defaults, and
observability.

Configuration is declarative and implementation independent, consistent with the
[Configuration Model](../../core/configuration-model.md).

---

# Configuration Sources

The Kubernetes Client Shared Skill SHALL resolve configuration from the following
sources, in increasing order of precedence.

```
Platform Defaults

↓

Assessment Configuration

↓

Consumer Configuration

↓

Invocation Override
```

A higher-precedence source MAY narrow scopes or tighten gating but SHALL NOT
widen a scope or enable exec where prohibited.

---

# Configuration Structure

```yaml
kubernetes_client:

  clusters:

  scopes:

  execution:

  bounds:

  governance:

  observability:
```

---

# Clusters

```yaml
clusters:
  - cluster_id:
    api_server:
    trust_anchor_ref:
```

`clusters` SHALL enumerate the configured clusters.

`api_server` SHALL identify the API-server endpoint.

`trust_anchor_ref` SHALL reference the cluster trust anchor for TLS validation.

Cluster configuration SHALL NOT contain tokens.

---

# Scopes

```yaml
scopes:
  - scope_id:
    cluster_id:
    namespaces:
    kinds:
    cluster_scoped:
```

`scopes` SHALL enumerate authorized namespace and resource-kind scopes.

`namespaces` SHALL bound namespaced operations.

`kinds` SHALL bound resource kinds.

`cluster_scoped` SHALL be a boolean authorizing cluster-scoped operations and
SHALL default to `false`.

---

# Execution

```yaml
execution:
  allow_mutations:
  allow_exec:
```

`allow_mutations` SHALL gate create, update, patch, and delete and SHALL default
to `false`.

`allow_exec` SHALL gate exec and attach, SHALL require elevated authorization,
and SHALL default to `false`.

---

# Bounds

```yaml
bounds:
  max_items:
  watch_duration:
  request_timeout:
```

`max_items` SHALL bound list result sets.

`watch_duration` SHALL bound watch operations.

`request_timeout` SHALL bound individual requests.

---

# Governance

```yaml
governance:
  default_rate_limit_policy_id:
  default_retry_policy_id:
  default_proxy_id:
```

`default_rate_limit_policy_id`, `default_retry_policy_id`, and
`default_proxy_id` SHALL reference canonical policies applied when an invocation
omits its own.

---

# Observability

```yaml
observability:
  emit_events:
  capture_evidence:
  metrics_enabled:
```

`emit_events` SHALL enable publication of lifecycle events.

`capture_evidence` SHALL enable operation evidence capture conforming to the
[Evidence schema](../../../schemas/evidence.md).

`metrics_enabled` SHALL enable metric exposure.

---

# Validation Rules

A valid configuration SHALL satisfy

- Every cluster defines a `cluster_id`, `api_server`, and `trust_anchor_ref`
- Every scope references an existing cluster
- Scope identifiers are unique
- `allow_mutations` and `allow_exec` default to `false`
- `max_items` is greater than or equal to `1`
- `watch_duration` and `request_timeout` are positive durations
- Referenced default policies exist and are valid
- No secret material appears in configuration

---

# Example Configuration

```yaml
kubernetes_client:

  clusters:
    - cluster_id: target-cluster
      api_server: https://k8s.example.com:6443
      trust_anchor_ref: trust-target-cluster

  scopes:
    - scope_id: audit-namespaces
      cluster_id: target-cluster
      namespaces:
        - default
        - app
      kinds:
        - pods
        - services
        - roles
        - rolebindings
      cluster_scoped: false

  execution:
    allow_mutations: false
    allow_exec: false

  bounds:
    max_items: 2000
    watch_duration: 60s
    request_timeout: 15s

  governance:
    default_rate_limit_policy_id: ratelimitpolicy-default-http
    default_retry_policy_id: retrypolicy-default-network
    default_proxy_id: proxy-corporate-egress

  observability:
    emit_events: true
    capture_evidence: true
    metrics_enabled: true
```

---

# Related Documents

- [Interface](interface.md)
- [Execution](execution.md)
- [Evidence Schema](../../../schemas/evidence.md)
- [Configuration Model](../../core/configuration-model.md)
