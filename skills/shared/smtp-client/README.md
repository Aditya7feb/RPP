# SMTP Client Shared Skill

**File:** `skills/shared/smtp-client/README.md`

**Version:** 1.0.0

---

# Purpose

The SMTP Client Shared Skill provides the canonical, implementation-independent
mechanism for conducting Simple Mail Transfer Protocol (SMTP) conversations
within the Robust PenTest Platform (RPP).

Rather than allowing individual skills to speak SMTP directly over raw sockets,
this shared skill centralizes session establishment, capability negotiation,
opportunistic TLS, authentication, command exchange, reply-code mapping, and
observability.

All packages that require SMTP transport SHALL delegate to this shared skill.

---

# Goals

The SMTP Client Shared Skill SHALL

- Abstract SMTP transport behind a stable interface
- Establish sessions through the [TCP Client](../tcp-client/README.md)
- Negotiate capabilities through `EHLO`
- Upgrade to TLS through `STARTTLS` via the [TLS Client](../tls-client/README.md)
- Authenticate through the [Authentication](../authentication/README.md) package
- Exchange commands and map reply codes to canonical outcomes
- Produce SMTP evidence
- Integrate with platform observability

---

# Non-Goals

The SMTP Client Shared Skill SHALL NOT

- Detect vulnerabilities such as open relays
- Produce security findings
- Send unsolicited mail
- Interpret reply codes as security weaknesses
- Parse message bodies as findings

The SMTP Client conducts protocol conversations and reports outcomes as data.
Interpretation, including open-relay assessment, belongs to domain skills.

---

# Design Principles

The SMTP Client Shared Skill SHALL be

- Deterministic in bounds given the same configuration and inputs
- Layered atop the TCP and TLS shared skills
- Bounded in message size and session duration
- Governed
- Observable
- Secure by default

---

# Architecture

```
Master Agent

↓

Domain Skill

↓

SMTP Client Shared Skill

├── Session Establisher     → TCP Client
├── Capability Negotiator
├── STARTTLS Upgrader       → TLS Client
├── Authenticator           → Authentication
├── Command Exchanger
├── Reply Mapper
├── Evidence Manager
├── Event Manager

↓

Transport Adapter
```

The SMTP Client conducts the conversation but SHALL remain unaware of the
transport adapter implementation.

---

# Responsibilities

The SMTP Client Shared Skill is responsible for

- Establishing a session via the [TCP Client](../tcp-client/README.md)
- Reading the server greeting and negotiating capabilities via `EHLO`
- Upgrading to TLS via `STARTTLS` through the
  [TLS Client](../tls-client/README.md)
- Authenticating via the [Authentication](../authentication/README.md) package
- Exchanging commands such as `MAIL FROM`, `RCPT TO`, and `DATA`
- Mapping SMTP reply codes to canonical outcomes
- Applying rate, retry, and proxy governance
- Emitting SMTP lifecycle events and capturing evidence

---

# Session Lifecycle

```
Receive Session Request

↓

Acquire Rate Permit

↓

Establish Session (TCP Client)

↓

Read Greeting

↓

EHLO → Negotiate Capabilities

↓

STARTTLS (if available/required) → TLS Client

↓

Authenticate (if configured)

↓

Exchange Commands

↓

QUIT / Close

↓

Emit Evidence and Events
```

The session outcome SHOULD be preserved as evidence.

---

# Capability Negotiation

The SMTP Client SHALL issue `EHLO` and record advertised capabilities such as
`STARTTLS`, `AUTH`, `SIZE`, and `PIPELINING`.

Advertised capabilities SHALL be reported as data. Their security significance
SHALL be interpreted by domain skills.

---

# Opportunistic And Required TLS

The SMTP Client SHALL support `STARTTLS` upgrade through the
[TLS Client](../tls-client/README.md).

Where a session requires TLS and `STARTTLS` is unavailable, the session SHALL be
terminated with a canonical error rather than continuing in cleartext.

Certificate validation outcomes SHALL be reported as data, not findings.

---

# Authentication

Where authentication is configured, the SMTP Client SHALL resolve credentials
through the [Authentication](../authentication/README.md) package using a
credential reference.

Credentials SHALL NOT appear in evidence or logs. Authentication SHALL occur only
after TLS where the session requires confidentiality.

---

