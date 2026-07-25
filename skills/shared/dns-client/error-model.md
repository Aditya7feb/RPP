# DNS Client Error Model

**File:** `skills/shared/dns-client/error-model.md`

**Version:** 1.0.0

---

# Purpose

The DNS Client Error Model defines how DNS-related failures are detected, classified, normalized, reported, and recovered within the Robust PenTest Platform (RPP).

It extends the platform-wide error framework defined in

```
skills/core/error-handling.md
```

Resolver-specific errors, protocol-specific failures, and implementation-specific exceptions SHALL be normalized into canonical DNS Client Errors.

---

# Design Principles

DNS errors SHALL be

- Deterministic
- Structured
- Observable
- Recoverable where appropriate
- Secure
- Resolver Independent
- Protocol Independent

---

# Error Lifecycle

```
Failure Detected

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

DNS Client errors SHALL belong to one of the following categories.

| Category | Description |
|----------|-------------|
| Configuration | Invalid DNS configuration |
| Resolver | Resolver unavailable or invalid |
| Query | Invalid DNS query |
| Transport | UDP/TCP/DoH/DoT communication failure |
| Network | Network connectivity failure |
| DNSSEC | DNSSEC validation failure |
| Cache | Cache lookup or storage failure |
| Wildcard | Wildcard detection failure |
| Timeout | Operation exceeded configured timeout |
| Resource | Resource exhaustion |
| Policy | Platform policy violation |
| Internal | Unexpected runtime failure |

---

# Canonical Error Structure

Every DNS error SHALL expose

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

resolver:

query:

evidence:
```

---

# Configuration Errors

Examples

- Invalid resolver profile
- Unsupported transport
- Invalid timeout
- Invalid retry configuration

Execution SHALL terminate before query execution.

---

# Resolver Errors

Examples

- Resolver unavailable
- Resolver refused connection
- Resolver authentication failure
- Resolver health check failure

Resolver implementation details SHALL remain abstracted.

---

# Query Errors

Examples

- Invalid domain name
- Unsupported record type
- Invalid query class
- Malformed request

Query validation SHALL occur before execution.

---

# Transport Errors

Examples

- UDP communication failure
- TCP connection failure
- DoH request failure
- DoT handshake failure

Transport-specific failures SHALL be normalized.

---

# Network Errors

Examples

- DNS server unreachable
- Connection timeout
- Packet loss
- Network interruption

Network diagnostics MAY be preserved in evidence.

---

# DNSSEC Errors

Examples

- Signature validation failure
- Missing trust anchor
- Invalid trust chain
- Expired signature

Returned DNS records SHALL remain unchanged unless policy specifies otherwise.

---

# Cache Errors

Examples

- Cache lookup failure
- Cache write failure
- Cache corruption
- TTL validation failure

Cache failures SHOULD NOT prevent live resolution unless required by policy.

---

# Wildcard Detection Errors

Examples

- Insufficient samples
- Detection timeout
- Confidence calculation failure

Wildcard detection failures SHALL be isolated from normal DNS resolution.

---

# Timeout Errors

Examples

- Resolver timeout
- Query timeout
- Batch timeout
- Overall execution timeout

Timeout duration SHOULD be preserved in evidence.

---

# Resource Errors

Examples

- Maximum concurrent queries exceeded
- Memory exhausted
- Queue overflow
- Response size exceeded

Resource limits SHALL be configurable.

---

# Policy Errors

Examples

- Resolver not approved
- Secure transport required
- DNSSEC required
- External resolver prohibited

Policy violations SHALL identify the violated policy without exposing sensitive configuration.

---

# Internal Errors

Examples

- Adapter failure
- Serialization failure
- Response normalization failure
- Unexpected runtime exception

Internal implementation details SHALL NOT be exposed.

---

# Severity Levels

Suggested severities

| Severity | Meaning |
|----------|---------|
| Low | Minor DNS degradation |
| Medium | Current DNS operation failed |
| High | DNS functionality unavailable |
| Critical | Platform unable to perform DNS operations safely |

---

# Retry Guidance

Retryable examples

- Temporary resolver outage
- Transport interruption
- Timeout
- Network instability

Non-retryable examples

- Invalid domain
- Unsupported record type
- Invalid configuration
- Policy violation

Retry behavior SHALL follow platform retry policies.

---

# Evidence Requirements

DNS errors SHOULD preserve

- Query
- Record Type
- Resolver Profile
- Transport
- Response Time
- DNSSEC Status
- Retry Count

Evidence SHALL conform to the canonical Evidence schema.

---

# Observability

The DNS Client SHOULD publish

- ResolverUnavailable
- QueryFailed
- QueryTimedOut
- DNSSECValidationFailed
- CacheFailure
- WildcardDetectionFailed

Events SHALL integrate with the platform Execution State.

---

# Logging

Logs SHOULD include

```yaml
request_id:

assessment_id:

task_id:

resolver:

transport:

query:

record_type:

error_category:

error_code:

duration:
```

Sensitive information SHALL be redacted.

---

# Recovery Expectations

Recovery MAY include

- Resolver retry
- Resolver failover
- Transport fallback
- Cache bypass
- Graceful termination

Recovery SHALL respect platform execution policies.

---

# Validation Rules

A compliant DNS Client Error Model SHALL

- Produce canonical DNS errors
- Normalize resolver-specific failures
- Preserve evidence
- Support retry classification
- Publish observable events
- Protect sensitive information

---

# Quality Requirements

The DNS Client Error Model SHALL

✓ Normalize resolver failures

✓ Normalize transport failures

✓ Preserve resolver abstraction

✓ Support deterministic classification

✓ Capture evidence

✓ Integrate with platform error handling

✓ Remain implementation independent

---

# Future Extensions

Future versions MAY support

- Resolver reputation scoring
- Automatic resolver failover
- Adaptive retry strategies
- Distributed resolver diagnostics
- Resolver federation health monitoring

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant DNS Client Error Model provides a consistent, implementation-independent mechanism for representing DNS failures across all supported resolvers, transports, and execution environments.

It enables standardized reporting, reliable recovery, secure evidence preservation, and seamless integration with the Robust PenTest Platform's execution, observability, and error handling architecture.