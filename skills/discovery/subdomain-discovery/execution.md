# Subdomain Discovery Execution Model

**File:** `skills/discovery/subdomain-discovery/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the execution model for the Subdomain Discovery Skill.

The execution model describes how the skill discovers subdomains for an apex
domain and produces canonical Assets, Observations, Evidence, Findings, and Risk,
gated by the Policy Engine for active resolution.

The model is deterministic given the same inputs and sources.

---

# Execution Overview

```
Receive Apex Domain

↓

Resolve Configuration

↓

Collect Passive Candidates

↓

Generate Bounded Active Candidates

↓

For Each Candidate Requiring Resolution:

  ├── Consult Policy Engine (active resolution)
  │     ├── deny → record suspected, skip resolution
  │     ├── requires_approval → route and defer
  │     └── allow → resolve (DNS Client)
  └── Record Observation → Evidence

↓

Build Subdomain Assets and Relationships

↓

Analyze For Takeover Exposure

↓

Emit Findings and Risk

↓

Emit Events

↓

Return Result
```

---

# Stage 1 — Configuration Resolution

The skill SHALL resolve sources, bounds, and analysis toggles using the precedence
defined in [configuration.md](configuration.md).

---

# Stage 2 — Passive Collection

The skill SHALL collect subdomain candidates from configured passive sources.

Passive candidates that are not actively resolved SHALL be recorded as `subdomain`
Assets in the `suspected` state.

---

# Stage 3 — Candidate Generation

The skill SHALL generate bounded active candidates from the wordlist within
`max_candidates`.

Candidates outside the apex domain SHALL NOT be generated.

---

# Stage 4 — Policy Gating For Resolution

Before every active resolution, the skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) with the candidate, the
`discovery` action class, and `active` intrusiveness.

- `deny` → the candidate SHALL be recorded as `suspected` without resolution
- `requires_approval` → resolution SHALL be routed to approval and deferred
- `allow` → resolution SHALL proceed within the attached rate ceiling

Out-of-scope candidates SHALL be recorded without active probing.

---

# Stage 5 — Resolution

The skill SHALL resolve candidates through the
[DNS Client](../../shared/dns-client/README.md), bounded by `max_concurrency` and
`per_resolution_timeout`.

The skill SHALL NOT perform DNS input or output directly.

---

# Stage 6 — Observation And Evidence

For each candidate, the skill SHALL record an
[Observation](../../../schemas/observation.md) and promote corroborated
observations to [Evidence](../../../schemas/evidence.md).

---

# Stage 7 — Asset And Relationship Construction

Resolved candidates SHALL be recorded as `confirmed` `subdomain`
[Assets](../../../schemas/asset.md) with `resolves-to`
[Asset Relationships](../../../schemas/asset-relationship.md), deduplicating by
`canonical_key`.

Each Asset SHALL carry `scope_status` and provenance to its Evidence.

---

# Stage 8 — Takeover Analysis

Where enabled, the skill SHALL analyze resolution results for subdomain-takeover
potential from dangling delegations and CNAMEs to unclaimed resources.

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

Given identical inputs and sources, the skill SHALL produce identical Assets and
Findings apart from timestamps and identifiers.

DNS resolution outcomes remain influenced by external state and are reflected in
Asset state.

---

# Interaction With Other Components

- The [Policy Engine](../../shared/policy-engine/README.md) authorizes active
  resolution.
- The [DNS Client](../../shared/dns-client/README.md) performs resolution.
- The [Evidence](../../shared/evidence/README.md) package stores evidence.
- DNS Enumeration and Port Discovery consume confirmed subdomains.

---

# Failure Handling

Execution failures SHALL be classified according to
[error-model.md](error-model.md).

A denial or resolution failure for one candidate SHALL NOT abort the discovery;
the outcome SHALL be `partial` where some candidates were not resolved.

---

# Execution Outputs

The execution model SHALL produce

- Suspected and confirmed subdomain Assets
- `resolves-to` relationships
- Observations and Evidence references
- Findings with Risk where takeover exposure is confirmed

Outputs SHALL remain implementation independent.

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Error Model](error-model.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [DNS Client](../../shared/dns-client/README.md)
- [Execution Model](../../core/execution-model.md)
