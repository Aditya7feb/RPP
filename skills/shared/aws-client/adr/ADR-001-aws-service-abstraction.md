# ADR-001 — AWS Service Abstraction

**File:** `skills/shared/aws-client/adr/ADR-001-aws-service-abstraction.md`

**Version:** 1.0.0

---

# Status

Accepted

---

# Context

The RPP platform assesses AWS environments. Assessment skills require access to AWS
control-plane services (IAM, EC2, networking, configuration) and the instance metadata
service. Allowing each skill to call AWS service APIs directly would scatter transport,
authentication, pagination, and scope-confinement concerns across domain skills, couple
them to specific SDKs, and risk unbounded enumeration or unauthorized mutation.

The platform already establishes a "one canonical client per access medium or provider"
pattern through the HTTP, gRPC, WebSocket, Kubernetes, and Cloud Storage clients. AWS
has a rich, provider-specific resource model that a provider-agnostic abstraction would
obscure, reducing the fidelity domain skills need to interpret posture.

A dedicated, provider-native AWS client is required: one that confines scope,
authenticates through the Authentication tier, prefers reads, gates mutations through the
Policy Engine, and reports provider-native metadata as data, while leaving all
interpretation to the AWS domain skill.

---

# Decision

We SHALL provide an AWS Client Shared Skill with the following properties.

- It abstracts AWS service access behind a stable, provider-native interface that
  preserves AWS resource models.
- It performs requests through the [HTTP Client](../../http-client/README.md) over TLS
  and SHALL NOT embed transport implementations.
- It authenticates through the [Authentication](../../authentication/README.md) package,
  resolving credentials through the [Secrets Client](../../secrets-client/README.md).
- It confines operations to authorized accounts, regions, and services, rejecting
  out-of-scope targets.
- It prefers describe, list, and get operations and gates create, update, delete, and tag
  as intrusive through the [Policy Engine](../../policy-engine/README.md).
- It observes IAM, network, configuration, and instance-metadata data and reports it as
  data, never as findings or risk.
- It captures [Evidence](../../../../schemas/evidence.md) with credentials redacted.
- It contains no cloud-domain assessment logic.

---

# Consequences

## Positive

- AWS transport, authentication, scope, and pagination are centralized and auditable.
- Domain skills receive provider-native models with full fidelity for interpretation.
- Mutations are consistently gated; reads are bounded.
- The client remains implementation independent and reuses shared infrastructure.

## Negative

- Provider-native modeling ties the client to AWS resource shapes, requiring maintenance
  as services evolve.

## Neutral

- Organization-wide aggregation and config-recorder snapshots are deferred to future
  extensions.

---

# Alternatives Considered

- A single provider-agnostic cloud client. Rejected because it would hide provider-specific
  resource models that domain skills require, contrary to the established one-client-per-
  provider pattern.
- Direct AWS SDK use within domain skills. Rejected because it couples skills to
  implementations and scatters scope, authentication, and mutation-gating concerns.

---

# Related Documents

- [README.md](../README.md)
- [capabilities.md](../capabilities.md)
- [interface.md](../interface.md)
- [HTTP Client](../../http-client/README.md)
- [Policy Engine](../../policy-engine/README.md)
