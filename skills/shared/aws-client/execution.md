# AWS Client Execution

**File:** `skills/shared/aws-client/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the deterministic execution model of the AWS Client Shared Skill,
stage by stage. Given the same configuration and inputs, execution SHALL be reproducible
within stated bounds.

---

# Execution Stages

```
Stage 1  Intake And Scope Confinement
Stage 2  Rate Permit Acquisition
Stage 3  Authentication
Stage 4  Mutation Gating
Stage 5  Operation Execution
Stage 6  Metadata Observation
Stage 7  Evidence And Events
```

---

# Stage 1 — Intake And Scope Confinement

The client SHALL validate the operation and confine it to authorized accounts, regions,
and services. An operation outside scope SHALL be rejected before any request.

---

# Stage 2 — Rate Permit Acquisition

The client SHALL acquire a permit from the [Rate Limiter](../rate-limiter/README.md)
before contacting any service endpoint.

---

# Stage 3 — Authentication

The client SHALL authenticate through the
[Authentication](../authentication/README.md) package, resolving credentials through
the [Secrets Client](../secrets-client/README.md). Credentials SHALL NOT be logged or
placed in evidence.

---

# Stage 4 — Mutation Gating

For mutating operations, the client SHALL consult the
[Policy Engine](../policy-engine/README.md). Only an `allow` decision permits the
mutation. A `requires_approval` decision SHALL defer it; a `deny` decision SHALL
suppress it.

---

# Stage 5 — Operation Execution

The client SHALL perform the operation through the
[HTTP Client](../http-client/README.md) over TLS, honoring pagination bounds. Read
operations preserve provider-native resource models in results. Transient failures MAY
be retried through the [Retry](../retry/README.md) shared skill.

---

# Stage 6 — Metadata Observation

The client SHALL observe IAM, network, configuration, and instance-metadata data as
configured and record it as data, never as findings.

---

# Stage 7 — Evidence And Events

The client SHALL capture [Evidence](../../../schemas/evidence.md) and publish lifecycle
events. Credentials and sensitive contents SHALL be redacted.

---

# Determinism

Given identical configuration, scope, and service state, the client SHALL produce
identical bounded results. Provider-side variability SHALL be reflected faithfully in
evidence.

---

# Idempotence

Read operations SHALL NOT alter account state. Mutations SHALL occur only when gated and
authorized, and SHALL be recorded.

---

# Related Documents

- [interface.md](interface.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
- [examples.md](examples.md)
