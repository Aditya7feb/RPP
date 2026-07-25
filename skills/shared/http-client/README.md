# HTTP Client Shared Skill

**File:** `skills/shared/http-client/README.md`

**Version:** 1.0.0

---

# Purpose

The HTTP Client Shared Skill provides the canonical mechanism for performing HTTP communication within the Robust PenTest Platform (RPP).

Rather than allowing individual skills to implement their own HTTP logic, this shared skill centralizes request execution, response handling, authentication, session management, retry behavior, rate limiting, evidence collection, and observability.

All HTTP-based skills SHOULD consume this shared capability.

---

# Design Principles

The HTTP Client SHALL be

- Protocol compliant
- Stateless where practical
- Reusable
- Observable
- Extensible
- Secure by default
- Implementation independent

---

# Responsibilities

The HTTP Client is responsible for

- Constructing HTTP requests
- Sending requests
- Receiving responses
- Following redirects
- Managing sessions
- Managing cookies
- Handling compression
- Applying authentication
- Recording evidence
- Collecting timing information
- Producing structured responses

The HTTP Client SHALL NOT determine security findings.

---

# Architecture

```
Master Agent

↓

Domain Skill

↓

HTTP Client

↓

HTTP Transport

↓

Target
```

---

# Provided Capabilities

The HTTP Client SHOULD expose

```
network.http.send

network.http.follow_redirects

network.http.upload

network.http.download

network.http.parse_headers

network.http.parse_cookies

network.http.parse_body
```

Additional capabilities MAY be introduced.

---

# Typical Consumers

The following domain skills commonly depend on the HTTP Client

- Recon
- GraphQL
- JWT
- CORS
- CSP
- SQL Injection
- XSS
- SSRF
- SSTI
- File Upload
- IDOR
- CMS Detection
- Technology Fingerprinting

---

# Supported HTTP Methods

Supported methods include

```
GET

POST

PUT

PATCH

DELETE

HEAD

OPTIONS

TRACE
```

Additional methods MAY be supported.

---

# Request Construction

The HTTP Client SHALL support

- URL construction
- Query parameters
- Headers
- Cookies
- Request body
- Multipart forms
- JSON payloads
- XML payloads
- Binary payloads

---

# Authentication

Supported authentication mechanisms MAY include

- Basic Authentication
- Bearer Tokens
- API Keys
- OAuth
- Cookie-based Sessions
- Client Certificates
- Custom Headers

Authentication SHALL integrate with the shared Authentication skill.

---

# Session Management

The HTTP Client SHOULD support

- Cookie persistence
- Session reuse
- Session isolation
- Session expiration
- Session reset

Sessions SHALL remain scoped to the current assessment unless explicitly configured otherwise.

---

# Redirect Handling

Redirect behavior SHALL be configurable.

Supported modes

```
Disabled

↓

Limited

↓

Unlimited
```

Redirect chains SHOULD be preserved as evidence.

---

# Compression

Supported encodings MAY include

- gzip
- deflate
- br
- identity

Compression SHALL be handled transparently where possible.

---

# TLS Support

The HTTP Client SHALL support

- TLS negotiation
- Certificate inspection
- Client certificates
- Certificate validation
- Configurable verification

TLS inspection SHALL integrate with the shared TLS capabilities.

---

# Proxy Support

Supported proxy types MAY include

- HTTP
- HTTPS
- SOCKS4
- SOCKS5

Proxy configuration SHALL be externalized.

---

# Retry Behavior

Retry behavior SHALL integrate with

```
skills/shared/retry/
```

The HTTP Client SHALL NOT implement retry policies independently.

---

# Rate Limiting

Rate limiting SHALL integrate with

```
skills/shared/rate-limiter/
```

---

# Evidence Collection

Every request SHOULD generate evidence.

Examples

- Request
- Response
- Headers
- Timing
- Redirect Chain
- TLS Information

Evidence SHALL conform to the canonical Evidence schema.

---

# Observability

The HTTP Client SHOULD emit events including

- Request Started
- Request Completed
- Redirect Followed
- Retry Performed
- Timeout
- Failure

These events SHOULD update the Execution State.

---

# Error Handling

Errors SHALL conform to

```
skills/core/error-handling.md
```

Common error categories include

- Network
- Timeout
- TLS
- Authentication
- Proxy
- Configuration

---

# Configuration

Configurable parameters MAY include

```yaml
timeout:

verify_tls:

follow_redirects:

proxy:

user_agent:

max_response_size:

retry_policy:

rate_limit:

compression:
```

---

# Outputs

The HTTP Client SHOULD produce

```yaml
status_code:

headers:

cookies:

body:

timings:

tls:

redirect_chain:

evidence:
```

Outputs SHALL conform to the standard interface specification.

---

# Security Considerations

The HTTP Client SHALL

- Respect Rules of Engagement
- Preserve authentication boundaries
- Protect secrets
- Avoid credential leakage
- Record audit information
- Enforce scope restrictions

---

# Dependencies

The HTTP Client MAY depend on

- Authentication
- Retry
- Rate Limiter
- Evidence
- Logging
- TLS Client

The HTTP Client SHALL NOT depend on domain skills.

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

Implementations SHOULD

- Produce deterministic responses
- Preserve evidence
- Support structured errors
- Separate transport from business logic
- Avoid hidden retries
- Remain protocol compliant

---

# Anti-Patterns

Implementations SHOULD NOT

- Detect vulnerabilities
- Generate findings
- Hardcode authentication
- Modify assessment scope
- Perform planning decisions
- Embed tool-specific assumptions

---

# Future Extensions

Future versions MAY include

- HTTP/2 support
- HTTP/3 support
- Connection pooling
- Request replay
- Traffic recording
- Distributed transports
- Adaptive throttling

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant HTTP Client Shared Skill provides a standardized, reusable, and observable mechanism for HTTP communication across the Robust PenTest Platform.

It enables domain skills to focus on security analysis while delegating transport concerns to a common, implementation-independent capability.