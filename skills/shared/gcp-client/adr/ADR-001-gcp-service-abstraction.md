# ADR-001 — GCP Service Abstraction

**File:** `skills/shared/gcp-client/adr/ADR-001-gcp-service-abstraction.md`

**Version:** 1.0.0

---

# Status

Accepted

---

# Context

The RPP platform assesses GCP environments. Assessment skills require access to GCP
control-plane services (IAM policy bindings, compute, networking, configuration) and the
GCP metadata server. Allowing each skill to call GCP service APIs directly would scatter
transport, authentication, pagination, and scope-confinement concerns across domain skills,
couple them to specific SDKs, and risk unbounded enumeration or unauthorized mutation.

The platform already establishes a "one canonical client per access medium or provider"
pattern through the HTTP, gRPC, WebSocket, Kubernetes, and Cloud Storage clients. GCP has a
rich, provider-specific resource model (organizations, projects, IAM policy bindings) that a
provider-agnostic abstraction would obscure, reducing the fidelity domain skills need to
interpret posture.

A dedicated, provider-native GCP client is required: one that confines scope, authenticates
through the Authentication tier, prefers reads, gates mutations through the Policy Engine,
and reports provider-native metadata as data, while leaving all interpretation to the GCP
domain skill.

---

# Decision

We SHALL provide a GCP Client Shared Skill with the following properties.

- It abstracts GCP service access behind a stable, provider-native interface that preserves
  GCP resource models.
- It performs requests through the [HTTP Client](../../http-client/README.md) over TLS and
  SHALL NOT embed transport implementations.
- It authenticates through the [Authentication](../../authentication/README.md) package,
  resolving credentials through the [Secrets Client](../../secrets-client/README.md).
- It confines operations to authorized organizations, projects, regions, and services,
  rejecting out-of-scope targets.
- It prefers get and list operations and gates create, update, delete, and set-iam-policy as
  intrusive through the [Policy Engine](../../policy-engine/README.md).
- It observes IAM, network, configuration, and metadata-server data and reports it as data,
  never as findings or risk.
- It captures [Evidence](../../../../schemas/evidence.md) with credentials redacted.
- It contains no cloud-domain assessment logic.

---

# Consequences

## Positive

- GCP transport, authentication, scope, and pagination are centralized and auditable.
- Domain skills receive provider-native models with full fidelity for interpretation.
- Mutations are consistently gated; reads are bounded.
- The client remains implementation independent and reuses shared infrastructure.

## Negative

- Provider-native modeling ties the client to GCP resource shapes, requiring maintenance as
  services evolve.

## Neutral

- Organization-policy aggregation and asset-inventory snapshots are deferred to future
  extensions.

---

# Alternatives Considered

- A single provider-agnostic cloud client. Rejected because it would hide provider-specific
  resource models that domain skills require, contrary to the established one-client-per-
  provider pattern.
- Direct GCP SDK use within domain skills. Rejected because it couples skills to
  implementations and scatters scope, authentication, and mutation-gating concerns.

---

# Related Documents

- [README.md](../README.md)
- [capabilities.md](../capabilities.md)
- [interface.md](../interface.md)
- [HTTP Client](../../http-client/README.md)
- [Policy Engine](../../policy-engine/README.md)
