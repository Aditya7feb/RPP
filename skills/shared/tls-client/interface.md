# TLS Client Interface

**File:** `skills/shared/tls-client/interface.md`

**Version:** 1.0.0

---

# Purpose

The TLS Client Interface defines the canonical contract through which platform components perform TLS operations.

It provides a stable, implementation-independent interface for TLS connection setup, handshake negotiation, certificate inspection, validation, session reuse, evidence generation, and error handling.

All consumers SHALL interact with TLS exclusively through this interface.

---

# Design Principles

The interface SHALL be

- Stable
- Versioned
- Deterministic
- Observable
- Secure
- Adapter independent
- Backward compatible

---

# Relationship

```
Master Agent

↓

Workflow

↓

Domain Skill / Shared Skill

↓

TLS Client Interface

↓

TLS Client Shared Skill

↓

TLS Adapter

↓

Target
```

Consumers SHALL NOT communicate directly with TLS libraries, command-line tools, or operating-system TLS APIs.

---

# Interface Overview

The interface consists of

```
Metadata

↓

Target

↓

TLS Request

↓

Execution Options

↓

TLS Response

↓

Evidence

↓

Metrics

↓

Errors
```

---

# Metadata

Every TLS invocation SHALL include

```yaml
request_id:

assessment_id:

task_id:

skill_id:

timestamp:
```

Metadata enables traceability and auditing.

`timestamp` SHALL be an RFC 3339 UTC timestamp.

---

# TLS Request

Every request SHALL define

```yaml
operation:

metadata:

target:

tls:

options:
```

---

# Supported Operations

The TLS Client SHALL support

```
network.tls.connect

network.tls.handshake

network.tls.inspect_certificate

network.tls.validate

network.tls.session.resume

network.tls.close
```

Additional operations MAY be introduced without breaking existing consumers.

---

# Target Definition

Each TLS target SHALL specify

```yaml
host:

port:

transport_protocol:
```

`host` SHALL be a DNS name or IP literal. `port` SHALL be an integer from 1 through 65535. `transport_protocol` SHALL be `tcp` unless a DTLS-enabled adapter and policy explicitly allow `udp`.

---

# TLS Parameters

TLS parameters MAY include

```yaml
server_name:

alpn_protocols:

validation_policy:

client_auth:

session_reference:
```

`server_name` SHOULD be the intended DNS hostname and SHALL NOT be an IP literal.

`validation_policy` SHALL be one of

```
strict

report_only

disabled
```

Secret values SHALL NOT be embedded in TLS requests. Client authentication material SHALL be referenced through the shared Authentication skill.

---

# Execution Options

Execution options MAY include

```yaml
connect_timeout_ms:

handshake_timeout_ms:

total_timeout_ms:

evidence_mode:

adapter_profile:

retry_policy:
```

Adapter profiles SHALL remain opaque to consumers.

---

# Connect Request Example

```yaml
operation: network.tls.connect
metadata:
  request_id: req-7a8d
  assessment_id: assessment-2026-001
  task_id: task-042
  skill_id: shared.tls-client
  timestamp: '2026-07-25T10:00:00Z'
target:
  host: api.example.com
  port: 443
  transport_protocol: tcp
tls:
  server_name: api.example.com
  alpn_protocols: [h2, http/1.1]
  validation_policy: strict
options:
  connect_timeout_ms: 5000
  handshake_timeout_ms: 10000
  evidence_mode: summary
```

---

# TLS Response

Successful operations SHALL return normalized TLS objects.

Example

```yaml
status: succeeded
connection:
  connection_id: tlsconn-01
  state: open
handshake:
  handshake_id: tlshs-01
  negotiated_protocol: TLSv1.3
certificate_chain:
  chain_id: tlschain-01
  certificates: [cert-leaf-01]
validation:
  validation_id: tlsval-01
  status: valid
evidence:
  - evidence-tls-01
metrics:
  connect_duration_ms: 21
  handshake_duration_ms: 83
```

Raw adapter output SHALL NOT be exposed.

---

# Required Success Fields

Successful `network.tls.connect` responses SHALL include

```yaml
status:

connection:

handshake:

validation:

evidence:

metrics:
```

`certificate_chain` MAY be absent only when no peer certificate was presented or the protocol does not provide one. The validation result SHALL explain that condition.

---

# Lifecycle Operations

`network.tls.close` requires

```yaml
connection_id:
```

`network.tls.session.resume` requires

```yaml
session_reference:
```

Consumers SHALL treat connection handles as opaque and SHALL close them when finished.

Session resumption SHALL NOT be reported merely because a new connection succeeded.

---

# Evidence

TLS operations SHALL expose structured evidence.

Evidence MAY include

- Target
- Handshake metadata
- Certificate fingerprints
- Validation result
- Timing metrics
- Adapter profile

Evidence SHALL conform to the canonical Evidence schema.

---

# Metrics

TLS metrics MAY include

```yaml
connect_duration_ms:

handshake_duration_ms:

validation_duration_ms:

certificate_count:

session_resumed:
```

Metrics SHOULD integrate with platform observability.

---

# Error Contract

Errors SHALL conform to

```
skills/core/error-handling.md
```

Typical categories include

- Configuration
- Request
- Adapter
- Network
- Timeout
- Handshake
- Validation
- ClientAuth
- Policy
- Resource
- Cancelled
- Internal

---

# Security Requirements

The TLS Client Interface SHALL

- Respect configured validation policies
- Prevent secret leakage
- Prevent session leakage between assessments
- Normalize all TLS responses
- Preserve auditability
- Keep adapter implementation details opaque

---

# Compatibility

Consumers SHALL remain independent of

- openssl
- rustls
- Go TLS
- Schannel
- Secure Transport
- language-specific TLS libraries
- command-line TLS utilities

The TLS response SHALL remain stable across implementations.

---

# Versioning

The interface SHALL follow semantic versioning.

Minor versions MAY introduce optional fields.

Major versions SHALL indicate breaking changes.

---

# Validation Rules

A compliant invocation SHALL include

- Metadata
- Target
- TLS Request
- Execution Options
- TLS Response
- Evidence
- Error Handling

---

# Quality Requirements

The TLS Client Interface SHALL

- Be adapter independent
- Produce normalized responses
- Support explicit validation policy
- Preserve evidence
- Support observability
- Remain backward compatible

---

# Future Extensions

Future versions MAY support

- DTLS
- QUIC/TLS metadata
- Certificate-transparency metadata
- Trust-store introspection
- Adapter capability discovery

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant TLS Client Interface provides a stable, implementation-independent contract for TLS operations across the Robust PenTest Platform.

It enables consistent TLS negotiation, certificate retrieval, validation, evidence generation, and observability while abstracting TLS libraries, tools, and operating-system implementations.
