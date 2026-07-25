# Port Discovery Skill

**File:** `skills/discovery/port-discovery/README.md`

**Version:** 1.0.0

---

# Purpose

The Port Discovery Skill is a Discovery-tier domain skill that identifies the
reachable network services exposed by an assessment target within the Robust
PenTest Platform (RPP).

It probes TCP and UDP ports on in-scope hosts, determines port state, and
produces canonical [Assets](../../../schemas/asset.md) of types `port` and
`service`, [Asset Relationships](../../../schemas/asset-relationship.md) such as
`exposes`, [Observations](../../../schemas/observation.md), and, where a weakness
is identified, [Findings](../../../schemas/finding.md) with associated
[Risk](../../../schemas/risk.md).

Unlike the [TCP Client](../../shared/tcp-client/README.md) and
[UDP Client](../../shared/udp-client/README.md) shared skills, which perform the
transport, this skill *interprets* connectivity results to map the network attack
surface. It consumes shared infrastructure and SHALL NOT invoke port-scanning
tools directly.

---

# Goals

The Port Discovery Skill SHALL

- Probe TCP and UDP ports on in-scope hosts
- Determine port state such as open, closed, or filtered
- Produce canonical `port` and `service` Assets and `exposes` relationships
- Emit Observations and Evidence for every probe
- Identify exposure-related weaknesses as Findings with Risk
- Consult the [Policy Engine](../../shared/policy-engine/README.md) before every
  probe
- Remain tool independent

---

# Non-Goals

The Port Discovery Skill SHALL NOT

- Perform raw socket input or output directly
- Fingerprint service software in depth (that is the Fingerprinting skill)
- Exploit exposed services
- Act on out-of-scope hosts
- Invoke port-scanning command-line tools or parse their output

Transport belongs to the [TCP Client](../../shared/tcp-client/README.md) and
[UDP Client](../../shared/udp-client/README.md); deep service fingerprinting
belongs to a dedicated Fingerprinting skill; exploitation is out of scope for
Discovery.

---

# Design Principles

The Port Discovery Skill SHALL be

- Scope-confined and policy-gated
- Evidence-backed for every produced Asset and Finding
- Deterministic given the same inputs and connectivity results
- Confidence-graded
- Bounded in port range and probe rate
- Tool independent

---

# Architecture

```
Recon Agent

↓

Port Discovery Skill

├── Policy Gate            → Policy Engine
├── TCP Prober             → TCP Client
├── UDP Prober             → UDP Client
├── State Classifier
├── Asset Builder
├── Weakness Analyzer
├── Evidence Recorder      → Evidence
└── Finding Emitter

↓

Assets · Relationships · Observations · Evidence · Findings · Risk
```

The skill orchestrates shared transport to interpret connectivity. It SHALL
remain unaware of any socket implementation.

---

# Responsibilities

The Port Discovery Skill is responsible for

- Consulting the [Policy Engine](../../shared/policy-engine/README.md) before each
  probe
- Probing ports through the [TCP Client](../../shared/tcp-client/README.md) and
  [UDP Client](../../shared/udp-client/README.md)
- Classifying port state from connectivity results
- Building `port` and `service` [Assets](../../../schemas/asset.md) and `exposes`
  [Asset Relationships](../../../schemas/asset-relationship.md)
- Recording [Observations](../../../schemas/observation.md) and promoting them to
  [Evidence](../../../schemas/evidence.md)
- Emitting [Findings](../../../schemas/finding.md) and
  [Risk](../../../schemas/risk.md) for exposure weaknesses

---

# Discovery Lifecycle

```
Receive Host Target

↓

Consult Policy Engine (per probe)

↓

Probe Ports (TCP / UDP Client)

↓

Classify Port State

↓

Record Observations → Evidence

↓

Build Port and Service Assets

↓

Analyze For Exposure Weaknesses

↓

Emit Findings and Risk (where applicable)
```

Every produced object SHALL be traceable to evidence.

---

# Inputs

The skill accepts

```yaml
target:

ports:

protocols:

scope_id:

roe_id:
```

`target` SHALL be an in-scope host or address.

`ports` SHALL declare the port set or ranges to probe.

`protocols` SHALL declare `tcp`, `udp`, or both.

