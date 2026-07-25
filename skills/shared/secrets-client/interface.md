# Secrets Client Interface

**File:** `skills/shared/secrets-client/interface.md`

**Version:** 1.0.0

---

# Purpose

The Secrets Client Interface defines the canonical contract through which platform
components resolve and apply secrets by reference.

The interface standardizes reference resolution, brokered application, lease
handling, and result propagation while never exposing secret values to general
consumers.

All consumers SHALL obtain and apply secrets exclusively through this interface
and the [Authentication](../authentication/README.md) broker.

---

# Design Principles

The interface SHALL be

- Stable
- Strongly Defined
- Store Independent
- Versioned
- Observable
- Backward Compatible
- Non-Exposing

---

# Relationship

```
Master Agent

↓

Shared Package or Domain Skill

↓

Secrets Client Interface

↓

Secrets Client Shared Skill

↓

Secret Store Adapter
```

The interface SHALL NOT expose or depend on adapter internals and SHALL NOT
return secret values to general consumers.

---

# Interface Overview

```
Metadata

↓

Secret Reference

↓

Access Mode

↓

Broker Target

↓

Execution Context

↓

Access Result

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

# Secret Reference

Every invocation SHALL define

```yaml
secret_ref:

version:
```

`secret_ref` SHALL identify the secret within a store namespace.

`version` MAY request a specific version; absence SHALL select the current
version.

The interface SHALL NOT accept or return secret values.

---

# Access Mode

Every invocation SHALL define

```yaml
mode:
```

`mode` SHALL be one of

```
resolve_handle

broker_apply
```

`resolve_handle` SHALL return an opaque handle only.

`broker_apply` SHALL apply the secret to a broker target without returning the
value.

---

# Broker Target

For `broker_apply`, the invocation SHALL define

```yaml
broker_target:
```

`broker_target` SHALL describe where the secret is applied, such as an outbound
request header or an authentication exchange, identified abstractly.

The broker SHALL apply the value without exposing it to the requesting skill.

---

# Execution Context

The Secrets Client Shared Skill SHALL receive read-only context.

```yaml
execution_id:

parent_span:

variables:
```

The interface SHALL treat context as read-only.

---

# Access Result

Every invocation SHALL return a normalized result.

```yaml
outcome:

handle:

lease:

version:

error:

evidence:
```

`outcome` SHALL be one of

```
resolved

brokered

denied

not_found

expired
```

`handle` SHALL be an opaque handle for `resolve_handle`; it SHALL NOT encode the
secret value.

`lease` SHALL include a lease identifier and expiry where applicable.

The result SHALL NEVER contain a secret value.

---

# Evidence

The interface SHALL expose structured, non-sensitive evidence.

Evidence MAY include

- Secret reference identifier
- Version or lease identifier
- Access purpose and outcome

Evidence SHALL conform to the canonical
[Evidence schema](../../../schemas/evidence.md) and SHALL NEVER contain secret
values.

---

# Error Contract

Errors SHALL conform to
[the platform error handling model](../../core/error-handling.md) and to
[the Secrets Client error model](error-model.md).

Errors SHALL NEVER contain secret values.

---

# Compatibility

The interface SHALL remain stable across stores and consumers.

Consumers SHALL require no modification when stores change.

---

# Versioning

The interface SHALL follow semantic versioning.

Minor versions MAY introduce optional fields.

Major versions SHALL indicate breaking changes.

---

# Validation Rules

A compliant invocation SHALL define

- Metadata
- Secret Reference
- Access Mode
- Broker Target for `broker_apply`
- Execution Context
- Access Result
- Error Handling
- Evidence

No field SHALL carry a secret value.

---

# Quality Requirements

The Secrets Client Interface SHALL

✓ Remain store independent

✓ Never expose secret values

✓ Support brokered application

✓ Support structured errors

✓ Preserve non-sensitive evidence

✓ Support observability

✓ Remain backward compatible

---

# Future Extensions

Future versions MAY include

- Dynamic secret generation descriptors
- Envelope-encryption handles
- Just-in-time brokered credentials

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Secrets Client Interface provides a stable,
implementation-independent, non-exposing contract through which all platform
components resolve and apply secrets by reference across the Robust PenTest
Platform.
