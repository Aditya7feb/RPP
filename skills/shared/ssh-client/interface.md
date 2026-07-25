# SSH Client Interface

**File:** `skills/shared/ssh-client/interface.md`

**Version:** 1.0.0

---

# Purpose

The SSH Client Interface defines the canonical contract through which platform
components establish SSH sessions and execute authorized operations.

The interface standardizes session requests, host-key trust, authentication,
channel operations, and result propagation while remaining independent of any
transport implementation.

All consumers SHALL perform SSH transport exclusively through this interface.

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

SSH Client Interface

↓

SSH Client Shared Skill

↓

TCP Client + Authentication
```

The interface SHALL NOT expose or depend on adapter internals.

---

# Interface Overview

```
Metadata

↓

Session Target

↓

Host-Key Policy

↓

Authentication

↓

Operations

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

# Host-Key Policy

Every invocation SHALL define

```yaml
trust_policy:

known_host_ref:
```

`trust_policy` SHALL be one of `strict`, `trust_on_first_use`, or `record_only`.

`known_host_ref` SHALL reference the known-host store consulted for verification.

---

# Authentication

Every invocation SHALL define

```yaml
username:

method:

credential_ref:
```

`method` SHALL be one of `password`, `public_key`, `keyboard_interactive`, or
`agent`.

`credential_ref` SHALL reference a credential resolved by the
[Authentication](../authentication/README.md) package.

The interface SHALL NOT accept inline secrets or private keys.

---

# Operations

Every invocation SHALL define

```yaml
operations:
```

`operations` SHALL be an ordered sequence, each declaring one of

```
exec

shell

subsystem

forward
```

`exec` operations SHALL declare a command and be authorized as intrusive.

`forward` operations SHALL declare direction and endpoints and be permitted by
governance.

The interface SHALL treat command content opaquely and bound output.

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

The SSH Client Shared Skill SHALL receive read-only context.

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

algorithms:

host_key:

authenticated:

operation_results:

error:

evidence:
```

`outcome` SHALL be one of

```
completed

host_key_rejected

auth_failed

rejected

timed_out
```

`host_key` SHALL include the fingerprint and trust decision.

`operation_results` SHALL summarize each operation, referencing bounded output
as artifacts.

Adapter-specific session objects SHALL NOT be exposed.

---

# Evidence

The interface SHALL expose structured evidence.

Evidence MAY include

- Negotiated algorithms
- Host-key fingerprint and trust decision
- Authentication method and outcome
- Operations and bounded output references

Evidence SHALL conform to the canonical
[Evidence schema](../../../schemas/evidence.md) and SHALL NOT contain credentials,
private keys, or unauthorized output.

---

# Error Contract

Errors SHALL conform to
[the platform error handling model](../../core/error-handling.md) and to
[the SSH Client error model](error-model.md).

A rejected host key SHALL map to a non-retryable error under `strict` policy.

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
- Host-Key Policy
- Authentication
- Operations
- Execution Context
- Session Result
- Error Handling
- Evidence

---

# Quality Requirements

The SSH Client Interface SHALL

✓ Remain transport independent

✓ Produce normalized results

✓ Enforce host-key trust

✓ Support structured errors

✓ Preserve evidence

✓ Protect credentials and keys

✓ Remain backward compatible

---

# Future Extensions

Future versions MAY include

- Certificate-based authentication descriptors
- Multiplexed session handles
- Structured SFTP operation results

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant SSH Client Interface provides a stable, implementation-independent
contract through which all platform components establish bounded, governed SSH
sessions across the Robust PenTest Platform.
