# ADR-001 — WebSocket Transport Abstraction

**File:** `skills/shared/websocket-client/adr/ADR-001-websocket-transport-abstraction.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Robust PenTest Platform must interact with real-time applications that use
WebSocket connections. WebSocket begins with an HTTP upgrade handshake, may run
over TLS as `wss`, and then exchanges framed messages over a long-lived
connection.

If each skill negotiated upgrades and framed messages directly, the platform
would suffer

- Duplicated handshake and framing logic
- Inconsistent reuse of existing HTTP and TLS handling
- Unbounded message sizes and connection lifetimes
- Divergent governance and evidence

The platform requires a single, canonical, implementation-independent WebSocket
transport that reuses the existing HTTP and TLS shared skills.

---

# Decision

The platform SHALL provide a dedicated WebSocket Client shared skill that
centralizes WebSocket transport behind a stable interface.

The WebSocket Client shared skill SHALL

- Perform the upgrade handshake through the
  [HTTP Client](../../http-client/README.md), preserving the handshake as an
  [HTTP Transaction](../../../../schemas/http-transaction.md)
- Secure `wss` connections through the [TLS Client](../../tls-client/README.md)
- Exchange bounded text and binary frames and manage control frames
- Negotiate subprotocols and extensions declaratively
- Apply rate, retry, and proxy governance
- Produce evidence conforming to the
  [Evidence schema](../../../../schemas/evidence.md)

Consumers SHALL perform WebSocket transport exclusively through the
[WebSocket Client Interface](../interface.md). The WebSocket Client SHALL NOT
interpret message semantics.

---

# Alternatives Considered

## Per-Skill WebSocket Handling

Each skill could negotiate upgrades and frame messages directly.

Rejected because it duplicates logic and fails to reuse existing HTTP and TLS
handling.

## A Standalone Transport Not Reusing HTTP And TLS

WebSocket could reimplement HTTP upgrade and TLS internally.

Rejected because it would duplicate mature, governed handling already provided by
the HTTP and TLS shared skills, including authentication, redirects, and
interception awareness.

## A New WebSocket Message Schema

A canonical WebSocket message schema could be introduced now.

Deferred. Frame structure is described in the interface and evidence, and the
handshake reuses the HTTP Transaction schema. A dedicated message schema MAY be
introduced when a domain WebSocket skill requires canonical message correlation,
avoiding premature schema creation.

---

# Consequences

## Positive

- Uniform WebSocket transport reusing HTTP and TLS handling
- Bounded message sizes and connection lifetimes
- Consistent governance and evidence
- Reusable, testable abstraction independent of adapters

## Negative

- Consumers MUST perform WebSocket through the interface
- An additional shared dependency is introduced
- A future message schema MAY be required for richer correlation

The negative consequences are outweighed by reuse and consistency.

---

# Compliance

Consumers SHALL

- Perform WebSocket through the WebSocket Client Interface
- Bound message sizes and connection lifetime
- Reference shared rate, retry, and proxy policies
- Delegate message semantics to domain skills

---

# Future Compatibility

Future versions MAY add a canonical WebSocket message schema, multiplexed
channels, and flow-control directives. These extensions SHALL preserve the
existing interface and SHALL maintain backward compatibility.

---

# Related Documents

- [WebSocket Client README](../README.md)
- [WebSocket Client Interface](../interface.md)
- [WebSocket Client Execution Model](../execution.md)
- [WebSocket Client Error Model](../error-model.md)
- [HTTP Client](../../http-client/README.md)
- [TLS Client](../../tls-client/README.md)
- [HTTP Transaction Schema](../../../../schemas/http-transaction.md)
- [Evidence Schema](../../../../schemas/evidence.md)
