# HTTP Client Capabilities

**File:** `skills/shared/http-client/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document defines the canonical capabilities provided by the HTTP Client Shared Skill.

These capabilities represent reusable HTTP behaviors that may be consumed by any domain skill within the Robust PenTest Platform (RPP).

Capabilities describe *what* the HTTP Client can do—not *how* it is implemented.

---

# Relationship

```
Master Agent

↓

Domain Skill

↓

Capability

↓

HTTP Client

↓

Transport
```

Domain skills SHALL depend on capabilities rather than transport implementations.

---

# Design Principles

Capabilities SHALL be

- Canonical
- Composable
- Independent
- Reusable
- Observable
- Versioned
- Implementation Independent

---

# Capability Categories

The HTTP Client provides capabilities in the following categories

```
Request Execution

↓

Response Processing

↓

Authentication

↓

Session Management

↓

Transport

↓

TLS

↓

Evidence

↓

Observability
```

---

# Request Execution

## network.http.send

### Purpose

Execute an HTTP request.

### Inputs

- URL
- Method
- Headers
- Body
- Query Parameters

### Outputs

- Response
- Timing
- Evidence

---

## network.http.upload

### Purpose

Upload multipart or binary content.

Supported payloads MAY include

- Multipart Forms
- Binary Files
- Streams

---

## network.http.download

### Purpose

Download remote resources.

Outputs SHALL include

- Response
- Content Metadata
- Download Metrics

---

# Response Processing

## network.http.parse_headers

Purpose

Parse response headers.

Outputs

- Header Collection
- Normalized Header Names

---

## network.http.parse_cookies

Purpose

Extract cookies from responses.

Outputs

- Cookie Collection
- Cookie Attributes

---

## network.http.parse_body

Purpose

Extract response body.

Supported formats MAY include

- HTML
- JSON
- XML
- Text
- Binary

---

## network.http.follow_redirects

Purpose

Handle HTTP redirect chains.

Outputs

- Redirect Chain
- Final Response

---

# Authentication

## network.http.authenticate

Purpose

Apply authentication to outgoing requests.

Supported mechanisms MAY include

- Basic
- Bearer
- OAuth
- API Keys
- Cookies
- Client Certificates

---

# Session Management

## network.http.session.create

Purpose

Create a new HTTP session.

---

## network.http.session.reuse

Purpose

Reuse an existing session.

---

## network.http.session.reset

Purpose

Destroy session state.

---

# Transport

## network.http.proxy

Purpose

Route requests through configured proxies.

Supported proxy types

- HTTP
- HTTPS
- SOCKS4
- SOCKS5

---

## network.http.timeout

Purpose

Apply timeout policies.

Supported timeout types

- Connection
- Read
- Total

---

## network.http.compression

Purpose

Handle compressed content.

Supported encodings MAY include

- gzip
- br
- deflate

---

# TLS

## network.http.tls.inspect

Purpose

Expose negotiated TLS information.

Outputs MAY include

- Protocol
- Cipher Suite
- Certificate
- Certificate Chain

---

## network.http.tls.verify

Purpose

Validate server certificates.

Outputs

- Validation Status
- Validation Errors

---

# Evidence

## network.http.evidence.capture

Purpose

Capture execution evidence.

Evidence MAY include

- Request
- Response
- Headers
- Cookies
- Redirects
- Timing
- TLS Information

---

# Observability

## network.http.metrics.collect

Purpose

Collect execution metrics.

Metrics MAY include

- Duration
- Response Size
- Request Size
- Retry Count
- Redirect Count

---

## network.http.events.publish

Purpose

Publish runtime events.

Events MAY include

- Request Started
- Response Received
- Retry
- Redirect
- Timeout
- Completed

---

# Capability Dependencies

Some capabilities depend on other shared skills.

| Capability | Dependency |
|------------|------------|
| network.http.authenticate | Authentication Shared Skill |
| network.http.tls.inspect | TLS Client |
| network.http.evidence.capture | Evidence Shared Skill |
| network.http.metrics.collect | Logging / Metrics |
| network.http.timeout | Retry |
| network.http.proxy | Transport |

The HTTP Client SHALL expose these capabilities regardless of implementation.

---

# Capability Composition

Capabilities MAY be composed.

Example

```
network.http.send

↓

network.http.follow_redirects

↓

network.http.parse_headers

↓

network.http.parse_body

↓

network.http.evidence.capture

↓

Agent Response
```

---

# Capability Constraints

Capabilities SHALL

- Respect assessment scope
- Preserve execution context
- Produce structured outputs
- Record evidence
- Generate structured errors

Capabilities SHALL NOT

- Detect vulnerabilities
- Produce findings
- Modify assessment scope
- Make planning decisions

---

# Versioning

Capabilities SHALL use semantic versioning.

Breaking semantic changes SHALL require a new capability version.

Capability identifiers SHOULD remain stable.

---

# Validation Rules

A compliant capability SHALL

- Have a unique identifier
- Define inputs
- Define outputs
- Specify dependencies
- Produce structured responses
- Support observability

---

# Quality Requirements

HTTP Client capabilities SHALL

✓ Be reusable

✓ Be deterministic

✓ Be implementation independent

✓ Support composition

✓ Integrate with canonical schemas

✓ Preserve evidence

✓ Support structured errors

✓ Remain transport agnostic

---

# Future Extensions

Future versions MAY include

- HTTP/2 capabilities
- HTTP/3 capabilities
- WebSocket support
- Server-Sent Events
- Streaming uploads
- Streaming downloads
- Adaptive transport selection

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant HTTP Client exposes a standardized set of reusable capabilities that provide HTTP communication services to domain skills without exposing transport-specific implementation details.

These capabilities form the foundation for web-based reconnaissance, validation, fingerprinting, and exploitation workflows throughout the Robust PenTest Platform.