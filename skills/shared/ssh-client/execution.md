# SSH Client Execution Model

**File:** `skills/shared/ssh-client/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the execution model for the SSH Client Shared Skill.

The execution model describes how the shared skill establishes a session from
transport negotiation through host-key verification, authentication, channel
operations, and closure.

The model is deterministic in bounds given the same configuration and inputs.

---

# Execution Overview

```
Receive Session Request

↓

Resolve Configuration

↓

Acquire Rate Permit

↓

Establish Transport (TCP Client)

↓

Negotiate Algorithms

↓

Verify Host Key (trust policy)

↓

Authenticate (bounded attempts)

↓

Open Channel(s)

↓

Execute Operations (bounded, authorized)

↓

Close Session

↓

Emit Evidence and Events

↓

Return Result
```

---

# Stage 1 — Configuration Resolution

The SSH Client SHALL resolve host-key trust, authentication bounds, execution
gating, and governance using the precedence defined in
[configuration.md](configuration.md).

A mandated `strict` policy SHALL always be honored.

---

# Stage 2 — Rate Permit

The SSH Client SHALL acquire a permit from the
[Rate Limiter](../rate-limiter/README.md) for the session.

---

# Stage 3 — Transport

The SSH Client SHALL establish the transport through the
[TCP Client](../tcp-client/README.md), routed through the
[Proxy](../proxy/README.md) shared skill where configured, including jump-host
traversal.

---

# Stage 4 — Algorithm Negotiation

The SSH Client SHALL negotiate transport algorithms and record them as data.

Negotiated algorithms SHALL NOT be classified as weaknesses by the shared skill.

---

# Stage 5 — Host-Key Verification

The SSH Client SHALL verify the host key against the trust policy.

- `strict` SHALL reject unknown or changed keys
- `trust_on_first_use` SHALL pin an unseen key and reject changes
- `record_only` SHALL record without rejecting, only where permitted

The fingerprint and trust decision SHALL be recorded.

---

# Stage 6 — Authentication

The SSH Client SHALL authenticate through the
[Authentication](../authentication/README.md) package using the declared method,
bounded by `max_attempts`.

Credentials and private keys SHALL never appear in evidence.

The shared skill SHALL NOT perform credential guessing; brute-force belongs to a
dedicated authorized domain skill.

---

# Stage 7 — Channel Operations

The SSH Client SHALL open the requested channels.

- `exec` and `shell` SHALL run only when execution is authorized
- `subsystem` SHALL open subsystems such as SFTP
- `forward` SHALL run only when forwarding is permitted

Command output SHALL be bounded by `max_output_bytes` and stored by reference.

---

# Stage 8 — Closure

The SSH Client SHALL close all channels and the session, releasing resources
including on error.

---

# Stage 9 — Evidence And Events

The SSH Client SHOULD emit session evidence and lifecycle events according to
configuration. Evidence SHALL exclude credentials, keys, and unauthorized
output.

---

# Retry Behavior

Transient transport failures MAY be retried through the
[Retry](../retry/README.md) shared skill, each retry acquiring a fresh permit.

Authentication failures SHALL NOT be retried beyond `max_attempts`.

Command execution SHALL be retried only when idempotent and authorized.

---

# Determinism

Given identical configuration and inputs, the SSH Client SHALL enforce identical
bounds and produce identical outcome classifications for the same observed server
behavior.

---

# Failure Handling

Execution failures SHALL be classified according to
[error-model.md](error-model.md).

A failed session SHALL close all channels and SHALL NOT leak partial state.

---

# Execution Outputs

The execution model SHALL produce

- Negotiated algorithm records
- Host-key fingerprint and trust decision
- Operation results with bounded output references
- Session metrics
- Evidence references

Outputs SHALL remain implementation independent.

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Error Model](error-model.md)
- [TCP Client](../tcp-client/README.md)
- [Authentication](../authentication/README.md)
- [Execution Model](../../core/execution-model.md)
