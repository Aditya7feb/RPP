# HTTP Client Error Model

**File:** `skills/shared/http-client/error-model.md`

**Version:** 1.0.0

---

# Purpose

The HTTP Client Error Model defines how HTTP-specific failures are classified, normalized, reported, and recovered within the Robust PenTest Platform (RPP).

It extends the platform-wide error framework defined in:

```
skills/core/error-handling.md
```

The HTTP Client SHALL normalize transport- and protocol-specific failures into canonical RPP error categories.

---

# Design Principles

Errors SHALL be

- Deterministic
- Structured
- Recoverable where possible
- Observable
- Evidence-backed
- Implementation Independent

---

# Error Lifecycle

```
Failure Occurs

↓

Detect

↓

Classify

↓

Normalize

↓

Capture Evidence

↓

Determine Recovery

↓

Publish Event

↓

Return Canonical Error
```

---

# Error Categories

The HTTP Client SHALL classify errors into one of the following categories.

| Category | Description |
|----------|-------------|
| Validation | Invalid request before execution |
| Configuration | Invalid or conflicting configuration |
| Authentication | Authentication failure |
| Authorization | Access denied |
| Network | Connectivity failures |
| DNS | Name resolution failures |
| Proxy | Proxy configuration or communication failures |
| TLS | Certificate or TLS negotiation failures |
| Timeout | Operation exceeded configured timeout |
| Redirect | Redirect policy violation |
| Protocol | Malformed or unsupported HTTP behavior |
| Response | Invalid or unexpected response |
| Transport | Adapter implementation failure |
| Internal | Unexpected HTTP Client failure |

---

# Canonical Error Structure

Every HTTP Client error SHALL expose

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

adapter:

evidence:
```

---

# Validation Errors

Examples include

- Unsupported HTTP method
- Missing URL
- Invalid header
- Malformed body
- Invalid configuration reference

Validation errors SHALL prevent execution.

---

# Configuration Errors

Examples

- Invalid timeout
- Unsupported proxy type
- Conflicting TLS settings
- Missing authentication profile

Execution SHALL NOT begin.

---

# Authentication Errors

Examples

- Invalid credentials
- Missing token
- Expired token
- Session expired
- Client certificate rejected

Authentication errors SHOULD reference the configured authentication profile.

---

# Authorization Errors

Examples

- HTTP 401
- HTTP 403
- Access denied by upstream

Authorization failures SHALL preserve the response body where permitted.

---

# DNS Errors

Examples

- NXDOMAIN
- Resolution timeout
- Resolver unavailable

Evidence SHOULD include the hostname and resolver information when available.

---

# Network Errors

Examples

- Connection refused
- Connection reset
- Host unreachable
- Broken pipe

Transport-specific exceptions SHALL be normalized.

---

# Proxy Errors

Examples

- Proxy authentication failure
- Proxy unreachable
- Invalid proxy configuration

The configured proxy profile SHOULD be referenced.

---

# TLS Errors

Examples

- Certificate expired
- Hostname mismatch
- Invalid certificate chain
- Unsupported protocol
- Handshake failure

TLS evidence SHOULD include

- Negotiated protocol (if available)
- Presented certificate
- Failure reason

Sensitive key material SHALL NEVER be recorded.

---

# Timeout Errors

Timeout types include

- Connect timeout
- Read timeout
- Total timeout

Timeout duration SHOULD be recorded.

---

# Redirect Errors

Examples

- Redirect loop
- Maximum redirects exceeded
- Redirect blocked by policy

The redirect chain SHOULD be preserved.

---

# Protocol Errors

Examples

- Invalid HTTP version
- Malformed headers
- Invalid chunked encoding
- Unexpected protocol behavior

---

# Response Errors

Examples

- Corrupted response
- Unsupported encoding
- Invalid content length

The raw response SHOULD be preserved when feasible.

---

# Transport Errors

Transport errors originate within the adapter.

Examples

- Adapter initialization failure
- Unsupported feature
- Adapter crash

Transport-specific details SHALL be translated into canonical errors.

---

# Internal Errors

Unexpected failures within the HTTP Client.

Examples

- Serialization failure
- State corruption
- Unexpected exception

Internal implementation details SHALL NOT be exposed to callers.

---

# Error Severity

Suggested severity levels

| Severity | Meaning |
|----------|---------|
| Low | Minor issue, execution may continue |
| Medium | Partial execution impacted |
| High | Request failed |
| Critical | Execution aborted or unsafe state detected |

---

# Retry Guidance

The HTTP Client SHALL indicate whether an error is retryable.

Typical retryable errors include

- Temporary network failure
- Connect timeout
- Read timeout
- Transient DNS failure
- Temporary proxy failure

Typical non-retryable errors include

- Validation error
- Invalid configuration
- Unsupported method
- Certificate validation failure (unless policy permits)

Retry decisions SHALL be delegated to the shared Retry capability.

---

# Evidence Requirements

Errors SHOULD preserve

- Request metadata
- Configuration reference
- Response (if received)
- Transport metadata
- Timing information
- TLS metadata (where applicable)
- Redirect chain (if applicable)

Evidence SHALL conform to the canonical Evidence schema.

---

# Observability

The HTTP Client SHOULD emit events including

- RequestFailed
- RetryRequested
- RetrySucceeded
- RetryExhausted
- TransportFailure
- TimeoutOccurred
- TLSFailure

Events SHALL integrate with the platform Execution State.

---

# Logging

Logs SHOULD include

```yaml
request_id:

assessment_id:

task_id:

error_category:

error_code:

adapter:

duration:
```

Sensitive information SHALL be redacted.

---

# Recovery Expectations

Recovery MAY include

- Retry
- Alternate transport selection
- Session refresh
- Authentication renewal
- Graceful termination

Recovery SHALL follow platform policy.

---

# Validation Rules

A compliant HTTP Client error model SHALL

- Produce canonical errors
- Preserve evidence
- Support retry classification
- Emit observable events
- Avoid exposing implementation details

---

# Quality Requirements

The error model SHALL

✓ Normalize transport failures

✓ Support deterministic classification

✓ Preserve evidence

✓ Integrate with platform error handling

✓ Remain transport independent

✓ Support observability

✓ Protect sensitive information

---

# Future Extensions

Future versions MAY include

- Distributed tracing integration
- Multi-error aggregation
- Probabilistic retry hints
- Adapter health scoring
- Automated recovery recommendations

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant HTTP Client Error Model provides a consistent mechanism for representing HTTP execution failures across all transport implementations.

It enables reliable recovery, standardized reporting, and evidence preservation while maintaining interoperability with the platform-wide error handling framework.