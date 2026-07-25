# Virtual Host Discovery Execution Model

**File:** `skills/discovery/virtual-host-discovery/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the execution model for the Virtual Host Discovery Skill.

The execution model describes how the skill discovers virtual hosts on an address
and produces canonical Assets, Observations, Evidence, Findings, and Risk, gated
by the Policy Engine.

The model is deterministic given the same inputs and responses.

---

# Execution Overview

```
Receive Target Address

↓

Resolve Configuration

↓

Consult Policy Engine

↓

Establish Baseline Response (HTTP Client)

↓

For Each Candidate Host Name:

  ├── Consult Policy Engine
  ├── Probe With Host Header (HTTP Client)
  ├── Compare To Baseline
  └── Record Observation → Evidence

↓

Build Virtual Host Assets

↓

Analyze For Hidden-Host Exposure

↓

Emit Findings and Risk

↓

Emit Events

↓

Return Result
```

---

# Stage 1 — Configuration Resolution

The skill SHALL resolve candidates, differential thresholds, bounds, and analysis
toggles using the precedence defined in [configuration.md](configuration.md).

---

# Stage 2 — Policy Gating

Before every probe, the skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) with the address, the
`discovery` action class, and `active` intrusiveness.

- `deny` → the probe SHALL be skipped and recorded
- `requires_approval` → the probe SHALL be routed to approval and deferred
- `allow` → the probe SHALL proceed within the attached rate ceiling

Out-of-scope addresses or candidate host names SHALL never be probed.

---

# Stage 3 — Baseline Establishment

The skill SHALL establish a baseline response for the target address using a
non-matching host name, so that distinct virtual hosts can be identified by
difference.

---

# Stage 4 — Candidate Probing

The skill SHALL probe candidate host names against the address through the
[HTTP Client](../../shared/http-client/README.md), bounded by `max_candidates`,
`max_concurrency`, and `per_request_timeout`.

The skill SHALL NOT perform HTTP input or output directly.

---

# Stage 5 — Differential Analysis

The skill SHALL compare each candidate response to the baseline using the
configured `similarity_threshold`.

Where `detect_wildcard` is enabled, wildcard responses SHALL be detected and
discounted to reduce false positives.

A candidate whose response differs materially from the baseline SHALL be
considered a distinct virtual host.

---

# Stage 6 — Observation And Evidence

For each probe, the skill SHALL record an
[Observation](../../../schemas/observation.md) and promote corroborated
observations to [Evidence](../../../schemas/evidence.md).

---

# Stage 7 — Asset And Relationship Construction

For distinct virtual hosts, the skill SHALL build canonical `web-application`
[Assets](../../../schemas/asset.md) and `serves`
[Asset Relationships](../../../schemas/asset-relationship.md) to the address,
deduplicating by `canonical_key`.

Each Asset SHALL carry `scope_status` and provenance to its Evidence.

---

# Stage 8 — Weakness Analysis

Where enabled, the skill SHALL analyze discovered virtual hosts for hidden or
internal hosts reachable publicly.

---

# Stage 9 — Finding And Risk Emission

For each confirmed exposure, the skill SHALL emit a
[Finding](../../../schemas/finding.md) referencing its Evidence and a
[Risk](../../../schemas/risk.md) scoring it.

A Finding SHALL NOT be emitted without supporting Evidence.

---

# Stage 10 — Events

The skill SHOULD emit lifecycle events to the Execution State.

---

# Determinism

Given identical inputs and responses, the skill SHALL produce identical Assets and
Findings apart from timestamps and identifiers.

---

# Interaction With Other Components

- The [Policy Engine](../../shared/policy-engine/README.md) authorizes every probe.
- The [HTTP Client](../../shared/http-client/README.md) performs transport.
- The [Evidence](../../shared/evidence/README.md) package stores evidence.
- Content Discovery and Fingerprinting consume discovered virtual hosts.

---

# Failure Handling

Execution failures SHALL be classified according to
[error-model.md](error-model.md).

A denial or failure for one candidate SHALL NOT abort probing of others; the
outcome SHALL be `partial` where some probes did not complete.

---

# Execution Outputs

The execution model SHALL produce

- Virtual host `web-application` Assets and `serves` relationships
- Observations and Evidence references
- Findings with Risk where hidden-host exposure is confirmed

Outputs SHALL remain implementation independent.

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Error Model](error-model.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [HTTP Client](../../shared/http-client/README.md)
- [Execution Model](../../core/execution-model.md)
