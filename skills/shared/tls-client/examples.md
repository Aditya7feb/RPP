# TLS Client Examples

**File:** `skills/shared/tls-client/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides illustrative examples for consuming the TLS Client Shared Skill.

Examples are not exhaustive. All requests SHALL satisfy `interface.md`, and all returned objects SHALL conform to the canonical TLS schemas.

---

# Example Categories

```
Recon Metadata Collection

↓

HTTP Transport Setup

↓

Report-Only Validation

↓

Connection Close

↓

Validation Failure
```

---

# Recon Metadata Collection

Recon has identified an in-scope HTTPS endpoint and needs transport facts, not a finding.

Request

```yaml
operation: network.tls.connect
metadata:
  request_id: recon-tls-001
  assessment_id: assessment-2026-001
  task_id: recon-https-003
  skill_id: recon
  timestamp: '2026-07-25T10:00:00Z'
target:
  host: www.example.com
  port: 443
  transport_protocol: tcp
tls:
  server_name: www.example.com
  validation_policy: strict
options:
  evidence_mode: summary
```

Response

```yaml
status: succeeded
connection:
  connection_id: tlsconn-recon-001
  state: open
handshake:
  handshake_id: tlshs-01
  negotiated_protocol: TLSv1.3
  negotiated_alpn: h2
validation:
  validation_id: tlsval-01
  status: valid
evidence:
  - evidence-tls-01
```

Recon MAY use the negotiated protocol, certificate issuer, and evidence reference to populate inventory data.

Recon SHALL NOT label an expired or untrusted certificate as a vulnerability without its own authorized finding workflow.

---

# HTTP Transport Setup

The HTTP Client requests a TLS connection before sending HTTP bytes.

Request

```yaml
operation: network.tls.connect
metadata:
  request_id: http-tls-001
  assessment_id: assessment-2026-001
  task_id: http-get-010
  skill_id: shared.http-client
  timestamp: '2026-07-25T10:01:00Z'
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
```

Consumer behavior

- The HTTP Client SHALL send HTTP only after `status: succeeded` and `connection.state: open`.
- The HTTP Client SHOULD use `handshake.negotiated_alpn` to select HTTP framing.
- The HTTP Client SHALL attach TLS evidence references to its HTTP evidence.
- The HTTP Client SHALL call `network.tls.close` when it does not retain the connection.

---

# Report-Only Validation

Report-only mode allows consumers to observe validation failures without rejecting the connection.

Request fragment

```yaml
tls:
  server_name: legacy.example.com
  validation_policy: report_only
```

Expected behavior

- The connection MAY remain open.
- `validation.status` MAY be `invalid`.
- Validation reasons SHALL be returned.
- Evidence SHALL be captured.
- Consumers SHALL explicitly decide whether to proceed.

---

# Disabled Validation

Disabled validation requires explicit policy authorization.

Request fragment

```yaml
tls:
  server_name: lab.example.com
  validation_policy: disabled
```

Expected behavior

- Validation SHALL report `not_checked`.
- Evidence SHALL record that validation was disabled.
- Consumers SHALL NOT treat the connection as trusted.

---

# Session Resumption

A consumer MAY request resumption using an eligible session reference.

Request fragment

```yaml
operation: network.tls.session.resume
metadata:
  request_id: tls-resume-001
  assessment_id: assessment-2026-001
  task_id: http-get-011
  skill_id: shared.http-client
  timestamp: '2026-07-25T10:02:00Z'
target:
  host: api.example.com
  port: 443
  transport_protocol: tcp
tls:
  server_name: api.example.com
  validation_policy: strict
  session_reference: tlssession-01
```

Expected behavior

- Resumption SHALL be attempted only within the configured isolation scope.
- The response SHALL indicate whether resumption was attempted and accepted.
- The client SHALL NOT claim resumption merely because a new connection succeeded.

---

# Connection Close

Consumers SHOULD close connection handles when finished.

Request

```yaml
operation: network.tls.close
metadata:
  request_id: tls-close-001
  assessment_id: assessment-2026-001
  task_id: http-get-010
  skill_id: shared.http-client
  timestamp: '2026-07-25T10:03:00Z'
connection_id: tlsconn-recon-001
```

Expected behavior

- The TLS Client SHALL release adapter resources.
- The connection state SHALL transition to `closed`.
- A close event SHOULD be published.

---

# Validation Failure

A strict validation failure returns a canonical error instead of an open connection.

Example response

```yaml
error_id: tlserr-01
category: Validation
code: TLS_HOSTNAME_MISMATCH
message: Peer certificate does not match the requested server name.
severity: error
recoverable: false
retryable: false
timestamp: '2026-07-25T10:00:01Z'
request_id: recon-tls-001
target:
  host: www.example.com
  port: 443
evidence:
  - evidence-tls-01
```

The consumer MAY use the evidence and validation result for later analysis.

The TLS Client SHALL NOT generate a security finding.

---

# Anti-Pattern Example

Consumers SHOULD NOT invoke OpenSSL directly.

Invalid pattern

```yaml
tool: openssl
args: s_client -connect api.example.com:443
```

Correct pattern

```yaml
operation: network.tls.connect
target:
  host: api.example.com
  port: 443
  transport_protocol: tcp
```

---

# Success Criteria

These examples demonstrate that consumers can perform TLS operations through a stable shared interface while preserving boundaries between transport observation, evidence collection, and security interpretation.
