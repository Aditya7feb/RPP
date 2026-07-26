# Master Agent Error Model

**File:** `agents/master/error-model.md`

**Version:** 1.0.0

---

# Purpose

This document defines the canonical orchestration error categories the Master
Agent recognizes and how each maps to an outcome. These are **orchestration**
errors — failures in coordinating work. Capability-internal errors are owned and
classified by the capability tiers and surface to the Master Agent only through
the [agent-response](../../schemas/agent-response.md) `status`.

---

# Error Categories

| Category | Meaning | Outcome |
|----------|---------|---------|
| `input-invalid` | Assessment, scope, or RoE failed validation | Stop before planning |
| `delegation-timeout` | Specialist tier agent did not respond in time | Retry per policy, else fail task |
| `agent-unavailable` | No specialist agent owns the required capability | Skip with recorded gap |
| `agent-failure` | Specialist agent returned `failed` | Retry per policy, else continue independent work |
| `agent-rejected` | Specialist agent returned `rejected` (out of scope/unsupported) | Do not retry; record |
| `dependency-unmet` | A required prior task did not complete | Defer or drop dependent work |
| `scope-violation` | A task would exceed scope or RoE | Do not dispatch; record |
| `approval-denied` | Required approval was rejected or expired | Stop at identification for that candidate |
| `resource-exhausted` | Transient infrastructure exhaustion | Retry per policy |

---

# Outcome Mapping

- **Stop** — Orchestration halts for this scope of work and preserves
  [execution-state](../../schemas/execution-state.md). Applies to
  `input-invalid`, `scope-violation`, and `approval-denied`.
- **Retry** — Re-dispatch the [task](../../schemas/task.md) under
  [retry-policy](../../schemas/retry-policy.md). Applies to
  `delegation-timeout`, `agent-failure`, and `resource-exhausted`.
- **Continue** — Proceed with independent, unaffected work. Applies to
  `agent-unavailable`, `agent-rejected`, and `dependency-unmet`.

---

# Retry Boundaries

The Master Agent SHALL retry only transient orchestration faults
(`delegation-timeout`, `agent-failure`, `resource-exhausted`). It SHALL NOT
retry `scope-violation`, `approval-denied`, or `agent-rejected`. See
[configuration.md](configuration.md) for retry configuration.

---

# Failure Handling

On any non-recoverable failure the Master Agent SHALL:

- Record the failure and its category in
  [execution-state](../../schemas/execution-state.md).
- Continue independent, unaffected work.
- Preserve all referenced Findings and Evidence unchanged.
- Ensure the reporting pipeline is informed of coverage gaps by reference.

The Master Agent SHALL NEVER discard, mutate, or synthesize Findings or Evidence
in response to an error; those objects are owned by their tiers.

---

# Terminal States

An assessment reaches `FAILED` only when no runnable work remains and mandatory
phases could not complete. It reaches `CANCELLED` on explicit human
cancellation. Both preserve execution state for reporting.
