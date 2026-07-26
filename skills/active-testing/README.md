# Active Testing Capability Tier

**File:** `skills/active-testing/README.md`

**Version:** 1.0.0

---

# Purpose

The Active Testing tier provides reusable, implementation-independent security capabilities
that generate inputs, exercise targets, and capture execution signals within the Robust
PenTest Platform (RPP).

Active Testing capabilities are **capabilities, not domain skills**: they generate and deliver
inputs and record what happened, but they never interpret results, produce Findings, or classify
Risk. Domain Security capabilities consume their outputs and perform interpretation.

This tier comprises the following capabilities.

- [Wordlists](wordlists/README.md)
- [Mutation Engine](mutation-engine/README.md)
- [Payload Generation](payload-generation/README.md)
- [Parameter Mining](parameter-mining/README.md)
- [Fuzzing](fuzzing/README.md)
- [Replay](replay/README.md)
- [Traffic Recording](traffic-recording/README.md)
- [Traffic Comparison](traffic-comparison/README.md)

---

# Safety Model

The Active Testing tier SHALL enforce a single, tier-wide safety model.

- **Non-destructive by default.** Every capability SHALL default to non-destructive execution.
  Payloads and operations that cannot alter or damage target state require no additional
  approval beyond ordinary policy gating.
- **Destructive execution requires approval.** Any operation that could alter or damage target
  state SHALL be gated by the [Policy Engine](../shared/policy-engine/README.md) and SHALL proceed
  only on an explicit approval decision.
- **Approval requirements propagate.** The
  [Payload](../../schemas/payload.md) `safety.requires_approval` marker set during generation and
  mutation SHALL propagate through payload generation into execution. Delivery capabilities
  (Fuzzing, Replay, Parameter Mining) SHALL honor that marker by deferring delivery to the Policy
  Engine rather than executing autonomously.
- **Bounded execution.** All target-facing execution SHALL be bounded in volume and rate and
  SHALL never constitute denial of service.

No Active Testing capability SHALL bypass the Policy Engine for target-facing execution.

---

# Lifecycle Ownership

The Active Testing tier participates in the canonical pipeline
`Observation → Evidence → Finding → Risk` as a producer of inputs and execution signals only.
Ownership is divided as follows.

- **Active Testing produces Payloads.** Payload generation, mutation, and the payload lifecycle
  originate in this tier.
- **Active Testing produces execution Observations.** Response-code changes, length changes,
  reflected input, timing differences, protocol errors, accepted parameters, and replay
  mismatches are execution Observations, not vulnerability Findings. Active Testing remains their
  producer.
- **Active Testing produces Artifacts.** Recorded traffic, corpora, replay logs, and difference
  outputs are emitted as [Artifacts](../../schemas/artifact.md) by reference.
- **The Evidence tier owns the Artifact lifecycle.** Archival, integrity, retention, redaction,
  packaging, and promotion of artifacts into durable Evidence are owned by the Evidence tier, not
  by Active Testing. Active Testing emits artifacts; it does not manage their durable lifecycle.
- **Domain Security capabilities own interpretation.** They consume execution Observations and
  Evidence, confirm vulnerabilities, and produce Findings and Risk. Active Testing produces no
  Findings and classifies no Risk.

The shared [Evidence](../shared/evidence/README.md) package provides common evidence primitives
and references consumed across tiers; it is distinct from the Evidence tier that will own
persistence, archival, integrity, retention, packaging, and promotion.

---

# Payload Lifecycle

The payload lifecycle represents **execution history** within the Active Testing tier and ends
at `successful`. It has three states.

| State | Owner | Meaning |
|-------|-------|---------|
| Generated | Active Testing | A candidate payload created by payload generation or mutation. |
| Executed | Active Testing | A generated payload delivered to a target. |
| Successful | Active Testing | An executed payload that produced an interesting execution Observation. |

The payload lifecycle SHALL NOT include a `validation` state. Validation is a Finding concern,
not a payload lifecycle concern.

---

# Validation Payloads

A Validation Payload is **not a new payload and not a payload state**. It is an existing
successful [Payload](../../schemas/payload.md) that a Domain Security capability selects as the
minimal reproducible proof for a Finding and references from the Finding's Validation section.
The payload's state does not change; only its role changes through association with the Finding.

Domain Security capabilities SHALL reference payload, execution, Observation, and Evidence
identifiers rather than duplicating corpora or large requests. Active Testing SHALL NOT attach
its generated corpus to Findings.

---

# Responsibilities

| Tier | Owns |
|------|------|
| Active Testing | payload generation, payload mutation, payload execution, replay, fuzzing, execution Observations |
| Domain Security | interpretation, vulnerability confirmation, selection of successful executions, promotion of successful executions into Validation Payloads, Findings, Risk |
| Evidence | request and response archival, HAR, screenshots, traces, certificates, logs, binary artifacts, integrity, retention, evidence lifecycle |
| Reporting | consumption of Findings |

---

# Canonical Schemas

- [Payload](../../schemas/payload.md)
- [Artifact](../../schemas/artifact.md)
- [Metrics](../../schemas/metrics.md)
- [Observation](../../schemas/observation.md)

---

# Related

- [Shared Infrastructure](../shared/README.md)
- [Policy Engine](../shared/policy-engine/README.md)
- [Evidence](../shared/evidence/README.md)

---

# Success Criteria

The Active Testing tier is compliant when its capabilities generate and execute inputs and
capture execution signals under a non-destructive, policy-gated safety model, emit Payloads,
execution Observations, Artifacts, and Metrics, and produce no Findings or Risk, leaving
interpretation, Validation Payload selection, and Finding production to Domain Security
capabilities and durable artifact lifecycle to the Evidence tier.
