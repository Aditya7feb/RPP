# TLS Client Execution Model

**File:** `skills/shared/tls-client/execution.md`

**Version:** 1.0.0

---

# Purpose

The TLS Client Execution Model defines how TLS operations are planned, validated, executed, observed, and completed.

Execution SHALL remain deterministic, policy aware, evidence producing, and independent of the selected TLS adapter.

---

# Execution Lifecycle

```
Receive Request

↓

Validate Request and Policy

↓

Resolve Configuration

↓

Select Adapter

↓

Connect Transport

↓

Negotiate TLS

↓

Normalize Peer Data

↓

Validate Peer

↓

Create Evidence

↓

Publish Events

↓

Return Result or Error

↓

Close or Release Resources
```

---

# Request Validation

The TLS Client SHALL validate the interface request before network activity.

Validation includes

- Metadata presence
- Target host format
- Target port range
- Transport policy
- TLS parameter compatibility
- Validation policy
- Timeout values
- Evidence mode

Invalid inputs SHALL fail with a `Configuration` or `Request` error.

---

# Configuration Resolution

The TLS Client SHALL resolve immutable configuration before selecting an adapter.

Resolved configuration SHALL include

- Protocol version policy
- ALPN preferences
- Validation policy
- Trust-store profile
- Client-authentication context
- Timeout policy
- Retry policy
- Session policy
- Evidence policy

The resolved configuration SHALL be traceable in evidence or execution metadata.

---

# Adapter Selection

The TLS Client SHALL select a compatible adapter based on resolved configuration and adapter capability declarations.

Consumers SHALL remain unaware of the selected implementation.

Raw adapter identifiers MAY appear only in protected diagnostics or namespaced `extensions`.

---

# Connection Setup

The TLS Client SHALL establish the configured transport before TLS negotiation.

Connection setup SHALL

- Respect scope and Rules of Engagement
- Honor connect timeouts
- Publish `TLSConnectionStarted`
- Fail safely on cancellation or network error

---

# Handshake Execution

The TLS Client SHALL perform the handshake using the resolved TLS configuration.

Handshake execution SHALL apply

- Protocol-version policy
- SNI
- ALPN preferences
- Client authentication
- Session resumption eligibility

Negotiated values SHALL be normalized into canonical TLS schemas.

---

# Peer Data Normalization

The TLS Client SHALL normalize

- TLS Connection
- TLS Handshake
- TLS Session
- Certificate Chain
- Certificate
- TLS Validation Result

Raw peer-observed values needed as evidence SHALL be preserved through evidence references or namespaced extensions.

---

# Validation

The TLS Client SHALL evaluate configured validation after peer data is available.

In `strict` mode, validation failure SHALL prevent an `open` connection result.

In `report_only` mode, validation failure MAY return an open connection and SHALL include validation reasons.

In `disabled` mode, validation SHALL report `not_checked`.

---

# Evidence Collection

The TLS Client SHALL generate evidence according to resolved evidence policy.

Evidence collection SHOULD include

- Target
- Handshake metadata
- Certificate fingerprints
- Validation result
- Timings
- Adapter profile

Evidence SHALL NOT include private keys, decrypted application data, pre-shared keys, or session-ticket secrets.

---

# Event Publication

The TLS Client SHOULD publish lifecycle events including

- TLSConnectionStarted
- TLSHandshakeCompleted
- TLSValidationCompleted
- TLSSessionResumed
- TLSConnectionClosed
- TLSConnectionFailed

Events SHALL update Execution State.

---

# Session Rules

Session resumption MAY be attempted only for a compatible

- Server name
- Port
- Transport
- Protocol policy
- Client-authentication context
- Isolation scope

The TLS Client SHALL NOT serialize session secrets into logs or evidence.

---

# Resource Cleanup

The TLS Client SHALL

- Close failed transports
- Release adapter resources
- Clear ephemeral key material where supported
- Treat connection handles as invalid after `closed` or `failed`

Consumers that request `network.tls.close` SHALL receive a final connection state.

---

# Determinism

The TLS Client SHOULD preserve request ordering for a single consumer.

Retries, session reuse, and fallback behavior SHALL be governed only by resolved configuration and policy.

---

# Cancellation

The TLS Client SHALL honor cancellation and timeouts at each blocking stage.

Cancellation SHALL produce a canonical `Cancelled` error, emit `TLSConnectionFailed`, and preserve only already-collected safe evidence.

---

# Failure Handling

Failed operations SHALL return canonical errors.

Partial adapter output SHALL NOT be returned as a successful response.

Diagnostic data MAY be retained only in protected storage.

---

# Success Criteria

A compliant TLS Client Execution Model provides predictable, observable, and policy-controlled TLS execution.

It ensures that every TLS operation is validated, normalized, evidenced, and cleaned up consistently across adapters and consumers.
