# SSH Client Shared Skill

**File:** `skills/shared/ssh-client/README.md`

**Version:** 1.0.0

---

# Purpose

The SSH Client Shared Skill provides the canonical, implementation-independent
mechanism for establishing Secure Shell (SSH) sessions within the Robust PenTest
Platform (RPP).

Rather than allowing individual skills to negotiate SSH directly, this shared
skill centralizes transport negotiation, host-key handling, authentication,
channel management, command and subsystem execution, and observability.

All packages that require SSH transport SHALL delegate to this shared skill.

---

# Goals

The SSH Client Shared Skill SHALL

- Abstract SSH transport behind a stable interface
- Establish connections through the [TCP Client](../tcp-client/README.md)
- Negotiate transport algorithms and record them as data
- Verify host keys against a configured trust policy
- Authenticate through the [Authentication](../authentication/README.md) package
- Open channels for commands, subsystems, and port forwarding
- Produce SSH evidence
- Integrate with platform observability

---

# Non-Goals

The SSH Client Shared Skill SHALL NOT

- Detect vulnerabilities such as weak algorithms or credential reuse
- Produce security findings
- Interpret negotiated algorithms as weaknesses
- Execute exploitation payloads implicitly
- Parse command output as findings

The SSH Client establishes sessions and executes explicitly requested,
authorized operations. Interpretation belongs to domain skills.

---

# Design Principles

The SSH Client Shared Skill SHALL be

- Deterministic in bounds given the same configuration and inputs
- Layered atop the TCP shared skill
- Bounded in output size and session duration
- Trust-policy driven for host keys
- Governed
- Secure by default

---

# Architecture

```
Master Agent

↓

Domain Skill

↓

SSH Client Shared Skill

├── Transport Establisher    → TCP Client
├── Host-Key Verifier
├── Authenticator            → Authentication
├── Channel Manager
├── Command Executor
├── Evidence Manager
├── Event Manager

↓

Transport Adapter
```

The SSH Client conducts the session but SHALL remain unaware of the transport
adapter implementation.

---

# Responsibilities

The SSH Client Shared Skill is responsible for

- Establishing the transport via the [TCP Client](../tcp-client/README.md)
- Negotiating and recording transport algorithms
- Verifying the host key against a configured trust policy
- Authenticating via the [Authentication](../authentication/README.md) package
- Opening channels for commands, subsystems such as SFTP, and forwarding
- Executing explicitly requested, authorized commands with bounded output
- Applying rate, retry, and proxy governance
- Emitting SSH lifecycle events and capturing evidence

---

# Session Lifecycle

```
Receive Session Request

↓

Acquire Rate Permit

↓

Establish Transport (TCP Client)

↓

Negotiate Algorithms

↓

Verify Host Key (trust policy)

↓

Authenticate

↓

Open Channel(s)

↓

Execute Commands / Subsystems (bounded, authorized)

↓

Close Session

↓

Emit Evidence and Events
```

The session outcome SHOULD be preserved as evidence.

---

# Host-Key Verification

The SSH Client SHALL verify the presented host key against a configured trust
policy.

The trust policy SHALL be one of

```
strict

trust_on_first_use

record_only
```

`strict` SHALL reject unknown or changed host keys.

`trust_on_first_use` SHALL accept and pin a previously unseen key and reject
subsequent changes.

`record_only` SHALL record the key without rejecting, and SHALL be used only
where explicitly permitted for discovery.

The host-key fingerprint SHALL be recorded as data. Whether a key represents a
weakness SHALL be interpreted by domain skills.

---

# Authentication

Where authentication is configured, the SSH Client SHALL resolve credentials
through the [Authentication](../authentication/README.md) package, supporting

- password
- public_key
- keyboard_interactive
- agent

Credentials and private keys SHALL NOT appear in evidence or logs.

---

# Channels And Execution

The SSH Client SHALL open channels for

- command execution
- shell sessions
- subsystems such as SFTP
- local and remote port forwarding

