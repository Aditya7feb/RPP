# Secrets Client Capabilities

**File:** `skills/shared/secrets-client/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the Secrets Client Shared
Skill. Capabilities describe *what* the shared skill provides, not *how* it is
implemented.

Each capability is implementation independent and consumed through the
[Secrets Client Interface](interface.md).

---

# Capability Model

```
Resolution

Brokering

Lease Management

Rotation

Protection

Observability
```

---

# Resolution Capabilities

## Reference Resolution

The Secrets Client SHALL resolve a secret reference to an opaque handle.

---

## Store Abstraction

The Secrets Client SHALL abstract secret stores behind a uniform interface.

---

# Brokering Capabilities

## Brokered Application

The Secrets Client SHALL apply a secret to an operation without returning its
value to the requesting skill.

---

## Non-Exposure

The Secrets Client SHALL NOT return secret values to general consumers.

---

# Lease Management Capabilities

## Lease Tracking

The Secrets Client SHALL track leases and versions where supported.

---

## Lease Renewal

The Secrets Client SHALL renew or invalidate expiring leases.

---

# Rotation Capabilities

## Rotation Awareness

The Secrets Client SHALL reflect rotation through handles.

---

# Protection Capabilities

## Redaction Guarantee

The Secrets Client SHALL redact secret values from all evidence, logs, and
results.

---

## Bounded Retention

The Secrets Client SHALL bound handle lifetime and clear values on lease expiry.

---

# Observability Capabilities

## Non-Sensitive Evidence

The Secrets Client SHOULD capture non-sensitive access evidence conforming to the
[Evidence schema](../../../schemas/evidence.md).

---

## Event Emission

The Secrets Client SHOULD publish lifecycle events without values.

---

## Metrics

The Secrets Client SHOULD expose metrics including resolutions, brokered
applications, renewals, and rotations.

---

# Capability Boundaries

The Secrets Client SHALL NOT

- Return secret values to general consumers
- Detect exposed secrets or other vulnerabilities
- Produce findings
- Cache secret values
- Persist secrets in evidence

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Reference Resolution | Resolution | SHALL |
| Store Abstraction | Resolution | SHALL |
| Brokered Application | Brokering | SHALL |
| Non-Exposure | Brokering | SHALL |
| Lease Tracking | Lease Management | SHALL |
| Lease Renewal | Lease Management | SHALL |
| Rotation Awareness | Rotation | SHALL |
| Redaction Guarantee | Protection | SHALL |
| Bounded Retention | Protection | SHALL |
| Non-Sensitive Evidence | Observability | SHOULD |
| Event Emission | Observability | SHOULD |
| Metrics | Observability | SHOULD |

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Execution](execution.md)
- [Error Model](error-model.md)
- [Authentication](../authentication/README.md)
