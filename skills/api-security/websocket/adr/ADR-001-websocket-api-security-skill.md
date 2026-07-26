# ADR-001 — WebSocket API Security Skill

**File:** `skills/api-security/websocket/adr/ADR-001-websocket-api-security-skill.md`

**Version:** 1.0.0

---

# Status

Accepted

---

# Context

The RPP platform assesses WebSocket APIs, which differ materially from REST, GraphQL,
SOAP, and gRPC. A WebSocket connection begins with an HTTP Upgrade handshake and then
carries bidirectional, long-lived, frame-based messaging. Its security weaknesses are
specific: the handshake may omit Origin validation, enabling Cross-Site WebSocket
Hijacking (CSWSH); the handshake may accept connections without authentication;
message-level authorization may be unenforced over the established channel; and the
connection may run over cleartext transport.

These concerns are not addressed by the REST, GraphQL, SOAP, or gRPC skills, nor by
the Discovery or TLS Analysis skills, whose responsibilities are to inventory Assets
and evaluate general transport posture rather than to evaluate WebSocket handshake and
message authorization behavior.

The platform requires a dedicated, tool-independent WebSocket API Security Skill that
consumes canonical Assets, drives the shared WebSocket Client, gates every action
through the Policy Engine, and emits evidence-backed Findings — without duplicating the
Discovery, TLS Analysis, or Web Security skills, and without performing destructive or
disruptive testing.

---

# Decision

We SHALL provide a WebSocket API Security Skill in the API Security tier with the
following properties.

- It consumes the `api` and `endpoint`
  [Assets](../../../../schemas/asset.md) produced by Discovery and MAY reference the
  set of allowed Origins.
- It drives the [WebSocket Client](../../../shared/websocket-client/README.md) and
  SHALL NOT open connections directly.
- It consults the [Policy Engine](../../../shared/policy-engine/README.md) before
  every target-facing action and honors `allow`, `requires_approval`, and `deny`
  decisions.
- It evaluates WebSocket-specific weaknesses: missing Origin validation / CSWSH
  (CWE-346), missing handshake authentication (CWE-306), missing message-level
  authorization (CWE-285), cleartext transport (CWE-319), and error or close-frame
  disclosure (CWE-209), aligned to the OWASP API Security Top 10 (2023).
- It uses two authorized controlled identities for authorization testing, performs
  minimal confirmations, and never enumerates or exfiltrates other principals' data.
- It bounds message exchanges to avoid denial of service.
- It emits [Findings](../../../../schemas/finding.md) with
  [Risk](../../../../schemas/risk.md), each backed by
  [Evidence](../../../../schemas/evidence.md).
- It delegates general TLS posture to TLS Analysis and generic payload injection
  testing to the Web Security skills.

---

# Consequences

## Positive

- WebSocket-specific weaknesses are assessed within a single, cohesive skill.
- Hijacking, authentication, and authorization testing is bounded, controlled, and
  non-destructive.
- The skill remains tool independent and reuses shared infrastructure and canonical
  schemas.
- Responsibilities remain cleanly separated from Discovery, TLS Analysis, and Web
  Security.

## Negative

- Message authorization testing depends on the availability of two controlled
  identities; without them, those checks are skipped.
- Origin validation analysis is bounded by the provided set of allowed Origins.

## Neutral

- Subprotocol-specific and compression-extension abuse modeling is deferred to future
  extensions.

---

# Alternatives Considered

- Extending the REST skill to cover WebSocket. Rejected because the WebSocket
  handshake, long-lived framing, and CSWSH semantics differ materially and would blur
  the REST skill's responsibilities.
- Handling WebSocket message payload testing within this skill. Rejected because
  generic payload injection belongs to the Web Security skills; this skill focuses on
  handshake and channel authorization concerns.

---

# Related Documents

- [README.md](../README.md)
- [capabilities.md](../capabilities.md)
- [interface.md](../interface.md)
- [WebSocket Client](../../../shared/websocket-client/README.md)
- [Policy Engine](../../../shared/policy-engine/README.md)
