# HTTP Client Execution Model

**File:** `skills/shared/http-client/execution.md`

**Version:** 1.0.0

---

# Purpose

The HTTP Client Execution Model defines how HTTP requests are processed from invocation through completion within the Robust PenTest Platform (RPP).

It specifies the runtime behavior of the HTTP Client Shared Skill while remaining independent of any transport implementation.

Execution SHALL follow the platform-wide execution model defined in:

```
skills/core/execution-model.md
```

---

# Design Principles

HTTP execution SHALL be

- Deterministic
- Observable
- Recoverable
- Stateless where practical
- Policy Aware
- Transport Independent
- Evidence Driven

---

# Relationship

```
Caller

↓

HTTP Interface

↓

Execution Engine

↓

HTTP Client

↓

Transport Interface

↓

Transport Adapter

↓

Target
```

---

# Execution Overview

Each HTTP request progresses through the following stages.

```
Receive Request

↓

Resolve Configuration

↓

Validate Request

↓

Resolve Authentication

↓

Resolve Transport

↓

Execute Request

↓

Receive Response

↓

Normalize Response

↓

Collect Evidence

↓

Publish Events

↓

Return Response
```

---

# Stage 1 — Receive Request

The HTTP Client SHALL receive

- Request metadata
- HTTP request
- Execution options
- Execution context

The request SHALL conform to the HTTP Client Interface.

---

# Stage 2 — Resolve Configuration

Configuration SHALL be resolved according to

```
skills/core/configuration-model.md
```

Resolved configuration SHALL remain immutable.

Configuration MAY include

- Timeout
- Proxy
- TLS
- Retry Policy
- Rate Limits
- User-Agent

---

# Stage 3 — Validate Request

The client SHALL validate

- HTTP Method
- URL
- Required Headers
- Payload Format
- Authentication References
- Configuration References

Invalid requests SHALL fail before transport selection.

---

# Stage 4 — Resolve Authentication

Authentication SHALL be obtained from

- Authentication Profile
- Session
- Credential Store

The HTTP Client SHALL never construct credentials itself.

---

# Stage 5 — Resolve Transport

A transport adapter SHALL be selected.

Selection MAY consider

- HTTP Version
- Browser Requirement
- Streaming
- Authentication
- Policy
- Protocol Support

The selection SHALL be transparent to callers.

---

# Stage 6 — Execute Request

The selected adapter SHALL

- Construct the native request
- Establish a connection
- Send the request
- Receive the response

Transport-specific behavior SHALL remain hidden.

---

# Stage 7 — Handle Redirects

Redirect processing SHALL follow configuration.

Supported modes

```
Disabled

↓

Limited

↓

Automatic
```

The complete redirect chain SHOULD be recorded.

---

# Stage 8 — Handle Retries

Retry decisions SHALL be delegated to the shared Retry Skill.

The HTTP Client SHALL

- Report failures
- Request retry evaluation
- Resume execution if approved

Retry policies SHALL remain external.

---

# Stage 9 — Receive Response

The transport SHALL return

- Status Code
- Headers
- Cookies
- Body
- Timing
- TLS Metadata

Transport-specific objects SHALL be normalized.

---

# Stage 10 — Normalize Response

The HTTP Client SHALL produce a canonical response.

Normalized fields include

```yaml
status_code:

headers:

cookies:

body:

timings:

redirect_chain:

tls:
```

---

# Stage 11 — Capture Evidence

Evidence SHOULD include

- Request
- Response
- Headers
- Cookies
- Redirect Chain
- Timing
- TLS Information

Evidence SHALL conform to the canonical Evidence schema.

---

# Stage 12 — Publish Events

The HTTP Client SHOULD publish

- Request Started
- Request Sent
- Redirect Followed
- Response Received
- Retry Requested
- Request Completed
- Request Failed

Events SHALL update the Execution State.

---

# Parallel Execution

The HTTP Client MAY execute multiple requests concurrently.

Concurrency SHALL respect

- Rate Limits
- Policy
- Resource Constraints
- Transport Limits

Parallel execution SHALL preserve request isolation.

---

# Streaming Execution

Streaming MAY be supported for

- Large Downloads
- Incremental Responses
- Event Streams

Streaming SHALL preserve

- Context
- Ordering
- Evidence
- Metrics

---

# Session Management

Execution MAY reuse existing sessions.

Session state MAY include

- Cookies
- CSRF Tokens
- Authentication
- Connection Reuse

Session boundaries SHALL remain isolated.

---

# Cancellation

Execution MAY be cancelled by

- Master Agent
- Workflow
- Policy Engine
- Operator

Cancellation SHALL

- Stop transport activity
- Preserve collected evidence
- Release resources
- Return structured status

---

# Timeout Handling

Timeout evaluation SHALL include

- Connection Timeout
- Read Timeout
- Total Timeout

Timeout behavior SHALL follow platform retry policy.

---

# Error Handling

Errors SHALL conform to

```
skills/core/error-handling.md
```

Examples

- Connection Failure
- TLS Failure
- Timeout
- Proxy Failure
- Authentication Failure

---

# Metrics

The HTTP Client SHOULD record

```yaml
duration:

request_size:

response_size:

dns_time:

connect_time:

tls_time:

retry_count:

redirect_count:
```

Metrics SHOULD support observability.

---

# Resource Cleanup

Execution SHALL release

- Connections
- Temporary Buffers
- Sessions (if configured)
- Streams

Cleanup SHALL occur even after failures.

---

# Audit Requirements

Execution SHOULD record

- Request Identifier
- Adapter Used
- Configuration Version
- Execution Duration
- Policy Decisions

Sensitive values SHALL be redacted.

---

# Validation Rules

A compliant execution SHALL

- Validate requests
- Resolve configuration
- Resolve authentication
- Select transport
- Normalize responses
- Preserve evidence
- Produce structured errors

---

# Quality Requirements

The execution model SHALL

✓ Remain transport independent

✓ Preserve execution context

✓ Support retries

✓ Support cancellation

✓ Support observability

✓ Produce normalized responses

✓ Preserve evidence

✓ Support concurrent execution

---

# Future Extensions

Future versions MAY include

- Adaptive transport selection
- HTTP/3 execution optimization
- Distributed execution
- Connection affinity
- Request batching
- Predictive retry strategies

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant HTTP Client Execution Model provides a consistent, observable, and implementation-independent mechanism for executing HTTP requests.

It enables all domain skills within the Robust PenTest Platform to perform reliable HTTP communication while abstracting transport complexity, preserving evidence, and integrating seamlessly with the platform's execution lifecycle.