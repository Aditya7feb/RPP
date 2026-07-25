# TLS Client Error Model

**File:** `skills/shared/tls-client/error-model.md`

**Version:** 1.0.0

---

# Purpose

The TLS Client Error Model defines the canonical errors returned by TLS operations.

All adapter, network, protocol, validation, policy, and resource failures SHALL be normalized into platform-compatible error objects.

---

# Design Principles

TLS errors SHALL be

- Structured
- Deterministic
- Safe to expose
- Retry aware
- Evidence linked
- Adapter independent
- Compatible with platform error handling

---

# Error Contract

Errors SHALL conform to

```
skills/core/error-handling.md
```

Adapter-specific errors SHALL be mapped to canonical TLS error categories and codes.

Raw adapter errors MAY be preserved only in protected diagnostic data.

---

# Canonical Error Shape

Example

```yaml
error_id: tlserr-01
category: Validation
code: TLS_HOSTNAME_MISMATCH
message: Peer certificate does not match the requested server name.
severity: error
recoverable: false
retryable: false
timestamp: '2026-07-25T10:00:01Z'
request_id: req-7a8d
target:
  host: api.example.com
  port: 443
evidence:
  - evidence-tls-01
```

---

# Required Fields

Every TLS error SHALL include

```yaml
error_id:

category:

code:

message:

severity:

recoverable:

retryable:

timestamp:

request_id:

target:
```

`evidence` MAY be empty when no safe artifact was collected.

---

# Message Safety

Error messages SHALL be safe for consumers.

Messages SHALL NOT expose

- Credentials
- Private keys
- Pre-shared keys
- Session-ticket secrets
- Decrypted application data
- Protected adapter diagnostics

---

# Error Categories

TLS errors SHALL use one of the following categories.

---

# Configuration Errors

Configuration errors represent invalid or unsupported resolved configuration.

Example codes

- TLS_INVALID_VERSION_RANGE
- TLS_UNSUPPORTED_ALPN
- TLS_INVALID_EVIDENCE_MODE

Retry rule

Configuration errors SHALL NOT be retried automatically.

---

# Request Errors

Request errors represent invalid invocation input.

Example codes

- TLS_INVALID_HOST
- TLS_INVALID_PORT
- TLS_INVALID_SERVER_NAME

Retry rule

Request errors SHALL NOT be retried automatically.

---

# Adapter Errors

Adapter errors represent unavailable or incompatible TLS implementations.

Example codes

- TLS_ADAPTER_UNAVAILABLE
- TLS_FEATURE_UNSUPPORTED
- TLS_ADAPTER_CAPABILITY_MISMATCH

Retry rule

Adapter errors MAY be retried only after adapter selection changes.

---

# Network Errors

Network errors represent transport failures before or during TLS execution.

Example codes

- TLS_CONNECT_FAILED
- TLS_CONNECTION_RESET
- TLS_NETWORK_UNREACHABLE

Retry rule

Network errors MAY be retried when configured.

---

# Timeout Errors

Timeout errors represent expired operation deadlines.

Example codes

- TLS_CONNECT_TIMEOUT
- TLS_HANDSHAKE_TIMEOUT
- TLS_VALIDATION_TIMEOUT

Retry rule

Timeout errors MAY be retried when configured.

---

# Handshake Errors

Handshake errors represent TLS negotiation failures.

Example codes

- TLS_HANDSHAKE_FAILED
- TLS_PROTOCOL_NEGOTIATION_FAILED
- TLS_ALPN_NEGOTIATION_FAILED

Retry rule

Handshake errors MAY be retried only if transient evidence supports retry.

---

# Validation Errors

Validation errors represent certificate or hostname validation failures.

Example codes

- TLS_UNTRUSTED_CHAIN
- TLS_HOSTNAME_MISMATCH
- TLS_CERTIFICATE_EXPIRED
- TLS_REVOCATION_UNKNOWN

Retry rule

Validation errors SHALL NOT be retried automatically.

Validation failures SHALL include a TLS Validation Result when validation began.

---

# Client Authentication Errors

Client authentication errors represent missing, invalid, or rejected client authentication material.

Example codes

- TLS_CLIENT_CERTIFICATE_REQUIRED
- TLS_CLIENT_AUTH_FAILED
- TLS_CLIENT_AUTH_MATERIAL_UNAVAILABLE

Retry rule

Client authentication errors SHALL NOT be retried automatically.

---

# Policy Errors

Policy errors represent denied behavior under platform, assessment, or workflow policy.

Example codes

- TLS_POLICY_DENIED
- TLS_INSECURE_VERSION_DENIED
- TLS_VALIDATION_DISABLED_DENIED

Retry rule

Policy errors SHALL NOT be retried.

---

# Resource Errors

Resource errors represent exhausted or invalid TLS resources.

Example codes

- TLS_RESOURCE_EXHAUSTED
- TLS_SESSION_INVALID
- TLS_CONNECTION_HANDLE_INVALID

Retry rule

Resource errors MAY be retried after recovery.

---

# Cancelled Errors

Cancelled errors represent user, workflow, or platform cancellation.

Example codes

- TLS_CANCELLED

Retry rule

Cancelled errors SHALL NOT be retried automatically.

---

# Internal Errors

Internal errors represent unexpected platform or adapter failures.

Example codes

- TLS_INTERNAL_ERROR
- TLS_NORMALIZATION_FAILED

Retry rule

Internal errors MAY be retried only if platform policy permits.

---

# Event Requirements

The TLS Client SHALL publish `TLSConnectionFailed` for every error.

Failure events SHALL include

- request_id
- assessment_id
- task_id
- timestamp
- error category
- error code
- status

---

# Evidence Requirements

Errors SHOULD reference safe evidence when available.

Evidence SHALL NOT include secret material or protected diagnostics.

Validation failures SHOULD reference certificate and validation evidence.

---

# Success Criteria

A compliant TLS Client Error Model converts implementation-specific TLS failures into safe, stable, retry-aware platform errors.

It enables consumers to handle TLS failures consistently without depending on adapter behavior or raw tool output.
