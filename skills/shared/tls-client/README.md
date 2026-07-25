# TLS Client Shared Skill

**File:** `skills/shared/tls-client/README.md`

**Version:** 1.0.0

---

# Purpose

The TLS Client Shared Skill provides the canonical mechanism for establishing and observing Transport Layer Security (TLS) connections within the Robust PenTest Platform (RPP).

Rather than allowing individual skills to negotiate TLS directly through OpenSSL, Go TLS, rustls, Schannel, Kali MCP, or other implementation-specific libraries, this shared skill centralizes TLS negotiation, certificate retrieval, validation policy handling, evidence collection, session management, and observability.

Consumers SHALL delegate TLS operations to this shared skill.

---

# Goals

The TLS Client Shared Skill SHALL

- Abstract TLS implementations
- Support TLS negotiation
- Support certificate-chain retrieval
- Support certificate and hostname validation
- Support client authentication where configured
- Support session reuse within isolation policy
- Produce canonical TLS schemas
- Capture TLS evidence
- Integrate with platform observability

---

# Non-Goals

The TLS Client Shared Skill SHALL NOT

- Detect vulnerabilities
- Generate security findings
- Assign finding severity
- Enumerate targets
- Interpret a validation failure as a reportable issue
- Replace the HTTP Client
- Expose adapter-specific TLS APIs to consumers

Those responsibilities belong to higher-level domain skills, workflows, and agents.

---

# Architecture

```
Master Agent

↓

Domain Skill / HTTP Client / Recon

↓

TLS Client Shared Skill

├── Configuration Resolver
├── Adapter Selector
├── Handshake Manager
├── Certificate Normalizer
├── Validation Manager
├── Session Manager
├── Evidence Manager
└── Event Manager

↓

TLS Adapter

↓

Target
```

The HTTP Client SHALL use the TLS Client for HTTPS transport. Recon MAY use it to collect TLS metadata for an in-scope endpoint. Domain skills MAY consume TLS observations, but interpretation remains outside this shared skill.

---

# Responsibilities

The TLS Client Shared Skill is responsible for

- TLS connection setup
- TLS handshake execution
- Protocol and ALPN negotiation
- SNI handling
- Peer certificate retrieval
- Certificate-chain normalization
- Certificate and hostname validation
- Client-certificate integration
- Session-ticket and session-ID handling
- Evidence generation
- Metrics collection
- Lifecycle event publication

The TLS Client SHALL NOT determine security findings.

---

# Provided Capabilities

The TLS Client SHALL expose

```
network.tls.connect

network.tls.handshake

network.tls.inspect_certificate

network.tls.validate

network.tls.session.resume

network.tls.close
```

Additional capabilities MAY be introduced when they preserve the implementation-independent contract.

---

# Typical Consumers

The following platform components commonly depend on the TLS Client

- HTTP Client
- Browser
- Recon
- Technology Fingerprinting
- Certificate Inventory
- Service Enumeration
- API Testing
- Domain Skills requiring HTTPS transport

---

# Supported Protocols

The TLS Client SHALL support TLS 1.2 and TLS 1.3 when supported by the selected adapter.

Legacy protocols

```
SSLv2

SSLv3

TLS 1.0

TLS 1.1
```

SHALL be disabled by default and MAY be enabled only by explicit, assessment-scoped policy.

DTLS MAY be supported only through a separately declared adapter profile. DTLS data SHALL NOT be represented as ordinary TLS without an explicit `transport_protocol` value.

---

# Validation Policy

Certificate validation SHALL be explicit.

Supported validation modes include

```
strict

report_only

disabled
```

`strict` SHALL require a trusted certificate chain and hostname match. `report_only` SHALL complete validation and report failures without rejecting the connection. `disabled` SHALL record that validation was not performed and SHOULD require assessment policy authorization.

---

# Canonical Outputs

Successful operations return canonical objects including

- TLS Connection
- TLS Handshake
- TLS Session
- Certificate Chain
- Certificate
- TLS Validation Result
- Evidence references
- Timing metrics
- Lifecycle status

Outputs SHALL conform to

```
schemas/tls-connection.md

schemas/tls-handshake.md

schemas/tls-session.md

schemas/certificate-chain.md

schemas/certificate.md

schemas/tls-validation-result.md
```

---

# Evidence

Every network handshake SHOULD generate evidence.

TLS evidence MAY include

- Target host and port
- Server name indication
- Negotiated protocol version
- Negotiated ALPN protocol
- Cipher suite
- Peer certificate fingerprints
- Validation result
- Timing information
- Adapter profile

Evidence SHALL conform to the canonical Evidence schema.

Private keys, decrypted application data, pre-shared keys, and session-ticket secrets SHALL NOT be included in evidence.

---

# Events

The TLS Client SHOULD emit events including

- TLSConnectionStarted
- TLSHandshakeCompleted
- TLSValidationCompleted
- TLSSessionResumed
- TLSConnectionClosed
- TLSConnectionFailed

Events SHALL integrate with Execution State.

---

# Dependencies

The TLS Client depends on

- Configuration Model
- Execution Model
- Error Handling
- Authentication Shared Skill
- Logging
- Evidence
- Execution State

The TLS Client SHALL NOT depend on domain skills.

---

# Configuration

Configurable parameters MAY include

```yaml
minimum_version:

maximum_version:

alpn_protocols:

validation_policy:

hostname_verification:

trust_store_profile:

client_auth:

connect_timeout:

handshake_timeout:

session_reuse:

evidence_mode:
```

Configuration SHALL be resolved before network activity and remain immutable for the request.

---

# Security Considerations

The TLS Client SHALL

- Respect Rules of Engagement
- Preserve authentication boundaries
- Protect private key material
- Avoid leaking session secrets
- Prevent session reuse across assessments
- Preserve auditability
- Normalize peer-observed values without discarding evidentiary data

---

# Documentation Requirements

This shared skill SHOULD include

- README
- capabilities.md
- interface.md
- configuration.md
- execution.md
- error-model.md
- examples.md

---

# Best Practices

Consumers SHOULD

- Use centralized TLS negotiation
- Request certificate validation explicitly
- Preserve TLS evidence references
- Treat connection handles as opaque
- Close connections when finished
- Use report-only validation only when policy permits

---

# Anti-Patterns

Consumers SHOULD NOT

- Execute TLS libraries directly
- Parse raw TLS tool output
- Bypass validation policy silently
- Store private keys in evidence
- Treat certificate observations as findings
- Depend on adapter-specific output
- Reuse TLS sessions across isolation boundaries

---

# Future Extensions

Future versions MAY include

- DTLS support
- QUIC/TLS metadata integration
- Certificate-transparency enrichment
- Trust-store health reporting
- OCSP and CRL evidence capture
- Adapter capability negotiation
- Distributed TLS connection workers

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant TLS Client Shared Skill provides a secure, reusable, and observable mechanism for TLS negotiation across the Robust PenTest Platform.

It enables domain skills to focus on security analysis while delegating transport security, certificate retrieval, validation, evidence generation, and adapter differences to a common, implementation-independent capability.
