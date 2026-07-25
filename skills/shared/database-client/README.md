# Database Client Shared Skill

**File:** `skills/shared/database-client/README.md`

**Version:** 1.0.0

---

# Purpose

The Database Client Shared Skill provides the canonical,
implementation-independent mechanism for executing parameterized database
operations within the Robust PenTest Platform (RPP).

Rather than allowing individual skills to open database connections and build
queries directly, this shared skill centralizes connection establishment,
transport encryption, authentication, parameterized statement execution, result
handling, and observability.

All packages that require database access SHALL delegate to this shared skill.

---

# Goals

The Database Client Shared Skill SHALL

- Abstract database engines behind a stable interface
- Establish connections through the [TCP Client](../tcp-client/README.md)
- Encrypt transport through the [TLS Client](../tls-client/README.md) where
  supported
- Authenticate through the [Authentication](../authentication/README.md) package
- Execute parameterized statements with bounded result sets
- Manage transactions explicitly
- Produce database evidence
- Integrate with platform observability

---

# Non-Goals

The Database Client Shared Skill SHALL NOT

- Detect vulnerabilities such as SQL injection
- Produce security findings
- Construct queries by concatenating untrusted input
- Interpret result contents as findings
- Perform schema changes without authorization

The Database Client executes explicitly authorized, parameterized operations and
reports results as data. Interpretation, including injection testing, belongs to
domain skills, which SHALL use this client's parameterization to remain safe.

---

# Design Principles

The Database Client Shared Skill SHALL be

- Deterministic in bounds given the same configuration and inputs
- Parameterization-first to prevent injection at the boundary
- Layered atop the TCP and TLS shared skills
- Bounded in result size and statement duration
- Governed
- Secure by default

---

# Architecture

```
Master Agent

↓

Domain Skill

↓

Database Client Shared Skill

├── Connection Establisher   → TCP Client
├── Transport Encryptor      → TLS Client
├── Authenticator            → Authentication
├── Statement Executor
├── Transaction Manager
├── Result Handler
├── Evidence Manager
├── Event Manager

↓

Engine Adapter
```

The Database Client executes operations but SHALL remain unaware of the engine
adapter implementation.

---

# Responsibilities

The Database Client Shared Skill is responsible for

- Establishing the connection via the [TCP Client](../tcp-client/README.md)
- Encrypting transport via the [TLS Client](../tls-client/README.md)
- Authenticating via the [Authentication](../authentication/README.md) package
- Executing parameterized statements with bound parameters
- Managing explicit transactions
- Returning bounded result sets by reference
- Applying rate, retry, and proxy governance
- Emitting database lifecycle events and capturing evidence

---

# Operation Lifecycle

```
Receive Operation Request

↓

Acquire Rate Permit

↓

Establish Connection (TCP Client)

↓

Encrypt Transport (TLS Client)

↓

Authenticate

↓

Begin Transaction (if requested)

↓

Execute Parameterized Statement(s)

↓

Handle Bounded Results

↓

Commit / Rollback

↓

Close Connection

↓

Emit Evidence and Events
```

The operation outcome SHOULD be preserved as evidence.

---

# Parameterized Execution

The Database Client SHALL execute statements using bound parameters supplied
separately from statement text.

The Database Client SHALL NOT interpolate parameter values into statement text.

This parameterization is a safety boundary: domain skills testing for injection
SHALL supply payloads as parameters or as explicitly marked statement text,
never through implicit concatenation.

Statement text SHALL be treated as caller-provided and SHALL NOT be modified by
the client.

---

# Transport Encryption

Where the engine supports it, the Database Client SHALL encrypt transport through
the [TLS Client](../tls-client/README.md).

Where a connection requires encryption and it is unavailable, the connection
SHALL fail rather than proceed in cleartext.

Certificate validation outcomes SHALL be reported as data, not findings.

---

# Authentication

Where authentication is configured, the Database Client SHALL resolve credentials
through the [Authentication](../authentication/README.md) package.

