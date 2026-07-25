# HTTP Client Configuration

**File:** `skills/shared/http-client/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the configuration parameters supported by the HTTP Client Shared Skill.

It extends the platform-wide configuration model defined in:

```
skills/core/configuration-model.md
```

Only HTTP-specific configuration is defined here.

---

# Relationship

```
Platform Configuration

↓

HTTP Client Configuration

↓

Execution Context

↓

Transport Adapter
```

---

# Design Principles

HTTP configuration SHALL be

- Explicit
- Predictable
- Immutable during execution
- Secure
- Transport Independent
- Validated

---

# Configuration Categories

The HTTP Client supports configuration in the following categories

```
Connection

↓

Timeouts

↓

Redirects

↓

TLS

↓

Authentication

↓

Proxy

↓

Request

↓

Response

↓

Performance

↓

Observability
```

---

# Connection

## keep_alive

Enable persistent HTTP connections.

Type

```
Boolean
```

Default

```
true
```

---

## max_connections

Maximum simultaneous outbound connections.

Type

```
Integer
```

Default

```
100
```

Minimum

```
1
```

---

## connection_pool_size

Maximum reusable connections.

Type

```
Integer
```

Default

```
25
```

---

# Timeouts

## connect_timeout

Maximum connection establishment time.

Type

```
Duration
```

Default

```
10s
```

---

## read_timeout

Maximum response read duration.

Type

```
Duration
```

Default

```
30s
```

---

## total_timeout

Maximum request lifetime.

Type

```
Duration
```

Default

```
60s
```

---

# Redirect Handling

## follow_redirects

Type

```
Boolean
```

Default

```
true
```

---

## max_redirects

Maximum redirect chain length.

Type

```
Integer
```

Default

```
10
```

---

## preserve_redirect_chain

Store complete redirect history.

Type

```
Boolean
```

Default

```
true
```

---

# TLS

## verify_tls

Validate server certificates.

Type

```
Boolean
```

Default

```
true
```

---

## minimum_tls_version

Supported values

```
TLS1.2

TLS1.3
```

---

## client_certificate

Reference to client certificate.

Type

```
Secret
```

---

## client_private_key

Reference to private key.

Type

```
Secret
```

---

## trusted_ca_bundle

Optional CA bundle.

Type

```
Secret
```

---

# Authentication

## authentication_profile

Reference to a shared authentication profile.

Type

```
Reference
```

---

## session_profile

Reference to an existing HTTP session.

Type

```
Reference
```

---

# Proxy

## proxy_enabled

Type

```
Boolean
```

---

## proxy_type

Supported values

```
HTTP

HTTPS

SOCKS4

SOCKS5
```

---

## proxy_address

Type

```
String
```

---

## proxy_credentials

Type

```
Secret
```

---

# Request Behaviour

## default_headers

Headers automatically included in every request.

Type

```
Object
```

---

## default_user_agent

Default User-Agent string.

Type

```
String
```

---

## default_accept

Default Accept header.

Type

```
String
```

---

## request_id_header

Optional correlation header.

Example

```
X-RPP-Request-ID
```

---

## custom_headers

Additional platform-defined headers.

Type

```
Map<String,String>
```

---

# Response Handling

## maximum_response_size

Maximum accepted response size.

Type

```
Size
```

Default

```
50 MB
```

---

## automatically_decompress

Automatically decompress responses.

Type

```
Boolean
```

Default

```
true
```

---

## preserve_raw_response

Store raw response as evidence.

Type

```
Boolean
```

---

# Retry

## retry_policy

Reference to shared retry policy.

Type

```
Reference
```

---

## retry_on_timeout

Type

```
Boolean
```

---

## retry_on_connection_failure

Type

```
Boolean
```

---

# Rate Limiting

## rate_limit_profile

Reference to shared rate limiter.

Type

```
Reference
```

---

## maximum_requests_per_second

Optional override.

Type

```
Integer
```

---

# Performance

## enable_connection_pooling

Type

```
Boolean
```

Default

```
true
```

---

## enable_http2

Type

```
Boolean
```

Default

```
true
```

---

## enable_http3

Type

```
Boolean
```

Default

```
false
```

---

# Observability

## capture_timings

Collect detailed timing metrics.

Type

```
Boolean
```

Default

```
true
```

---

## capture_request_headers

Record outbound headers.

Type

```
Boolean
```

---

## capture_response_headers

Record inbound headers.

Type

```
Boolean
```

---

## capture_tls_metadata

Store negotiated TLS metadata.

Type

```
Boolean
```

---

## capture_network_metrics

Collect transport statistics.

Type

```
Boolean
```

---

# Evidence

## preserve_requests

Store outbound requests.

Type

```
Boolean
```

---

## preserve_responses

Store inbound responses.

Type

```
Boolean
```

---

## preserve_redirects

Store redirect history.

Type

```
Boolean
```

---

## preserve_cookies

Store cookie activity.

Type

```
Boolean
```

---

# Security Constraints

Implementations SHALL

- Protect secrets
- Redact credentials
- Validate TLS by default
- Enforce scope restrictions
- Respect organizational policy

---

# Configuration Dependencies

The HTTP Client integrates with

```
Authentication

↓

Retry

↓

Rate Limiter

↓

Evidence

↓

Logging

↓

Transport
```

Configuration SHALL reference these shared skills rather than duplicating their configuration.

---

# Validation Rules

A compliant HTTP Client configuration SHALL

- Validate all parameter types
- Validate timeout values
- Validate proxy configuration
- Validate TLS configuration
- Validate referenced profiles
- Reject conflicting settings

---

# Quality Requirements

The configuration SHALL

✓ Be transport independent

✓ Support secure defaults

✓ Validate before execution

✓ Integrate with shared configuration

✓ Preserve backward compatibility

✓ Avoid duplicated configuration semantics

---

# Future Extensions

Future versions MAY include

- HTTP/3 tuning
- QUIC configuration
- Connection affinity
- Adaptive timeout policies
- Smart transport selection
- Dynamic protocol negotiation

---

# Success Criteria

A compliant HTTP Client Configuration provides a standardized mechanism for configuring HTTP communication while remaining consistent with the platform-wide configuration model.

It enables reusable, secure, and predictable HTTP behavior across all domain skills without exposing transport-specific implementation details.