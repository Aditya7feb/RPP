# FTP Client Shared Skill

**File:** `skills/shared/ftp-client/README.md`

**Version:** 1.0.0

---

# Purpose

The FTP Client Shared Skill provides the canonical, implementation-independent
mechanism for conducting File Transfer Protocol (FTP) conversations within the
Robust PenTest Platform (RPP).

Rather than allowing individual skills to speak FTP directly over raw sockets,
this shared skill centralizes control-channel establishment, data-channel
coordination, explicit TLS (FTPS), authentication, command exchange, reply-code
mapping, and observability.

All packages that require FTP transport SHALL delegate to this shared skill.

---

# Goals

The FTP Client Shared Skill SHALL

- Abstract FTP transport behind a stable interface
- Establish control channels through the [TCP Client](../tcp-client/README.md)
- Coordinate passive and active data channels
- Upgrade to TLS through explicit FTPS via the
  [TLS Client](../tls-client/README.md)
- Authenticate through the [Authentication](../authentication/README.md) package
- Exchange commands and map reply codes to canonical outcomes
- Produce FTP evidence
- Integrate with platform observability

---

# Non-Goals

The FTP Client Shared Skill SHALL NOT

- Detect vulnerabilities such as anonymous write access
- Produce security findings
- Interpret reply codes as security weaknesses
- Parse transferred file contents as findings
- Modify remote files without authorization

The FTP Client conducts protocol conversations and reports outcomes as data.
Interpretation belongs to domain skills.

---

# Design Principles

The FTP Client Shared Skill SHALL be

- Deterministic in bounds given the same configuration and inputs
- Layered atop the TCP and TLS shared skills
- Bounded in transfer size and session duration
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

FTP Client Shared Skill

├── Control Channel         → TCP Client
├── Data Channel Coordinator → TCP Client
├── FTPS Upgrader           → TLS Client
├── Authenticator           → Authentication
├── Command Exchanger
├── Reply Mapper
├── Evidence Manager
├── Event Manager

↓

Transport Adapter
```

The FTP Client conducts the conversation but SHALL remain unaware of the
transport adapter implementation.

---

# Responsibilities

The FTP Client Shared Skill is responsible for

- Establishing the control channel via the [TCP Client](../tcp-client/README.md)
- Upgrading to TLS via explicit FTPS through the
  [TLS Client](../tls-client/README.md)
- Authenticating via the [Authentication](../authentication/README.md) package
- Coordinating passive or active data channels
- Exchanging commands such as `LIST`, `RETR`, and `STOR`
- Mapping FTP reply codes to canonical outcomes
- Applying rate, retry, and proxy governance
- Emitting FTP lifecycle events and capturing evidence

---

# Session Lifecycle

```
Receive Session Request

↓

Acquire Rate Permit

↓

Establish Control Channel (TCP Client)

↓

Read Greeting

↓

AUTH TLS (if required/available) → TLS Client

↓

Authenticate (USER / PASS)

↓

Set Transfer Mode

↓

Open Data Channel (passive/active)

↓

Exchange Commands / Transfer

↓

QUIT / Close

↓