Command and shell execution SHALL be treated as intrusive and SHALL be gated by
authorization. Output SHALL be bounded and stored by reference.

Port forwarding SHALL be permitted only where explicitly configured.

---

# Governance

The SSH Client SHALL

- Acquire a permit from the [Rate Limiter](../rate-limiter/README.md) per session
- Route through the [Proxy](../proxy/README.md) shared skill where configured,
  including jump-host style traversal
- Recover transient transport failures through the [Retry](../retry/README.md)
  shared skill

Authentication attempts SHALL be bounded to avoid brute-force behavior; credential
guessing belongs to a dedicated, authorized domain skill, not this transport.

---

# Evidence

The SSH Client Shared Skill SHOULD capture

- Negotiated algorithms
- Host-key fingerprint and trust decision
- Authentication method and outcome
- Channels opened and commands executed
- Bounded command output by reference
- Session duration

Evidence SHALL conform to the canonical
[Evidence schema](../../../schemas/evidence.md) and SHALL NOT contain credentials,
private keys, or unauthorized output.

---

# Events

The SSH Client Shared Skill SHOULD publish

- SessionStarted
- AlgorithmsNegotiated
- HostKeyVerified
- Authenticated
- ChannelOpened
- CommandExecuted
- SessionClosed
- SessionFailed

Events SHALL integrate with the platform Execution State.

---

# Dependencies

The SSH Client Shared Skill depends on

- [Configuration Model](../../core/configuration-model.md)
- [Execution Model](../../core/execution-model.md)
- [Error Handling](../../core/error-handling.md)
- [TCP Client](../tcp-client/README.md)
- [Authentication](../authentication/README.md)
- [Rate Limiter](../rate-limiter/README.md)
- [Retry](../retry/README.md)
- [Evidence Schema](../../../schemas/evidence.md)

The SSH Client Shared Skill SHALL NOT depend on domain skills.

---

# Consumers

Typical consumers include

- SSH-server assessment skills
- Post-authentication configuration-review skills
- Service enumeration skills probing SSH

---

# Outputs

Typical outputs MAY include

- Negotiated algorithm records
- Host-key fingerprints
- Bounded command output by reference
- Session metrics
- SSH evidence references

Outputs SHALL remain implementation independent.

---

# Security Principles

The SSH Client Shared Skill SHALL

- Verify host keys against a trust policy
- Protect credentials and private keys from evidence and logs
- Treat command and shell execution as intrusive
- Bound authentication attempts and output size
- Report negotiated algorithms as data, not findings
- Preserve auditability

Executing remote commands has real-world side effects. The shared skill SHALL
treat execution as intrusive and subject to authorization.

---

# Best Practices

Consumers SHOULD

- Use `strict` host-key policy outside discovery contexts
- Reference credentials and keys rather than inlining them
- Bound command output and session duration
- Authorize command execution explicitly
- Capture session evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Negotiate SSH directly
- Disable host-key verification silently
- Brute-force credentials through this transport
- Execute unauthorized commands
- Persist credentials or private keys in evidence

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
- adr/ADR-001-ssh-transport-abstraction.md

---

# Related Shared Packages

- [TCP Client](../tcp-client/README.md)
- [Authentication](../authentication/README.md)
- [Proxy](../proxy/README.md)
- [FTP Client](../ftp-client/README.md)

---

# Canonical Schemas

- [Evidence](../../../schemas/evidence.md)

---

# Architecture Decisions

- [ADR-001 — SSH Transport Abstraction](adr/ADR-001-ssh-transport-abstraction.md)

---

# Future Extensions

Future versions MAY support

- Certificate-based host and user authentication
- Multiplexed session reuse
- Structured SFTP operations
- Agent-forwarding descriptors under strict governance

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant SSH Client Shared Skill provides a bounded, governed, and
implementation-independent SSH transport abstraction for the Robust PenTest
Platform.

It enables consistent, auditable SSH sessions atop the TCP shared skill while
enforcing host-key trust and authorization, without embedding security
interpretation or transport implementations in consumers.