Credentials SHALL NOT appear in evidence, logs, or statement text.

---

# Transactions

The Database Client SHALL support explicit transactions with begin, commit, and
rollback.

Statements that modify data or schema SHALL be treated as intrusive and SHALL be
gated by authorization.

Read-only operations SHALL be preferred by default.

---

# Result Handling

The Database Client SHALL bound returned result sets by row and byte limits.

Large result sets SHALL be stored by reference rather than inlined.

The Database Client SHALL NOT interpret result contents as findings.

---

# Governance

The Database Client SHALL

- Acquire a permit from the [Rate Limiter](../rate-limiter/README.md) per
  operation
- Route through the [Proxy](../proxy/README.md) shared skill where configured
- Recover transient connection failures through the [Retry](../retry/README.md)
  shared skill

Write and schema-change statements SHALL be gated as intrusive.

---

# Evidence

The Database Client Shared Skill SHOULD capture

- Engine and connection target
- Transport-encryption outcome
- Statement kind and parameter count, excluding parameter values
- Row and byte counts
- Transaction outcome
- Operation duration

Evidence SHALL conform to the canonical
[Evidence schema](../../../schemas/evidence.md) and SHALL NOT contain credentials
or sensitive result contents unless explicitly authorized and redacted.

---

# Events

The Database Client Shared Skill SHOULD publish

- ConnectionEstablished
- TransportEncrypted
- Authenticated
- TransactionBegan
- StatementExecuted
- TransactionCommitted
- ConnectionClosed
- OperationFailed

Events SHALL integrate with the platform Execution State.

---

# Dependencies

The Database Client Shared Skill depends on

- [Configuration Model](../../core/configuration-model.md)
- [Execution Model](../../core/execution-model.md)
- [Error Handling](../../core/error-handling.md)
- [TCP Client](../tcp-client/README.md)
- [TLS Client](../tls-client/README.md)
- [Authentication](../authentication/README.md)
- [Rate Limiter](../rate-limiter/README.md)
- [Retry](../retry/README.md)
- [Evidence Schema](../../../schemas/evidence.md)

The Database Client Shared Skill SHALL NOT depend on domain skills.

---

# Consumers

Typical consumers include

- SQL-injection testing skills, which use parameterization to stay safe
- Database configuration-review skills
- Service enumeration skills probing database ports

---

# Outputs

Typical outputs MAY include

- Bounded result sets by reference
- Row and byte counts
- Transaction outcomes
- Database evidence references

Outputs SHALL remain implementation independent.

---

# Security Principles

The Database Client Shared Skill SHALL

- Enforce parameterization to prevent injection at the boundary
- Require encryption where confidentiality is mandated
- Protect credentials from evidence, logs, and statement text
- Treat data and schema modification as intrusive
- Bound result size and statement duration
- Report results as data, not findings
- Preserve auditability

Database operations can expose sensitive data and cause irreversible changes. The
shared skill SHALL enforce parameterization, encryption, and authorization.

---

# Best Practices

Consumers SHOULD

- Supply values as bound parameters
- Prefer read-only operations
- Require encryption for sensitive engines
- Reference credentials rather than inlining them
- Bound result sets and capture evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Concatenate untrusted input into statements
- Open database connections directly
- Perform unauthorized writes or schema changes
- Interpret result contents as findings within the transport layer
- Persist credentials or sensitive results in evidence

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
- adr/ADR-001-database-transport-abstraction.md

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

- [ADR-001 — Database Transport Abstraction](adr/ADR-001-database-transport-abstraction.md)

---

# Future Extensions

Future versions MAY support

- Prepared-statement reuse handles
- Streaming cursor result descriptors
- Connection pooling
- Engine-specific capability descriptors expressed canonically

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Database Client Shared Skill provides a bounded, parameterized, and
implementation-independent database transport abstraction for the Robust PenTest
Platform.

It enables consistent, auditable database operations atop the TCP and TLS shared
skills while preventing injection at the boundary and protecting credentials,
without embedding security interpretation or engine implementations in
consumers.
