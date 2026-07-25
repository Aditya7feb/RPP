# FTP Client Interface

**File:** `skills/shared/ftp-client/interface.md`

**Version:** 1.0.0

---

# Purpose

The FTP Client Interface defines the canonical contract through which platform
components conduct FTP conversations.

The interface standardizes session requests, data-channel coordination, TLS
upgrade, authentication, command exchange, and result propagation while
remaining independent of any transport implementation.

All consumers SHALL perform FTP transport exclusively through this interface.

---

# Design Principles

The interface SHALL be

- Stable
- Strongly Defined
- Transport Independent
- Versioned
- Observable
- Backward Compatible
- Bounded

---

# Relationship

```
Master Agent

↓

Domain Skill

↓

FTP Client Interface

↓

FTP Client Shared Skill

↓

TCP Client + TLS Client + Authentication
```

The interface SHALL NOT expose or depend on adapter internals.

---

# Interface Overview

```
Metadata

↓

Session Target

↓

Security

↓

Authentication

↓

Transfer Mode

↓

Command Program

↓

Governance References

↓

Execution Context

↓

Session Result

↓

Evidence

↓

Errors
```

---

# Metadata

Every invocation SHALL include

```yaml
request_id:

assessment_id:

task_id:

skill_id:

timestamp:
```

Metadata enables tracing and auditing.

---

# Session Target

Every invocation SHALL define

```yaml
host:

port:
```

`port` SHALL be an integer from `1` through `65535`.

---

# Security

Every invocation SHALL define

```yaml
tls_mode:
```

`tls_mode` SHALL be one of

```
none

explicit_optional

explicit_required
```

`explicit_required` SHALL guarantee confidentiality; `none` and
`explicit_optional` MAY proceed in cleartext where TLS is unavailable.

---

# Authentication

Every invocation SHALL define

```yaml
credential_ref:

anonymous:
```

`credential_ref` SHALL reference a credential resolved by the
[Authentication](../authentication/README.md) package when `anonymous` is
`false`.

`anonymous` SHALL declare anonymous authentication.

The interface SHALL NOT accept inline secrets.

---

# Transfer Mode

Every invocation SHALL define

```yaml
mode:

type:
```

`mode` SHALL be one of `passive` or `active`.

`type` SHALL be one of `ascii` or `binary`.

---

# Command Program

Every invocation SHALL define

```yaml
commands:
```

`commands` SHALL be an ordered sequence of FTP operations, each declaring the
verb and bounded arguments.

Uploaded content SHALL be provided by reference and bounded by configured size
limits.

The interface SHALL treat file content opaquely.

---

# Governance References

Every invocation MAY reference

```yaml
rate_limit_policy_id:

retry_policy_id:

proxy_id:
```

Referenced policies SHALL conform to their canonical schemas. Absent references
SHALL inherit configured defaults.

---

# Execution Context

The FTP Client Shared Skill SHALL receive read-only context.

```yaml
execution_id:

parent_span:

variables:
```

The interface SHALL treat context as read-only.

---

# Session Result

Every invocation SHALL return a normalized result.

```yaml
outcome:

tls_established:

authenticated:

transcript:

transfers:

error:

evidence:
```

`outcome` SHALL be one of

```
completed

tls_required_unavailable

auth_failed

rejected

timed_out
```

`transcript` SHALL be an ordered sequence of commands and reply codes, excluding
credentials.

`transfers` SHALL summarize data transfers by size and direction, referencing
transferred content as artifacts.

Adapter-specific session objects SHALL NOT be exposed.

---

# Evidence

The interface SHALL expose structured evidence.

Evidence MAY include

- Greeting and features
- TLS upgrade outcome
- Command and reply-code transcript
- Transfer summaries

Evidence SHALL conform to the canonical
[Evidence schema](../../../schemas/evidence.md) and SHALL NOT contain credentials.

---

# Error Contract

Errors SHALL conform to
[the platform error handling model](../../core/error-handling.md) and to
[the FTP Client error model](error-model.md).

A `5xx` reply SHALL map to a non-retryable error; a `4xx` reply MAY map to a
retryable error.

---

# Compatibility

The interface SHALL remain stable across transport adapters and consumers.

Consumers SHALL require no modification when adapters change.

---

# Versioning

The interface SHALL follow semantic versioning.

Minor versions MAY introduce optional fields.

Major versions SHALL indicate breaking changes.

---

# Validation Rules

A compliant invocation SHALL define

- Metadata
- Session Target with a valid port
- Security mode
- Authentication declaration
- Transfer Mode
- Command Program
- Execution Context
- Session Result
- Error Handling
- Evidence

---

# Quality Requirements

The FTP Client Interface SHALL

✓ Remain transport independent

✓ Produce normalized results

✓ Enforce confidentiality where required

✓ Support structured errors

✓ Preserve evidence

✓ Protect credentials

✓ Remain backward compatible

---

# Future Extensions

Future versions MAY include

- Structured MLSD listings
- Resume and range transfers
- Implicit FTPS profiles

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant FTP Client Interface provides a stable, implementation-independent
contract through which all platform components conduct bounded, governed FTP
conversations across the Robust PenTest Platform.
