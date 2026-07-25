# FTP Client Examples

**File:** `skills/shared/ftp-client/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-independent examples of the
FTP Client Shared Skill in use.

Examples demonstrate session establishment, FTPS upgrade, authentication,
passive transfers, reply mapping, governance, evidence, and expected outputs.

All examples are illustrative and contain no implementation code.

---

# Example 1 — FTPS Directory Listing

An FTP-server assessment skill authenticates over FTPS and lists a directory.

## Invocation

```yaml
metadata:
  request_id: req-9501
  assessment_id: asmt-42
  task_id: task-ftp-probe
  skill_id: ftp-assessment
host: files.example.com
port: 21
tls_mode: explicit_required
credential_ref: cred-ftp-service
anonymous: false
mode: passive
type: ascii
commands:
  - verb: LIST
    args: /
```

## Result

```yaml
outcome: completed
tls_established: true
authenticated: true
transfers:
  - direction: download
    kind: listing
    bytes: 1284
    content_ref: artifact://ftp/req-9501-listing
transcript:
  - command: AUTH TLS
    reply_code: 234
  - command: USER
    reply_code: 331
  - command: PASS
    reply_code: 230
  - command: PASV
    reply_code: 227
  - command: LIST
    reply_code: 226
```

The listing is stored as an artifact; credentials never appear in the transcript.

---

# Example 2 — Required TLS Unavailable

FTPS is required but the server does not support `AUTH TLS`.

## Result

```yaml
outcome: tls_required_unavailable
error:
  category: Security
  code: tls_required_unavailable
  retryable: false
```

The session terminates rather than authenticating in cleartext.

---

# Example 3 — Anonymous Access Reported As Data

An anonymous session is established where explicitly requested.

## Invocation

```yaml
anonymous: true
tls_mode: explicit_optional
```

## Result

```yaml
outcome: completed
authenticated: true
evidence:
  anonymous: true
```

The fact of anonymous access is recorded as data; whether it is a weakness is
determined by domain skills.

---

# Example 4 — Write Blocked

A `STOR` command is attempted while writes are disabled.

## Configuration

```yaml
governance:
  allow_write_operations: false
```

## Result

```yaml
outcome: rejected
error:
  category: Governance
  code: write_blocked
  retryable: false
```

Write operations are treated as intrusive and require authorization.

---

# Example 5 — Active Mode Prohibited

Active mode is attempted while prohibited.

## Result

```yaml
outcome: rejected
error:
  category: Governance
  code: rejected
  retryable: false
```

Passive mode is preferred; active mode requires explicit permission.

---

# Example 6 — Transient Reply Retried

A `421` service-busy reply is retried.

## Flow

```
Attempt 1 → acquire permit → 421 busy

↓ Retry

Attempt 2 → acquire permit → 230 logged in
```

Each attempt acquires its own rate permit.

---

# Example 7 — Evidence Record

A single session produces the following evidence.

```yaml
evidence:
  type: ftp-session
  host: files.example.com:21
  tls_established: true
  anonymous: false
  transcript_codes: [234, 331, 230, 227, 226]
  bytes_transferred: 1284
  duration_ms: 733
  decided_at: 2026-07-25T15:30:00Z
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
