# Reporting Execution Model

**File:** `skills/shared/reporting/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the execution model for the Reporting Shared Skill.

The execution model describes how the shared skill processes a compose request
from aggregation through deduplication, correlation, ordering, evidence
bundling, composition, and rendering.

The model is deterministic given the same inputs.

---

# Execution Overview

```
Receive Compose Request

↓

Resolve Configuration

↓

Aggregate Findings

↓

Deduplicate

↓

Correlate

↓

Order

↓

Bundle Evidence

↓

Compose Canonical Report

↓

Render Outputs

↓

Emit Events

↓

Return Report Result
```

---

# Stage 1 — Configuration Resolution

The Reporting Shared Skill SHALL resolve composition, ordering, evidence, and
renderer settings using the precedence defined in [configuration.md](configuration.md).

Redaction preservation SHALL always be enforced.

---

# Stage 2 — Aggregation

The Reporting Shared Skill SHALL aggregate the referenced
[Findings](../../../schemas/finding.md), preserving provenance.

Invalid or malformed findings SHALL be rejected according to
[error-model.md](error-model.md).

---

# Stage 3 — Deduplication

Where enabled, the Reporting Shared Skill SHALL merge findings describing the
same issue at the same location.

Merged findings SHALL retain the highest severity and confidence and SHALL merge
evidence references.

---

# Stage 4 — Correlation

Where enabled, the Reporting Shared Skill SHALL group related findings into
correlations without altering individual validity.

---

# Stage 5 — Ordering

The Reporting Shared Skill SHALL order findings using the configured `order_by`
and a stable `tie_breaker`, ensuring deterministic output.

---

# Stage 6 — Evidence Bundling

Where evidence is included, the Reporting Shared Skill SHALL bundle referenced
evidence through the [Evidence](../evidence/README.md) shared package.

Bundling SHALL preserve integrity and redaction and SHALL reference rather than
duplicate evidence.

Evidence outside `bundle_scope` SHALL NOT be bundled.

---

# Stage 7 — Composition

The Reporting Shared Skill SHALL compose a canonical
[Report](../../../schemas/report.md) containing summary, ordered findings,
correlations, and evidence references.

The canonical report SHALL be format independent.

---

# Stage 8 — Rendering

The Reporting Shared Skill SHALL render the canonical report into each requested
format through adapters.

A renderer failure SHALL NOT discard the canonical report; the outcome SHALL be
`partial`.

Rendered output SHALL never expose redacted material.

---

# Stage 9 — Events

The Reporting Shared Skill SHOULD emit lifecycle events according to
configuration.

---

# Determinism

Given identical findings, options, and evidence, the composed canonical report
SHALL be identical apart from timestamps and references.

Stable tie-breaking SHALL ensure identical ordering across runs.

---

# Concurrency

The Reporting Shared Skill MAY render multiple formats concurrently.

Concurrent rendering SHALL NOT alter the canonical report model.

---

# Interaction With Other Shared Skills

- The [Evidence](../evidence/README.md) shared package SHALL provide bundled
  evidence and enforce integrity and redaction.
- The [Logging](../logging/README.md) shared package SHOULD record composition
  lifecycle events.

---

# Failure Handling

Execution failures SHALL be classified according to
[error-model.md](error-model.md).

Aggregation and composition failures SHALL fail the request.

Renderer failures SHALL degrade to a `partial` outcome, preserving the canonical
report.

---

# Execution Outputs

The execution model SHALL produce

- A canonical report model
- Rendered outputs by format
- An evidence bundle by reference
- Reporting metrics

Outputs SHALL remain implementation independent at the model layer.

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Error Model](error-model.md)
- [Report Schema](../../../schemas/report.md)
- [Execution Model](../../core/execution-model.md)
