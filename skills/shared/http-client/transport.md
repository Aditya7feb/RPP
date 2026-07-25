# HTTP Transport Architecture

**File:** `skills/shared/http-client/transport.md`

**Version:** 1.0.0

---

# Purpose

The HTTP Transport Architecture defines how the HTTP Client Shared Skill communicates with remote targets.

The transport layer separates HTTP capabilities from transport implementations, enabling the Robust PenTest Platform (RPP) to support multiple HTTP engines without changing domain skills.

Transport implementations SHALL remain interchangeable.

---

# Design Principles

The transport layer SHALL be

- Implementation Independent
- Replaceable
- Observable
- Testable
- Stateless where practical
- Capability Driven

Domain skills SHALL never directly invoke transport implementations.

---

# Architecture

```
Master Agent

↓

Domain Skill

↓

HTTP Client

↓

Transport Interface

↓

Transport Adapter

↓

Target
```

Only the Transport Interface SHALL be visible to the HTTP Client.

---

# Responsibilities

The Transport Interface is responsible for

- Sending requests
- Receiving responses
- Managing connections
- Applying transport configuration
- Returning normalized responses

Transport implementations SHALL NOT

- Detect vulnerabilities
- Produce findings
- Interpret security results
- Modify assessment scope

---

# Transport Interface

Every transport SHALL support

- Request execution
- Response retrieval
- Redirect handling
- Cookie management
- Header processing
- Timeout enforcement
- TLS negotiation
- Proxy support

Additional capabilities MAY be implemented.

---

# Transport Adapters

Supported transport implementations MAY include

```
httpx

Playwright

curl

requests

.NET HttpClient

Go net/http
```

Organizations MAY implement custom adapters.

---

# Adapter Responsibilities

Every adapter SHALL

- Translate requests into native API calls
- Normalize responses
- Convert transport-specific errors
- Preserve execution metadata
- Preserve evidence

Adapters SHALL hide implementation details.

---

# Transport Selection

Transport selection MAY depend on

- Capability requirements
- Execution environment
- Protocol support
- Browser requirements
- Authentication requirements
- Organizational policy

Selection SHOULD be transparent to domain skills.

---

# Capability Mapping

| Capability | Typical Adapter |
|------------|-----------------|
| Simple HTTP Request | httpx |
| Browser Rendering | Playwright |
| HTTP/3 | Future Adapter |
| Headless Automation | Playwright |
| Lightweight API Calls | requests |
| Enterprise .NET Runtime | HttpClient |

Capabilities SHALL remain identical regardless of adapter.

---

# Normalized Request

Every adapter SHALL consume a normalized request model.

Example

```yaml
method:

url:

headers:

cookies:

query:

body:

timeout:

proxy:

verify_tls:
```

Transport-specific request objects SHALL NOT be exposed outside the adapter.

---

# Normalized Response

Every adapter SHALL return a normalized response model.

```yaml
status_code:

headers:

cookies:

body:

timings:

redirects:

tls:

raw_metadata:
```

Responses SHALL remain independent of the underlying HTTP library.

---

# Connection Management

Adapters MAY implement

- Connection pooling
- Persistent connections
- HTTP Keep-Alive
- Connection reuse

These optimizations SHALL remain transparent.

---

# TLS Handling

TLS responsibilities include

- Negotiation
- Certificate validation
- Cipher collection
- Protocol detection
- Client certificates

TLS metadata SHALL be exposed in a normalized form.

---

# Redirect Handling

Adapters SHALL support

- Disabled redirects
- Limited redirects
- Automatic redirects
- Redirect history

Redirect behavior SHALL be configurable.

---

# Streaming Support

Adapters MAY support

- Streaming uploads
- Streaming downloads
- Incremental response reading

Streaming SHALL integrate with the execution model.

---

# Browser-Based Transports

Browser transports MAY expose additional metadata

Examples

- DOM
- Rendered HTML
- JavaScript Console
- Screenshots
- Storage
- Service Workers

These capabilities SHALL remain optional.

---

# Error Translation

Transport-specific errors SHALL be translated into canonical RPP error categories.

Examples

| Adapter Error | Canonical Category |
|--------------|--------------------|
| Connection Refused | Network |
| TLS Failure | TLS |
| Timeout | Timeout |
| Proxy Failure | Network |
| Certificate Error | TLS |

Transport exceptions SHALL NOT propagate directly.

---

# Evidence Collection

Every adapter SHOULD provide

- Raw Request
- Raw Response
- Timing
- Redirect Chain
- TLS Metadata

Evidence SHALL conform to the canonical Evidence schema.

---

# Observability

Adapters SHOULD emit events including

- Connection Opened
- Request Sent
- Response Received
- Redirect Followed
- Timeout
- Retry
- Connection Closed

Events SHOULD integrate with the Execution State.

---

# Version Compatibility

Adapters SHOULD declare

```yaml
adapter_name:

adapter_version:

supported_protocols:

supported_capabilities:
```

---

# Adapter Registration

Each adapter SHOULD register

```yaml
id:

name:

version:

priority:

supported_capabilities:

supported_protocols:
```

The HTTP Client MAY use this metadata when selecting an adapter.

---

# Quality Requirements

The transport architecture SHALL

✓ Hide implementation details

✓ Normalize requests

✓ Normalize responses

✓ Support multiple adapters

✓ Preserve evidence

✓ Produce structured errors

✓ Support observability

✓ Remain implementation independent

---

# Validation Rules

A compliant transport adapter SHALL

- Implement the Transport Interface
- Produce normalized responses
- Translate errors
- Preserve execution metadata
- Preserve evidence

---

# Future Extensions

Future versions MAY include

- HTTP/3
- QUIC
- WebSockets
- gRPC transports
- Remote transport workers
- Distributed transport pools
- Adaptive transport selection

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant HTTP Transport Architecture provides a stable abstraction between HTTP capabilities and transport implementations.

It enables the Robust PenTest Platform to adopt new HTTP technologies and execution environments without affecting domain skills, shared capabilities, or orchestration logic.