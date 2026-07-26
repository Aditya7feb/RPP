# ADR-001 — Container Engine Abstraction

**File:** `skills/shared/container-client/adr/ADR-001-container-engine-abstraction.md`

**Version:** 1.0.0

---

# Status

Accepted

---

# Context

The RPP platform assesses container platforms. Assessment skills require access to a
container engine to inspect images, containers, networks, and daemon configuration. Allowing
each skill to call a container engine directly would scatter transport, authentication,
inspection-bounding, and scope-confinement concerns across domain skills, couple them to
specific engine implementations, and risk unauthorized mutation or workload execution.

The platform already establishes a "one canonical client per access medium or provider"
pattern through the HTTP, gRPC, WebSocket, Kubernetes, and Cloud Storage clients. A container
engine has a provider-specific resource model (images, layers, containers, daemon
configuration) that a provider-agnostic abstraction would obscure, reducing the fidelity
domain skills need to interpret posture. A Container Client was anticipated during shared
infrastructure planning but not yet realized.

A dedicated, provider-native container client is required: one that confines scope,
authenticates through the Authentication tier, prefers reads, gates mutations and workload
execution through the Policy Engine, and reports provider-native metadata as data, while
leaving all interpretation to the Docker domain skill.

---

# Decision

We SHALL provide a Container Client Shared Skill with the following properties.

- It abstracts container-engine access behind a stable, provider-native interface that
  preserves container resource models.
- It performs requests through the [HTTP Client](../../http-client/README.md) where the
  engine exposes an HTTP API and reads image or layer contents through the
  [Filesystem Client](../../filesystem-client/README.md) where authorized.
- It authenticates through the [Authentication](../../authentication/README.md) package,
  resolving credentials through the [Secrets Client](../../secrets-client/README.md).
- It confines operations to authorized engines, images, and containers, rejecting
  out-of-scope targets.
- It prefers inspect, list, and get operations and gates run, exec, stop, and remove as
  intrusive through the [Policy Engine](../../policy-engine/README.md), with run and exec
  requiring elevated authorization.
- It observes image, container, network, and daemon configuration and reports it as data,
  never as findings or risk.
- It captures [Evidence](../../../../schemas/evidence.md) with credentials redacted.
- It contains no container-domain assessment logic.

---

# Consequences

## Positive

- Container transport, authentication, scope, and inspection bounds are centralized and
  auditable.
- Domain skills receive provider-native models with full fidelity for interpretation.
- Mutations and workload execution are consistently gated; reads are bounded.
- The client remains implementation independent and reuses shared infrastructure.

## Negative

- Provider-native modeling ties the client to container resource shapes, requiring
  maintenance as engines evolve.

## Neutral

- Image signature and provenance descriptors are deferred to future extensions.

---

# Alternatives Considered

- A single provider-agnostic cloud client. Rejected because it would hide the container
  resource model that the Docker domain skill requires, contrary to the established
  one-client-per-provider pattern.
- Composing filesystem and HTTP clients directly within the Docker skill. Rejected because it
  scatters engine transport, scope, and mutation-gating concerns into a domain skill and
  risks tool-coupled logic.

---

# Related Documents

- [README.md](../README.md)
- [capabilities.md](../capabilities.md)
- [interface.md](../interface.md)
- [HTTP Client](../../http-client/README.md)
- [Filesystem Client](../../filesystem-client/README.md)
- [Policy Engine](../../policy-engine/README.md)