Emit Evidence and Events
```

The session outcome SHOULD be preserved as evidence.

---

# Data Channels

The FTP Client SHALL coordinate data channels through the
[TCP Client](../tcp-client/README.md).

Passive mode SHALL be preferred to simplify proxy and firewall traversal.

Active mode SHALL be used only where explicitly configured and permitted by
governance.

Data-channel establishment SHALL respect the same proxy and rate governance as
the control channel.

---

# Explicit TLS (FTPS)

The FTP Client SHALL support explicit FTPS by issuing `AUTH TLS` and upgrading
the control channel through the [TLS Client](../tls-client/README.md).

Data channels SHALL be protected consistently with the control channel where TLS
is negotiated.

Where a session requires TLS and FTPS is unavailable, the session SHALL terminate
rather than continue in cleartext.

Certificate validation outcomes SHALL be reported as data, not findings.

---

# Authentication

Where authentication is configured, the FTP Client SHALL resolve credentials
through the [Authentication](../authentication/README.md) package.

Anonymous authentication MAY be used where explicitly requested; the fact of
anonymous access SHALL be reported as data, not a finding.

Credentials SHALL NOT appear in evidence or logs.

---

# Reply-Code Mapping

The FTP Client SHALL map FTP reply codes to canonical outcomes.

- `1xx`/`2xx`/`3xx` map to intermediate or successful outcomes
- `4xx` maps to transient, potentially retryable outcomes
- `5xx` maps to permanent, non-retryable outcomes

Reply-code interpretation as a security weakness SHALL remain with domain skills.

---

# Governance

The FTP Client SHALL

- Acquire a permit from the [Rate Limiter](../rate-limiter/README.md) per session
  and per data transfer
- Route through the [Proxy](../proxy/README.md) shared skill where configured
- Recover transient failures through the [Retry](../retry/README.md) shared skill

Write and delete operations SHALL be treated as intrusive and subject to
authorization.

---

# Evidence

The FTP Client Shared Skill SHOULD capture

- Greeting and negotiated features
- TLS upgrade outcome
- Command and reply-code sequence
- Transfer sizes and directions
- Session duration

Evidence SHALL conform to the canonical
[Evidence schema](../../../schemas/evidence.md) and SHALL NOT contain credentials
or transferred file contents unless explicitly authorized and redacted.

---

# Events

The FTP Client Shared Skill SHOULD publish

- SessionStarted
- TlsUpgraded
- Authenticated
- DataChannelOpened
- CommandExchanged
- TransferCompleted
- SessionClosed
- SessionFailed

Events SHALL integrate with the platform Execution State.

---

# Dependencies

The FTP Client Shared Skill depends on

- [Configuration Model](../../core/configuration-model.md)
- [Execution Model](../../core/execution-model.md)
- [Error Handling](../../core/error-handling.md)
- [TCP Client](../tcp-client/README.md)
- [TLS Client](../tls-client/README.md)
- [Authentication](../authentication/README.md)
- [Rate Limiter](../rate-limiter/README.md)
- [Retry](../retry/README.md)
- [Evidence Schema](../../../schemas/evidence.md)

The FTP Client Shared Skill SHALL NOT depend on domain skills.

---

# Consumers

Typical consumers include

- FTP-server assessment skills
- Anonymous-access and FTPS analysis skills
- Service enumeration skills probing FTP

---

# Outputs

Typical outputs MAY include

- A session transcript of commands and reply codes
- Directory listings by reference
- Transfer metrics
- FTP evidence references

Outputs SHALL remain implementation independent.

---

# Security Principles

The FTP Client Shared Skill SHALL

- Refuse cleartext where confidentiality is required
- Protect credentials from evidence and logs
- Treat write and delete operations as intrusive
- Bound transfer size and session duration
- Report reply codes as data, not findings
- Preserve auditability

Modifying remote files can have real-world side effects. The shared skill SHALL
treat such operations as intrusive and subject to authorization.

---

# Best Practices

Consumers SHOULD

- Prefer explicit FTPS and require it for authenticated sessions
- Prefer passive mode for traversal
- Reference credentials rather than inlining secrets
- Bound transfer size and session duration
- Capture session evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Speak FTP over raw sockets
- Authenticate over cleartext
- Perform unauthorized writes or deletes
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
- adr/ADR-001-ftp-transport-abstraction.md

---

# Related Shared Packages

- [TCP Client](../tcp-client/README.md)
- [TLS Client](../tls-client/README.md)
- [Authentication](../authentication/README.md)
- [SMTP Client](../smtp-client/README.md)

---

# Canonical Schemas

- [Evidence](../../../schemas/evidence.md)
- [TLS Session](../../../schemas/tls-session.md)

---

# Architecture Decisions

- [ADR-001 — FTP Transport Abstraction](adr/ADR-001-ftp-transport-abstraction.md)

---

# Future Extensions

Future versions MAY support

- Implicit FTPS profiles
- MLST and MLSD structured listings
- Resume and range transfers
- IPv6 extended passive mode descriptors

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant FTP Client Shared Skill provides a bounded, governed, and
implementation-independent FTP transport abstraction for the Robust PenTest
Platform.

It enables consistent, auditable file-transfer conversations atop the TCP and
TLS shared skills, without embedding security interpretation or transport
implementations in consumers.
