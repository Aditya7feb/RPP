# Session Management Capabilities

**File:** `skills/authentication/sessions/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the Session Management Skill.
Capabilities describe *what* the skill provides, not *how* it is implemented.

Each capability is implementation independent and consumed through the
[Session Management Interface](interface.md).

---

# Capability Model

```
Authorization

Session Observation

Cookie Analysis

Lifecycle Analysis

Weakness Analysis

Observability
```

---

# Authorization Capabilities

## Policy Consultation

The skill SHALL consult the [Policy Engine](../../shared/policy-engine/README.md)
before every target-facing action.

---

## Scope Confinement

The skill SHALL test only in-scope applications.

---

# Session Observation Capabilities

## Session Issuance Observation

The skill SHALL observe how session identifiers are issued through the
[HTTP Client](../../shared/http-client/README.md).

---

## Authenticated-State Observation

The skill SHALL observe session behavior across pre-authentication and
post-authentication states using managed credentials.

---

# Cookie Analysis Capabilities

## Cookie Attribute Analysis

The skill SHALL analyze [HTTP Cookie](../../../schemas/http-cookie.md) attributes,
including `Secure`, `HttpOnly`, `SameSite`, path, domain, and expiry.

---

## Transport Analysis

The skill SHALL determine whether session identifiers are transmitted over secure
transport.

---

# Lifecycle Analysis Capabilities

## Renewal Analysis

The skill SHALL determine whether identifiers are rotated after authentication.

---

## Invalidation Analysis

The skill SHALL determine whether sessions are invalidated on logout and after
timeout.

---

## Entropy Analysis

The skill SHALL assess identifier predictability using deterministic criteria.

---

# Weakness Analysis Capabilities

## Weakness Identification

The skill SHALL identify session-management weaknesses from observed behavior.

---

## Finding Production

The skill SHALL produce [Findings](../../../schemas/finding.md) with
[Risk](../../../schemas/risk.md), each backed by Evidence.

---

# Observability Capabilities

## Observation And Evidence

The skill SHALL record [Observations](../../../schemas/observation.md) and promote
them to [Evidence](../../../schemas/evidence.md) with secrets redacted.

---

## Event Emission

The skill SHOULD publish lifecycle events to the Execution State.

---

## Metrics

The skill SHOULD expose metrics including checks performed and findings emitted.

---

# Capability Boundaries

The skill SHALL NOT

- Perform HTTP input or output directly
- Discover applications or endpoints
- Test token formats or authorization decisions
- Persist session secrets
- Produce a Finding without Evidence
- Act on out-of-scope applications

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Policy Consultation | Authorization | SHALL |
| Scope Confinement | Authorization | SHALL |
| Session Issuance Observation | Session Observation | SHALL |
| Authenticated-State Observation | Session Observation | SHALL |
| Cookie Attribute Analysis | Cookie Analysis | SHALL |
| Transport Analysis | Cookie Analysis | SHALL |
| Renewal Analysis | Lifecycle Analysis | SHALL |
| Invalidation Analysis | Lifecycle Analysis | SHALL |
| Entropy Analysis | Lifecycle Analysis | SHALL |
| Weakness Identification | Weakness Analysis | SHALL |
| Finding Production | Weakness Analysis | SHALL |
| Observation And Evidence | Observability | SHALL |
| Event Emission | Observability | SHOULD |
| Metrics | Observability | SHOULD |

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Execution](execution.md)
- [Error Model](error-model.md)
- [HTTP Cookie Schema](../../../schemas/http-cookie.md)
