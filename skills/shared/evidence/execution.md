# Evidence Execution Model

**File:** `skills/shared/evidence/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the execution model for the Evidence Shared Skill.

The execution model describes how the shared skill processes a capture request
from composition through artifact storage, redaction, sealing, persistence, and
reference issuance, and how it resolves evidence by reference.

The model is deterministic in composition given the same request and context.

---

# Capture Execution Overview

```
Receive Capture Request

↓

Resolve Configuration

↓

Compose Evidence Record

↓

Store Artifacts

↓

Apply Redaction

↓

Seal Integrity

↓

Persist Evidence

↓

Issue Reference

↓

Emit Events

↓

Return Capture Result
```

---

# Stage 1 — Configuration Resolution

The Evidence Shared Skill SHALL resolve backends, integrity, redaction, scope,
and retention using the precedence defined in [configuration.md](configuration.md).

Integrity sealing and redaction SHALL always be enforced.

---

# Stage 2 — Composition

The Evidence Shared Skill SHALL compose a canonical
[Evidence](../../../schemas/evidence.md) record from the request and context,
recording correlation identifiers.

---

# Stage 3 — Artifact Storage

Referenced payloads SHALL be stored in a configured backend, bounded by
`max_artifact_bytes`.

Each stored artifact SHALL yield a stable reference resolvable within scope.

---

# Stage 4 — Redaction

The Evidence Shared Skill SHALL redact secret material from inputs, outputs,
artifacts, and metadata before sealing.

Redacted fields SHALL be recorded. Secrets SHALL never be persisted.

Redaction SHALL precede sealing.

---

# Stage 5 — Integrity Sealing

The Evidence Shared Skill SHALL compute a content digest over the redacted record
and its artifact references, producing integrity metadata.

Once sealed, the evidence SHALL be immutable.

---

# Stage 6 — Persistence

The sealed evidence SHALL be persisted to a configured backend.

Persistence failure SHALL be classified according to
[error-model.md](error-model.md) and SHALL NOT yield a partial reference.

---

# Stage 7 — Reference Issuance

The Evidence Shared Skill SHALL issue a stable `evidence_ref` that other packages
use to correlate findings, logs, and reports.

---

# Resolution Execution Overview

```
Receive Reference Request

↓

Enforce Scope

↓

Load Evidence

↓

Verify Integrity

↓

Resolve Artifacts

↓

Return Resolution Result
```

---

# Resolution Stages

The Evidence Shared Skill SHALL

- Reject references outside the resolved scope with `out_of_scope`
- Return `not_found` when no evidence matches
- Verify the integrity seal before returning evidence
- Resolve artifact references within scope

Integrity verification failure SHALL produce a canonical integrity error and
SHALL NOT return the evidence as valid.

---

# Determinism

Given identical capture input and context, composed evidence fields SHALL be
identical apart from the issued reference and timestamps.

The integrity digest SHALL be reproducible from the redacted record.

---

# Concurrency

The Evidence Shared Skill SHALL support concurrent captures.

Sealed evidence SHALL never be modified concurrently; corrections SHALL create
new linked records.

---

# Interaction With Other Shared Skills

- The [Logging](../logging/README.md) shared package SHOULD link events to
  evidence through `evidence_ref`.
- The [Reporting](../reporting/README.md) shared package SHALL reference evidence
  when composing reports.
- Domain skills SHALL reference evidence from [Findings](../../../schemas/finding.md).

---

# Failure Handling

Execution failures SHALL be classified according to
[error-model.md](error-model.md).

A failed capture SHALL NOT issue a reference.

A failed artifact store SHALL fail the capture rather than persist evidence with
dangling references.

---

# Execution Outputs

The execution model SHALL produce

- A sealed evidence record
- Artifact references
- A stable evidence reference
- Evidence metrics

Outputs SHALL remain implementation independent.

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Error Model](error-model.md)
- [Evidence Schema](../../../schemas/evidence.md)
- [Execution Model](../../core/execution-model.md)
