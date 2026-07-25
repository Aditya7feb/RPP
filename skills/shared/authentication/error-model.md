# Authentication Error Model

**File:** `skills/shared/authentication/error-model.md`

**Version:** 1.0.0

---

# Purpose

The Authentication Error Model defines how authentication-related failures are detected, classified, normalized, reported, and recovered within the Robust PenTest Platform (RPP).

It extends the platform-wide error framework defined in:

```
skills/core/error-handling.md
```

The Authentication Shared Skill SHALL normalize provider-specific and mechanism-specific failures into canonical RPP authentication errors.

---

# Design Principles

Authentication errors SHALL be

- Deterministic
- Structured
- Recoverable where appropriate
- Observable
- Auditable
- Provider Independent
- Secure

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

Authentication errors SHALL belong to one of the following categories.

| Category | Description |
|----------|-------------|
| Validation | Invalid authentication request |
| Configuration | Invalid authentication configuration |
| Profile | Authentication profile resolution failure |
| Credential | Credential resolution or validation failure |
| Secret Provider | Secret backend unavailable or failed |
| Identity Provider | Authentication service failure |
| Authentication | Authentication unsuccessful |
| Authorization | Authenticated but access denied |
| Session | Session lifecycle failure |
| Token | Token issuance, validation, refresh, or revocation failure |
| Policy | Platform policy violation |
| Timeout | Authentication exceeded configured timeout |
| Network | Network communication failure |
| Internal | Unexpected Authentication Shared Skill failure |

---

# Canonical Error Structure

Every authentication error SHALL expose

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

profile:

provider:

evidence:
```

---

# Validation Errors

Examples

- Missing authentication profile
- Unsupported authentication operation
- Invalid request structure
- Missing required fields

Validation errors SHALL prevent execution.

---

# Configuration Errors

Examples

- Invalid provider reference
- Unsupported authentication type
- Invalid session policy
- Invalid refresh configuration

Execution SHALL NOT begin.

---

# Profile Errors

Examples

- Profile not found
- Profile disabled
- Profile violates policy
- Invalid profile schema

Profile resolution SHALL fail before credential resolution.

---

# Credential Errors

Examples

- Missing secret
- Expired credential
- Invalid certificate
- Invalid API key
- Unsupported credential format

Credential values SHALL NEVER appear in error messages.

---

# Secret Provider Errors

Examples

- Vault unavailable
- Secret lookup timeout
- Permission denied
- Provider authentication failure

Provider-specific exceptions SHALL be normalized.

---

# Identity Provider Errors

Examples

- OAuth server unavailable
- OIDC discovery failed
- LDAP unavailable
- SAML assertion failure
- Kerberos service unavailable

Provider implementation details SHOULD be abstracted.

---

# Authentication Errors

Examples

- Invalid username/password
- Invalid API key
- Invalid client certificate
- Invalid bearer token
- Login rejected

Authentication failures SHALL NOT expose sensitive validation details.

---

# Authorization Errors

Examples

- HTTP 401
- HTTP 403
- Missing required role
- Insufficient permissions

Authorization evidence SHOULD include the evaluated policy when available.

---

# Session Errors

Examples

- Session expired
- Session invalid
- Session not found
- Cookie store corrupted

Session identifiers SHOULD be redacted in logs and evidence.

---

# Token Errors

Examples

- Token expired
- Invalid signature
- Refresh failed
- Revoked token
- Invalid issuer
- Invalid audience

Raw token values SHALL NEVER appear in evidence or logs.

---

# Policy Errors

Examples

- Unsupported authentication mechanism
- Session reuse prohibited
- Authentication outside approved scope
- Credential usage prohibited

Policy violations SHALL identify the policy without exposing sensitive configuration.

---

# Timeout Errors

Examples

- Provider timeout
- Login timeout
- Token refresh timeout

Timeout duration SHOULD be preserved.

---

# Network Errors

Examples

- Connection refused
- DNS failure
- TLS negotiation failure
- Proxy failure

Transport-specific exceptions SHALL be normalized.

---

# Internal Errors

Examples

- Authentication context construction failure
- Serialization failure
- Unexpected runtime exception

Internal implementation details SHALL NOT be exposed.

---

# Severity Levels

Suggested severities

| Severity | Meaning |
|----------|---------|
| Low | Authentication partially degraded |
| Medium | Current operation failed |
| High | Authentication unavailable |
| Critical | Platform unable to authenticate safely |

---

# Retry Guidance

Retryable examples

- Temporary provider outage
- Secret backend timeout
- Network interruption
- Temporary identity provider failure

Non-retryable examples

- Invalid credentials
- Disabled profile
- Policy violation
- Unsupported authentication type

Retry decisions SHALL be delegated to the platform retry capability.

---

# Evidence Requirements

Authentication errors SHOULD preserve

- Authentication profile
- Provider identifier
- Authentication mechanism
- Session metadata (redacted)
- Token metadata (non-sensitive)
- Policy evaluation
- Timing information

Evidence SHALL conform to the canonical Evidence schema.

---

# Observability

The Authentication Shared Skill SHOULD publish

- AuthenticationFailed
- AuthenticationSucceeded
- AuthenticationRetried
- SessionExpired
- SessionRefreshFailed
- TokenRefreshFailed
- ProviderUnavailable

Events SHALL integrate with the platform Execution State.

---

# Logging

Logs SHOULD include

```yaml
request_id:

assessment_id:

task_id:

profile:

authentication_type:

provider:

error_category:

error_code:

duration:
```

Sensitive values SHALL be redacted.

---

# Recovery Expectations

Recovery MAY include

- Retry
- Session refresh
- Token refresh
- Provider failover
- Profile fallback (if permitted)
- Graceful termination

Recovery SHALL respect platform policy.

---

# Validation Rules

A compliant Authentication Error Model SHALL

- Produce canonical errors
- Normalize provider-specific failures
- Preserve evidence
- Support retry classification
- Emit observable events
- Protect sensitive information

---

# Quality Requirements

The error model SHALL

✓ Normalize provider failures

✓ Support deterministic classification

✓ Preserve evidence

✓ Protect credentials

✓ Integrate with platform error handling

✓ Support observability

✓ Remain provider independent

---

# Future Extensions

Future versions MAY include

- Identity provider health scoring
- Automated provider failover
- Risk-based recovery strategies
- Distributed authentication tracing
- Multi-provider error aggregation

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Authentication Error Model provides a consistent mechanism for representing authentication failures across all supported authentication mechanisms and identity providers.

It enables reliable recovery, standardized reporting, secure evidence preservation, and seamless interoperability with the platform-wide error handling framework.