# Virtual Host Discovery Skill

**File:** `skills/discovery/virtual-host-discovery/README.md`

**Version:** 1.0.0

---

# Purpose

The Virtual Host Discovery Skill is a Discovery-tier domain skill that identifies
name-based virtual hosts served from a shared in-scope address within the Robust
PenTest Platform (RPP).

It probes candidate host names against a target address and distinguishes distinct
virtual hosts from a default response, producing canonical `web-application`
[Assets](../../../schemas/asset.md), `serves`
[Asset Relationships](../../../schemas/asset-relationship.md),
[Observations](../../../schemas/observation.md), and, where a weakness is
identified, [Findings](../../../schemas/finding.md) with associated
[Risk](../../../schemas/risk.md).

Unlike the [HTTP Client](../../shared/http-client/README.md) shared skill, which
performs requests, this skill *interprets* differential responses to reveal hidden
virtual hosts. It consumes shared infrastructure and SHALL NOT invoke
virtual-host tools directly.

---

# Goals

The Virtual Host Discovery Skill SHALL

- Probe candidate host names against an in-scope address
- Distinguish distinct virtual hosts from the default response
- Produce canonical `web-application` Assets and `serves` relationships
- Emit Observations and Evidence for every probe
- Identify hidden or internal virtual hosts as Findings with Risk
- Consult the [Policy Engine](../../shared/policy-engine/README.md) before every
  probe
- Remain tool independent

---

# Non-Goals

The Virtual Host Discovery Skill SHALL NOT

- Perform HTTP input or output directly
- Enumerate content within a discovered host (that is Content Discovery)
- Exploit discovered hosts
- Act on out-of-scope addresses or host names
- Invoke virtual-host enumeration command-line tools or parse their output

HTTP transport belongs to the [HTTP Client](../../shared/http-client/README.md);
content enumeration belongs to the
[Content Discovery](../content-discovery/README.md) skill; exploitation is out of
scope for Discovery.

---

# Design Principles

The Virtual Host Discovery Skill SHALL be

- Scope-confined and policy-gated
- Evidence-backed for every produced Asset and Finding
- Deterministic given the same inputs and responses
- Differential, comparing candidate responses to a baseline
- Bounded in candidate volume and request rate
- Tool independent

---

# Architecture

```
Recon Agent

↓

Virtual Host Discovery Skill

├── Policy Gate            → Policy Engine
├── Baseline Establisher   → HTTP Client
├── Host Prober            → HTTP Client
├── Differential Analyzer
├── Asset Builder
├── Weakness Analyzer
├── Evidence Recorder      → Evidence
└── Finding Emitter

↓

Assets · Relationships · Observations · Evidence · Findings · Risk
```

The skill orchestrates the HTTP Client to interpret differential responses. It
SHALL remain unaware of any HTTP implementation.

---

# Responsibilities

The Virtual Host Discovery Skill is responsible for

- Consulting the [Policy Engine](../../shared/policy-engine/README.md) before each
  probe
- Establishing a baseline response for the target address
- Probing candidate host names through the
  [HTTP Client](../../shared/http-client/README.md)
- Analyzing responses differentially to distinguish distinct virtual hosts
- Building `web-application` [Assets](../../../schemas/asset.md) and `serves`
  relationships to the address
- Recording [Observations](../../../schemas/observation.md) and promoting them to
  [Evidence](../../../schemas/evidence.md)
- Emitting [Findings](../../../schemas/finding.md) and
  [Risk](../../../schemas/risk.md) for hidden-host exposure

---

# Discovery Lifecycle

```
Receive Target Address

↓

Consult Policy Engine (per probe)

↓

Establish Baseline Response (HTTP Client)

↓

Probe Candidate Host Names (HTTP Client)

↓

Analyze Differentially

↓

Record Observations → Evidence

↓

Build Virtual Host Assets

↓

Analyze For Hidden-Host Exposure

↓

Emit Findings and Risk (where applicable)
```

Every produced object SHALL be traceable to evidence.

---

# Inputs

The skill accepts

```yaml
target_address:

host_candidates_ref:

base_scheme:

scope_id:

roe_id:
```

`target_address` SHALL be an in-scope address or host serving one or more virtual
hosts.

`host_candidates_ref` SHALL reference a curated host-name candidate list, such as
discovered subdomains.

`base_scheme` SHALL declare `http`, `https`, or both.

`scope_id` and `roe_id` reference the assessment
[Scope](../../../schemas/scope.md) and
[Rules of Engagement](../../../schemas/rules-of-engagement.md).

---

# Produced Assets

The skill SHALL produce canonical `web-application`
[Assets](../../../schemas/asset.md) for distinct virtual hosts and `serves`
[Asset Relationships](../../../schemas/asset-relationship.md) linking each virtual
host to the address that serves it.

Each Asset SHALL carry provenance and a `scope_status` set from the assessment
Scope.

---

# Produced Findings

The skill MAY produce [Findings](../../../schemas/finding.md), each with
[Risk](../../../schemas/risk.md), for exposure such as

- Hidden or internal virtual hosts reachable on a public address
- Staging or administrative virtual hosts served alongside production

Every Finding SHALL reference supporting [Evidence](../../../schemas/evidence.md).

---

# Policy Enforcement

The Virtual Host Discovery Skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) before every probe. Host
probing is an `active` action; it SHALL proceed only on an `allow` decision and
within the attached rate ceiling. Candidate host names or addresses that are
out-of-scope SHALL never be probed.

---

# Dependencies

The Virtual Host Discovery Skill depends on

- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Asset Schema](../../../schemas/asset.md)
- [Asset Relationship Schema](../../../schemas/asset-relationship.md)
- [Observation Schema](../../../schemas/observation.md)
- [Finding Schema](../../../schemas/finding.md)
- [Risk Schema](../../../schemas/risk.md)

The Virtual Host Discovery Skill SHALL NOT depend on other domain skills.

---

# Consumers

Typical consumers include

- The Recon Agent and recon workflows
- The Content Discovery and Fingerprinting skills
- Reporting, through the produced Findings and Risk

---

# Outputs

Typical outputs MAY include

- Virtual host `web-application` Assets and `serves` relationships
- Observations and Evidence references
- Findings with Risk for hidden-host exposure

Outputs SHALL remain implementation independent.

---

# Security Principles

The Virtual Host Discovery Skill SHALL

- Act only within scope and Rules of Engagement, enforced by the Policy Engine
- Bound candidate volume and request rate
- Produce no Finding without supporting Evidence
- Report hidden-host exposure as data; exploitation is out of scope
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide an in-scope address and a curated candidate list, such as discovered
  subdomains
- Rely on the skill for differential analysis
- Treat discovered virtual hosts as inputs to Content Discovery and Fingerprinting
- Capture the produced Evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Issue HTTP requests directly
- Bypass the Policy Engine
- Probe unbounded candidate lists
- Act on out-of-scope addresses or host names

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
- adr/ADR-001-virtual-host-discovery-skill.md

---

# Related Packages

- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Content Discovery](../content-discovery/README.md)

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

- [ADR-001 — Virtual Host Discovery Skill](adr/ADR-001-virtual-host-discovery-skill.md)

---

# Future Extensions

Future versions MAY support

- Response-similarity clustering to reduce false positives
- TLS SNI-based virtual host correlation
- Wildcard-response detection and filtering

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Virtual Host Discovery Skill produces a canonical, evidence-backed set
of virtual host `web-application` Assets and hidden-host Findings, while acting
strictly within scope and Rules of Engagement through the Policy Engine, without
invoking virtual-host tools directly.
