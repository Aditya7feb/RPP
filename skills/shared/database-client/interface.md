# Database Client Interface

**File:** `skills/shared/database-client/interface.md`

**Version:** 1.0.0

---

# Purpose

The Database Client Interface defines the canonical contract through which
platform components execute parameterized database operations.

The interface standardizes connection requests, parameterized statements,
transactions, result handling, and result propagation while remaining
independent of any engine implementation.

All consumers SHALL perform database access exclusively through this interface.

---

# Design Principles

The interface SHALL be

- Stable
- Strongly Defined
- Engine Independent
- Versioned
- Observable
- Backward Compatible
- Parameterization-First

---

# Relationship

```
Master Agent

↓

Domain Skill

↓

Database Client Interface

↓

Database Client Shared Skill

↓

TCP Client + TLS Client + Authentication
```

The interface SHALL NOT expose or depend on engine internals.

---

# Interface Overview

```
Metadata

↓

Connection Target

↓

Security

↓

Authentication

↓

Statement Program

↓

Governance References

↓

Execution Context

↓

Operation Result

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

# Connection Target

Every invocation SHALL define

```yaml
engine:

host:

port:

database:
```

`engine` SHALL identify the database engine family by canonical name.

`port` SHALL be an integer from `1` through `65535`.

---

# Security

Every invocation SHALL define

```yaml
tls_mode:
```

`tls_mode` SHALL be one of

```
disabled

preferred

required
```

`required` SHALL guarantee encryption; `disabled` and `preferred` MAY proceed in
cleartext where encryption is unavailable.

---

# Authentication

Every invocation MAY define

```yaml
credential_ref:
```

`credential_ref` SHALL reference a credential resolved by the
[Authentication](../authentication/README.md) package.

The interface SHALL NOT accept inline secrets.

---

# Statement Program

Every invocation SHALL define

```yaml
transaction:

statements:
```

`transaction` SHALL declare whether the statements run within an explicit
transaction and its isolation intent.

Each statement SHALL define

```yaml
text:

parameters:

kind:
```

`text` SHALL be the parameterized statement text with placeholders.

`parameters` SHALL be an ordered or named set of bound values supplied
separately from `text`. Values SHALL NOT be interpolated into `text`.

`kind` SHALL be one of `read` or `write`. `write` statements SHALL be authorized
as intrusive.

The interface SHALL treat statement text as caller-provided and SHALL NOT modify
it.

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

The Database Client Shared Skill SHALL receive read-only context.

```yaml
execution_id:

parent_span:

variables:
```

The interface SHALL treat context as read-only.

---

# Operation Result

Every invocation SHALL return a normalized result.

```yaml
outcome:

tls_established:

statement_results:

transaction_outcome:

error:

evidence:
```

`outcome` SHALL be one of

```
completed

encryption_required_unavailable

auth_failed

rejected

timed_out
```

Each statement result SHALL include row count, affected count, and a bounded
result-set reference for reads.

Engine-specific result objects SHALL NOT be exposed.

---

# Evidence

The interface SHALL expose structured evidence.

Evidence MAY include

- Engine and target
- Transport-encryption outcome
- Statement kinds and parameter counts, excluding values
- Row and byte counts
- Transaction outcome

Evidence SHALL conform to the canonical
[Evidence schema](../../../schemas/evidence.md) and SHALL NOT contain credentials
or parameter values.

---

# Error Contract

Errors SHALL conform to
[the platform error handling model](../../core/error-handling.md) and to
[the Database Client error model](error-model.md).

Engine error codes SHALL be preserved in mapped errors for domain interpretation.

---

# Compatibility

The interface SHALL remain stable across engines and consumers.

Consumers SHALL require no modification when engines change.

---

# Versioning

The interface SHALL follow semantic versioning.

Minor versions MAY introduce optional fields.

Major versions SHALL indicate breaking changes.

---

# Validation Rules

A compliant invocation SHALL define

- Metadata
- Connection Target with a valid port
- Security mode
- Statement Program with parameterized statements
- Execution Context
- Operation Result
- Error Handling
- Evidence

Values SHALL be supplied as parameters, never interpolated into statement text.

---

# Quality Requirements

The Database Client Interface SHALL

✓ Remain engine independent

✓ Enforce parameterization

✓ Require encryption where mandated

✓ Support structured errors

✓ Preserve evidence

✓ Protect credentials and values

✓ Remain backward compatible

---

# Future Extensions

Future versions MAY include

- Prepared-statement handles
- Streaming cursor descriptors
- Batch statement programs

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Database Client Interface provides a stable, implementation-independent
contract through which all platform components perform bounded, parameterized,
governed database operations across the Robust PenTest Platform.
