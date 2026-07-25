# SMTP Client Execution Model

**File:** `skills/shared/smtp-client/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the execution model for the SMTP Client Shared Skill.

The execution model describes how the shared skill conducts a session from
establishment through capability negotiation, TLS upgrade, authentication,
command exchange, and closure.

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

Establish Session (TCP Client)

↓

Read Greeting

↓

EHLO → Negotiate Capabilities

↓

STARTTLS (if required/available) → TLS Client

↓

Authenticate (if configured)

↓

Exchange Commands

↓

QUIT / Close

↓

Emit Evidence and Events

↓

Return Result
```

---

# Stage 1 — Configuration Resolution

The SMTP Client SHALL resolve security, bounds, and governance using the
precedence defined in [configuration.md](configuration.md).

A required-TLS setting SHALL always be honored.

---

# Stage 2 — Rate Permit

The SMTP Client SHALL acquire a permit from the
[Rate Limiter](../rate-limiter/README.md) for the session.

---

# Stage 3 — Session Establishment

The SMTP Client SHALL establish the session through the
[TCP Client](../tcp-client/README.md), routed through the
[Proxy](../proxy/README.md) shared skill where configured.

For `implicit` TLS, the channel SHALL be secured immediately through the
[TLS Client](../tls-client/README.md).

---

# Stage 4 — Greeting And EHLO

The SMTP Client SHALL read the server greeting and issue `EHLO`, recording
advertised capabilities.

A greeting or `EHLO` failure SHALL produce a canonical error.

---

# Stage 5 — STARTTLS

Where `tls_mode` is `starttls_optional` or `starttls_required` and `STARTTLS` is
advertised, the SMTP Client SHALL upgrade through the
[TLS Client](../tls-client/README.md) and re-issue `EHLO`.

Where `tls_mode` is `starttls_required` and `STARTTLS` is unavailable, the
session SHALL terminate with `tls_required_unavailable` rather than continuing in
cleartext.

---

# Stage 6 — Authentication

Where authentication is configured, the SMTP Client SHALL authenticate through
the [Authentication](../authentication/README.md) package.

Authentication SHALL occur only after TLS when confidentiality is required.

Credentials SHALL never appear in the transcript or evidence.

---

# Stage 7 — Command Exchange

The SMTP Client SHALL issue the command program, bounded by `command_timeout`,
`max_recipients`, and `max_message_bytes`.

Commands that transmit mail SHALL be issued only when `allow_message_send` is
enabled, as they are intrusive and subject to authorization.

The SMTP Client SHALL record each command and its reply code.

---

# Stage 8 — Reply Mapping

The SMTP Client SHALL map reply codes to canonical outcomes.

- `2xx`/`3xx` map to success or intermediate
- `4xx` maps to transient, potentially retryable
- `5xx` maps to permanent, non-retryable

---

# Stage 9 — Closure

The SMTP Client SHALL issue `QUIT` and close the session, releasing resources
including on error.

---

# Stage 10 — Evidence And Events

The SMTP Client SHOULD emit session evidence and lifecycle events according to
configuration. Evidence SHALL exclude credentials.

---

# Retry Behavior

Transient `4xx` outcomes and connection failures MAY be retried through the
[Retry](../retry/README.md) shared skill, each retry acquiring a fresh permit.

Message-sending commands SHALL be retried only when idempotent and authorized.

---

# Determinism

Given identical configuration and inputs, the SMTP Client SHALL enforce identical
bounds and produce identical outcome classifications for the same observed server
behavior.

---

# Failure Handling

Execution failures SHALL be classified according to
[error-model.md](error-model.md).

A failed session SHALL be fully closed and SHALL NOT leak partial state.

---

# Execution Outputs

The execution model SHALL produce

- A command and reply-code transcript
- Negotiated capabilities
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
