# Parameter Mining Capability

**File:** `skills/active-testing/parameter-mining/README.md`

**Version:** 1.0.0

---

# Purpose

The Parameter Mining Capability is an Active-Testing-tier capability that discovers the
request parameters an in-scope target accepts within the Robust PenTest Platform (RPP).

It probes candidate parameter names across query, body, header, and cookie locations using
bounded, non-destructive requests, and reports accepted or reflected parameters as
observations and artifacts. It performs delivery only through shared transport and produces no
Findings.

The Parameter Mining Capability drives the [HTTP Client](../../shared/http-client/README.md),
draws candidates from [Wordlists](../wordlists/README.md), gates every request through the
[Policy Engine](../../shared/policy-engine/README.md), and emits
[Observations](../../../schemas/observation.md), [Artifacts](../../../schemas/artifact.md),
and [Metrics](../../../schemas/metrics.md).

---

# Goals

The Parameter Mining Capability SHALL

- Probe candidate parameters across query, body, header, and cookie locations
- Detect accepted, reflected, or behavior-changing parameters as observations
- Consult the [Policy Engine](../../shared/policy-engine/README.md) before every request
- Bound request volume and preserve non-destructive behavior
- Emit [Observations](../../../schemas/observation.md),
  [Artifacts](../../../schemas/artifact.md), and [Metrics](../../../schemas/metrics.md)
- Remain implementation independent
- Produce no Findings or Risk

---

# Non-Goals

The Parameter Mining Capability SHALL NOT

- Issue requests directly rather than through the shared HTTP Client
- Interpret discovered parameters as vulnerabilities or produce Findings or Risk
- Perform destructive or state-changing probing
- Test injection or other weaknesses (those are Web Security and API Security skills)
- Invoke command-line tools or parse their output

Interpretation of discovered parameters belongs to domain skills; weakness testing belongs to
Web Security and API Security skills.

---

# Design Principles

The Parameter Mining Capability SHALL be

- Scope-confined and policy-gated
- Deterministic given the same target behavior and candidate set
- Bounded in request volume
- Non-destructive
- Implementation independent

---

# Architecture

```
Consuming Skill

↓

Parameter Mining Capability

├── Policy Gate            → Policy Engine
├── Candidate Source       → Wordlists
├── Probe Requester        → HTTP Client
├── Acceptance Detector
├── Observation Recorder   → Observation
├── Artifact Emitter       → Artifact
└── Metrics Emitter        → Metrics

↓

Observations · Artifacts · Metrics
```

The Parameter Mining Capability observes acceptance signals and SHALL remain unaware of the
transport implementation.

---

# Responsibilities

The Parameter Mining Capability is responsible for

- Consulting the [Policy Engine](../../shared/policy-engine/README.md) before each request
- Drawing candidate parameter names from [Wordlists](../wordlists/README.md)
- Issuing bounded probes through the [HTTP Client](../../shared/http-client/README.md)
- Detecting acceptance, reflection, or behavior change
- Emitting [Observations](../../../schemas/observation.md),
  [Artifacts](../../../schemas/artifact.md), and [Metrics](../../../schemas/metrics.md)

---

# Inputs

```yaml
target:

locations:

candidate_source:
  wordlist_name:
  max_candidates:

bounds:
  max_requests:

scope_id:

roe_id:
```

`target` SHALL be an in-scope endpoint. `locations` selects query, body, header, or cookie.
`candidate_source` draws candidate names. `bounds` limits request volume.

---

# Outputs

Typical outputs MAY include

- Observations of accepted, reflected, or behavior-changing parameters
- Artifacts capturing probe interactions
- Metrics describing coverage and request counts

Outputs SHALL contain no Findings or Risk.

---

# Policy Enforcement

The Parameter Mining Capability SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) before every request. Probing is an
`active` action permitted only on an `allow` decision and within the attached rate ceiling.
A `requires_approval` decision SHALL defer the action. Probing SHALL be non-destructive and
bounded. Out-of-scope targets SHALL never be probed.

---

# Dependencies

The Parameter Mining Capability depends on

- [HTTP Client](../../shared/http-client/README.md)
- [Wordlists](../wordlists/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Observation Schema](../../../schemas/observation.md)
- [Artifact Schema](../../../schemas/artifact.md)
- [Metrics Schema](../../../schemas/metrics.md)

The Parameter Mining Capability SHALL NOT depend on domain skills.

---

# Consumers

Typical consumers include

- Web Security and API Security skills requiring a parameter surface
- Fuzzing, which targets discovered parameters

---

# Security Principles

The Parameter Mining Capability SHALL

- Act only within scope and Rules of Engagement, enforced by the Policy Engine
- Bound request volume and preserve non-destructive behavior
- Report discovered parameters as data, not findings
- Produce no Findings or Risk
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide an in-scope target and a bounded candidate source
- Rely on the capability for parameter discovery only
- Route interpretation and weakness testing to domain skills
- Capture emitted Observations and Artifacts

---

# Anti-Patterns

Consumers SHOULD NOT

- Issue probes directly
- Bypass the Policy Engine
- Expect vulnerability findings from this capability
- Probe out-of-scope targets

---

# Documentation Requirements

This capability includes

- README.md
- capabilities.md
- interface.md
- configuration.md
- execution.md
- error-model.md
- examples.md
- adr/ADR-001-parameter-mining-capability.md

---

# Related Packages

- [HTTP Client](../../shared/http-client/README.md)
- [Wordlists](../wordlists/README.md)
- [Fuzzing](../fuzzing/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)

---

# Canonical Schemas

- [Observation](../../../schemas/observation.md)
- [Artifact](../../../schemas/artifact.md)
- [Metrics](../../../schemas/metrics.md)

---

# Architecture Decisions

- [ADR-001 — Parameter Mining Capability](adr/ADR-001-parameter-mining-capability.md)

---

# Future Extensions

Future versions MAY support

- Behavior-differential detection tuning
- Context-ranked candidate ordering
- Correlation with Discovery endpoint inventory

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Parameter Mining Capability discovers accepted parameters through bounded,
policy-gated, non-destructive probing and reports them as data, without interpreting them or
producing Findings or Risk.
