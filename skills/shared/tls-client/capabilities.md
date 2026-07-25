# TLS Client Capability Model

**File:** `skills/shared/tls-client/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document defines the canonical capabilities provided by the TLS Client Shared Skill.

Capabilities describe reusable TLS operations that may be composed by shared skills, domain skills, workflows, and agents throughout the Robust PenTest Platform (RPP).

Capabilities define **what** the TLS Client provides rather than **how** TLS operations are implemented.

---

# Design Principles

TLS capabilities SHALL be

- Reusable
- Deterministic
- Observable
- Secure
- Composable
- Adapter independent
- Policy aware

---

# Capability Categories

```
Connection Management

↓

TLS Negotiation

↓

Certificate Inspection

↓

Validation

↓

Session Management

↓

Normalization

↓

Evidence

↓

Observability
```

---

# Capability Registry

---

# Connection Management

## network.tls.connect

Open a TLS connection and return normalized connection data.

Responsibilities

- Resolve TLS configuration
- Select a compatible adapter
- Establish the underlying transport
- Perform the TLS handshake
- Run configured validation
- Capture evidence
- Return a TLS Connection

Outputs

- TLS Connection
- TLS Handshake
- TLS Validation Result
- Evidence Reference

---

## network.tls.close

Close a TLS connection and release associated resources.

Responsibilities

- Transition the connection state
- Release adapter resources
- Clear ephemeral secrets where supported
- Publish close events

Outputs

- Connection Status

---

# TLS Negotiation

## network.tls.handshake

Negotiate TLS and return normalized handshake data.

Responsibilities

- Apply protocol-version policy
- Apply SNI
- Apply ALPN preferences
- Apply client-authentication context
- Normalize negotiated parameters

Outputs

- TLS Handshake

---

# Certificate Inspection

## network.tls.inspect_certificate

Obtain and normalize the peer certificate chain.

Responsibilities

- Retrieve peer certificates
- Normalize certificate fields
- Preserve raw certificate evidence references
- Return chain ordering

Outputs

- Certificate Chain
- Certificate References
- Evidence Reference

---

# Validation

## network.tls.validate

Evaluate the configured certificate and hostname validation policy.

Responsibilities

- Validate trust chain
- Validate hostname
- Apply revocation policy where configured
- Apply expiration checks
- Produce normalized validation reasons

Outputs

- TLS Validation Result

---

# Session Management

## network.tls.session.resume

Attempt session resumption using an eligible session.

Responsibilities

- Check isolation boundary
- Check target compatibility
- Check client-authentication compatibility
- Attempt resumption only when policy permits
- Report whether resumption was attempted and accepted

Outputs

- TLS Session
- Resumption Status

Failure to resume MUST fall back to a full handshake only when policy permits.

---

# Evidence

## network.tls.evidence.capture

Capture TLS evidence for a connection, handshake, validation result, or certificate chain.

Evidence MAY include

- Target
- Server name
- Negotiated TLS version
- Cipher suite
- ALPN protocol
- Certificate fingerprints
- Validation result
- Timing data
- Adapter profile

Outputs

- Evidence Reference

Evidence SHALL NOT include private keys, decrypted application data, pre-shared keys, or session-ticket secrets.

---

# Observability

## network.tls.events.publish

Publish TLS lifecycle events.

Examples

- TLSConnectionStarted
- TLSHandshakeCompleted
- TLSValidationCompleted
- TLSSessionResumed
- TLSConnectionClosed
- TLSConnectionFailed

---

## network.tls.metrics.collect

Collect TLS timing and execution metrics.

Examples

- Connect Duration
- Handshake Duration
- Validation Duration
- Certificate Count
- Session Reuse Status

---

# Protocol Support

The TLS Client SHALL support TLS 1.2 and TLS 1.3 when the selected adapter supports them.

The TLS Client MAY support DTLS only through a separately declared adapter profile.

SSLv2, SSLv3, TLS 1.0, and TLS 1.1 SHALL be disabled by default and MAY be enabled only by explicit, assessment-scoped policy.

---

# Capability Composition

Example

```
HTTP Client

↓

TLS Client

├── network.tls.connect
├── network.tls.handshake
├── network.tls.validate
└── network.tls.evidence.capture
```

Capabilities SHOULD compose rather than duplicate functionality.

---

# Dependencies

The TLS Client Shared Skill depends on

- Configuration Model
- Execution Model
- Authentication Shared Skill
- Logging
- Evidence
- Error Handling

---

# Constraints

The TLS Client SHALL NOT

- Detect vulnerabilities
- Generate findings
- Select targets
- Expose adapter-specific APIs
- Return raw tool output
- Relax validation policy silently

---

# Versioning

Capability identifiers SHALL remain stable across minor releases.

Breaking capability changes SHALL require a major version increment.

---

# Validation Rules

A compliant implementation SHALL

- Publish supported capabilities
- Produce normalized TLS objects
- Respect validation policy
- Preserve evidence
- Support observability
- Remain adapter independent

---

# Quality Requirements

The TLS Capability Model SHALL

- Support canonical TLS connection handling
- Support certificate-chain retrieval
- Support explicit validation policy
- Produce normalized responses
- Capture evidence
- Support observability
- Remain implementation independent

---

# Future Extensions

Future versions MAY support

- DTLS
- QUIC/TLS metadata
- OCSP stapling evidence
- CRL checks
- Certificate-transparency metadata
- Adapter health scoring

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant TLS Capability Model provides a standardized, reusable set of TLS operations for the Robust PenTest Platform.

It enables consistent TLS negotiation, certificate inspection, validation, evidence generation, and observability while remaining independent of TLS libraries, utilities, and operating-system implementations.
