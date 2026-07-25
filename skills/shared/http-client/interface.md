# HTTP Client Interface

**File:** `skills/shared/http-client/interface.md`

**Version:** 1.0.0

---

# Purpose

The HTTP Client Interface defines the canonical contract through which skills interact with the HTTP Client Shared Skill.

The interface standardizes request construction, response handling, execution behavior, and error propagation while remaining independent of any transport implementation.

All consumers SHALL communicate exclusively through this interface.

---

# Design Principles

The interface SHALL be

- Stable
- Strongly Defined
- Transport Independent
- Versioned
- Observable
- Backward Compatible
- Capability Driven

---

# Relationship

```
Master Agent

↓

Workflow

↓

Domain Skill

↓

HTTP Client Interface

↓

HTTP Client

↓

Transport Interface

↓

Transport Adapter
```

Consumers SHALL NOT communicate directly with transport adapters.

---

# Interface Overview

The interface consists of

```
Metadata

↓

Request

↓

Execution Options

↓

Execution Context

↓

Response

↓

Errors

↓

Evidence

↓

Metrics
```

---

# Metadata

Every invocation SHALL include metadata.

```yaml
request_id:

assessment_id:

task_id:

skill_id:

timestamp:
```

Metadata enables tracing and auditing.

---

# Request

Every request SHALL define

```yaml
method:

url:

headers:

query:

cookies:

body:
```

---

## Method

Supported methods

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

---

## URL

The request SHALL specify an absolute URL.

Relative URLs MAY be resolved by higher-level skills before invocation.

---

## Headers

Headers SHALL be represented as key-value pairs.

Examples

```yaml
Accept:

Content-Type:

Authorization:

User-Agent:
```

---

## Query Parameters

Query parameters SHALL be represented independently from the URL.

Example

```yaml
page: 1

limit: 25
```

---

## Cookies

Cookies SHALL be represented separately from headers.

Cookie management SHALL remain the responsibility of the HTTP Client.

---

## Body

Supported payloads MAY include

- JSON
- XML
- Form Data
- Multipart
- Binary
- Plain Text

---

# Execution Options

The caller MAY specify execution behavior.

```yaml
follow_redirects:

verify_tls:

timeout:

proxy:

compression:

stream:

retry_policy:
```

These options influence execution without changing the interface.

---

# Execution Context

The HTTP Client SHALL receive context from the Execution Engine.

Example

```yaml
authentication:

session:

variables:

technology_inventory:

assessment:
```

The interface SHALL treat context as read-only.

---

# Authentication

Authentication SHALL reference shared authentication state.

Supported mechanisms MAY include

- Basic
- Bearer
- OAuth
- API Keys
- Client Certificates
- Session Cookies

Credentials SHALL NOT be embedded directly into interface definitions.

---

# Session

Session state MAY include

```yaml
session_id:

cookie_store:

csrf_tokens:
```

The HTTP Client SHALL maintain session consistency.

---

# Response

Every execution SHALL return a normalized response.

```yaml
status_code:

headers:

cookies:

body:

timings:

redirect_chain:

tls:

evidence:
```

Transport-specific response objects SHALL NOT be exposed.

---

## Timing

Timing metadata MAY include

```yaml
dns:

connect:

tls:

request:

response:

total:
```

---

## Redirect Chain

Redirect history SHALL include

- Source
- Destination
- Status Code

The complete chain SHOULD be preserved.

---

## TLS Metadata

TLS information MAY include

```yaml
protocol:

cipher_suite:

certificate:

certificate_chain:
```

---

# Evidence

The interface SHALL expose structured evidence.

Evidence MAY include

- Request
- Response
- Headers
- Cookies
- Redirects
- TLS Metadata
- Timing Information

Evidence SHALL conform to the canonical Evidence schema.

---

# Metrics

Execution metrics MAY include

```yaml
duration:

request_size:

response_size:

retry_count:

redirect_count:
```

Metrics SHOULD support observability.

---

# Error Contract

Errors SHALL conform to

```
skills/core/error-handling.md
```

Typical categories include

- Validation
- Network
- TLS
- Authentication
- Timeout
- Configuration

Errors SHALL remain implementation independent.

---

# Streaming Responses

The interface MAY support streaming.

Streaming responses SHALL preserve

- Ordering
- Context
- Evidence
- Metrics

Streaming SHALL integrate with the execution model.

---

# Compatibility

The interface SHALL remain stable across transport implementations.

Example

```
httpx

↓

Same Interface

↓

Playwright

↓

Same Interface

↓

curl

↓

Same Interface
```

Consumers SHALL require no modification when transport adapters change.

---

# Versioning

The interface SHALL follow semantic versioning.

Minor versions MAY introduce optional fields.

Major versions SHALL indicate breaking changes.

---

# Validation Rules

A compliant invocation SHALL define

- Metadata
- Request
- Execution Options
- Context
- Response
- Error Handling
- Evidence

---

# Quality Requirements

The HTTP Client Interface SHALL

✓ Remain transport independent

✓ Produce normalized responses

✓ Support structured errors

✓ Preserve execution context

✓ Preserve evidence

✓ Support observability

✓ Remain backward compatible

---

# Future Extensions

Future versions MAY include

- HTTP/2 Features
- HTTP/3 Features
- WebSocket Sessions
- Server-Sent Events
- Streaming Uploads
- Incremental Responses

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant HTTP Client Interface provides a stable, implementation-independent contract through which all platform components perform HTTP communication.

It enables interchangeable transport implementations while preserving consistency, interoperability, observability, and maintainability across the Robust PenTest Platform.