`scope_id` and `roe_id` reference the assessment
[Scope](../../../schemas/scope.md) and
[Rules of Engagement](../../../schemas/rules-of-engagement.md).

---

# Produced Assets

The skill SHALL produce canonical [Assets](../../../schemas/asset.md) of types

- `port`
- `service`

and `exposes` and `serves`
[Asset Relationships](../../../schemas/asset-relationship.md) linking a host to
its ports and services.

Each Asset SHALL carry provenance and a `scope_status` set from the assessment
Scope.

---

# Produced Findings

The skill MAY produce [Findings](../../../schemas/finding.md), each with
[Risk](../../../schemas/risk.md), for exposure weaknesses such as

- Unexpected or administrative services exposed to untrusted networks
- Plaintext services observed where encryption is expected
- Services exposed outside a documented baseline

Every Finding SHALL reference supporting [Evidence](../../../schemas/evidence.md).

---

# Policy Enforcement

The Port Discovery Skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) before every probe. Port
probing is an `active` action; it SHALL proceed only on an `allow` decision and
within the attached rate ceiling. Probes outside a required maintenance window or
against out-of-scope hosts SHALL be denied.

---

# Dependencies

The Port Discovery Skill depends on

- [TCP Client](../../shared/tcp-client/README.md)
- [UDP Client](../../shared/udp-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Asset Schema](../../../schemas/asset.md)
- [Asset Relationship Schema](../../../schemas/asset-relationship.md)
- [Observation Schema](../../../schemas/observation.md)
- [Finding Schema](../../../schemas/finding.md)
- [Risk Schema](../../../schemas/risk.md)

The Port Discovery Skill SHALL NOT depend on other domain skills.

---

# Consumers

Typical consumers include

- The Recon Agent and recon workflows
- The Fingerprinting and TLS Analysis skills, which build on service Assets
- Reporting, through the produced Findings and Risk

---

# Outputs

Typical outputs MAY include

- Port and service Assets
- Asset Relationships forming the network portion of the asset graph
- Observations and Evidence references
- Findings with Risk for exposure weaknesses

Outputs SHALL remain implementation independent.

---

# Security Principles

The Port Discovery Skill SHALL

- Act only within scope and Rules of Engagement, enforced by the Policy Engine
- Bound port ranges and probe rate to avoid target disruption
- Produce no Finding without supporting Evidence
- Report exposure as data; exploitation is out of scope
- Preserve auditability

Aggressive scanning can disrupt targets. The skill SHALL respect the rate ceiling
and maintenance windows enforced by the Policy Engine and Rate Limiter.

---

# Best Practices

Consumers SHOULD

- Provide an explicit, in-scope host and bounded port set
- Rely on the skill for Asset and Relationship construction
- Treat produced service Assets as inputs to Fingerprinting and TLS Analysis
- Capture the produced Evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Open sockets directly
- Bypass the Policy Engine
- Probe unbounded port ranges without rate governance
- Act on out-of-scope hosts

---

# Documentation Requirements

This skill includes

- README.md
- capabilities.md
- interface.md
- configuration.md
- execution.md
- error-model.md
- examples.md
- adr/ADR-001-port-discovery-skill.md

---

# Related Packages

- [TCP Client](../../shared/tcp-client/README.md)
- [UDP Client](../../shared/udp-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)

---

# Canonical Schemas

- [Asset](../../../schemas/asset.md)
- [Asset Relationship](../../../schemas/asset-relationship.md)
- [Observation](../../../schemas/observation.md)
- [Evidence](../../../schemas/evidence.md)
- [Finding](../../../schemas/finding.md)
- [Risk](../../../schemas/risk.md)

---

# Architecture Decisions

- [ADR-001 — Port Discovery Skill](adr/ADR-001-port-discovery-skill.md)

---

# Future Extensions

Future versions MAY support

- Adaptive timing based on target responsiveness
- Service-version hinting handed to Fingerprinting
- IPv6 sweep support within scope
- Rate-adaptive probe scheduling

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Port Discovery Skill produces a canonical, evidence-backed map of
reachable services — `port` and `service` Assets, `exposes` relationships, and
exposure Findings — while acting strictly within scope and Rules of Engagement
through the Policy Engine, without invoking port-scanning tools directly.
