# Secrets Client Shared Skill

**File:** `skills/shared/secrets-client/README.md`

**Version:** 1.0.0

---

# Purpose

The Secrets Client Shared Skill provides the canonical, implementation-independent
mechanism for resolving and brokering secrets within the Robust PenTest Platform
(RPP).

Rather than allowing individual skills to fetch secrets from stores directly,
this shared skill centralizes secret resolution, reference-based handling,
brokered use, lease and rotation awareness, and observability behind a stable
interface.

All packages that require secrets SHALL obtain them through this shared skill and
the [Authentication](../authentication/README.md) package, never by value.

---

# Goals

The Secrets Client Shared Skill SHALL

- Abstract secret stores behind a stable interface
- Resolve secrets by opaque reference, never returning raw values to consumers
- Broker secret use so that values are applied without exposure
- Track leases, versions, and rotation
- Produce non-sensitive secret-access evidence
- Integrate with platform observability

---

# Non-Goals

The Secrets Client Shared Skill SHALL NOT

- Return secret values to general consumers
- Detect vulnerabilities such as exposed secrets
- Produce security findings
- Log, persist, or embed secret values in evidence
- Replace the platform identity provider

The Secrets Client brokers secrets by reference. Interpretation, including
exposed-secret detection, belongs to domain skills operating on other data, not
on values from this client.

---

# Design Principles

The Secrets Client Shared Skill SHALL be

- Reference-first, never value-returning to general consumers
- Least-exposure by construction
- Lease and rotation aware
- Bounded in cache lifetime
- Observable without leaking secrets
- Secure by default

---

# Architecture

```
Master Agent

↓

Shared Package or Domain Skill

↓

Secrets Client Shared Skill

├── Reference Resolver
├── Broker
├── Lease Manager
├── Rotation Tracker
├── Redaction Guard
├── Evidence Manager
├── Event Manager

↓

Secret Store Adapter
```

The Secrets Client resolves and brokers secrets but SHALL remain unaware of the
secret store adapter implementation and SHALL never expose raw values through the
interface.

---

# Responsibilities

The Secrets Client Shared Skill is responsible for

- Resolving a secret reference to an opaque handle
- Brokering the application of a secret to an operation without exposing its
  value
- Tracking leases, versions, and rotation
- Enforcing bounded cache lifetimes for handles
- Producing non-sensitive access evidence
- Emitting secret lifecycle events without values

---

# Access Model

```
Receive Secret Request

↓

Resolve Reference

↓

Issue Opaque Handle

↓

Broker Application (value never leaves the boundary)

↓

Track Lease / Rotation

↓

Emit Non-Sensitive Evidence
```

Consumers SHALL receive a handle, not a value.

---

# Reference-Based Handling

The Secrets Client SHALL resolve a secret reference to an opaque handle that
identifies the secret without revealing it.

General consumers SHALL use the handle to request brokered application. The value
SHALL remain within the secrets boundary.

Only the [Authentication](../authentication/README.md) package, acting as a
trusted broker at the point of use, SHALL apply the resolved value to an
outbound operation, and SHALL do so without exposing it to the calling skill.

---

# Brokered Use

The Secrets Client SHALL support brokered application, in which a secret is
applied to an operation such as an outbound request header or an authentication
exchange without the value being returned to the requesting skill.

Brokering SHALL redact the value from all evidence, logs, and results.

---

# Leases And Rotation

The Secrets Client SHALL track leases and versions where the store supports them.

Where a secret rotates, handles SHALL reflect the current version, and expired
leases SHALL be renewed or invalidated.

Consumers SHALL tolerate rotation by using handles rather than cached values.

---

# Caching

The Secrets Client MAY cache resolved handles for a bounded lifetime.

Secret values SHALL NOT be cached in a form that could be persisted or logged.
Any in-memory retention SHALL be bounded and cleared on lease expiry.

The [Cache](../cache/README.md) shared skill SHALL NOT be used to store secret
values.

---

# Evidence

The Secrets Client Shared Skill SHOULD capture non-sensitive access evidence such
as

- Secret reference identifier
- Version or lease identifier
- Access purpose
- Access outcome

Evidence SHALL conform to the canonical
[Evidence schema](../../../schemas/evidence.md) and SHALL NEVER contain secret
values.

---

# Events

The Secrets Client Shared Skill SHOULD publish

- SecretResolved
- SecretBrokered
- LeaseRenewed
- RotationDetected
- HandleExpired
- AccessDenied

Events SHALL integrate with the platform Execution State and SHALL NEVER contain
secret values.

---

# Dependencies

The Secrets Client Shared Skill depends on

- [Configuration Model](../../core/configuration-model.md)
- [Execution Model](../../core/execution-model.md)
- [Error Handling](../../core/error-handling.md)
- [Evidence Schema](../../../schemas/evidence.md)

The [Authentication](../authentication/README.md) package is the primary broker
that applies resolved secrets at the point of use. The Secrets Client SHALL NOT
depend on domain skills.

---

# Consumers

Typical consumers include

- The [Authentication](../authentication/README.md) package, as broker
- The [Proxy](../proxy/README.md) shared skill for proxy credentials
- Any package requiring a credential reference

---

# Outputs

Typical outputs MAY include

- Opaque secret handles
- Lease and version identifiers
- Non-sensitive access evidence references

Outputs SHALL NEVER include secret values.

---

# Security Principles

The Secrets Client Shared Skill SHALL

- Never return secret values to general consumers
- Broker application so values are used without exposure
- Redact values from all evidence, logs, and results
- Bound handle lifetime and clear values on lease expiry
- Preserve auditability without exposing secrets

Exposing a secret even once can compromise an engagement. The shared skill SHALL
treat non-exposure as an absolute requirement.

---

# Best Practices

Consumers SHOULD

- Use handles rather than requesting values
- Rely on brokered application at the point of use
- Tolerate rotation through handles
- Capture only non-sensitive access evidence
- Scope secret references narrowly

---

# Anti-Patterns

Consumers SHOULD NOT

- Request or hold raw secret values
- Cache secret values
- Log or embed secrets in evidence
- Bypass the broker to apply secrets directly
- Reuse handles beyond their lease

---

# Documentation Requirements

This shared skill includes

- README.md
- capabilities.md
- interface.md
- configuration.md
- execution.md
- error-model.md
- examples.md
- adr/ADR-001-secret-reference-abstraction.md

---

# Related Shared Packages

- [Authentication](../authentication/README.md)
- [Proxy](../proxy/README.md)
- [Logging](../logging/README.md)
- [Evidence](../evidence/README.md)

---

# Canonical Schemas

- [Evidence](../../../schemas/evidence.md)

---

# Architecture Decisions

- [ADR-001 — Secret Reference Abstraction](adr/ADR-001-secret-reference-abstraction.md)

---

# Future Extensions

Future versions MAY support

- Dynamic secret generation with short leases
- Envelope encryption descriptors
- Multi-store federation
- Just-in-time brokered credentials

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Secrets Client Shared Skill provides a reference-first,
non-exposing, and implementation-independent secrets abstraction for the Robust
PenTest Platform.

It enables consistent, auditable secret use across every package while
guaranteeing that secret values are never exposed to consumers, logs, or
evidence, without embedding store implementations in consumers.