# Reply-Code Mapping

The SMTP Client SHALL map SMTP reply codes to canonical outcomes.

- `2xx` and `3xx` map to successful or intermediate outcomes
- `4xx` maps to transient, potentially retryable outcomes
- `5xx` maps to permanent, non-retryable outcomes

Reply-code interpretation as a security weakness SHALL remain with domain skills.

---

# Governance

The SMTP Client SHALL

- Acquire a permit from the [Rate Limiter](../rate-limiter/README.md) per session
- Route through the [Proxy](../proxy/README.md) shared skill where configured
- Recover transient failures through the [Retry](../retry/README.md) shared skill

Session duration and message size SHALL be bounded.

---

# Evidence

The SMTP Client Shared Skill SHOULD capture

- Server greeting and negotiated capabilities
- TLS upgrade outcome
- Command and reply-code sequence
- Session duration

Evidence SHALL conform to the canonical
[Evidence schema](../../../schemas/evidence.md) and SHALL NOT contain credentials
or message bodies unless explicitly authorized and redacted.

---

# Events

The SMTP Client Shared Skill SHOULD publish

- SessionStarted
- CapabilitiesNegotiated
- TlsUpgraded
- Authenticated
- CommandExchanged
- SessionClosed
- SessionFailed

Events SHALL integrate with the platform Execution State.

---

# Dependencies

The SMTP Client Shared Skill depends on

- [Configuration Model](../../core/configuration-model.md)
- [Execution Model](../../core/execution-model.md)
- [Error Handling](../../core/error-handling.md)
- [TCP Client](../tcp-client/README.md)
- [TLS Client](../tls-client/README.md)
- [Authentication](../authentication/README.md)
- [Rate Limiter](../rate-limiter/README.md)
- [Retry](../retry/README.md)
- [Evidence Schema](../../../schemas/evidence.md)

The SMTP Client Shared Skill SHALL NOT depend on domain skills.

---

# Consumers

Typical consumers include

- Mail-server assessment skills
- Open-relay and STARTTLS analysis skills
- Service enumeration skills probing SMTP

---

# Outputs

Typical outputs MAY include

- A session transcript of commands and reply codes
- Negotiated capabilities
- Session metrics
- SMTP evidence references

Outputs SHALL remain implementation independent.

---

# Security Principles

The SMTP Client Shared Skill SHALL

- Refuse cleartext where confidentiality is required
- Protect credentials from evidence and logs
- Avoid sending unsolicited mail
- Bound session duration and message size
- Report reply codes as data, not findings
- Preserve auditability

Sending mail can have real-world side effects. The shared skill SHALL treat
message-sending operations as intrusive and subject to authorization.

---

# Best Practices

Consumers SHOULD

- Prefer `STARTTLS` and require it for authenticated sessions
- Reference credentials rather than inlining secrets
- Bound session duration and message size
- Reference shared rate, retry, and proxy policies
- Capture session evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Speak SMTP over raw sockets
- Authenticate over cleartext
- Send unsolicited or unauthorized mail
- Interpret reply codes as findings within the transport layer
- Persist credentials in evidence

---

# Documentation Requirements

This shared skill includes

- README.md
- capabilities.md
- interface.md
- configuration.md
- execution.md
- error-model.md
- examples.md
- adr/ADR-001-smtp-transport-abstraction.md

---

# Related Shared Packages

- [TCP Client](../tcp-client/README.md)
- [TLS Client](../tls-client/README.md)
- [Authentication](../authentication/README.md)
- [Proxy](../proxy/README.md)

---

# Canonical Schemas

- [Evidence](../../../schemas/evidence.md)
- [TLS Session](../../../schemas/tls-session.md)

---

# Architecture Decisions

- [ADR-001 — SMTP Transport Abstraction](adr/ADR-001-smtp-transport-abstraction.md)

---

# Future Extensions

Future versions MAY support

- SMTPUTF8 and internationalized addresses
- DSN and delivery-status handling
- Submission-port and implicit-TLS profiles
- Pipelining optimization descriptors

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant SMTP Client Shared Skill provides a bounded, governed, and
implementation-independent SMTP transport abstraction for the Robust PenTest
Platform.

It enables consistent, auditable mail-protocol conversations atop the TCP and
TLS shared skills, without embedding security interpretation or transport
implementations in consumers.
