# SMTP Client Interface

**File:** `skills/shared/smtp-client/interface.md`

**Version:** 1.0.0

---

# Purpose

The SMTP Client Interface defines the canonical contract through which platform
components conduct SMTP conversations.

The interface standardizes session requests, capability negotiation, TLS upgrade,
authentication, command exchange, and result propagation while remaining
independent of any transport implementation.

All consumers SHALL perform SMTP transport exclusively through this interface.

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

SMTP Client Interface

↓

SMTP Client Shared Skill

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

ehlo_name:
```

`port` SHALL be an integer from `1` through `65535`.

`ehlo_name` SHALL be the domain presented in `EHLO`.

---

# Security

Every invocation SHALL define

```yaml
tls_mode:
```

`tls_mode` SHALL be one of

```
none

starttls_optional

starttls_required

implicit
```

`starttls_required` and `implicit` SHALL guarantee confidentiality; `none` and
`starttls_optional` MAY proceed in cleartext where TLS is unavailable.

---

# Authentication

Every invocation MAY define

```yaml
credential_ref:

mechanism:
```

`credential_ref` SHALL reference a credential resolved by the
[Authentication](../authentication/README.md) package.

The interface SHALL NOT accept inline secrets.

---

# Command Program

Every invocation SHALL define

```yaml
commands:
```

`commands` SHALL be an ordered sequence of SMTP commands to issue, each declaring
the verb and bounded arguments.

Message bodies, where present, SHALL be provided by reference and bounded by
configured size limits.

The interface SHALL treat message content opaquely.

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

The SMTP Client Shared Skill SHALL receive read-only context.

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

capabilities:

tls_established:

authenticated:

transcript:

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

`transcript` SHALL be an ordered sequence of issued commands and reply codes,
excluding credentials and unauthorized message bodies.

Adapter-specific session objects SHALL NOT be exposed.

---

# Evidence

The interface SHALL expose structured evidence.

Evidence MAY include

- Greeting and capabilities
- TLS upgrade outcome
- Command and reply-code transcript
- Session duration

Evidence SHALL conform to the canonical
[Evidence schema](../../../schemas/evidence.md) and SHALL NOT contain credentials.

---

# Error Contract

Errors SHALL conform to
[the platform error handling model](../../core/error-handling.md) and to
[the SMTP Client error model](error-model.md).

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
- Command Program
- Execution Context
- Session Result
- Error Handling
- Evidence

---

# Quality Requirements

The SMTP Client Interface SHALL

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

- Delivery-status notification handling
- Pipelining directives
- Internationalized address support

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant SMTP Client Interface provides a stable, implementation-independent
contract through which all platform components conduct bounded, governed SMTP
conversations across the Robust PenTest Platform.
