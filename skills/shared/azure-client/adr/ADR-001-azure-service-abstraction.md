# ADR-001 — Azure Service Abstraction

**File:** `skills/shared/azure-client/adr/ADR-001-azure-service-abstraction.md`

**Version:** 1.0.0

---

# Status

Accepted

---

# Context

The RPP platform assesses Azure environments. Assessment skills require access to Azure
Resource Manager control-plane services (Entra ID role assignments, compute, networking,
configuration) and the Azure Instance Metadata Service. Allowing each skill to call Azure
service APIs directly would scatter transport, authentication, pagination, and
scope-confinement concerns across domain skills, couple them to specific SDKs, and risk
unbounded enumeration or unauthorized mutation.

The platform already establishes a "one canonical client per access medium or provider"
pattern through the HTTP, gRPC, WebSocket, Kubernetes, and Cloud Storage clients. Azure
has a rich, provider-specific resource model (subscriptions, resource groups, role
assignments) that a provider-agnostic abstraction would obscure, reducing the fidelity
domain skills need to interpret posture.

A dedicated, provider-native Azure client is required: one that confines scope,
authenticates through the Authentication tier, prefers reads, gates mutations through the
Policy Engine, and reports provider-native metadata as data, while leaving all
interpretation to the Azure domain skill.

---

# Decision

We SHALL provide an Azure Client Shared Skill with the following properties.

- It abstracts Azure service access behind a stable, provider-native interface that
  preserves Azure resource models.
- It performs requests through the [HTTP Client](../../http-client/README.md) over TLS and
  SHALL NOT embed transport implementations.
- It authenticates through the [Authentication](../../authentication/README.md) package,
  resolving credentials through the [Secrets Client](../../secrets-client/README.md).
- It confines operations to authorized subscriptions, resource groups, regions, and
  services, rejecting out-of-scope targets.
- It prefers get and list operations and gates create, update, delete, and tag as
  intrusive through the [Policy Engine](../../policy-engine/README.md).
- It observes role, network, configuration, and instance-metadata data and reports it as
  data, never as findings or risk.
- It captures [Evidence](../../../../schemas/evidence.md) with credentials redacted.
- It contains no cloud-domain assessment logic.

---

# Consequences

## Positive

- Azure transport, authentication, scope, and pagination are centralized and auditable.
- Domain skills receive provider-native models with full fidelity for interpretation.
- Mutations are consistently gated; reads are bounded.
- The client remains implementation independent and reuses shared infrastructure.

## Negative

- Provider-native modeling ties the client to Azure resource shapes, requiring maintenance
  as services evolve.

## Neutral

- Management-group aggregation and Azure Policy state snapshots are deferred to future
  extensions.

---

# Alternatives Considered

- A single provider-agnostic cloud client. Rejected because it would hide provider-specific
  resource models that domain skills require, contrary to the established one-client-per-
  provider pattern.
- Direct Azure SDK use within domain skills. Rejected because it couples skills to
  implementations and scatters scope, authentication, and mutation-gating concerns.

---

# Related Documents

- [README.md](../README.md)
- [capabilities.md](../capabilities.md)
- [interface.md](../interface.md)
- [HTTP Client](../../http-client/README.md)
- [Policy Engine](../../policy-engine/README.md)
