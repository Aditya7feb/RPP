# FTP Client Execution Model

**File:** `skills/shared/ftp-client/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the execution model for the FTP Client Shared Skill.

The execution model describes how the shared skill conducts a session from
control-channel establishment through TLS upgrade, authentication, data-channel
coordination, command exchange, and closure.

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

Establish Control Channel (TCP Client)

↓

Read Greeting

↓

AUTH TLS (if required/available) → TLS Client

↓

Authenticate (USER / PASS)

↓

Set Transfer Type And Mode

↓

Open Data Channel (passive/active)

↓

Exchange Commands / Transfer

↓

QUIT / Close

↓

Emit Evidence and Events

↓

Return Result
```

---

# Stage 1 — Configuration Resolution

The FTP Client SHALL resolve security, data-channel, bounds, and governance using
the precedence defined in [configuration.md](configuration.md).

A required-TLS setting SHALL always be honored.

---

# Stage 2 — Rate Permit

The FTP Client SHALL acquire a permit from the
[Rate Limiter](../rate-limiter/README.md) for the session.

---

# Stage 3 — Control Channel

The FTP Client SHALL establish the control channel through the
[TCP Client](../tcp-client/README.md), routed through the
[Proxy](../proxy/README.md) shared skill where configured.

---

# Stage 4 — Greeting And FTPS

The FTP Client SHALL read the greeting.

Where `tls_mode` is `explicit_optional` or `explicit_required` and FTPS is
available, the FTP Client SHALL issue `AUTH TLS` and upgrade the control channel
through the [TLS Client](../tls-client/README.md).

Where `tls_mode` is `explicit_required` and FTPS is unavailable, the session
SHALL terminate with `tls_required_unavailable`.

---

# Stage 5 — Authentication

The FTP Client SHALL authenticate through the
[Authentication](../authentication/README.md) package, or anonymously where
requested.

Non-anonymous authentication over cleartext SHALL be refused when confidentiality
is required.

Credentials SHALL never appear in the transcript or evidence.

---

# Stage 6 — Transfer Setup

The FTP Client SHALL set the transfer type and open a data channel in the
configured mode, preferring passive.

Data-channel establishment SHALL respect proxy and rate governance and acquire a
permit per transfer.

---

# Stage 7 — Command Exchange

The FTP Client SHALL issue the command program, bounded by `command_timeout` and
`max_transfer_bytes`.

Write and delete commands SHALL be issued only when `allow_write_operations` is
enabled, as they are intrusive.

The FTP Client SHALL record each command and its reply code.

---

# Stage 8 — Reply Mapping

The FTP Client SHALL map reply codes to canonical outcomes.

- `1xx`/`2xx`/`3xx` map to intermediate or success
- `4xx` maps to transient, potentially retryable
- `5xx` maps to permanent, non-retryable

---

# Stage 9 — Closure

The FTP Client SHALL issue `QUIT` and close both channels, releasing resources
including on error.

---

# Stage 10 — Evidence And Events

The FTP Client SHOULD emit session evidence and lifecycle events according to
configuration. Evidence SHALL exclude credentials.

---

# Retry Behavior

Transient `4xx` outcomes and connection failures MAY be retried through the
[Retry](../retry/README.md) shared skill, each retry acquiring a fresh permit.

Write operations SHALL be retried only when idempotent and authorized.

---

# Determinism

Given identical configuration and inputs, the FTP Client SHALL enforce identical
bounds and produce identical outcome classifications for the same observed server
behavior.

---

# Failure Handling

Execution failures SHALL be classified according to
[error-model.md](error-model.md).

A failed session SHALL close both channels and SHALL NOT leak partial state.

---

# Execution Outputs

The execution model SHALL produce

- A command and reply-code transcript
- Transfer summaries
- Session metrics
- Evidence references

Outputs SHALL remain implementation independent.

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Error Model](error-model.md)
- [TCP Client](../tcp-client/README.md)
- [TLS Client](../tls-client/README.md)
- [Execution Model](../../core/execution-model.md)
