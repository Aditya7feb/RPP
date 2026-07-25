# Evidence Interface

**File:** `skills/shared/evidence/interface.md`

**Version:** 1.0.0

---

# Purpose

The Evidence Interface defines the canonical contract through which platform
components capture, reference, and resolve evidence.

The interface standardizes evidence capture, artifact storage, sealing, and
reference issuance while remaining independent of any backend implementation.

All consumers SHALL capture evidence exclusively through this interface.

---

# Design Principles

The interface SHALL be

- Stable
- Strongly Defined
- Backend Independent
- Versioned
- Observable
- Backward Compatible
- Integrity Preserving

---

# Relationship

```
Master Agent

↓

Workflow

↓

Shared Package or Domain Skill

↓

Evidence Interface

↓

Evidence Shared Skill

↓

Configured Artifact Backends
```

The interface SHALL NOT expose or depend on backend internals.

---

# Interface Overview

```
Capture Request

↓

Artifacts

↓

Execution Context

↓

Capture Result

↓

Reference Request

↓

Resolution Result

↓

Errors
```

---

# Capture Request

Every capture SHALL define

```yaml
type:

inputs:

outputs:

metadata:

scope:

artifacts:
```

`type` SHALL identify the evidence type, such as `http-transaction` or
`tls-handshake`.

`inputs`, `outputs`, and `metadata` SHALL conform to the
[Evidence schema](../../../schemas/evidence.md) and SHALL NOT contain secrets
that cannot be redacted.

`scope` SHALL bound visibility.

`artifacts` SHALL reference payloads to be stored by reference.

---

# Artifacts

Each artifact SHALL define

```yaml
name:

content_type:

content_ref:

size_bytes:
```

Large payloads SHALL be provided by reference rather than inline.

---

# Execution Context

The Evidence Shared Skill SHALL receive read-only context.

```yaml
assessment_id:

task_id:

request_id:

execution_id:

span_id:
```

Correlation identifiers SHALL be recorded with the evidence.

The interface SHALL treat context as read-only.

---

# Capture Result

Every capture SHALL return a normalized result.

```yaml
outcome:

evidence_ref:

integrity:

redaction:
```

`outcome` SHALL be one of

```
captured

rejected

error
```

`evidence_ref` SHALL be a stable reference when `outcome` is `captured`.

`integrity` SHALL include the sealing digest.

`redaction` SHALL record whether redaction occurred and which fields.

Backend-specific objects SHALL NOT be exposed.

---

# Reference Request

Consumers MAY resolve evidence by reference.

```yaml
evidence_ref:

scope:
```

Resolution SHALL succeed only within the evidence scope.

---

# Resolution Result

```yaml
outcome:

evidence:

artifacts:
```

`outcome` SHALL be one of `resolved`, `not_found`, or `out_of_scope`.

`evidence` SHALL conform to the
[Evidence schema](../../../schemas/evidence.md).

---

# Error Contract

Errors SHALL conform to
[the platform error handling model](../../core/error-handling.md) and to
[the Evidence error model](error-model.md).

Integrity verification failure on resolution SHALL produce a canonical integrity
error.

---

# Determinism

Given identical capture input and context, composed evidence fields SHALL be
identical apart from the issued reference and timestamps.

---

# Compatibility

The interface SHALL remain stable across evidence types and backends.

Consumers SHALL require no modification when backends change.

---

# Versioning

The interface SHALL follow semantic versioning.

Minor versions MAY introduce optional fields.

Major versions SHALL indicate breaking changes.

---

# Validation Rules

A compliant capture SHALL define

- Type
- Scope
- Execution Context for correlation
- Non-secret inputs, outputs, and metadata
- Artifacts by reference where large

---

# Quality Requirements

The Evidence Interface SHALL

✓ Remain backend independent

✓ Produce canonical evidence records

✓ Seal integrity

✓ Enforce redaction

✓ Enforce scope

✓ Support structured errors

✓ Remain backward compatible

---

# Future Extensions

Future versions MAY include

- Signed capture attestations
- Batch capture requests
- Chain-of-custody linkage descriptors

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Evidence Interface provides a stable, implementation-independent
contract through which all platform components capture and resolve
integrity-preserving, scope-bounded evidence across the Robust PenTest Platform.
