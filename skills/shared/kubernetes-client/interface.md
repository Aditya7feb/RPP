# Kubernetes Client Interface

**File:** `skills/shared/kubernetes-client/interface.md`

**Version:** 1.0.0

---

# Purpose

The Kubernetes Client Interface defines the canonical contract through which
platform components interact with Kubernetes API servers.

The interface standardizes resource operations, scope confinement, mutation
gating, and result propagation while remaining independent of any API
implementation.

All consumers SHALL perform Kubernetes access exclusively through this interface.

---

# Design Principles

The interface SHALL be

- Stable
- Strongly Defined
- API Independent
- Versioned
- Observable
- Backward Compatible
- Scope-Confined

---

# Relationship

```
Master Agent

↓

Cloud or Container Domain Skill

↓

Kubernetes Client Interface

↓

Kubernetes Client Shared Skill

↓

HTTP Client (TLS) → Kubernetes API Server
```

The interface SHALL NOT expose or depend on adapter internals.

---

# Interface Overview

```
Metadata

↓

Cluster Target

↓

Scope Reference

↓

Operation

↓

Governance References

↓

Execution Context

↓

Operation Result

↓

Evidence

↓

Errors
```

---

# Metadata

Every invocation SHALL include

```yaml
request_id:

assessment_id:

task_id:

skill_id:

timestamp:
```

Metadata enables tracing and auditing.

---

# Cluster Target

Every invocation SHALL define

```yaml
cluster_id:

credential_ref:
```

`cluster_id` SHALL reference a configured cluster and its API server.

`credential_ref` SHALL reference a credential resolved by the
[Authentication](../authentication/README.md) package.

The interface SHALL NOT accept inline secrets or tokens.

---

# Scope Reference

Every invocation SHALL define

```yaml
namespace:

group:

version:

kind:

name:
```

`namespace` SHALL confine namespaced operations; cluster-scoped operations SHALL
declare cluster scope explicitly.

`group`, `version`, and `kind` SHALL identify the resource type.

`name` MAY identify a specific resource.

---

# Operation

Every invocation SHALL define

```yaml
verb:

body_ref:

options:
```

`verb` SHALL be one of `get`, `list`, `watch`, `create`, `update`, `patch`,
`delete`, or `exec`.

`body_ref` SHALL reference the request body for mutating verbs.

`options` MAY include `max_items`, `watch_duration`, and label or field
selectors.

Mutating verbs and `exec` SHALL be authorized as intrusive; `exec` SHALL require
elevated authorization.

---

# Governance References

Every invocation MAY reference

```yaml
rate_limit_policy_id:

retry_policy_id:

proxy_id:
```

Referenced policies SHALL conform to their canonical schemas. Absent references
SHALL inherit configured defaults.

---

# Execution Context

The Kubernetes Client Shared Skill SHALL receive read-only context.

```yaml
execution_id:

parent_span:

variables:
```

The interface SHALL treat context as read-only.

---

# Operation Result

Every invocation SHALL return a normalized result.

```yaml
outcome:

items:

object_ref:

rbac:

watch_events_ref:

error:

evidence:
```

`outcome` SHALL be one of

```
completed

scope_rejected

forbidden

not_found

rejected

timed_out
```

`items` SHALL summarize listed resources; large objects SHALL be referenced as
artifacts.

`rbac`, when observed, SHALL report effective permissions as data.

`forbidden` SHALL map from an API authorization denial.

API-specific client objects SHALL NOT be exposed.

---

# Evidence

The interface SHALL expose structured evidence.

Evidence MAY include

- Cluster and namespace
- Resource kind and verb
- Result counts
- Observed RBAC

Evidence SHALL conform to the canonical
[Evidence schema](../../../schemas/evidence.md) and SHALL NOT contain tokens or
sensitive resource contents.

---

# Error Contract

Errors SHALL conform to
[the platform error handling model](../../core/error-handling.md) and to
[the Kubernetes Client error model](error-model.md).

An API `403` SHALL map to a `forbidden` outcome preserving the reason.

---

# Compatibility

The interface SHALL remain stable across API versions and consumers.

Consumers SHALL require no modification when clusters change.

---

# Versioning

The interface SHALL follow semantic versioning.

Minor versions MAY introduce optional fields.

Major versions SHALL indicate breaking changes.

---

# Validation Rules

A compliant invocation SHALL define

- Metadata
- Cluster Target
- Scope Reference
- Operation
- Execution Context
- Operation Result
- Error Handling
- Evidence

Mutating verbs SHALL be authorized; `exec` SHALL require elevated authorization.

---

# Quality Requirements

The Kubernetes Client Interface SHALL

✓ Remain API independent

✓ Enforce scope confinement

✓ Gate mutations and exec

✓ Support structured errors

✓ Preserve evidence

✓ Protect tokens and contents

✓ Remain backward compatible

---

# Future Extensions

Future versions MAY include

- Custom resource descriptors
- Server-side apply
- Admission-review observation

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Kubernetes Client Interface provides a stable,
implementation-independent contract through which all platform components perform
confined, governed Kubernetes API operations across the Robust PenTest Platform.
