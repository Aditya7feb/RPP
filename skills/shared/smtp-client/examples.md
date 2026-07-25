# SMTP Client Examples

**File:** `skills/shared/smtp-client/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-independent examples of the
SMTP Client Shared Skill in use.

Examples demonstrate session establishment, capability negotiation, STARTTLS,
authentication, reply mapping, governance, evidence, and expected outputs.

All examples are illustrative and contain no implementation code.

---

# Example 1 — Capability Probe With STARTTLS

A mail-server assessment skill negotiates capabilities and upgrades to TLS.

## Invocation

```yaml
metadata:
  request_id: req-9401
  assessment_id: asmt-42
  task_id: task-smtp-probe
  skill_id: mail-assessment
host: mail.example.com
port: 587
ehlo_name: scanner.example.org
tls_mode: starttls_required
commands:
  - verb: EHLO
  - verb: QUIT
```

## Result

```yaml
outcome: completed
capabilities:
  - STARTTLS
  - AUTH LOGIN PLAIN
  - SIZE 10485760
tls_established: true
transcript:
  - command: EHLO
    reply_code: 250
  - command: STARTTLS
    reply_code: 220
  - command: EHLO
    reply_code: 250
  - command: QUIT
    reply_code: 221
```

Capabilities are reported as data; open-relay or weak-TLS assessment is left to
domain skills.

---

# Example 2 — Required TLS Unavailable

`STARTTLS` is required but not advertised.

## Result

```yaml
outcome: tls_required_unavailable
error:
  category: Security
  code: tls_required_unavailable
  retryable: false
```

The session terminates rather than continuing in cleartext.

---

# Example 3 — Authenticated Session Over TLS

Authentication occurs only after TLS.

## Invocation

```yaml
tls_mode: starttls_required
credential_ref: cred-smtp-service
mechanism: PLAIN
```

## Result

```yaml
outcome: completed
tls_established: true
authenticated: true
```

Credentials are resolved by the
[Authentication](../authentication/README.md) package and never appear in the
transcript.

---

# Example 4 — Message Send Blocked

A message-sending command is attempted while sending is disabled.

## Configuration

```yaml
governance:
  allow_message_send: false
```

## Result

```yaml
outcome: rejected
error:
  category: Governance
  code: send_blocked
  retryable: false
```

Mail transmission is treated as intrusive and requires authorization.

---

# Example 5 — Transient Reply Retried

A `4xx` greylisting reply is retried.

## Flow

```
Attempt 1 → acquire permit → 451 try again

↓ Retry

Attempt 2 → acquire permit → 250 ok
```

Each attempt acquires its own rate permit.

---

# Example 6 — Permanent Reply

A `5xx` reply is not retried.

## Result

```yaml
outcome: completed
transcript:
  - command: RCPT TO
    reply_code: 550
error:
  category: Protocol
  code: permanent_reply
  reply_code: 550
  retryable: false
```

The reply code is preserved for domain interpretation.

---

# Example 7 — Evidence Record

A single session produces the following evidence.

```yaml
evidence:
  type: smtp-session
  host: mail.example.com:587
  tls_established: true
  capabilities:
    - STARTTLS
    - AUTH LOGIN PLAIN
  transcript_codes: [250, 220, 250, 221]
  duration_ms: 402
  decided_at: 2026-07-25T15:00:00Z
```

The evidence conforms to the canonical
[Evidence schema](../../../schemas/evidence.md), excludes credentials, and
supports auditing.

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Execution](execution.md)
- [Error Model](error-model.md)
- [TCP Client](../tcp-client/README.md)
- [TLS Client](../tls-client/README.md)
